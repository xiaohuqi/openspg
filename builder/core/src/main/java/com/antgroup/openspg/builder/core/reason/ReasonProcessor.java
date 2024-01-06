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

import com.antgroup.openspg.builder.core.physical.process.BaseProcessor;
import com.antgroup.openspg.builder.core.reason.impl.CausalConceptReasoner;
import com.antgroup.openspg.builder.core.reason.impl.InductiveConceptReasoner;
import com.antgroup.openspg.builder.core.runtime.BuilderContext;
import com.antgroup.openspg.builder.core.strategy.linking.RecordLinking;
import com.antgroup.openspg.builder.core.strategy.linking.RecordLinkingImpl;
import com.antgroup.openspg.builder.model.exception.BuilderException;
import com.antgroup.openspg.builder.model.pipeline.config.BaseNodeConfig;
import com.antgroup.openspg.builder.model.pipeline.enums.NodeTypeEnum;
import com.antgroup.openspg.builder.model.record.BaseAdvancedRecord;
import com.antgroup.openspg.builder.model.record.BaseRecord;
import com.antgroup.openspg.builder.model.record.BaseSPGRecord;
import com.antgroup.openspg.core.schema.model.semantic.DynamicTaxonomySemantic;
import com.antgroup.openspg.core.schema.model.semantic.LogicalCausationSemantic;
import com.antgroup.openspg.core.schema.model.type.ConceptList;
import com.antgroup.openspg.reasoner.catalog.impl.OpenSPGCatalog;
import com.antgroup.openspg.reasoner.common.graph.vertex.IVertexId;
import com.antgroup.openspg.reasoner.graphstate.GraphState;
import com.antgroup.openspg.reasoner.lube.catalog.Catalog;
import com.antgroup.openspg.reasoner.warehouse.cloudext.CloudExtGraphState;
import com.google.common.collect.Lists;
import java.util.*;

@SuppressWarnings({"unchecked", "rawtypes"})
public class ReasonProcessor extends BaseProcessor<ReasonProcessor.ReasonerNodeConfig> {

  public static class ReasonerNodeConfig extends BaseNodeConfig {
    public ReasonerNodeConfig() {
      super(NodeTypeEnum.REASON);
    }
  }

  private RecordLinking recordNormalizer;
  private InductiveConceptReasoner inductiveConceptReasoner;
  private CausalConceptReasoner causalConceptReasoner;

  public ReasonProcessor() {
    super("", "", null);
  }

  @Override
  public void doInit(BuilderContext context) throws BuilderException {
    super.doInit(context);
    Catalog catalog = buildCatalog();
    GraphState<IVertexId> graphState = buildGraphState(context.getGraphStoreUrl());
    this.inductiveConceptReasoner = new InductiveConceptReasoner();
    this.inductiveConceptReasoner.setCatalog(catalog);
    this.inductiveConceptReasoner.setGraphState(graphState);

    this.causalConceptReasoner = new CausalConceptReasoner();
    this.causalConceptReasoner.setCatalog(catalog);
    this.causalConceptReasoner.setBuilderCatalog(context.getCatalog());
    this.causalConceptReasoner.setGraphState(graphState);
    this.causalConceptReasoner.setInductiveConceptReasoner(inductiveConceptReasoner);

    this.recordNormalizer = new RecordLinkingImpl();
    this.recordNormalizer.init(context);
  }

  @Override
  public List<BaseRecord> process(List<BaseRecord> inputs) {
    List<BaseRecord> results = new ArrayList<>();
    for (BaseRecord baseRecord : inputs) {
      if (!(baseRecord instanceof BaseAdvancedRecord)) {
        continue;
      }
      BaseAdvancedRecord advancedRecord = (BaseAdvancedRecord) baseRecord;

      // now only supports single classification of one entity type
      ConceptList conceptList =
          ReasonerProcessorUtils.getConceptList(advancedRecord, context.getCatalog());
      if (conceptList == null) {
        continue;
      }

      // perform inductive and causal reasoning logic on the input advancedRecord
      results.addAll(reasoning(advancedRecord, conceptList));
    }

    for (BaseRecord baseRecord : results) {
      recordNormalizer.linking((BaseSPGRecord) baseRecord);
    }
    return results;
  }

  private List<BaseSPGRecord> reasoning(BaseAdvancedRecord record, ConceptList conceptList) {
    // run the inductive reasoning logic
    List<BaseSPGRecord> spgRecords = Lists.newArrayList(record);
    for (DynamicTaxonomySemantic belongTo : conceptList.getDynamicTaxonomyList()) {
      spgRecords = inductiveConceptReasoner.reason(spgRecords, belongTo);
    }

    // then run causal reasoning logic
    for (LogicalCausationSemantic leadTo : conceptList.getLogicalCausation()) {
      spgRecords = causalConceptReasoner.reason(spgRecords, leadTo);
    }
    return spgRecords;
  }

  private Catalog buildCatalog() {
    Catalog catalog =
        new OpenSPGCatalog(context.getProjectId(), null, context.getCatalog().getProjectSchema());
    catalog.init();
    return catalog;
  }

  private GraphState<IVertexId> buildGraphState(String graphStoreUrl) {
    return new CloudExtGraphState(graphStoreUrl);
  }

  @Override
  public void close() throws Exception {}
}
