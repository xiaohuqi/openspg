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

# ATTENTION!
# This file is generated by Schema automatically, it will be refreshed after schema has been committed
# PLEASE DO NOT MODIFY THIS FILE!!!
#

from knext.common.schema_helper import SPGTypeHelper, PropertyHelper, RelationHelper


class RiskMining:
    class App(SPGTypeHelper):
        description = PropertyHelper("description")
        id = PropertyHelper("id")
        name = PropertyHelper("name")
        riskMark = PropertyHelper("riskMark")
        belongTo = PropertyHelper("belongTo")
        useCert = PropertyHelper("useCert")

    class Cert(SPGTypeHelper):
        description = PropertyHelper("description")
        id = PropertyHelper("id")
        name = PropertyHelper("name")
        certNum = PropertyHelper("certNum")

    class Company(SPGTypeHelper):
        description = PropertyHelper("description")
        id = PropertyHelper("id")
        name = PropertyHelper("name")
        hasPhone = PropertyHelper("hasPhone")

        hasCert = RelationHelper("hasCert")
        holdShare = RelationHelper("holdShare")

    class Device(SPGTypeHelper):
        description = PropertyHelper("description")
        id = PropertyHelper("id")
        name = PropertyHelper("name")
        umid = PropertyHelper("umid")
        install = PropertyHelper("install")

    class Person(SPGTypeHelper):
        description = PropertyHelper("description")
        id = PropertyHelper("id")
        name = PropertyHelper("name")
        belongTo = PropertyHelper("belongTo")
        hasPhone = PropertyHelper("hasPhone")
        age = PropertyHelper("age")

        holdShare = RelationHelper("holdShare")
        hasDevice = RelationHelper("hasDevice")
        hasCert = RelationHelper("hasCert")
        fundTrans = RelationHelper("fundTrans")
        release = RelationHelper("release")
        developed = RelationHelper("developed")

    class TaxOfRiskApp(SPGTypeHelper):
        description = PropertyHelper("description")
        id = PropertyHelper("id")
        name = PropertyHelper("name")
        stdId = PropertyHelper("stdId")
        alias = PropertyHelper("alias")

    class TaxOfRiskUser(SPGTypeHelper):
        description = PropertyHelper("description")
        id = PropertyHelper("id")
        name = PropertyHelper("name")
        alias = PropertyHelper("alias")
        stdId = PropertyHelper("stdId")

    App = App("RiskMining.App")
    Cert = Cert("RiskMining.Cert")
    Company = Company("RiskMining.Company")
    Device = Device("RiskMining.Device")
    Person = Person("RiskMining.Person")
    TaxOfRiskApp = TaxOfRiskApp("RiskMining.TaxOfRiskApp")
    TaxOfRiskUser = TaxOfRiskUser("RiskMining.TaxOfRiskUser")

    pass
