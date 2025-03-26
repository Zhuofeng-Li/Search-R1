# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Preprocess the nq dataset to parquet format
"""

import re
import os
import datasets

from verl.utils.hdfs_io import copy, makedirs
import argparse

# prefix = f"""Answer the following question. 
# You must conduct reasoning inside <think> and </think>. 
# If, during reasoning, you determine that calculations or logical operations are needed, 
# write Python code inside <search> and </search> to call the Python interpreter, ensuring that the desired result is placed inside the print function to interact with the Python interpreter. 
# The output of the print function or any error message will be captured and returned from the Python interpreter between <information> and </information>.
# You can use the Python interpreter as many times as necessary. 
# If no further calculations or logical operations are required, provide the final answer directly inside <answer> and </answer> without detailed explanations. 
# For example: <answer>42</answer> Question: {question}\n""" # TODO: update: add no python interpreter version

def make_prefix(dp, template_type):
    question = dp['problem']

    # NOTE: also need to change reward_score/countdown.py
    if template_type == 'base':
        """This works for any base model"""
        prefix = f"""Answer the following question. 
You must conduct reasoning inside <think> and </think>. 
If, during reasoning, you determine that calculations or logical operations are needed, 
write Python code inside <python> and </python> to call the Python interpreter, ensuring that the desired result is placed inside the print function to interact with the Python interpreter. 
The output of the print function or any error message will be captured and returned from the Python interpreter between <information> and </information>.
You can use the Python interpreter as many times as necessary. 
If no further calculations or logical operations are required, provide the final answer directly inside <answer> and </answer> without detailed explanations. 
For example: <answer>42</answer> Question: {question}\n"""
    elif template_type == 'no_python':
        prefix = f"""Answer the following question. Let's think step by step.
You must conduct reasoning inside <think> and </think>. 
If no further calculations or logical operations are required, provide the final answer directly inside <answer> and </answer> without detailed explanations. 
For example: <answer>42</answer> Question: {question}\n"""
    else:
        raise NotImplementedError
    return prefix


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_dir', default='./data/big_math')
    parser.add_argument('--hdfs_dir', default=None)
    parser.add_argument('--template_type', type=str, default='base')

    args = parser.parse_args()

    data_source = 'big_math'

    dataset = datasets.load_dataset('SynthLabsAI/Big-Math-RL-Verified')

    train_dataset = dataset['train']
    # test_dataset = dataset['test']

    # add a row to each data item that represents a unique id
    def make_map_fn(split):

        def process_fn(example, idx):
            example['problem'] = example['problem'].strip()
            if example['problem'][-1] != '?':
                example['problem'] += '?'
            problem = make_prefix(example, template_type=args.template_type)
            solution = {
                "target": example['answer'],
            }

            data = {
                "data_source": data_source,
                "prompt": [{
                    "role": "user",
                    "content": problem,
                }],
                "ability": "math",
                "reward_model": {
                    "style": "rule",
                    "ground_truth": solution 
                },
                "extra_info": {
                    'split': split,
                    'index': idx,
                }
            }
            return data

        return process_fn

    train_dataset = train_dataset.map(function=make_map_fn('train'), with_indices=True)
    # test_dataset = test_dataset.map(function=make_map_fn('test'), with_indices=True)

    local_dir = args.local_dir
    hdfs_dir = args.hdfs_dir

    train_dataset.to_parquet(os.path.join(local_dir, 'train.parquet'))
    # test_dataset.to_parquet(os.path.join(local_dir, 'test.parquet'))

    if hdfs_dir is not None:
        makedirs(hdfs_dir)
        copy(src=local_dir, dst=hdfs_dir)
