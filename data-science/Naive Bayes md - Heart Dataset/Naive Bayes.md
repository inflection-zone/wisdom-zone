# Naive Bayes

- **Supervised** learning model
- Used for **classification** problems
- Used to find which label belongs to any point.
- Base on **Bayes Theorem**
<img src="naive.png" width="600"/>

## Formula:
#### P(Y|X) = P(X|Y)*P(Y)/P(X)
- **P(Y|X)**: probability of Y according to X
- **P(X|Y)**: likelihood
- **P(Y)**: prior probability
- **P(X)**: marginal likehood

---
We can understand this concept more with the help of a heart related dataset. This dataset can be found on kaggle: https://www.kaggle.com/datasets/nareshbhat/health-care-data-set-on-heart-attack-possibility

### Importing dependencies
```python
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

```


The dataset looks like this:

<img src="data.png" width="600"/> 

It consists 303 observations and 14 features. There are no null values. 
> `target = 1` represents the patient is in risk of a heart attack and `target = 0` represents they are safe.

---
Lets find out the number of observations in each category by plotting a countplot using seaborn using the code:

```python
ax = sns.countplot(data = df, x = 'target', palette = 'hls')
ax.bar_label(ax.containers[0])
```

<img src="countplot_obs.png" width="350"/> 

---

### Range of data and Outliers

Now, we need to plot a **boxenplot** which will show us the range of data of each parameter and if there are any outliers.

```python
plt.figure(figsize = (12,6))
sns.boxenplot(data = df.drop(columns = 'target'))
plt.xticks(rotation = 30)
plt.show()
```

<img src="boxenplot.png" width="550"/> 

This plot shows that the range of the data in this dataset is quite uneven and there is an outlier in the cholestrol feature but in case of medical records, removing an outlier observation is not a good idea.

---
### Handling the outlier

In Gaussian Naive Bayes, outliers will affect the shape of the Gaussian distribution and have the usual effects on the mean. So its better to remove outliers.

We can remove the observation with this outlier with the following code:

```python
df.loc[df['chol']==df['chol'].max()]
```
> <img src="outlier.png" width="550"/> 

```python
df.drop(85, axis = 0, inplace = True)
```
---
### Scaling the data

As Naive Bayes algorithm is based on probability not on distance, so it doesn't require feature scaling.

---
### Splitting data into training and testing sets

```python
X = df.drop(columns = 'target')
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.30, stratify = y, random_state = 14)
```
---
### Model Fitting and Training

```Python
model=GaussianNB()
model.fit(X_train,y_train)
```
### Checking the training and testing scores:

```Python
print(model.score(X_train, y_train), model.score(X_test, y_test))
```
> Training accuracy score : 84.2 <br> Testing accuracy score : 86.8

### Classification Report

```Python
print(classification_report(y_test, model.predict(X_test)))
```

<img src="classification_report.png" width="450"/> 

### Confusion matrix

```Python
cm = confusion_matrix(y_test, model.predict(X_test))
sns.heatmap(cm, annot = True, cmap = 'Blues')
```

<img src="confusion_matrix.png" width="350"/> 

---
## Summary

> - It is **simple** and **easy** to implement.<br>
> - It doesn’t require as much **training data**.<br>
> - It is **highly scalable** with the number of predictors and data points.<br>
> - It is **fast** and can be used to make real-time predictions. <br>


```python

```
