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
from .antlr import ANTLRv4Parser
from .element import Element

class Rule:
    def __init__(self, node:ANTLRv4Parser.ParserRuleSpecContext):
        self.node = node

    def name(self):
        return self.node.RULE_REF().getText()

    def elements(self):
        elements = []
        for labeled_alt in self.node.ruleBlock().ruleAltList().labeledAlt():
            for element in labeled_alt.alternative().element():
                elements.append(Element(element))
        return elements

    def find(self, name):
        for elem in self.elements():
            if elem.name() == name:
                return elem
        return None

    def __str__(self):
        desc = ''
        for elem in self.elements():
            desc += elem.name() + ' '
        return desc
