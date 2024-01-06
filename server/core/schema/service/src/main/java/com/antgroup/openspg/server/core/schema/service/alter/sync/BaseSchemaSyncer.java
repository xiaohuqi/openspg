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

package com.antgroup.openspg.server.core.schema.service.alter.sync;

import com.antgroup.openspg.core.schema.model.SPGSchemaAlterCmd;

/** The abstract class of schema writer. */
public abstract class BaseSchemaSyncer {
  /**
   * sync new schema of project into db.
   *
   * @param projectId the context of deploy pipeline
   * @param schemaEditCmd sync cmd
   */
  public abstract void syncSchema(Long projectId, SPGSchemaAlterCmd schemaEditCmd);
}
