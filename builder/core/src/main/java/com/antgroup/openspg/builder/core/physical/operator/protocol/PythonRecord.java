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

package com.antgroup.openspg.builder.core.physical.operator.protocol;

import java.util.HashMap;
import java.util.Map;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;

/** Python operator entity */
@Getter
@Setter
@Accessors(chain = true)
public class PythonRecord {

  private String spgTypeName;
  private Map<String, String> properties;

  public String getId() {
    return properties.get("id");
  }

  public Map<String, Object> toMap() {
    Map<String, Object> results = new HashMap<>(2);
    results.put("spgTypeName", spgTypeName);
    results.put("properties", properties);
    return results;
  }
}
