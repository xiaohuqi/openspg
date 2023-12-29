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

package com.antgroup.openspg.builder.runner.local.physical.sink;

import com.antgroup.openspg.builder.core.logical.BaseLogicalNode;
import com.antgroup.openspg.builder.core.logical.GraphStoreSinkNode;
import com.antgroup.openspg.builder.runner.local.physical.sink.impl.GraphStoreSinkWriter;

public class SinkWriterFactory {

  public static BaseSinkWriter<?> getSinkWriter(BaseLogicalNode<?> baseNode) {
    switch (baseNode.getType()) {
      case GRAPH_SINK:
        return new GraphStoreSinkWriter(
            baseNode.getId(), baseNode.getName(), ((GraphStoreSinkNode) baseNode).getNodeConfig());
      default:
        throw new IllegalArgumentException("illegal nodeType=" + baseNode.getType());
    }
  }
}
