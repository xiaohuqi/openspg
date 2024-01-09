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

from abc import ABC
from enum import Enum

from knext.component.base import Component


class ComponentTypeEnum(str, Enum):
    DataReportGenerator = "DATA_REPORT_GENERATOR"
    DataExplainGenerator = "DATA_EXPLAIN_GENERATOR"
    SPGComplexGenerator = "SPG_COMPLEX_GENERATOR"


class AIGCComponent(Component, ABC):
    """
    Abstract base class for all AIGC component.
    """

    @property
    def type(self):
        return ComponentTypeEnum.__members__[self.__class__.__name__].value


class LLMInvokeComponent(Component, ABC):
    """
    Abstract base class for all llm invoke component.
    """

    @property
    def type(self):
        return ComponentTypeEnum.__members__[self.__class__.__name__].value

    def generate(self, prompt):
        return


class VectorEngineComponent(Component, ABC):
    """
    Abstract base class for all llm invoke component.
    """

    @property
    def type(self):
        return ComponentTypeEnum.__members__[self.__class__.__name__].value

    def save(self, embeddings):
        return





