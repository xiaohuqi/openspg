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


class SPGDataEmgedding():

    def __init__(self, llm_invoke, vector_engine):
        """
        初始化
        """
        self.llm_invoke = llm_invoke  # 调用的语义向量模型
        self.vector_engine = vector_engine      # 向量引擎

    def get_sgpt_concept_types(self, spg_id):
        """
        获取SPG的概念类型
        参数说明：
            spg_id：SPG数据id
        """
        return

    def get_sgpt_event_types(self, spg_id):
        """
        获取SPG的事件类型
        参数说明：
            spg_id：SPG数据id
        """
        return

    def get_split_data(self, spg_id, type_id, from_index, num):
        """
        按照SPG类型依次获取执行数据
        参数说明：
            spg_id: SPG数据id
            type_id: 类型的id
            from_index: 起始位置
            num: 获取的条数
        """
        return

    def embeddeing_data(self, spg_data):
        """
        对切分的数据进行向量化

        逻辑说明：使用指定的语义向量模型进行数据向量化，返回数据对应的向量列表
        参数说明：
            spg_data 参数是数据列表
        """
        self.llm_invoke.embedding(spg_data)
    pass

    def save_embeddeing(self, spg_id, embeddings):
        """
        保存向量

        逻辑说明：保存数据向量化后得到的向量到向量搜索引擎
        参数说明：
            spg_id 参数是向量数据表id
            embeddings 参数是向量列表
        """
    pass

    def spgt_embeddeing(self, spg_id):
        """
        调用上述步骤进行SPG的数据向量化并存储
        逻辑说明：先获取类型，然后按照类型读取分布的SPG数据，然后调用embedding 接口进行向量化，最后调用向量搜索引擎保存
        参数说明：
            spg_id 参数是向量数据表id
        """
    pass