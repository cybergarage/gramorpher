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
from .grammar import Grammar
from .corpus import Corpus
from anytree import RenderTree

class Generator:
    def __init__(self, corpus = Corpus()):
        self.grammar = Grammar()
        self.corpus = corpus

    def parse_grammar_file(self, file_name):
        return self.grammar.parse_file(file_name)

    def parse_corpus_file(self, file_name):
        return self.corpus.parse_file(file_name)

    def find_rule(self, name):
        return self.grammar.find_rule(name)

    def generate(self, name):
        rule = Generator.Rule(self.find_rule(name))
        while True:
            rule.print()
            # Confirms all leaf nodes can get the symbols to genarete test cases
            all_leaf_node_has_symbols = True
            for _, _, node in RenderTree(rule):
                #print('%s %s %s' % (node.name, node.is_leaf(), node.is_terminal()))
                if not node.is_leaf():
                    continue
                if node.is_terminal():
                    continue
                symbol_name = node.name
                if not self.corpus.has_symbol(symbol_name):
                    all_leaf_node_has_symbols = False
            if all_leaf_node_has_symbols:
                return rule

            # Expands only a grammar node
            all_nodes_are_expanded = True
            for _, _, node in RenderTree(rule):
                if node.has_children():
                    continue
                if node.has_elements():
                    node.add_children(node.elements(True))
                    all_nodes_are_expanded = False
                    break

            # Breaks the loop to raise a generation error when all nodes are expanded and any leaf nodes not has symbols
            if all_nodes_are_expanded:
                break
        #raise Generator.Error('Rule (%s) has no all symbols' % name)
        return rule

    class Rule(Grammar.Rule):
        def __init__(self, rule):
            super().__init__(rule.root, rule.node, rule.parent)

    class Error(Exception):
        def __init__(self, msg):
            self.message = msg
