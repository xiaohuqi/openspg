package com.antgroup.openspg.builder.core.physical.process;

import com.antgroup.openspg.builder.core.runtime.BuilderCatalog;
import com.antgroup.openspg.builder.core.runtime.BuilderContext;
import com.antgroup.openspg.builder.core.strategy.fusing.SubjectFusing;
import com.antgroup.openspg.builder.core.strategy.fusing.SubjectFusingImpl;
import com.antgroup.openspg.builder.core.strategy.linking.RecordLinking;
import com.antgroup.openspg.builder.core.strategy.linking.RecordLinkingImpl;
import com.antgroup.openspg.builder.core.strategy.predicting.RecordPredicting;
import com.antgroup.openspg.builder.core.strategy.predicting.RecordPredictingImpl;
import com.antgroup.openspg.builder.model.exception.BuilderRecordException;
import com.antgroup.openspg.builder.model.pipeline.config.SPGTypeMappingNodeConfig;
import com.antgroup.openspg.builder.model.record.BaseAdvancedRecord;
import com.antgroup.openspg.builder.model.record.BaseSPGRecord;
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
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.apache.commons.collections4.CollectionUtils;

@Getter
@AllArgsConstructor
public class SPGTypeMappingHelper {

  private final SPGTypeIdentifier identifier;
  private BaseSPGType spgType;

  private RecordLinking recordPropertyLinking;
  private RecordLinking recordRelationLinking;

  private RecordPredicting recordPropertyPredicting;
  private RecordPredicting recordRelationPredicting;

  private SubjectFusing subjectFusing;

  private final SPGTypeMappingNodeConfig config;

  public SPGTypeMappingHelper(SPGTypeMappingNodeConfig config) {
    this.config = config;
    this.identifier = SPGTypeIdentifier.parse(config.getSpgType());
  }

  public void init(BuilderContext context) {
    this.spgType = (BaseSPGType) loadSchema(identifier, context.getCatalog());

    this.recordPropertyLinking = new RecordLinkingImpl(config.getPropertyLinkingConfigs());
    this.recordPropertyLinking.init(context);
    this.recordRelationLinking = new RecordLinkingImpl(config.getRelationLinkingConfigs());
    this.recordRelationLinking.init(context);

    this.recordPropertyPredicting = new RecordPredictingImpl(config.getPropertyPredictingConfigs());
    this.recordPropertyPredicting.init(context);
    this.recordRelationPredicting = new RecordPredictingImpl(config.getRelationPredictingConfigs());
    this.recordRelationPredicting.init(context);

    this.subjectFusing = new SubjectFusingImpl(config.getSubjectFusingConfig());
    this.subjectFusing.init(context);
  }

  private BaseOntology loadSchema(BaseSPGIdentifier identifier, BuilderCatalog catalog) {
    SPGIdentifierTypeEnum identifierType = identifier.getIdentifierType();
    if (identifierType == SPGIdentifierTypeEnum.SPG_TYPE) {
      return catalog.getSPGType((SPGTypeIdentifier) identifier);
    }
    throw new IllegalArgumentException("illegal identifier type=" + identifierType);
  }

  public boolean isFiltered(BuilderRecord record) {
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

  public BuilderRecord mapping(BuilderRecord record) {
    List<SPGTypeMappingNodeConfig.MappingConfig> mappingConfigs = config.getMappingConfigs();
    if (CollectionUtils.isEmpty(mappingConfigs)) {
      // if empty, perform mapping with the same name
      return record;
    }
    Map<String, String> newProps = new HashMap<>(record.getProps().size());
    for (SPGTypeMappingNodeConfig.MappingConfig mappingConfig : mappingConfigs) {
      String source = mappingConfig.getSource();
      String target = mappingConfig.getPredicate();

      String sourceValue = record.getPropValue(source);
      if (sourceValue != null) {
        newProps.put(target, sourceValue);
      }
    }
    return record.withNewProps(newProps);
  }

  public List<BaseSPGRecord> toSPGRecords(BuilderRecord record) {
    return null;
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
