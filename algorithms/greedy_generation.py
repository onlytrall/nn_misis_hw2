
import torch
import random

import utils
import time
import numpy as np

from transformers import AutoModelForCausalLM, AutoTokenizer

def greedy_generate(model, tokenizer, system_prompt, prompt, max_tokens=1000):
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
    print(time.time() - ctime)
    ctime = time.time()
    
    if torch.argmax(next_logits) == eos_token:
      generated_eos = True
    else:
      text += tokenizer.decode(torch.argmax(next_logits))
      generated_tokens += [torch.argmax(next_logits)]
      if cnt_op == 25:
        cnt_op = 0
        torch.cuda.empty_cache()
      
      print(time.time() - ctime)
  
    print()
  

  return generated_text, generated_tokens
  


