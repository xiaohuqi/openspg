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

import com.antgroup.openspg.builder.model.record.BaseSPGRecord;
import com.antgroup.openspg.core.schema.model.semantic.BaseConceptSemantic;
import java.util.List;

public interface ConceptReasoner<T extends BaseConceptSemantic> {

  List<BaseSPGRecord> reason(List<BaseSPGRecord> records, T conceptSemantic);
}
