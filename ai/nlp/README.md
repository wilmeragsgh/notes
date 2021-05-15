---
description: NLP Knowledge and experiences
---

# NLP



### Python

```python
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
# instantiate an ngram counter
counts = CountVectorizer(analyzer='word', ngram_range=(n,n))

# create a dictionary of n-grams by calling `.fit`
vocab2int = counts.fit([a_text, s_text]).vocabulary_
```



## Resources

- [CS 224N](http://web.stanford.edu/class/cs224n/)  (Don't remember why i need this: 51506490)
- https://www.fast.ai/
- [Intro to TensorFlow for Deep Learning \| Udacity](https://www.udacity.com/course/intro-to-tensorflow-for-deep-learning--ud187)
- [Embedding projector - visualization of high-dimensional data](https://projector.tensorflow.org/)
- [LDA visualized using t-SNE and Bokeh \| Kaggle](https://www.kaggle.com/yohanb/lda-visualized-using-t-sne-and-bokeh)
- [(PDF) Classification of Twitter Users Who Tweet About E-Cigarettes](https://www.researchgate.net/publication/320051140_Classification_of_Twitter_Users_Who_Tweet_About_E-Cigarettes)
- [Visualizing Top Tweeps with t-SNE, in Javascript](http://karpathy.github.io/2014/07/02/visualizing-top-tweeps-with-t-sne-in-Javascript/)
