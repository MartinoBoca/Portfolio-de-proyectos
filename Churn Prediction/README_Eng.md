# 📊 Customer Churn Analysis

This repository contains a detailed analysis of customer churn using statistical and machine learning models. It explores variable relationships, hypothesis testing, and predictive model comparisons.

## 📂 Contents

- **Data Exploration**: Descriptive analysis and visualization of the dataset.  
- **Hypothesis Testing**: Evaluating the impact of different variables on churn.  
- **Predictive Modeling**: Implementing regression models (MLP, Probit, and Logit) to predict churn.  
- **Model Evaluation**: Comparing accuracy and performance metrics using statistical tests and confusion matrices.  
- **Final Predictions**: Applying the best-performing model to new customers.  

## 📊 Exploratory Data Analysis  

The analysis begins with descriptive statistics, including:  
- Distribution of key variables.  
- Missing data evaluation.  
- Heatmaps to identify correlations.  

Findings suggest that `Churn` is correlated with `Num_Sites` and `Years`, indicating these factors may influence customer retention.  

## 📈 Hypothesis Testing  

Two key tests are conducted:  

1. **Proportion Difference Test**: Analyzing whether having an assigned account manager reduces churn. The null hypothesis is rejected, suggesting that account manager allocation may not be effective.  
2. **Churn Rate for Customers with Over 7 Years**: Investigating if their churn rate exceeds 30%. The null hypothesis is not rejected, indicating their churn rate is not significantly higher.  

## 🤖 Predictive Modeling  

Three models are trained to predict churn:  

- **MLP (Linear Probability Model)**: Provides interpretability but has predictive limitations.  
- **Probit and Logit Models**: More robust for binary classification.  

Models are compared using:  

- **Pseudo-R²**: To evaluate model fit.  
- **Confusion Matrices**: To analyze false positives/negatives.  
- **RMSE (Root Mean Squared Error)**: To measure prediction accuracy.  

The **Logit model** is selected as the best predictor due to its lower error and better performance.  

## 🎯 Predictions for New Customers  

The Logit model is used to predict churn for a new set of customers. Results indicate that 4 out of 6 customers analyzed have a high probability of churning.  

## 📌 Conclusions  

- Assigning account managers does not seem to reduce churn, suggesting possible inefficiencies in resource allocation.  
- Factors such as customer tenure and the number of subscribed sites significantly influence churn probability.  
- The **Logit model** is the most effective for predicting churn in this dataset.  

## ⚡ Requirements & Usage  

To reproduce the analysis, ensure you have the following R packages installed:  

```r
install.packages(c("ggplot2", "corrplot", "caret", "forecast", "stargazer"))
