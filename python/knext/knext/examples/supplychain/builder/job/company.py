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
from knext.api.component import (
    CSVReader,
    KGWriter,
    SPGTypeMapping,
    RelationMapping,
)
from schema.supplychain_schema_helper import SupplyChain


class Company(BuilderJob):
    parallelism = 6

    def build(self):
        source = CSVReader(
            local_path="./builder/job/data/Company.csv",
            columns=["id", "name", "products"],
            start_row=2,
        )

        mapping = (
            SPGTypeMapping(spg_type_name=SupplyChain.Company)
            .add_property_mapping("id", SupplyChain.Company.id)
            .add_property_mapping("name", SupplyChain.Company.name)
            .add_property_mapping("products", SupplyChain.Company.product)
        )

        sink = KGWriter()

        return source >> mapping >> sink


class CompanyUpdate(BuilderJob):
    parallelism = 6

    def build(self):
        source = CSVReader(
            local_path="./builder/job/data/CompanyUpdate.csv",
            columns=["id", "name", "products"],
            start_row=2,
        )

        mapping = (
            SPGTypeMapping(spg_type_name=SupplyChain.Company)
            .add_property_mapping("id", SupplyChain.Company.id)
            .add_property_mapping("name", SupplyChain.Company.name)
            .add_property_mapping("products", SupplyChain.Company.product)
        )

        sink = KGWriter()

        return source >> mapping >> sink


class CompanyFundTrans(BuilderJob):
    def build(self):
        source = CSVReader(
            local_path="./builder/job/data/Company_fundTrans_Company.csv",
            columns=["src", "dst", "transDate", "transAmt"],
            start_row=2,
        )

        mapping = (
            RelationMapping(
                subject_name=SupplyChain.Company,
                predicate_name="fundTrans",
                object_name=SupplyChain.Company,
            )
            .add_sub_property_mapping("src", "srcId")
            .add_sub_property_mapping("dst", "dstId")
            .add_sub_property_mapping("transDate", "transDate")
            .add_sub_property_mapping("transAmt", "transAmt")
        )

        sink = KGWriter()

        return source >> mapping >> sink
