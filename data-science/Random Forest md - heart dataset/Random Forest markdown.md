# Random Forest 

- **Supervised** learning model
- Ensemble learning model used for both **classification** and **regression**
    - **Classification**: Output is class predicted by **majority** of the trees
    - **Regression**: Output is the **mean/average** of predictions of all individual trees
- Random Forest Algorithm corrects the problem of **overfitting** in Decision Tree Algorithm


## Random Forest Classifier

A random forest classifier works with data having discrete labels or better known as class. 

_**Example**: Let us now build a Random Forest Model for say buying a car._

The trees are built with a **random subset of data points** and their own set of **random features** and each tree would execute independently to provide its decision.

<img src="example.png" width="500"/> 

Assuming the Decision Tree 1 suggests ‘Buy’, Decision Tree 2 Suggests ‘Don’t Buy’ and Decision Tree 3 suggests ‘Buy’, then the **max vote** would be for Buy and the result from Random Forest would be to ‘Buy’

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

from sklearn.ensemble import RandomForestClassifier
```

This is what the dataset looks like:

<img src="data.png" width="600"/> 

It consists 303 observations and 14 features. There are no null values. 

---
### Classification categories

> `target = 1` represents the patient is in risk of a heart attack and `target = 0` represents they are safe.</br>

Lets find out the **number of observations** in each category by plotting a countplot using seaborn using the code:

```python
ax = sns.countplot(data = df, x = 'target', palette = ['green', 'orange'])
ax.bar_label(ax.containers[0])
```

<img src="countplot_obs.png" width="350"/> 

---
### Duplicate data points

We have 1 duplicate data point in the dataset. Duplicate values can put weight on the nodes and **can make them biased**. So, its better to drop them.

```python
df.drop_duplicates(inplace = True)
```

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

#### Range of data

This plot shows that the range of the data in this dataset is quite uneven. But _feature scaling_ is not required as Random Forest uses a _rule-based approach_.

#### Outliers

The plot indicates that there is an outlier in the _cholestrol_ feature. Usually, outliers have a negligible effect with dealing with tree-based models because the nodes are determined based on sample proportions in each split region and not on their absolute values. That being said, if the dataset is small, it might still have an impact.

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
#### Separating independent and dependent variables

```python
X = df.drop(columns = 'target')
y = df['target']
```

---
#### Splitting data into training and testing sets

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 8, stratify = y)
```

---
#### Model Fitting and Training

```Python
model = RandomForestClassifier()
model.fit(X_train, y_train)
```

---
#### Checking the training and testing accuracy scores:

```Python
print(model.score(X_train, y_train), model.score(X_test, y_test))
```
> Training accuracy score : **100.0** <br> Testing accuracy score : **91.8**

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

> Random Forest uses **averaging** to improve the predictive accuracy and **control over-fitting**. <br>
> The features are always **randomly permuted** at each split. Thus, the **best found split may vary** even with the same training data and features. <br>
> **Normalizing of data is not required** as it uses rule-based approach. <br>
> This algorithm is usually **robust to outliers**. <br>


