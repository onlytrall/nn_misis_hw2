import os
os.environ["CUDE_VISIBLE_DEVICES"] = "0"

import torch

from algorithms.greedy_generation import greedy_generate
from transformers import AutoModelForCausalLM, AutoTokenizer
from tokenizers import Tokenizer
from dataclasses import dataclass

@dataclass
class Config:
  system_prompt_storyteller = 'You are a storyteller. Generate a story based on user message.\n'
  system_prompt_json = 'You are a JSON machine. Generate a JSON with format {"contractor": string with normalized contractor name, "sum": decimal, "currency": string with uppercased 3-letter currency code} based on user message.'
  model_name = 'Qwen/Qwen2.5-0.5B-Instruct'

if __name__ == "__main__":

  config = Config()
  device = 'cuda' if torch.cuda.is_available() else 'cpu'
  # device='cpu'
  print(device)

  model = AutoModelForCausalLM.from_pretrained(config.model_name).to(device).eval()
  tokenizer = AutoTokenizer.from_pretrained(config.model_name, use_fast=True)

  prompt = 'Transfer 100 rubles and 50 kopeck to Mike'
  print(prompt)

  all_text, generated = greedy_generate(model=model, tokenizer=tokenizer, system_prompt=config.system_prompt_json, prompt=prompt)
  
  print(all_text)
  print(tokenizer.decode(generated))
