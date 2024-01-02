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

import copy
import json
import numpy as np
from typing import Dict, List
from knext.operator.base import BaseOp
from knext.operator.op import ExtractOp, LinkOp, FuseOp, PredictOp, SPGRecord


def jaccard_distance(a: str, b: str):
    terms_reference = list(b.replace(" ", ""))
    terms_model = list(a.replace(" ", ""))
    grams_reference = set(terms_reference)
    grams_model = set(terms_model)
    temp = 0
    for i in grams_reference:
        if i in grams_model:
            temp = temp + 1
    denominator = len(grams_model) + len(grams_reference) - temp
    if denominator == 0:
        return 0
    return float(temp / denominator)


class DummyOp(BaseOp):
    pass


class TestExtractOp(ExtractOp):
    def invoke(self, record: Dict[str, str]) -> List[SPGRecord]:
        spg_type = record["type"]
        properties = json.loads(record["properties"])
        return [SPGRecord(spg_type, properties)]


class TestLinkOp(LinkOp):
    bind_to = "Company"

    @property
    def num_outputs(self):
        return 10

    def invoke(self, property: str, subject_record: SPGRecord) -> List[SPGRecord]:
        output = []
        for i in range(self.num_outputs):
            record = copy.deepcopy(subject_record)
            record.update_property("index", str(i + 1))
            record.update_property("indexed_property", f"{property}_{i+1}")
            output.append(record)
        return output


class TestFuseOp(FuseOp):
    bind_to = "Company"

    @property
    def num_outputs(self):
        return 1

    def link(self, subject_record: SPGRecord) -> List[SPGRecord]:
        name = subject_record.get_property("name")
        output = []
        dummy_name = name
        for i in range(3):
            dummy_name = f"{dummy_name}{i+1}"
            record = copy.deepcopy(subject_record)
            record.update_property("name", dummy_name)
            record.update_property("index", str(i + 1))
            output.append(record)
        np.random.shuffle(output)
        print(f"link output = {output}")
        return output

    def merge(
        self, subject_record: SPGRecord, linked_records: List[SPGRecord]
    ) -> List[SPGRecord]:
        subject_name = subject_record.get_property("name")
        object_names = [x.get_property("name") for x in linked_records]
        scores = [jaccard_distance(subject_name, x) for x in object_names]
        idx = np.argmax(scores)
        output_record = linked_records[idx]
        print(f"merge output = {output_record}")
        return [output_record]


class TestPredictOp(PredictOp):
    bind_to = ("Company", "isSubsidiaryOf", "Company")

    @property
    def num_outputs(self):
        return 3

    def invoke(self, subject_record: SPGRecord) -> List[SPGRecord]:
        name = subject_record.get_property("name")
        output = []
        for i in range(self.num_outputs):
            record = copy.deepcopy(subject_record)
            new_name = f"{name}{i+1}"
            record.update_property("name", new_name)
            record.update_property("index", str(i + 1))
            output.append(record)
        return output