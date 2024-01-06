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

package com.antgroup.openspg.cloudext.interfaces.graphstore.adapter.util;

import com.antgroup.openspg.builder.model.record.BaseAdvancedRecord;
import com.antgroup.openspg.builder.model.record.ConceptRecord;
import com.antgroup.openspg.builder.model.record.EntityRecord;
import com.antgroup.openspg.builder.model.record.EventRecord;
import com.antgroup.openspg.builder.model.record.StandardRecord;
import com.antgroup.openspg.builder.model.record.property.SPGPropertyRecord;
import com.antgroup.openspg.cloudext.interfaces.graphstore.model.lpg.record.VertexRecord;
import com.antgroup.openspg.core.schema.model.identifier.ConceptIdentifier;
import com.antgroup.openspg.core.schema.model.type.BaseSPGType;
import com.antgroup.openspg.core.schema.model.type.ConceptType;
import com.antgroup.openspg.core.schema.model.type.EntityType;
import com.antgroup.openspg.core.schema.model.type.EventType;
import com.antgroup.openspg.core.schema.model.type.StandardType;
import com.antgroup.openspg.server.common.model.exception.GraphStoreException;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Convertor for {@link VertexRecord} and {@link BaseAdvancedRecord AdvancedRecord}s. <strong>NOTE:
 * </strong> {@link BaseAdvancedRecord AdvancedRecord} includes {@link ConceptRecord}, {@link
 * EntityRecord}, {@link EventRecord}, {@link StandardRecord}.
 */
public class VertexRecordConvertor {

  /** Convert the SPG record to an LPG record. */
  public static VertexRecord toVertexRecord(BaseAdvancedRecord advancedRecord) {
    return new VertexRecord(
        advancedRecord.getId(),
        advancedRecord.getName(),
        PropertyRecordConvertor.toLPGProperties(advancedRecord.getProperties()));
  }

  /**
   * Convert the SPG property record to an LPG record, which is currently used only for standard
   * types, as a standard type will automatically generate an LPG record based on the property.
   */
  public static List<VertexRecord> toVertexRecords(SPGPropertyRecord propertyRecord) {
    if (propertyRecord.isBasicType()) {
      throw GraphStoreException.unexpectedSPGPropertyRecordType(propertyRecord);
    }
    String vertexType = propertyRecord.getProperty().getObjectTypeRef().getName();
    List<String> vertexIdList = propertyRecord.getValue().getIds();
    return vertexIdList.stream()
        .map(vertexId -> new VertexRecord(vertexId, vertexType, Collections.emptyList()))
        .collect(Collectors.toList());
  }

  /**
   * Convert the LPG record to an SPG record, mainly used in the mapping or reasoning process of
   * knowledge builder.
   */
  public static BaseAdvancedRecord toAdvancedRecord(
      BaseSPGType baseSpgType, String bizId, Map<String, String> properties) {
    BaseAdvancedRecord advancedRecord = null;
    switch (baseSpgType.getSpgTypeEnum()) {
      case ENTITY_TYPE:
        advancedRecord =
            new EntityRecord(
                (EntityType) baseSpgType,
                bizId,
                PropertyRecordConvertor.toSPGProperties(properties, baseSpgType));
        break;
      case CONCEPT_TYPE:
        advancedRecord =
            new ConceptRecord(
                (ConceptType) baseSpgType,
                new ConceptIdentifier(bizId),
                PropertyRecordConvertor.toSPGProperties(properties, baseSpgType));
        break;
      case EVENT_TYPE:
        advancedRecord =
            new EventRecord(
                (EventType) baseSpgType,
                bizId,
                PropertyRecordConvertor.toSPGProperties(properties, baseSpgType));
        break;
      case STANDARD_TYPE:
        advancedRecord =
            new StandardRecord(
                (StandardType) baseSpgType,
                bizId,
                PropertyRecordConvertor.toSPGProperties(properties, baseSpgType));
        break;
      default:
        throw GraphStoreException.unexpectedSPGTypeEnum(baseSpgType.getSpgTypeEnum());
    }
    return advancedRecord;
  }
}
