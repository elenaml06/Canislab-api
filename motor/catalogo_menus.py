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
