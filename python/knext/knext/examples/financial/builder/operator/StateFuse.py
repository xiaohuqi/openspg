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

from knext.client.search import SearchClient
from knext.operator.op import FuseOp
from knext.operator.spg_record import SPGRecord


class StateFuse(FuseOp):
    bind_to = "Financial.State"

    def __init__(self):
        super().__init__()
        self.search_client = SearchClient("Financial.State")

    def link(self, subject_record: SPGRecord) -> List[SPGRecord]:
        print("####################StateFuse(状态融合)#####################")
        print("StateFuse(Input): ")
        print("----------------------")
        print(subject_record)
        linked_records = []
        query = {"match": {"name": subject_record.get_property("name", "")}}
        recall_records = self.search_client.search(query, start=0, size=10)
        if recall_records is not None and len(recall_records) > 0:
            linked_records.append(
                SPGRecord(
                    "Financial.State",
                    {
                        "id": recall_records[0].doc_id,
                        "name": recall_records[0].properties.get("name", ""),
                    },
                )
            )

        return linked_records

    def merge(
        self, subject_record: SPGRecord, linked_records: List[SPGRecord]
    ) -> List[SPGRecord]:
        merged_records = [subject_record]
        print("StateFuse(Output): ")
        print("----------------------")
        [print(r) for r in merged_records]
        return merged_records
