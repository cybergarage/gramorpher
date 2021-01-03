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
from antlr4 import InputStream, FileStream, CommonTokenStream
from .antlr import ANTLRv4Parser, ANTLRv4Lexer

class Parser:
    def __init__(self):
        pass

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
        return self._parse_node(self.root)

    def _parse_node(self, node):
        assert isinstance(node, ANTLRv4Parser.GrammarSpecContext)
        for rule in node.rules().ruleSpec():
            if rule.parserRuleSpec():
                rule_spec = rule.parserRuleSpec()
                rule_name = rule_spec.RULE_REF().getText()
                print(rule_name)
                # for child in rule_spec.getChildren():
                #     self._parse_node(child)
        return True

    def print(self):
        self._print_node(self.root)

    def _print_node(self, node):
        for rule in node.rules().ruleSpec():
            print(rule)
