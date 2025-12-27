import zipfile
import os

# Archivos a incluir en el ZIP
files = [
    'INSTALAR.bat',
    'vecta_self_install.py', 
    'vecta_12d_launcher.py',
    'paquete_vecta.pkg'
]

zip_name = 'VECTA_12D_Automatico.zip'

print("Creando ZIP de VECTA 12D...")
print("-" * 40)

# Crear archivo ZIP
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in files:
        if os.path.exists(file):
            zipf.write(file)
            print(f'✓ Añadido: {file}')
        else:
            print(f'✗ No encontrado: {file}')

# Verificar
size = os.path.getsize(zip_name)
print("\n" + "=" * 40)
print(f'✅ ZIP creado: {zip_name}')
print(f'📦 Tamaño: {size} bytes = {size/1024/1024:.2f} MB')
print(f'📍 Ubicación: {os.path.abspath(zip_name)}')
print("=" * 40)
print("\n¡Listo! Este ZIP contiene VECTA 12D completo.")
print("Solo extrae y ejecuta INSTALAR.bat como administrador.")

# Verificar contenido
print("\nContenido del ZIP:")
with zipfile.ZipFile(zip_name, 'r') as zipf:
    for info in zipf.infolist():
        print(f'  • {info.filename} ({info.file_size} bytes)')