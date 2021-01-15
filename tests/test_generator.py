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
from gramorpher import Generator
from .test import get_test_grammar_file

def test_generator_unql():
    generator = Generator()
    test_grammar_file = get_test_grammar_file('UnQL.g4')
    assert generator.parse_grammar_file(test_grammar_file)
    stmt_names = ['insert_stmt', 'select_stmt', 'update_stmt', 'delete_stmt']
    for stmt_name in stmt_names:
        stmt = generator.find_rule(stmt_name)
        assert(stmt)
    insert_stmt = generator.find_rule('insert_stmt')
    assert(insert_stmt)
    print(str(insert_stmt))
