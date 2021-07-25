---
description: ML knowledge and experiences
---

# ML



**ML Workflows by company**

- [AWS](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html)
- [GCP](https://cloud.google.com/ai-platform/docs/ml-solutions-overview)
- [Azure](https://docs.microsoft.com/en-us/azure/machine-learning/overview-what-is-azure-ml)

## Some ideas

### Style transfer on text

- [GitHub - fuzhenxin/Style-Transfer-in-Text: Paper List for Style Transfer in Text](https://github.com/fuzhenxin/Style-Transfer-in-Text)

- [[1711.06861] Style Transfer in Text: Exploration and Evaluation](https://arxiv.org/abs/1711.06861)

- [[1808.04365] What is wrong with style transfer for texts?](https://arxiv.org/abs/1808.04365)

- [Unsupervised Text Style Transfer using Language Models as Discriminators](https://papers.nips.cc/paper/7959-unsupervised-text-style-transfer-using-language-models-as-discriminators)

- [What is wrong with style transfer for texts?](https://www.groundai.com/project/what-is-wrong-with-style-transfer-for-texts/1)

- [Bad Gateway – Medium](https://medium.com/@mukundan_8066/author-style-transfer-using-recurrent-neural-networks-c8c8f83b33cc)

## TL;DR

**Metrics by problem:**

- Classification Metrics (accuracy, precision, recall, F1-score, ROC, AUC, …)
- Regression Metrics (MSE, MAE)
- Ranking Metrics (MRR, DCG, NDCG)
- Statistical Metrics (Correlation)
- Computer Vision Metrics (PSNR, SSIM, IoU)
- NLP Metrics (Perplexity, BLEU score)
- Deep Learning Related Metrics (Inception score, Frechet Inception distance)

> Following sections are probably from a course if you find which one is (i don't remember) you can create a PR, thanks in advance.

**Trade-offs Between Cross-Validation and Train-Test Split**
Cross-validation gives a more accurate measure of model quality, which is especially important if you are making a lot of modeling decisions. However, it can take more time to run, because it estimates models once for each fold. So it is doing more total work.

Given these tradeoffs, when should you use each approach? On small datasets, the extra computational burden of running cross-validation isn't a big deal. These are also the problems where model quality scores would be least reliable with train-test split. So, if your dataset is smaller, you should run cross-validation.

For the same reasons, a simple train-test split is sufficient for larger datasets. It will run faster, and you may have enough data that there's little need to re-use some of it for holdout.

There's no simple threshold for what constitutes a large vs small dataset. If your model takes a couple minute or less to run, it's probably worth switching to cross-validation. If your model takes much longer to run, cross-validation may slow down your workflow more than it's worth.

Alternatively, you can run cross-validation and see if the scores for each experiment seem close. If each experiment gives the same results, train-test split is probably sufficient.

**Data leakage**
Data leakage is one of the most important issues for a data scientist to understand. If you don't know how to prevent it, leakage will come up frequently, and it will ruin your models in the most subtle and dangerous ways. Specifically, leakage causes a model to look accurate until you start making decisions with the model, and then the model becomes very inaccurate. This tutorial will show you what leakage is and how to avoid it.

There are two main types of leakage: Leaky Predictors and a Leaky Validation Strategies.

**Leaky Predictors**
This occurs when your predictors include data that will not be available at the time you make predictions.

For example, imagine you want to predict who will get sick with pneumonia. The top few rows of your raw data might look like this:

| got_pneumonia | age  | weight | male  | took_antibiotic_medicine | ...  |
| ------------- | ---- | ------ | ----- | ------------------------ | ---- |
| False         | 65   | 100    | False | False                    | ...  |
| False         | 72   | 130    | True  | False                    | ...  |
| True          | 58   | 100    | False | True                     | ...  |

People take antibiotic medicines after getting pneumonia in order to recover. So the raw data shows a strong relationship between those columns. But took_antibiotic_medicine is frequently changed after the value for got_pneumonia is determined. This is target leakage.

The model would see that anyone who has a value of False for took_antibiotic_medicine didn't have pneumonia. Validation data comes from the same source, so the pattern will repeat itself in validation, and the model will have great validation (or cross-validation) scores. But the model will be very inaccurate when subsequently deployed in the real world.

To prevent this type of data leakage, any variable updated (or created) after the target value is realized should be excluded. Because when we use this model to make new predictions, that data won't be available to the model.

**Leaky Validation Strategy**

A much different type of leak occurs when you aren't careful distinguishing training data from validation data. For example, this happens if you run preprocessing (like fitting the Imputer for missing values) before calling train_test_split. Validation is meant to be a measure of how the model does on data it hasn't considered before. You can corrupt this process in subtle ways if the validation data affects the preprocessing behavoir.. The end result? Your model will get very good validation scores, giving you great confidence in it, but perform poorly when you deploy it to make decisions.

**Preventing Leaky Predictors**

There is no single solution that universally prevents leaky predictors. It requires knowledge about your data, case-specific inspection and common sense.

However, leaky predictors frequently have high statistical correlations to the target. So two tactics to keep in mind:

To screen for possible leaky predictors, look for columns that are statistically correlated to your target.
If you build a model and find it extremely accurate, you likely have a leakage problem.
Preventing Leaky Validation Strategies
If your validation is based on a simple train-test split, exclude the validation data from any type of fitting, including the fitting of preprocessing steps. This is easier if you use scikit-learn Pipelines. When using cross-validation, it's even more critical that you use pipelines and do your preprocessing inside the pipeline.



**Important considerations when deploying**

Model versioning

Model monitoring

Model updating & routing (route between different model variants for comparison)

Predictions type:

- On-demand.
- Batch.

## Glosary

**hyperparameter** is a parameter whose value *cannot* be estimated from the data. [more info](https://scikit-learn.org/stable/modules/grid_search.html#)



## Resources

- [Building a Production Machine Learning Infrastructure](https://machinelearningmastery.com/building-a-production-machine-learning-infrastructure/)
- [Deploy Your Predictive Model To Production](https://machinelearningmastery.com/deploy-machine-learning-model-to-production/)
- [Introduction  \|  Introduction to Machine Learning Problem Framing  |  Google Developers](https://developers.google.com/machine-learning/problem-framing/)
- [Become a Machine Learning Engineer \| Udacity | Udacity](https://www.udacity.com/course/machine-learning-engineer-nanodegree--nd009t)
- [Machine learning education  \|  TensorFlow](https://www.tensorflow.org/resources/learn-ml)
- [Tune: a Python library for fast hyperparameter tuning at any scale](https://towardsdatascience.com/fast-hyperparameter-tuning-at-scale-d428223b081c)
- [Tune Examples — Ray 0.9.0.dev0 documentation](https://ray.readthedocs.io/en/latest/tune-examples.html)
- [ray-project/ray · GitHub](https://github.com/ray-project/ray/blob/master/python/ray/tune/examples/xgboost_example.py)
- [Tune Examples — Ray 0.9.0.dev0 documentation](https://ray.readthedocs.io/en/latest/tune-examples.html)
- [Cheatsheets](https://startupsventurecapital.com/essential-cheat-sheets-for-machine-learning-and-deep-learning-researchers-efb6a8ebd2e5)



**Other tools**

- https://dagshub.com/
- https://www.mlflow.org/docs/latest/concepts.html
- https://zenml.io/
- https://www.kubeflow.org/docs/distributions/microk8s/kubeflow-on-microk8s/

