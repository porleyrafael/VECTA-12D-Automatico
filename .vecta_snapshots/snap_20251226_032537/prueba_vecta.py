import sys 
import os 
sys.path.insert(0, ".") 
print("Probando VECTA 12D...") 
try: 
    from core.vecta_12d_core import VECTA_12D_Core 
    v = VECTA_12D_Core() 
    print("? Sistema cargado") 
    res = v.procesar("Hola mundo") 
    if res["exito"]: 
        print(f"? Vector creado - Magnitud: {res['magnitud']:.4f}") 
    else: 
        print(f"? Error: {res.get('error')}") 
except Exception as e: 
    print(f"? Error: {e}") 
