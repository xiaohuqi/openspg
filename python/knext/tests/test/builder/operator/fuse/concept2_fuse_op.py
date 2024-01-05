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
from knext.api.client import SearchClient

from schema.test_schema_helper import TEST


class Concept2FuseOp(FuseOp):
    bind_to = TEST.Concept2

    def __init__(self):
        super().__init__()
        self.search_client = SearchClient(self.bind_to)

    def link(self, subject_record: SPGRecord) -> List[SPGRecord]:
        print("####################Concept2FuseOp#####################")
        print("Concept2FuseOp.link(Input): ")
        print("--------------------------------------------")
        print(subject_record)

        linked_records = self.search_client.fuzzy_search(subject_record, TEST.Concept2.name)

        print("Concept2FuseOp.link(Output): ")
        print("--------------------------------------------")
        print(linked_records)
        return linked_records

    def merge(
            self, subject_record: SPGRecord, linked_records: List[SPGRecord]
    ) -> List[SPGRecord]:
        print("Concept2FuseOp.merge(Input): ")
        print("--------------------------------------------")
        print(f"subject_record: {subject_record}, linked_records: {linked_records}")

        for prop_name, prop_value in subject_record.properties.items():
            new_value = ".".join(
                [r.get_property(prop_name, "") for r in [linked_records[0], subject_record]])
            new_value_list = new_value.split('.')
            if len(new_value_list) > 1:
                new_value = new_value_list[0] + new_value_list[1]
            subject_record.upsert_property(prop_name, new_value)

        print("Concept2FuseOp.merge(Output): ")
        print("--------------------------------------------")
        print([subject_record])
        return [subject_record]
