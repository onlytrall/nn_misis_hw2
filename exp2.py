import os
os.environ["CUDE_VISIBLE_DEVICES"] = "0"

import torch

from algorithms.sampling_generation import sampling_generate
from transformers import AutoModelForCausalLM, AutoTokenizer
from tokenizers import Tokenizer
from dataclasses import dataclass

_STORY_TELLER_SYSTEM_PROMPT = 'You are a storyteller. Generate a story based on user message.\n'
_JSON_SYSTEM_PROMPT = 'You are a JSON machine. Generate a JSON with format {"contractor": string with normalized contractor name, "sum": decimal, "currency": string with uppercased 3-letter currency code} based on user message.'

_STORY_TELLER_USER_PROMPT = 'Generate me a short story about a tiny hedgehog named Sonic.'
_JSON_USER_PROMPT = 'Transfer 100 rubles and 50 kopeck to Mike'

@dataclass
class Config:
  system_prompt = _STORY_TELLER_SYSTEM_PROMPT
  prompt = _STORY_TELLER_USER_PROMPT
  model_name = 'Qwen/Qwen2.5-0.5B-Instruct'

if __name__ == "__main__":

  config = Config()
  device = 'cuda' if torch.cuda.is_available() else 'cpu'
  # device='cpu'

  model = AutoModelForCausalLM.from_pretrained(config.model_name).to(device).eval()
  tokenizer = AutoTokenizer.from_pretrained(config.model_name, use_fast=True)

  all_text, generated = sampling_generate(model=model, tokenizer=tokenizer, system_prompt=config.system_prompt, prompt=config.prompt)
  
  # print(all_text)
  print(tokenizer.decode(generated))
