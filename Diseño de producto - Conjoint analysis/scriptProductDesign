#Conjoint Analysis
install.packages("readxl")
library(readxl)
install.packages("dplyr")
library(dplyr)
install.packages("ggplot2")
install.packages("tidyr")
library(tidyr)
library("ggplot2")
install.packages("gridExtra")
library("gridExtra")
install.packages("fastDummies")
library(fastDummies)

 
#Cargamos el dataframe con los 18 productos generados con la libreria conjoint:
df_prod = read.csv("C:\\Users\\Usuario\\Documents\\df_cjb.csv") 

## PREPARANDO LOS DATOS -----

# Dropeo la primera columna y columnas desde "Tamaño pulgadas" en adelante
df_prod <- df_prod %>% select(-1, -(which(colnames(df_prod) == "Tamaño..pulgadas."):ncol(df_prod)))

# Para la columna Tamaño..pulgadas..1, seleccionamos "42" como nivel base
df_prod$Tamaño..pulgadas..1 <- factor(df_prod$Tamaño..pulgadas..1, levels = unique(df_prod$Tamaño..pulgadas..1))
df_prod$Tamaño..pulgadas..1 <- relevel(df_prod$Tamaño..pulgadas..1, ref = "42")

# Para la columna Resolución, seleccionamos "1080p" como nivel base
df_prod$Resolución <- factor(df_prod$Resolución, levels = unique(df_prod$Resolución))
df_prod$Resolución <- relevel(df_prod$Resolución, ref = "1080p")

# Para la columna Marca, seleccionamos "Noblex" como nivel base
df_prod$Marca <- factor(df_prod$Marca, levels = unique(df_prod$Marca))
df_prod$Marca <- relevel(df_prod$Marca, ref = "Noblex")

# Para la columna Emisor.Aromático.1, seleccionamos "Naturales" como nivel base
df_prod$Emisor.Aromático.1 <- factor(df_prod$Emisor.Aromático.1, levels = unique(df_prod$Emisor.Aromático.1))
df_prod$Emisor.Aromático.1 <- relevel(df_prod$Emisor.Aromático.1, ref = "Naturales")

# Para la columna Precio..ARS..1, seleccionamos "550000" como nivel base
df_prod$Precio..ARS..1 <- factor(df_prod$Precio..ARS..1, levels = unique(df_prod$Precio..ARS..1))
df_prod$Precio..ARS..1 <- relevel(df_prod$Precio..ARS..1, ref = "550000")

# Generamos las variables dummy utilizando el paquete fastDummies
dummies_df <- dummy_cols(df_prod, 
                         select_columns = c("Tamaño..pulgadas..1", "Resolución", "Marca", "Emisor.Aromático.1", "Precio..ARS..1"),
                         remove_first_dummy = TRUE, # Esto elimina el nivel base
                         remove_selected_columns = TRUE) # Esto elimina las columnas originales



# Cargamos el dataframe con los datos de las encuestas
surveys_complete = read.csv("C:\\Users\\Usuario\\Downloads\\users_surveyed.csv")
#Por ahora nos quedamos solo con los puntajes a los productos
surveys <- surveys_complete %>% select(Producto.1:Producto.18)

#Formateamos para tener un dataframe por usuario encuestado (18 usuarios) y sus respectivos puntajes a los 18 productos

# Iteramos sobre cada usuario
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


## PREGUNTA 1 Corremos la Regresion para los 18 usuarios---- 

# Para los 18 user dataframes: user_1, user_2, ..., user_18
# Crear una lista para almacenar los modelos
modelos_list <- list()
modelos_summary <- list()

# Ajustar un modelo de regresión para cada usuario 
for (i in 1:18) {
  # Nombre del dataframe correspondiente al usuario
  user_df <- get(paste("user_", i, sep = ""))
  
  # Ajustar el modelo de regresión lineal
  modelo <- lm(puntaje ~ ., data = user_df)
  
  # Guardar el modelo en la lista
  modelos_summary[[paste("Modelo_Usuario_", i, sep = "")]] <- modelo
  
  # Mostrar el resumen del modelo
  cat("Resumen del Modelo para el Usuario", i, ":\n")
  print(summary(modelo))
  cat("\n")  # Añadir una línea en blanco para mejorar la legibilidad
}

## Solo coeficientes
# Ajustar un modelo de regresión para cada usuario 
for (i in 1:18) {
  # Nombre del dataframe correspondiente al usuario
  user_df <- get(paste("user_", i, sep = ""))
  
  # Ajustar el modelo de regresión lineal
  modelo <- lm(puntaje ~ ., data = user_df)
  
  # Guardar el modelo en la lista
  modelos_list[[paste("Modelo_Usuario_", i, sep = "")]] <- modelo
}


##  PREGUNTA 2: Importancia relativa de los atributos -----

library(ggplot2)

# Crear un dataframe para almacenar las importancias relativas de cada usuario y el atributo de mayor importancia
importancias_relativas_df <- data.frame(
  Usuario = integer(),
  Tamaño = numeric(),
  Resolución = numeric(),
  Marca = numeric(),
  Emisor_Aromático = numeric(),
  Precio = numeric(),
  Atributo_Mayor_Importancia = character()
)

# Bucle para calcular las importancias relativas para cada usuario, generar gráficos y almacenar resultados
for (indice_usuario in 1:18) {
  # Obtener coeficientes del modelo para el usuario actual
  coeffs <- as.vector(summary(modelos_list[[indice_usuario]])$coefficients[, 1])
  
  # Calcular el rango de las utilidades parciales para cada atributo
  tamaño_range <- max(c(coeffs[2:4])) - min(c(0, coeffs[2:4]))
  resolucion_range <- max(c(coeffs[5:6])) - min(c(0, coeffs[5:6]))
  marca_range <- max(c(coeffs[7:9])) - min(c(0, coeffs[7:9]))
  emisor_range <- max(c(coeffs[10:11])) - min(c(0, coeffs[10:11]))
  precio_range <- max(c(coeffs[12:13])) - min(c(0, coeffs[12:13]))
  
  # Calcular el rango total sumando los rangos de todos los atributos
  total_range <- sum(tamaño_range, resolucion_range, marca_range, emisor_range, precio_range)
  
  # Calcular la importancia relativa para cada atributo
  tamaño_importance <- tamaño_range / total_range
  resolucion_importance <- resolucion_range / total_range
  marca_importance <- marca_range / total_range
  emisor_importance <- emisor_range / total_range
  precio_importance <- precio_range / total_range
  
  # Crear un vector de importancias relativas para determinar el atributo de mayor importancia
  importancias <- c(tamaño_importance, resolucion_importance, marca_importance, emisor_importance, precio_importance)
  nombres_atributos <- c("Tamaño (pulgadas)", "Resolución", "Marca", "Emisor Aromático", "Precio")
  
  # Identificar el atributo con la mayor importancia relativa
  atributo_mayor_importancia <- nombres_atributos[which.max(importancias)]
  
  # Almacenar las importancias relativas y el atributo de mayor importancia en el dataframe
  importancias_relativas_df <- rbind(
    importancias_relativas_df,
    data.frame(
      Usuario = indice_usuario,
      Tamaño = tamaño_importance,
      Resolución = resolucion_importance,
      Marca = marca_importance,
      Emisor_Aromático = emisor_importance,
      Precio = precio_importance,
      Atributo_Mayor_Importancia = atributo_mayor_importancia
    )
  )
  
  # Crear un dataframe para el gráfico de importancias relativas
  relative_importance <- data.frame(
    Attribute = c("Tamaño (pulgadas)", "Resolución", "Marca", "Emisor Aromático", "Precio"),
    Importance = importancias
  )
  
  # Crear el gráfico de importancias relativas para el usuario actual
  p <- ggplot(relative_importance, aes(x = Attribute, y = Importance)) +
    geom_bar(stat = "identity", fill = "steelblue") +
    theme_minimal() +
    labs(
      title = paste("Relative Importance of Attributes (Usuario", indice_usuario, ")"),
      x = "Attributes",
      y = "Relative Importance"
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # Mostrar el gráfico
  print(p)
}

# Mostrar el dataframe con las importancias relativas y el atributo de mayor importancia para cada usuario
print(importancias_relativas_df)


## PREGUNTA 3 Price PW utilities ----------------------------------------------------------------
library(ggplot2)
library(gridExtra)

# Bucle para generar los gráficos de utilidades parciales para cada usuario
for (indice_usuario in 1:18) {
  # Obtener coeficientes del modelo
  coeffs <- as.vector(summary(modelos_list[[indice_usuario]])$coefficients[,1])
  
  # Utilidades parciales para Precio (asumimos que el nivel base es 550000)
  pw_ut_precio <- c(0, coeffs[12:13])  # Ajustar índices si es necesario
  
  # Crear un dataframe con las utilidades parciales
  precio_levels <- c("550000", "950000", "1250000")
  pw_ut_precio_df <- data.frame(Precio = precio_levels, PartWorthUtility = pw_ut_precio)
  
  # Crear el gráfico de utilidades parciales para el precio usando líneas
  p <- ggplot(pw_ut_precio_df, aes(x = Precio, y = PartWorthUtility, group = 1)) +
    geom_line(color = "steelblue", size = 1.2) +  # Línea que conecta los puntos
    geom_point(size = 4, color = "steelblue") +   # Puntos en cada nivel de precio
    theme_minimal() +
    labs(title = paste("Part-Worth Utilities for Precio (Usuario", indice_usuario, ")"),
         x = "Precio (ARS)",
         y = "Part-Worth Utilities") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # Mostrar el gráfico
  print(p)
}

## PREGUNTA 4: WTP ante cambios en el atributo más importante para cada usuario. -----
# Crear un dataframe para almacenar la disposición a pagar (WTP) de cada usuario
wtp_df <- data.frame(
  Usuario = integer(),
  Atributo_Mayor_Importancia = character(),
  WTP = numeric()
)

# Bucle para calcular la disposición a pagar para cada usuario
for (indice_usuario in 1:18) {
  # Obtener coeficientes del modelo para el usuario actual
  coeffs <- as.vector(summary(modelos_list[[indice_usuario]])$coefficients[, 1])
  
  # Identificar el atributo más importante para el usuario actual
  atributo_mayor_importancia <- importancias_relativas_df$Atributo_Mayor_Importancia[indice_usuario]
  
  # Calcular la diferencia en utilidades para el atributo más importante
  if (atributo_mayor_importancia == "Tamaño (pulgadas)") {
    diff_utilidad_importante <- max(coeffs[2:4]) - min(c(0, coeffs[2:4])) # pasar de 42 a 72"
  } else if (atributo_mayor_importancia == "Resolución") {
    diff_utilidad_importante <- max(coeffs[5:6]) - min(c(0, coeffs[5:6])) # pasar de 1080p a 8K
  } else if (atributo_mayor_importancia == "Marca") {
    diff_utilidad_importante <- max(coeffs[7:9]) - min(c(0, coeffs[7:9])) # pasar de Noblex a cualquiera de las otras 3 marcas -> las preferencias no son tan lineales
  } else if (atributo_mayor_importancia == "Emisor Aromático") {
    diff_utilidad_importante <- max(coeffs[10:11]) - min(c(0, coeffs[10:11])) # pasar del emisor de aromas naturales al premium
  } else if (atributo_mayor_importancia == "Precio") {
    diff_utilidad_importante <- max(coeffs[12:13]) - min(c(0, coeffs[12:13])) #pasar del precio base de 1250000 a 550000
  }
  
  # Calcular la diferencia en utilidades para el atributo Precio
  diff_utilidad_precio <- max(coeffs[12:13]) - min(c(0, coeffs[12:13]))
  
  # Calcular la diferencia de precio en dinero (de 550,000 a 1,250,000)
  diff_precio_dinero <- 1250000 - 550000
  
  # Calcular la disposición a pagar (WTP)
  wtp <- diff_utilidad_importante * (diff_precio_dinero / diff_utilidad_precio)
  
  # Almacenar la WTP y el atributo más importante en el dataframe
  wtp_df <- rbind(
    wtp_df,
    data.frame(
      Usuario = indice_usuario,
      Atributo_Mayor_Importancia = atributo_mayor_importancia,
      WTP = wtp
    )
  )
}

# Mostrar el dataframe con la disposición a pagar (WTP) para cada usuario
print(wtp_df)



## PREGUNTA 5: Realizar una segmentación. A partir de los segmentos identificados según su uso


#Comente respecto a los segmentos obtenidos. ¿Qué producto/servicio podría ofrecer a cada segmento? (HINT: considere no más de 4 segmentos).

surveys_complete
surveys_complete <- surveys_complete[, -ncol(surveys_complete)]
# Obtener la posición de "Columna.24"
pos_columna_24 <- which(names(surveys_complete) == "Columna.24")

# Renombrar las columnas a partir de la columna siguiente a "Columna.24"
names(surveys_complete)[(pos_columna_24 + 1):ncol(surveys_complete)] <- c("Uso_Movies_Series", "Uso_TV_Live", "Uso_Videogames", "Uso_RRSS", "Uso_YT_Spotify")

# Eliminar la última fila si todos los valores son NA
if (all(is.na(surveys_complete[nrow(surveys_complete), ]))) {
  surveys_complete <- surveys_complete[-nrow(surveys_complete), ]
}

# Eliminar la columna "Columna.24"
surveys_complete <- surveys_complete[, !(names(surveys_complete) %in% "Columna.24")]

# Eliminar la columna "Marca.temporal"
surveys_complete <- surveys_complete[, !(names(surveys_complete) %in% "Marca.temporal")]

# Agregar columna de índices
surveys_complete <- cbind(Usuario = 1:nrow(surveys_complete), surveys_complete)

# Mostrar el DataFrame actualizado
# Supongamos que la columna común es 'usuario_id'
merged_df <- merge(surveys_complete, importancias_relativas_df, by = "Usuario", all.x = TRUE)

# Visualiza el dataframe resultante
merged_df



# Filtrar usuarios que puntuaron con 5 en cada uno de los usos
usuarios_con_5_movies_series <- merged_df[
  merged_df$Uso_Movies_Series == 5,
]
usuarios_con_5_movies_series <- usuarios_con_5_movies_series[, c("Atributo_Mayor_Importancia", "Edad", "Género", "Provincia.donde.vivís")]
usuarios_con_5_movies_series

usuarios_con_5_TV_Live <- merged_df[
  merged_df$Uso_TV_Live == 5,
]
usuarios_con_5_TV_Live <- usuarios_con_5_TV_Live[, c("Atributo_Mayor_Importancia", "Edad", "Género", "Provincia.donde.vivís")]


usuarios_con_5_Videogames <- merged_df[
  merged_df$Uso_Videogames == 5,
]
usuarios_con_5_Videogames <- usuarios_con_5_Videogames[, c("Atributo_Mayor_Importancia", "Edad", "Género", "Provincia.donde.vivís")]


usuarios_con_5_YT_spt <- merged_df [
  merged_df$Uso_YT_Spotify == 5,
]
usuarios_con_5_YT_spt <- usuarios_con_5_YT_spt[, c("Atributo_Mayor_Importancia", "Edad", "Género", "Provincia.donde.vivís")]


usuarios_con_5_RRSS <- merged_df [
  merged_df$Uso_RRSS == 5,
]
usuarios_con_5_RRSS <- usuarios_con_5_RRSS[, c("Atributo_Mayor_Importancia", "Edad", "Género", "Provincia.donde.vivís")]


##PREGUNTA 6 ¿Qué producto se quedaría con el market share? -----
#Genere dos perfiles de productos que no aparezcan en su cuestionario. Suponga que
#actualmente éstos son los únicos productos en el mercado ofrecidos por los
#competidores X e Y. Basándose en el total de sus encuestas, ¿cuál sería su estimación
#sobre la participación de mercado para cada uno de estos productos?


#En que indices estan los coeficientes necesarios?
#PROD 1: tamaño55: 4; resol8k: 6; MARCASAMS: 7; Emisor natural: nivel base = 0; Precio 950k: 12
#PROD 2; tamaño65: 3; resol4k: 5; marcaLG: 8; eMISOR especfico: 10; precio1250k: 13

# Imprimir el dataframe de nuevos productos
print(nuevos_productos)
# Definir los niveles de los nuevos productos
nuevo_producto_1 <- c("Tamaño..pulgadas..1_55", "Resolucion_8k", "Marca_Samsung", "Emisor_Aromatico_Naturales", "Precio..ARS..1_950000")
nuevo_producto_2 <- c("Tamaño..pulgadas..1_65", "Resolución_4k", "Marca_LG", "Emisor.Aromático.1_Específicos", "Precio..ARS..1_1250000")

# Definir los índices de los niveles de los nuevos productos
nuevo_producto_1_indices <- c(4, 6, 7, 0, 12)  # PROD 1: tamaño55, resol8k, MARCASAMS, Emisor natural (0), Precio 950k
nuevo_producto_2_indices <- c(3, 5, 8, 10, 13) # PROD 2: tamaño65, resol4k, marcaLG, eMISOR específico, precio1250k

# Inicializar los dataframes para almacenar los resultados
resultados_producto_1 <- data.frame(Usuario = 1:18, Suma_Utilidades = numeric(18))
resultados_producto_2 <- data.frame(Usuario = 1:18, Suma_Utilidades = numeric(18))

# Iterar sobre cada usuario
for (indice_usuario in 1:18) {
  # Obtener coeficientes del modelo
  coeffs <- as.vector(summary(modelos_list[[indice_usuario]])$coefficients[, 1])
  
  # Inicializar suma de utilidades
  suma_utilidades_producto_1 <- 0
  suma_utilidades_producto_2 <- 0
  
  # Sumar utilidades para el primer nuevo producto
  for (indice in nuevo_producto_1_indices) {
    if (indice != 0) {  # Evitar sumar el valor base que es 0
      suma_utilidades_producto_1 <- suma_utilidades_producto_1 + coeffs[indice]
    } else {
      suma_utilidades_producto_1 <- suma_utilidades_producto_1 + 0  # Agregar 0 por el nivel base
    }
  }
  
  # Sumar utilidades para el segundo nuevo producto
  for (indice in nuevo_producto_2_indices) {
    suma_utilidades_producto_2 <- suma_utilidades_producto_2 + coeffs[indice]
  }
  
  # Guardar resultados en los dataframes
  resultados_producto_1$Suma_Utilidades[indice_usuario] <- suma_utilidades_producto_1
  resultados_producto_2$Suma_Utilidades[indice_usuario] <- suma_utilidades_producto_2
}

# Asignar nombres de las columnas
colnames(resultados_producto_1) <- c("Usuario", "Suma Utilidades Producto 1")
colnames(resultados_producto_2) <- c("Usuario", "Suma Utilidades Producto 2")

# Mostrar resultados
print(suma_utilidades_1 <- sum(resultados_producto_1$`Suma Utilidades Producto 1`))
print(suma_utilidades_2 <- sum(resultados_producto_2$`Suma Utilidades Producto 2`))



#luego calcular el mkt share en base a las sumas de utilidades 
max(suma_utilidades_1, suma_utilidades_2) 
#El producto que se llevaría el market share es el numero 2. Ya que si tenemos en cuenta la suma de sus utilidades, 
