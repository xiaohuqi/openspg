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
from knext.api.operator import FuseOp


class TestFuseOp(FuseOp):
    bind_to = "TEST.CenterEvent"

    def link(self, subject_record: SPGRecord) -> List[SPGRecord]:
        print("####################TestFuseOp#####################")
        print("TestFuseOp.link(Input): ")
        print("----------------------")
        print(subject_record)

        linked_record = subject_record
        linked_record.update_property(
            "id", linked_record.get_property("id") + "_linked"
        )
        linked_record.update_property(
            "name", linked_record.get_property("name") + "_linked"
        )
        print("TestFuseOp.link(Output): ")
        print("----------------------")
        print([linked_record])
        return [linked_record]

    def merge(
        self, subject_record: SPGRecord, linked_records: List[SPGRecord]
    ) -> List[SPGRecord]:
        print("TestFuseOp.merge(Input): ")
        print("----------------------")
        print(f"subject_record: {subject_record}, linked_records: {linked_records}")

        merged_record = subject_record
        merged_record.update_property(
            "id",
            "_".join([r.get_property("id") for r in linked_records + [subject_record]]),
        )
        merged_record.update_property(
            "name",
            "_".join(
                [r.get_property("name") for r in linked_records + [subject_record]]
            ),
        )
        print("TestFuseOp.merge(Output): ")
        print("----------------------")
        print([merged_record])
        return [merged_record]
