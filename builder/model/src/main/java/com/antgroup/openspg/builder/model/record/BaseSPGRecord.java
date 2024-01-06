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

package com.antgroup.openspg.builder.model.record;

import com.antgroup.openspg.builder.model.record.property.BasePropertyRecord;
import com.antgroup.openspg.builder.model.record.property.SPGPropertyValue;
import com.antgroup.openspg.core.schema.model.type.WithSPGTypeEnum;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Getter;

@Getter
public abstract class BaseSPGRecord extends BaseRecord implements WithSPGTypeEnum {

  private final SPGRecordTypeEnum recordType;

  protected BaseSPGRecord(SPGRecordTypeEnum recordType) {
    this.recordType = recordType;
  }

  public abstract List<BasePropertyRecord> getProperties();

  public Map<String, String> getRawPropertyValueMap() {
    Map<String, String> rawPropertyValueMap = new HashMap<>(getProperties().size());
    for (BasePropertyRecord propertyRecord : getProperties()) {
      rawPropertyValueMap.put(propertyRecord.getName(), propertyRecord.getValue().getRaw());
    }
    return rawPropertyValueMap;
  }

  public Map<String, String> getStdStrPropertyValueMap() {
    Map<String, String> stdStrPropertyValueMap = new HashMap<>(getProperties().size());
    for (BasePropertyRecord propertyRecord : getProperties()) {
      SPGPropertyValue value = propertyRecord.getValue();
      stdStrPropertyValueMap.put(propertyRecord.getName(), value.getStdValue());
    }
    return stdStrPropertyValueMap;
  }
}
