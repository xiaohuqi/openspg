# coding: utf-8
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


"""
    knext

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from knext.rest.configuration import Configuration


class BaseNodeConfig(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {"type": "str"}

    attribute_map = {"type": "type"}

    discriminator_value_class_map = {
        "CSV_SOURCE": "CsvSourceNodeConfig",
        "GRAPH_SINK": "GraphStoreSinkNodeConfig",
        "MAPPING": "MappingNodeConfig",
        "EXTRACT": "ExtractNodeConfig",
    }

    def __init__(self, type=None, local_vars_configuration=None):  # noqa: E501
        """BaseNodeConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self.discriminator = None

        self.type = type

    @property
    def type(self):
        """Gets the type of this BaseNodeConfig.  # noqa: E501


        :return: The type of this BaseNodeConfig.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this BaseNodeConfig.


        :param type: The type of this BaseNodeConfig.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and type is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `type`, must not be `None`"
            )  # noqa: E501
        allowed_values = ["CSV_SOURCE", "SPG_TYPE_MAPPING", "RELATION_MAPPING", "SUBGRAPH_MAPPING", "USER_DEFINED_EXTRACT", "LLM_BASED_EXTRACT", "GRAPH_SINK"]  # noqa: E501
        if (
            self.local_vars_configuration.client_side_validation
            and type not in allowed_values
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}".format(  # noqa: E501
                    type, allowed_values
                )
            )

        self._type = type

    def get_real_child_model(self, data):
        """Returns the child model by discriminator"""
        if "@type" in data:
            child_type = data.get("@type")
            real_child_model = self.discriminator_value_class_map.get(child_type)
            return real_child_model
        return None

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BaseNodeConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BaseNodeConfig):
            return True

        return self.to_dict() != other.to_dict()
