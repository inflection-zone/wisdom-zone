# Support Vector Machine (SVM)

- **Supervised** learning model
- Used for both **classification** and **regression**
- Predominantly used for **binary classification**

## SVM Classifier

SVM maps training datapoints in space so as to **maximize the gap**   (margin) between the categories. 
The best boundary that separates the data points into classes is called a **hyperplane**.
The new points will be classified based off on which side of the hyperplane the fall.
The points closest to the hyperplane are called **support vectors**.
The separation gap between the two lines on the closest data points. is called the **margin**.

<img src="svm_terms.png" width="400?"/> 

---
We can understand this concept more with the help of a **heart related dataset**. This dataset can be found on kaggle: https://www.kaggle.com/datasets/nareshbhat/health-care-data-set-on-heart-attack-possibility

But first we need to import the dependencies:

### Importing dependencies

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from sklearn.svm import SVC
```

The dataset looks like this:

<img src="data.png" width="600"/> 

It consists 303 observations and 14 features. There are no null values. 

### Classification categories

> `target = 1` represents the patient is in risk of a heart attack and `target = 0` represents they are safe.

---
Lets find out the **number of observations** in each category by plotting a countplot using seaborn using the code:

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

This plot shows that the range of the data in this dataset is quite uneven and there is an outlier in the cholestrol feature. Removing this outlier can increase the accuracy of the model.

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
### Feature Scaling

SVM tries to maximize the distance between the separating plane and the support vectors. If one feature (i.e. one dimension in this space) has very large values, it will dominate the other features when calculating the distance. If we rescale all features in a certain range, they all have the same influence on the distance metric and thus, improve the accuracy of the algorithm dramatically.

```python
X = df.drop(columns = 'target')
y = df['target']

X_std = StandardScaler().fit_transform(X)
X_std = pd.DataFrame(X_std, columns = list(X.columns))
```

Now our boxenplot looks like this:

<img src="boxenplot_scaled.png" width="550"/> 

---
#### Splitting data into training and testing sets

```python
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size = 0.2, random_state = 13, stratify = y)
```

---
#### Model Fitting and Training

```Python
model = SVC()
model.fit(X_train, y_train)
```
#### Checking the training and testing accuracy scores:

```Python
print(model.score(X_train, y_train), model.score(X_test, y_test))
```
> Training accuracy score : **90.0** <br> Testing accuracy score : **95.1**

#### Classification Report

```Python
print(classification_report(y_test, model.predict(X_test)))
```

<img src="classification_report.png" width="450"/> 

#### Confusion matrix

```Python
cm = confusion_matrix(y_test, model.predict(X_test))
sns.heatmap(cm, annot = True, cmap = 'Blues')
```

<img src="confusion_matrix.png" width="300"/> 

### Summary

> SVM is a **simple** and **accurate model** if given a right quality dataset. <br>
> **Not** suitable for **large datasets** due to increased training time. <br>
> Works well with datasets with show a **clear margin of separation** between classes. <br>
> **Not** suitable for **noisy** datasets with **overlapping classes**. <br>
> It tends to be sensitive to the **scale of data**. <br>
> Works well with **high dimensional data**.

