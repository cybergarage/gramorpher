# Copyright (C} 2020 Yahoo Japan Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"};
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

SHELL := bash

PKG_NAME=antlr
ANTLR_GRAMMERS_URL=https://raw.githubusercontent.com/antlr/grammars-v4/master/antlr/antlr4/
ANTLR_GRAMMER_FILES=ANTLRv4Lexer.g4 ANTLRv4Parser.g4 LexBasic.g4 LexerAdaptor.py
ANTLR=antlr

.PHONY: ${ANTLR_GRAMMER_FILES}

all: antlr

${ANTLR_GRAMMER_FILES}:
	@wget -nv ${ANTLR_GRAMMERS_URL}$@ -O $@

antlr: ${ANTLR_GRAMMER_FILES}
	@${ANTLR} -package ${PKG_NAME} -visitor -Dlanguage=Python3 *.g4
