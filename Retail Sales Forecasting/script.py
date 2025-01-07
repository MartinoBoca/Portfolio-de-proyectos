import pandas as pd
import numpy as np
from fastai.tabular.all import *
import functions_male_tp_def as f #v6
from functions_male_tp_def import (rmspe, #v6
                               assign_competition_distance_category,
                               process_competition_data, process_promo2_active, nan_summary,
                               try_model, get_mean,try_model_ols
                               )

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
import gc
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

##Decision tree imports
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

#=============================================================== Input & Prep

# Función que procesa los df y devuelve uno único, tomando un sample de frac
folder_path = r'C:/Users/octav/OneDrive/Escritorio/MiM + Analytics/Machine Learning 2024/'
#C:\Users\eunoblea\OneDrive - Anheuser-Busch InBev\Desktop\UTDT\5. Machine Learning\TP\\
df = f.df_import(folder_path, frac=0.3)
#glosary = pd.read_csv('glosary.csv', sep=";")

data_types = df.dtypes
descript = df.describe()

print('Import & Prep completed!')

#========================================================= Feature Engineering

#----------------------------------------------------- Date Data

# Granularizamos campo Date
df = add_datepart(df, 'Date', drop= False)

#----------------------------------------------------- Competition Data

# Aplicamos procesamiento
df = process_competition_data(df)
df = assign_competition_distance_category(df)
# Probamos un LOG
df['log_competitiondistance'] = np.log10(df.CompetitionDistance)


#----------------------------------------------------- Open Data

# Tienda abierta en feriado
df['Open_Holiday'] = df.apply(lambda row: 1 if row['Open'] == 1 and row['StateHoliday'] != 0 else 0, axis=1)
# Categórica
df['StateHoliday'] = df['StateHoliday'].map({'0': 0, 'a': 1, 'b': 2, 'c': 3, 0: 0})

#----------------------------------------------------- Promo Data

df = process_promo2_active(df)

#----------------------------------------------------- Ordinal Encoder

ordinal_encoder = OrdinalEncoder(categories=[['a', 'b', 'c', 'd']])
df['StoreType'] = ordinal_encoder.fit_transform(df[['StoreType']])

ordinal_encoder2 = OrdinalEncoder(categories=[['a', 'b', 'c']])
df['Assortment'] = ordinal_encoder2.fit_transform(df[['Assortment']])


df[df.select_dtypes(include=['bool']).columns] = df.select_dtypes(include=['bool']).astype(int)


print('Feature Engeeniring Completed!')


#================================================================== Model Prep

df = df.drop(columns=['Date', 'Elapsed', 'Id'])
# DF para el problema adicional
df_add_problem = df.copy()
# Elimino las columnas que no corresponden a cada problema
df = df.drop(columns=['Customers'])
df_add_problem = df_add_problem.drop(columns=['Sales'])

# Definición de conjuntos train, val y test.
train = df[df.train_eval == 'train'].drop(columns=['train_eval'])
test_df = df[df.train_eval == 'eval'].drop(columns=['train_eval'])
val = train[train.Year == 2015]
train = train[train.Year <= 2014]

print(f"Training Shape: {train.shape}")
print(f"Validation Shape: {val.shape}")
print(f"Test Shape: {test_df.shape}")

input_cols = [item for item in train.columns if item != 'Sales']
target_col = 'Sales'
problem2_target_col = 'Customer'

train_inputs = train[input_cols].copy()
train_targets = train[target_col].copy()

val_inputs = val[input_cols].copy()
val_targets = val[target_col].copy()

test_inputs = test_df[input_cols].copy()

#train_nans = nan_summary(train_inputs)
#test_nans = nan_summary(test_inputs)

# Escalo
scaler = MinMaxScaler().fit(train_inputs)
train_inputs= scaler.transform(train_inputs)
val_inputs = scaler.transform(val_inputs)
test_inputs = scaler.transform(test_inputs)

#================================================================ Modeling

#------------------------------------------------------------- Baseline
dum_train_preds = get_mean(train)
dum_val_preds = get_mean(val)
dum_train_eval = mean_squared_error(dum_train_preds, train_targets, squared=False)
dum_val_eval = mean_squared_error(dum_val_preds, val_targets, squared=False)
train_rmspe = rmspe(dum_train_preds, train_targets)
val_rmspe = rmspe(dum_val_preds, val_targets)
print(f"train_rmse: {dum_train_eval}")
print(f"val_rmse: {dum_val_eval}")
print()
print(f"train_rmspe: {train_rmspe}")
print(f"val_rmspe: {val_rmspe}")

#------------------------------------------------------------- Random Forest
gc.collect()
random_forest_model = RandomForestRegressor(random_state=42, 
                                            n_jobs=-1)
try_model(random_forest_model, train_inputs, train_targets, val_inputs, val_targets)
test_preds = random_forest_model.predict(test_inputs)

print('Random Forest run completed!')


print("Hiperparámetros del Random Forest antes de entrenar:")
print(random_forest_model.get_params())

# Guardar la predicción inicial del Random Forest en un archivo
submission_df = pd.read_csv('sample_submission.csv')
submission_df['Sales'] = test_preds
submission_df.to_csv('submission_starter_rf.csv', index=False)

print('RF before opt - Completed!')

#========================================================= Optimización de hiperparámetros

# Importamos RandomizedSearchCV para hacer la búsqueda de los mejores hiperparámetros
from sklearn.model_selection import RandomizedSearchCV

# Definimos el grid de hiperparámetros
hyperparameter_grid = {
    'n_estimators': np.arange(100, 1100, 100),  # Vamos a probar entre 100 y 1000 árboles
    'max_depth': list(range(2, 21)) + [None],  # Profundidad entre 2 y 20 niveles, además de sin límite (None)
    'max_features': range(2,train_inputs.shape[1]),
    'min_samples_split': np.linspace(0.0001, 0.01, 10)  # Probamos con splits mínimos pequeños
}


# Creamos el modelo Random Forest con OOB scoring habilitado
rf_model = random_forest_model

# Realizamos una búsqueda aleatoria para optimizar los hiperparámetros
random_search = RandomizedSearchCV(
    estimator=rf_model,
    param_distributions=hyperparameter_grid,
    scoring=lambda estimator, X, y: -rmspe(y, estimator.predict(X)),  # Usamos RMSPE como métrica a minimizar
    n_iter=20,  # Número de combinaciones de hiperparámetros a probar
    cv=3,  # Usamos validación cruzada de 3 pliegues
    random_state=42,
    verbose=3
)

# Ajustamos el modelo con los datos de entrenamiento
random_search.fit(train_inputs, train_targets)

# Obtenemos los mejores hiperparámetros seleccionados por la búsqueda aleatoria
print(f"Mejores parámetros encontrados: {random_search.best_params_}")

# Imprimimos el mejor score OOB obtenido
print(f"Puntaje OOB (out-of-bag) estimado: {random_search.best_score_:.3f}")

# Entrenamos un nuevo RandomForest con los mejores hiperparámetros
optimized_rf = RandomForestRegressor(
    n_estimators=random_search.best_params_['n_estimators'],
    max_depth=random_search.best_params_['max_depth'],
    min_samples_split=random_search.best_params_['min_samples_split'],
    max_features=random_search.best_params_['max_features'],
    random_state=42,
    n_jobs=-1,
    oob_score=True
)

optimized_rf.fit(train_inputs, train_targets)

# Realizamos predicciones sobre los datos de entrenamiento
train_preds = optimized_rf.predict(train_inputs)
train_rmspe = rmspe(train_targets, train_preds)

# Evaluamos el rendimiento del modelo sobre el conjunto de validación
val_preds = optimized_rf.predict(val_inputs)
val_rmspe = rmspe(val_targets, val_preds)

# Mostramos los resultados de RMSPE
print(f'RMSPE del conjunto de entrenamiento: {train_rmspe:.3f}')
print(f'RMSPE del conjunto de validación: {val_rmspe:.3f}')

# Calculamos e imprimimos la importancia de los atributos
importances = pd.DataFrame({
    'feature': input_cols,
    'importance': optimized_rf.feature_importances_
}).sort_values(by='importance', ascending=True)

plt.barh(importances['feature'], importances['importance'])
plt.xlabel('Importancia')
plt.ylabel('Atributos')
plt.title('Importancia de los atributos en Random Forest')
plt.show()

print("\nCaracterísticas más importantes:")
print(importances)

## Feature importances del modelo pre-optimización
importances_original = pd.DataFrame({
    'feature': input_cols,
    'importance': random_forest_model.feature_importances_
}).sort_values(by='importance', ascending=True)

plt.barh(importances_original['feature'], importances_original['importance'])
plt.xlabel('Importancia')
plt.ylabel('Atributos')
plt.title('Importancia de los atributos en Random Forest')
plt.show()

print("\nCaracterísticas más importantes:")
print(importances_original)

# Hacer las predicciones finales en el conjunto de prueba con el modelo optimizado
test_preds_opt = optimized_rf.predict(test_inputs)
submission_df['Sales'] = test_preds_opt
submission_df.to_csv('submission_starter_rf_opt.csv', index=False)

print("Optimización completada y archivo de predicción generado.")


#================================================================== Output RF
submission_df = pd.read_csv('sample_submission.csv')
submission_df['Sales'] = test_preds
submission_df.to_csv('submission_starter_rf.csv', index=False)

#================================================================== Decision Trees

#Modelo Árbol de decisión - OutOfTheBox-----------------------------------------

# Crear el modelo de Árbol de Decisión
decision_tree_model = DecisionTreeRegressor(random_state=42)

# Probar el modelo usando una función personalizada (try_model(model, train_inputs, train_targets, val_inputs, val_targets))
try_model(decision_tree_model,train_inputs, train_targets, val_inputs, val_targets)

# Realizar predicciones con el conjunto de test
test_preds = decision_tree_model.predict(test_inputs)

print(f"train_rmspe: {train_rmspe}")
print(f"val_rmspe: {val_rmspe}")

# Guardar las predicciones en el archivo de salida (CSV)
submission_df = pd.read_csv('sample_submission.csv')
submission_df['Sales'] = test_preds
submission_df.to_csv('submission_starter_treev4.csv', index=False)

#------------------------------------------------------------------------
#Modelo árbol de decisión + Optimización de hiperparámetros---------------------------------------------------

gc.collect()

# Definir el modelo de Árbol de Decisión
decision_tree_model = DecisionTreeRegressor(random_state=42)

# Random Search - Definir los rangos de hiperparámetros a probar
param_distributions = {
    'max_depth': [10, 20, 30, 40, None],
    'min_samples_split': [2, 10, 20],
    'min_samples_leaf': [1, 5, 10],
    'max_features': [None, 'sqrt', 'log2'],
}

# Realizar la búsqueda aleatoria de hiperparámetros
random_search = RandomizedSearchCV(estimator=decision_tree_model,
                                   param_distributions=param_distributions,
                                   n_iter=50,
                                   cv=5,
                                   scoring='neg_mean_squared_error',
                                   random_state=42,
                                   n_jobs=-1)

# Ajustar el modelo a los datos
random_search.fit(train_inputs, train_targets)

# Obtener el mejor modelo
best_model = random_search.best_estimator_

print("Mejores hiperparámetros encontrados:", random_search.best_params_)

# Evaluar el mejor modelo encontrado por Random Search
try_model(best_model, train_inputs, train_targets, val_inputs, val_targets)

""" Mejores hiperparámetros luego de hacer RandomSearch:
best_params_ = {
    'min_samples_split': 20, 
    'min_samples_leaf': 5, 
    'max_features': None, 
    'max_depth': None
}
"""

feature_importances = pd.DataFrame(best_model.feature_importances_,
                                   index=input_cols,
                                   columns=['importance']).sort_values('importance', ascending=True)

plt.barh(feature_importances.index, feature_importances['importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature importance')
plt.show()

print(f"train_rmspe: {train_rmspe}")
print(f"val_rmspe: {val_rmspe}")

# Visualizar el árbol de decisión con max_depth = 3----------------------------------------------------
#plt.figure(figsize=(16,10))
##tree.plot_tree(decision_tree_model, filled=True, feature_names=input_cols, rounded=True)
#plt.show()
#---------------------------------------------------------------------------------------------------------

#================================================================== Output Decision trees
test_preds = best_model.predict(test_inputs)
# Guardar las predicciones en el archivo de salida (CSV)
submission_df = pd.read_csv('sample_submission.csv')
submission_df['Sales'] = test_preds
submission_df.to_csv('submission_starter_tree.csv', index=False)


#========================================================== Problema Adicional

# Lo uso para modelar OLS
feature_importances = ['Open', 'Store', 'Promo', 'CompetitionDistance', 'log_competitiondistance',
                       'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Dayofyear', 'Dayofweek',
                       'StoreType', 'Assortment', 'DayOfWeek', 'Day', 'cat_CompetitionDistance', 'Promo2']

# Solamente tengo Train
train = df_add_problem[df_add_problem.train_eval == 'train'].drop(columns=['train_eval'])
# Train y test
val = train[train.Year == 2015]
train = train[train.Year <= 2014]

print(f"Training Shape: {train.shape}")
print(f"Validation Shape: {val.shape}")
print(f"Test Shape: {test_df.shape}")

input_cols = feature_importances
target_col = 'Customers'

train_inputs = train[input_cols].copy()
train_targets = train[target_col].copy()
val_inputs = val[input_cols].copy()
val_targets = val[target_col].copy()

# Escalo
scaler = MinMaxScaler().fit(train_inputs)
train_inputs = scaler.transform(train_inputs)
val_inputs = scaler.transform(val_inputs)

# Fiteo
linear_model = LinearRegression()
try_model_ols(linear_model, train_inputs, train_targets, val_inputs, val_targets, input_cols)
