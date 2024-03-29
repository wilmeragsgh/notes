---
description: Xgboost related knowledge and experiances
---

# xgboost

## Parameters

The overall parameters have been divided into 3 categories by XGBoost authors:

* **General Parameters**: Guide the overall functioning
* **Booster Parameters**: Guide the individual booster \(tree/regression\) at each step
* **Learning Task Parameters**: Guide the optimization performed

### General parameters

* booster \[default=gbtree\] Select the type of model to run at each iteration. It has 2 options:
  * gbtree: tree-based models
  * gblinear: linear models
* silent \[default=0\]: Silent mode is activated if set to 1, i.e. no running messages will be printed. It’s generally good to keep it 0 as the messages might help in understanding the model.
* nthread \[default to maximum number of threads available if not set\] This is used for parallel processing and number of cores in the system should be entered. If you wish to run on all cores, value should not be entered and algorithm will detect automatically

### Booster parameters \(gbtree\)

Though there are 2 types of boosters, I’ll consider only tree booster here because it always outperforms the linear booster and thus the later is rarely used.

- **eta** [default=0.3]
Makes the model more robust by shrinking the weights on each step
Typical final values to be used: 0.01-0.2

- **min_child_weight** [default=1]
Defines the minimum sum of weights of all observations required in a child.
This refers to min “sum of weights” of observations.
Used to control over-fitting. Higher values prevent a model from learning relations which might be highly specific to the particular sample selected for a tree.
Too high values can lead to under-fitting hence, it should be tuned using CV.

- **max_depth** [default=6]
Used to control over-fitting as higher depth will allow model to learn relations very specific to a particular sample.
Should be tuned using CV.
Typical values: 3-10

- **max_leaf_nodes**
The maximum number of terminal nodes or leaves in a tree.
Can be defined in place of max_depth. Since binary trees are created, a depth of ‘n’ would produce a maximum of 2^n leaves.
If this is defined, GBM will ignore max_depth.

- **gamma** [default=0]
A node is split only when the resulting split gives a positive reduction in the loss function. Gamma specifies the minimum loss reduction required to make a split.
Makes the algorithm conservative. The values can vary depending on the loss function and should be tuned.

- **max_delta_step** [default=0]
In maximum delta step we allow each tree’s weight estimation to be. If the value is set to 0, it means there is no constraint. If it is set to a positive value, it can help making the update step more conservative.
Usually this parameter is not needed, but it might help in logistic regression when class is extremely imbalanced.
This is generally not used but you can explore further if you wish.

- **subsample** [default=1]
Same as the subsample of GBM. Denotes the fraction of observations to be randomly samples for each tree.
Lower values make the algorithm more conservative and prevents overfitting but too small values might lead to under-fitting.
Typical values: 0.5-1

- **colsample_bytree** [default=1]
Similar to max_features in GBM. Denotes the fraction of columns to be randomly samples for each tree.
Typical values: 0.5-1

- **colsample_bylevel** [default=1]
Denotes the subsample ratio of columns for each split, in each level.
I don’t use this often because subsample and colsample_bytree will do the job for you. but you can explore further if you feel so.

- **lambda** [default=1]
L2 regularization term on weights (analogous to Ridge regression)
This used to handle the regularization part of XGBoost. Though many data scientists don’t use it often, it should be explored to reduce overfitting.

- **alpha** [default=0]
L1 regularization term on weight (analogous to Lasso regression)
Can be used in case of very high dimensionality so that the algorithm runs faster when implemented

- **scale_pos_weight** [default=1]
A value greater than 0 should be used in case of high class imbalance as it helps in faster convergence.

These parameters are used to define the optimization objective the metric to be calculated at each step.

* objective \[default=reg:linear\] This defines the loss function to be minimized. Mostly used values are:
  * binary:logistic –logistic regression for binary classification, returns predicted probability \(not class\)
  * multi:softmax –multiclass classification using the softmax objective, returns predicted class \(not probabilities\)

    you also need to set an additional num\_class \(number of classes\) parameter defining the number of unique classes

  * multi:softprob –same as softmax, but returns predicted probability of each data point belonging to each class.
* eval\_metric \[ default according to objective \] The metric to be used for validation data. The default values are rmse for regression and error for classification. Typical values are:
  * rmse – root mean square error
  * mae – mean absolute error
  * logloss – negative log-likelihood
  * error – Binary classification error rate \(0.5 threshold\)
  * merror – Multiclass classification error rate
  * mlogloss – Multiclass logloss
  * auc: Area under the curve
* seed \[default=0\] The random number seed. Can be used for generating reproducible results and also for parameter tuning.

If you’ve been using Scikit-Learn till now, these parameter names might not look familiar. A good news is that xgboost module in python has an sklearn wrapper called XGBClassifier. It uses sklearn style naming convention. The parameters names which will change are:

eta –&gt; learning\_rate lambda –&gt; reg\_lambda alpha –&gt; reg\_alpha You must be wondering that we have defined everything except something similar to the “n\_estimators” parameter in GBM. Well this exists as a parameter in XGBClassifier. However, it has to be passed as “num\_boosting\_rounds” while calling the fit function in the standard xgboost implementation.


### Other recommendations

**If overfitting:**

- Lower `max_depth` , `subsample` , `colsample_bytree` , 
- Increase `gamma`,`eta` , `min_child_weight` , `lambda` and or `alpha`,

**If underfitting:**

- Incrementar `max_depth` (compute intense), `scale_pos_weight` ,
- Disminuir `lambda` and or `alpha`,

**Unbalanced datasets**

- Incrementar `max_delta_step` (start with 1-10), `base_score` (set with the proportions of positive class ie label = 1)

**Misc recommended defaults**

- `seed` =42 (consistency is preferred), `eval_metric` include (`logloss` y `auc`)



**Note**
To predict one:

```python
for index in enumerate(observations):
    model.predict( pd.DataFrame( [input_features.iloc[index].to_dict()], columns=model_columns ) )[0]
```

---

## Notes

Buenos días equipo sobre los casos en que no funcionen bien los modelos, les aconsejo seguir la siguente metodología:Una vez entrenado el modelo en training(70% de la muestra inicial):

- Probar modelo sobre el mismo training set, si el modelo se porta bien continua al siguiente punto. Si no, hay que hacer el modelo más complejo por ejemplo probando más valores en los hiperparámetros.
- Probar modelo sobre el validation set (15% de la muestra inicial), si el modelo se porta lo suficientemente bien continua con el test set. Si no, entonces hay que aplicar alguna medida de regularización.
- Predecir sobre el test set (15% final de la muestra inicial), si el modelo se porta bien está listo. Si no, hay que probar con una muestra diferente de validation set para que tenga una muestra que contenga ejemplos más representativos de la muestra.

**Los siguientes parámetros sirven para cuando el modelo está sobreajustado:**

- Disminuir `max_depth` , `subsample` , `colsample_bytree` , 
- Incrementar el `gamma`,`eta` , `min_child_weight` , `lambda` and or `alpha`,

**Los siguientes parámetros sirven para cuando el modelo está subajustado:**

- Incrementar `max_depth` (esto consume mas recursos), `scale_pos_weight` ,
- Disminuir `lambda` and or `alpha`,

**Datos muy desbalanceados**

- Incrementar `max_delta_step` (comenzar con valores entre 1-10), `base_score` (fijar con la proporción de valores de la clase positiva, ie etiqueta = 1)

**Otros parámetros recomendados por defecto**

- `seed` =42 (lo importante es que todos usemos el mismo), `eval_metric` que incluya (`logloss` y `auc`)

Hey team hoy estuve trabajando con los datos de Produbanco (el primer corte de datos que enviaron) y hay algunas cosas que creo que podemos considerar:Si los datos de un cliente tienen:

- Menos de 30% y más de 10% de observaciones de default, es recomendable tratarlo como un dataset desbalanceado.
- Menos de 10% y más de 5% de observaciones de default, es recomendable hacer más abiertos los intervalos de pbounds para evaluar factibilidad de creación del modelo con tal desbalanceo.
- Menos de 5% de observaciones de default, es recomendable solicitar más datos de default al cliente.

Al procesar datos desbalanceados es recomendable que utilizar `scoring='balanced_accuracy'` en la llamada a la función cross_val_score, así mismo fijar el valor del parámetro `scale_pos_weight` con el valor dado por n_obs_negatives / n_obs_positives , en general sí hay menos de 5% de desbalanceo es mejor usar 10 * proporción de valores no default (por ejemplo si solo hay 2% de valores default se usaría 9.8 cómo valor de `scale_pos_weight`). En estos escenarios también es útil flexibilizar las ejecuciones del optimizador cambiando los parametros a la llamada de maximize incrementando los parámetros `init_points` y `n_iter` específicamente.Observaciones:Es importante asegurar de pasar todos los parámetros usados dentro de la función `xgboost_hyper_param` a la instancia de `XGBClassifier` que se crea luego de finalizar el optimizador, recuerden `optimizer.max['params']` solo tendrá los parámetros que el optimizador tiene cómo entradas, entonces hay que pasar manualmente los que fijamos, (por ejemplo `scale_pos_weight`)



## References

* [Code](https://xgboost.readthedocs.io/en/latest/tutorials/model.html) , [Python API Reference](https://xgboost.readthedocs.io/en/latest/python/python_api.html)
* [Paper](https://arxiv.org/pdf/1603.02754.pdf)
* [Winning solution for](https://github.com/dmlc/xgboost/tree/master/demo#machine-learning-challenge-winning-solutions)
* [Some FAQs](https://towardsdatascience.com/20-burning-xgboost-faqs-answered-to-use-the-library-like-a-pro-f8013b8df3e4)

