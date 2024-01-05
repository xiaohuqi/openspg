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
from typing import Union, Type, List

import networkx as nx

from knext.common.restable import RESTable
from knext.common.runnable import Runnable


class Chain(Runnable, RESTable):
    """
    Base class for creating structured sequences of calls to components.
    """

    """The execution process of Chain, represented by a dag structure."""
    dag: nx.DiGraph

    def invoke(self, input=None, **kwargs):
        from knext.chain.builder_chain import BuilderChain

        return BuilderChain.from_chain(self).invoke(**kwargs)

    def __rshift__(
        self,
        other: Union[
            Type["Chain"],
            List[Type["Chain"]],
            Type["Component"],
            List[Type["Component"]],
            None,
        ],
    ):
        from knext.component.base import Component
        from knext.component.builder.mapping import SPGTypeMapping
        from knext.component.builder.mapping import _SPGTypeMappings

        if not other:
            return self
        if not isinstance(other, list):
            other = [other]
        if all(isinstance(o, SPGTypeMapping) for o in other):
            other = [_SPGTypeMappings(spg_type_mappings=other)]
        dag_list = []
        for o in other:
            if not o:
                dag_list.append(o.dag)
            if isinstance(o, Component):
                end_nodes = [
                    node
                    for node, out_degree in self.dag.out_degree()
                    if out_degree == 0 or node._last
                ]
                dag = nx.DiGraph(self.dag)
                if len(end_nodes) > 0:
                    for end_node in end_nodes:
                        dag.add_edge(end_node, o)
                dag.add_node(o)
                dag_list.append(dag)
            elif isinstance(o, Chain):
                combined_dag = nx.compose(self.dag, o.dag)
                end_nodes = [
                    node
                    for node, out_degree in self.dag.out_degree()
                    if out_degree == 0 or node._last
                ]
                start_nodes = [
                    node for node, in_degree in o.dag.in_degree() if in_degree == 0
                ]

                if len(end_nodes) > 0 and len(start_nodes) > 0:
                    for end_node in end_nodes:
                        for start_node in start_nodes:
                            combined_dag.add_edge(end_node, start_node)
        final_dag = nx.compose_all(dag_list)
        return Chain(dag=final_dag)
