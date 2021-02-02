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
import csv
from io import StringIO

class SymbolCase(dict):
    def __init__(self):
        pass

    def add_case(self, name, v):
        self[name] = v

class SymbolCases(list):
    def __init__(self):
        super().__init__()

    def add_case(self, s):
        self.append(s)

class Symbols(SymbolCases):
    def __init__(self):
        super().__init__()
        self.names = []
        self.cases = SymbolCases()

class PictSymbols(Symbols):
    def __init__(self):
        super().__init__()

    def parse_file(self, file_name):
        obj = open(file_name, newline='')
        return self._parse_object(obj)

    def parse_string(self, str):
        obj = StringIO(str)
        return self._parse_object(obj)

    def _parse_object(self, obj):
        reader = csv.reader(obj, delimiter='\t')
        self.names = next(reader)
        name_cnt = len(self.names)
        for row in reader:
            sc = SymbolCase()
            for n in range(name_cnt):
                sc.add_case(self.names[n], row[n])
            self.cases.add_case(sc)
        obj.close()
        return True
