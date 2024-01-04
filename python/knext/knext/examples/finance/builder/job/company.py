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


from schema.finance_schema_helper import Finance

from knext.api.component import CSVReader, LLMBasedExtractor, KGWriter, SubGraphMapping
from knext.client.model.builder_job import BuilderJob
from nn4k.invoker import LLMInvoker

from knext.component.builder import SPGTypeMapping


class Company(BuilderJob):
    def build(self):
        source = CSVReader(
            local_path="builder/job/data/company.csv", columns=["input"], start_row=2
        )

        from knext.api.auto_prompt import REPrompt

        prompt = REPrompt(
            spg_type_name=Finance.Company,
            property_names=[
                Finance.Company.name,
                Finance.Company.orgCertNo,
                Finance.Company.regArea,
                Finance.Company.businessScope,
                Finance.Company.establishDate,
                Finance.Company.legalPerson,
                Finance.Company.regCapital,
            ],
            relation_names=[

            ]
        )

        extract = LLMBasedExtractor(
            llm=LLMInvoker.from_config("builder/model/openai_infer.json"),
            prompt_ops=[prompt],
        )

        mapping = (
            SPGTypeMapping(spg_type_name=Finance.Company)
            # .add_sub_property_mapping("sub1", Finance.Company.belongTo.score2, Finance.Person, [])   score1
            # .add_sub_property_mapping("sub2", Finance.Company.belongTo, Finance.Cert)    score2
        )

        sink = KGWriter()

        return source >> extract >> mapping >> sink


if __name__ == "__main__":
    from knext.api.auto_prompt import REPrompt

    prompt = REPrompt(
        spg_type_name=Finance.Company,
        property_names=[
            Finance.Company.orgCertNo,
            Finance.Company.regArea,
            Finance.Company.businessScope,
            Finance.Company.establishDate,
            Finance.Company.legalPerson,
            Finance.Company.regCapital,
        ],
    )
    print(prompt.template)
