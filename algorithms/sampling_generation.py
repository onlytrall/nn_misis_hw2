
import torch
import random

import utils
import time
import numpy as np

from transformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger

def sampling_generate(model, tokenizer, system_prompt, prompt, max_tokens=1000):
  generated_tokens = []
  eos_token = tokenizer(tokenizer.eos_token).to(model.device)['input_ids'][0]
  generated_text = ''

  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
  ]

  text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
  )
  
  logger.info(f"Model's input prompt: {text}")
  
  cnt_op = 0
  generated_eos = False
  while len(generated_tokens) < max_tokens and not generated_eos:
    cnt_op += 1
    ctime = time.time()
    next_logits = utils.get_next_token_logits(
      tokenizer=tokenizer,
      model=model, 
      prompt=text
    )
    probs = torch.nn.Softmax(dim=-1)(next_logits)
    next_token = torch.multinomial(probs, 1, replacement=True).squeeze()
    ctime = time.time()
    
    if next_token == eos_token:
      generated_eos = True
    else:
      text += tokenizer.decode(next_token)
      generated_tokens += [next_token]
      if time.time() - ctime > 0.1:
        cnt_op = 0
        torch.cuda.empty_cache()
          

  return generated_text, generated_tokens
  


