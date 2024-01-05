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

from knext.client.model.builder_job import BuilderJob
from knext.component.builder import CSVReader, SPGTypeMapping, KGWriter
from schema.riskmining_schema_helper import RiskMining


class Cert(BuilderJob):
    def build(self):
        source = CSVReader(
            local_path="./builder/job/data/Cert.csv",
            columns=["id", "certNum"],
            start_row=2,
        )

        mapping = (
            SPGTypeMapping(spg_type_name=RiskMining.Cert)
            .add_property_mapping("certNum", RiskMining.Cert.id)
            .add_property_mapping("certNum", RiskMining.Cert.certNum)
            .add_property_mapping("certNum", RiskMining.Cert.name)
        )

        sink = KGWriter()

        return source >> mapping >> sink
