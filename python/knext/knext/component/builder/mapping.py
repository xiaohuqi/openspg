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
from enum import Enum
from typing import Union, Dict, List, Tuple, Sequence, Optional, Any

from knext import rest
from knext.client.base import Client
from knext.client.builder import BuilderClient
from knext.client.model.base import BaseSpgType
from knext.client.schema import SchemaClient
from knext.common.runnable import Input, Output

from knext.common.schema_helper import SPGTypeName, PropertyName, RelationName, TripletName
from knext.component.builder.base import Mapping
from knext.operator.op import LinkOp, FuseOp, PredictOp
from knext.operator.spg_record import SPGRecord


class LinkingStrategyEnum(str, Enum):
    IDEquals = "ID_EQUALS"


class FusingStrategyEnum(str, Enum):
    pass


class PredictingStrategyEnum(str, Enum):
    pass


FusingStrategy = Union[FusingStrategyEnum, FuseOp]
LinkingStrategy = Union[LinkingStrategyEnum, LinkOp]
PredictingStrategy = Union[PredictingStrategyEnum, PredictOp]


class SPGTypeMapping(Mapping):
    """A Builder Component that mapping source field[UnresolvedRecord with column names and values]
    to target field[SPGRecord with entity/event/concept/standard type and properties].

    The UnresolvedRecord will go through the following execution processes and be converted into SPGRecord:
    1. Field Mapping
        Map the source field data to the schema attribute field of the target type.
    2. Object Linking
        Traverse all mapped properties.
        If the object type of property is not `BasicType`, execute the default `IDEqual` linking strategy:
            Query with the property value as the `id` of the object SPGType instance.
            If a corresponding SPGType instance exists, establish an SPO relationship between subject and object.

        If a LinkOp is bound to the object type, the chain pointing process of generating objects based on attribute values is executed.
        Based on the property values, link to
        Establish an SPO relationship between the current subject type and the attribute type based on the attribute values.

    3. Predicate Predicting
        For the linked properties
    4. Subject Fusing


    Args:
        spg_type_name: The SPG type name of subject import from SPGTypeHelper.
    Examples:
        mapping = SPGTypeMapping(
            spg_type_name=DEFAULT.App
        ).add_mapping_field("id", DEFAULT.App.id) \
            .add_mapping_field("name", DEFAULT.App.name) \
            .add_mapping_field("riskMark", DEFAULT.App.riskMark) \
            .add_predicting_field(DEFAULT.App.useCert)
    """

    """The target subject type name of this mapping component."""
    spg_type_name: SPGTypeName

    fusing_strategy: FusingStrategy = None

    _property_mapping: Dict[TripletName, str] = dict()
    _relation_mapping: Dict[TripletName, str] = dict()
    _sub_property_mapping: Dict[TripletName, str] = dict()

    _filters: List[Tuple[str, str]] = list()

    _subject_fusing_strategy: Optional[FusingStrategy] = None

    _object_linking_strategies: Dict[TripletName, LinkingStrategy] = dict()

    _predicate_predicting_strategies: Dict[TripletName, PredictingStrategy] = dict()

    schema_session: SchemaClient.SchemaSession = None

    spg_type: BaseSpgType = None

    def model_post_init(self, __context: Any) -> None:
        if not self.schema_session:
            self.schema_session = SchemaClient(project_id=4).create_session()
        if not self.spg_type:
            self.spg_type = self.schema_session.get(self.spg_type_name)

    @property
    def input_types(self) -> Input:
        return Dict[str, str]

    @property
    def output_types(self) -> Output:
        return SPGRecord

    def add_property_mapping(
        self,
        source_name: str,
        target_name: PropertyName,
        target_type: SPGTypeName = None,
        linking_strategy: LinkingStrategy = None,
    ):
        if target_name not in self.spg_type.properties:
            raise ValueError(f"Property [{target_name}] does not exist in [{self.spg_type_name}].")
        object_type_name = self.spg_type.properties[target_name].object_type_name
        if target_type:
            assert target_type == object_type_name,\
                f"The SPGType of Property [{target_name}] is [{object_type_name}], but [{target_type}] is given." \
                f"Please check your schema config."
        triplet_name = (self.spg_type_name, target_name, object_type_name)

        if linking_strategy:
            pass
        elif object_type_name in LinkOp.bind_schemas:
            op_name = LinkOp.bind_schemas[object_type_name]
            linking_strategy = LinkOp.by_name(op_name)()
        else:
            linking_strategy = None
        self._property_mapping[triplet_name] = source_name
        self._object_linking_strategies[triplet_name] = linking_strategy
        return self

    def add_relation_mapping(
        self,
        source_name: str,
        target_name: PropertyName,
        target_type: SPGTypeName,
        linking_strategy: LinkingStrategy = None,
    ):
        relation_name = target_name + '_' + target_type
        if relation_name not in self.spg_type.relations:
            raise ValueError(f"Relation [{relation_name}] with ObjectType [target_type]"
                             f" does not exist in [{self.spg_type_name}].")
        triplet_name = (self.spg_type_name, target_name, target_type)
        if linking_strategy:
            pass
        elif target_type in LinkOp.bind_schemas:
            op_name = LinkOp.bind_schemas[target_type]
            linking_strategy = LinkOp.by_name(op_name)()
        else:
            linking_strategy = None
        self._realtion_mapping[triplet_name] = source_name
        self._object_linking_strategies[triplet_name] = linking_strategy

        return self

    def add_predicting_property(
        self,
        target_name: PropertyName,
        target_type: SPGTypeName = None,
        predicting_strategy: PredictingStrategy = None,
    ):
        if target_name not in self.spg_type.properties:
            raise ValueError(f"Property [{target_name}] does not exist in [{self.spg_type_name}].")
        object_type_name = self.spg_type.properties[target_name].object_type_name
        if target_type:
            assert target_type == object_type_name,\
                f"The SPGType of Property [{target_name}] is [{object_type_name}], but [{target_type}] is given." \
                f"Please check your schema config."
        triplet_name = (self.spg_type_name, target_name, object_type_name)
        if predicting_strategy:
            pass
        elif triplet_name in PredictOp.bind_schemas:
            op_name = PredictOp.bind_schemas[triplet_name]
            predicting_strategy = PredictOp.by_name(op_name)()
        else:
            predicting_strategy = None
        self._predicate_predicting_strategies[triplet_name] = predicting_strategy

        return self

    def add_predicting_relation(
        self,
        target_name: RelationName,
        target_type: SPGTypeName,
        predicting_strategy: PredictingStrategy = None,
    ):
        relation_name = target_name + '_' + target_type
        if relation_name not in self.spg_type.relations:
            raise ValueError(f"Relation [{relation_name}] with ObjectType [target_type]"
                             f" does not exist in [{self.spg_type_name}].")
        triplet_name = (self.spg_type_name, target_name, target_type)

        if predicting_strategy:
            pass
        elif triplet_name in PredictOp.bind_schemas:
            op_name = PredictOp.bind_schemas[triplet_name]
            predicting_strategy = PredictOp.by_name(op_name)()
        else:
            predicting_strategy = None
        self._predicate_predicting_strategies[triplet_name] = predicting_strategy
        return self

    def add_sub_property_mapping(self):
        pass

    def add_filter(self, column_name: str, column_value: str):
        """Adds data filtering rule.
        Only the column that meets `column_name=column_value` will execute the mapping.

        :param column_name: The column name to be filtered.
        :param column_value: The column value to be filtered.
        :return: self
        """
        self._filters.append((column_name, column_value))
        return self

    def to_rest(self):
        """
        Transforms `SPGTypeMapping` to REST model `SpgTypeMappingNodeConfig`.
        """

        mapping_filters = [
            rest.MappingFilter(column_name=name, column_value=value)
            for name, value in self.filters
        ]
        mapping_configs = []
        for tgt_name, src_name in self.mapping.items():
            linking_strategy = self.object_linking_strategies.get(tgt_name, None)
            if isinstance(linking_strategy, LinkOp):
                strategy_config = rest.OperatorLinkingConfig(
                    operator_config=linking_strategy.to_rest()
                )
            elif linking_strategy == LinkingStrategyEnum.IDEquals:
                strategy_config = rest.IdEqualsLinkingConfig()
            elif not linking_strategy:
                object_type_name = spg_type.properties[tgt_name].object_type_name
                if object_type_name in LinkOp.bind_schemas:
                    op_name = LinkOp.bind_schemas[object_type_name]
                    op = LinkOp.by_name(op_name)()
                    strategy_config = rest.OperatorLinkingConfig(
                        operator_config=op.to_rest()
                    )
                else:
                    strategy_config = None
            else:
                raise ValueError(f"Invalid linking_strategy [{linking_strategy}].")
            mapping_configs.append(
                rest.MappingConfig(
                    source=src_name,
                    target=tgt_name,
                    strategy_config=strategy_config,
                )
            )

        predicting_configs = []
        for (
            predicate_name,
            predicting_strategy,
        ) in self.predicate_predicting_strategies.items():
            if isinstance(predicting_strategy, PredictOp):
                strategy_config = rest.OperatorPredictingConfig(
                    operator_config=predicting_strategy.to_rest()
                )
            elif not predicting_strategy:
                object_type_name = spg_type.properties[predicate_name].object_type_name
                if (
                    self.spg_type_name,
                    predicate_name,
                    object_type_name,
                ) in PredictOp.bind_schemas:
                    op_name = PredictOp.bind_schemas[
                        (self.spg_type_name, predicate_name, object_type_name)
                    ]
                    op = PredictOp.by_name(op_name)()
                    strategy_config = rest.OperatorPredictingConfig(
                        operator_config=op.to_rest()
                    )
                else:
                    strategy_config = None
            else:
                raise ValueError(
                    f"Invalid predicting_strategy [{predicting_strategy}]."
                )
            if strategy_config:
                predicting_configs.append(
                    rest.PredictingConfig(
                        target=predicate_name, predicting_config=strategy_config
                    )
                )

        if isinstance(self.subject_fusing_strategy, FuseOp):
            fusing_config = rest.OperatorFusingConfig(
                operator_config=self.fusing_strategy.to_rest()
            )
        elif not self.subject_fusing_strategy:
            if self.spg_type_name in FuseOp.bind_schemas:
                op_name = FuseOp.bind_schemas[self.spg_type_name]
                op = FuseOp.by_name(op_name)()
                fusing_config = rest.OperatorFusingConfig(operator_config=op.to_rest())
            else:
                fusing_config = None
        else:
            raise ValueError(
                f"Invalid fusing_strategy [{self.subject_fusing_strategy}]."
            )

        config = rest.SpgTypeMappingNodeConfig(
            spg_type=self.spg_type_name,
            mapping_filters=mapping_filters,
            mapping_configs=mapping_configs,
            subject_fusing_config=fusing_config,
            predicting_configs=predicting_configs,
        )
        return rest.Node(**super().to_dict(), node_config=config)

    def invoke(self, input: Input) -> Sequence[Output]:
        raise NotImplementedError(
            f"`invoke` method is not currently supported for {self.__class__.__name__}."
        )

    @classmethod
    def from_rest(cls, rest_model):
        raise NotImplementedError(
            f"`from_rest` method is not currently supported for {cls.__name__}."
        )

    def submit(self):
        raise NotImplementedError(
            f"`submit` method is not currently supported for {self.__class__.__name__}."
        )


if __name__ == '__main__':
    a = SPGTypeMapping(spg_type_name="TEST.Entity1")
    print(a.spg_type)
