# Proyecto: Análisis Conjoint para Smart TVs

Este proyecto forma parte de un análisis realizado en el marco de la asignatura "Ventas & Marketing" del programa Master in Management & Analytics en la Universidad Torcuato Di Tella. El objetivo es evaluar las preferencias de los consumidores hacia Smart TVs, incluyendo atributos tradicionales e innovadores, como un difusor aromático dinámico.

## Objetivo del Proyecto

El objetivo principal es identificar las preferencias de los consumidores y su disposición a pagar por distintas características de un Smart TV. Entre los atributos analizados se encuentra un difusor aromático innovador, diseñado para ofrecer una experiencia inmersiva sincronizada con el contenido audiovisual.

## Atributos y Niveles

Los atributos seleccionados y sus niveles son los siguientes:

1. **Tamaño**: 42” (base), 55”, 65”, 72”.
2. **Resolución**: 1080p (base), 4K, 8K.
3. **Marca**: Noblex (base), Samsung, LG, Phillips.
4. **Precio**: $550,000 (base), $950,000, $1,250,000.
5. **Difusor Aromático**:
   - **Naturales**: Aromas simples como bosque, playa, o flores.
   - **Específicos**: Aromas más detallados como comida o chimenea.
   - **Personalizados (Premium)**: Aromas configurables en intensidad y frecuencia.

## Metodología

### Diseño del Estudio
- **Encuestas**: Diseñadas con el paquete `Conjoint` de R, generando 18 combinaciones de atributos.
- **Público**: 18 participantes con diversidad en edad, género y ubicación geográfica.
- **Recolección de Datos**: Las encuestas se realizaron mediante Google Forms.

### Análisis de Datos
1. **Regresiones Lineales**: 
   - Se generaron variables dummy para las combinaciones de atributos.
   - Se realizaron modelos de regresión por cada usuario para estimar las utilidades parciales de cada atributo.

2. **Importancia Relativa de Atributos**:
   - Se calculó el rango de variabilidad de cada atributo y su importancia relativa.
   - Se identificó el atributo más relevante para cada usuario.

3. **Disposición a Pagar (WTP)**:
   - Fórmula utilizada:
     \[
     WTP = \frac{\text{Dif. utilidades del mejor atributo}}{\text{Dif. utilidades del precio}} \times \text{Dif. monetaria en ARS}
     \]
   - Los resultados indicaron una baja significancia del precio como atributo relevante.

4. **Segmentación del Mercado**:
   - Basada en el uso del Smart TV:
     1. **Cinéfilos Digitales**: Prioridad en resolución y marca.
     2. **Televidentes Clásicos**: Tamaño y marca.
     3. **Gamers**: Resolución y tamaño.
     4. **Conectados**: Resolución, tamaño y marca.

5. **Nuevos Productos**:
   - Se evaluaron dos nuevos productos para estimar su market share basado en las utilidades calculadas.

## Resultados Principales

- El atributo innovador del difusor aromático fue el segundo más relevante para un tercio de los usuarios.
- Los segmentos de mercado identificados permiten diseñar estrategias personalizadas basadas en los atributos más valorados.
- El **producto 2** (65", 4K, LG, Difusor Premium) obtuvo la mayor utilidad global, sugiriendo un mayor market share en comparación con el producto 1.

## Conclusión

Este análisis muestra cómo las técnicas de Conjoint Analysis pueden ser utilizadas para entender las preferencias de los consumidores y desarrollar productos adaptados a sus necesidades. La inclusión de un atributo innovador como el difusor aromático destaca el potencial de ofrecer experiencias inmersivas en el hogar.

## Tecnologías Utilizadas

- R (paquete `Conjoint`)
- Google Forms
- Python (análisis complementario)

---

Este proyecto demuestra cómo una metodología robusta puede generar insights valiosos para la toma de decisiones estratégicas en marketing y diseño de producto.
