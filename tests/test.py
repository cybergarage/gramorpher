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

def get_test_grammars_path():
    test_dir = os.path.dirname(__file__)
    return os.path.join(test_dir, "grammars")

def get_test_grammar_files():
    grammar_files = []
    grammars_dir = get_test_grammars_path()
    for file in os.listdir(grammars_dir):
        if file.endswith(".g4"):
            test_grammar_file = os.path.join(grammars_dir, file)
            grammar_files.append(test_grammar_file)
    return grammar_files
