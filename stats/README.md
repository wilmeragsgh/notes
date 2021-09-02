## Calculate confidence interval for classification performance metric

Asumming  a Gaussian distribution of the proportion

```python
interval = z * sqrt( (accuracy * (1 - accuracy)) / n)
```

z (for a given confidence level):

- 1.64 (90%)
- 1.96 (95%)
- 2.33 (98%)
- 2.58 (99%)

### Alternative approach

The example below demonstrates this function in a hypothetical case where a model made 88 correct predictions out of a dataset with 100 instances and we are interested in the 95% confidence interval (provided to the function as a significance of 0.05).

```python
from statsmodels.stats.proportion import proportion_confint
lower, upper = proportion_confint(88, 100, 0.05)
print('lower=%.3f, upper=%.3f' % (lower, upper))
```
