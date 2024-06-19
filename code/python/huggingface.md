---
description: Frequently used code for huggingface related code snippets
---

# Huggingface

## Recipes

**Use logits from models**

```python
sentimodel = RobertaForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')
print(sentimodel.num_labels)
outputs = sentimodel(**inputs)
print(outputs.logits.softmax(dim=-1).tolist())
```