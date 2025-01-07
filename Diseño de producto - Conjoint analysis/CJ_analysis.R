#Conjoint Analysis
install.packages("readxl")
library(readxl)
install.packages("dplyr")
library(dplyr)
install.packages("ggplot2")
install.packages("tidyr")
library(tidyr)
library("ggplot2")

install.packages("fastDummies")
library(fastDummies)

df_prod = read.csv("C:\\Users\\Usuario\\Documents\\df_cjb.csv") 


# Ver las columnas actuales del dataframe para referencia
colnames(df_prod)

# Drop la primera columna y columnas desde "Tamaño pulgadas" en adelante
df_prod <- df_prod %>% select(-1, -(which(colnames(df_prod) == "Tamaño..pulgadas."):ncol(df_prod)))

# Convertir las columnas numéricas relevantes a factores
df_prod$`Tamaño..pulgadas..1` <- as.factor(df_prod$Tamaño)
df_prod$`Precio..ARS..1` <- as.factor(df_prod$Precio)

# Verificar las columnas actuales en df_prod
print(colnames(df_prod))

# Generar las variables dummy para todas las columnas categóricas (incluyendo las numéricas convertidas)
dummies_df <- dummy_cols(df_prod, remove_first_dummy = TRUE, remove_selected_columns = TRUE)

# Verificar los nombres de las columnas generadas para asegurarse de que las dummies se crearon correctamente
print(colnames(dummies_df))

# Ver el dataframe con las variables dummy
dummies_df


# Eliminar la primera columna y las columnas desde "Tamaño pulgadas" en adelante
#df_prod <- df_prod %>% select(-1, -(which(colnames(df_prod) == "Tamaño..pulgadas."):ncol(df_prod)))

# Verificar las columnas actuales en df_prod
print(colnames(df_prod))
df_prod
####
# Identificar las columnas categóricas en df_prod

# Generar las variables dummy para todas las columnas categóricas
dummies_df <- dummy_cols(df_prod, remove_first_dummy = TRUE, remove_selected_columns = TRUE)

# Verificar los nombres de las columnas generadas
print(colnames(dummies_df))

# Identificar las columnas categóricas y sus niveles únicos
unique_levels <- lapply(df_prod, unique)

# Crear un dataframe vacío con las columnas dummy necesarias
required_columns <- c()
for (i in names(unique_levels)) {
  for (level in unique_levels[[i]]) {
    required_columns <- c(required_columns, paste0(i, "_", gsub(" ", "", level)))
  }
}

# Asegúrate de que dummies_df contiene todas las columnas necesarias
# Agregar las columnas faltantes manualmente
for (col in required_columns) {
  if (!col %in% colnames(dummies_df)) {
    dummies_df[[col]] <- 0
  }
}

dummies_df

# Reordenar las columnas para que coincidan con el orden esperado
dummies_df <- dummies_df %>% select(all_of(required_columns))


# Verificar las columnas finales en dummies_df
print(colnames(dummies_df))

dummies_df



##############################


surveys = read.csv("C:\\Users\\Usuario\\Downloads\\users_surveyed.csv")
head(surveys)

surveys <- surveys %>% select(Producto.1:Producto.18)
surveys
# Supongamos que tu dataframe surveys tiene las puntuaciones de los usuarios
# Seleccionar la fila del usuario 1
# Supongamos que dummies_df ya contiene las variables dummy y que surveys tiene los puntajes

# Iterar sobre cada usuario (asumiendo que surveys tiene 15 filas)



for (i in 1:18) {
  # Seleccionar la fila correspondiente al usuario i
  puntaje_usuario <- surveys[i, ]  # Obtener los puntajes del usuario i
  puntaje_transpuesto <- as.vector(t(puntaje_usuario))  # Transponer los puntajes
  
  # Crear un nuevo dataframe con las variables dummy
  user_df <- dummies_df
  
  # Añadir la columna 'puntaje' al nuevo dataframe
  user_df$puntaje <- puntaje_transpuesto
  
  # Asignar el dataframe a una variable con nombre dinámico
  assign(paste0("user_", i), user_df)
}

# Ejemplo para ver el contenido de user_1
head(dummies_df)

head(user_1)

user_11
## ya podemos realizar las regresiones para cada usuario



