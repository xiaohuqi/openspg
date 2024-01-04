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
from knext.api.operator import LinkOp


class TestLinkOp(LinkOp):
    bind_to = "TEST.Entity2"

    def invoke(self, property: str, subject_record: SPGRecord) -> List[SPGRecord]:
        print("####################TestLinkOp#####################")
        print("TestLinkOp(Input): ")
        print("----------------------")
        print(f"property: {property}, subject_record: {subject_record}")

        recall_record = SPGRecord(
            spg_type_name="TEST.Entity2",
            properties={
                "id": "TestEntity2",
                "name": "TestEntity2",
            }
        )
        print("TestLinkOp(Output): ")
        print("----------------------")
        print([recall_record])

        return [recall_record]
