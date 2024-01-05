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

import os
from enum import Enum
from typing import Dict

from knext import rest
from knext.client.base import Client
from knext.common.class_register import register_from_package
from knext.operator.base import BaseOp


class OperatorTypeEnum(str, Enum):
    LinkOp = "LINK"
    FuseOp = "FUSE"
    PredictOp = "PREDICT"
    ExtractOp = "EXTRACT"
    PromptOp = "PROMPT"


class OperatorClient(Client):
    """SPG Operator Client."""

    _rest_client = rest.OperatorApi()

    def __init__(self, host_addr: str = None, project_id: int = None):
        super().__init__(host_addr, project_id)
        if not BaseOp._has_registered and (
            "KNEXT_ROOT_PATH" in os.environ
            and "KNEXT_BUILDER_OPERATOR_DIR" in os.environ
        ):
            self._builder_operator_path = os.path.join(
                os.environ["KNEXT_ROOT_PATH"], os.environ["KNEXT_BUILDER_OPERATOR_DIR"]
            )

            register_from_package(self._builder_operator_path, BaseOp)

    def publish(self, op_name: str):
        """Upload operator files and publish a new version.
        If the operator has not been published, this method will create an operator overview firstly.

        """
        op = BaseOp.by_name(op_name)()

        operator_list = self._rest_client.operator_overview_get(name=op.name)
        if len(operator_list) == 0:
            self._rest_client.operator_overview_post(
                operator_create_request=rest.OperatorCreateRequest(
                    name=op.name, desc=op.desc, operator_type=op._type
                )
            )
            operator_id = self._rest_client.operator_overview_get(name=op.name)[0].id
        else:
            operator_id = operator_list[0].id

        add_response = self._rest_client.operator_version_post(
            project_id=self._project_id, operator_id=operator_id, file=op._local_path
        )
        op._version = add_response.latest_version

        if op.bind_to is not None:
            from knext.client.schema import SchemaClient
            from knext.client.model.base import SpgTypeEnum

            schema_session = SchemaClient().create_session()
            spg_type = schema_session.get(op.bind_to)
            if spg_type.spg_type_enum in [SpgTypeEnum.Entity, SpgTypeEnum.Event]:
                spg_type.bind_link_operator(op)
            elif spg_type.spg_type_enum == SpgTypeEnum.Concept:
                spg_type.bind_normalize_operator(op)
            else:
                pass
            schema_session.update_type(spg_type)
            schema_session.commit()

        return op

    def _generate_op_config(
        self, op_name: str, version: int = None, params: Dict[str, str] = None
    ):
        """Transforms a list of components to REST model `OperatorConfig`."""
        overviews = self._rest_client.operator_overview_get(op_name)
        if not overviews:
            raise ValueError(
                f"Operator [{op_name}] is not published."
                f" Use ` knext operator publish {op_name}` to publish this operator."
            )
        op = None
        operator_versions = self._rest_client.operator_version_get(op_name)
        if not operator_versions:
            raise ValueError(
                f"Operator [{op_name}] is not published."
                f" Use ` knext operator publish {op_name}` to publish this operator."
            )
        if version:
            # Pull operator from server with specified version.
            for operator_version in operator_versions:
                if operator_version.version == version:
                    op = operator_version
                    break
            if not op:
                raise ValueError(
                    f"Operator [{op_name}] with Version [{version}] is not published."
                    f" Use ` knext operator publish {op_name} ` to publish this operator."
                )
        else:
            # Pull operator from server with the latest version.
            op = self._rest_client.operator_version_get(op_name)[0]

        return rest.OperatorConfig(
            file_path=op.file_path,
            module_path=op.__module__,
            class_name=op.name,
            method="_handle",
            params=params,
        )
