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
from gramorpher import Grammar
from .test import get_test_grammar_file, get_test_grammar_files

# def test_grammar():
#     for test_grammar_file in get_test_grammar_files():
#         grammar = Grammar()
#         assert grammar.parse_file(test_grammar_file)
#         rules = grammar.rules()
#         assert 0 < len(rules)
#         for rule in rules:
#             elements = rule.elements()
#             assert(elements)

# def test_grammar_parse_hello():
#     grammar = Grammar()
#     test_grammar_file = get_test_grammar_file('Hello.g4')
#     assert grammar.parse_file(test_grammar_file)
#     rules = grammar.rules()
#     assert 0 < len(rules)
#     r = grammar.find("r")
#     assert(r)
#     elements = r.elements()
#     assert(elements)
#     hello_elem = r.find("'hello'")
#     assert(hello_elem)
#     id_elem = r.find("ID")
#     assert(id_elem)

def test_grammar_parse_unql():
    grammar = Grammar()
    test_grammar_file = get_test_grammar_file('UnQL.g4')
    assert grammar.parse_file(test_grammar_file)
    stmt_names = ["insert_stmt", "select_stmt", "update_stmt", "delete_stmt"]
    for stmt_name in stmt_names:
        stmt = grammar.find(stmt_name)
        assert(stmt)
