**Exámen Final**

Alumno: Boca Martino

Master in Management & Analytics

Universidad Torcuato Di Tella

Asignatura: Ventas & Marketing

Profesores: Ricardo Montoya, Julieta De Antonio, Santiago Loose 7/10/2024

El producto seleccionado para evaluar las valoraciones de los usuarios encuestados fue un Smart TV o TV inteligente. Se consideró este producto por ser ampliamente conocido por distintos públicos y por estar estrechamente ligado a la vida diaria de las personas, lo que asegura que la mayoría de los usuarios posean un buen nivel de familiaridad con sus características y especificaciones técnicas en términos generales.

En cuanto a los atributos seleccionados para el estudio, incluimos características típicas como el tamaño en pulgadas, la marca, la resolución y el precio. Además, exploramos un atributo innovador diseñado para mejorar la experiencia de disfrutar de contenido audiovisual: un difusor aromático dinámico. Este dispositivo se activaría en momentos clave de una serie, película o documental, emitiendo aromas que complementan la escena en pantalla. Los niveles de diferenciación del difusor aromático son los siguientes:

1. Aromas Naturales: Emisión de aromas sencillos como el olor a bosque, playa, flores o lluvia, sincronizados con escenas que muestran paisajes naturales.
1. Aromas Específicos: Aromas relacionados con situaciones más específicas, como el olor a comida (por ejemplo, pan recién horneado, café) o una chimenea encendida.
1. Aromas Personalizados (Premium\_custom): Aromas secuenciales configurables. El usuario puede ajustar tanto la intensidad como la frecuencia de los aromas. Este nivel permite transiciones entre aromas naturales y específicos, como en una escena de acción en la playa que comienza con el olor a brisa marina, cambia a pólvora durante una escena de disparos, y termina con un aroma de fuego o humo si hay una explosión.

   Creemos que existe un gran potencial en ofrecer experiencias cada vez más inmersivas dentro de la industria del entretenimiento, inspiradas en conceptos ya existentes como el cine 4D. La idea detrás de este atributo innovador es brindar una experiencia sensorial avanzada que esté al alcance de todos, en la comodidad de sus hogares, ya sea en el living o en el dormitorio.

   Diseño del estudio

   El diseño de la encuesta se realizó utilizando un script en R que emplea la librería Conjoint. Este enfoque generó un conjunto de 18 combinaciones de atributos con sus respectivos niveles, permitiendo una evaluación completa y balanceada de las preferencias de los usuarios. Luego, la encuesta fue realizada por medio de google forms ([link](https://docs.google.com/forms/d/1bsNGngqxy27yd72lI-ZhRgzu9PmgWmgP48L_CyDKXBk/prefill)) a 18 personas de diferentes características en términos de edad, género y locación geográfica, con el objetivo de captar un público amplio para analizar sus preferencias y valoraciones

   Atributos y niveles

1. Tamaño: 42” (base), 55”, 65”, 72”.
1. Resolución: 1080p (base), 4K, 8K.
1. Marca: Noblex (base), Samsung, LG, Phillips.
1. Precio: $550,000 (base), $950,000, $1,250,000.

Es importante destacar que los niveles base de estos atributos fueron seleccionados por cuestiones ordinales, eligiendo siempre el nivel más básico, con la excepción del atributo de la marca, donde se seleccionó una opción que representara una oferta conocida pero accesible para un público amplio. Esta selección tiene el objetivo de facilitar comparaciones y entender la predisposición del consumidor a optar por niveles superiores solo si perciben un valor claro en las mejoras ofrecidas.

Pregunta 1: Modelos de regresión lineal

Primero, le aplicamos formatos correctos tanto a los datos de las encuestas, contenidos en el archivo users\_surveyed como a los datos que contienen los 18 diferentes productos formados a partir de las combinaciones de niveles de los atributos (df\_cjb.csv).

Luego de ello, seteamos los niveles base para cada atributo y con la librería *fastdummies*, generamos las variables dummy correspondientes a las 18 combinaciones de atributos. Posteriormente, generamos un dataframe por usuario concatenando los puntajes asignados por los mismos al dataframe de dummies. Con esto, ya podemos correr la regresión para cada uno de los usuarios y guardar el resumen del modelo de cada uno de ellos. Por cuestiones de espacio los reportes de las 18 regresiones se encuentran en este [archivo](https://docs.google.com/document/d/1Lc5bKqrSyBWvCDLKfD6DPXsf_yFVuAs4bEjII41cpK8/edit?tab=t.0), o dentro de la carpeta de entrega llamado Regresiones\_Usuarios.

Pregunta 2: Importancias relativas

Luego, nos dedicamos a analizar la importancia relativa de cada uno de los atributos siguiendo la siguiente fórmula:

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.001.png)

Iterando por los 18 usuarios encuestados:

1. Calculamos el rango de variabilidad en el que se mueven cada una de las utilidades parciales de los atributos: Tamaño, Resolucion, Marca, Emisor aromatico y Precio
1. Calculamos el rango total, a partir de sumar los rangos calculados en el paso anterior.
1. Calculamos la importancia relativa para cada atributo, realizando la división del rango del atributo determinado por el rango total.
1. Una vez calculadas las importancias relativas para todos los atributos, para todos los usuarios, las almacenamos en un vector que nos servirá para luego identificar cuál es el atributo de mayor importancia en cada usuario. Lo que nos servirá luego en la consigna 4 para determinar la disposición a pagar por cambios en dicho atributo.
1. Al identificar el atributo con el valor de importancia relativa mayor, podemos ahora concatenarlo con el índice del usuario y tener para cada usuario, cuál fue el atributo más relevante. Eso es lo que vemos en la tabla subsiguiente.
1. Por último, realizamos gráficos para cada usuario. A modo de ejemplo, estas fueron las importancias relativas para los usuario 1 y 7:

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.002.jpeg)

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.003.jpeg) ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.004.jpeg)

Respecto al atributo innovador propuesto, es destacable que para los usuarios 1, 7, 10, 12 16 y 17 sea el **segundo atributo más importante**. lo cual es un indicio de aceptación muy interesante ya que representan ⅓ de los usuarios encuestados.

Pregunta 3: Part Worth Utilities del Precio

Para evaluar las implicancias de estos gráficos a la hora de tomar decisiones debemos aclarar la variable Precio solo fue lo suficientemente significativa para las encuestas #07 y #16.

Para el usuario 7, vemos que, a medida que el precio sube, la probabilidad de comprar el producto (medida en útiles), baja. Este patrón, si bien en encuestas no significativas, se repite para la mayoría de los encuestados. Sin embargo, existen ciertos casos en donde ocurre exactamente lo opuesto; yendo al caso significativo, el usuario 16 aumenta la utilidad reportada pasando del precio base (550000) al precio medio, y aún más al precio más alto. Esto y que en la mayor parte de las encuestas el precio no posee significatividad estadística, nos indica que los factores más determinantes en la elección del producto son sus características o especificaciones y no su precio.

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.005.jpeg) ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.006.jpeg)

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.007.jpeg) ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.008.jpeg)

` `![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.009.jpeg)![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.010.jpeg)

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.011.png)

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.012.jpeg) ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.013.jpeg)

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.014.jpeg) ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.015.jpeg)

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.016.jpeg) ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.017.jpeg)

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.018.jpeg) ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.019.jpeg)

Pregunta 4: Willingness-To-Pay

Para determinar la disposición a pagar, lo que hicimos fue seguir los siguientes pasos:

Disponiendo del dato de qué atributo es más importante, identificado en la pregunta 2, podemos proceder a, nuevamente iterando por cada usuario:

1. En un condicional if/else, determinar si el atributo de mayor importancia para el usuario i, es el correspondiente,
1. Se procede a calcular la diferencia en utilidades entre el nivel “más alto” y el nivel “más bajo” (disposición en utiles de pasar del nivel más alto al mas bajo
   1. viceversa), excepto en el caso de marca en el que simplemente es el cambio de una marca hacia otra ya que esta característica no es ordinal.
1. Se calcula la diferencia en utilidades para el atributo precio
1. Por último, la diferencia de precio en dinero (ARS) entre el precio más alto y el más bajo. En este caso es ARS 700000.
1. Con todos estos datos, procedemos a calcular la disposición a pagar (WTP) medida en unidades monetarias, de la siguiente manera:

=  . ( )  \* ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.020.png)

` `( )  

Básicamente es una regla de tres simple, que nos permite traducir la utilidad que nos reporta pasar de un nivel base a un nivel más alto de nuestro atributo de mayor importancia a un valor monetario tangible.

Como se observa en la tabla a continuación, los valores del WTP son notablemente elevados, lo que refleja dos aspectos clave previamente mencionados: 1) el precio no es un atributo estadísticamente significativo y 2) no resulta relevante para ninguno de los usuarios en términos de preferencia. Esta falta de relevancia implica que la diferencia en los coeficientes del precio, el cual actúa como denominador en la fórmula utilizada para calcular el WTP, tiende a ser muy cercana a cero. Como consecuencia, al dividir la diferencia monetaria por esta diferencia tan chica, los valores de WTP se incrementan de manera desproporcionada.

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.021.jpeg)

Pregunta 5: Segmentación

Para segmentar mejor a los usuarios, además de las preguntas clásicas sobre edad, género, provincia y ciudad de residencia, se incluyó una pregunta en el formulario sobre los usos que le dan al Smart TV. Los usos identificados fueron cinco:

1. Ver películas o series en servicios de streaming.
1. Ver programas de TV en vivo (noticias, deportes, espectáculos).
1. Jugar videojuegos.
1. Navegar o usar redes sociales.
1. Usar plataformas como YouTube o Spotify.

La consigna para los encuestados fue puntuar estos usos del Smart TV según el tiempo que dedican a cada uno, utilizando una escala del 1 al 5 (donde 5 indica el uso al que más tiempo dedican y 1 el que menos). Los participantes debían asignar un puntaje único a cada uso, sin repetir calificaciones.

A continuación, se presenta un gráfico que muestra los resultados obtenidos, lo cual nos permitirá segmentar el mercado en cuatro grupos diferentes. Cabe destacar que hemos decidido agrupar a los usuarios que prefieren usar el Smart TV para redes sociales junto con aquellos que priorizan el uso de plataformas como YouTube o Spotify, dado que ambos usos están relacionados con el consumo de contenido en línea.

![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.022.jpeg)

Para segmentar mejor a los usuarios, aplicamos un filtro a cada grupo, seleccionando aquellos que puntuaron con 5 puntos el uso específico que define cada segmento. Esto nos permitirá identificar patrones adicionales en función de variables demográficas como la edad, el género, la ciudad y la provincia de residencia.

Además de la cantidad de usuarios en cada grupo , que nos sirve para tener una idea clara del tamaño y las características de cada segmento, podemos identificar para cada usuario, en cada grupo cuál es el atributo más relevante. Lo que nos aporta valiosa información a la hora de ofrecerles un producto puntual.

Este análisis detallado nos proporcionará información valiosa para desarrollar estrategias y ofertas personalizadas para cada segmento de usuarios, asegurando que las soluciones propuestas respondan a sus preferencias y patrones de uso. Con esta información, podemos diseñar alternativas que realmente se adapten a las necesidades y expectativas de cada grupo, aumentando la relevancia y efectividad de nuestras propuestas para los diferentes perfiles de usuarios.

Podemos identificar entonces 4 segmentos:

1. *Cinéfilos Digitales*: Usuarios que utilizan principalmente el Smart TV para ver películas o series en servicios de streaming. N° de usuarios: 5. Atributos estrella: Marca y resolución.

   ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.023.png)

- Producto recomendado (n° 17): Una TV con excelente resolución, de marca prestigiosa como LG y con precio elevado, si, pero en general no es un problema para este grupo de usuarios. Además el emisor custom les permitirá llevar su experiencia multisensorial a otro nivel mientras disfrutan de sus películas o series favoritas.

  ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.024.png)

2. Televidentes Clásicos: Aquellos que prefieren ver programas de TV en vivo, como noticias, deportes o espectáculos. N° usuarios: 3. Atributos estrella: Tamaño y marca.

   ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.025.png)

- Producto recomendado (n° 14): Una TV grande para ver sus shows favoritos y deportes a gran escala, no requieren una excelente resolución pero si buscan calidad en cuanto a la marca. El emisor específico concentra un buen balance para este grupo de usuarios.

  ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.026.png)

3. Gamers: Usuarios que dedican la mayor parte de su tiempo a jugar videojuegos en el Smart TV. N° Usuarios: 2. Atributos estrella: Tamaño y resolución

   ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.027.png)

- Producto recomendado (n° 18): Aprovechando que el usuario 10 tiene al emisor aromático como 2° mejor atributo, le ofrecemos una TV con la mayor resolución y el emisor premium para disfrutar de sus videojuegos de manera mucho más realista.

  ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.028.png)

4. Conectados: Este segmento combina a los usuarios que usan el Smart TV para navegar en redes sociales y aquellos que utilizan plataformas como YouTube o Spotify, enfocándose en el consumo de contenido online y la interacción en redes. Atributos estrella: Resolución, Tamaño y Marca. N° usuarios: 8.
- Producto recomendado(n° 10): No requieren una pantalla enorme para el uso que le dan, pero si buscan una buena resolución para ver sus canales favoritos de Youtube, lo cual es el combo perfecto para contar con un emisor personalizado de aromas.

  ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.029.png)

  ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.030.png)

  ![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.031.png)

Pregunta 6: Nuevos productos

Tenemos estos dos nuevos productos, distintos a los mostrados en las encuestas:



|Tamaño (pulgadas)|Resolucion|Marca|Emisor aromático|Precio|
| :- | - | - | - | - |
|55|8k|Samsung|Naturales|950000|
|65|4K|LG|Premium\_Custom|1250000|

Lo primero que hicimos fue identificar, en la lista de coeficientes de cada regresión de cada usuario, cuáles eran los índices correspondientes a las utilidades parciales tanto del primer producto nuevo, como del segundo producto nuevo propuesto.

Una vez identificados, procedimos a calcular, **iterando por los 18 usuarios**, la suma de las utilidades del producto 1, a partir de sumar los coeficientes de: Tamaño\_55 + Resolucion\_8K + Marca\_Samsung + Emisor Naturales (0, porque es el nivel base) + Precio\_950000.

Lo mismo para el producto 2, sumamos los coeficientes de: Tamaño\_65 + Resolucion\_4K + Marca\_LG + Emisor\_Premium\_custom + Precio\_1250000.

Finalmente comparamos las sumas de las utilidades:

- print(suma\_utilidades\_1 <- sum(resultados\_producto\_1$`Suma Utilidades Producto 1`))
  - 40.6733
- print(suma\_utilidades\_2 <- sum(resultados\_producto\_2$`Suma Utilidades Producto 2`))

  [1] 47.76774

  Por lo que podemos afirmar, que el producto 2, se llevaría la mayor parte del market share en caso de que solo esos 2 productos existan en el mercado.
11![](Aspose.Words.38947e60-a98b-4a97-a296-f7ba53eab11b.032.jpeg)
