from huggingface_hub import create_repo
from transformers import AutoModelForCausalLM, AutoTokenizer

# create_repo("pot-r1-grpo-qwen2.5-7b-Instruct")

tokenizer = AutoTokenizer.from_pretrained("verl_checkpoints/pot-r1-grpo-qwen2.5-7b-Instruct-warmup/actor/global_step_80")
actor_module = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path="verl_checkpoints/pot-r1-grpo-qwen2.5-7b-Instruct-warmup/actor/global_step_80")

tokenizer.push_to_hub("ZhuofengLi/pot-r1-grpo-qwen2.5-7b-Instruct")
actor_module.push_to_hub("ZhuofengLi/pot-r1-grpo-qwen2.5-7b-Instruct")