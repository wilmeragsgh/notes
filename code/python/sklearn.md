---
description: Frecuently used commands for sklearn
---

# Sklearn

## Recipes

**Generating confusion matrix**

```python
from sklearn.metrics import confusion_matrix
y_true = [2, 0, 2, 2, 0, 1]
y_pred = [0, 0, 2, 2, 0, 2]
confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = confusion_matrix([0, 1, 0, 1], [1, 1, 1, 0]).ravel()
```

**Generating training/test set**

```python
import numpy as np
from sklearn.model_selection import train_test_split
X, y = np.arange(10).reshape((5, 2)), range(5)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
```

**Gini calculation**

```python
import numpy as np
from sklearn import metrics
fpr, tpr, thresholds = metrics.roc_curve(label, score, pos_label=1)
2 * metrics.auc(fpr, tpr) - 1
```

**KS statistics**

```python
from scipy.stats import ks_2samp 
ks_2samp(dt[dt['label']== 0]['score'],dt[dt['label']== 1]['score']) # classes 0, 1
```

**Filtering best f1 model**

```python
import pandas as pd
y_pred = model.predict_proba(X_test)
y_score = [y[1] for y in y_pred]

model_performance = pd.DataFrame({"accuracy":[],"precision":[],"recall":[],"f1":[],"cut":[]})
for x in range(0,100):
    pred = [1 if y > (x*0.01) else 0 for y in y_score]
    acc = (y_test == pred).mean()
    prec = sum(np.multiply(y_test,pred)) / (sum( np.multiply([ 1 - pr for pr in y_test], pred)) + sum(np.multiply(y_test,pred)))
    reca = sum(np.multiply(y_test,pred)) / (sum( np.multiply([ 1 - pr for pr in pred], y_test)) + sum(np.multiply(y_test,pred)))
    f_1 = 2 * prec * reca/ (prec + reca)
    model_performance = model_performance.append({
        "accuracy": acc,
        "precision": prec,
        "recall": reca,
        "f1": f_1,
        "cut": x
    }, ignore_index=True)
model_performance

model_performance.iloc[model_performance['f1'].idxmax()]
```



**Random search of parameters**

```python
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

params = {
    'min_child_weight': [1, 5, 7, 10],
    'gamma': [0.5, 1, 1.5, 2, 5],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'max_depth': [3, 4, 5]
}

xgb = XGBClassifier(learning_rate=0.02,
                    n_estimators=600,
                    objective='binary:logistic',
                    silent=True,
                    nthread=1)

folds = 3
param_comb = 5
skf = StratifiedKFold(n_splits=folds, shuffle = True, random_state = 1001)
random_search = RandomizedSearchCV(xgb, param_distributions=params, n_iter=param_comb,
                                   scoring='roc_auc', n_jobs=4, cv=skf.split(X_train,y_train),
                                   verbose=3, random_state=42)
random_search.fit(X_train,y_train)
print('\n Best hyperparameters:')
print(random_search.best_params_)
```



**Bayesian optimization**

```python
#pip install bayesian-optimization
import numpy as np
from xgboost import XGBClassifier
from bayes_opt import BayesianOptimization
from sklearn.model_selection import cross_val_score

pbounds = {
    'learning_rate': (0.01, 1.0),
    'n_estimators': (100, 1000),
    'max_depth': (3,10),
    'subsample': (1.0, 1.0),  # Change for big datasets
    'colsample': (1.0, 1.0),  # Change for datasets with lots of features
    'gamma': (0, 5)}

def xgboost_hyper_param(learning_rate,
                        n_estimators,
                        max_depth,
                        subsample,
                        colsample,
                        gamma):
    max_depth = int(max_depth)
    n_estimators = int(n_estimators)
    clf = XGBClassifier(
        max_depth=max_depth,
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        gamma=gamma)
    return np.mean(cross_val_score(clf, X_train, y_train, cv=3, scoring='roc_auc'))

optimizer = BayesianOptimization(
    f=xgboost_hyper_param,
    pbounds=pbounds,
    random_state=1,
)

optimizer.maximize(init_points=2, n_iter=3)
print(optimizer.max)
```



## References

- [Automated Machine Learning Hyperparameter Tuning in Python](https://towardsdatascience.com/automated-machine-learning-hyperparameter-tuning-in-python-dfda59b72f8a)