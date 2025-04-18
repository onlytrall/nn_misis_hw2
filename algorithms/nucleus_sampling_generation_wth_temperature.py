
import torch
import random

import utils
import time
import numpy as np

from transformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger

@torch.no_grad
def sampling_generate(model, tokenizer, system_prompt, prompt, max_tokens=1000, temperature=1.0, top_p=0.0):
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
    logger.info(f'proccesing {len(generated_tokens) + 1} token;')
    cnt_op += 1
    ctime = time.time()
    next_logits = utils.get_next_token_logits(
      tokenizer=tokenizer,
      model=model, 
      prompt=text
    )

    # Choose next token
    probs_init = torch.nn.Softmax(dim=-1)(next_logits / temperature)
    next_token = None

    ctime = time.time()
    probs_vals, prob_indices = torch.sort(probs_init, descending=True)
    if probs_vals[0] > top_p:
      next_token = prob_indices[0]
    else:
      pref_sum = 0
      prob_coef = torch.zeros(len(probs_vals)).to(model.device)
      for i in range(len(probs_vals)):
        p = probs_vals[i]
        ind = prob_indices[i]
        if p + pref_sum <= top_p:
          pref_sum += p
          prob_coef[ind] = 1
        else:
          break

      probs_init = probs_init * prob_coef
      probs = probs_init / pref_sum
      next_token = torch.multinomial(probs, 1, replacement=True).squeeze()

    
    if next_token == eos_token:
      generated_eos = True
    else:
      text += tokenizer.decode(next_token)
      generated_tokens += [next_token]
      if time.time() - ctime > 0.1:
        cnt_op = 0
        torch.cuda.empty_cache()
          

  return generated_text, generated_tokens
  


