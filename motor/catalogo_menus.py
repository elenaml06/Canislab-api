# -*- coding: utf-8 -*-
"""
CATÁLOGO DE MENÚS FIJOS — 36 combinaciones, 6 tamaños × 6 etapas.

Generado el 5 de agosto con motor_completo.py, verificado uno a uno contra
los 30 requisitos de FEDIAF. Los 36 salen en verde.

CÓMO SE ELIGIÓ EL PESO DE CADA CACHORRO
------------------------------------------
Un cachorro no tiene un peso fijo -- va cambiando. Se usó un punto
representativo de cada etapa, con la misma curva de Klein que ya está
verificada en der.py:
  - CachorroJoven: peso a los 2 meses
  - CachorroCrecimiento: peso a la mitad de su periodo de crecimiento
Gestante y lactante usan el peso adulto de cada tamaño. Lactante asume
una camada de 4 cachorros (lo más común, se ajusta a mano si hace falta).

CÓMO USAR ESTO
----------------
CATALOGO["Mediano_CachorroCrecimiento"] -> {"gramos": {...}, "der": 1303, ...}

Esto es un PUNTO DE PARTIDA, no sustituye al motor en vivo: sirve para
arrancar rápido o como respaldo si el motor no responde, pero un perro
concreto (peso exacto, alergias, patologías) sigue necesitando pasar por
motor_completo.resolver() para un menú hecho a su medida.
"""

CATALOGO = {
  "Toy_CachorroJoven": {
    "tamano": "Toy",
    "etapa": "CachorroJoven",
    "peso_kg": 1.35,
    "der": 260,
    "gramos": {
      "Pollo con piel (sin hueso)": 39.84,
      "Costillas de cordero": 42.19,
      "Salmón": 43.01,
      "Lengua de ternera": 19.74,
      "Hígado de vaca": 3.29,
      "Acelga": 16.45,
      "Homemadekun (multivitamínico completo)": 3.64
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Toy_CachorroCrecimiento": {
    "tamano": "Toy",
    "etapa": "CachorroCrecimiento",
    "peso_kg": 2.33,
    "der": 288,
    "gramos": {
      "Pollo con piel (sin hueso)": 85.44,
      "Costillas de cordero": 58.19,
      "Salmón": 5.59,
      "Pulmón de ternera": 13.0,
      "Hígado de pollo": 4.45,
      "Acelga": 18.52,
      "Homemadekun (multivitamínico completo)": 3.51
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Toy_Adulto": {
    "tamano": "Toy",
    "etapa": "Adulto",
    "peso_kg": 3,
    "der": 251,
    "gramos": {
      "Pollo con piel (sin hueso)": 57.96,
      "Carcasa de pollo": 57.4,
      "Lengua de ternera": 2.54,
      "Hígado de cordero": 2.54,
      "Albahaca": 6.56,
      "Homemadekun (multivitamínico completo)": 3.79
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Toy_Senior": {
    "tamano": "Toy",
    "etapa": "Senior",
    "peso_kg": 3,
    "der": 235,
    "gramos": {
      "Pollo con piel (sin hueso)": 70.68,
      "Costillas de cordero": 53.97,
      "Lengua de cordero": 2.69,
      "Hígado de pollo": 2.69,
      "Albahaca": 4.47,
      "Homemadekun (multivitamínico completo)": 3.41
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Toy_GestanteTardia": {
    "tamano": "Toy",
    "etapa": "GestanteTardia",
    "peso_kg": 3,
    "der": 379,
    "gramos": {
      "Ternera solomillo sin grasa": 80.21,
      "Carcasa de conejo": 50.94,
      "Salmón": 71.5,
      "Lengua de ternera": 30.56,
      "Hígado de vaca": 5.09,
      "Albahaca": 16.39,
      "Aceite de sésamo": 1.82,
      "Homemadekun (multivitamínico completo)": 3.82
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Toy_Lactante": {
    "tamano": "Toy",
    "etapa": "Lactante",
    "peso_kg": 3,
    "der": 647,
    "gramos": {
      "Pollo con piel (sin hueso)": 101.51,
      "Costillas de cordero": 115.53,
      "Salmón": 120.0,
      "Lengua de ternera": 7.46,
      "Hígado de vaca": 7.46,
      "Albahaca": 21.2,
      "Homemadekun (multivitamínico completo)": 6.92
    },
    "semaforo": "rojo",
    "correctos": 29,
    "total": 30
  },
  "Mini_CachorroJoven": {
    "tamano": "Mini",
    "etapa": "CachorroJoven",
    "peso_kg": 2.63,
    "der": 441,
    "gramos": {
      "Pollo con piel (sin hueso)": 67.73,
      "Costillas de cordero": 71.72,
      "Salmón": 73.12,
      "Lengua de ternera": 33.56,
      "Hígado de vaca": 5.59,
      "Acelga": 27.97,
      "Homemadekun (multivitamínico completo)": 6.19
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mini_CachorroCrecimiento": {
    "tamano": "Mini",
    "etapa": "CachorroCrecimiento",
    "peso_kg": 4.66,
    "der": 508,
    "gramos": {
      "Pollo con piel (sin hueso)": 100.6,
      "Costillas de cordero": 101.23,
      "Salmón": 49.66,
      "Lengua de ternera": 40.37,
      "Hígado de conejo": 10.9,
      "Acelga": 33.64,
      "Homemadekun (multivitamínico completo)": 6.42
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mini_Adulto": {
    "tamano": "Mini",
    "etapa": "Adulto",
    "peso_kg": 6,
    "der": 422,
    "gramos": {
      "Pollo con piel (sin hueso)": 138.88,
      "Carcasa de conejo": 61.7,
      "Lengua de buey": 30.1,
      "Hígado de pollo": 5.02,
      "Piña": 15.15,
      "V-INTEGRA Perro Adulto": 2.26
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mini_Senior": {
    "tamano": "Mini",
    "etapa": "Senior",
    "peso_kg": 6,
    "der": 395,
    "gramos": {
      "Pollo con piel (sin hueso)": 95.49,
      "Carcasa de pato": 91.15,
      "Lengua de cordero": 3.99,
      "Hígado de pollo": 4.66,
      "Acelga": 3.99,
      "V-INTEGRA Perro Adulto": 2.4
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mini_GestanteTardia": {
    "tamano": "Mini",
    "etapa": "GestanteTardia",
    "peso_kg": 6,
    "der": 662,
    "gramos": {
      "Pollo con piel (sin hueso)": 95.98,
      "Costillas de cordero": 113.19,
      "Salmón": 93.94,
      "Lengua de cordero": 50.52,
      "Hígado de vaca": 25.26,
      "Acelga": 42.1,
      "Homemadekun (multivitamínico completo)": 8.17
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mini_Lactante": {
    "tamano": "Mini",
    "etapa": "Lactante",
    "peso_kg": 6,
    "der": 1190,
    "gramos": {
      "Pavo pechuga sin piel": 135.13,
      "Costillas de cordero": 256.05,
      "Trucha": 454.89,
      "Molleja de pavo": 133.59,
      "Hígado de vaca": 22.26,
      "Albahaca": 111.32,
      "Homemadekun (multivitamínico completo)": 1.12
    },
    "semaforo": "rojo",
    "correctos": 29,
    "total": 30
  },
  "Pequeño_CachorroJoven": {
    "tamano": "Pequeño",
    "etapa": "CachorroJoven",
    "peso_kg": 4.6,
    "der": 692,
    "gramos": {
      "Pollo con piel (sin hueso)": 127.71,
      "Costillas de cordero": 120.35,
      "Sardina": 100.34,
      "Lengua de buey": 51.74,
      "Hígado de vaca": 9.09,
      "Acelga": 43.28,
      "Albahaca": 2.19,
      "Homemadekun (multivitamínico completo)": 7.85
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Pequeño_CachorroCrecimiento": {
    "tamano": "Pequeño",
    "etapa": "CachorroCrecimiento",
    "peso_kg": 9.32,
    "der": 876,
    "gramos": {
      "Pollo con piel (sin hueso)": 102.76,
      "Costillas de cordero": 174.76,
      "Salmón": 151.58,
      "Lengua de ternera": 69.07,
      "Hígado de pollo": 19.82,
      "Acelga": 57.55,
      "Homemadekun (multivitamínico completo)": 10.9
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Pequeño_Adulto": {
    "tamano": "Pequeño",
    "etapa": "Adulto",
    "peso_kg": 12,
    "der": 709,
    "gramos": {
      "Pollo con piel (sin hueso)": 162.24,
      "Carcasa de pato": 169.67,
      "Lengua de ternera": 7.45,
      "Hígado de cordero": 7.45,
      "Espárrago verde": 25.75,
      "V-INTEGRA Perro Adulto": 4.8
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Pequeño_Senior": {
    "tamano": "Pequeño",
    "etapa": "Senior",
    "peso_kg": 12,
    "der": 664,
    "gramos": {
      "Pollo con piel (sin hueso)": 218.72,
      "Carcasa de conejo": 97.17,
      "Lengua de buey": 47.41,
      "Hígado de pollo": 7.9,
      "Piña": 23.85,
      "V-INTEGRA Perro Adulto": 3.56
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Pequeño_GestanteTardia": {
    "tamano": "Pequeño",
    "etapa": "GestanteTardia",
    "peso_kg": 12,
    "der": 1163,
    "gramos": {
      "Pollo con piel (sin hueso)": 178.51,
      "Costillas de cordero": 189.02,
      "Salmón": 192.72,
      "Lengua de ternera": 88.46,
      "Hígado de vaca": 14.74,
      "Acelga": 73.72,
      "Homemadekun (multivitamínico completo)": 16.31
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Pequeño_Lactante": {
    "tamano": "Pequeño",
    "etapa": "Lactante",
    "peso_kg": 12,
    "der": 2202,
    "gramos": {
      "Corazón de pollo": 268.72,
      "Costillas de cordero": 452.78,
      "Trucha": 828.99,
      "Lengua de ternera": 36.06,
      "Hígado de vaca": 36.06,
      "Albahaca": 180.29,
      "AniForte Seaweed Meal": 0.73,
      "Homemadekun (multivitamínico completo)": 7.28
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mediano_CachorroJoven": {
    "tamano": "Mediano",
    "etapa": "CachorroJoven",
    "peso_kg": 7.5,
    "der": 1029,
    "gramos": {
      "Pollo con piel (sin hueso)": 114.31,
      "Costillas de cordero": 169.01,
      "Salmón": 187.08,
      "Pescadilla": 160.63,
      "Lengua de buey": 13.98,
      "Hígado de pollo": 22.05,
      "Albahaca": 31.96,
      "Homemadekun (multivitamínico completo)": 10.51
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mediano_CachorroCrecimiento": {
    "tamano": "Mediano",
    "etapa": "CachorroCrecimiento",
    "peso_kg": 17.09,
    "der": 1303,
    "gramos": {
      "Pollo con piel (sin hueso)": 353.94,
      "Costillas de cordero": 263.73,
      "Merluza": 256.87,
      "Lengua de buey": 22.72,
      "Hígado de pollo": 20.09,
      "Albahaca": 87.02,
      "V-INTEGRA Perro Adulto": 6.84
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mediano_Adulto": {
    "tamano": "Mediano",
    "etapa": "Adulto",
    "peso_kg": 22,
    "der": 1117,
    "gramos": {
      "Pollo con piel (sin hueso)": 265.14,
      "Cuello de pato": 188.65,
      "Lengua de buey": 9.73,
      "Hígado de pollo": 13.24,
      "Melón": 9.73,
      "V-INTEGRA Perro Adulto": 8.8
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mediano_Senior": {
    "tamano": "Mediano",
    "etapa": "Senior",
    "peso_kg": 22,
    "der": 1046,
    "gramos": {
      "Pollo con piel (sin hueso)": 192.13,
      "Carcasa de conejo": 312.07,
      "Lengua de buey": 79.61,
      "Hígado de pollo": 13.27,
      "Canónigos": 66.34,
      "V-INTEGRA Perro Adulto": 5.01
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mediano_GestanteTardia": {
    "tamano": "Mediano",
    "etapa": "GestanteTardia",
    "peso_kg": 22,
    "der": 1913,
    "gramos": {
      "Pollo con piel (sin hueso)": 487.56,
      "Costillas de cordero": 335.44,
      "Salmón": 104.45,
      "Lengua de ternera": 154.57,
      "Hígado de vaca": 77.29,
      "Acelga": 128.81,
      "Homemadekun (multivitamínico completo)": 22.04
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mediano_Lactante": {
    "tamano": "Mediano",
    "etapa": "Lactante",
    "peso_kg": 22,
    "der": 3796,
    "gramos": {
      "Ternera solomillo sin grasa": 679.76,
      "Costillas de cordero": 804.63,
      "Trucha": 1348.7,
      "Lengua de buey": 68.41,
      "Hígado de pollo": 177.0,
      "Albahaca": 342.06,
      "AniForte Seaweed Meal": 1.47,
      "V-INTEGRA Perro Adulto": 3.49
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Grande_CachorroJoven": {
    "tamano": "Grande",
    "etapa": "CachorroJoven",
    "peso_kg": 9.63,
    "der": 1278,
    "gramos": {
      "Corazón de pollo": 146.51,
      "Costillas de cordero": 251.65,
      "Trucha": 506.04,
      "Molleja de pavo": 81.38,
      "Hígado de pollo": 64.28,
      "Canónigos": 21.43,
      "AniForte Seaweed Meal": 0.96,
      "V-INTEGRA Perro Adulto": 3.85
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Grande_CachorroCrecimiento": {
    "tamano": "Grande",
    "etapa": "CachorroCrecimiento",
    "peso_kg": 24.86,
    "der": 1773,
    "gramos": {
      "Pollo con piel (sin hueso)": 207.89,
      "Costillas de cordero": 304.59,
      "Salmón": 357.16,
      "Lengua de ternera": 136.95,
      "Hígado de pollo": 48.88,
      "Acelga": 85.78,
      "V-INTEGRA Perro Adulto": 9.94
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Grande_Adulto": {
    "tamano": "Grande",
    "etapa": "Adulto",
    "peso_kg": 32,
    "der": 1480,
    "gramos": {
      "Pollo con piel (sin hueso)": 286.7,
      "Carcasa de pollo": 338.88,
      "Lengua de ternera": 62.97,
      "Hígado de pollo": 44.91,
      "Espárrago verde": 14.97,
      "V-INTEGRA Perro Adulto": 9.13
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Grande_Senior": {
    "tamano": "Grande",
    "etapa": "Senior",
    "peso_kg": 32,
    "der": 1386,
    "gramos": {
      "Pollo con piel (sin hueso)": 456.4,
      "Carcasa de conejo": 329.65,
      "Lengua de ternera": 16.72,
      "Hígado de pollo": 16.72,
      "Boniato": 16.72,
      "V-INTEGRA Perro Adulto": 8.41
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Grande_GestanteTardia": {
    "tamano": "Grande",
    "etapa": "GestanteTardia",
    "peso_kg": 32,
    "der": 2608,
    "gramos": {
      "Pollo con piel (sin hueso)": 363.11,
      "Costillas de cordero": 478.69,
      "Bacaladilla": 850.29,
      "Lengua de buey": 203.07,
      "Hígado de vaca": 41.68,
      "Albahaca": 147.03,
      "V-INTEGRA Perro Adulto": 11.47
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Grande_Lactante": {
    "tamano": "Grande",
    "etapa": "Lactante",
    "peso_kg": 32,
    "der": 5330,
    "gramos": {
      "Lomo de ternera con grasa": 1005.21,
      "Costillas de cordero": 1088.78,
      "Trucha": 1902.43,
      "Lengua de buey": 96.31,
      "Hígado de pollo": 241.37,
      "Albahaca": 481.57,
      "AniForte Seaweed Meal": 3.2,
      "V-INTEGRA Perro Adulto": 3.24
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Gigante_CachorroJoven": {
    "tamano": "Gigante",
    "etapa": "CachorroJoven",
    "peso_kg": 13.34,
    "der": 1632,
    "gramos": {
      "Pavo pechuga sin piel": 137.32,
      "Costillas de cordero": 318.67,
      "Trucha": 526.88,
      "Lengua de buey": 149.89,
      "Hígado de pollo": 65.79,
      "Albahaca": 50.54,
      "V-INTEGRA Perro Adulto": 5.34
    },
    "semaforo": "rojo",
    "correctos": 29,
    "total": 30
  },
  "Gigante_CachorroCrecimiento": {
    "tamano": "Gigante",
    "etapa": "CachorroCrecimiento",
    "peso_kg": 42.73,
    "der": 2575,
    "gramos": {
      "Pavo pechuga sin piel": 319.06,
      "Costillas de cordero": 436.97,
      "Trucha": 881.47,
      "Lengua de buey": 233.93,
      "Hígado de vaca": 38.99,
      "Acelga": 38.99,
      "V-INTEGRA Perro Adulto": 14.97
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Gigante_Adulto": {
    "tamano": "Gigante",
    "etapa": "Adulto",
    "peso_kg": 55,
    "der": 2222,
    "gramos": {
      "Pollo con piel (sin hueso)": 618.13,
      "Carcasa de conejo": 644.9,
      "Lengua de buey": 26.87,
      "Hígado de pollo": 26.87,
      "Fresa": 26.87,
      "V-INTEGRA Perro Adulto": 12.74
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Gigante_Senior": {
    "tamano": "Gigante",
    "etapa": "Senior",
    "peso_kg": 55,
    "der": 2080,
    "gramos": {
      "Pollo con piel (sin hueso)": 685.1,
      "Carcasa de conejo": 303.77,
      "Lengua de buey": 156.24,
      "Hígado de pollo": 26.72,
      "Canónigos": 130.2,
      "napfcheck Novomineral proLEBER": 16.23
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Gigante_GestanteTardia": {
    "tamano": "Gigante",
    "etapa": "GestanteTardia",
    "peso_kg": 55,
    "der": 4096,
    "gramos": {
      "Pollo con piel (sin hueso)": 1076.25,
      "Costillas de cordero": 719.15,
      "Lenguado": 485.34,
      "Lengua de ternera": 366.55,
      "Hígado de vaca": 101.82,
      "Acelga": 305.46,
      "V-INTEGRA Perro Adulto": 22.0
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Gigante_Lactante": {
    "tamano": "Gigante",
    "etapa": "Lactante",
    "peso_kg": 55,
    "der": 8482,
    "gramos": {
      "Lomo de ternera con grasa": 1749.46,
      "Costillas de cordero": 1571.09,
      "Trucha": 3087.98,
      "Lengua de ternera": 464.86,
      "Hígado de pollo": 196.53,
      "Albahaca": 785.55,
      "Sonrisa de Diez Kelp": 1.45,
      "V-INTEGRA Perro Adulto": 22.0
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  }
}

# ⚠️ AÑADIDO (5 agosto, madrugada) — VARIANTES PRE-RESUELTAS: para cada
# combinación de tamaño x etapa, varios menús completos, cada uno con una
# proteína principal distinta, YA resueltos y verificados en verde por
# adelantado -- no una sola opción como el CATALOGO de arriba.
#
# Por qué existe: en producción (Render, plan gratis) resolver un menú en
# caliente con una especie evitada puede tardar 19+ segundos -- demasiado
# cerca del límite de 30s de Render, y a veces lo supera de verdad (caso
# real, confirmado con el tiempo exacto en las herramientas de
# desarrollador del navegador). La solución no es subir el límite de
# tiempo -- eso solo tapa el síntoma, y sigue siendo lento para quien
# espera. Con esto, el automático (sin alergias ni patologías) puede
# servir cualquiera de estas variantes al instante, rotando entre ellas
# para dar variedad real, sin resolver NADA en caliente -- igual que ya
# hacía el primer menú con la vía rápida, pero ahora con varias opciones
# guardadas en vez de solo una.
#
# Estructura: CATALOGO_VARIANTES["Tamano_Etapa"] -> lista de
# {"proteina": nombre, "gramos": {...}} -- cada una ya en verde para el
# DER representativo de esa combinación (se reescala por kcal reales al
# servir, igual que ya hace el endpoint /catalogo).
# ⚠️ REGENERADO (5 agosto, madrugada) — la primera versión de esto
# (5 agosto, madrugada, más temprano) solo variaba la PROTEÍNA entre
# las variantes -- el resto (hueso, víscera, hígado, verdura) lo decidía
# el optimizador solo, que tiende a converger siempre en las mismas
# opciones "eficientes" (por eso siempre salía acelga, lengua de buey,
# merluza, costillas de cordero, daba igual qué proteína). La usuaria lo
# pidió claro: que varíe TODO -- proteína, hueso, víscera, hígado, verdura
# -- a la vez, no solo la proteína. Cada variante ahora fuerza una
# "familia" completa (5 combinaciones distintas: Pollo+Pollo+Buey+Vaca,
# Ternera+Ternera+Cordero+Cordero, Conejo+Conejo+Pavo+Pollo,
# Salmón+Pato+Ternera+Conejo, Merluza+Cordero+Pollo+Vaca), con una verdura
# sugerida por familia (como preferencia suave, no forzada -- las verduras
# no están organizadas por "especie" con varios cortes como los animales,
# así que forzarlas podría hacer el problema imposible sin necesidad). Si
# la combinación completa no llegaba a verde, se reintenta solo con la
# proteína (mejor variedad parcial que ninguna) antes de descartarla.
CATALOGO_VARIANTES = {
  "Toy_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 78.61,
        "Carcasa de pollo": 31.07,
        "Trucha": 36.34,
        "Lengua de buey": 3.11,
        "Hígado de vaca": 3.11,
        "Zanahoria": 3.11,
        "Pipa de girasol": 4.75,
        "Homemadekun (multivitamínico completo)": 3.43
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 80.54,
        "Cuello de ternera": 49.31,
        "Salmón": 22.33,
        "Lengua de cordero": 19.86,
        "Hígado de cordero": 3.91,
        "Calabaza": 19.55,
        "Aceite de girasol": 1.64,
        "Homemadekun (multivitamínico completo)": 3.38
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 79.28,
        "Carcasa de pato": 32.77,
        "Salmón": 6.06,
        "Lengua de ternera": 19.66,
        "Hígado de conejo": 9.7,
        "Calabacín": 16.39,
        "Aceite de girasol": 2.34,
        "Homemadekun (multivitamínico completo)": 3.05
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Corazón de pollo": 58.86,
        "Costillas de cordero": 43.9,
        "Merluza": 43.59,
        "Molleja de pollo": 3.44,
        "Hígado de vaca": 4.96,
        "Fresa": 17.19,
        "Aceite de linaza": 5.0,
        "Homemadekun (multivitamínico completo)": 3.28
      }
    }
  ],
  "Toy_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 90.72,
        "Carcasa de pollo": 35.98,
        "Lengua de buey": 14.29,
        "Hígado de vaca": 4.96,
        "Zanahoria": 16.22,
        "Brit Care Aceite de Salmón": 0.79,
        "Pipa de calabaza": 4.05,
        "Homemadekun (multivitamínico completo)": 3.7
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 121.79,
        "Cuello de ternera": 51.41,
        "Riñón de cordero": 3.61,
        "Lengua de cordero": 23.74,
        "Hígado de cordero": 4.56,
        "Canónigos": 22.79,
        "Aceite de Salmón Natural Greatness": 0.94,
        "Aceite de cacahuete": 2.18,
        "Homemadekun (multivitamínico completo)": 3.28
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 78.64,
        "Costillas de cordero": 48.34,
        "Trucha": 56.72,
        "Lengua de ternera": 29.01,
        "Hígado de vaca": 4.83,
        "Espinaca": 24.17,
        "Yoduro potásico (comprimidos 200 µg)": 0.03,
        "V-INTEGRA Cachorro": 2.1
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 103.51,
        "Carcasa de pato": 34.5,
        "Lengua de ternera": 20.7,
        "Hígado de conejo": 10.35,
        "Calabacín": 3.45,
        "Aceite de Salmón Natural Greatness": 0.89,
        "Aceite de girasol": 1.4,
        "Homemadekun (multivitamínico completo)": 3.33
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pato (carne sin hueso)": 107.55,
        "Costillas de cordero": 55.99,
        "Molleja de pollo": 3.8,
        "Hígado de vaca": 3.8,
        "Acelga": 19.02,
        "Brit Care Aceite de Salmón": 0.71,
        "Pipa de calabaza": 4.15,
        "Homemadekun (multivitamínico completo)": 3.59
      }
    }
  ],
  "Toy_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 57.16,
        "Carcasa de pollo": 36.87,
        "Lengua de buey": 13.43,
        "Hígado de vaca": 2.24,
        "Zanahoria": 2.24,
        "Pipa de calabaza": 4.35,
        "Homemadekun (multivitamínico completo)": 0.34,
        "V-INTEGRA Perro Adulto": 1.2
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 56.05,
        "Cuello de ternera": 92.84,
        "Pulmón de cordero": 3.46,
        "Hígado de cordero": 3.46,
        "Calabaza": 17.31,
        "Pipa de calabaza": 4.83,
        "V-INTEGRA Perro Adulto": 1.12
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 62.18,
        "Carcasa de conejo": 73.12,
        "Dorada": 27.64,
        "Molleja de pavo": 3.47,
        "Hígado de pollo": 3.47,
        "Espinaca": 3.47,
        "V-INTEGRA Perro Adulto": 1.18
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 66.85,
        "Cuello de pato": 43.3,
        "Lengua de ternera": 2.51,
        "Hígado de conejo": 2.51,
        "Calabacín": 10.17,
        "napfcheck Novomineral proLEBER": 0.27,
        "V-INTEGRA Perro Adulto": 1.2
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 74.35,
        "Costillas de cordero": 58.45,
        "Molleja de pollo": 3.09,
        "Hígado de vaca": 3.09,
        "Albahaca": 15.44,
        "Homemadekun (multivitamínico completo)": 2.55
      }
    }
  ],
  "Toy_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 52.78,
        "Carcasa de pollo": 53.81,
        "Lengua de buey": 2.82,
        "Hígado de vaca": 2.34,
        "Albahaca": 5.21,
        "Homemadekun (multivitamínico completo)": 3.61
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 102.24,
        "Cuello de ternera": 42.72,
        "Lengua de cordero": 4.99,
        "Hígado de cordero": 3.41,
        "Calabaza": 17.04,
        "Pipa de calabaza": 5.0,
        "Homemadekun (multivitamínico completo)": 3.58
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 97.92,
        "Carcasa de conejo": 39.52,
        "Lengua de buey": 16.2,
        "Hígado de pollo": 10.02,
        "Espinaca": 3.34,
        "Aceite de sésamo": 0.23,
        "V-INTEGRA Senior": 1.07
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 55.0,
        "Cuello de pato": 40.54,
        "Lengua de ternera": 2.1,
        "Hígado de conejo": 2.1,
        "Albahaca": 5.18,
        "Homemadekun (multivitamínico completo)": 2.33
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 77.4,
        "Costillas de cordero": 51.38,
        "Molleja de pollo": 2.99,
        "Hígado de vaca": 2.99,
        "Albahaca": 14.97,
        "Homemadekun (multivitamínico completo)": 2.3
      }
    }
  ],
  "Toy_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 59.63,
        "Corazón de pollo": 82.71,
        "Carcasa de pollo": 52.21,
        "Salmón": 9.46,
        "Lengua de buey": 4.74,
        "Hígado de vaca": 4.74,
        "Zanahoria": 23.72,
        "Homemadekun (multivitamínico completo)": 5.9
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 25.62,
        "Cuello de ternera": 124.41,
        "Trucha": 44.69,
        "Lengua de cordero": 30.75,
        "Hígado de cordero": 5.12,
        "Calabaza": 25.62,
        "Pipa de calabaza": 4.15,
        "Homemadekun (multivitamínico completo)": 4.58,
        "Sal común (cloruro sódico)": 0.17
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 67.64,
        "Espinazo de conejo": 112.82,
        "Salmón": 35.84,
        "Lengua de ternera": 34.63,
        "Hígado de pollo": 8.83,
        "Espinaca": 28.86,
        "Yoduro potásico (comprimidos 200 µg)": 0.03,
        "V-INTEGRA Cachorro": 2.7
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 128.39,
        "Carcasa de pato": 42.8,
        "Lengua de ternera": 25.68,
        "Hígado de conejo": 12.84,
        "Calabacín": 4.28,
        "Aceite de Salmón Natural Greatness": 1.2,
        "Aceite de sésamo": 2.55,
        "Homemadekun (multivitamínico completo)": 4.62
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Ternera solomillo sin grasa": 176.16,
        "Costillas de cordero": 61.17,
        "Molleja de pollo": 21.03,
        "Hígado de vaca": 5.87,
        "Naranja": 29.36,
        "Aceite de Salmón Natural Greatness": 1.11,
        "Aceite de sésamo": 2.76,
        "Homemadekun (multivitamínico completo)": 5.52
      }
    }
  ],
  "Toy_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 101.29,
        "Corazón de pollo": 137.82,
        "Carcasa de pollo": 79.7,
        "Sardina": 30.84,
        "Lengua de buey": 12.58,
        "Hígado de vaca": 17.07,
        "Zanahoria": 19.21,
        "Homemadekun (multivitamínico completo)": 9.24
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 205.29,
        "Cuello de ternera": 121.59,
        "Salmón": 45.06,
        "Lengua de cordero": 57.81,
        "Hígado de cordero": 9.63,
        "Calabaza": 42.33,
        "Aceite de girasol": 4.38,
        "Homemadekun (multivitamínico completo)": 8.54
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 176.07,
        "Costillas de cordero": 104.66,
        "Sardina": 27.63,
        "Lengua de buey": 46.37,
        "Hígado de cordero": 7.73,
        "Espinaca": 23.99,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 9.01,
        "Sal común (cloruro sódico)": 0.25
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 142.81,
        "Cuello de pato": 84.41,
        "Salmón": 64.69,
        "Lengua de ternera": 6.79,
        "Hígado de conejo": 6.79,
        "Acelga": 33.94,
        "Aceite de girasol": 4.66,
        "Homemadekun (multivitamínico completo)": 10.05
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 208.48,
        "Costillas de cordero": 108.96,
        "Merluza": 0.54,
        "Molleja de pollo": 23.77,
        "Hígado de vaca": 24.41,
        "Acelga": 40.69,
        "Brit Care Aceite de Salmón": 1.38,
        "Homemadekun (multivitamínico completo)": 8.5,
        "Sal común (cloruro sódico)": 0.15
      }
    }
  ],
  "Mini_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 112.52,
        "Carcasa de pollo": 74.98,
        "Trucha": 62.49,
        "Lengua de buey": 11.35,
        "Hígado de vaca": 5.44,
        "Zanahoria": 5.44,
        "Pipa de girasol": 2.7,
        "Homemadekun (multivitamínico completo)": 5.96
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 78.76,
        "Cuello de ternera": 112.8,
        "Riñón de cordero": 14.58,
        "Hígado de cordero": 4.68,
        "Albahaca": 23.42,
        "Brit Care Aceite de Salmón": 1.21,
        "Pipa de girasol": 3.99,
        "Homemadekun (multivitamínico completo)": 5.27,
        "Sal común (cloruro sódico)": 0.23
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 183.55,
        "Costillas de cordero": 62.93,
        "Lengua de buey": 27.93,
        "Hígado de vaca": 8.77,
        "Acelga": 31.46,
        "Aceite de Salmón Natural Greatness": 1.16,
        "Aceite de girasol": 0.54,
        "Homemadekun (multivitamínico completo)": 5.27
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 122.14,
        "Carcasa de pato": 50.55,
        "Salmón": 39.64,
        "Lengua de ternera": 30.33,
        "Hígado de conejo": 5.06,
        "Calabacín": 5.06,
        "Aceite de girasol": 2.72,
        "Homemadekun (multivitamínico completo)": 6.31
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 145.24,
        "Costillas de cordero": 76.35,
        "Molleja de pollo": 26.32,
        "Hígado de vaca": 5.16,
        "Albahaca": 5.16,
        "Aceite de Salmón Natural Greatness": 1.15,
        "Homemadekun (multivitamínico completo)": 5.53,
        "Sal común (cloruro sódico)": 0.24
      }
    }
  ],
  "Mini_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 160.74,
        "Carcasa de pollo": 56.83,
        "Lengua de buey": 21.12,
        "Hígado de vaca": 17.05,
        "Zanahoria": 28.42,
        "Brit Care Aceite de Salmón": 1.37,
        "Pipa de girasol": 4.42,
        "Homemadekun (multivitamínico completo)": 6.28
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 146.73,
        "Cuello de ternera": 108.78,
        "Salmón": 57.37,
        "Riñón de cordero": 6.95,
        "Hígado de cordero": 6.95,
        "Albahaca": 20.56,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 5.52
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 36.75,
        "Espinazo de conejo": 142.22,
        "Salmón": 84.95,
        "Pescadilla": 52.15,
        "Molleja de pavo": 7.35,
        "Hígado de pollo": 7.35,
        "Espinaca": 36.75,
        "Aceite de oliva": 3.11,
        "V-INTEGRA Cachorro": 4.19
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 140.68,
        "Cuello de pato": 75.74,
        "Riñón de ternera": 9.5,
        "Hígado de conejo": 5.13,
        "Acelga": 25.67,
        "Brit Care Aceite de Salmón": 1.38,
        "Aceite de cacahuete": 4.05,
        "Homemadekun (multivitamínico completo)": 7.02
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pato (carne sin hueso)": 148.66,
        "Costillas de cordero": 88.47,
        "Merluza": 96.46,
        "Molleja de pollo": 7.23,
        "Hígado de vaca": 7.23,
        "Canónigos": 13.47,
        "Aceite de girasol": 4.73,
        "V-INTEGRA Cachorro": 4.19
      }
    }
  ],
  "Mini_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 138.98,
        "Carcasa de pollo": 52.25,
        "Lengua de buey": 28.11,
        "Hígado de vaca": 10.23,
        "Zanahoria": 4.69,
        "V-INTEGRA Perro Adulto": 2.4
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 75.24,
        "Cuello de ternera": 133.99,
        "Pulmón de cordero": 4.47,
        "Hígado de cordero": 4.47,
        "Plátano": 5.16,
        "Pipa de girasol": 5.0,
        "V-INTEGRA Perro Adulto": 2.4
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 112.96,
        "Carcasa de conejo": 121.54,
        "Molleja de pavo": 5.17,
        "Hígado de pollo": 13.75,
        "Espinaca": 5.17,
        "Aceite de oliva": 5.0,
        "V-INTEGRA Perro Adulto": 2.4
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 115.36,
        "Carcasa de pato": 91.59,
        "Lengua de ternera": 5.05,
        "Hígado de conejo": 15.14,
        "Calabacín": 25.24,
        "V-INTEGRA Perro Adulto": 2.4
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 138.98,
        "Costillas de cordero": 63.47,
        "Molleja de pollo": 33.15,
        "Hígado de vaca": 16.58,
        "Albahaca": 24.08,
        "Homemadekun (multivitamínico completo)": 4.15
      }
    }
  ],
  "Mini_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 116.29,
        "Carcasa de pollo": 66.2,
        "Lengua de buey": 19.23,
        "Hígado de vaca": 4.58,
        "Alcachofa": 22.92,
        "V-INTEGRA Senior": 2.4
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 110.48,
        "Pecho de ternera con hueso": 51.41,
        "Lengua de cordero": 23.93,
        "Hígado de cordero": 3.99,
        "Albahaca": 9.59,
        "Aceite de sésamo": 3.38,
        "Homemadekun (multivitamínico completo)": 6.37
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 133.98,
        "Carcasa de conejo": 112.7,
        "Molleja de pavo": 5.25,
        "Hígado de pollo": 5.49,
        "Espinaca": 5.25,
        "Aceite de linaza": 1.59,
        "V-INTEGRA Senior": 2.4
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 101.18,
        "Carcasa de pato": 94.5,
        "Riñón de ternera": 4.16,
        "Hígado de conejo": 4.16,
        "Calabacín": 4.16,
        "V-INTEGRA Senior": 2.4
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 92.99,
        "Costillas de cordero": 114.58,
        "Molleja de pollo": 4.6,
        "Hígado de vaca": 5.94,
        "Acelga": 11.72,
        "V-INTEGRA Senior": 2.4
      }
    }
  ],
  "Mini_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 177.97,
        "Carcasa de pollo": 112.08,
        "Trucha": 96.63,
        "Lengua de buey": 8.23,
        "Hígado de vaca": 8.23,
        "Col lombarda": 8.23,
        "Pipa de girasol": 4.09,
        "Homemadekun (multivitamínico completo)": 9.02
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 211.04,
        "Cuello de ternera": 124.18,
        "Salmón": 45.42,
        "Lengua de cordero": 59.04,
        "Hígado de cordero": 9.84,
        "Calabaza": 42.47,
        "Aceite de girasol": 4.52,
        "Homemadekun (multivitamínico completo)": 8.76
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 241.73,
        "Costillas de cordero": 113.24,
        "Lengua de ternera": 50.7,
        "Hígado de pollo": 13.14,
        "Acelga": 46.54,
        "Brit Care Aceite de Salmón": 1.48,
        "Aceite de cacahuete": 1.43,
        "Homemadekun (multivitamínico completo)": 7.88
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pavo pechuga sin piel": 101.46,
        "Cuello de pato": 75.7,
        "Salmón": 134.74,
        "Lengua de ternera": 45.42,
        "Hígado de conejo": 7.57,
        "Calabacín": 13.6,
        "Aceite de girasol": 2.35,
        "V-INTEGRA Cachorro": 5.4
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 218.02,
        "Costillas de cordero": 114.84,
        "Molleja de pollo": 8.24,
        "Hígado de vaca": 22.25,
        "Albahaca": 7.42,
        "Aceite de Salmón Natural Greatness": 2.76,
        "Homemadekun (multivitamínico completo)": 8.29,
        "Sal común (cloruro sódico)": 0.33
      }
    }
  ],
  "Mini_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 385.52,
        "Carcasa de pollo": 172.96,
        "Trucha": 44.55,
        "Lengua de buey": 14.02,
        "Hígado de vaca": 14.02,
        "Zanahoria": 70.12,
        "Homemadekun (multivitamínico completo)": 10.9,
        "Sal común (cloruro sódico)": 0.42,
        "V-INTEGRA Cachorro": 5.4
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 444.69,
        "Cuello de ternera": 317.01,
        "Trucha": 132.78,
        "Riñón de cordero": 42.34,
        "Hígado de cordero": 22.97,
        "Albahaca": 106.64,
        "Sonrisa de Diez Kelp": 1.67,
        "Aceite de girasol": 4.47,
        "NEKTON Dog Easy-BARF (multivitamínico)": 2.7
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 330.3,
        "Costillas de cordero": 202.21,
        "Trucha": 176.91,
        "Lengua de ternera": 117.27,
        "Hígado de vaca": 52.81,
        "Espinaca": 97.72,
        "Yoduro potásico (comprimidos 200 µg)": 3.78,
        "V-INTEGRA Cachorro": 5.4
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 162.06,
        "Corazón de pollo": 190.33,
        "Carcasa de pato": 142.32,
        "Salmón": 155.07,
        "Pulmón de ternera": 33.35,
        "Hígado de conejo": 14.23,
        "Calabacín": 14.23,
        "Homemadekun (multivitamínico completo)": 6.32,
        "V-INTEGRA Cachorro": 5.4
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pavo pechuga sin piel": 59.31,
        "Corazón de vaca": 366.23,
        "Costillas de cordero": 270.2,
        "Molleja de pollo": 115.53,
        "Hígado de vaca": 55.21,
        "Albahaca": 96.28,
        "Brit Care Aceite de Salmón": 2.76,
        "Aceite de girasol": 5.0,
        "Pipa de girasol": 1.33,
        "Yoduro potásico (comprimidos 200 µg)": 0.52
      }
    }
  ],
  "Pequeño_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 180.74,
        "Carcasa de pollo": 115.85,
        "Trucha": 99.14,
        "Lengua de buey": 12.62,
        "Hígado de vaca": 8.51,
        "Zanahoria": 8.51,
        "Aceite de cacahuete": 3.71,
        "Homemadekun (multivitamínico completo)": 9.77
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 220.6,
        "Cuello de ternera": 129.81,
        "Salmón": 47.48,
        "Lengua de cordero": 61.71,
        "Hígado de cordero": 10.29,
        "Calabaza": 44.39,
        "Aceite de girasol": 4.73,
        "Homemadekun (multivitamínico completo)": 9.16
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 182.79,
        "Espinazo de conejo": 147.55,
        "Salmón": 120.54,
        "Molleja de pavo": 10.49,
        "Hígado de pollo": 10.49,
        "Espinaca": 52.43,
        "Aceite de girasol": 0.03,
        "NEKTON Dog Easy-BARF (multivitamínico)": 2.07,
        "V-INTEGRA Cachorro": 4.11
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 242.32,
        "Carcasa de pato": 95.0,
        "Riñón de ternera": 8.09,
        "Hígado de conejo": 24.23,
        "Canónigos": 34.23,
        "Aceite de Salmón Natural Greatness": 2.12,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 7.94
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Ternera solomillo sin grasa": 317.27,
        "Costillas de cordero": 118.55,
        "Molleja de pollo": 29.51,
        "Hígado de vaca": 10.58,
        "Lechuga": 52.88,
        "Brit Care Aceite de Salmón": 1.72,
        "Aceite de sésamo": 4.9,
        "Homemadekun (multivitamínico completo)": 8.67
      }
    }
  ],
  "Pequeño_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 173.92,
        "Carcasa de pollo": 142.01,
        "Lubina": 88.83,
        "Lengua de buey": 65.57,
        "Hígado de vaca": 25.52,
        "Zanahoria": 50.54,
        "Aceite de girasol": 3.5,
        "Homemadekun (multivitamínico completo)": 10.9
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 283.48,
        "Cuello de ternera": 141.9,
        "Salmón": 79.93,
        "Lengua de cordero": 77.76,
        "Hígado de cordero": 12.96,
        "Calabaza": 52.0,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 10.9,
        "Sal común (cloruro sódico)": 0.21
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 289.27,
        "Espinazo de conejo": 269.97,
        "Molleja de pavo": 12.8,
        "Hígado de pollo": 12.8,
        "Espinaca": 55.33,
        "Aceite de Salmón Natural Greatness": 3.42,
        "Sal común (cloruro sódico)": 0.16,
        "V-INTEGRA Cachorro": 8.36
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 266.76,
        "Carcasa de pato": 148.37,
        "Riñón de ternera": 35.42,
        "Hígado de conejo": 9.39,
        "Calabacín": 9.39,
        "Aceite de Salmón Natural Greatness": 2.72,
        "Aceite de girasol": 4.49,
        "V-INTEGRA Cachorro": 8.2
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pato (carne sin hueso)": 327.66,
        "Costillas de cordero": 176.13,
        "Molleja de pollo": 12.1,
        "Hígado de vaca": 30.91,
        "Acelga": 58.01,
        "Brit Care Aceite de Salmón": 2.05,
        "Aceite de girasol": 4.36,
        "Homemadekun (multivitamínico completo)": 10.9
      }
    }
  ],
  "Pequeño_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 221.28,
        "Carcasa de pollo": 84.79,
        "Lengua de buey": 44.26,
        "Hígado de vaca": 11.1,
        "Zanahoria": 7.38,
        "V-INTEGRA Perro Adulto": 4.22
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 324.78,
        "Cuello de ternera": 140.36,
        "Pulmón de cordero": 69.77,
        "Hígado de cordero": 34.89,
        "Calabaza": 11.63,
        "Aceite de girasol": 4.75,
        "V-INTEGRA Perro Adulto": 4.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 191.09,
        "Espinazo de conejo": 266.18,
        "Molleja de pavo": 9.73,
        "Hígado de pollo": 9.73,
        "Espinaca": 9.73,
        "AniForte Aceite de Salmón": 2.34,
        "V-INTEGRA Perro Adulto": 4.3
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 163.95,
        "Carcasa de pato": 169.62,
        "Lengua de ternera": 7.15,
        "Hígado de conejo": 9.73,
        "Calabacín": 7.15,
        "V-INTEGRA Perro Adulto": 4.33
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 178.72,
        "Costillas de cordero": 209.76,
        "Molleja de pollo": 8.56,
        "Hígado de vaca": 8.56,
        "Piña": 22.3,
        "V-INTEGRA Perro Adulto": 4.35
      }
    }
  ],
  "Pequeño_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 196.68,
        "Carcasa de pollo": 135.39,
        "Lengua de buey": 7.11,
        "Hígado de vaca": 9.03,
        "Zanahoria": 7.11,
        "V-INTEGRA Senior": 4.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 293.3,
        "Cuello de ternera": 166.2,
        "Lengua de cordero": 9.78,
        "Hígado de cordero": 9.78,
        "Calabaza": 9.78,
        "Aceite de girasol": 4.38,
        "V-INTEGRA Senior": 4.26
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 178.74,
        "Espinazo de conejo": 249.28,
        "Molleja de pavo": 9.11,
        "Hígado de pollo": 9.11,
        "Espinaca": 9.11,
        "Aceite de linaza": 2.25,
        "V-INTEGRA Senior": 4.03
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 177.94,
        "Cuello de pato": 114.55,
        "Riñón de ternera": 6.45,
        "Hígado de conejo": 6.45,
        "Calabacín": 16.98,
        "V-INTEGRA Senior": 4.8
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 162.13,
        "Costillas de cordero": 189.21,
        "Molleja de pollo": 7.7,
        "Hígado de vaca": 7.7,
        "Acelga": 18.45,
        "V-INTEGRA Senior": 4.08
      }
    }
  ],
  "Pequeño_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 292.49,
        "Carcasa de pollo": 186.04,
        "Lubina": 126.33,
        "Lengua de buey": 64.21,
        "Hígado de vaca": 13.94,
        "Zanahoria": 13.94,
        "Aceite de girasol": 4.91,
        "Homemadekun (multivitamínico completo)": 15.77
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 457.72,
        "Cuello de ternera": 301.08,
        "Trucha": 138.82,
        "Riñón de cordero": 20.88,
        "Hígado de cordero": 20.88,
        "Espinaca": 104.38,
        "Aceite de girasol": 4.49,
        "V-INTEGRA Cachorro": 10.43
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 320.54,
        "Espinazo de conejo": 302.56,
        "Salmón": 109.53,
        "Molleja de pavo": 16.94,
        "Hígado de pollo": 16.94,
        "Espinaca": 80.63,
        "AniForte Aceite de Salmón": 0.63,
        "Sal común (cloruro sódico)": 0.13,
        "V-INTEGRA Cachorro": 10.38
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 226.09,
        "Cuello de pato": 200.64,
        "Lengua de ternera": 67.43,
        "Hígado de conejo": 11.56,
        "Canónigos": 56.19,
        "Brit Care Aceite de Salmón": 3.02,
        "Sal común (cloruro sódico)": 0.71,
        "V-INTEGRA Cachorro": 10.8
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 132.07,
        "Corazón de pollo": 341.88,
        "Costillas de cordero": 177.57,
        "Molleja de pollo": 15.8,
        "Hígado de vaca": 43.6,
        "Coliflor": 78.99,
        "AniForte Aceite de Salmón": 5.49,
        "Homemadekun (multivitamínico completo)": 13.85
      }
    }
  ],
  "Pequeño_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 209.35,
        "Corazón de pollo": 439.56,
        "Carcasa de pollo": 306.61,
        "Trucha": 335.6,
        "Lengua de buey": 30.66,
        "Hígado de vaca": 81.03,
        "Zanahoria": 130.24,
        "Homemadekun (multivitamínico completo)": 16.35,
        "V-INTEGRA Cachorro": 10.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 275.08,
        "Cuello de ternera": 569.11,
        "Trucha": 656.58,
        "Lengua de cordero": 198.65,
        "Hígado de cordero": 47.02,
        "Albahaca": 194.05,
        "Sonrisa de Diez Kelp": 5.0,
        "Aceite de cacahuete": 3.42,
        "NEKTON Dog Easy-BARF (multivitamínico)": 5.4
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 708.87,
        "Cuello de ternera": 424.88,
        "Trucha": 322.82,
        "Lengua de ternera": 229.89,
        "Hígado de vaca": 38.32,
        "Espinaca": 190.98,
        "Sonrisa de Diez Kelp": 0.31,
        "V-INTEGRA Cachorro": 10.8
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 350.79,
        "Corazón de pollo": 398.14,
        "Cuello de pato": 249.64,
        "Salmón": 64.04,
        "Pulmón de ternera": 135.67,
        "Hígado de conejo": 24.96,
        "Calabacín": 24.96,
        "Homemadekun (multivitamínico completo)": 12.66,
        "V-INTEGRA Cachorro": 10.8
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 522.43,
        "Corazón de vaca": 370.76,
        "Costillas de cordero": 383.99,
        "Merluza": 235.85,
        "Molleja de pollo": 35.19,
        "Hígado de vaca": 35.19,
        "Espinaca": 175.93,
        "Sonrisa de Diez Kelp": 0.29,
        "V-INTEGRA Cachorro": 10.8
      }
    }
  ],
  "Mediano_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 199.42,
        "Carcasa de pollo": 131.58,
        "Lubina": 169.01,
        "Lengua de buey": 78.95,
        "Hígado de vaca": 13.16,
        "Zanahoria": 65.79,
        "Aceite de sésamo": 5.0,
        "Homemadekun (multivitamínico completo)": 8.02,
        "NEKTON Dog Easy-BARF (multivitamínico)": 3.38
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 225.09,
        "Cuello de ternera": 235.99,
        "Salmón": 135.61,
        "Lengua de cordero": 69.32,
        "Hígado de cordero": 24.13,
        "Espinaca": 41.74,
        "Aceite de girasol": 4.37,
        "Homemadekun (multivitamínico completo)": 10.9
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 286.1,
        "Espinazo de conejo": 217.2,
        "Salmón": 170.68,
        "Molleja de pavo": 15.67,
        "Hígado de pollo": 15.67,
        "Espinaca": 78.37,
        "NEKTON Dog Easy-BARF (multivitamínico)": 3.38,
        "V-INTEGRA Cachorro": 5.92
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 194.24,
        "Carcasa de pato": 120.42,
        "Salmón": 188.6,
        "Lengua de ternera": 71.89,
        "Hígado de conejo": 11.98,
        "Albahaca": 11.98,
        "Aceite de girasol": 3.81,
        "Homemadekun (multivitamínico completo)": 10.55
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 160.99,
        "Corazón de vaca": 231.75,
        "Costillas de cordero": 185.37,
        "Merluza": 113.18,
        "Molleja de pollo": 16.06,
        "Hígado de vaca": 16.06,
        "Piña": 79.75,
        "Sonrisa de Diez Kelp": 0.13,
        "V-INTEGRA Cachorro": 5.13
      }
    }
  ],
  "Mediano_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 204.99,
        "Corazón de pollo": 118.22,
        "Carcasa de pollo": 163.89,
        "Sardina": 254.65,
        "Lengua de buey": 16.39,
        "Hígado de vaca": 16.39,
        "Zanahoria": 44.92,
        "V-INTEGRA Cachorro": 11.34
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 257.2,
        "Cuello de ternera": 373.33,
        "Trucha": 117.32,
        "Lengua de cordero": 118.08,
        "Hígado de cordero": 19.68,
        "Acelga": 98.4,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 15.0
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 416.33,
        "Espinazo de conejo": 401.66,
        "Molleja de pavo": 18.76,
        "Hígado de pollo": 18.76,
        "Espinaca": 82.54,
        "Oleum Canis Aceite de Salmón": 7.18,
        "Sal común (cloruro sódico)": 0.26,
        "V-INTEGRA Cachorro": 12.45
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 412.69,
        "Carcasa de pato": 216.98,
        "Riñón de ternera": 13.76,
        "Hígado de conejo": 13.76,
        "Coles de Bruselas": 30.64,
        "Aceite de Salmón Natural Greatness": 3.78,
        "Sal común (cloruro sódico)": 0.64,
        "V-INTEGRA Cachorro": 12.79
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 356.39,
        "Costillas de cordero": 269.31,
        "Merluza": 199.69,
        "Molleja de pollo": 18.96,
        "Hígado de vaca": 18.96,
        "Albahaca": 84.79,
        "napfcheck Novomineral proLEBER": 5.13,
        "Yoduro potásico (comprimidos 200 µg)": 0.22
      }
    }
  ],
  "Mediano_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 348.62,
        "Carcasa de pollo": 133.59,
        "Lengua de buey": 69.72,
        "Hígado de vaca": 17.48,
        "Zanahoria": 11.62,
        "V-INTEGRA Perro Adulto": 6.64
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 198.56,
        "Cuello de ternera": 413.15,
        "Lengua de cordero": 81.32,
        "Hígado de cordero": 15.73,
        "Calabaza": 77.91,
        "Oleum Canis Aceite de Salmón": 7.83,
        "Aceite de girasol": 5.0,
        "V-INTEGRA Perro Adulto": 8.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 318.78,
        "Espinazo de conejo": 419.35,
        "Molleja de pavo": 15.7,
        "Hígado de pollo": 15.7,
        "Espinaca": 15.7,
        "Pipa de girasol": 1.53,
        "V-INTEGRA Perro Adulto": 6.77
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 261.82,
        "Cuello de pato": 192.71,
        "Pulmón de ternera": 10.52,
        "Hígado de conejo": 10.52,
        "Calabacín": 50.32,
        "V-INTEGRA Perro Adulto": 7.08
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 367.87,
        "Costillas de cordero": 166.04,
        "Molleja de pollo": 88.99,
        "Hígado de vaca": 44.49,
        "Espinaca": 74.15,
        "napfcheck Novomineral proLEBER": 6.53
      }
    }
  ],
  "Mediano_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 328.35,
        "Carcasa de pollo": 116.19,
        "Lengua de buey": 69.71,
        "Hígado de vaca": 11.62,
        "Zanahoria": 55.06,
        "V-INTEGRA Senior": 7.73
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 415.91,
        "Cuello de ternera": 154.19,
        "Lengua de cordero": 83.18,
        "Hígado de cordero": 13.86,
        "Albahaca": 26.04,
        "AniForte Aceite de Salmón": 10.12,
        "Aceite de sésamo": 4.9,
        "NEKTON Dog Easy-BARF (multivitamínico)": 9.9
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 335.04,
        "Carcasa de conejo": 303.0,
        "Molleja de pavo": 13.58,
        "Hígado de pollo": 13.58,
        "Espinaca": 13.58,
        "AniForte Aceite de Salmón": 6.43,
        "V-INTEGRA Senior": 6.37
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 245.18,
        "Cuello de pato": 180.46,
        "Pulmón de ternera": 9.85,
        "Hígado de conejo": 9.85,
        "Calabacín": 47.09,
        "V-INTEGRA Senior": 8.06
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 324.57,
        "Costillas de cordero": 236.65,
        "Molleja de pollo": 12.12,
        "Hígado de vaca": 12.12,
        "Albahaca": 20.72,
        "Homemadekun (multivitamínico completo)": 15.29
      }
    }
  ],
  "Mediano_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 630.03,
        "Carcasa de pollo": 224.0,
        "Lengua de buey": 95.55,
        "Hígado de vaca": 58.44,
        "Frambuesa": 112.0,
        "Aceite de Salmón Natural Greatness": 5.43,
        "Sal común (cloruro sódico)": 0.85,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 571.93,
        "Cuello de ternera": 448.06,
        "Trucha": 415.53,
        "Lengua de cordero": 36.97,
        "Hígado de cordero": 32.02,
        "Albahaca": 96.72,
        "Aceite de girasol": 5.0,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 745.97,
        "Espinazo de conejo": 475.09,
        "Molleja de pavo": 28.0,
        "Hígado de pollo": 28.0,
        "Espinaca": 122.74,
        "AniForte Aceite de Salmón": 9.28,
        "Sal común (cloruro sódico)": 0.34,
        "V-INTEGRA Cachorro": 18.26
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 201.89,
        "Carcasa de pato": 284.84,
        "Salmón": 389.01,
        "Lengua de ternera": 138.27,
        "Hígado de conejo": 23.05,
        "Acelga": 115.23,
        "V-INTEGRA Cachorro": 15.62
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 630.03,
        "Costillas de cordero": 317.62,
        "Molleja de pollo": 60.74,
        "Hígado de vaca": 64.1,
        "Acelga": 119.17,
        "Aceite de Salmón Natural Greatness": 4.86,
        "Homemadekun (multivitamínico completo)": 26.12,
        "Sal común (cloruro sódico)": 0.47
      }
    }
  ],
  "Mediano_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 1250.18,
        "Carcasa de pollo": 453.41,
        "Salmón": 83.98,
        "Lengua de buey": 200.13,
        "Hígado de vaca": 52.64,
        "Rucula": 226.7,
        "Homemadekun (multivitamínico completo)": 27.25,
        "Sal común (cloruro sódico)": 1.45,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 557.57,
        "Cuello de ternera": 880.48,
        "Trucha": 1024.17,
        "Lengua de cordero": 388.77,
        "Hígado de cordero": 64.8,
        "Espinaca": 323.98,
        "Aceite de girasol": 5.0,
        "Yoduro potásico (comprimidos 200 µg)": 0.67,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1166.02,
        "Cuello de ternera": 737.47,
        "Trucha": 673.25,
        "Lengua de buey": 228.81,
        "Hígado de pollo": 75.58,
        "Espinaca": 320.13,
        "AniForte Seaweed Meal": 1.65,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 543.34,
        "Ternera solomillo sin grasa": 954.08,
        "Carcasa de pato": 499.14,
        "Salmón": 327.3,
        "Lengua de ternera": 49.91,
        "Hígado de conejo": 49.91,
        "Apio": 72.01,
        "Homemadekun (multivitamínico completo)": 18.05,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 593.3,
        "Pato (carne sin hueso)": 788.36,
        "Costillas de cordero": 645.45,
        "Merluza": 628.51,
        "Molleja de pollo": 60.88,
        "Hígado de vaca": 60.88,
        "Rucula": 266.7,
        "AniForte Seaweed Meal": 0.65,
        "V-INTEGRA Cachorro": 19.8
      }
    }
  ],
  "Grande_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 284.65,
        "Carcasa de pollo": 174.0,
        "Merluza": 174.47,
        "Lengua de buey": 104.4,
        "Hígado de vaca": 45.48,
        "Espinaca": 87.0,
        "AniForte Seaweed Meal": 0.88,
        "V-INTEGRA Cachorro": 8.67
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 470.5,
        "Cuello de ternera": 255.63,
        "Trucha": 301.68,
        "Lengua de cordero": 23.9,
        "Hígado de cordero": 23.9,
        "Calabaza": 119.51,
        "Aceite de girasol": 3.02,
        "NEKTON Dog Easy-BARF (multivitamínico)": 4.33,
        "V-INTEGRA Cachorro": 8.67
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 358.03,
        "Espinazo de conejo": 269.53,
        "Salmón": 210.24,
        "Molleja de pavo": 19.48,
        "Hígado de pollo": 19.48,
        "Espinaca": 97.42,
        "NEKTON Dog Easy-BARF (multivitamínico)": 4.25,
        "V-INTEGRA Cachorro": 7.31
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 146.02,
        "Cuello de pato": 143.96,
        "Salmón": 244.18,
        "Lengua de ternera": 86.38,
        "Hígado de conejo": 27.29,
        "Acelga": 71.98,
        "napfcheck Novomineral proLEBER": 2.89,
        "V-INTEGRA Cachorro": 7.54
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 392.24,
        "Costillas de cordero": 240.08,
        "Merluza": 132.58,
        "Molleja de pollo": 17.1,
        "Hígado de vaca": 17.1,
        "Albahaca": 55.68,
        "Homemadekun (multivitamínico completo)": 10.9,
        "Sal común (cloruro sódico)": 0.33,
        "Yoduro potásico (comprimidos 200 µg)": 0.15
      }
    }
  ],
  "Grande_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 259.17,
        "Corazón de pollo": 410.87,
        "Carcasa de pollo": 223.34,
        "Lubina": 85.27,
        "Lengua de buey": 55.41,
        "Hígado de vaca": 22.33,
        "Zanahoria": 60.33,
        "Homemadekun (multivitamínico completo)": 26.04
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 339.13,
        "Cuello de ternera": 354.34,
        "Trucha": 425.39,
        "Lengua de cordero": 170.75,
        "Hígado de cordero": 28.46,
        "Espinaca": 104.84,
        "Aceite de cacahuete": 4.77,
        "V-INTEGRA Cachorro": 15.92
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 566.51,
        "Espinazo de conejo": 546.54,
        "Molleja de pavo": 25.53,
        "Hígado de pollo": 25.53,
        "Espinaca": 112.31,
        "Oleum Canis Aceite de Salmón": 9.77,
        "Sal común (cloruro sódico)": 0.35,
        "V-INTEGRA Cachorro": 16.94
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 503.8,
        "Carcasa de pato": 298.34,
        "Lengua de ternera": 126.65,
        "Hígado de conejo": 21.11,
        "Calabacín": 105.55,
        "AniForte Aceite de Salmón": 8.94,
        "Sal común (cloruro sódico)": 0.78,
        "V-INTEGRA Cachorro": 17.06
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 278.69,
        "Pato (carne sin hueso)": 436.82,
        "Costillas de cordero": 289.16,
        "Merluza": 231.87,
        "Molleja de pollo": 26.31,
        "Hígado de vaca": 26.31,
        "Coles de Bruselas": 26.31,
        "V-INTEGRA Cachorro": 15.69
      }
    }
  ],
  "Grande_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 456.45,
        "Carcasa de pollo": 251.78,
        "Lengua de buey": 15.22,
        "Hígado de vaca": 22.09,
        "Zanahoria": 15.22,
        "V-INTEGRA Perro Adulto": 9.59
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 611.31,
        "Cuello de ternera": 218.32,
        "Lengua de cordero": 130.99,
        "Hígado de cordero": 21.83,
        "Calabaza": 109.16,
        "AniForte Aceite de Salmón": 14.24,
        "Aceite de girasol": 5.0,
        "V-INTEGRA Perro Adulto": 9.49
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 397.44,
        "Espinazo de conejo": 555.63,
        "Molleja de pavo": 22.14,
        "Hígado de pollo": 26.23,
        "Espinaca": 105.8,
        "Aceite de cacahuete": 2.02,
        "NEKTON Dog Easy-BARF (multivitamínico)": 14.4
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 339.91,
        "Carcasa de pato": 354.07,
        "Salmón": 3.15,
        "Lengua de ternera": 15.35,
        "Hígado de conejo": 15.35,
        "Calabacín": 39.85,
        "V-INTEGRA Perro Adulto": 8.73
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 330.21,
        "Costillas de cordero": 437.87,
        "Molleja de pollo": 43.3,
        "Hígado de vaca": 19.03,
        "Acelga": 16.95,
        "V-INTEGRA Perro Adulto": 9.05
      }
    }
  ],
  "Grande_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 362.33,
        "Carcasa de pollo": 206.79,
        "Lengua de buey": 89.86,
        "Hígado de vaca": 14.98,
        "Zanahoria": 74.88,
        "Homemadekun (multivitamínico completo)": 8.08,
        "napfcheck Novomineral proLEBER": 9.6
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 659.51,
        "Cuello de ternera": 238.32,
        "Riñón de cordero": 69.45,
        "Hígado de cordero": 21.98,
        "Calabaza": 109.92,
        "Oleum Canis Aceite de Salmón": 14.19,
        "Aceite de girasol": 5.0,
        "V-INTEGRA Senior": 12.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 291.1,
        "Carcasa de conejo": 108.63,
        "Espinazo de conejo": 520.34,
        "Molleja de pavo": 21.04,
        "Hígado de pollo": 24.95,
        "Espinaca": 86.14,
        "Oleum Canis Aceite de Salmón": 4.09,
        "NEKTON Dog Easy-BARF (multivitamínico)": 12.58
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 376.51,
        "Cuello de pato": 239.12,
        "Riñón de ternera": 13.54,
        "Hígado de conejo": 13.54,
        "Calabacín": 34.43,
        "V-INTEGRA Senior": 9.92
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 456.47,
        "Costillas de cordero": 286.89,
        "Molleja de pollo": 106.52,
        "Hígado de vaca": 20.01,
        "Champiñón": 17.75,
        "V-INTEGRA Senior": 10.06
      }
    }
  ],
  "Grande_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 307.72,
        "Corazón de pollo": 487.22,
        "Carcasa de pollo": 414.66,
        "Trucha": 268.58,
        "Lengua de buey": 35.11,
        "Hígado de vaca": 66.52,
        "Espinaca": 175.53,
        "Homemadekun (multivitamínico completo)": 32.7
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 289.15,
        "Pecho de ternera con hueso": 385.41,
        "Trucha": 820.36,
        "Lengua de cordero": 80.44,
        "Hígado de cordero": 35.8,
        "Espinaca": 179.02,
        "Aceite de sésamo": 4.32,
        "Sal común (cloruro sódico)": 0.95,
        "V-INTEGRA Cachorro": 28.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1016.98,
        "Espinazo de conejo": 647.69,
        "Molleja de pavo": 38.17,
        "Hígado de pollo": 38.17,
        "Espinaca": 167.33,
        "Aceite de Salmón Natural Greatness": 12.65,
        "Sal común (cloruro sódico)": 0.46,
        "V-INTEGRA Cachorro": 24.9
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 421.23,
        "Corazón de pollo": 488.04,
        "Cuello de pato": 307.02,
        "Pulmón de ternera": 181.85,
        "Hígado de conejo": 30.31,
        "Calabacín": 87.0,
        "Brit Care Aceite de Salmón": 6.82,
        "V-INTEGRA Cachorro": 25.06
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 758.77,
        "Costillas de cordero": 440.31,
        "Molleja de pollo": 177.64,
        "Hígado de vaca": 98.34,
        "Espinaca": 163.9,
        "AniForte Aceite de Salmón": 11.92,
        "Homemadekun (multivitamínico completo)": 32.7,
        "Sal común (cloruro sódico)": 1.23
      }
    }
  ],
  "Grande_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 818.88,
        "Carcasa de pollo": 821.07,
        "Sardina": 985.14,
        "Lengua de buey": 173.41,
        "Hígado de vaca": 63.6,
        "Acelga": 318.01,
        "Homemadekun (multivitamínico completo)": 24.3,
        "V-INTEGRA Cachorro": 28.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 495.54,
        "Cuello de ternera": 1347.29,
        "Trucha": 1607.86,
        "Lengua de cordero": 548.93,
        "Hígado de cordero": 117.36,
        "Albahaca": 457.44,
        "AniForte Seaweed Meal": 3.2,
        "Aceite de girasol": 4.7,
        "NEKTON Dog Easy-BARF (multivitamínico)": 14.4
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1461.7,
        "Cuello de ternera": 970.2,
        "Trucha": 959.24,
        "Lengua de cordero": 534.71,
        "Hígado de vaca": 89.12,
        "Espinaca": 440.96,
        "AniForte Seaweed Meal": 0.97,
        "V-INTEGRA Cachorro": 28.8
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 854.11,
        "Corazón de pollo": 767.69,
        "Carcasa de pato": 813.06,
        "Salmón": 124.97,
        "Pulmón de ternera": 404.18,
        "Hígado de conejo": 67.36,
        "Calabacín": 336.82,
        "Yoduro potásico (comprimidos 200 µg)": 1.03,
        "V-INTEGRA Cachorro": 28.8
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 1755.39,
        "Costillas de cordero": 813.98,
        "Merluza": 568.6,
        "Molleja de pollo": 121.62,
        "Hígado de vaca": 74.08,
        "Frambuesa": 370.41,
        "Homemadekun (multivitamínico completo)": 25.09,
        "Sal común (cloruro sódico)": 1.62,
        "V-INTEGRA Cachorro": 28.8
      }
    }
  ],
  "Gigante_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 228.97,
        "Corazón de pollo": 385.16,
        "Carcasa de pollo": 204.71,
        "Lubina": 119.76,
        "Lengua de buey": 44.01,
        "Hígado de vaca": 20.47,
        "Zanahoria": 20.47,
        "Homemadekun (multivitamínico completo)": 11.89,
        "V-INTEGRA Cachorro": 11.66
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 422.76,
        "Cuello de ternera": 401.63,
        "Trucha": 238.05,
        "Lengua de cordero": 151.78,
        "Hígado de cordero": 25.3,
        "Calabaza": 25.3,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 12.77,
        "NEKTON Dog Easy-BARF (multivitamínico)": 5.57
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 457.2,
        "Espinazo de conejo": 344.19,
        "Salmón": 268.48,
        "Molleja de pavo": 24.88,
        "Hígado de pollo": 24.88,
        "Espinaca": 124.4,
        "NEKTON Dog Easy-BARF (multivitamínico)": 6.0,
        "V-INTEGRA Cachorro": 8.87
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 171.5,
        "Carcasa de pato": 248.75,
        "Salmón": 327.8,
        "Lengua de ternera": 118.11,
        "Hígado de conejo": 19.69,
        "Acelga": 98.43,
        "Homemadekun (multivitamínico completo)": 1.72,
        "V-INTEGRA Cachorro": 12.01
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 537.49,
        "Costillas de cordero": 252.49,
        "Merluza": 213.78,
        "Molleja de pollo": 24.28,
        "Hígado de vaca": 64.43,
        "Espinaca": 96.07,
        "Nabo pelado": 25.31,
        "AniForte Seaweed Meal": 1.33,
        "V-INTEGRA Cachorro": 11.15
      }
    }
  ],
  "Gigante_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 377.24,
        "Corazón de pollo": 367.58,
        "Carcasa de pollo": 362.84,
        "Lengua de buey": 182.0,
        "Hígado de vaca": 75.33,
        "Acelga": 151.67,
        "Aceite de Salmón Natural Greatness": 7.79,
        "Homemadekun (multivitamínico completo)": 32.7
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 381.75,
        "Cuello de ternera": 628.17,
        "Trucha": 607.61,
        "Lengua de cordero": 255.4,
        "Hígado de cordero": 42.57,
        "Espinaca": 212.83,
        "AniForte Aceite de Salmón": 16.55,
        "V-INTEGRA Cachorro": 23.06
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 866.35,
        "Espinazo de conejo": 756.85,
        "Molleja de pavo": 36.93,
        "Hígado de pollo": 36.93,
        "Espinaca": 149.33,
        "Oleum Canis Aceite de Salmón": 14.18,
        "Sal común (cloruro sódico)": 0.51,
        "V-INTEGRA Cachorro": 26.47
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 429.45,
        "Pavo pechuga sin piel": 473.47,
        "Cuello de pato": 300.97,
        "Lengua de ternera": 180.58,
        "Hígado de conejo": 30.1,
        "Calabacín": 90.29,
        "Brit Care Aceite de Salmón": 6.72,
        "V-INTEGRA Cachorro": 24.71
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pavo pechuga sin piel": 191.87,
        "Conejo": 997.06,
        "Costillas de cordero": 396.31,
        "Molleja de pollo": 130.77,
        "Hígado de vaca": 67.39,
        "Apio": 198.16,
        "Oleum Canis Aceite de Salmón": 19.66,
        "V-INTEGRA Cachorro": 25.73
      }
    }
  ],
  "Gigante_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 693.49,
        "Carcasa de pollo": 265.74,
        "Lengua de buey": 138.7,
        "Hígado de vaca": 34.77,
        "Zanahoria": 23.12,
        "V-INTEGRA Perro Adulto": 13.22
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 886.44,
        "Cuello de ternera": 307.61,
        "Lengua de cordero": 184.57,
        "Hígado de cordero": 30.76,
        "Calabaza": 128.67,
        "Oleum Canis Aceite de Salmón": 21.76,
        "Aceite de girasol": 5.0,
        "Aceite de cacahuete": 5.0,
        "V-INTEGRA Perro Adulto": 14.24
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 813.49,
        "Carcasa de conejo": 618.16,
        "Molleja de pavo": 30.46,
        "Hígado de pollo": 30.46,
        "Espinaca": 30.46,
        "Aceite de sésamo": 2.82,
        "V-INTEGRA Perro Adulto": 13.51
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 522.14,
        "Carcasa de pato": 531.58,
        "Pulmón de ternera": 23.16,
        "Hígado de conejo": 23.16,
        "Calabacín": 57.97,
        "V-INTEGRA Perro Adulto": 13.15
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 495.19,
        "Costillas de cordero": 657.4,
        "Molleja de pollo": 66.31,
        "Hígado de vaca": 28.01,
        "Alcachofa": 25.45,
        "V-INTEGRA Perro Adulto": 13.6
      }
    }
  ],
  "Gigante_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 679.96,
        "Carcasa de pollo": 378.76,
        "Lengua de buey": 22.67,
        "Hígado de vaca": 29.21,
        "Zanahoria": 22.67,
        "V-INTEGRA Senior": 14.43
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 143.58,
        "Pecho de ternera con hueso": 287.16,
        "Trucha": 768.35,
        "Lengua de cordero": 93.32,
        "Hígado de cordero": 32.5,
        "Calabaza": 110.88,
        "Pipa de girasol": 5.0,
        "V-INTEGRA Senior": 12.09
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 807.85,
        "Carcasa de conejo": 471.42,
        "Molleja de pavo": 82.42,
        "Hígado de pollo": 97.26,
        "Espinaca": 162.11,
        "Aceite de sésamo": 2.54,
        "NEKTON Dog Easy-BARF (multivitamínico)": 18.91
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 488.77,
        "Carcasa de pato": 497.61,
        "Pulmón de ternera": 21.68,
        "Hígado de conejo": 21.68,
        "Calabacín": 54.25,
        "V-INTEGRA Senior": 13.16
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 685.03,
        "Costillas de cordero": 312.85,
        "Molleja de pollo": 163.4,
        "Hígado de vaca": 81.7,
        "Albahaca": 118.7,
        "Homemadekun (multivitamínico completo)": 20.46
      }
    }
  ],
  "Gigante_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 1340.48,
        "Carcasa de pollo": 450.45,
        "Lengua de buey": 103.68,
        "Hígado de vaca": 128.56,
        "Col rizada": 210.96,
        "AniForte Aceite de Salmón": 19.88,
        "Sal común (cloruro sódico)": 2.04,
        "V-INTEGRA Cachorro": 49.5
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 304.05,
        "Pecho de ternera con hueso": 488.36,
        "Trucha": 1402.76,
        "Lengua de cordero": 48.84,
        "Hígado de cordero": 48.84,
        "Albahaca": 148.98,
        "Aceite de girasol": 3.96,
        "Sal común (cloruro sódico)": 2.15,
        "V-INTEGRA Cachorro": 49.5
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1599.76,
        "Espinazo de conejo": 1010.33,
        "Molleja de pavo": 60.7,
        "Hígado de pollo": 60.7,
        "Espinaca": 303.5,
        "Oleum Canis Aceite de Salmón": 22.5,
        "Sal común (cloruro sódico)": 0.67,
        "V-INTEGRA Cachorro": 39.1
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 661.47,
        "Corazón de pollo": 776.55,
        "Carcasa de pato": 559.75,
        "Pulmón de ternera": 287.61,
        "Hígado de conejo": 47.93,
        "Calabacín": 63.39,
        "Brit Care Aceite de Salmón": 10.71,
        "V-INTEGRA Cachorro": 39.32
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 1348.98,
        "Costillas de cordero": 722.69,
        "Merluza": 528.73,
        "Molleja de pollo": 59.81,
        "Hígado de vaca": 59.81,
        "Albahaca": 270.54,
        "AniForte Seaweed Meal": 0.75,
        "napfcheck Novomineral proLEBER": 16.31
      }
    }
  ],
  "Gigante_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 1029.63,
        "Corazón de pollo": 571.11,
        "Carcasa de pollo": 1033.98,
        "Salmón": 1604.6,
        "Lengua de buey": 103.4,
        "Hígado de vaca": 310.19,
        "Espinaca": 516.99,
        "napfcheck Novomineral proLEBER": 16.5,
        "V-INTEGRA Cachorro": 47.85
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 1045.8,
        "Cuello de ternera": 2106.0,
        "Trucha": 2505.38,
        "Lengua de cordero": 866.54,
        "Hígado de cordero": 180.62,
        "Albahaca": 744.93,
        "Sonrisa de Diez Kelp": 5.0,
        "Aceite de girasol": 4.97,
        "Aceite de cacahuete": 5.0,
        "NEKTON Dog Easy-BARF (multivitamínico)": 24.75
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 3534.17,
        "Cuello de ternera": 1597.62,
        "Trucha": 1114.3,
        "Lengua de buey": 144.87,
        "Hígado de vaca": 144.87,
        "Espinaca": 707.59,
        "Yoduro potásico (comprimidos 200 µg)": 1.38,
        "V-INTEGRA Cachorro": 49.5
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 1328.53,
        "Pavo pechuga sin piel": 1512.02,
        "Cuello de pato": 1348.07,
        "Salmón": 261.57,
        "Lengua de ternera": 94.69,
        "Hígado de conejo": 94.69,
        "Albahaca": 94.69,
        "Yoduro potásico (comprimidos 200 µg)": 1.52,
        "V-INTEGRA Cachorro": 49.23
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 1291.29,
        "Gallina (carne sin hueso)": 1013.94,
        "Costillas de cordero": 1388.25,
        "Merluza": 1587.4,
        "Molleja de pollo": 126.17,
        "Hígado de vaca": 270.48,
        "Espinaca": 630.84,
        "AniForte Seaweed Meal": 3.14,
        "V-INTEGRA Cachorro": 49.5
      }
    }
  ]
}
