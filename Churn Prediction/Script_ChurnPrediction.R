library("tidyverse")
setwd("~/Documents/Universidad Torcuato Di Tella/MG01 MEAN")
customer_churn <- read.csv("customer_churn.csv")
new_customers <- read_csv("new_customers.csv")

#(a)
#Llamando a las librerías que utilizaremos
library("ggplot2")

sum(is.na(customer_churn))
#No hay datos que falten

#Información de los datos (media, mediana, min, max, count, etc)
customer_churn %>%
  summary()

#Barplot comparando los grupos que tienen gestor y los que no tienen con si 
#volvieron o no usando ggplot
customer_churn %>%
  filter(Account_Manager == 1 | Account_Manager == 0) %>%
  ggplot(aes(as.character(Account_Manager), fill = as.character(Churn))
  ) + geom_bar(position = "dodge"
  ) + ggtitle("Comparación de customer churn para\nclientes con y sin gestor"
  ) + labs(x = "Tiene gestor o no", y =
             "Frecuencia")

#(b)
#Para el heatmap hay que usar el package corrplot
#Variables no-numéricos no pueden tener correlation
library(corrplot)

#Llamando al archivo y guardandolo en el variable customer_churn
setwd("~/Documents/Universidad Torcuato Di Tella/MG01 MEAN")
customer_churn <- read.csv("customer_churn.csv")

#Haciendo el mapa de calor de la correlaciones
corrplot(cor(select_if(customer_churn, is.numeric)))

#Parece haber una gran correlación entre las variables Churn y Num_Sites.
#Después parece haber una correlación significante entre Years y Churn.
#Ninguna otra combinación de variables tiene alta correlación.

#(c)
#Queremos ver si Churn disminuye dependiendo si el cliente tiene gestor asignado
#Entonces nos interesa la proporción de Churn para cada subgrupo
#Haremos un proportion test para la diferencia de las proporciones

#Filtrando los que tuvieron gestores
customer_churn %>%
  filter(Account_Manager == 1) %>%
  select(Churn) -> con_gestor

#Filtrando los que no tuevieron gestores
customer_churn %>%
  filter(Account_Manager == 0) %>%
  select(Churn) -> sin_gestor

#Haremos el calculo "a mano"
#Calculando las n
n_x <- dim(con_gestor)[1]
n_y <- dim(sin_gestor)[1]

#La cantidad de Churn por grupo
churn_x <- sum(con_gestor)
churn_y <- sum(sin_gestor)

#Calculando las proporciones
p_raya_x <- churn_x/n_x
p_raya_y <- churn_y/n_y

n_x*p_raya_x*(1 - p_raya_x) > 5
n_y*p_raya_y*(1 - p_raya_y) > 5
#Las dos cumplen la condición np(1-p) > 5. Son muestras suficientemente grandes
#y podemos considerar el estadístico con distribución normal

#Usamos prop.test() de R
prop.test(c(churn_x, churn_y), c(n_x, n_y), correct = FALSE)

##Nuestro p-valor es 0.034, menor a nuestro alpha de 0.05, así que rechazamos
#la hipótesis nula en el nivel de significación de 95%. Además, vemos que 0 no 
#está en el rango de valor para el intervalo de confianza (más evidencía de 
#diferencia de proporciones). 

#(d)
#Tenemos que filtrar ahora para solo tener las filas donde Years > 7. 
#Filtrando
customer_churn %>%
  filter(Years > 7) -> customers_seven_plus_years

#Ahora filtrando para que sólo nos de Churn:
customers_seven_plus_years %>%
  select(Churn) -> churn_spy

#Ahora haciendo los calculos para  obtener los variables para la prueba de 
#hipótesis
p_raya <- sum(churn_spy)/dim(churn_spy)[1]
pi_cero <- 0.3
n <- dim(churn_spy)[1]

#Comprobando que np(1-p) > 5:
n*p_raya*(1 - p_raya) > 5

#Nos da TRUE. Podemos continuar. Usando binom.test()
binom.test(sum(churn_spy), dim(churn_spy)[1], p = 0.3, alternative = "greater")

#Vemos con el binom.test que no podemos rechazar la hipótesis nula

#Ahora calculando y graficando la potencia
pi_estrella <- seq(from = 0.3001, to = 1.000, by = 0.001)
z_crit <- pi_cero + qnorm(0.95)*sqrt(pi_cero*(1 - pi_cero)/n)
potencia <- 1 - pnorm((z_crit - pi_estrella)/sqrt(pi_cero*(1 - pi_cero)/n))
plot(pi_estrella, potencia, xlab = "pi", main = "Curva de Potencia", type = "l", 
     lwd = 1)

#(e)
#Vamos a convertir la variable Account_Manager en factor variable
customer_churn$Account_Manager <- as.factor(customer_churn$Account_Manager)

#Creando el train set y el validation set
smp_size <- floor(0.80 * nrow(customer_churn))
set.seed(123)
train_ind <- sample(seq_len(nrow(customer_churn)), size = smp_size)

train <- customer_churn[train_ind, ]
validation <- customer_churn[-train_ind, ] 

#(f)
n_distinct(customer_churn$Names)
n_distinct(customer_churn$Location)
n_distinct(customer_churn$Company)
#Podemos ver que hay muchos valores únicos para estas tres columnas. No los 
#incluiremos en los modelos ya que tampoco hay forma de agruparlos en grupos
#más chicos (podríamos intentar agrupar por estado pero muy complicado)

n_distinct(customer_churn$Onboard_date)
#También no incluiría Onboard_date porque tiene muchísimos valores únicos
#pero tal vez hay una forma de agrupar por año? Pero esto es mejor porque
#tendríamos cómo 11 niveles para año (un poco mucho?)

#MLP
#Vamos a empezar creando un modelo con todos las variables restantes:
modelo_mlp_1 <- lm(Churn ~ Age + Account_Manager + Years + Num_Sites
                   + Total_Purchase, data = train)
summary(modelo_mlp_1)
#Todas las variables que dieron significativas en el modelo las incluiremos
#en el próximo modelo también. Ser significativa significa que hemos rechazado
#la hipótesis nula que su verdadero valor es 0 al 95% de significatividad.
#Aunque Account_Manager no es significativo al 5% en este modelo, sí lo es al 
#10%; lo incluiremos porque el analisis surge de ver cómo afecta tener un gestor. 
#Total_Purchase no es significativo en ningún nivel importante y este sí no 
#lo consideramos en el próximo modelo.

#Think about using log for Num_Sites because we can see from the plot that
#there seems to be a positive relationship. Also think about squaring Years
#and leave Age as is. But our adjusted R2 is worse.

modelo_mlp_2 <- lm(Churn ~ Age + Account_Manager + Years + Num_Sites, 
                   data =train)
summary(modelo_mlp_2)
#Vemos que el único valor que realmente cambia es el constante, así que no 
#tenemos problemas de multicolinealidad con Total_Purchase y las otras variables.
#Además,al  excluirlo, no tendremos sesgo por variable omitida? El R2 ajustado
#es menor en el segundo modelo, pero es una diferencia casi nula. Todas las 
#otras variables siguen dando significativas por lo menos al 10% así que este 
#será nuestro modelo que utilizaremos.

#Cómo este es un modelo de probabilidad lineal, podemos interpretar los 
#coeficientes directamente

#Constante: un cliente sin gestor de 0 años con 0 años cómo cliente con 0 
#sitios web que utilizan el servicio. Lógicamente no tiene sentido este origen.

#Pendientes:
#Age: con cada año de edad que un cliente cumpla, su probabilidad de volver a 
#comprar el servicio aumenta 0.4609 puntos porcentuales, ceteris paribus.

#Account_Manager: si un cliente es asignado un gestor, su probabilidad de volver
#a comprar el servicio es 4.0085 puntos porcentuales más alta que la de un 
#cliente sin un gestor asignado, ceteris paribus.

#Years: por casa año como cliente de la agencia, la probabilidad de que ese 
#cliente vuelva a comprar el servicio aumenta 6.1888 puntos porcentuales, ceteris
#paribus.

#Num_Sites: por cada sitio web que utiliza el servicio, la probabilidad del
#cliente que vuelva a comprar el servicio aumenta 10.7422 puntos porcentuales,
#ceteris paribus.


#Probit
#Usamos la misma lógica que usamos en el modelo linear de probabilidad. Omitiremos
#las variables con muchos valores únicos e incluiremos las variables restantes.
#Armamos el primer modelo con todas estas variables:
modelo_probit_1 <- glm(Churn ~ Age + Account_Manager + Years + Num_Sites
                       + Total_Purchase, family = binomial(link = "probit"),
                       data = train)
summary(modelo_probit_1)
#De nuevo vemos que Total_Purchase es la única variable que no es significativa.
#Armaremos un nuevo modelo excluyendola:
modelo_probit_2 <- glm(Churn ~ Age + Account_Manager + Years + Num_Sites,
                       family = binomial(link = "probit"), data = train)
summary(modelo_probit_2)
#De nuevo, el único valor que realmente cambia es el constante. Ahora, no podemos
#sólo interpretar los valores de los coeficientes ya que este es un modelo 
#probit. Calcularemos los efectos marginales viendo la diferencia de probabilidades
#para dos "clientes" que sólo cambia la media de una categoría por una unidad.

#Age:
#Efecto de cambio de una unidad a la edad media sin gestor:
pred_probit_age_sg <- predict(modelo_probit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age) + 1), Account_Manager = factor(0:0),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_probit_age_sg)

#Efecto de cambio de una unidad a la edad media con gestor:
pred_probit_age_cg <- predict(modelo_probit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age) + 1), Account_Manager = factor(1:1),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_probit_age_cg)

#Account_Manager:
pred_probit_am <- predict(modelo_probit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(0:1),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_probit_am)

#Years:
#Efecto de cambio de una unidad a la antigüedad media sin gestor:
pred_probit_years_sg <- predict(modelo_probit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(0:0),
  Years = c(mean(train$Years), mean(train$Years) + 1),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_probit_years_sg)

#Efecto de cambio de una unidad a la antigüedad media con gestor:
pred_probit_years_cg <- predict(modelo_probit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(1:1),
  Years = c(mean(train$Years), mean(train$Years) + 1),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_probit_years_cg)

#Num_Sites:
#Efecto de cambio de una unidad a la media de sitios de web utilizados sin
#gestor:
pred_probit_numsites_sg <- predict(modelo_probit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(0:0),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites) + 1)),
  type = "response")
diff(pred_probit_numsites_sg)

#Efecto de cambio de una unidad a la media de sitios de web utilizados con
#gestor:
pred_probit_numsites_cg <- predict(modelo_probit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(1:1),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites) + 1)),
  type = "response")
diff(pred_probit_numsites_cg)


#Logit
modelo_logit_1 <- glm(Churn ~ Age + Account_Manager + Years + Num_Sites + 
                        Total_Purchase, family = binomial(link = "logit"), 
                      data = train)
summary(modelo_logit_1)
#De nuevo vemos que Total_Purchase es la única variable que no es significativa.
#Armaremos un nuevo modelo excluyendola:
modelo_logit_2 <- glm(Churn ~ Age + Account_Manager + Years + Num_Sites,
                      family = binomial(link = "logit"), data = train)
summary(modelo_logit_2)
#De nuevo, el único valor que realmente cambia es el constante. Ahora, no podemos
#sólo interpretar los valores de los coeficientes ya que este es un modelo 
#probit. Calcularemos los efectos marginales viendo la diferencia de probabilidades
#para dos "clientes" que sólo cambia la media de una categoría por una unidad.

#Age:
#Efecto de cambio de una unidad a la edad media sin gestor:
pred_logit_age_sg <- predict(modelo_logit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age) + 1), Account_Manager = factor(0:0),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_logit_age_sg)

#Efecto de cambio de una unidad a la edad media con gestor:
pred_logit_age_cg <- predict(modelo_logit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age) + 1), Account_Manager = factor(1:1),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_logit_age_cg)

#Account_Manager:
pred_logit_am <- predict(modelo_logit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(0:1),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_logit_am)

#Years:
#Efecto de cambio de una unidad a la antigüedad media sin gestor:
pred_logit_years_sg <- predict(modelo_logit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(0:0),
  Years = c(mean(train$Years), mean(train$Years) + 1),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_logit_years_sg)

#Efecto de cambio de una unidad a la antigüedad media con gestor:
pred_logit_years_cg <- predict(modelo_logit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(1:1),
  Years = c(mean(train$Years), mean(train$Years) + 1),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites))),
  type = "response")
diff(pred_logit_years_cg)

#Num_Sites:
#Efecto de cambio de una unidad a la media de sitios de web utilizados sin
#gestor:
pred_logit_numsites_sg <- predict(modelo_logit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(0:0),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites) + 1)),
  type = "response")
diff(pred_logit_numsites_sg)

#Efecto de cambio de una unidad a la media de sitios de web utilizados con
#gestor:
pred_logit_numsites_cg <- predict(modelo_logit_2, newdata = data.frame(
  Age = c(mean(train$Age), mean(train$Age)),
  Account_Manager = factor(1:1),
  Years = c(mean(train$Years), mean(train$Years)),
  Num_Sites = c(mean(train$Num_Sites), mean(train$Num_Sites) + 1)),
  type = "response")
diff(pred_logit_numsites_cg)

#(g)
#Utilizando los modelos para predecir el churn usando el validation set
fcst_mlp <- predict(modelo_mlp_2, newdata = validation, type="response")
fcst_probit <- predict(modelo_probit_2, newdata = validation, type="response")
fcst_logit <- predict(modelo_logit_2, newdata = validation, type="response")

#Veamos los modelos para comparar cual es preferible.
library("stargazer")
stargazer(list(modelo_mlp_2, modelo_probit_2, modelo_logit_2), type = "text",
          keep.stat = c("n", "adj.rsq"))

#Usemos vif(mod) de car package para chequear multicolinealidad. Para estos
#modelos hay poca evidencia de multicolinealidad (todos los vif = 1)
vif(modelo_mlp_2)
vif(modelo_probit_2)
vif(modelo_logit_2)

#Chequeando el pseudo R2 para los modelos:
pseudoR2_probit <- 1- (modelo_probit_2$deviance)/(modelo_probit_2$null.deviance)
pseudoR2_logit <- 1- (modelo_logit_2$deviance)/(modelo_logit_2$null.deviance)
c(pseudoR2_probit, pseudoR2_logit)
#Muy similares para los dos

#Es peor tener falsos negativos: predecir que no vuelven pero vuelven en vez
#de predecir que vuelven pero en realidad no. Buscaremos el modelo con menor
#porcentaje de falsos negativos (amongst other things). Haciendo la matriz
#de confusión:
library("caret")
dummy_mlp <- as.numeric(fcst_mlp >= 0.5)
dummy_probit <- as.numeric(fcst_probit >= 0.5)
dummy_logit <- as.numeric(fcst_logit >= 0.5)
dummy_mlp <- as.factor(dummy_mlp)
dummy_probit <- as.factor(dummy_probit)
dummy_logit <- as.factor(dummy_logit)

churn <- as.factor(validation$Churn)

confusionMatrix(dummy_mlp, churn)
confusionMatrix(dummy_probit, churn)
confusionMatrix(dummy_logit, churn)

#Evaluacion de pronosticos
library(forecast)
accuracy(validation$Churn,fcst_mlp)
accuracy(validation$Churn,fcst_probit)
accuracy(validation$Churn,fcst_logit)

#Test de igualdad en el desempeño
e_mlp <- validation$Churn - fcst_mlp
e_probit <- validation$Churn - fcst_probit
e_logit <- validation$Churn - fcst_logit

L2_mlp <- e_mlp^2
L2_probit <- e_probit^2
L2_logit <- e_logit^2

DL_pl <- L2_probit - L2_logit
summary(lm(DL_pl ~ 1))

DL_pm <- L2_probit - L2_mlp
summary(lm(DL_pm ~ 1))

DL_lm <- L2_logit - L2_mlp
summary(lm(DL_lm ~ 1))

#Elegimos el modelo logit. Ahora prediciendo Churn en new_customers
new_customers$Account_Manager <- as.factor(new_customers$Account_Manager)
predict(modelo_logit_2, newdata = new_customers, type="response")

#(h)
bootstrap_predictions_mlp <- c()
bootstrap_predictions_probit <- c()
bootstrap_predictions_logit <- c()

for (i in 1:1000)
{
  train_ind_boot <- sample(seq_len(nrow(customer_churn)), size = smp_size)
  train_boot <- customer_churn[train_ind_boot, ]
  modelo_mlp_boot <- lm(Churn ~ Age + Account_Manager + Years + Num_Sites, 
                        data = train_boot)
  modelo_probit_boot <- glm(Churn ~ Age + Account_Manager + Years + Num_Sites,
                            family = binomial(link = "probit"), data = train_boot)
  modelo_logit_boot <- glm(Churn ~ Age + Account_Manager + Years + Num_Sites,
                           family = binomial(link = "logit"), data = train_boot)
  fcst_mlp_boot <- predict(modelo_mlp_boot, newdata = validation,
                           type="response")
  fcst_probit_boot <- predict(modelo_probit_boot, newdata = validation,
                              type="response")
  fcst_logit_boot <- predict(modelo_logit_boot, newdata = validation,
                             type="response")
  bootstrap_predictions_mlp <- append(bootstrap_predictions_mlp, fcst_mlp_boot)
  bootstrap_predictions_probit <- append(bootstrap_predictions_probit, fcst_probit_boot)
  bootstrap_predictions_logit <- append(bootstrap_predictions_logit, fcst_logit_boot)
}

matriz_boot_mlp <- matrix(bootstrap_predictions_mlp, nrow = 1000, ncol = 180, byrow = TRUE)
matriz_boot_probit <- matrix(bootstrap_predictions_probit, nrow = 1000, ncol = 180, byrow = TRUE)
matriz_boot_logit <- matrix(bootstrap_predictions_logit, nrow = 1000, ncol = 180, byrow = TRUE)

bootstrap_mean_mlp <-  c()
bootstrap_mean_probit <-  c()
bootstrap_mean_logit <-  c()

for (i in 1:180)
{
  bootstrap_mean_mlp[i] = mean(matriz_boot_mlp[,i])
  bootstrap_mean_probit[i] = mean(matriz_boot_probit[,i])
  bootstrap_mean_logit[i] = mean(matriz_boot_logit[,i])
}

ic_mlp_boot <- quantile(bootstrap_mean_mlp, probs = c(0.025, 0.975))
ic_probit_boot <- quantile(bootstrap_mean_probit, probs = c(0.025, 0.975))
ic_logit_boot <- quantile(bootstrap_mean_logit, probs = c(0.025, 0.975))