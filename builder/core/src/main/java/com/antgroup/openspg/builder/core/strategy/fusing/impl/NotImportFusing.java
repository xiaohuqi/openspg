package com.antgroup.openspg.builder.core.strategy.fusing.impl;

import com.antgroup.openspg.builder.core.runtime.BuilderContext;
import com.antgroup.openspg.builder.core.strategy.fusing.EntityFusing;
import com.antgroup.openspg.builder.model.exception.BuilderException;
import com.antgroup.openspg.builder.model.exception.FusingException;
import com.antgroup.openspg.builder.model.record.BaseAdvancedRecord;

import java.util.Collections;
import java.util.List;

public class NotImportFusing implements EntityFusing {

  public static final NotImportFusing INSTANCE = new NotImportFusing();

  private NotImportFusing() {}

  @Override
  public void init(BuilderContext context) throws BuilderException {}

  @Override
  public List<BaseAdvancedRecord> fusing(List<BaseAdvancedRecord> records) throws FusingException {
    return Collections.emptyList();
  }
}
