# -*- coding: utf-8 -*-
# Copyright 2024 PlantData CO., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from knext.component.aigc.base import AIGCComponent


class DataExplainGenerator(AIGCComponent):
    """ generate content in data explain mode """

    explain_prompt = '给定如下文本数据及列表数据，请从列表中选取与文本描述数据对应的数据：\n文本数据: {text}\n列表数据：{data_list}'

    def __init__(self, llm_invoke, vector_engine):
        self.llm_invok = llm_invoke
        self.vector_engine = vector_engine

    def data_explain(self, input_text, custom_prompt=explain_prompt):
        """
        基本过程：
        1、先针对输入文本调用LLM进行向量化
        2、调用向量搜索执行搜索
        3、把搜索的结果组装、替换得到prompt
        4、调用LLM进行最后的解释数据选取

        参数说明：
            input_text 输入的文本描述
            custom_prompt是【可选】参数，可以用户传入指定的提示词模板，包含${input_data}变量
        """
        embedding = self.llm_invoke.embedding(input_text)
        data_list = self.vector_engine.search(embedding, 10)
        prompt = custom_prompt.replace('{text}', input_text).replace('{data_list}', data_list)
        result = self.llm_invok.generate(prompt)
        return result
