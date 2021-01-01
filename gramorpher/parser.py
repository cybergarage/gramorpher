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
from io import StringIO
from antlr4 import FileStream, CommonTokenStream
from .antlr import ANTLRv4Parser, ANTLRv4Lexer

class Parser:
    def __init__(self):
        pass

    def parse(self, file):
        return self.parse_stream(FileStream(file, encoding="utf-8"))
    
    def parse_string(self, string):
        return self.parse_stream(StringIO(string))

    def parse_stream(self, stream):
        self.antlr = ANTLRv4Parser(CommonTokenStream(ANTLRv4Lexer(stream)))
        return True

