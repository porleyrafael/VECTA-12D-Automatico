# correccion_simple.py
import os

# Leer el archivo
with open('auto_implementar_vecta.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Buscar y corregir la línea específica
corregido = False
for i, linea in enumerate(lineas):
    if 'file_path = self.base_dir / "vecta_ai_chat.py"' in linea:
        print(f"Línea {i+1} encontrada: {linea.rstrip()}")
        
        # Calcular indentación actual
        espacios = len(linea) - len(linea.lstrip())
        print(f"Espacios actuales: {espacios}")
        
        # Corregir a 8 espacios (4 para método + 4 para cuerpo)
        nueva_linea = ' ' * 8 + linea.lstrip()
        lineas[i] = nueva_linea
        corregido = True
        print(f"Corregido a 8 espacios: {nueva_linea.rstrip()}")
        break

# Guardar si hubo cambios
if corregido:
    with open('auto_implementar_vecta.py', 'w', encoding='utf-8') as f:
        f.writelines(lineas)
    print("\n✅ Archivo corregido")
else:
    print("\n⚠️ No se encontró la línea problemática")

# Verificar
print("\n🔍 Verificando indentación de método completo...")
en_metodo = False
for i, linea in enumerate(lineas):
    if 'def create_vecta_ai_chat(self):' in linea:
        en_metodo = True
        print(f"\nMétodo encontrado en línea {i+1}")
    elif en_metodo and 'def ' in linea:
        en_metodo = False
    
    if en_metodo and linea.strip():
        espacios = len(linea) - len(linea.lstrip())
        if espacios > 0 and espacios < 8:
            print(f"  Línea {i+1}: {espacios} espacios (mínimo 8)")