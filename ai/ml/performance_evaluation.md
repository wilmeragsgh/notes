---
description: Frecuently used techniques for performance evaluation
---

# Performance evaluation

## Metrics

**Gini**

- **Definition:** Indicates how discriminative is the model (predictive power)
- **Possible values:** 
  - 0 would indicate no discrimination based features to make a choice.
  - 1 would indicate the model is completely relying on features as discriminators to make a choice (desirable for banks for example)

**KS statistic**

- **Definition:** Indicates the maximum distance between distribution functions (classes samples in supervised learning) of two samples (empirical, or one reference).
- **Possible values:**
  - 0 would indicate no distinction on the two samples (no difference in label A-label B scores).
  - 1 would indicate Maximum distance between the two samples.

**Student's t-test**

- **Definition:** Indicates how likely a set of samples came from the exact same distribution (P-value). P-Value can be compared with a threshold call statistical significance (e.g. .05).
- **Possible values:**
  - P-Value < 0.05, indicate we can reject the null hypothesis that the two samples are coming from the exact same distribution.

- **Comment:** Samples must be shaped in a normal distribution.