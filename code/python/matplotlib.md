---
description: Frecuently used Matplotlib code
---

# Matplotlib

## Recipes

**Make the plot larger in notebook**

```python
# In the chunk you want to plot
import matplotlib.pyplot as plt
fig=plt.figure(figsize=(18, 16), dpi= 80, facecolor='w', edgecolor='k')
```

**Correlation plot**

```python
import seaborn as sns
corr = data.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);
ax
```

**2D plot of pandas dataframe**

```python
# data is DataFrame(pandas)
data.plot('A','B')
```