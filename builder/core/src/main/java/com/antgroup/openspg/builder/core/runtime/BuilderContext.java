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

package com.antgroup.openspg.builder.core.runtime;

import com.antgroup.openspg.builder.model.record.RecordAlterOperationEnum;
import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;

@Setter
@Getter
@Accessors(chain = true)
public class BuilderContext implements Serializable {

  private long projectId;
  private String jobName;
  private RecordAlterOperationEnum operation;
  private BuilderCatalog catalog;

  private String pythonExec;
  private String pythonPaths;
  private String graphStoreUrl;
  private String searchEngineUrl;

  private int batchSize = 1;
  private int parallelism = 1;
  private boolean enableLeadTo;
}
