
import torch
import random

import utils
import time
import numpy as np

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from loguru import logger

@torch.no_grad
def beam_search_builtin(model, tokenizer, system_prompt, prompt, num_beams):
  generate_config = GenerationConfig(
      num_beams=num_beams,
      do_sample=False,
      num_return_sequences=num_beams,
      repetition_penalty=1.0,
      length_penalty=2.0,
      return_dict_in_generate=True,
      max_new_tokens=500,
      output_logits=True
  )

  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
  ]

  text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
  )

  out = model.generate(**tokenizer(text, return_tensors="pt").to(model.device), generation_config=generate_config, tokenizer=tokenizer)

  for i in range(num_beams):
    logger.info(tokenizer.decode(out.sequences[i], skip_special_tokens=True))

  return tokenizer.decode(out.sequences[0], skip_special_tokens=True)

@torch.no_grad
def beam_search(model, tokenizer, system_prompt, prompt, max_tokens=1000, num_beams=1, length_penalty=0.0):
  eos_token = tokenizer(tokenizer.eos_token).to(model.device)['input_ids'][0]

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
    
  unfinished = []
  finished = []

  first_inference = utils.get_next_token_logits(model=model, tokenizer=tokenizer, prompt=text)
  sorted_log, sorted_ind = torch.sort(first_inference, descending=True)

  for i in range(num_beams):
    curr_log = sorted_log[i]
    curr_token = sorted_ind[i]

    if curr_token == eos_token:
      finished += [(tokenizer.decode(curr_token), curr_log, 1)]
    else:
      unfinished += [(tokenizer.decode(curr_token), curr_log, sorted_ind[i])]

  cnt_iter = 0
  while len(finished) < num_beams:

    new_candidates = []
    logger.info(f'Finised {len(finished)} after {cnt_iter} iterations')
    for txt, score, last_token in unfinished:
      input = text + txt
      logits = torch.nn.functional.log_softmax(utils.get_next_token_logits(model=model, tokenizer=tokenizer, prompt=input))

      topk_scores, topk_tokens = torch.topk(logits, num_beams)
      for i in range(num_beams):
        curr_log = topk_scores[i]
        curr_token = topk_tokens[i]
        # logger.info(f'{tokenizer.decode(curr_token)} with {curr_log}')
        
        if curr_token != eos_token:
          new_candidates += [(txt + tokenizer.decode(curr_token), score + curr_log, curr_token)]
        else:
          new_candidates += [(txt, score + curr_log, curr_token)]
    
    seq_len = cnt_iter + 2
    new_candidates.sort(key=lambda x: x[1], reverse=True)
    # for x in new_candidates:
    #   logger.info(f'new_candidates with {x[1]} score: {x[0]}')

    unfinished = []
    for i, (txt, score, last_token) in enumerate(new_candidates):
      if len(unfinished) == num_beams:
        break
      
      if (seq_len > max_tokens or last_token == eos_token) and i < num_beams:
        finished += [(txt, score, seq_len)]
      else:
        unfinished += [(txt, score, last_token)]

    cnt_iter += 1

  finished.sort(key=lambda x: x[1] / (x[2]**length_penalty), reverse=True)

  logger.info('Beam search results:')
  for x in finished:
    logger.info(f'best generate with {x[1] / (x[2]**length_penalty)} score: {x[0]}')

  return finished[0][0], finished[0][2]
  


