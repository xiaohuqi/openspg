# -*- coding: utf-8 -*-
# Copyright 2023 Ant Group CO., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from typing import List

from knext.api.record import SPGRecord
from knext.api.operator import PredictOp


class TestPredictOp(PredictOp):
    bind_to = ("TEST.Entity1", "predictProperty", "TEST.Entity3")

    def invoke(self, subject_record: SPGRecord) -> List[SPGRecord]:
        print("####################TestPredictOp#####################")
        print("TestPredictOp(Input): ")
        print("----------------------")
        print(subject_record)

        predict_record = SPGRecord(
            spg_type_name="TEST.Entity3",
            properties={
                "id": "TestEntity3",
                "name": "TestEntity3",
            }
        )
        print("TestPredictOp(Output): ")
        print("----------------------")
        print([predict_record])

        return [predict_record]

