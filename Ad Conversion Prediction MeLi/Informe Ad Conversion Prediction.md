# Informe de trabajo: Ad conversion prediction Mercado Libre

---

## Introducción
El trabajo analiza un dataset con 36,152 observaciones correspondientes a impresiones en anuncios de Mercado Libre y 58 variables. Se busca optimizar la predicción de conversiones a partir de un modelo de aprendizaje automático, priorizando la transformación de datos mediante técnicas de ingeniería de atributos y un sistema de validación robusto.

---

## Análisis Exploratorio de Datos (AED)

- **Características destacadas**:
  - `available_quantity`: Rango amplio (0-99,999), desviación estándar alta (11,251).
  - `original_price` y `price`: Alta variabilidad, posible indicador de descuentos.
  - `sold_quantity`: Media de 79.92, rango de 0 a 32,369, relevante para predecir conversiones.
  - `total_visits_domain` y `total_visits_item`: Importantes para medir tráfico y popularidad.

- **Insights**:
  - **Logística vs Conversión**: Servicios personalizados ("custom") tienen la conversión más alta (15.16%) pese a precios elevados (~ARS 12,500).  
  - **Imágenes principales**: Productos con imágenes tienen precios más altos pero conversiones ligeramente menores.

---

## Ingeniería de Atributos

### Procedimientos destacados:
1. **Variables descartadas**: Eliminadas `benefit`, `etl_version`, `accepts_mercadopago` y `site_id` por baja relevancia.
2. **Transformaciones**:
   - `product_id` y `user_id`: Convertidas a categóricas (`object`).
   - Fechas: Extraídas características como día, hora y día de la semana.
   - `NANs`: Transformados a `-1` en variables clave (`is_pdp`, `user_id`).
3. **Creación de ratios**:
   - Conversión por ítem y dominio.
   - Descuento (`price/original_price`).
   - Ratio de ventas sobre stock disponible.
4. **Interacciones**: Nuevas variables basadas en combinaciones relevantes según F-score.
5. **One-Hot Encoding**:
   - Variables categóricas como `tags`, `platform`, `fulfillment`, `logistic_type`.
6. **Procesamiento de texto**: Keywords como "nuevo", "oficial", "envío" extraídas de `title`.

---

## Sistemas de Validación

- **División de datos**:
  - Conjuntos: Entrenamiento, validación y evaluación.
  - Estratificación: Basada en la variable objetivo para evitar data leakage.
- **Estrategia**:
  - Uso de objetos `DMatrix` para XGBoost.
  - Monitorización de rendimiento en entrenamiento y validación mediante `watchlist`.

---

## Resultados de Validación

- **AUC alcanzado**: 0.889 en validación, con ligera variación en Kaggle.
- **Consistencia**: Resultados iniciales alineados con Kaggle, aunque ajustes adicionales no siempre mejoraron el rendimiento.

---

## Selección del Modelo

### Modelos evaluados:
1. **KNN**: Alta sensibilidad al número de variables, bajo rendimiento.
2. **Decision Trees**: Alta varianza y sobreajuste.
3. **XGBoost**: Mejor rendimiento, eficiente con datos desequilibrados y relaciones no lineales.

### Optimización de Hiperparámetros:
- **Técnica**: Búsqueda aleatoria (`random_search`).
- **Parámetros seleccionados**:
  - `max_depth`: 4
  - `eta`: 0.1
  - `lambda`, `alpha`: 1
  - `subsample`, `colsample_bytree`: 0.7
  - `min_child_weight`: 5
  - `gamma`: 1
  - `num_boost_round`: 100

---

## Distribución de Tiempos
- **AED**: 15%-20% del tiempo total.
- **Ingeniería de Atributos**: 50%-60%.
- **Validación e Hiperparámetros**: 25%-30%.

---

## Conclusión
El modelo XGBoost mostró ser efectivo para predecir conversiones, destacándose la importancia de una robusta ingeniería de atributos. La estrategia de validación aseguró un buen rendimiento generalizable, aunque ajustes adicionales deben equilibrar la mejora en validación y el rendimiento en Kaggle.

---
