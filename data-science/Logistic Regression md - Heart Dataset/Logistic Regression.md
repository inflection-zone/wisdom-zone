# Logistic Regression

- **Supervised** learning model
- Used for **classification** problems
- Uses the concept of **Predictive Modeling**
- Fit **'S'** shaped logistic function

<img src="logistic.jpg" width="600"/>

## Logistic Function (Sigmoid Function)
- S-form curve is known by **Sigmoid function**
- Mathematical function map predicted value to probablity
- Value must be in range of **0** and **1**

### Types of Logistic Regression
- **Binomial** - Two possible value Eg.: (0/1), (True/False)
- **Mutlinomial** - Two or more unordered possible values Eg.: (Happy/Sad/Angry)
- **Ordinal** - Two or more ordred possible values Eg.: (Good/Better/Best) (Low/Medium/High)

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
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

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

Since Logistic Regression is very sensitive to range of data points.So we need to perform normalizing and scaling the training data to improve accuracy dramatically.

```python
X = df.drop(columns = 'target')
y = df['target']

X_std = StandardScaler().fit_transform(X)
X_std = pd.DataFrame(X_std, columns = list(X.columns))
```

Now our boxenplot looks like this:

<img src="boxenplot_scaled.png" width="550"/> 

---
### Splitting data into training and testing sets

```python
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.20, stratify = y, random_state = 14)
```
---
### Model Fitting and Training

```Python
model=LogisticRegression()
model.fit(X_train,y_train)
```
### Checking the training and testing scores:

```Python
print(model.score(X_train, y_train), model.score(X_test, y_test))
```
> Training accuracy score : 83.7 <br> Testing accuracy score : 93.4

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

> - **Logistic regression** may not be accurate if the **sample size** is too **small**. <br>
> - It works well for cases where the dataset is **linearly separable**. <br>
> - It is much **easier** to implement than other methods. <br>


```python

```
