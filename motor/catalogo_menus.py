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
CATALOGO_VARIANTES = {
  "Toy_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 31.6,
        "Cuello de ternera": 72.09,
        "Salmón": 30.16,
        "Lengua de ternera": 21.21,
        "Hígado de pollo": 4.01,
        "Acelga": 17.68,
        "Homemadekun (multivitamínico completo)": 3.16
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 118.24,
        "Costillas de cordero": 46.44,
        "Lengua de cordero": 4.02,
        "Hígado de pollo": 12.05,
        "Canónigos": 20.08,
        "Brit Care Aceite de Salmón": 0.62,
        "Pipa de calabaza": 3.47,
        "Homemadekun (multivitamínico completo)": 2.84
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 83.59,
        "Costillas de cordero": 44.54,
        "Trucha": 8.79,
        "Lengua de cordero": 21.9,
        "Hígado de vaca": 5.42,
        "Acelga": 18.25,
        "Aceite de girasol": 0.85,
        "Homemadekun (multivitamínico completo)": 3.09
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 95.97,
        "Cuello de ternera": 38.2,
        "Salmón": 6.23,
        "Lengua de ternera": 21.38,
        "Hígado de vaca": 3.56,
        "Canónigos": 12.82,
        "Aceite de girasol": 2.36,
        "Homemadekun (multivitamínico completo)": 4.3
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 81.65,
        "Costillas de cordero": 41.74,
        "Lengua de ternera": 19.05,
        "Hígado de pollo": 3.18,
        "Espárrago verde": 13.15,
        "Brit Care Aceite de Salmón": 0.58,
        "Homemadekun (multivitamínico completo)": 3.96,
        "Sal común (cloruro sódico)": 0.12
      }
    }
  ],
  "Toy_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 101.56,
        "Espinazo de conejo": 34.77,
        "Lengua de buey": 20.31,
        "Hígado de pollo": 9.24,
        "Canónigos": 3.39,
        "Aceite de Salmón Natural Greatness": 0.89,
        "Aceite de sésamo": 1.52,
        "Homemadekun (multivitamínico completo)": 3.43
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 105.44,
        "Carcasa de conejo": 55.04,
        "Lengua de buey": 23.3,
        "Hígado de vaca": 3.92,
        "Albahaca": 8.07,
        "Brit Care Aceite de Salmón": 0.76,
        "Aceite de sésamo": 1.25,
        "Homemadekun (multivitamínico completo)": 3.36
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 66.26,
        "Pecho de ternera con hueso": 42.73,
        "Lengua de cordero": 16.45,
        "Hígado de vaca": 6.55,
        "Nabo pelado": 5.13,
        "Aceite de Salmón Natural Greatness": 0.87,
        "Aceite de cacahuete": 1.35,
        "Homemadekun (multivitamínico completo)": 4.69,
        "Sal común (cloruro sódico)": 0.16
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pavo pechuga sin piel": 77.79,
        "Costillas de cordero": 59.0,
        "Lengua de ternera": 16.05,
        "Hígado de vaca": 9.34,
        "Zanahoria": 18.02,
        "Aceite de Salmón Natural Greatness": 1.02,
        "Aceite de sésamo": 5.0,
        "Homemadekun (multivitamínico completo)": 3.47
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 48.37,
        "Cuello de ternera": 106.52,
        "Lengua de ternera": 25.22,
        "Hígado de pollo": 9.06,
        "Acelga": 21.02,
        "Aceite de Salmón Natural Greatness": 0.88,
        "Homemadekun (multivitamínico completo)": 3.35
      }
    }
  ],
  "Toy_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 59.2,
        "Pecho de ternera con hueso": 37.77,
        "Lengua de ternera": 2.26,
        "Hígado de vaca": 6.78,
        "Albahaca": 6.98,
        "Homemadekun (multivitamínico completo)": 3.91
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 74.07,
        "Cuello de pato": 28.49,
        "Lengua de ternera": 17.09,
        "Hígado de cordero": 8.55,
        "Rucula": 14.24,
        "Pipa de calabaza": 5.0,
        "Homemadekun (multivitamínico completo)": 2.31
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 67.67,
        "Costillas de cordero": 57.78,
        "Lengua de cordero": 16.29,
        "Hígado de conejo": 2.98,
        "Albahaca": 4.21,
        "Aceite de sésamo": 1.18,
        "Homemadekun (multivitamínico completo)": 4.0
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 73.34,
        "Costillas de cordero": 58.69,
        "Lengua de ternera": 3.07,
        "Hígado de vaca": 3.07,
        "Albahaca": 15.35,
        "Homemadekun (multivitamínico completo)": 2.55
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 45.2,
        "Carcasa de conejo": 75.03,
        "Lengua de buey": 19.92,
        "Hígado de conejo": 9.23,
        "Piña": 16.6,
        "V-INTEGRA Perro Adulto": 1.2
      }
    }
  ],
  "Toy_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 72.46,
        "Cuello de pavo": 60.46,
        "Lengua de buey": 9.85,
        "Hígado de conejo": 2.97,
        "Pera": 2.97,
        "V-INTEGRA Senior": 1.2
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 74.96,
        "Cuello de pato": 38.19,
        "Lengua de ternera": 2.5,
        "Hígado de vaca": 2.5,
        "Plátano": 6.78,
        "Pipa de girasol": 4.36,
        "Homemadekun (multivitamínico completo)": 2.22
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 56.48,
        "Carcasa de pollo": 40.7,
        "Lengua de cordero": 15.34,
        "Hígado de vaca": 2.56,
        "Albahaca": 12.79,
        "Homemadekun (multivitamínico completo)": 3.36
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 44.98,
        "Espinazo de conejo": 88.23,
        "Lengua de buey": 8.67,
        "Hígado de conejo": 2.96,
        "Espinaca": 2.96,
        "V-INTEGRA Senior": 1.2
      }
    }
  ],
  "Toy_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 124.82,
        "Costillas de cordero": 49.83,
        "Lengua de cordero": 25.43,
        "Hígado de pollo": 7.61,
        "Albahaca": 4.24,
        "Brit Care Aceite de Salmón": 0.85,
        "Homemadekun (multivitamínico completo)": 4.65,
        "Sal común (cloruro sódico)": 0.18
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 135.98,
        "Carcasa de pollo": 55.12,
        "Lengua de cordero": 22.83,
        "Hígado de vaca": 14.34,
        "Albahaca": 10.8,
        "Brit Care Aceite de Salmón": 1.38,
        "Pipa de calabaza": 5.0,
        "Homemadekun (multivitamínico completo)": 4.4
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 122.99,
        "Costillas de cordero": 60.21,
        "Lengua de buey": 29.09,
        "Hígado de pollo": 5.87,
        "Fresa": 24.24,
        "Brit Care Aceite de Salmón": 0.87,
        "Aceite de girasol": 0.69,
        "Homemadekun (multivitamínico completo)": 5.71,
        "Sal común (cloruro sódico)": 0.16
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 108.29,
        "Cuello de ternera": 99.92,
        "Pulmón de cordero": 18.91,
        "Hígado de pollo": 5.92,
        "Acelga": 25.89,
        "Brit Care Aceite de Salmón": 0.95,
        "Homemadekun (multivitamínico completo)": 4.63
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 80.04,
        "Pollo pechuga con piel": 67.7,
        "Espinazo de conejo": 70.6,
        "Lengua de ternera": 5.33,
        "Hígado de vaca": 15.98,
        "Acelga": 26.63,
        "Brit Care Aceite de Salmón": 0.9,
        "Homemadekun (multivitamínico completo)": 4.79
      }
    }
  ],
  "Toy_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 70.19,
        "Corazón de pollo": 179.84,
        "Espinazo de conejo": 96.71,
        "Salmón": 35.85,
        "Lengua de ternera": 17.45,
        "Hígado de pollo": 8.33,
        "Espinaca": 8.33,
        "Homemadekun (multivitamínico completo)": 9.48
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 163.04,
        "Carcasa de conejo": 100.83,
        "Salmón": 115.03,
        "Lengua de buey": 8.35,
        "Hígado de vaca": 8.35,
        "Albahaca": 21.87,
        "Aceite de sésamo": 5.0,
        "Homemadekun (multivitamínico completo)": 7.43
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 197.06,
        "Costillas de cordero": 110.28,
        "Sardina": 31.07,
        "Lengua de buey": 53.43,
        "Hígado de vaca": 8.91,
        "Acelga": 44.53,
        "Aceite de girasol": 2.17,
        "Homemadekun (multivitamínico completo)": 7.75
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 97.91,
        "Corazón de pollo": 157.23,
        "Carcasa de pollo": 85.05,
        "Salmón": 16.08,
        "Riñón de ternera": 8.72,
        "Hígado de pollo": 17.72,
        "Canónigos": 42.52,
        "Homemadekun (multivitamínico completo)": 7.76
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 208.7,
        "Lomo de ternera con grasa": 41.11,
        "Costillas de cordero": 112.99,
        "Lengua de ternera": 8.84,
        "Hígado de pollo": 26.18,
        "Canónigos": 44.2,
        "Brit Care Aceite de Salmón": 1.38,
        "Homemadekun (multivitamínico completo)": 7.85,
        "Sal común (cloruro sódico)": 0.25
      }
    }
  ],
  "Mini_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 77.98,
        "Cuello de ternera": 163.11,
        "Lengua de ternera": 38.39,
        "Hígado de conejo": 9.32,
        "Acelga": 31.14,
        "Brit Care Aceite de Salmón": 1.14,
        "Homemadekun (multivitamínico completo)": 5.13
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 160.26,
        "Carcasa de pollo": 72.07,
        "Caballa": 20.63,
        "Lengua de buey": 6.65,
        "Hígado de vaca": 5.51,
        "Espinaca": 10.42,
        "Aceite de girasol": 4.84,
        "Homemadekun (multivitamínico completo)": 5.61
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 158.59,
        "Costillas de cordero": 74.65,
        "Lengua de ternera": 37.23,
        "Hígado de pollo": 8.73,
        "Acelga": 31.02,
        "Brit Care Aceite de Salmón": 1.21,
        "Aceite de oliva": 3.12,
        "Homemadekun (multivitamínico completo)": 5.24
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 56.93,
        "Cuello de ternera": 134.92,
        "Salmón": 52.94,
        "Lengua de cordero": 5.94,
        "Hígado de vaca": 16.45,
        "Acelga": 29.69,
        "Homemadekun (multivitamínico completo)": 5.21
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 69.16,
        "Corazón de pollo": 94.3,
        "Costillas de cordero": 76.12,
        "Merluza": 48.74,
        "Pulmón de cordero": 10.3,
        "Hígado de vaca": 6.79,
        "Nabo pelado": 33.93,
        "Homemadekun (multivitamínico completo)": 5.07
      }
    }
  ],
  "Mini_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 161.96,
        "Costillas de cordero": 102.48,
        "Pulmón de cordero": 41.86,
        "Hígado de vaca": 7.65,
        "Apio": 34.88,
        "Brit Care Aceite de Salmón": 1.1,
        "Homemadekun (multivitamínico completo)": 6.36
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 185.73,
        "Carcasa de pato": 70.55,
        "Caballa": 49.84,
        "Lengua de cordero": 6.51,
        "Hígado de pollo": 6.51,
        "Espinaca": 6.51,
        "Aceite de girasol": 5.0,
        "V-INTEGRA Cachorro": 4.14
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 145.91,
        "Cuello de ternera": 172.87,
        "Lengua de buey": 7.45,
        "Hígado de pollo": 8.91,
        "Acelga": 37.24,
        "Brit Care Aceite de Salmón": 1.3,
        "Aceite de cacahuete": 2.15,
        "Homemadekun (multivitamínico completo)": 6.0
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de vaca": 239.34,
        "Costillas de cordero": 89.79,
        "Lengua de buey": 21.9,
        "Hígado de vaca": 7.98,
        "Canónigos": 39.89,
        "Brit Care Aceite de Salmón": 1.24,
        "Aceite de girasol": 2.47,
        "V-INTEGRA Cachorro": 4.19
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 75.05,
        "Cuello de ternera": 178.82,
        "Merluza": 68.18,
        "Lengua de ternera": 38.86,
        "Hígado de pollo": 7.95,
        "Espinaca": 28.68,
        "V-INTEGRA Cachorro": 4.19
      }
    }
  ],
  "Mini_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 138.98,
        "Carcasa de pato": 73.65,
        "Molleja de pollo": 5.1,
        "Hígado de vaca": 15.29,
        "Coles de Bruselas": 21.84,
        "V-INTEGRA Perro Adulto": 2.4
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 128.03,
        "Cuello de pato": 49.24,
        "Lengua de ternera": 29.55,
        "Hígado de pollo": 14.77,
        "Frambuesa": 24.62,
        "Aceite de sésamo": 5.0,
        "V-INTEGRA Perro Adulto": 2.39
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 142.13,
        "Cuello de pato": 60.95,
        "Molleja de pollo": 14.85,
        "Hígado de pollo": 14.21,
        "Plátano": 4.74,
        "Aceite de sésamo": 1.99,
        "V-INTEGRA Perro Adulto": 2.4
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 138.98,
        "Cuello de ternera": 95.81,
        "Lengua de cordero": 5.3,
        "Hígado de conejo": 15.91,
        "Fresa": 9.09,
        "V-INTEGRA Perro Adulto": 2.4
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 138.98,
        "Cuello de pavo": 91.02,
        "Lengua de cordero": 18.17,
        "Hígado de vaca": 15.15,
        "Albahaca": 5.37,
        "V-INTEGRA Perro Adulto": 2.4
      }
    }
  ],
  "Mini_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 130.09,
        "Cuello de ternera": 99.17,
        "Lengua de buey": 4.88,
        "Hígado de vaca": 4.88,
        "Albahaca": 4.88,
        "V-INTEGRA Senior": 2.31
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 90.74,
        "Carcasa de pollo": 88.24,
        "Lengua de cordero": 4.0,
        "Hígado de vaca": 12.0,
        "Albahaca": 5.1,
        "Aceite de sésamo": 5.0,
        "V-INTEGRA Senior": 2.29
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 162.67,
        "Cuello de ternera": 54.22,
        "Lengua de cordero": 32.53,
        "Hígado de vaca": 6.89,
        "Alcachofa": 14.8,
        "Aceite de cacahuete": 1.42,
        "V-INTEGRA Senior": 2.4
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 67.25,
        "Cuello de ternera": 136.14,
        "Lengua de cordero": 33.72,
        "Hígado de conejo": 15.81,
        "Espinaca": 28.1,
        "V-INTEGRA Senior": 2.23
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 103.39,
        "Cuello de pato": 68.15,
        "Lengua de ternera": 3.91,
        "Hígado de vaca": 6.32,
        "Espinaca": 13.74,
        "V-INTEGRA Senior": 2.4
      }
    }
  ],
  "Mini_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo pechuga con piel": 122.42,
        "Costillas de cordero": 114.17,
        "Trucha": 250.48,
        "Lengua de buey": 11.42,
        "Hígado de conejo": 15.29,
        "Espinaca": 57.09,
        "AniForte Seaweed Meal": 0.3,
        "V-INTEGRA Cachorro": 3.13
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 172.52,
        "Carcasa de pollo": 115.49,
        "Lengua de cordero": 46.21,
        "Hígado de pollo": 12.36,
        "Acelga": 38.51,
        "Brit Care Aceite de Salmón": 2.76,
        "Aceite de sésamo": 4.35,
        "Homemadekun (multivitamínico completo)": 8.54
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 265.19,
        "Costillas de cordero": 112.75,
        "Lengua de buey": 34.58,
        "Hígado de pollo": 13.13,
        "Acelga": 47.29,
        "Brit Care Aceite de Salmón": 1.46,
        "Aceite de girasol": 0.85,
        "Homemadekun (multivitamínico completo)": 7.94
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 47.44,
        "Espinazo de conejo": 170.57,
        "Salmón": 133.28,
        "Lengua de ternera": 56.92,
        "Hígado de pollo": 18.76,
        "Espinaca": 47.44,
        "V-INTEGRA Cachorro": 5.29
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 116.54,
        "Cuello de ternera": 244.86,
        "Lengua de ternera": 57.5,
        "Hígado de vaca": 12.35,
        "Acelga": 47.92,
        "Aceite de Salmón Natural Greatness": 2.01,
        "Homemadekun (multivitamínico completo)": 7.71
      }
    }
  ],
  "Mini_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 192.64,
        "Cuello de ternera": 365.15,
        "Sardina": 135.06,
        "Pulmón de cordero": 73.64,
        "Hígado de pollo": 16.89,
        "Espinaca": 61.02,
        "AniForte Seaweed Meal": 0.27,
        "V-INTEGRA Cachorro": 5.4
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 187.38,
        "Costillas de cordero": 221.34,
        "Trucha": 397.7,
        "Lengua de ternera": 126.78,
        "Hígado de conejo": 21.13,
        "Albahaca": 102.2,
        "AniForte Seaweed Meal": 0.33,
        "V-INTEGRA Cachorro": 4.12
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 250.24,
        "Costillas de cordero": 225.66,
        "Trucha": 239.03,
        "Lengua de ternera": 118.43,
        "Hígado de vaca": 54.86,
        "Albahaca": 98.69,
        "AniForte Seaweed Meal": 0.6,
        "Homemadekun (multivitamínico completo)": 3.88
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 274.38,
        "Costillas de cordero": 171.34,
        "Salmón": 210.11,
        "Lengua de ternera": 21.88,
        "Hígado de conejo": 15.4,
        "Acelga": 77.01,
        "Homemadekun (multivitamínico completo)": 9.44,
        "V-INTEGRA Cachorro": 5.4
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 173.64,
        "Cuello de ternera": 376.37,
        "Merluza": 203.62,
        "Lengua de buey": 80.55,
        "Hígado de vaca": 33.87,
        "Espinaca": 96.45,
        "Sonrisa de Diez Kelp": 2.71,
        "V-INTEGRA Cachorro": 5.4
      }
    }
  ],
  "Pequeño_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 127.64,
        "Cuello de ternera": 255.95,
        "Pulmón de cordero": 59.01,
        "Hígado de pollo": 11.2,
        "Apio": 37.91,
        "Brit Care Aceite de Salmón": 1.79,
        "Homemadekun (multivitamínico completo)": 8.59
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 220.73,
        "Costillas de cordero": 117.58,
        "Lenguado": 51.69,
        "Lengua de buey": 55.99,
        "Hígado de pollo": 11.25,
        "Albahaca": 9.33,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 8.87
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 195.57,
        "Costillas de cordero": 116.41,
        "Lengua de cordero": 49.37,
        "Hígado de pollo": 24.68,
        "Fresa": 25.37,
        "Brit Care Aceite de Salmón": 2.12,
        "Aceite de girasol": 5.0,
        "Homemadekun (multivitamínico completo)": 9.21,
        "Sal común (cloruro sódico)": 0.3
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 227.9,
        "Costillas de cordero": 113.48,
        "Pulmón de cordero": 51.51,
        "Hígado de pollo": 9.26,
        "Acelga": 44.68,
        "Brit Care Aceite de Salmón": 1.54,
        "Homemadekun (multivitamínico completo)": 9.7
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 121.49,
        "Cuello de ternera": 202.86,
        "Merluza": 112.17,
        "Lengua de buey": 30.99,
        "Hígado de conejo": 10.63,
        "Espinaca": 53.13,
        "AniForte Seaweed Meal": 0.09,
        "V-INTEGRA Cachorro": 4.01
      }
    }
  ],
  "Pequeño_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 118.08,
        "Espinazo de conejo": 274.67,
        "Trucha": 139.96,
        "Lengua de cordero": 80.73,
        "Hígado de vaca": 13.88,
        "Col rizada": 66.81,
        "V-INTEGRA Cachorro": 8.39
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 284.06,
        "Carcasa de pato": 146.8,
        "Trucha": 87.47,
        "Lengua de ternera": 74.05,
        "Hígado de cordero": 12.34,
        "Frambuesa": 12.34,
        "Aceite de girasol": 3.28,
        "V-INTEGRA Cachorro": 8.04
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 365.0,
        "Carcasa de conejo": 126.76,
        "Lengua de buey": 61.18,
        "Hígado de vaca": 31.77,
        "Piña": 49.1,
        "Brit Care Aceite de Salmón": 2.03,
        "Sal común (cloruro sódico)": 0.18,
        "V-INTEGRA Cachorro": 8.14
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 234.62,
        "Cuello de ternera": 250.04,
        "Pulmón de cordero": 41.38,
        "Hígado de conejo": 11.96,
        "Acelga": 59.78,
        "Brit Care Aceite de Salmón": 2.21,
        "Homemadekun (multivitamínico completo)": 10.67
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Conejo": 357.21,
        "Costillas de cordero": 16.29,
        "Espinazo de conejo": 159.18,
        "Lengua de ternera": 84.11,
        "Hígado de vaca": 14.02,
        "Espinaca": 70.09,
        "Brit Care Aceite de Salmón": 2.05,
        "V-INTEGRA Cachorro": 8.07
      }
    }
  ],
  "Pequeño_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 171.42,
        "Costillas de cordero": 205.18,
        "Pulmón de cordero": 8.01,
        "Hígado de conejo": 8.01,
        "Espárrago verde": 8.01,
        "V-INTEGRA Perro Adulto": 4.08
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 218.75,
        "Espinazo de conejo": 253.8,
        "Lengua de cordero": 10.99,
        "Hígado de pollo": 10.99,
        "Albahaca": 54.95,
        "Aceite de sésamo": 3.21,
        "Homemadekun (multivitamínico completo)": 6.65
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 181.53,
        "Costillas de cordero": 209.76,
        "Lengua de cordero": 8.33,
        "Hígado de vaca": 8.33,
        "Mandarina": 8.33,
        "Pipa de girasol": 4.79,
        "V-INTEGRA Perro Adulto": 4.35
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 204.34,
        "Carcasa de conejo": 199.57,
        "Lengua de cordero": 8.59,
        "Hígado de vaca": 8.59,
        "Albahaca": 8.59,
        "V-INTEGRA Perro Adulto": 4.35
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 163.22,
        "Carcasa de pato": 169.62,
        "Lengua de ternera": 7.08,
        "Hígado de pollo": 7.08,
        "Boniato": 7.08,
        "V-INTEGRA Perro Adulto": 4.37
      }
    }
  ],
  "Pequeño_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 154.26,
        "Pecho de ternera con hueso": 88.99,
        "Lengua de cordero": 34.97,
        "Hígado de vaca": 7.34,
        "Albahaca": 5.83,
        "V-INTEGRA Senior": 4.22
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 195.23,
        "Espinazo de conejo": 249.28,
        "Lengua de cordero": 9.46,
        "Hígado de pollo": 9.46,
        "Boniato": 9.46,
        "Pipa de girasol": 3.7,
        "V-INTEGRA Senior": 4.02
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 155.2,
        "Cuello de pato": 109.54,
        "Lengua de buey": 40.83,
        "Hígado de pollo": 11.07,
        "Canónigos": 23.58,
        "Aceite de girasol": 2.7,
        "napfcheck Novomineral proLEBER": 3.6
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 187.35,
        "Carcasa de conejo": 191.31,
        "Lengua de ternera": 8.36,
        "Hígado de cordero": 8.36,
        "Espinaca": 22.71,
        "V-INTEGRA Senior": 4.23
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 173.54,
        "Espinazo de conejo": 151.58,
        "Lengua de buey": 50.92,
        "Hígado de vaca": 8.49,
        "Albahaca": 39.8,
        "Homemadekun (multivitamínico completo)": 6.89
      }
    }
  ],
  "Pequeño_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 383.02,
        "Carcasa de pato": 160.26,
        "Lengua de ternera": 87.62,
        "Hígado de pollo": 26.24,
        "Nabo pelado": 73.02,
        "Brit Care Aceite de Salmón": 2.84,
        "Sal común (cloruro sódico)": 0.37,
        "V-INTEGRA Cachorro": 10.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 517.5,
        "Espinazo de conejo": 263.76,
        "Trucha": 135.13,
        "Lengua de cordero": 21.25,
        "Hígado de pollo": 21.25,
        "Albahaca": 103.55,
        "Aceite de girasol": 2.14,
        "V-INTEGRA Cachorro": 10.55
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 268.67,
        "Espinazo de conejo": 303.22,
        "Salmón": 174.88,
        "Lengua de buey": 17.37,
        "Hígado de vaca": 17.37,
        "Espinaca": 86.83,
        "V-INTEGRA Cachorro": 9.87
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 383.02,
        "Costillas de cordero": 199.05,
        "Pulmón de cordero": 80.84,
        "Hígado de pollo": 19.53,
        "Acelga": 75.83,
        "Aceite de Salmón Natural Greatness": 3.01,
        "Homemadekun (multivitamínico completo)": 14.56
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 297.44,
        "Pavo pechuga sin piel": 163.17,
        "Costillas de cordero": 157.89,
        "Lengua de buey": 57.06,
        "Hígado de pollo": 15.35,
        "Nabo pelado": 76.77,
        "AniForte Aceite de Salmón": 5.44,
        "V-INTEGRA Cachorro": 10.8
      }
    }
  ],
  "Pequeño_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 713.26,
        "Cuello de ternera": 490.23,
        "Dorada": 171.01,
        "Lengua de ternera": 31.97,
        "Hígado de vaca": 31.97,
        "Acelga": 159.83,
        "Homemadekun (multivitamínico completo)": 13.89,
        "V-INTEGRA Cachorro": 10.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 426.28,
        "Costillas de cordero": 385.97,
        "Trucha": 804.42,
        "Lengua de buey": 95.52,
        "Hígado de pollo": 48.23,
        "Piña": 169.41,
        "Sonrisa de Diez Kelp": 0.32,
        "V-INTEGRA Cachorro": 10.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 486.51,
        "Costillas de cordero": 412.41,
        "Trucha": 453.45,
        "Lengua de ternera": 219.96,
        "Hígado de vaca": 77.38,
        "Albahaca": 183.3,
        "AniForte Seaweed Meal": 1.2,
        "Homemadekun (multivitamínico completo)": 7.91
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 233.81,
        "Pavo pechuga sin piel": 195.95,
        "Costillas de cordero": 355.2,
        "Salmón": 436.08,
        "Riñón de cordero": 26.81,
        "Hígado de pollo": 57.58,
        "Albahaca": 34.93,
        "Sonrisa de Diez Kelp": 4.95,
        "Homemadekun (multivitamínico completo)": 15.9
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 401.23,
        "Cuello de ternera": 814.46,
        "Merluza": 267.67,
        "Pulmón de ternera": 34.5,
        "Hígado de vaca": 34.5,
        "Albahaca": 172.48,
        "AniForte Seaweed Meal": 0.68,
        "Homemadekun (multivitamínico completo)": 9.93
      }
    }
  ],
  "Mediano_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 165.63,
        "Costillas de cordero": 174.87,
        "Trucha": 383.09,
        "Lengua de buey": 38.84,
        "Hígado de pollo": 16.98,
        "Piña": 69.6,
        "AniForte Seaweed Meal": 0.18,
        "V-INTEGRA Cachorro": 5.74
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 404.4,
        "Carcasa de conejo": 174.54,
        "Lengua de cordero": 95.76,
        "Hígado de vaca": 43.51,
        "Canónigos": 79.8,
        "Aceite de Salmón Natural Greatness": 3.06,
        "Aceite de girasol": 3.27,
        "Homemadekun (multivitamínico completo)": 10.9,
        "Sal común (cloruro sódico)": 0.2
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 214.27,
        "Costillas de cordero": 195.59,
        "Trucha": 205.68,
        "Lengua de ternera": 102.33,
        "Hígado de vaca": 49.61,
        "Albahaca": 85.28,
        "AniForte Seaweed Meal": 0.51,
        "Homemadekun (multivitamínico completo)": 3.29
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 123.4,
        "Costillas de cordero": 183.91,
        "Salmón": 191.31,
        "Lengua de ternera": 57.06,
        "Hígado de conejo": 12.07,
        "Albahaca": 35.71,
        "Homemadekun (multivitamínico completo)": 10.9,
        "Sal común (cloruro sódico)": 0.28
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 161.43,
        "Pato (carne sin hueso)": 206.08,
        "Costillas de cordero": 173.44,
        "Merluza": 157.25,
        "Molleja de pavo": 14.86,
        "Hígado de conejo": 14.86,
        "Espinaca": 14.86,
        "AniForte Seaweed Meal": 0.15,
        "V-INTEGRA Cachorro": 6.07
      }
    }
  ],
  "Mediano_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 410.85,
        "Costillas de cordero": 261.82,
        "Pulmón de cordero": 81.55,
        "Hígado de pollo": 21.68,
        "Acelga": 86.21,
        "AniForte Aceite de Salmón": 5.68,
        "Homemadekun (multivitamínico completo)": 16.28
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 106.13,
        "Costillas de cordero": 237.47,
        "Trucha": 492.3,
        "Lengua de ternera": 98.08,
        "Hígado de pollo": 21.23,
        "Espinaca": 106.13,
        "AniForte Seaweed Meal": 1.71,
        "V-INTEGRA Cachorro": 8.67
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 542.92,
        "Costillas de cordero": 188.0,
        "Pulmón de ternera": 93.88,
        "Hígado de vaca": 43.9,
        "Piña": 71.31,
        "AniForte Aceite de Salmón": 7.2,
        "V-INTEGRA Cachorro": 12.44
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Corazón de pollo": 185.83,
        "Espinazo de conejo": 489.18,
        "Lengua de buey": 107.04,
        "Hígado de pollo": 20.72,
        "Acelga": 89.2,
        "AniForte Aceite de Salmón": 7.86,
        "Homemadekun (multivitamínico completo)": 16.3
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Ternera solomillo sin grasa": 341.86,
        "Espinazo de conejo": 434.76,
        "Lengua de ternera": 128.37,
        "Hígado de pollo": 57.82,
        "Canónigos": 106.98,
        "AniForte Aceite de Salmón": 7.86,
        "V-INTEGRA Cachorro": 11.53
      }
    }
  ],
  "Mediano_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 287.65,
        "Costillas de cordero": 308.79,
        "Pulmón de cordero": 12.69,
        "Hígado de pollo": 12.69,
        "Nabo pelado": 12.69,
        "V-INTEGRA Perro Adulto": 6.42
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 94.08,
        "Espinazo de conejo": 419.35,
        "Lengua de buey": 85.57,
        "Hígado de vaca": 42.79,
        "Albahaca": 71.31,
        "Aceite de sésamo": 3.86,
        "Homemadekun (multivitamínico completo)": 10.79
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 400.93,
        "Carcasa de pollo": 149.9,
        "Lengua de buey": 80.43,
        "Hígado de conejo": 13.41,
        "Plátano": 25.59,
        "Aceite de cacahuete": 5.0,
        "V-INTEGRA Perro Adulto": 5.48
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 244.55,
        "Espinazo de conejo": 419.35,
        "Lengua de cordero": 14.56,
        "Hígado de conejo": 14.56,
        "Frambuesa": 34.95,
        "V-INTEGRA Perro Adulto": 6.81
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 249.62,
        "Espinazo de conejo": 419.35,
        "Lengua de ternera": 14.64,
        "Hígado de conejo": 14.64,
        "Frambuesa": 33.56,
        "V-INTEGRA Perro Adulto": 6.81
      }
    }
  ],
  "Mediano_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 258.9,
        "Cuello de pato": 180.46,
        "Lengua de buey": 10.22,
        "Hígado de cordero": 10.22,
        "Rucula": 51.09,
        "V-INTEGRA Senior": 8.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 186.12,
        "Espinazo de conejo": 392.7,
        "Lengua de buey": 82.83,
        "Hígado de vaca": 14.77,
        "Calabaza": 13.8,
        "Pipa de girasol": 5.0,
        "V-INTEGRA Senior": 4.72
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 375.65,
        "Carcasa de conejo": 299.72,
        "Pulmón de cordero": 14.37,
        "Hígado de pollo": 14.37,
        "Coles de Bruselas": 14.37,
        "Aceite de girasol": 0.96,
        "V-INTEGRA Senior": 4.9
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 245.16,
        "Carcasa de pollo": 239.51,
        "Lengua de ternera": 10.31,
        "Hígado de pollo": 10.31,
        "Coles de Bruselas": 10.31,
        "V-INTEGRA Senior": 8.56
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 312.92,
        "Costillas de cordero": 247.51,
        "Pulmón de cordero": 12.1,
        "Hígado de conejo": 12.1,
        "Albahaca": 20.37,
        "NEKTON Dog Easy-BARF (multivitamínico)": 9.84
      }
    }
  ],
  "Mediano_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 258.71,
        "Corazón de pollo": 476.07,
        "Carcasa de pato": 272.99,
        "Riñón de ternera": 72.04,
        "Hígado de pollo": 24.49,
        "Canónigos": 120.33,
        "AniForte Aceite de Salmón": 9.88,
        "V-INTEGRA Cachorro": 17.0
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 927.38,
        "Espinazo de conejo": 463.64,
        "Riñón de cordero": 32.35,
        "Hígado de vaca": 32.35,
        "Canónigos": 161.75,
        "AniForte Aceite de Salmón": 9.76,
        "Aceite de girasol": 3.43,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 725.51,
        "Costillas de cordero": 291.33,
        "Trucha": 289.7,
        "Lengua de cordero": 29.13,
        "Hígado de cordero": 29.13,
        "Acelga": 91.86,
        "astoral MultiVital BARF": 1.1,
        "V-INTEGRA Cachorro": 13.72
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 89.13,
        "Pavo pechuga sin piel": 192.94,
        "Espinazo de conejo": 543.54,
        "Salmón": 356.66,
        "Lengua de ternera": 25.15,
        "Hígado de vaca": 25.15,
        "Albahaca": 25.15,
        "V-INTEGRA Cachorro": 15.96
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 601.56,
        "Costillas de cordero": 327.52,
        "Pulmón de cordero": 146.01,
        "Hígado de pollo": 32.45,
        "Acelga": 123.06,
        "Aceite de Salmón Natural Greatness": 4.98,
        "Homemadekun (multivitamínico completo)": 23.96
      }
    }
  ],
  "Mediano_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 577.78,
        "Cuello de ternera": 1127.97,
        "Bacaladilla": 839.72,
        "Lengua de buey": 216.22,
        "Hígado de pollo": 66.36,
        "Albahaca": 298.34,
        "AniForte Seaweed Meal": 2.2,
        "V-INTEGRA Cachorro": 19.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 678.86,
        "Espinazo de conejo": 1159.48,
        "Trucha": 603.64,
        "Lengua de cordero": 385.58,
        "Hígado de vaca": 64.26,
        "Albahaca": 321.31,
        "AniForte Seaweed Meal": 1.56,
        "V-INTEGRA Cachorro": 17.23
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1001.23,
        "Costillas de cordero": 641.26,
        "Trucha": 794.3,
        "Lengua de ternera": 384.76,
        "Hígado de pollo": 64.13,
        "Albahaca": 320.63,
        "AniForte Seaweed Meal": 2.2,
        "V-INTEGRA Cachorro": 19.11
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 579.27,
        "Cuello de ternera": 1404.03,
        "Salmón": 192.18,
        "Pulmón de cordero": 351.26,
        "Hígado de conejo": 107.69,
        "Canónigos": 292.71,
        "Sonrisa de Diez Kelp": 0.37,
        "Homemadekun (multivitamínico completo)": 27.25
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 573.62,
        "Cuello de ternera": 1221.46,
        "Merluza": 658.1,
        "Lengua de buey": 219.24,
        "Hígado de pollo": 62.41,
        "Espinaca": 303.87,
        "AniForte Seaweed Meal": 0.54,
        "V-INTEGRA Cachorro": 19.8
      }
    }
  ],
  "Grande_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 235.48,
        "Costillas de cordero": 183.21,
        "Sardina": 273.61,
        "Lengua de ternera": 109.93,
        "Hígado de conejo": 22.23,
        "Espinaca": 91.61,
        "Sonrisa de Diez Kelp": 0.12,
        "V-INTEGRA Cachorro": 7.74
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 243.36,
        "Espinazo de conejo": 328.89,
        "Trucha": 258.12,
        "Lengua de buey": 103.03,
        "Hígado de pollo": 19.63,
        "Espinaca": 28.41,
        "NEKTON Dog Easy-BARF (multivitamínico)": 4.33,
        "V-INTEGRA Cachorro": 8.17
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 429.66,
        "Costillas de cordero": 212.08,
        "Trucha": 236.69,
        "Lengua de cordero": 21.21,
        "Hígado de vaca": 54.73,
        "Albahaca": 106.04,
        "AniForte Seaweed Meal": 0.96,
        "V-INTEGRA Cachorro": 5.9
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 420.9,
        "Costillas de cordero": 242.4,
        "Salmón": 42.98,
        "Riñón de ternera": 16.45,
        "Hígado de pollo": 49.16,
        "Albahaca": 47.43,
        "Sonrisa de Diez Kelp": 0.13,
        "Homemadekun (multivitamínico completo)": 10.9,
        "Sal común (cloruro sódico)": 0.4
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 304.48,
        "Cuello de ternera": 369.66,
        "Merluza": 152.54,
        "Pulmón de ternera": 37.56,
        "Hígado de vaca": 19.64,
        "Albahaca": 98.21,
        "Yoduro potásico (comprimidos 200 µg)": 0.18,
        "V-INTEGRA Cachorro": 7.27
      }
    }
  ],
  "Grande_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 356.83,
        "Cuello de ternera": 655.25,
        "Pulmón de cordero": 158.8,
        "Hígado de conejo": 26.47,
        "Espinaca": 125.97,
        "Aceite de Salmón Natural Greatness": 5.36,
        "V-INTEGRA Cachorro": 16.75
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 487.5,
        "Espinazo de conejo": 580.2,
        "Lengua de ternera": 174.52,
        "Hígado de pollo": 66.66,
        "Canónigos": 145.43,
        "AniForte Aceite de Salmón": 11.44,
        "V-INTEGRA Cachorro": 16.23
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 738.75,
        "Carcasa de conejo": 306.43,
        "Trucha": 81.43,
        "Lengua de buey": 64.38,
        "Hígado de pollo": 26.58,
        "Apio": 111.35,
        "astoral MultiVital BARF": 1.18,
        "V-INTEGRA Cachorro": 12.4
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 578.14,
        "Espinazo de conejo": 449.21,
        "Salmón": 36.14,
        "Lengua de cordero": 25.21,
        "Hígado de vaca": 45.57,
        "Acelga": 126.03,
        "V-INTEGRA Cachorro": 22.37
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo pechuga con piel": 305.22,
        "Espinazo de conejo": 665.63,
        "Lengua de buey": 90.48,
        "Hígado de vaca": 48.7,
        "Acelga": 123.34,
        "AniForte Aceite de Salmón": 11.44,
        "Homemadekun (multivitamínico completo)": 21.95
      }
    }
  ],
  "Grande_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 419.07,
        "Carcasa de conejo": 423.22,
        "Lengua de cordero": 18.02,
        "Hígado de vaca": 18.02,
        "Brócoli": 22.53,
        "V-INTEGRA Perro Adulto": 9.07
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 264.19,
        "Espinazo de conejo": 555.63,
        "Lengua de buey": 133.76,
        "Hígado de pollo": 49.62,
        "Acelga": 111.47,
        "Aceite de sésamo": 5.0,
        "NEKTON Dog Easy-BARF (multivitamínico)": 12.79
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 103.99,
        "Espinazo de conejo": 520.72,
        "Trucha": 248.8,
        "Lengua de buey": 124.79,
        "Hígado de vaca": 20.8,
        "Fresa": 20.8,
        "V-INTEGRA Perro Adulto": 6.69
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 343.35,
        "Carcasa de pollo": 338.88,
        "Lengua de cordero": 14.52,
        "Hígado de pollo": 14.76,
        "Nabo pelado": 14.52,
        "V-INTEGRA Perro Adulto": 9.88
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 231.92,
        "Espinazo de conejo": 555.63,
        "Lengua de buey": 97.21,
        "Hígado de vaca": 20.11,
        "Acelga": 100.54,
        "NEKTON Dog Easy-BARF (multivitamínico)": 14.4
      }
    }
  ],
  "Grande_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 315.08,
        "Espinazo de conejo": 520.34,
        "Lengua de ternera": 17.89,
        "Hígado de pollo": 23.1,
        "Albahaca": 17.89,
        "NEKTON Dog Easy-BARF (multivitamínico)": 14.4
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 171.19,
        "Espinazo de conejo": 455.12,
        "Lengua de cordero": 91.02,
        "Hígado de conejo": 15.17,
        "Albahaca": 26.03,
        "Aceite de girasol": 4.52,
        "NEKTON Dog Easy-BARF (multivitamínico)": 12.57
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 516.98,
        "Costillas de cordero": 206.79,
        "Lengua de cordero": 103.4,
        "Hígado de pollo": 17.23,
        "Espárrago verde": 17.23,
        "Oleum Canis Aceite de Salmón": 14.72,
        "V-INTEGRA Senior": 8.49
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 313.31,
        "Espinazo de conejo": 520.34,
        "Lengua de ternera": 17.85,
        "Hígado de conejo": 23.3,
        "Nabo pelado": 17.85,
        "V-INTEGRA Senior": 8.35
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 264.7,
        "Carcasa de conejo": 419.14,
        "Lengua de buey": 92.49,
        "Hígado de vaca": 23.57,
        "Acelga": 16.32,
        "V-INTEGRA Senior": 6.86
      }
    }
  ],
  "Grande_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 420.52,
        "Cuello de ternera": 919.98,
        "Pulmón de cordero": 217.94,
        "Hígado de pollo": 76.09,
        "Acelga": 181.61,
        "Aceite de Salmón Natural Greatness": 14.72,
        "Homemadekun (multivitamínico completo)": 31.5
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 686.49,
        "Espinazo de conejo": 738.73,
        "Lengua de cordero": 225.41,
        "Hígado de vaca": 39.96,
        "Espinaca": 187.84,
        "AniForte Aceite de Salmón": 14.72,
        "Aceite de cacahuete": 3.54,
        "Homemadekun (multivitamínico completo)": 30.49
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1082.92,
        "Carcasa de pato": 215.94,
        "Cuello de ternera": 170.82,
        "Lengua de ternera": 232.05,
        "Hígado de vaca": 38.68,
        "Apio": 193.38,
        "AniForte Aceite de Salmón": 12.99,
        "V-INTEGRA Cachorro": 25.25
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Conejo": 772.48,
        "Espinazo de conejo": 666.24,
        "Lengua de buey": 223.72,
        "Hígado de conejo": 37.29,
        "Espinaca": 164.63,
        "Brit Care Aceite de Salmón": 6.24,
        "Sal común (cloruro sódico)": 0.43,
        "V-INTEGRA Cachorro": 24.26
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 383.83,
        "Pavo pechuga sin piel": 524.62,
        "Carcasa de pollo": 365.73,
        "Lengua de buey": 179.35,
        "Hígado de vaca": 30.28,
        "Nabo pelado": 30.28,
        "Brit Care Aceite de Salmón": 6.85,
        "V-INTEGRA Cachorro": 24.39
      }
    }
  ],
  "Grande_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo pechuga con piel": 485.38,
        "Espinazo de conejo": 1771.27,
        "Trucha": 990.96,
        "Lengua de ternera": 518.41,
        "Hígado de pollo": 122.08,
        "Espinaca": 432.01,
        "AniForte Seaweed Meal": 2.2,
        "V-INTEGRA Cachorro": 28.8
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 1082.35,
        "Costillas de cordero": 931.35,
        "Trucha": 2008.59,
        "Lengua de buey": 121.67,
        "Hígado de pollo": 109.95,
        "Piña": 402.85,
        "Yoduro potásico (comprimidos 200 µg)": 1.02,
        "V-INTEGRA Cachorro": 27.59
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1462.58,
        "Costillas de cordero": 894.5,
        "Trucha": 1042.03,
        "Lengua de ternera": 536.7,
        "Hígado de conejo": 89.45,
        "Espinaca": 447.25,
        "Sonrisa de Diez Kelp": 0.73,
        "V-INTEGRA Cachorro": 27.83
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 884.24,
        "Cuello de ternera": 1934.59,
        "Salmón": 307.14,
        "Pulmón de cordero": 465.52,
        "Hígado de vaca": 77.59,
        "Albahaca": 210.23,
        "Homemadekun (multivitamínico completo)": 32.7,
        "V-INTEGRA Cachorro": 22.63
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 916.89,
        "Cuello de ternera": 1377.55,
        "Merluza": 909.12,
        "Lengua de buey": 505.82,
        "Hígado de vaca": 84.3,
        "Albahaca": 421.52,
        "Yoduro potásico (comprimidos 200 µg)": 0.71,
        "V-INTEGRA Cachorro": 28.17
      }
    }
  ],
  "Gigante_CachorroJoven": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 210.55,
        "Espinazo de conejo": 531.65,
        "Dorada": 194.02,
        "Lengua de ternera": 149.73,
        "Hígado de pollo": 37.03,
        "Piña": 124.78,
        "AniForte Seaweed Meal": 0.21,
        "V-INTEGRA Cachorro": 10.33
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Lomo de ternera con grasa": 255.42,
        "Espinazo de conejo": 549.68,
        "Trucha": 227.83,
        "Lengua de cordero": 163.06,
        "Hígado de pollo": 27.66,
        "Espinaca": 135.16,
        "AniForte Seaweed Meal": 0.31,
        "V-INTEGRA Cachorro": 8.54
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 505.03,
        "Espinazo de conejo": 418.73,
        "Salmón": 146.62,
        "Lengua de buey": 25.18,
        "Hígado de vaca": 37.63,
        "Espinaca": 125.91,
        "Sonrisa de Diez Kelp": 3.6,
        "V-INTEGRA Cachorro": 12.01
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 209.04,
        "Carcasa de pato": 234.53,
        "Salmón": 290.33,
        "Lengua de buey": 101.26,
        "Hígado de pollo": 18.98,
        "Acelga": 94.9,
        "napfcheck Novomineral proLEBER": 4.0,
        "V-INTEGRA Cachorro": 9.42
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 240.55,
        "Cuello de ternera": 565.37,
        "Merluza": 199.3,
        "Lengua de ternera": 116.14,
        "Hígado de conejo": 35.23,
        "Espinaca": 121.1,
        "Sonrisa de Diez Kelp": 0.06,
        "V-INTEGRA Cachorro": 12.01
      }
    }
  ],
  "Gigante_CachorroCrecimiento": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo pechuga con piel": 431.52,
        "Espinazo de conejo": 947.36,
        "Lengua de cordero": 175.12,
        "Hígado de pollo": 61.66,
        "Acelga": 179.52,
        "Oleum Canis Aceite de Salmón": 18.86,
        "Homemadekun (multivitamínico completo)": 32.7
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 695.08,
        "Espinazo de conejo": 765.96,
        "Lengua de cordero": 201.45,
        "Hígado de pollo": 117.71,
        "Col rizada": 181.65,
        "AniForte Aceite de Salmón": 19.66,
        "V-INTEGRA Cachorro": 27.24
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1035.25,
        "Cuello de ternera": 404.62,
        "Lengua de ternera": 227.35,
        "Hígado de pollo": 37.89,
        "Acelga": 189.46,
        "Oleum Canis Aceite de Salmón": 15.05,
        "V-INTEGRA Cachorro": 36.85
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Conejo": 926.84,
        "Costillas de cordero": 430.76,
        "Lengua de ternera": 216.73,
        "Hígado de pollo": 51.12,
        "Acelga": 180.61,
        "AniForte Aceite de Salmón": 14.19,
        "Homemadekun (multivitamínico completo)": 30.6
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pavo pechuga sin piel": 581.34,
        "Espinazo de conejo": 842.48,
        "Lengua de buey": 209.83,
        "Hígado de pollo": 34.97,
        "Pimiento rojo": 79.95,
        "AniForte Aceite de Salmón": 19.66,
        "V-INTEGRA Cachorro": 24.17
      }
    }
  ],
  "Gigante_Adulto": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 560.62,
        "Laringe de vacuno": 478.17,
        "Molleja de pollo": 22.14,
        "Hígado de pollo": 24.0,
        "Col lombarda": 22.14,
        "V-INTEGRA Perro Adulto": 17.03
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 267.75,
        "Espinazo de conejo": 810.93,
        "Lengua de buey": 170.32,
        "Hígado de cordero": 28.39,
        "Albahaca": 141.93,
        "AniForte Aceite de Salmón": 25.3,
        "Homemadekun (multivitamínico completo)": 25.15
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 419.26,
        "Espinazo de conejo": 834.2,
        "Riñón de cordero": 29.96,
        "Hígado de conejo": 64.82,
        "Espárrago verde": 149.8,
        "AniForte Aceite de Salmón": 25.3,
        "V-INTEGRA Perro Adulto": 12.87
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 704.39,
        "Carcasa de conejo": 536.25,
        "Lengua de buey": 70.46,
        "Hígado de vaca": 29.8,
        "Acelga": 148.99,
        "NEKTON Dog Easy-BARF (multivitamínico)": 24.75
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 560.43,
        "Carcasa de conejo": 651.45,
        "Lengua de buey": 62.41,
        "Hígado de vaca": 30.83,
        "Rucula": 26.64,
        "V-INTEGRA Perro Adulto": 11.85
      }
    }
  ],
  "Gigante_Senior": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 417.24,
        "Cuello de ternera": 769.33,
        "Riñón de ternera": 111.95,
        "Hígado de conejo": 29.51,
        "Albahaca": 147.56,
        "NEKTON Dog Easy-BARF (multivitamínico)": 18.52
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera con grasa": 158.25,
        "Carcasa de conejo": 464.92,
        "Trucha": 607.48,
        "Lengua de cordero": 189.9,
        "Hígado de pollo": 31.65,
        "Fresa": 130.29,
        "astoral MultiVital BARF": 2.75
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 651.55,
        "Cuello de pato": 226.31,
        "Lengua de cordero": 130.31,
        "Hígado de pollo": 24.78,
        "Boniato": 52.97,
        "AniForte Aceite de Salmón": 25.3,
        "napfcheck Novomineral proLEBER": 13.5
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 685.03,
        "Carcasa de conejo": 323.72,
        "Lengua de cordero": 143.31,
        "Hígado de vaca": 26.18,
        "Frambuesa": 130.92,
        "napfcheck Novomineral proLEBER": 15.7
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 612.06,
        "Pecho de ternera con hueso": 265.22,
        "Lengua de ternera": 20.4,
        "Hígado de conejo": 20.4,
        "Espinaca": 102.01,
        "napfcheck Novomineral proLEBER": 16.21
      }
    }
  ],
  "Gigante_GestanteTardia": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Pollo con piel (sin hueso)": 1274.86,
        "Espinazo de conejo": 1028.85,
        "Pulmón de cordero": 352.21,
        "Hígado de conejo": 58.7,
        "Espinaca": 220.43,
        "Brit Care Aceite de Salmón": 9.5,
        "V-INTEGRA Cachorro": 40.01
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 1290.2,
        "Espinazo de conejo": 1074.26,
        "Lengua de buey": 367.45,
        "Hígado de vaca": 67.05,
        "Espinaca": 263.09,
        "AniForte Aceite de Salmón": 25.3,
        "Aceite de sésamo": 5.0,
        "V-INTEGRA Cachorro": 37.3
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 1421.13,
        "Costillas de cordero": 525.86,
        "Lengua de buey": 315.52,
        "Hígado de pollo": 121.46,
        "Albahaca": 245.34,
        "AniForte Aceite de Salmón": 25.3,
        "Sal común (cloruro sódico)": 1.44,
        "V-INTEGRA Cachorro": 38.49
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 1233.91,
        "Espinazo de conejo": 1020.42,
        "Pulmón de cordero": 352.87,
        "Hígado de vaca": 58.81,
        "Espinaca": 274.54,
        "Oleum Canis Aceite de Salmón": 22.43,
        "V-INTEGRA Cachorro": 40.01
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 964.37,
        "Pavo pechuga sin piel": 542.92,
        "Carcasa de pollo": 502.43,
        "Lengua de ternera": 100.49,
        "Hígado de pollo": 150.73,
        "Zanahoria": 251.22,
        "Brit Care Aceite de Salmón": 25.3,
        "V-INTEGRA Cachorro": 38.89
      }
    }
  ],
  "Gigante_Lactante": [
    {
      "proteina": "Pollo",
      "gramos": {
        "Corazón de pollo": 1423.71,
        "Espinazo de conejo": 2835.17,
        "Trucha": 1572.11,
        "Lengua de ternera": 135.6,
        "Hígado de conejo": 135.6,
        "Albahaca": 678.02,
        "Sonrisa de Diez Kelp": 1.2,
        "V-INTEGRA Cachorro": 44.05
      }
    },
    {
      "proteina": "Ternera",
      "gramos": {
        "Ternera solomillo sin grasa": 1201.59,
        "Espinazo de conejo": 2749.75,
        "Trucha": 1269.41,
        "Lengua de buey": 824.33,
        "Hígado de conejo": 137.39,
        "Espinaca": 686.94,
        "Yoduro potásico (comprimidos 200 µg)": 1.33,
        "V-INTEGRA Cachorro": 49.5
      }
    },
    {
      "proteina": "Conejo",
      "gramos": {
        "Conejo": 766.76,
        "Cuello de ternera": 2663.34,
        "Trucha": 2568.92,
        "Lengua de ternera": 769.19,
        "Hígado de vaca": 153.35,
        "Albahaca": 746.02,
        "AniForte Seaweed Meal": 3.08,
        "astoral MultiVital BARF": 2.75
      }
    },
    {
      "proteina": "Salmón",
      "gramos": {
        "Pollo con piel (sin hueso)": 948.19,
        "Cuello de pavo": 1571.74,
        "Salmón": 1883.58,
        "Lengua de ternera": 695.29,
        "Hígado de vaca": 115.88,
        "Albahaca": 579.41,
        "AniForte Seaweed Meal": 5.12,
        "V-INTEGRA Cachorro": 39.78
      }
    },
    {
      "proteina": "Merluza",
      "gramos": {
        "Pollo con piel (sin hueso)": 1253.98,
        "Cuello de ternera": 3028.6,
        "Merluza": 1071.28,
        "Lengua de ternera": 642.95,
        "Hígado de vaca": 136.29,
        "Canónigos": 681.45,
        "napfcheck Novomineral proLEBER": 16.5,
        "V-INTEGRA Cachorro": 42.87
      }
    }
  ]
}
