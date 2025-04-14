import torch

def get_next_token_logits(model, tokenizer, prompt):
  with torch.no_grad():
    tokens = tokenizer(prompt, return_tensors='pt').to(model.device)
    logits = model(**tokens).logits
    last_logits = logits[0, -1]

    return last_logits