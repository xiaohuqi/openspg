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

from typing import List, Dict

from knext.api.record import SPGRecord
from knext.api.operator import ExtractOp


class AddressExtractOp(ExtractOp):
    def __init__(self, params: Dict[str, str] = None):
        super().__init__(params)

    def invoke(self, record: Dict[str, str]) -> List[SPGRecord]:
        province = record.get("province", "")
        city = record.get("city", "")
        district = record.get("district", "")

        record.update({"address", province + city + district})
        return [SPGRecord(properties=record)]
