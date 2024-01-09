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


class DataReportGenerator(AIGCComponent):
    """ generate content in data report mode """

    report_by_cell_prompt = '给定如下表格数据，请使用自然语言对表格的数据进行总体描述，\n表格数据: {input_data}'
    report_by_row_prompt = '给定如下表格数据，请使用自然语言对表格的第{row}行数据进行总体描述，\n表格数据: {input_data}'
    report_by_col_prompt = '给定如下表格数据，请使用自然语言对表格的第{col}列数据进行总体描述，\n表格数据: {input_data}'
    report_by_rc_prompt = '给定如下表格数据，请使用自然语言对表格的{subject}相关的数据进行描述，\n表格数据: {input_data}'

    def __init__(self, llm_invoke):
        self.llm_invok = llm_invoke

    def report_by_cell(self, input_data, custom_prompt=report_by_cell_prompt):
        """
                先生成逐个单元格播报的提示词，然后调用LLM进行生成
                逻辑说明：取默认提示词然后替换${input_data}
                参数说明：
                	spg_data 参数是数据列表
                    custom_prompt是【可选】参数，可以用户传入指定的提示词模板，包含${input_data}变量
                """
        prompt = custom_prompt.replace('{input_data}', input_data)
        return self.llm_invok.generate(prompt)

    def report_by_row(self, input_data, custom_prompt=report_by_row_prompt, row_no=1):
        """
        先依据数据及给定行生成以行为逻辑单元进行播报的提示词，然后调用LLM进行生成

        逻辑说明：取默认提示词然后替换${input_data} 和 ${row}
        参数说明：
            input_data 参数是数据列表
            custom_prompt 是【可选】参数，可以用户传入指定的提示词模板，包含${input_data}变量 和 ${row}变量
            row_no 指定的播报行
        """
        prompt = custom_prompt.replace('{input_data}', input_data).replace('{row}', str(row_no))
        return self.llm_invok.generate(prompt)

    def report_by_col(self, input_data, custom_prompt=report_by_col_prompt, col_no=1):
        """
        先依据数据及给定列生成以列为逻辑单元进行播报的提示词，然后调用LLM进行生成

        逻辑说明：取默认提示词然后替换${input_data}和 ${col} 变量
        参数说明：
            input_data 参数是数据列表
            custom_prompt是【可选】参数，可以用户传入指定的提示词模板，包含${input_data}变量和 ${col} 变量
            row_no 指定的播报行
        """
        prompt = custom_prompt.replace('{input_data}', input_data).replace('{col}', str(col_no))
        return self.llm_invok.generate(prompt)

    def report_by_rc(self, input_data, subject, custom_prompt=report_by_rc_prompt) -> str:
        """
        先依据数据及给定主题生成行列穿插进行播报的提示词，；此种播报时通常是与任务相关的，因此通常不直接使用默认的提示

        逻辑说明：取默认提示词然后替换${schema}
        参数说明：
            input_data 参数是数据列表
            subject 要播报的相关数据描述
            custom_prompt是【可选】参数，可以用户传入指定的提示词模板，包含${schema}变量和 ${subject} 变量
        """
        prompt = custom_prompt.replace('{input_data}', input_data).replace('{subject}', subject)
        return self.llm_invok.generate(prompt)

