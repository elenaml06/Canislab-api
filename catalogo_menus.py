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
      "Pollo con piel (sin hueso)": 57.9,
      "Costillas de cordero": 44.12,
      "Pulpo": 31.49,
      "Molleja de pavo": 22.25,
      "Hígado de cordero": 11.13,
      "Albahaca": 18.54,
      "Homemadekun (multivitamínico completo)": 2.57
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
      "Pollo con piel (sin hueso)": 49.88,
      "Costillas de cordero": 53.72,
      "Salmón": 47.37,
      "Lengua de buey": 3.68,
      "Hígado de vaca": 11.05,
      "Acelga": 18.41,
      "Homemadekun (multivitamínico completo)": 3.76
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
      "Pollo con piel (sin hueso)": 56.12,
      "Carcasa de conejo": 74.97,
      "Lengua de buey": 18.73,
      "Hígado de pollo": 3.12,
      "Canónigos": 3.12,
      "V-INTEGRA Perro Adulto": 1.2
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
      "Pollo con piel (sin hueso)": 68.9,
      "Costillas de cordero": 56.4,
      "Lengua de buey": 8.32,
      "Hígado de pollo": 2.78,
      "Canónigos": 2.78,
      "V-INTEGRA Perro Adulto": 1.2
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
      "Pollo con piel (sin hueso)": 84.56,
      "Costillas de cordero": 64.48,
      "Pulpo": 45.96,
      "Molleja de pavo": 32.45,
      "Hígado de cordero": 16.15,
      "Albahaca": 26.83,
      "Homemadekun (multivitamínico completo)": 3.75
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
      "Pollo con piel (sin hueso)": 160.17,
      "Costillas de cordero": 114.67,
      "Sepia": 34.1,
      "Lengua de buey": 46.9,
      "Hígado de vaca": 7.82,
      "Albahaca": 27.2,
      "Homemadekun (multivitamínico completo)": 7.12
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Mini_CachorroJoven": {
    "tamano": "Mini",
    "etapa": "CachorroJoven",
    "peso_kg": 2.63,
    "der": 441,
    "gramos": {
      "Pollo con piel (sin hueso)": 109.2,
      "Costillas de cordero": 78.17,
      "Sepia": 23.25,
      "Lengua de buey": 31.98,
      "Hígado de vaca": 5.33,
      "Albahaca": 18.54,
      "Homemadekun (multivitamínico completo)": 4.85
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
      "Pollo con piel (sin hueso)": 90.16,
      "Carcasa de conejo": 73.28,
      "Salmón": 11.49,
      "Gamba roja": 91.32,
      "Lengua de cordero": 43.97,
      "Hígado de cordero": 21.98,
      "Albahaca": 34.19,
      "Homemadekun (multivitamínico completo)": 3.56
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
      "Pollo con piel (sin hueso)": 118.38,
      "Cuello de pato": 50.29,
      "Lengua de buey": 20.74,
      "Hígado de pollo": 3.95,
      "Albahaca": 3.95,
      "V-INTEGRA Perro Adulto": 2.4
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
      "Pollo con piel (sin hueso)": 130.06,
      "Carcasa de conejo": 66.28,
      "Lengua de cordero": 28.1,
      "Hígado de pollo": 5.02,
      "Nabo pelado": 4.68,
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
      "Pollo con piel (sin hueso)": 163.81,
      "Costillas de cordero": 117.27,
      "Sepia": 34.87,
      "Lengua de buey": 47.97,
      "Hígado de vaca": 7.99,
      "Albahaca": 27.81,
      "Homemadekun (multivitamínico completo)": 7.28
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
      "Pollo con piel (sin hueso)": 159.32,
      "Costillas de cordero": 168.73,
      "Salmón": 130.0,
      "Gamba roja": 234.33,
      "Lengua de buey": 16.87,
      "Hígado de cordero": 50.62,
      "Albahaca": 83.79,
      "Homemadekun (multivitamínico completo)": 7.39
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Pequeño_CachorroJoven": {
    "tamano": "Pequeño",
    "etapa": "CachorroJoven",
    "peso_kg": 4.6,
    "der": 692,
    "gramos": {
      "Pollo con piel (sin hueso)": 154.34,
      "Costillas de cordero": 117.62,
      "Pulpo": 83.95,
      "Molleja de pavo": 59.32,
      "Hígado de cordero": 29.66,
      "Albahaca": 49.43,
      "Homemadekun (multivitamínico completo)": 6.85
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
      "Pollo con piel (sin hueso)": 175.59,
      "Costillas de cordero": 175.48,
      "Pulpo": 113.53,
      "Molleja de pavo": 54.84,
      "Hígado de cordero": 37.1,
      "Albahaca": 61.84,
      "Homemadekun (multivitamínico completo)": 8.49
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
      "Pollo con piel (sin hueso)": 160.05,
      "Carcasa de pato": 169.67,
      "Lengua de buey": 7.29,
      "Hígado de cordero": 7.29,
      "Espinaca": 20.31,
      "V-INTEGRA Perro Adulto": 4.64
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
      "Pollo con piel (sin hueso)": 195.94,
      "Costillas de cordero": 153.58,
      "Lengua de cordero": 7.76,
      "Hígado de cordero": 7.76,
      "Espárrago verde": 23.06,
      "V-INTEGRA Perro Adulto": 4.2
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
      "Pollo con piel (sin hueso)": 201.06,
      "Costillas de cordero": 205.46,
      "Pulpo": 207.12,
      "Lengua de buey": 89.96,
      "Hígado de pollo": 14.99,
      "Albahaca": 31.09,
      "V-INTEGRA Perro Adulto": 4.8
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
      "Pollo con piel (sin hueso)": 300.92,
      "Costillas de cordero": 415.89,
      "Caballa": 121.24,
      "Gamba roja": 299.12,
      "Lengua de buey": 111.23,
      "Hígado de pollo": 89.17,
      "Canónigos": 148.62,
      "Homemadekun (multivitamínico completo)": 16.35
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
      "Pollo con piel (sin hueso)": 153.32,
      "Costillas de cordero": 188.34,
      "Gamba roja": 239.34,
      "Molleja de pavo": 81.77,
      "Hígado de pollo": 43.22,
      "Albahaca": 14.41,
      "Aceite de Salmón Natural Greatness": 3.45,
      "Homemadekun (multivitamínico completo)": 7.45
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
      "Pollo con piel (sin hueso)": 135.78,
      "Carcasa de pollo": 240.56,
      "Gamba roja": 203.53,
      "Lengua de buey": 82.84,
      "Hígado de cordero": 13.81,
      "Zanahoria": 13.81,
      "AniForte Aceite de Salmón": 7.86,
      "Homemadekun (multivitamínico completo)": 16.35
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
      "Pollo con piel (sin hueso)": 253.75,
      "Cuello de pato": 192.78,
      "Lengua de buey": 9.58,
      "Hígado de pollo": 13.47,
      "Plátano": 9.58,
      "V-INTEGRA Perro Adulto": 7.75
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
      "Pollo con piel (sin hueso)": 266.62,
      "Costillas de cordero": 309.56,
      "Lengua de buey": 12.26,
      "Hígado de pollo": 12.26,
      "Zanahoria": 12.26,
      "V-INTEGRA Perro Adulto": 6.02
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
      "Pollo con piel (sin hueso)": 426.88,
      "Costillas de cordero": 325.53,
      "Pulpo": 232.02,
      "Molleja de pavo": 163.83,
      "Hígado de cordero": 81.53,
      "Albahaca": 135.44,
      "Homemadekun (multivitamínico completo)": 18.92
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
      "Pollo con piel (sin hueso)": 656.04,
      "Costillas de cordero": 693.71,
      "Trucha": 132.09,
      "Gamba roja": 1140.87,
      "Molleja de pavo": 56.47,
      "Hígado de pollo": 56.47,
      "Albahaca": 87.73,
      "Homemadekun (multivitamínico completo)": 23.46
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
      "Lomo de ternera con grasa": 150.33,
      "Costillas de cordero": 247.01,
      "Trucha": 457.91,
      "Gamba roja": 103.07,
      "Lengua de buey": 67.85,
      "Hígado de pollo": 21.77,
      "Albahaca": 21.39,
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
      "Pollo con piel (sin hueso)": 288.2,
      "Costillas de cordero": 378.22,
      "Bacaladilla": 476.94,
      "Lengua de ternera": 166.23,
      "Hígado de conejo": 27.71,
      "Albahaca": 47.97,
      "V-INTEGRA Perro Adulto": 8.27
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
      "Pollo con piel (sin hueso)": 487.43,
      "Carcasa de conejo": 182.11,
      "Lengua de buey": 109.26,
      "Hígado de cordero": 54.63,
      "Albahaca": 77.11,
      "V-INTEGRA Perro Adulto": 7.83
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
      "Pollo con piel (sin hueso)": 407.45,
      "Costillas de cordero": 326.34,
      "Lengua de cordero": 15.74,
      "Hígado de cordero": 15.74,
      "Albahaca": 21.81,
      "V-INTEGRA Perro Adulto": 8.76
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
      "Pollo con piel (sin hueso)": 588.2,
      "Costillas de cordero": 455.61,
      "Pulpo": 396.45,
      "Lengua de buey": 205.75,
      "Hígado de pollo": 34.29,
      "Canónigos": 34.29,
      "V-INTEGRA Perro Adulto": 12.34
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
      "Pollo con piel (sin hueso)": 691.86,
      "Costillas de cordero": 810.22,
      "Trucha": 195.67,
      "Gamba roja": 1757.46,
      "Lengua de buey": 427.34,
      "Hígado de cordero": 81.02,
      "Albahaca": 87.55,
      "Homemadekun (multivitamínico completo)": 32.7
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
      "Pollo con piel (sin hueso)": 363.98,
      "Costillas de cordero": 277.62,
      "Pulpo": 197.95,
      "Molleja de pavo": 139.51,
      "Hígado de cordero": 69.93,
      "Albahaca": 116.55,
      "Homemadekun (multivitamínico completo)": 16.14
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  },
  "Gigante_CachorroCrecimiento": {
    "tamano": "Gigante",
    "etapa": "CachorroCrecimiento",
    "peso_kg": 42.73,
    "der": 2575,
    "gramos": {
      "Ternera solomillo sin grasa": 506.56,
      "Costillas de cordero": 517.14,
      "Trucha": 991.88,
      "Molleja de pavo": 42.88,
      "Hígado de pollo": 42.88,
      "Canónigos": 42.88,
      "V-INTEGRA Perro Adulto": 14.88
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
      "Pollo con piel (sin hueso)": 513.14,
      "Costillas de cordero": 607.24,
      "Lengua de cordero": 27.33,
      "Hígado de pollo": 81.98,
      "Canónigos": 136.63,
      "napfcheck Novomineral proLEBER": 16.5
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
      "Pollo con piel (sin hueso)": 582.34,
      "Carcasa de conejo": 591.0,
      "Lengua de cordero": 25.85,
      "Hígado de cordero": 25.85,
      "Col rizada": 67.59,
      "V-INTEGRA Perro Adulto": 13.14
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
      "Conejo": 1122.96,
      "Carcasa de conejo": 619.96,
      "Salmón": 592.87,
      "Lengua de ternera": 371.97,
      "Hígado de pollo": 82.05,
      "Albahaca": 309.98,
      "V-INTEGRA Perro Adulto": 21.36
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
      "Pollo con piel (sin hueso)": 740.38,
      "Costillas de cordero": 1587.76,
      "Trucha": 1888.23,
      "Gamba roja": 1410.56,
      "Lengua de ternera": 888.46,
      "Hígado de pollo": 148.08,
      "Albahaca": 740.38,
      "V-INTEGRA Perro Adulto": 21.94
    },
    "semaforo": "verde",
    "correctos": 30,
    "total": 30
  }
}
