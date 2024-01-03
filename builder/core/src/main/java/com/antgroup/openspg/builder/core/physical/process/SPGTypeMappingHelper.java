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
import com.antgroup.openspg.builder.model.pipeline.config.SPGTypeMappingNodeConfig;
import com.antgroup.openspg.core.schema.model.BaseOntology;
import com.antgroup.openspg.core.schema.model.identifier.BaseSPGIdentifier;
import com.antgroup.openspg.core.schema.model.identifier.SPGIdentifierTypeEnum;
import com.antgroup.openspg.core.schema.model.identifier.SPGTypeIdentifier;
import com.antgroup.openspg.core.schema.model.type.BaseSPGType;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class SPGTypeMappingHelper {

  private final SPGTypeIdentifier identifier;
  private BaseSPGType spgType;
  private RecordLinking recordLinking;
  private RecordPredicting recordPredicting;
  private SubjectFusing subjectFusing;

  private final SPGTypeMappingNodeConfig config;

  public SPGTypeMappingHelper(SPGTypeMappingNodeConfig config) {
    this.config = config;
    this.identifier = SPGTypeIdentifier.parse(config.getSpgType());
  }

  public void init(BuilderContext context) {
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
}
