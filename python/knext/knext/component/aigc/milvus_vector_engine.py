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

from knext.component.aigc.base import VectorEngineComponent


class MilvusVectorEngine(VectorEngineComponent):
    """ the milvus vector engine ."""

    def save(self, embeddings):
        """save embeddings to milvus`.

        """
        return

    def search(self, embeddings, top_n):
        """ search with embedding in milvus."""
        return

