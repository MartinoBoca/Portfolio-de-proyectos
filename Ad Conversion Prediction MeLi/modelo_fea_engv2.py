import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import randint, uniform
from scipy.stats._distn_infrastructure import rv_frozen
from sklearn.model_selection import train_test_split
import gzip
import os
import unidecode

from tqdm import tqdm
#Load data
def load_comp_data(path_to_data, sample_frac=1.0):
    """
    Carga y preprocesa los datos de competencia de los archivos de entrenamiento y prueba.
    
    Args:
        path_to_data (str): Ruta al directorio que contiene los archivos de datos.
        sample_frac (float, optional): Fracción de datos de entrenamiento a muestrear. Por defecto es 1.0.
        
    Returns:
        pd.DataFrame: Datos de competencia preprocesados con filas de entrenamiento y evaluación.
    """

    # Construir rutas de archivos utilizando os.path.join()
    train_file = os.path.join(path_to_data, "train.csv.gz")
    eval_file = os.path.join(path_to_data, "test.csv")
    
    # Cargar datos de entrenamiento desde el archivo CSV comprimido con gzip
    with gzip.open(train_file, "rt", encoding="utf-8") as f:
        train_data = pd.read_csv(f)
    
    # Cargar datos de evaluación desde el archivo CSV
    eval_data = pd.read_csv(eval_file)
    
    # Realizar muestreo estratificado si sample_frac es menor que 1.0
    if sample_frac < 1.0:
        train_data, _ = train_test_split(
            train_data,
            train_size=sample_frac,
            stratify=train_data["conversion"],
            random_state = 42        )
    
    # Agregar columna "train_eval" para indicar filas de entrenamiento y evaluación
    train_data["train_eval"] = "train"
    eval_data["train_eval"] = "eval"
    
    # Concatenar verticalmente los datos de entrenamiento y evaluación
    df = pd.concat([train_data, eval_data], axis=0, ignore_index=True)
    
    return df

def random_search(param_dist, dtrain, watchlist, n_iter=50):
    exp_results = []
    best_score = -np.inf
    best_params = None

    for i in range(n_iter):
        params = {}
        for k, v in param_dist.items():
            if isinstance(v, rv_frozen):
                params[k] = v.rvs()
            else:
                params[k] = np.random.choice(v)
        num_boost_round = params.pop("num_boost_round")
        
        evals_result = {}
        model = xgb.train(params, dtrain, num_boost_round=num_boost_round, evals=watchlist, evals_result=evals_result, verbose_eval=False)
        train_auc = evals_result['train']["auc"][-1]
        val_auc = evals_result['validation']["auc"][-1]
        
        if val_auc > best_score:
            best_score = val_auc
            best_params = params
            best_params["num_boost_round"] = num_boost_round
            best_model = model
        
        params.update({"train_auc": train_auc, "val_auc": val_auc, "num_boost_round": num_boost_round})
        exp_results.append(params)
        print(f"Iteration {i+1}/{n_iter} - AUC: {val_auc:.4f} - Params: {params}")
    
    exp_results = pd.DataFrame(exp_results)
    exp_results = exp_results.sort_values(by="val_auc", ascending=False)
    return best_params, best_score, best_model, exp_results


def to_ralas(df):
    # Convertir los conjuntos de datos a matrices ralas en formato CSR
    df = df.astype(pd.SparseDtype(float, fill_value=0))
    df_names = df.columns
    df = df.sparse.to_coo().tocsr()
    return df, df_names


def process_text(text, rm_s = True):
    # Convertir a minúsculas, eliminar tildes y remover 's' al final
    text = text.lower()  # Convertir a minúsculas
    text = unidecode.unidecode(text)  # Eliminar tildes
    if rm_s:
        if text.endswith('s'):
            text = text[:-1]  # Remover 's' al final
    return text

## Cargar los datos de competencia
df = load_comp_data(r"C:\Users\Usuario\Documents\Martino\AAA MiM + Analytics\Modulo 2\Data Mining\datos TP", sample_frac = 0.2)


## Realizar ingeniería de atributos

#Cambar product_id y user_id de float a object
df['product_id'] = df['product_id'].astype('object')
df['user_id'] = df['user_id'].astype('object')


#Sacar variables sin variabilidad
df["accepts_mercadopago"].value_counts()
cols_to_delete = ["accepts_mercadopago", "site_id", "benefit", "etl_version"]
df = df.drop(columns=cols_to_delete)


#Transformar la fecha a timestamp
df['print_server_timestamp'] = pd.to_datetime(df['print_server_timestamp'])
#Crear variables a partir de la fecha
df['print_day'] = df['print_server_timestamp'].dt.day
df['print_month'] = df['print_server_timestamp'].dt.month
df['print_day_month'] = df['print_day'].astype(str) + '-' + df['print_month'].astype(str) # no se usa para OHE, seria inef 60 columnas (una por dia)
df["print_week"] = df["print_server_timestamp"].dt.isocalendar().week
df["print_hour"] = df["print_server_timestamp"].dt.hour
df["print_weekday"] = df['print_server_timestamp'].dt.weekday < 5 #0 para el lunes. 6 para el domingo
df['print_day_of_week'] = df['print_server_timestamp'].dt.day_name()
df['print_server_numeric'] =  df['print_server_timestamp'].values.astype("float64")


#Transformar los missings NO aleatorios a -1  
df["is_pdp"]  =  df["is_pdp"].astype('float').fillna(-1).astype('int') #agregamos is_pdp aca xque al haber cambiado los Nans a -1, xGboost hace mejores cortes
df['user_id'] = np.where(df['user_id'].isna(), "-1", df['user_id'])


#Crear algunos ratios
df["conversion_item_30d"] = df["total_orders_item_30days"] / df["total_visits_item"]
df['conversion_domain_30d'] = df['total_orders_domain_30days'] / df['total_visits_domain']
df["discount_applied"] = df["price"] / df["original_price"]


df['sales_rate'] = df['sold_quantity'] / df['available_quantity'] #qué proporcion del stock disponible s eha vendido

# Reemplazo divisiones por cero (inf) con -1, para no incurrir en indeterminaciones
df['sales_rate'] = np.where(np.isinf(df['sales_rate']), -1, df['sales_rate'])


df['total_visits_domain_avg'] = df["total_visits_domain"].mean()
 

#Unir dos variables relevantes
df["offset_print_potition"] = df["offset"] * df["print_position"]
df["price_orders_interaction"] = df["price"] * df["total_orders_item_30days"]


#Estandarizar la garantía
pattern= r'(?:\w+\s+)?(\d+(?:\.\d+)?)\s+(\w+)'
df[["warranty_qty", "warranty_time_type"]] = df['warranty'].str.extract(pattern)
df["warranty_time_type"].value_counts() #Tenemos problemas de formato
df['warranty_time_type'] = np.where(df['warranty_time_type'].isna(), "No", df['warranty_time_type']) #Primero transformar los missings
df['warranty_time_type'] = df['warranty_time_type'].apply(process_text)
df["warranty_time_type"].value_counts()

df["warranty_qty"] = df["warranty_qty"].astype(np.float64)
df["warranty_qty"] = np.where(df["warranty_qty"].isna(), -1, df["warranty_qty"]) # Transformar los missings


#Arpvechar el texto
df["title"] = df["title"].apply(lambda x: process_text(x, rm_s = False)) #Limpiar el texto

df['title_oficial'] = df['title'].str.contains("oficial")*1 #Buscar si la palabra "oficial" esta dentro del titulo
df['title_liquidacion'] = df['title'].str.contains("liquidacion")*1
df['title_envio'] = df['title'].str.contains("envio")*1
df['title_nuevo'] = df['title'].str.contains("nuevo")*1
df['title_nueva'] = df['title'].str.contains("nueva")*1

df['title_oficial'].value_counts(normalize=True)
df['title_liquidacion'].value_counts(normalize=True)
df['title_envio'].value_counts(normalize=True)
df['title_nuevo'].value_counts(normalize=True)
df['title_nueva'].value_counts(normalize=True)

#Otra forma de aprovechar el texto
df["title_len"] = df["title"].str.len()


#Transformar booleanos en int
df["free_shipping"] = np.where(df["free_shipping"], 1, 0)
df["print_weekday"] = np.where(df["print_weekday"], 1, 0)


#Hacer OHE de la columna tags
# Obtener todos los valores únicos de la columna tags, compuestaa por strings entre [].
unique_values = set()
for row in df['tags']:
    unique_values.update(row[1:-1].split(",")) #Con [1:-1] sacamos los corchetes del string del principio y final
# Crear columnas dummy para cada valor único !
for value in unique_values:
    df[value] = df['tags'].apply(lambda x: 1 if value in x else 0)


## Seleccionar las columnas relevantes
to_keep_numeric = df.select_dtypes(include="number").columns.tolist()
to_do_ohe = ["platform", "fulfillment", "logistic_type", "listing_type_id", "category_id","domain_id", 
             "product_id", "user_id","warranty_time_type", "print_day_of_week"] 
to_keep_boolean = ["conversion"]

# Realizar One-Hot Encoding (OHE) en las columnas categóricas
df_categorical = pd.get_dummies(df[to_do_ohe], sparse=True, dummy_na=True)

#Columnas a utilizar para el modelo. Permitanme incluir domain_id y print_day_month.
df = pd.concat([df[["train_eval", "domain_id","print_day_month"] + to_keep_numeric + to_keep_boolean], df_categorical], axis=1)


# Convertir las columnas booleanas a 0 y 1, manteniendo los valores NaN
for col in to_keep_boolean:
    df[col] = np.where(df[col].isna(), np.nan, df[col].astype(float))
    to_keep_numeric.append(col)


# Separar el conjunto de entrenamiento y evaluación
df_train = df.loc[df["train_eval"] == "train"]
df_train = df_train.drop(columns=["ROW_ID", "train_eval"])

df_eval = df.loc[df["train_eval"] == "eval"]
df_eval = df_eval.drop(columns=["conversion", "train_eval"])


# Separar un conjunto de validación del conjunto de entrenamiento

df_train, df_valid = train_test_split(df_train, test_size = 0.2, stratify = df_train["conversion"])

#Eliminar domain_id y print_day_month para el modelo
df_train = df_train.drop(columns = ["domain_id","print_day_month"])
df_valid = df_valid.drop(columns = ["domain_id","print_day_month"])
df_eval = df_eval.drop(columns = ["domain_id","print_day_month"])

#%% Analisis exploratorio graficos: quitar comillas para su ejecución
'''
#Grafico 1: Relacion del tipo de logistica, con el prcio y la conversion
conversion_rate_logistic_type = df_train.groupby('logistic_type').agg({'price': 'mean', 'conversion': 'mean'}).reset_index()

conversion_rate_logistic_type = conversion_rate_logistic_type.sort_values(by='price', ascending=True)

sns.set(style="whitegrid", rc={"axes.grid": False})

fig, ax1 = plt.subplots(figsize=(12, 6))

color_palette = sns.color_palette("Blues", n_colors=2)
sns.barplot(data=conversion_rate_logistic_type, x='logistic_type', y='price', ax=ax1, palette=color_palette)

ax1.set_title('Relación entre el tipo de Logística, el Precio del Artículo y la Conversión', fontsize=14)
ax1.set_xlabel('Tipo de logística', fontsize=12)
ax1.set_ylabel('Precio Promedio (AR$)', fontsize=12)

ax2 = ax1.twinx()
sns.lineplot(data=conversion_rate_logistic_type, x='logistic_type', y='conversion', ax=ax2, color='red', marker='o', linestyle='--')

for i, percentage in enumerate(conversion_rate_logistic_type['conversion'] * 100):
    ax2.text(i, conversion_rate_logistic_type['conversion'][i], f'{percentage:.2f}%', color='red', ha='center', va='bottom', fontsize=10)

ax2.set_ylabel('Tasa de Conversión (%)', fontsize=12)
ax2.set_ylim(0, max(conversion_rate_logistic_type['conversion']) * 1.2)

plt.tight_layout()

plt.show()

#Grafico 2: Relación entre la Presencia de una Imagen Principal y el Precio del Artículo con la Conversión

df_train['main_picture'] = df_train['main_picture'].notna()

grouped_data = df_train.groupby('main_picture').agg({
    'price': 'mean',
    'conversion': 'mean',
    'item_id': 'count'
}).reset_index()

grouped_data.columns = ['Main Picture', 'Average Price', 'Conversion Rate', 'Count']

fig, ax1 = plt.subplots(figsize=(12, 6))

sns.barplot(data=grouped_data, x='Main Picture', y='Average Price', ax=ax1, palette='Blues')

ax1.set_title('Relación entre la Presencia de una Imagen Principal y el Precio del Artículo con la Conversión')
ax1.set_xlabel('Presencia de Imagen Principal')
ax1.set_ylabel('Precio Promedio (AR$)')

ax2 = ax1.twinx()
ax2.plot(grouped_data['Main Picture'], grouped_data['Conversion Rate'], color='red', marker='o', linestyle='--', linewidth=2, markersize=6)
ax2.set_ylabel('Tasa de Conversión')

for i in range(len(grouped_data)):
    ax2.text(i, grouped_data['Conversion Rate'][i] + 0.002, f'{grouped_data["Conversion Rate"][i]*100:.2f}%', color='red', ha='center')

plt.show()
'''
#%%

dtrain_rala, df_train_names = to_ralas(df_train)
dvalid_rala, df_valid_names = to_ralas(df_valid)
deval_rala, df_eval_names = to_ralas(df_eval)


# Crear objetos DMatrix para XGBoost
dtrain = xgb.DMatrix(dtrain_rala[:,df_train_names != "conversion"],
                     label=dtrain_rala[:,df_train_names == "conversion"].todense().squeeze(),
                     feature_names=df_train_names[df_train_names != "conversion"].tolist())

dvalid = xgb.DMatrix(dvalid_rala[:,df_valid_names != "conversion"],
                     label=dvalid_rala[:,df_valid_names == "conversion"].todense().squeeze(),
                     feature_names=df_valid_names[df_valid_names != "conversion"].tolist())

deval = xgb.DMatrix(deval_rala[:,df_eval_names != "ROW_ID"],
                    feature_names=df_eval_names[df_eval_names != "ROW_ID"].tolist())


# Definir los parámetros del modelo XGBoost
watchlist = [(dtrain, "train"), (dvalid, "validation")]


# Definir el espacio de hiperparámetros para la búsqueda aleatoria. En nuestro informe se explica el porqué de estos valores.

param_dist = {
    "objective": ["binary:logistic"],
    "eval_metric": ["auc"],
    "max_depth": [3, 4, 5, 6],  # Reducir max_depth
    "eta": [0.1, 0.05, 0.01],  # Diferentes tasas de aprendizaje
    "lambda": [0.1, 1, 10],  # Regularización L2
    "alpha": [0.1, 1, 10],  # Regularización L1
    "subsample": [0.5, 0.7, 0.9],  # Reducir muestra por árbol
    "colsample_bytree": [0.5, 0.7, 0.9],  # Reducir muestra de características
    "min_child_weight": [1, 5, 10],  # Ajustar min_child_weight
    "gamma": [0, 1, 5],  # Ajustar gamma
    "num_boost_round": [100, 200]  # Ajustar número de rondas
}


# Probar solo una combinacion
best_params, best_score, best_model, exp_results = random_search(param_dist, dtrain, watchlist, n_iter=20)

# Calcular la importancia de las características
importance = best_model.get_score(importance_type='gain')


# Graficamos la importancia de las características en base a su F-score
plt.figure(figsize=(10, 6))
xgb.plot_importance(best_model, importance_type='gain', max_num_features=20)
plt.title('Feature Importance')
plt.show()

y_preds_eval = best_model.predict(deval)

# Crear el archivo de envío para Kaggle
submission_df = pd.DataFrame({"ROW_ID": deval_rala[:,df_eval_names == "ROW_ID"].toarray().squeeze(),
                              "conversion": y_preds_eval})
submission_df["ROW_ID"] = submission_df["ROW_ID"].astype(int)
submission_df.to_csv("final_model_xGboost.csv", sep=",", index=False)

