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

package com.antgroup.openspg.builder.core.reason;

import com.antgroup.openspg.builder.core.runtime.BuilderCatalog;
import com.antgroup.openspg.builder.model.record.BaseAdvancedRecord;
import com.antgroup.openspg.builder.model.record.BaseSPGRecord;
import com.antgroup.openspg.builder.model.record.RelationRecord;
import com.antgroup.openspg.builder.model.record.property.SPGPropertyRecord;
import com.antgroup.openspg.builder.model.record.property.SPGPropertyValue;
import com.antgroup.openspg.cloudext.interfaces.graphstore.adapter.util.EdgeRecordConvertor;
import com.antgroup.openspg.cloudext.interfaces.graphstore.adapter.util.VertexRecordConvertor;
import com.antgroup.openspg.common.util.CollectionsUtils;
import com.antgroup.openspg.core.schema.model.identifier.RelationIdentifier;
import com.antgroup.openspg.core.schema.model.identifier.SPGTypeIdentifier;
import com.antgroup.openspg.core.schema.model.predicate.Property;
import com.antgroup.openspg.core.schema.model.predicate.Relation;
import com.antgroup.openspg.core.schema.model.semantic.SystemPredicateEnum;
import com.antgroup.openspg.core.schema.model.type.BaseSPGType;
import com.antgroup.openspg.core.schema.model.type.ConceptList;
import com.antgroup.openspg.core.schema.model.type.SPGTypeRef;
import com.antgroup.openspg.reasoner.common.graph.edge.IEdge;
import com.antgroup.openspg.reasoner.common.graph.property.IProperty;
import com.antgroup.openspg.reasoner.common.graph.vertex.IVertex;
import com.antgroup.openspg.reasoner.common.graph.vertex.IVertexId;
import com.antgroup.openspg.reasoner.common.graph.vertex.impl.VertexBizId;
import com.antgroup.openspg.reasoner.runner.local.model.LocalReasonerResult;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.apache.commons.collections4.CollectionUtils;

public class ReasonerProcessorUtils {

  public static void setBelongToProperty(
      LocalReasonerResult result, BaseAdvancedRecord advancedRecord) {
    if (CollectionUtils.isEmpty(result.getEdgeList())) {
      return;
    }

    Property belongToProperty =
        advancedRecord.getSpgType().getPredicateProperty(SystemPredicateEnum.BELONG_TO);
    if (belongToProperty == null) {
      throw new IllegalStateException(
          String.format("spgType=%s has not belongTo property", advancedRecord.getName()));
    }

    IEdge<IVertexId, IProperty> edge = result.getEdgeList().get(0);
    SPGPropertyRecord propertyRecord =
        new SPGPropertyRecord(
            belongToProperty, new SPGPropertyValue(((VertexBizId) edge.getTargetId()).getBizId()));
    advancedRecord.mergePropertyValue(propertyRecord);
  }

  public static List<BaseSPGRecord> toSpgRecords(
      LocalReasonerResult result, BuilderCatalog catalog) {
    List<IVertex<IVertexId, IProperty>> vertices =
        CollectionsUtils.defaultEmpty(result.getVertexList());
    List<IEdge<IVertexId, IProperty>> edges = CollectionsUtils.defaultEmpty(result.getEdgeList());

    List<BaseSPGRecord> results = new ArrayList<>(vertices.size() + edges.size());
    vertices.forEach(
        vertex -> {
          VertexBizId vertexId = (VertexBizId) vertex.getId();
          Map<String, String> properties = toProps(vertex.getValue());
          BaseSPGType spgType = catalog.getSPGType(SPGTypeIdentifier.parse(vertexId.getType()));

          BaseAdvancedRecord advancedRecord =
              VertexRecordConvertor.toAdvancedRecord(spgType, vertexId.getBizId(), properties);
          results.add(advancedRecord);
        });

    edges.forEach(
        edge -> {
          Relation relationType = catalog.getRelation(RelationIdentifier.parse(edge.getType()));
          Map<String, String> properties = toProps(edge.getValue());

          RelationRecord relationRecord =
              EdgeRecordConvertor.toRelationRecord(
                  relationType,
                  ((VertexBizId) edge.getSourceId()).getBizId(),
                  ((VertexBizId) edge.getTargetId()).getBizId(),
                  properties);
          results.add(relationRecord);
        });
    return results;
  }

  private static Map<String, String> toProps(IProperty property) {
    Collection<String> keySet = property.getKeySet();

    Map<String, String> properties = new HashMap<>(keySet.size());
    for (String key : keySet) {
      Object value = property.get(key);
      if (value != null) {
        properties.put(key, value.toString());
      }
    }
    return properties;
  }

  public static ConceptList getConceptList(BaseSPGRecord spgRecord, BuilderCatalog catalog) {
    if (!(spgRecord instanceof BaseAdvancedRecord)) {
      return null;
    }
    BaseAdvancedRecord advancedRecord = (BaseAdvancedRecord) spgRecord;
    Property belongToProperty =
        advancedRecord.getSpgType().getPredicateProperty(SystemPredicateEnum.BELONG_TO);
    if (belongToProperty == null) {
      return null;
    }

    SPGTypeRef objectTypeRef = belongToProperty.getObjectTypeRef();
    if (!objectTypeRef.isConceptType()) {
      return null;
    }
    return catalog.getConceptList(objectTypeRef.getBaseSpgIdentifier());
  }
}
