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
from gramorpher import symbols
import os
import sys
from enum import Enum
from antlr4 import InputStream, FileStream, CommonTokenStream, ParserRuleContext
from .antlr import ANTLRv4Parser, ANTLRv4Lexer
from anytree import NodeMixin, RenderTree

class Grammar:
    def __init__(self):
        self.root = None

    def parse_file(self, file_name):
        stream = FileStream(file_name, encoding="utf-8")
        return self._parse_stream(stream)

    def parse_string(self, string):
        stream = InputStream(string)
        return self._parse_stream(stream)

    def _parse_stream(self, stream):
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
        raise Grammar.Error('Rule (%s) is not found' % name)

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

    class BaseContext(object):
        def __init__(self, root, node):
            self.grammar = root
            self.node = node
            self.rep = None

        def has_repetition(self):
            if self.rep is not None:
                return True
            return False

        def set_repetition(self, rep):
            self.rep = rep

        def repetition(self):
            return self.rep

        def find_rule(self, name):
            return self.grammar.find_rule(name)

        def elements(self, only_direct_elements = False):
            return []

        def has_elements(self):
            elements = self.elements(True)
            if len(elements) <= 0:
                return False
            return True

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

        def is_blockcontext(self):
            return isinstance(self.node, ANTLRv4Parser.BlockContext)


    class Context(BaseContext, NodeMixin):
        def __init__(self, root, node, parent = None, children = None):
            super(Grammar.Context, self).__init__(root, node)
            self.name = self.symbol()
            self.parent = parent
            if children:
                self.children = children

        def __str__(self):
            desc = ''
            for pre, _, node in RenderTree(self.tree()):
                #desc += "%s%s (%d)" % (pre, node.name, node.depth)
                desc += "%s%s" % (pre, node.name)
                if node.has_repetition():
                    desc += " %s" % node.rep
                #desc += " (%d:%s)" % (node.depth, str(type(self.node)))
                desc += "\n"
            return desc

        def _add_child_element(self, elem):
            children = list(self.children)
            children.append(elem)
            self.children = children

        def _add_child_recursive(self, elem, depth, max_depth):
            if (0 < max_depth) and (max_depth <= depth):
                return
            self._add_child_element(elem)
            if elem.is_recursive_definition():
                return
            if elem.is_rulespeccontext():
                for elem_child in elem.elements():
                    elem._add_child_recursive(elem_child, (depth+1), max_depth)

        def add_child(self, elem, is_recursive = False):
            if not is_recursive:
                self._add_child_element(elem)
                return
            self._add_child_recursive(elem, 0, 30)

        def add_children(self, elems, is_recursive = False):
            for elem in elems:
                self.add_child(elem, is_recursive)

        def has_children(self):
            if len(self.children) <= 0:
                return False
            return True

        def is_recursive_definition(self):
            parent_node = self.parent
            while parent_node:
                if self.symbol() == parent_node.symbol():
                    return True
                parent_node = parent_node.parent
            return False

        def tree(self):
            name = self.symbol()
            rule = self.find_rule(name)
            assert(rule)
            elems = rule.elements()
            self.add_children(elems)
            return self

        def print(self):
            print(str(self))

    class RuleContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.ParserRuleSpecContext):
            super().__init__(root, node)

        def elements(self, only_direct_elements = False):
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

        def elements(self, only_direct_elements = False):
            #node_str = self.node.getText()
            #print(node_str)
            if self.node.actionBlock():
                return []
            if self.node.labeledElement():
                labeled_elem = Grammar.LabeledElementContext(self.root, self.node.labeledElement())
                return labeled_elem.elements()
            if self.node.atom():
                atom = Grammar.AtomContext(self.root, self.node.atom())
                elem = atom.element()
                if self.node.ebnfSuffix():
                    elem.set_repetition(self.node.ebnfSuffix().getText())
                return [elem]
            if self.node.ebnf():
                block = Grammar.BlockContext(self.root, self.node.ebnf().block(), self.node.ebnf().blockSuffix())
                if not only_direct_elements:
                    block.add_children(block.elements())
                return [block]
            return []

    class LabeledElementContext(Context):
        def __init__(self, root, node:ANTLRv4Parser.LabeledElementContext):
            super().__init__(root, node)

        def elements(self, only_direct_elements = False):
            if self.node.atom():
                atom = Grammar.AtomContext(self.root, self.node.atom())
                return [atom.element()]
            if self.node.block():
                block = Grammar.BlockContext(self.root, self.node.ebnf().block(), self.node.ebnf().blockSuffix())
                if not only_direct_elements:
                    block.add_children(block.elements())
                return [block]
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
            if suffix is not None:
                self.set_repetition(suffix.getText())

        def elements(self, only_direct_elements = False):
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
            symbol_names = {}
            for _, _, node in RenderTree(self):
                if node is self:
                    continue
                if node.is_blockcontext():
                    continue
                if node.is_terminal():
                    continue
                symbol_names[node.symbol()] = 1
            return symbol_names.keys()

    class Element(Context):
        def __init__(self, root, node:ParserRuleContext):
            super().__init__(root, node)
