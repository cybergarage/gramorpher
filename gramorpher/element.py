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

class Element:
    def __init__(self, node:ANTLRv4Parser.ElementContext):
        self.node = node

    def __str__(self):
        desc = self.name()
        if self.is_atom():
            desc += '(A)'
        return desc

    def name(self):
        return self.node.getText()

    def is_labeled(self):
        return True if self.node.labeledElement() else False

    def is_atom(self):
        if self.node.atom():
            return True
        labeled_elem = self.node.labeledElement()
        if labeled_elem:
            if labeled_elem.atom():
                return True
        return False

    def atom(self):
        atom = self.node.atom()
        if atom:
            return atom
        labeled_elem = self.node.labeledElement()
        if labeled_elem:
            atom = labeled_elem.atom()
        if atom:
            return atom
        return None

    def is_action(self):
        return True if self.node.actionBlock() else False
