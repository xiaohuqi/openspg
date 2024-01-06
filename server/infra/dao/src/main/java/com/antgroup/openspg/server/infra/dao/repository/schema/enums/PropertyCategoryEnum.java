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

package com.antgroup.openspg.server.infra.dao.repository.schema.enums;

public enum PropertyCategoryEnum {
  /** Basic type. */
  BASIC,

  /** Advanced type. */
  ADVANCED;

  public static PropertyCategoryEnum getEnum(String name) {
    for (PropertyCategoryEnum categoryEnum : PropertyCategoryEnum.values()) {
      if (categoryEnum.name().equalsIgnoreCase(name)) {
        return categoryEnum;
      }
    }
    throw new IllegalArgumentException("illegal type=" + name);
  }
}
