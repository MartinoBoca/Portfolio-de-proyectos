# Sistema de Recomendación para AdTech

## Alcance del Trabajo
Desarrollo de un sistema de recomendación de productos para publicidad digital, integrando herramientas de procesamiento de datos, almacenamiento en la nube y despliegue de servicios. El sistema genera recomendaciones personalizadas basadas en logs de interacciones de usuarios y las sirve mediante una API en tiempo real.

---

## Herramientas Utilizadas
- **Cloud Services (AWS)**:
  - **EC2**: Ejecución del pipeline de Airflow.
  - **S3**: Almacenamiento de datos crudos y resultados intermedios.
  - **RDS (PostgreSQL)**: Base de datos para recomendaciones precomputadas.
  - **ECR/App Runner**: Dockerización y despliegue de la API.
- **Orquestación**: Apache Airflow (DAGs para procesamiento diario).
- **API**: FastAPI + Uvicorn (endpoints para recomendaciones).
- **Lenguajes**: Python (scripts de Airflow, API, conexiones a AWS).
- **Otros**: Docker, Git, psycopg2, boto3.

---

## Arquitectura de la Solución
1. **Pipeline de Datos**:
   - **Airflow en EC2**: Procesa logs diarios desde S3, genera métricas (TopProducts y TopCTR) y escribe resultados en RDS.
   - **Tareas Principales**: 
     - `FiltrarDatos`: Limpieza de logs de advertisers inactivos.
     - `TopProducts`: Productos más vistos por advertiser.
     - `TopCTR`: Productos con mejor tasa de clics.
     - `DBWriting`: Escritura en PostgreSQL.

2. **API**:
   - **FastAPI en App Runner**: Endpoints para acceder a recomendaciones:
     - `/recommendations/<ADV>/<Modelo>`: Recomendaciones del día.
     - `/stats/`: Estadísticas generales.
     - `/history/<ADV>/`: Historial de 7 días.
   - **Dockerización**: Imagen basada en `python:3.10-slim-bullseye`.

3. **Almacenamiento**:
   - **S3**: Datos crudos y resultados intermedios.
   - **RDS**: Tablas `top_products` y `top_ctr`.

---

## Tareas Realizadas
- Configuración de instancia EC2 para Airflow con conexión a RDS.
- Desarrollo de DAGs para procesamiento diario con manejo de dependencias y fechas.
- Implementación de API con FastAPI y despliegue en AWS App Runner.
- Conexión segura a S3 y RDS usando `boto3` y `psycopg2`.
- Dockerización de la API y manejo de variables de entorno.

---

## Desafíos Encontrados
1. **Permisos de AWS**:
   - Bloqueo de instancia EC2 por política `AWSCompromisedKeyQuarantineV3`.
   - Restricciones en ECR para subir imágenes Docker.
2. **Configuración de Airflow**:
   - Uso de `catchup=True` y conflictos en ejecuciones paralelas.
   - Solución: Nombrado de archivos intermedios con `execution_date`.
3. **Despliegue de API**:
   - Errores en App Runner (`Failed to build your application source code`).
   - Dificultades para integrar credenciales de AWS de forma segura.

---

## Posibles Mejoras
- **Seguridad**:
  - Reemplazar credenciales hardcodeadas por variables de entorno o Secrets Manager.
  - Usar `Airflow Connections` para integrar S3 y PostgreSQL.
- **Optimización**:
  - Migrar archivos CSV a Parquet para reducir costos de almacenamiento.
- **Monitoreo**:
  - Implementar logs centralizados y alertas para el pipeline y la API.

---

## Repositorio de Código
[Código en GitHub](https://github.com/MartinoBoca/TP-Final-ML-Ops)  
Incluye branches para el DAG de Airflow y la API.

---
