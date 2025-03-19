# 📊 Análisis de Customer Churn

Este repositorio contiene un análisis detallado sobre la tasa de abandono (customer churn) utilizando modelos estadísticos y de machine learning. Se exploran relaciones entre variables, se realizan pruebas de hipótesis y se comparan modelos de predicción.

## 📂 Contenido

- **Exploración de datos**: Análisis descriptivo y visualización de la base de datos.
- **Pruebas de hipótesis**: Evaluación del impacto de distintas variables en el churn.
- **Modelos predictivos**: Implementación de modelos de regresión (MLP, Probit y Logit) para predecir el churn.
- **Evaluación de modelos**: Comparación de precisión y métricas mediante pruebas estadísticas y matrices de confusión.
- **Predicciones finales**: Aplicación del modelo más preciso a nuevos clientes.

## 📊 Análisis Exploratorio

Se comienza con un análisis descriptivo de los datos, incluyendo:
- Distribución de variables clave.
- Evaluación de datos faltantes.
- Mapas de calor para identificar correlaciones.

Se observa que la variable `Churn` está correlacionada con `Num_Sites` y `Years`, indicando que estos factores pueden influir en la probabilidad de abandono.

## 📈 Pruebas de Hipótesis

Se realizan dos pruebas clave:
1. **Diferencia de proporciones:** Se analiza si tener un gestor asignado reduce el churn. Se rechaza la hipótesis nula, lo que sugiere que la asignación de gestores podría no estar optimizada.
2. **Clientes con más de 7 años de antigüedad:** Se investiga si su tasa de churn supera el 30%. No se rechaza la hipótesis nula, indicando que su tasa de abandono no es significativamente mayor.

## 🤖 Modelado Predictivo

Se entrenan tres modelos para predecir el churn:
- **MLP (Modelo Lineal de Probabilidad)**: Proporciona interpretabilidad pero presenta limitaciones en la predicción.
- **Probit y Logit**: Modelos más robustos para clasificación binaria.

Se comparan los modelos con métricas como:
- **Pseudo-R²**: Para evaluar el ajuste de los modelos.
- **Matriz de confusión**: Para analizar falsos positivos/negativos.
- **RMSE (Error Cuadrático Medio)**: Para medir la precisión.

El modelo Logit es seleccionado como el mejor predictor debido a su menor error y mejor ajuste.

## 🎯 Predicción para Nuevos Clientes

Se utiliza el modelo Logit para predecir la tasa de abandono de un nuevo conjunto de clientes. Los resultados indican que 4 de los 6 clientes analizados tienen alta probabilidad de churn.

## 📌 Conclusiones

- La asignación de gestores no parece reducir el churn, lo que sugiere una posible mala distribución de recursos.
- Factores como la antigüedad del cliente y la cantidad de sitios contratados influyen en la probabilidad de abandono.
- El modelo Logit es el más efectivo para predecir el churn en esta muestra.

## ⚡ Requisitos y Uso

Para reproducir el análisis, asegúrate de tener instalados los siguientes paquetes en R:

```r
install.packages(c("ggplot2", "corrplot", "caret", "forecast", "stargazer"))
