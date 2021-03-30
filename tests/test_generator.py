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

import os
import pytest
from gramorpher import Generator, PictCorpus, corpus
    
from .test import get_test_grammar_file_path, get_test_corpus_file_path

def generator_test(grammar_file, corpus_file, rule_name):
    generator = Generator(PictCorpus())

    test_grammar_file = get_test_grammar_file_path(grammar_file)
    assert generator.parse_grammar_file(test_grammar_file)

    test_corpus_file = get_test_corpus_file_path(corpus_file)
    assert generator.parse_corpus_file(test_corpus_file)

    grammar_rule = generator.find_rule(rule_name)
    assert(grammar_rule)
    # grammar_rule.print()
    #symbols = grammar_rule.symbols()
    #assert(generator.corpus.has_symbols(symbols))
    #for symbol in symbols:
    #    assert(generator.corpus.has_symbol(symbol))

    rule = generator.generate(rule_name)
    rule.print()

def test_csv_generator():
    generator_test('CSV.g4', 'CSV.pict', 'row')
