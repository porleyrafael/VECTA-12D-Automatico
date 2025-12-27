import zipfile 
import os 
 
print("?? VERIFICACI‡N DE VECTA 12D") 
print("="*50) 
 
zip_file = "VECTA_12D_Automatico.zip" 
 
print("1. Verificando ZIP...") 
if os.path.exists(zip_file): 
    size = os.path.getsize(zip_file) 
    print(f"   V ZIP existe: {size} bytes ({size/1024:.1f} KB)") 
else: 
    print(f"   ? ZIP no encontrado") 
 
print("2. Contenido del ZIP:") 
try: 
    with zipfile.ZipFile(zip_file, "r") as z: 
        files = z.namelist() 
        print(f"   V {len(files)} archivos encontrados:") 
        for file in files: 
            info = z.getinfo(file) 
            print(f"      {file} ({info.file_size} bytes)") 
except Exception as e: 
    print(f"   ? Error: {e}") 
 
print("3. Verificando archivos requeridos:") 
required = ["INSTAR.bat", "vecta_self_install.py", "vecta_12d_launcher.py", "paquete_vecta.pkg"] 
try: 
    with zipfile.ZipFile(zip_file, "r") as z: 
        zip_files = z.namelist() 
        for req in required: 
            if req in zip_files: 
                print(f"   V {req} - PRESENTE") 
            else: 
                print(f"   ? {req} - FALTANTE") 
except: 
    print("   ? No se pudo verificar") 
 
print("="*50) 
print("? VERIFICACI‡N COMPLETADA") 
print("\nPara instalar:") 
print("1. Extrae el ZIP") 
