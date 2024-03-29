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
from .symbols import SymbolCases

class Corpus:
    def __init__(self):
        super().__init__()
        self.names = []
        self.cases = SymbolCases()

    def add_case(self, s):
        self.cases.append(s)

    def parse_file(self, file_name):
        return False

    def has_symbol(self, name):
        return False

    def has_symbols(self, names):
        for name in names:
            if not self.has_symbol(name):
                return False
        return True
