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
                rules.append(Grammar.RuleContext(self, rule_spec))
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

        def find(self, name):
            return self.root.find(name)

    class RuleContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.ParserRuleSpecContext):
            self.root = root
            self.node = node

        def __str__(self):
            desc = ''
            for elem in self.elements():
                desc += elem.name() + ' '
            return desc

        def name(self):
            return self.node.RULE_REF().getText()

        def elements(self):
            elems = []
            for labeled_alt in self.node.ruleBlock().ruleAltList().labeledAlt():
                for atl_elem in labeled_alt.alternative().element():
                    elem_ctx = Grammar.ElementContext(self.root, atl_elem)
                    elem = elem_ctx.element()
                    if not elem:
                        continue
                    elems.append(elem)
            return elems

        def find(self, name):
            for elem in self.elements():
                if elem.name() == name:
                    return elem
            return None

        def print(self):
            for elem in self.elements():
                print(str(elem))

    class Element:
        def __init__(self, node:ParserRuleContext, rep=""):
            self.node = node
            self.rep = rep
        def __str__(self):
            desc = self.name()
            if 0 < len(self.rep):
                desc += ' (' + self.rep + ')'
            return desc

        def set_repetition(self, rep):
            self.rep = rep

        def name(self):
            return self.node.getText()

        def repetition(self):
            return self.rep

    class ElementContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.ElementContext):
            self.root = root
            self.node = node

        def element(self):
            if self.node.actionBlock():
                return None
            if self.node.labeledElement():
                labeled_elem = Grammar.LabeledElementContext(self.root, self.node.labeledElement())
                elem = labeled_elem.element()
                if self.node.ebnfSuffix():
                    elem.set_repetition(self.node.ebnfSuffix().getText())
                return elem
            if self.node.atom():
                atom = Grammar.AtomContext(self.root, self.node.atom())
                elem = atom.element()
                if self.node.ebnfSuffix():
                    elem.set_repetition(self.node.ebnfSuffix().getText())
                return elem
            if self.node.ebnf():
                block = Grammar.BlockContext(self.root, self.node.ebnf().block(), self.node.ebnf().blockSuffix())
                return block.element()
            return None

    class LabeledElementContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.LabeledElementContext):
            self.root = root
            self.node = node

        def element(self):
            if self.node.atom():
                atom = Grammar.AtomContext(self.root, self.node.atom())
                return atom.element()
            if self.node.block():
                block = Grammar.BlockContext(self.root, self.node.ebnf().block())
                return block.element()
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
                print("ERROR" + rule_ref.RULE_REF().getText())
            return None

    class BlockContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.BlockContext, suffix:ANTLRv4Parser.BlockSuffixContext = None):
            self.root = root
            self.node = node
            self.suffix = suffix

        def element(self):
            block = self.node.altList()
            elem = Grammar.Element(block)
            if self.suffix:
                elem.set_repetition(self.suffix.getText())
            return elem
