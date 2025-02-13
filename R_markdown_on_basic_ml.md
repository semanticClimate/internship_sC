---
title: "Machine Learning on Iris dataset using R"
author: "Anudev"
date: "`r Sys.Date()`"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(
  message = FALSE,
  warning = FALSE,
  fig.align = "center")
```

## Introduction

This R markdown file demonstrate how to build and evaluate two machine learning models using the famous iris data set.

The models we are going to discuss are:\

-   Decision tree
-   Logistic Regression

Creating machine learning models usually involves the following processes:\

**1.Exploratory data analysis:** Exploring the data to find important patterns and to help out with feature engineering.\
**2.Feature engineering:** Creating new variables out of existing ones.\
**3.Handling missing values:** Deciding what to do with missing values in the data.\
**4.Machine learning:** Creating predictive model.\
**5.Prediction:** Using machine learning model to make prediction.\

Usually steps 1-3 take the longest while actually creating the model takes much less time. For this particular situation we will skip feature engineering and treating missing values as these steps are not necessary with our data, however, with real world data these steps are usually needed and also an important part of the process.\

## Load the necessary packages

First we need to load all the necessary packages that we are going to use for our analysis.\

```{r}
library(ggplot2) # Data visualization
library(psych) # Used for correlation visualizations
library(rattle) # Graphing decision trees
library(caret) # Machine learning
```

Let's load iris data. This data set is part of the base data sets built-in in **R**, hence, we do not need to load it externally.

```{r}
#chunk3
data("iris")
```

## Taking a glance at the data {.tabset .tabset-fade}

Lets check the first 6 rows as well as the summary statistics of our data to get a feel of how the data looks.

### Head {.unnumbered}

```{r}
head(iris, n=15)
```

### Summary {.unnumbered}

```{r}
#chunk4
summary(iris)
```

<br>

# Exploratory data analysis {.tabset .tabset-fade}

Let's do some exploratory data analysis to visually investigate and find patterns and insight into our data. This step can help us understand the data better and prepare us for creating our model later.

## Correlation matrix

A correlation matrix is a rectangular array that shows the correlation coefficients between all possible pairs of variables in a data set. Each cell in the matrix represents the correlation between two variables.\

Lets create a correlation matrix using the `pairs.panels()` function from the PSYCH package to see how our variables correlate.\

```{r}
#chunk5
pairs.panels(
  iris[,1:4], # Our data
  scale = TRUE, # Changes the size of the correlation value labels based on strength
  hist.col = 'grey85', # Histogram color
  bg = c("mediumseagreen","orange2","mediumpurple1")[iris$Species], # Colors of the Species levels.
       pch = 21, # The plot characters shape and size.
       main = 'Correlation matrix of Iris data')  # Title.
```

-   Here the diagonal boxes represents the histogram of the individual features. 

-   The lower left section represents the scatter plots where each point represents a species of iris flowers, visualizing the relationship between two features.

-   The upper right part section represents correlation coeffcient (from -1 to 1) between features.

### Explanation of Each Box

-   Histograms: These summarize the distribution of a single feature.\

For example, the top-left box shows the histogram of Sepal.Length, representing how frequently certain sepal lengths occur in the dataset.

-   Lower-Left Boxes (Scatter Plots): These plots show the relationships between pairs of features.

For example, Sepal.Length vs Sepal.Width: The plot in the second row, first column, shows the relationship between the length and width of the sepal. Each point is colored by species. The trend is weak, with points scattered, indicating a low correlation.

-   Upper-Right Boxes (Correlation Coefficients): These numbers measure the strength of the relationship between features

for example, 0.87 (Sepal.Length vs Petal.Length): A very strong positive correlation and -0.43 (Sepal.Width vs Petal.Length): A moderate negative correlation, meaning that as Sepal.Width increases, Petal.Length tends to decrease.

<br>

## Sepal width {.unnumbered}

**Box plot of Sepal width:**\
(A box plot is a graphical representation of data that displays the distribution through five key summary statistics: minimum, first quartile, median, third quartile, and maximum, often highlighting outliers.)

```{r}
#chunk6
ggplot(data = iris, # Load the data
       mapping = aes(x = Species, y = Sepal.Width, #Specify X and Y variables
                     fill = Species)) + # 'fill' color separates our Species levels
       geom_boxplot() + # Species that we want a box plots
       scale_fill_brewer(palette = 'Dark2') + # Change the color of the box plot
       theme_light() + # set light theme
       labs(title = 'Box plot of Sepal width for each species' ,
              x = 'Species' , y = 'Sepal width') # Assign a title, axes name
```

From this box plot it can be seen that the *Setosa* species has a higher sepal width median and interquartile range compared to the other two species. In contrast, the *Versicolor* and *Virginica* show quite a bit of overlap with each other in term of their interquartile range. This will make it harder for a machine learning algorithm to distinguish between the two species levels when predicting using this variable.

<br>

## Sepal length {.unnumbered}

**Box plot of Sepal length:**\

```{r}
#chunk7
ggplot(data = iris,
       mapping = aes(x = Species, y = Sepal.Length, fill = Species)) +
       geom_boxplot() + 
       scale_fill_brewer(palette = 'Dark2') + 
       theme_light() +
       labs(title = 'Box plot of Sepal length for each species',
            x = 'Species', y = 'Sepal length')
```

The ranges of the three species seem to somewhat overlap on the sepal length variable. However, their medians seem like they differ (at least visually. We don't know if they're statistically significantly different--we could test for this, but it is not necessary for the purposes of this exercise).

<br>

## Petal width {.unnumbered}

**Box plot of Petal width:**\

```{r}
#chunk8
ggplot(data = iris,
       mapping = aes(x = Species, y = Petal.Width, fill = Species)) +
       geom_boxplot() + 
       scale_fill_brewer(palette = 'Dark2') + 
       theme_light() +
       labs(title = 'Box plot of Petal width for each species',
            x = 'Species', y = 'Petal width')
```

This box plot seems to indicate quite a difference in petal width between the species.

<br>

## Petal length {.unnumbered}

**Box plot of Sepal length:**\

```{r}
#chunk9
ggplot(data = iris,
       mapping = aes(x = Species, y = Petal.Length, fill = Species)) +
       geom_boxplot() + 
       scale_fill_brewer(palette = 'Dark2') + 
       theme_light() +
       labs(title = 'Box plot of Petal length for each species',
            x = 'Species', y = 'Petal length')
```

This plot seems to indicate that the three species vary in terms of interquartile range on petal length. The setosa seems to have a very narrow interquartile range and have quite a lot shorter petal length compared to the other two species.

<br>

# Data partitioning

Before we begin to train our machine learning model we need to divide our data set into train and test subset. The train set is used for teaching or "training" our machine learning model how to make predictions with our data, while the test data set is used to test our model on data it has not seen in order to see how it performs.\

First, lets set a random seed. This will ensure that we will be able to replicate our results when we rerun our analysis.\

```{r}
#chunk10
set.seed(222)
```

Next, we will create train/test partition with `createDataPartition()` from the CARET package. This will split our data through random sampling within our species levels and give us the sampled index.\

```{r}
#chunk11
train_index <- createDataPartition(y = iris$Species, # y = dependent variable.
                                   p = .7, # Species split into 70% training set and 30% testing set 
                                   list = FALSE, #  Sets results to matrix form
                                   times = 1) # Sets number of partitions to be created, which is 1 in this case
```

Now we can split our data into train and test data using the randomly sampled `train_index` that we just formed.\

```{r}
#chunk12
train_data <- iris[train_index,] # Use train_index of iris data set to create train_data
test_data <- iris[-train_index,] # Use whatever the is not in train_index to create test_data
```

<br>

# Machine Learning

It is finally time to create machine learning models in order to predict which category of species (setosa, versicolor, virginica) each iris flower belongs to.

## **Decision tree**

<font size ="4"> **Quick facts:** </font>

-   **Uses:** classification and regression\
-   **How it works:** A decision tree uses input variables to create branches of decisions to ultimately derive a prediction.
-   **Pros:** (1) easy to interpret, (2) can handle both numeric and categorical data, (3) good at dealing with outliers, (4) doesn't have assumptions regarding the data (e.g., the data distribution)
-   **Cons:** (1) can overfit to train data, (2) susceptible to variance such that small input differences can result in different prediction models

<br>

Evaluate the Decision tree model with a 10 fold cross validation

```{r}
#chunk13
fitControl <- trainControl(method = "cv", number = 10, savePredictions = TRUE)
```

<br>

Create a predictor model with `train()` from CARET package. Specify `method = 'rpart'` to run the decision tree model

```{r}
#chunk14
# Create model
dt_model <- train(Species ~ ., # Set Y variable followed by '~'. The period indicates to include all variables for prediction. 
                     data = train_data, # Data
                     method = 'rpart', # Specify SVM model
                     trControl = fitControl) # Use cross validation
```

<br>

Check the predicted accuracy of our decision tree model by running it on resamples of our *train data*. Later we will test the accuracy of the model by running a prediction on our *test data*.

```{r}
confusionMatrix(dt_model)
```

The results here tell us that our average accuracy is 90.48% when testing our data on re samples of our training data. We can also see what was predicted correctly/incorrectly.\

<br>

Lets check the importance of each variants

```{r fig.height=2.5}
#chunk15
# Create object of importance of our variables 
dt_importance <- varImp(dt_model)

# Create plot of importance of variables
ggplot(data = dt_importance, mapping = aes(x = dt_importance[,1])) + # Data & mapping
  geom_boxplot() + # Create box plot
  labs(title = "Variable importance: Decision tree model") + # Title
  theme_light() # Theme
```

This table gives us the importance of each variable in predicting the species

Now lets plot the decision tree using `fancyRpartPlot()` from the RATTLE package. This will give us clear insight into how the model makes its predictions.

```{r}
#chunk16
fancyRpartPlot(dt_model$finalModel, # Accesses the underlying decision tree model
               sub = '') # Specifies a subtitle for the plot.
```

This decision tree tells us that:\

-   If petal length is less than 2.6 it is *setosa*
-   If petal length is in between 2.6 and 4.8 it is *virginica*
-   if petal length is in greater than 4.8 it is *versicolor*

As we can see petal length was the only variable that was needed to predict the model.\

#### Prediction

Use the created `dt_model` to run a prediction on the test data.

```{r}
#chunk17
prediction_dt <- predict(dt_model, test_data)
```

Check the proportions of the predictions which are accurate.

```{r}
#chunk18
# Generate the prediction table
confusion_matrix <- table(prediction_dt, test_data$Species) %>% # Create prediction table. 
                      prop.table() %>% # Convert table values into proportions instead of counts. 
                      round(2) # Round numbers to 2 significant values.

accuracy <- sum(diag(confusion_matrix)) / sum(confusion_matrix) # Calculate accuracy

confusion_matrix # Display the matrix

accuracy # Display the accuracy
```

As we can see, almost 98% of the species classification predicted correctly.\

<br>

## **Logistic Regression model**

<font size ="4"> **Quick facts:** </font>

-   **Uses:** Binary classification, multi-class classification (via extensions), and probability prediction.
-   **How it works:** Logistic Regression maps input features to probabilities using the sigmoid function. It predicts the likelihood of an outcome, and a threshold (commonly 0.5) is applied to make binary predictions.
-   **Pros:** (1) Easy to interpret and implement, (2) Computationally efficient for large datasets, (3) Computationally efficient for large datasets.
-   **Cons:** (1) Assumes a linear relationship between features and log-odds, (2) Sensitive to outliers, which can skew results, (3) Limited for complex, non-linear data unless extended.

<br>

### Implementation

We will create a binary classification problem by grouping the species into "setosa" and "non-setosa".

#### Create a Binary Variable

We start by creating a new column in the Iris dataset, called *BinarySpecies.* This column will label a flower as *setosa* if its species is setosa, or *non-setosa* otherwise.

```{r}
#chunk19
iris$BinarySpecies <- ifelse(iris$Species == "setosa", "setosa", "non-setosa") # Create a binary species column
```

<br>

#### Convert Binary Variable to a Factor

Logistic regression requires the target variable to be a factor (categorical data). Let’s convert *BinarySpecies* to a factor.

```{r}
#chunk20
iris$BinarySpecies <- as.factor(iris$BinarySpecies)
```

<br>

#### Add *BinarySpecies* to train_data and test_data based on their row names

As we already split the data into training data set and testing data set, so we are going to build the logistic model.

But there is an issue. We need to pass the *BinarySpecies* column to the train and test data set.

```{r}
#chunk21
train_data$BinarySpecies <- iris[row.names(train_data), "BinarySpecies"]
test_data$BinarySpecies <- iris[row.names(test_data), "BinarySpecies"]
```

<br>

#### Build a Logistic Regression Model

Now, let’s build the logistic regression model using the `glm()` function. The goal is to predict the *BinarySpecies* column using the flower’s measurements (sepal length, sepal width, petal length, and petal width).

```{r}
#chunk22
log_model <- glm(BinarySpecies ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, # Response variable and predictor variables
                 data = train_data, 
                 family = binomial) # Assumes a binary outcome
```

Here `BinarySpecies` is the response variable (dependent variable), which the outcome being predicted.  It is assumed to be a binary variable (e.g., 0 or 1) because of the `family = binomial` argument.

<br>

#### View Model Summary

To see how well the model fits the training data, we use the `summary()` function.

```{r}
summary(log_model)
```

#### Visualizing the Model's Predictions

We can plot the logistic regression curve for one of the most significant predictors to understand how it distinguishes between "setosa" and "non-setosa."

```{r}
#chunk23
ggplot(data = train_data, aes(x = Petal.Length, y = as.numeric(BinarySpecies == "setosa"), color = BinarySpecies)) + # Map Petal.Length to x-axis and binary species to y-axis, coloring by species.
  geom_point(size = 3, alpha = 0.7) + # Add scatter points with size and transparency.
  stat_smooth(method = "glm", method.args = list(family = "binomial"), color = "blue") + # Add a logistic regression curve in blue.
  labs(title = "Logistic Regression Curve for Petal Length", x = "Petal Length", y = "Probability of Being Setosa") + # Add title and axis labels.
  theme_minimal() # Apply a minimal theme to the plot.
```

Explanation:

-   Blue Curve: Represents the logistic regression model's predicted probability of being classified as "setosa" based on `Petal.Length.`

-   Points: Show actual classifications (1 for "setosa," 0 for "non-setosa").

-   Trend: A sharp increase in the probability of "setosa" classification is observed as `Petal.Length` increases, which aligns with our understanding of the data.

<br>

#### Make Predictions on the Test Data

We use the `predict()` function to generate predictions on the test dataset.

```{r}
#chunk24
log_preds <- predict(log_model, test_data, type = "response")
```

The `type = "response"` option gives probabilities (values between 0 and 1) for the predicted class.

<br>

#### Convert Probabilities to Class Labels

We classify the predictions as *setosa* if the probability is greater than 0.5, and *non-setosa* otherwise.

```{r}
#chunk25
log_class <- ifelse(log_preds > 0.5, "setosa", "non-setosa") # Threshold is set at 0.5 to classify predictions as 'setosa' or 'non-setosa'

log_class <- as.factor(log_class) # Converts the predicted labels to factors for comparison with actual labels.
```

<br>

#### Evaluate the Model

To evaluate the model, we compare the predicted labels with the actual labels in the test dataset using a confusion matrix.

```{r}
#chunk26
conf_matrix_log <- table(Predicted = log_class, Actual = test_data$BinarySpecies) # A confusion matrix is created to compare predicted and actual labels.


conf_matrix_log
```

##### Interpretation

From the table above table:

-   Predicted as "setosa" and actually "setosa" (True Positives): 30
-   Predicted as "non-setosa" and actually "non-setosa" (True Negatives): 15
-   Predicted as "set osa" but actually "non-setosa" (False Positives): 0
-   Predicted as "non-setosa" but actually "setosa" (False Negatives): 0