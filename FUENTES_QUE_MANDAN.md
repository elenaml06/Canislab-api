# Qué fuente manda, y por qué, estando en España

**11 de septiembre de 2026.** Pregunta de Elena: «¿puedes buscar en algún sitio
la fiabilidad de las fuentes y cuál debemos tener en cuenta estando en España
para construir un motor nutricional?»

La respuesta corta: **la jerarquía que ya aplica el repo es la correcta**, pero
el motivo estaba escrito a medias. Aquí queda entero, y con una distinción que
importa mucho y que no estaba dicha.

---

## La distinción que lo cambia todo: nosotros NO fabricamos pienso

Casi toda la normativa europea de alimentación animal regula **poner un producto
en el mercado**: qué puede decir una etiqueta, qué aditivos se autorizan, qué
puede llamarse «completo». Rawku **no fabrica ni vende alimento**: calcula una
ración que una persona prepara en su casa con comida que compra en el
supermercado.

Eso significa que **la ley de piensos no nos obliga**, y hay que decirlo sin
rodeos. Pero tampoco nos deja libres: esas normas son **la mejor referencia
disponible de qué se considera nutricionalmente completo en Europa**, y si el
motor se apartara de ellas tendría que justificar por qué.

---

## La jerarquía, de más vinculante a menos

| Nivel | Fuente | Qué es | Qué hace el motor |
|---|---|---|---|
| **1. LEY** | **Reglamento (UE) 2020/354** | Los objetivos nutricionales particulares (renal, urinario, hepático…) y sus límites. Es **derecho de la UE, directamente aplicable en España** | Lo aplica como techo del que no se sale nadie. Está en el repo y lo audita `auditar_margen_profesional.py` |
| **1. LEY** | **Reglamento (CE) 767/2009** | Comercialización y etiquetado de piensos. **No nos obliga** (no vendemos alimento), pero es el marco que sostiene lo demás | No se aplica. Declarado aquí para que se sepa por qué |
| **2. ESTÁNDAR EUROPEO** | **FEDIAF, *Nutritional Guidelines*** | La referencia nutricional de la industria europea. **No es ley**: es autorregulación, y el propio 767/2009 la contempla al invitar al sector a interpretar la norma | **Es la que manda en el motor.** Sus 43 filas son los requisitos que se verifican |
| **3. BASE CIENTÍFICA** | **NRC 2006** | El trabajo del que FEDIAF y AAFCO derivan sus perfiles. Da MR, AI, RA y SUL | Se lee y se cita. No sustituye a FEDIAF |
| **3. ESTÁNDAR NO EUROPEO** | **AAFCO** | El equivalente estadounidense | **No se aplica.** Se cita para explicar de dónde vienen cifras de libros americanos |
| **4. CLÍNICA** | **SACN5, Ettinger, Fascetti** | Libros de texto de nutrición y medicina interna | De aquí salen los límites por patología, que **aprietan dentro** de FEDIAF |
| **5. PROFESIÓN** | **ECVCN / ESVCN**, **WSAVA** | El colegio europeo de especialistas en nutrición y el comité global. No publican tablas de requerimientos | Se citan para el BCS, la valoración nutricional y quién firma una pauta |

---

## Por qué FEDIAF y no AAFCO, estando en España

Tres motivos, y ninguno es de gusto:

1. **Es la referencia europea.** FEDIAF es la federación de la industria europea
   de alimentos para animales de compañía, y sus guías son el estándar que sigue
   el producto que se vende aquí.
2. **El Reglamento 767/2009 prevé esa autorregulación.** La Comisión invita a los
   sectores a interpretar la legislación y dar guía práctica, y las guías de
   FEDIAF son exactamente ese documento para el pienso de compañía.
3. **AAFCO no tiene ninguna fuerza en España.** Citarla está bien para entender
   de dónde sale una cifra de un libro americano — la mayoría de los que usamos
   lo son — pero aplicarla sería tomar el estándar de otro mercado.

---

## ⚠️ Y lo que esta jerarquía NO resuelve

Aquí está el hueco de verdad, y conviene tenerlo escrito:

**Ninguna de estas fuentes regula la ración casera cruda.** FEDIAF escribe para
pienso completo; el Reglamento 2020/354 para alimentos dietéticos comerciales;
NRC para requerimientos de nutrientes, no para recetas. **Lo que hacemos nosotras
no está cubierto por ninguna norma**, y por eso el motor se autoexige cumplir la
más estricta que le aplica en espíritu.

De ahí sale la regla del repo, **y su matiz nuevo del 11 de septiembre**:

> Si otra fuente contradice a FEDIAF, **gana FEDIAF**.
>
> **Salvo** cuando esa fuente habla específicamente de lo que nosotros hacemos
> —ración casera o cruda— y FEDIAF no. Entonces se puede aplicar la otra,
> **siempre** apuntando las dos cifras y llevándolo al documento del
> nutricionista para que lo juzgue. Decisión de Elena.

**Y quien decide de verdad es el nutricionista veterinario**, no el software y no
nosotras. Es lo que ya dice `PARA_EL_NUTRICIONISTA.md` en su §0: el motor no puede
tomar decisiones clínicas que nadie ha firmado.

---

## De dónde sale esto

- Comisión Europea, *Feed marketing* — el marco del Reglamento (CE) 767/2009 y la
  autorregulación sectorial: https://food.ec.europa.eu/food-safety/animal-feed/feed-marketing_en
- FEDIAF, *Nutritional Guidelines* (edición 2024): https://europeanpetfood.org/wp-content/uploads/2024/09/FEDIAF-Nutritional-Guidelines_2024.pdf
- ECVCN, el colegio europeo de especialistas, reconocido por el EBVS desde 2009:
  https://www.ecvcn.org/homepage-ecvcn
- WSAVA, *Global Nutrition Guidelines*: https://wsava.org/global-guidelines/global-nutrition-guidelines/
- El Reglamento (UE) 2020/354 está en el repo de fuentes, en inglés y en
  castellano, con su lectura.

⚠️ **Consultado el 11 de septiembre de 2026 y puede caducar.** FEDIAF revisa sus
guías cada pocos años: el motor trabaja hoy contra la edición **2025**, y conviene
comprobar que sigue siendo la vigente antes de una revisión.
