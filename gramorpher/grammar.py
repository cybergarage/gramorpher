# Copyright (C) 2020 Yahoo Japan Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import os
import sys
from enum import Enum
from antlr4 import InputStream, FileStream, CommonTokenStream, ParserRuleContext
from .antlr import ANTLRv4Parser, ANTLRv4Lexer

class Grammar:
    def __init__(self):
        self.root = None

    def parse_file(self, file_name):
        stream = FileStream(file_name, encoding="utf-8")
        return self.parse(stream)

    def parse_string(self, string):
        stream = InputStream(string)
        return self.parse(stream)

    def parse(self, stream):
        lexer = ANTLRv4Lexer(stream)
        parser = ANTLRv4Parser(CommonTokenStream(lexer))
        self.root = parser.grammarSpec()
        assert isinstance(self.root, ANTLRv4Parser.GrammarSpecContext)
        return True

    def rules(self):
        rules = []
        for rule in self.root.rules().ruleSpec():
            if rule.parserRuleSpec():
                rule_spec = rule.parserRuleSpec()
                rules.append(Grammar.Rule(self, rule_spec))
        return rules

    def find(self, name):
        for rule in self.rules():
            if rule.name() == name:
                return rule
        return None

    def print(self):
        self._print_node(self.root)

    def _print_node(self, node):
        for rule in node.rules().ruleSpec():
            print(rule)

    class Error(Exception):
        def __init__(self, msg):
            self.message = msg

    class Repetition(Enum):
        NONE = 0
        QUESTION = 2
        STAR = 3
        PLUS = 4

    class Context:
        def __init__(self, root):
            self.root = root
            self.node = None

        def find(self, name):
            return self.root.find(name)

        def elements(self):
            return []

        def is_terminal(self):
            return True if len(self.elements()) == 0 else False

    class RuleContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.ParserRuleSpecContext):
            self.root = root
            self.node = node

        def __str__(self):
            desc = ''
            for elem in self.elements():
                desc += elem.name() + ' '
                desc += '[' + type(self).__name__ + "/" + type(self.node).__name__ + '] '
            return desc

        def name(self):
            return self.node.RULE_REF().getText()

        def elements(self):
            elems = []
            for labeled_alt in self.node.ruleBlock().ruleAltList().labeledAlt():
                for atl_elem in labeled_alt.alternative().element():
                    elem_ctx = Grammar.ElementContext(self.root, atl_elem)
                    elem_elems = elem_ctx.elements()
                    if not elem_elems:
                        continue
                    elems.extend(elem_elems)
            return elems

        def find(self, name):
            for elem in self.elements():
                if elem.name() == name:
                    return elem
            return None

        def print(self):
            for elem in self.elements():
                print(str(elem))

    class ElementContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.ElementContext):
            self.root = root
            self.node = node

        def elements(self):
            if self.node.actionBlock():
                return []
            if self.node.labeledElement():
                labeled_elem = Grammar.LabeledElementContext(self.root, self.node.labeledElement())
                elems = labeled_elem.elements()
                # TODO: Set repetition suffix all elements
                # if self.node.ebnfSuffix():
                #     elem.set_repetition(self.node.ebnfSuffix().getText())
                return elems
            if self.node.atom():
                atom = Grammar.AtomContext(self.root, self.node.atom())
                elem = atom.element()
                if self.node.ebnfSuffix():
                    elem.set_repetition(self.node.ebnfSuffix().getText())
                return [elem]
            if self.node.ebnf():
                block = Grammar.BlockContext(self.root, self.node.ebnf().block(), self.node.ebnf().blockSuffix())
                return block.elements()
            return []

    class LabeledElementContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.LabeledElementContext):
            self.root = root
            self.node = node

        def elements(self):
            if self.node.atom():
                atom = Grammar.AtomContext(self.root, self.node.atom())
                return [atom.element()]
            if self.node.block():
                block = Grammar.BlockContext(self.root, self.node.ebnf().block())
                return block.elements()
            return None

    class AtomContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.AtomContext):
            self.root = root
            self.node = node

        def element(self):
            term = self.node.terminal()
            if term:
                return Grammar.Element(term)
            rule_ref = self.node.ruleref()
            if rule_ref:
                rule_name = rule_ref.RULE_REF().getText()
                rule = self.find(rule_name)
                if rule:
                   return Grammar.Rule(self.root, rule.node) 
            return None

    class BlockContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.BlockContext, suffix:ANTLRv4Parser.BlockSuffixContext = None):
            self.root = root
            self.node = node
            self.suffix = suffix

        def elements(self):
            elems = []
            for alt in self.node.altList().alternative():
                for alt_elem in alt.element():
                    elem_ctx = Grammar.ElementContext(self.root, alt_elem)
                    elem_elems = elem_ctx.elements()
                    elems.extend(elem_elems)
            return elems

    class Symbol:
        def __init__(self):
            self.rep = ""

        def set_repetition(self, rep):
            self.rep = rep

        def repetition(self):
            return self.rep

        def is_rulespeccontext(self):
            return isinstance(self.node, ANTLRv4Parser.ParserRuleSpecContext)

    class Rule(RuleContext, Symbol):
        def __init__(self, root, node:ANTLRv4Parser.ParserRuleSpecContext):
            self.root = root
            self.node = node

        def symbols(self):
            symbols = self.elements()

            while True:
                self._print_symbols(symbols)
                has_rule_elements = False
                for symbol in symbols:
                    if symbol.is_rulespeccontext():
                        has_rule_elements = True
                        break
                if not has_rule_elements:
                    break
                expanded_symbols = []
                while 0 < len(symbols):
                    symbol = symbols.pop(0)
                    if symbol.is_rulespeccontext():
                        expanded_symbols.extend(symbol.elements())
                    else:
                        expanded_symbols.append(symbol)
                symbols = expanded_symbols

            return symbols

        def print(self):
            self._print_symbols(self.symbols())

        def _print_symbols(self, symbols):
            for elem in symbols:
                print(str(elem))

    class Element(Symbol):
        def __init__(self, node:ParserRuleContext, rep=""):
            self.node = node
            self.rep = rep

        def __str__(self):
            desc = self.name()
            if 0 < len(self.rep):
                desc += ' (' + self.rep + ')'
            desc += ' [' + type(self).__name__ + "/" + type(self.node).__name__ + ']'
            return desc

        def set_repetition(self, rep):
            self.rep = rep

        def name(self):
            return self.node.getText()

        def repetition(self):
            return self.rep
