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
from anytree import Node, RenderTree

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

    def find_rule(self, name):
        for rule in self.rules():
            if rule.symbol() == name:
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

    class Context(Node):
        def __init__(self, root, node, parent=None):
            self.grammar = root
            self.node = node
            self.rep = ""
            super().__init__(self.symbol(), parent)

        def __str__(self):
            name = self.symbol()
            print(name + "(" + str(type(self.node)) + ")")
            if self.is_terminal() or self.is_lexerrulespeccontext():
                return name
            rule = self.find_rule(name)
            assert(rule)
            elems = rule.elements()
            assert(0 < len(elems))
            if len(elems) <= 1:
                if elems[0].is_lexerrulespeccontext():
                    return elems[0].symbol()
                return str(elems[0])
            desc = ""
            for elem in elems:
                if 0 < len(desc):
                    desc += ' | ' 
                desc += str(elem)
            desc = '(' + desc + ')'
            return desc

        def set_repetition(self, rep):
            self.rep = rep

        def repetition(self):
            return self.rep

        def find_rule(self, name):
            return self.grammar.find_rule(name)

        def elements(self):
            return []

        def symbol(self):
            if self.is_rulespeccontext():
                return self.node.RULE_REF().getText()
            return self.node.getText()

        def is_rulespeccontext(self):
            return isinstance(self.node, ANTLRv4Parser.ParserRuleSpecContext)

        def is_lexerrulespeccontext(self):
            return isinstance(self.node, ANTLRv4Parser.LexerRuleSpecContext)

        def is_terminal(self):
            if isinstance(self.node, ANTLRv4Parser.TerminalContext):
                return True
            return False

        def add_child(self, ctx):
            children = list(self.children)
            children.append(ctx)
            self.children = children

        def tree(self):
            name = self.symbol()
            rule = self.find_rule(name)
            assert(rule)
            elems = rule.elements()
            for elem in elems:
                if elem.is_rulespeccontext():
                    for celem in elem.elements():
                        elem.add_child(celem)
                self.add_child(elem)
            return self

        def print(self):
            for pre, fill, node in RenderTree(self.tree()):
                print("%s%s" % (pre, node.name))

    class RuleContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.ParserRuleSpecContext):
            super().__init__(root, node)

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
                if elem.symbol() == name:
                    return elem
            return None

    class ElementContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.ElementContext):
            super().__init__(root, node)

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
            super().__init__(root, node)

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
            super().__init__(root, node)

        def element(self):
            term = self.node.terminal()
            if term:
                return Grammar.Element(self.root, term)
            rule_ref = self.node.ruleref()
            if rule_ref:
                rule_name = rule_ref.RULE_REF().getText()
                rule = self.find_rule(rule_name)
                if rule:
                   return Grammar.Rule(self.root, rule.node) 
            return None

    class BlockContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.BlockContext, suffix:ANTLRv4Parser.BlockSuffixContext = None):
            super().__init__(root, node)
            self.suffix = suffix

        def elements(self):
            elems = []
            for alt in self.node.altList().alternative():
                for alt_elem in alt.element():
                    elem_ctx = Grammar.ElementContext(self.root, alt_elem)
                    elem_elems = elem_ctx.elements()
                    elems.extend(elem_elems)
            return elems

    class Rule(RuleContext):
        def __init__(self, root, node:ANTLRv4Parser.ParserRuleSpecContext, parent=None):
            super().__init__(root, node)

        def symbols(self):
            symbols = self.elements()

            while True:
                has_rule_elements = False
                for symbol in symbols:
                    if symbol.is_rulespeccontext() and not symbol.is_terminal():
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

    class Element(Context):
        def __init__(self, root, node:ParserRuleContext):
            super().__init__(root, node)
