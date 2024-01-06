# Copyright 2023 Ant Group CO., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

import json
from typing import Dict, List

from knext.api.operator import ExtractOp
from knext.operator.spg_record import SPGRecord
from nn4k.invoker import NNInvoker


class _BuiltInOnlineExtractor(ExtractOp):
    def __init__(self, params: Dict[str, str] = None):
        super().__init__(params)
        self.model = self.load_model()
        self.prompt_ops = self.load_operator()
        self.max_retry_times = int(self.params.get("max_retry_times", "3"))

    def load_model(self):
        model_config = json.loads(self.params["model_config"])
        return NNInvoker.from_config(model_config)

    def load_operator(self):
        import importlib.util

        prompt_config = json.loads(self.params["prompt_config"])
        prompt_ops = []
        for op_config in prompt_config:
            spec = importlib.util.spec_from_file_location(
                op_config["modulePath"], op_config["filePath"]
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            op_clazz = getattr(module, op_config["className"])
            params = op_config.get("params", {})
            op_obj = op_clazz(**params)
            prompt_ops.append(op_obj)

        return prompt_ops

    def invoke(self, record: Dict[str, str]) -> List[SPGRecord]:

        collector = []
        input_params = [record]
        for op in self.prompt_ops:
            next_params = []
            for input_param in input_params:
                retry_times = 0
                while retry_times < self.max_retry_times:
                    try:
                        query = op.build_prompt(input_param)
                        response = self.model.remote_inference(query)
                        collector.extend(op.parse_response(response))
                        next_params.extend(
                            op._build_next_variables(input_param, response)
                        )
                        break
                    except Exception as e:
                        retry_times += 1
                        raise e
            input_params = next_params
        return collector
