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
from gramorpher import PictCorpus
from .test import get_test_corpus_file_paths

def test_corpus_symbols():
    for test_corpus_file in get_test_corpus_file_paths():
        pict = PictCorpus()
        assert pict.parse_file(test_corpus_file)
        symbol_names = pict.names
        assert 0 < len(symbol_names)
        symbol_cases = pict.cases
        assert 0 < len(symbol_cases)
        for symbol_case in symbol_cases:
            for symbol_name in symbol_names:
                symbol = symbol_case.find_case(symbol_name)
                assert symbol