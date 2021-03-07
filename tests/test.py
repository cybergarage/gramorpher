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

def get_test_file_paths(test_file_dir, text_file_ext):
    test_files = []
    for file in os.listdir(test_file_dir):
        if file.endswith(text_file_ext):
            test_file_path = os.path.join(test_file_dir, file)
            test_files.append(test_file_path)
    return test_files

def get_test_grammars_path():
    test_dir = os.path.dirname(__file__)
    return os.path.join(test_dir, "grammars")

def get_test_grammar_file_path(file_name):
    return os.path.join(get_test_grammars_path(), file_name)

def get_test_grammar_file_paths():
    return get_test_file_paths(get_test_grammars_path(), ".g4")

def get_test_corpuses_path():
    test_dir = os.path.dirname(__file__)
    return os.path.join(test_dir, "corpuses")

def get_test_corpus_file_path(file_name):
    return os.path.join(get_test_corpuses_path(), file_name)

def get_test_corpus_file_paths():
    return get_test_file_paths(get_test_corpuses_path(), ".pict")
