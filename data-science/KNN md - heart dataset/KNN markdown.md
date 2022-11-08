# K Nearest Neighbors (KNN)

- **Supervised** learning model
- Used for both **classification** and **regression**
- Based on **feature similarity**

## KNN Classification

A new datapoint is classified based on the votes of its 'k' nearest neighbors measured in Euclidean distance. 

Example: Here we have chosen k to be 3 and thus, based on the majority of votes, the green point will be classified as a triangle.

<img src="example.png" width="200"/> 

---
We can understand this concept more with the help of a heart related dataset. This dataset can be found on kaggle: https://www.kaggle.com/datasets/nareshbhat/health-care-data-set-on-heart-attack-possibility

But first we need to import the dependencies:

### Importing dependencies

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from sklearn.neighbors import KNeighborsClassifier
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
### Feature Scaling

Since KNN algorithm, relies on distance for classification if the features show a vast difference in range of data (eg. age and cholestrol) sometimes due to their units, then normalizing and scaling the training data can improve accuracy dramatically.

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
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size = 0.2, stratify = y, random_state = 14)
```
---

### Value of k

- As k is the number of datapoint neighbors, it can only be a **positive integer**.
- If `k = 1`, then the new datapoint will be assigned to the class of that of the single nearest neighbor. 
- If `k = 11`, then we use the vote of 11 nearest neighbors to determine the class of our datapoint.
- The value of k should neither be too high nor too low.

#### Choosing the right value

Picking out the right value for k comes under a process called **parameter tuning** and is important for better accuracy.
To get it right, we need to run the algorithm several times with different values of k and choose the one with less errors and better accuracy.

We will accomplish this by the following code:

```python
train_score = []
test_score = []
k_value = []

for k in range(1,26):     
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(X_train, y_train)    
    k_value.append(k)
    train_score.append(knn.score(X_train, y_train))
    test_score.append(knn.score(X_test, y_test))
```

We have the training and testing scores for every k value ranging from **1 to 25**. We need to plot a graph to get a better look.

```python
plt.figure(figsize = (12,8))
plt.plot(k_value, train_score, label = 'Training Accuracy')
plt.plot(k_value, test_score, label = 'Testing Accuracy')
plt.legend()
plt.title('Accuracy Graph for different values of k')
plt.xlabel('Number of Neighbors')
plt.ylabel('Accuracy Score (Train and Test)')
plt.xticks(k_value)
plt.grid(linestyle = '--')
plt.show()
```
<img src="choice_of_k.png" width="600"/> 

Best accuracy is given by `k=7`

---
#### Model Fitting and Training

```Python
knn = KNeighborsClassifier(n_neighbors = 7)
knn.fit(X_train, y_train)
```
#### Checking the training and testing scores at `k=7`:

```Python
print(knn.score(X_train, y_train), knn.score(X_test, y_test))
```
> Training accuracy score : 87.2 <br> Testing accuracy score : 93.4

#### Classification Report

```Python
print(classification_report(y_test, knn.predict(X_test)))
```

<img src="classification_report.png" width="450"/> 

#### Confusion matrix

```Python
cm = confusion_matrix(y_test, knn.predict(X_test))
sns.heatmap(cm, annot = True, cmap = 'Blues')
```

<img src="confusion_matrix.png" width="300"/> 

### Summary

> KNN is a **quick**, **simple** and **accurate model** if given a right quality dataset. <br>
> It works better with **smaller** and **noise-free** datasets. <br>
> It tends to be sensitive to the **scale of data**. <br>
> **Optimal value of k** can be found by running the algorithms several times with different values.



