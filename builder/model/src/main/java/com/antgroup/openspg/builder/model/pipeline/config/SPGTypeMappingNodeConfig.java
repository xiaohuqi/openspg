/*
 * Copyright 2023 Ant Group CO., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied.
 */

package com.antgroup.openspg.builder.model.pipeline.config;

import com.antgroup.openspg.builder.model.pipeline.config.fusing.BaseFusingConfig;
import com.antgroup.openspg.builder.model.pipeline.enums.NodeTypeEnum;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
public class SPGTypeMappingNodeConfig extends BaseNodeConfig {

  @Getter
  @AllArgsConstructor
  public static class MappingFilter {
    private final String columnName;
    private final String columnValue;
  }

  public enum MappingType {
    PROPERTY,
    RELATION,
    SUB_PROPERTY,
    SUB_RELATION,
    ;
  }

  @Getter
  @AllArgsConstructor
  public static class MappingConfig {
    private final String source;
    private final String predicate;
    private final String object;
    private final BaseStrategyConfig strategyConfig;
    private final MappingType mappingType;
  }

  private final String spgType;

  private final List<MappingFilter> mappingFilters;

  private final List<MappingConfig> mappingConfigs;

  private final BaseFusingConfig subjectFusingConfig;

  public SPGTypeMappingNodeConfig(
      String spgType,
      List<MappingFilter> mappingFilters,
      List<MappingConfig> mappingConfigs,
      BaseFusingConfig subjectFusingConfig) {
    super(NodeTypeEnum.SPG_TYPE_MAPPING);
    this.spgType = spgType;
    this.mappingFilters = mappingFilters;
    this.mappingConfigs = mappingConfigs;
    this.subjectFusingConfig = subjectFusingConfig;
  }
}
