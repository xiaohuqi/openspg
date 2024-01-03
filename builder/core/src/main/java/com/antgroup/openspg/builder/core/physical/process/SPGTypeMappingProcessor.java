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

package com.antgroup.openspg.builder.core.physical.process;

import com.antgroup.openspg.builder.core.runtime.BuilderCatalog;
import com.antgroup.openspg.builder.core.runtime.BuilderContext;
import com.antgroup.openspg.builder.core.strategy.fusing.SubjectFusing;
import com.antgroup.openspg.builder.core.strategy.fusing.SubjectFusingImpl;
import com.antgroup.openspg.builder.core.strategy.linking.RecordLinking;
import com.antgroup.openspg.builder.core.strategy.linking.RecordLinkingImpl;
import com.antgroup.openspg.builder.core.strategy.linking.impl.SearchBasedLinking;
import com.antgroup.openspg.builder.core.strategy.predicting.RecordPredicting;
import com.antgroup.openspg.builder.core.strategy.predicting.RecordPredictingImpl;
import com.antgroup.openspg.builder.model.exception.BuilderException;
import com.antgroup.openspg.builder.model.exception.BuilderRecordException;
import com.antgroup.openspg.builder.model.pipeline.config.SPGTypeMappingNodeConfig;
import com.antgroup.openspg.builder.model.record.BaseAdvancedRecord;
import com.antgroup.openspg.builder.model.record.BaseRecord;
import com.antgroup.openspg.builder.model.record.BuilderRecord;
import com.antgroup.openspg.builder.model.record.RelationRecord;
import com.antgroup.openspg.cloudext.interfaces.graphstore.adapter.util.EdgeRecordConvertor;
import com.antgroup.openspg.cloudext.interfaces.graphstore.adapter.util.VertexRecordConvertor;
import com.antgroup.openspg.common.util.StringUtils;
import com.antgroup.openspg.core.schema.model.BaseOntology;
import com.antgroup.openspg.core.schema.model.identifier.BaseSPGIdentifier;
import com.antgroup.openspg.core.schema.model.identifier.SPGIdentifierTypeEnum;
import com.antgroup.openspg.core.schema.model.identifier.SPGTypeIdentifier;
import com.antgroup.openspg.core.schema.model.predicate.Relation;
import com.antgroup.openspg.core.schema.model.type.BaseSPGType;
import com.google.common.collect.Lists;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;

@Slf4j
@SuppressWarnings({"unchecked", "rawtypes"})
public class SPGTypeMappingProcessor extends BaseProcessor<SPGTypeMappingNodeConfig> {

  private final SPGTypeIdentifier identifier;
  private BaseSPGType spgType;
  private RecordLinking recordLinking;
  private RecordPredicting recordPredicting;
  private SubjectFusing subjectFusing;

  public SPGTypeMappingProcessor(String id, String name, SPGTypeMappingNodeConfig config) {
    super(id, name, config);
    this.identifier = SPGTypeIdentifier.parse(config.getSpgType());
  }

  @Override
  public void doInit(BuilderContext context) throws BuilderException {
    super.doInit(context);

    this.spgType = (BaseSPGType) loadSchema(identifier, context.getCatalog());

    this.recordLinking = new RecordLinkingImpl(config.getLinkingConfigs());
    this.recordLinking.setDefaultPropertyLinking(new SearchBasedLinking());
    this.recordLinking.init(context);

    this.subjectFusing = new SubjectFusingImpl(config.getSubjectFusingConfig());
    this.subjectFusing.init(context);

    this.recordPredicting = new RecordPredictingImpl(config.getPredictingConfigs());
    this.recordPredicting.init(context);
  }

  private BaseOntology loadSchema(BaseSPGIdentifier identifier, BuilderCatalog catalog) {
    SPGIdentifierTypeEnum identifierType = identifier.getIdentifierType();
    if (identifierType == SPGIdentifierTypeEnum.SPG_TYPE) {
      return catalog.getSPGType((SPGTypeIdentifier) identifier);
    }
    throw new IllegalArgumentException("illegal identifier type=" + identifierType);
  }

  @Override
  public List<BaseRecord> process(List<BaseRecord> inputs) {
    List<BaseAdvancedRecord> advancedRecords = new ArrayList<>(inputs.size());
    for (BaseRecord baseRecord : inputs) {
      BuilderRecord record = (BuilderRecord) baseRecord;
      if (isFiltered(record)) {
        continue;
      }

      BuilderRecord mappedRecord = mapping(record);
      BaseAdvancedRecord advancedRecord = toSPGRecord(mappedRecord, spgType);
      if (advancedRecord != null) {
        recordLinking.linking(advancedRecord);
        recordPredicting.predicting(advancedRecord);
        List<BaseAdvancedRecord> subjectFusedRecord =
            subjectFusing.fusing(Lists.newArrayList(advancedRecord));
        advancedRecords.addAll(subjectFusedRecord);
      }
    }
    return (List) advancedRecords;
  }

  @Override
  public void close() throws Exception {}

  private boolean isFiltered(BuilderRecord record) {
    List<SPGTypeMappingNodeConfig.MappingFilter> mappingFilters = config.getMappingFilters();
    if (record.getIdentifier() != null && !record.getIdentifier().equals(identifier)) {
      return true;
    }
    if (CollectionUtils.isEmpty(mappingFilters)) {
      return false;
    }
    for (SPGTypeMappingNodeConfig.MappingFilter mappingFilter : mappingFilters) {
      String columnName = mappingFilter.getColumnName();
      String columnValue = mappingFilter.getColumnValue();

      String propertyValue = record.getPropValue(columnName);
      if (columnValue.equals(propertyValue)) {
        return false;
      }
    }
    return true;
  }

  private BuilderRecord mapping(BuilderRecord record) {
    List<SPGTypeMappingNodeConfig.MappingConfig> mappingConfigs = config.getMappingConfigs();
    if (CollectionUtils.isEmpty(mappingConfigs)) {
      // if empty, perform mapping with the same name
      return record;
    }
    Map<String, String> newProps = new HashMap<>(record.getProps().size());
    for (SPGTypeMappingNodeConfig.MappingConfig mappingConfig : mappingConfigs) {
      String source = mappingConfig.getSource();
      String target = mappingConfig.getTarget();

      String sourceValue = record.getPropValue(source);
      if (sourceValue != null) {
        newProps.put(target, sourceValue);
      }
    }
    return record.withNewProps(newProps);
  }

  private BaseAdvancedRecord toSPGRecord(BuilderRecord record, BaseSPGType spgType) {
    String bizId = record.getPropValue("id");
    if (StringUtils.isBlank(bizId)) {
      throw new BuilderRecordException("");
    }
    return VertexRecordConvertor.toAdvancedRecord(spgType, bizId, record.getProps());
  }

  private RelationRecord toSPGRecord(BuilderRecord record, Relation relation) {
    String srcId = record.getPropValue("srcId");
    String dstId = record.getPropValue("dstId");
    if (StringUtils.isBlank(srcId) || StringUtils.isBlank(dstId)) {
      throw new BuilderRecordException("");
    }
    return EdgeRecordConvertor.toRelationRecord(relation, srcId, dstId, record.getProps());
  }
}
