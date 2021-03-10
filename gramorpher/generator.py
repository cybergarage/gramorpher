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
        pass

    class Error(Exception):
        def __init__(self, msg):
            self.message = msg
