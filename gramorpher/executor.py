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
from argparse import ArgumentParser

def main():
    arg_parser = ArgumentParser(prog = 'gramorpher')
    arg_parser.add_argument('command', help='command')
    arg_parser.add_argument('grammer', help='grammar file')
    arg_parser.add_argument('rule', help='rule name')
    args = arg_parser.parse_args()
    print(args.command)
    print(args.grammer_file)
    print(args.rule_name)

if __name__ == '__main__':
    main()