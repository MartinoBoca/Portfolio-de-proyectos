

## Introducción

El objetivo del proyecto fue desarrollar un modelo de **forecasting de demanda** para una cadena de retail en Europa.  
Se utilizó un dataset histórico de ventas (2013-2015) proporcionado en una competencia de Kaggle para predecir las ventas de las próximas seis semanas. Esto optimiza la gestión de recursos y facilita la toma de decisiones estratégicas.

- **Dataset**: Incluye más de 1 millón de observaciones y archivos adicionales con características de las tiendas.
- **Métrica de evaluación**: RMSPE (Root Mean Square Percentage Error).

---

## Exploratory Data Analysis (EDA) & Feature Engineering

### Variables Analizadas
- **Nulos**: Imputados o tratados según cada caso.
- **Variables Competition**: 
  - Generación de `CompetitionOpen` y categorías para `CompetitionDistance`.
- **Variables Promo**: Creación de `Promo2Active` para indicar promociones activas.
- **Variables Date**: Descomposición en granularidades como año, mes, día, etc.
- **Otras Variables**: Creación de `Open_Holiday` y transformación de variables categóricas como `StoreType` y `Assortment`.

---

## Técnica de Validación

Se utilizó un enfoque **Hold-out set**, dividiendo el dataset en:
- **Entrenamiento**: Datos hasta 2014.
- **Validación**: Datos de 2015.  

Esto evita **data leakage** y simula un escenario real para problemas de series temporales.

---

## Modelos Implementados

### Modelo 1: Random Forest
- **Descripción**: Modelo de ensamble que combina múltiples árboles de decisión.
- **Resultados** (modelo original):  
  - Train RMSPE: 0.09216  
  - Val RMSPE: 0.18758  
  - Kaggle RMSPE (public): 0.14323  

- **Optimización de Hiperparámetros**:  
  - RandomSearch mejoró la robustez, pero el modelo original tuvo mejor desempeño.  

- **Importancia de Features** (Top 5):  
  1. Open  
  2. Store  
  3. Promo  
  4. CompetitionDistance  
  5. CompetitionOpenSinceYear  

---

### Modelo 2: Decision Trees
- **Descripción**: Modelo simple implementado para comparación con Random Forest.
- **Optimización**:
  - Hiperparámetros ajustados con RandomSearch (`min_samples_split`, `max_depth`, etc.).
- **Resultados**:
  - Peor rendimiento que Random Forest, pero mejoras significativas frente al modelo básico.
- **Ventaja**: Interpretabilidad clara, con la variable `Open` como criterio principal.

---

## Problema Adicional: Predicción de Clientes

### Definición
Predicción de la variable `Customer` como herramienta para:
- Optimizar decisiones de layout y stock.
- Gestionar campañas publicitarias.

### Modelo Implementado: Regresión Lineal
- Baseline con variables seleccionadas del feature engineering previo.
- **Resultados**: El modelo explicó solo el 48% de la variabilidad en `Customer`.

---

## Conclusión

Este proyecto destacó la importancia de una sólida ingeniería de atributos y validación adecuada en problemas de forecasting de series temporales.  
El modelo **Random Forest** demostró ser el más robusto, mientras que los árboles de decisión ofrecieron mayor interpretabilidad.  
Finalmente, el problema adicional permitió explorar nuevas aplicaciones de los datos para decisiones comerciales.

