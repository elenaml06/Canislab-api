"""Mismo presupuesto, dos reparto: 40 % por intento contra un tercio.

Se aprieta el presupuesto a mano para imitar lo lento que va Render, que es
como lo hace el BLOQUE 43 -- lo que se compara son las DOS columnas entre si,
no los segundos contra un reloj de pared.
"""
import main as api
from main import PeticionMenu

CASOS = [
 ("toy 1,5 kg", dict(der_objetivo=200.0, etapa_requisitos="Adulto", peso_perro_kg=1.5)),
 ("cachorro grande 31", dict(der_objetivo=1581.0, etapa_requisitos="CachorroCrecimiento",
                             peso_perro_kg=20.0, peso_adulto_esperado_kg=31.0, tamano="Mediano")),
 ("Cairo 10 % premios", dict(der_objetivo=1581.0, etapa_requisitos="CachorroCrecimiento",
                             peso_perro_kg=20.0, peso_adulto_esperado_kg=31.0, tamano="Mediano",
                             premios_nivel="hasta_el_maximo")),
]
N = 5
for presu in (14.0, 20.0, 28.0):
    for frac, etq_f in ((0.4, "40 %"), (1.0/3.0, "1/3 ")):
        api.FRACCION_DE_UN_INTENTO = frac
        for etq, extra in CASOS:
            con = 0
            for _ in range(N):
                d = PeticionMenu(nombres_alimentos=[], modo="automatico",
                                 presupuesto_segundos=presu, **extra)
                r = api._resolver_menu_v2_interno(d)
                con += bool(r.get("factible"))
            print(f"  presupuesto {presu:4.0f}s  reparto {etq_f}  {etq:20s} {con}/{N} con menu", flush=True)
print("FIN", flush=True)
