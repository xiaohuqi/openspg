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


class SPGComplexGenerator(AIGCComponent):
    """ generate content in data explain mode """

    explain_prompt = '给定表格数据和数据的模式描述，请回答问题{question}\n表格数据: {input_data}\n数据描述：{spg_schema}'

    def __init__(self, llm_invoke):
        self.llm_invok = llm_invoke

    def get_schema_of_data(self, spg_data):
        """
        依据数据查询对应的schema
        参数说明：
            spg_data 参数是数据列表
        """
        pass

    def transfer_schema_description(self, spg_schema):
        """
        把数据对应schema 转换成文本描述
        参数说明：
            spg_schema：schema 描述
        """
        pass

    def data_explain(self, input_data, question, custom_prompt=explain_prompt):
        """
        基本过程：
        1、先针对输入数据获取数据相关的schema
        2、把schema转换与文本描述
        3、替换prompt模板中的数据及schema描述
        4、调用LLM进行最后的生成

        参数说明：
            input_data 输入的文本描述
            custom_prompt是【可选】参数，可以用户传入指定的提示词模板，包含${input_data}变量
        """
        schema = self.get_schema_of_data(input_data)
        schema_text = self.transfer_schema_description(schema)
        prompt = custom_prompt.replace('{input_data}', input_data).replace('{spg_schema}', schema_text).replace(f'{question}', question)
        result = self.llm_invok.generate(prompt)
        return result
