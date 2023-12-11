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


class PropertyNormalizerConfig(object):
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
    openapi_types = {
        'normalizer_type': 'str'
    }

    attribute_map = {
        'normalizer_type': 'normalizerType'
    }

    def __init__(self, normalizer_type=None, local_vars_configuration=None):  # noqa: E501
        """PropertyNormalizerConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._normalizer_type = None
        self.discriminator = None

        self.normalizer_type = normalizer_type

    @property
    def normalizer_type(self):
        """Gets the normalizer_type of this PropertyNormalizerConfig.  # noqa: E501


        :return: The normalizer_type of this PropertyNormalizerConfig.  # noqa: E501
        :rtype: str
        """
        return self._normalizer_type

    @normalizer_type.setter
    def normalizer_type(self, normalizer_type):
        """Sets the normalizer_type of this PropertyNormalizerConfig.


        :param normalizer_type: The normalizer_type of this PropertyNormalizerConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and normalizer_type is None:  # noqa: E501
            raise ValueError("Invalid value for `normalizer_type`, must not be `None`")  # noqa: E501
        allowed_values = ["OPERATOR", "ID_EQUALS"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and normalizer_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `normalizer_type` ({0}), must be one of {1}"  # noqa: E501
                .format(normalizer_type, allowed_values)
            )

        self._normalizer_type = normalizer_type

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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
        if not isinstance(other, PropertyNormalizerConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PropertyNormalizerConfig):
            return True

        return self.to_dict() != other.to_dict()
