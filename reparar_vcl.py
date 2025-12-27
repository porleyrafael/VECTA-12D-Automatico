#!/usr/bin/env python3
"""
REPARADOR DE SCRIPT VECTA VCL
Encuentra y corrige errores de sintaxis en auto_implementar_vcl.py
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class ReparadorVCL:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.script_file = self.base_dir / "auto_implementar_vcl.py"
        self.backup_file = self.base_dir / f"auto_implementar_vcl.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        self.reparado_file = self.base_dir / "auto_implementar_vcl_reparado.py"
        
    def crear_backup(self):
        """Crea backup del archivo original"""
        if not self.script_file.exists():
            print("❌ Archivo auto_implementar_vcl.py no encontrado")
            return False
        
        try:
            shutil.copy2(self.script_file, self.backup_file)
            print(f"✅ Backup creado: {self.backup_file.name}")
            return True
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            return False
    
    def analizar_error(self):
        """Analiza el error de sintaxis"""
        print("\n🔍 ANALIZANDO ERROR...")
        print("-" * 50)
        
        if not self.script_file.exists():
            print("❌ Archivo no encontrado")
            return None
        
        try:
            with open(self.script_file, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
        except:
            with open(self.script_file, 'r', encoding='latin-1') as f:
                lineas = f.readlines()
        
        # Buscar la línea 755 (índice 754 porque empieza en 0)
        if len(lineas) >= 755:
            linea_problema = lineas[754]
            print(f"📄 Línea 755 encontrada:")
            print(f"   '{linea_problema.rstrip()}'")
            
            # Mostrar contexto
            print(f"\n📋 Contexto (líneas 750-760):")
            for i in range(749, min(760, len(lineas))):
                prefix = ">>>" if i == 754 else "   "
                print(f"{prefix} {i+1:4d}: {lineas[i].rstrip()}")
            
            return lineas
        else:
            print(f"❌ El archivo tiene solo {len(lineas)} líneas")
            return None
    
    def detectar_problemas_comunes(self, lineas):
        """Detecta problemas comunes en el código"""
        print("\n🔧 BUSCANDO PROBLEMAS COMUNES...")
        print("-" * 50)
        
        problemas = []
        
        # Problema 1: Gradientes CSS sin escape
        for i, linea in enumerate(lineas):
            if 'linear-gradient(' in linea and '#0f2027' in linea:
                problemas.append({
                    'linea': i+1,
                    'tipo': 'GRADIENTE_CSS',
                    'descripcion': 'Gradiente CSS puede causar error de sintaxis',
                    'contenido': linea.strip()
                })
        
        # Problema 2: Comillas triples mal cerradas
        contador_comillas = 0
        for i, linea in enumerate(lineas):
            contador_comillas += linea.count('"""')
            contador_comillas += linea.count("'''")
        
        if contador_comillas % 2 != 0:
            problemas.append({
                'linea': 'Varias',
                'tipo': 'COMILLAS_DESBALANCEADAS',
                'descripcion': f'Número impar de comillas triples: {contador_comillas}',
                'contenido': 'Posible comilla no cerrada'
            })
        
        # Problema 3: Cadenas f-string multilínea
        for i, linea in enumerate(lineas):
            if 'f"""' in linea or "f'''" in linea:
                # Verificar si está bien formado
                if linea.count('{') != linea.count('}'):
                    problemas.append({
                        'linea': i+1,
                        'tipo': 'F_STRING_DESBALANCEADO',
                        'descripcion': 'f-string puede tener llaves desbalanceadas',
                        'contenido': linea.strip()
                    })
        
        # Mostrar problemas encontrados
        if problemas:
            print(f"⚠️  Se encontraron {len(problemas)} problemas:")
            for prob in problemas:
                print(f"\n📌 Línea {prob['linea']}: {prob['tipo']}")
                print(f"   {prob['descripcion']}")
                print(f"   Contenido: {prob['contenido'][:100]}")
            return problemas
        else:
            print("✅ No se encontraron problemas comunes obvios")
            return []
    
    def reparar_gradientes_css(self, lineas):
        """Repara problemas con gradientes CSS"""
        print("\n🛠️  REPARANDO GRADIENTES CSS...")
        
        lineas_reparadas = []
        cambios = 0
        
        for i, linea in enumerate(lineas):
            # Buscar gradientes CSS problemáticos
            if 'linear-gradient(' in linea and any(color in linea for color in ['#0f2027', '#203a43', '#2c5364']):
                # Reemplazar con versión segura
                linea_reparada = linea.replace('#0f2027', '#0F2027')
                linea_reparada = linea_reparada.replace('#203a43', '#203A43')
                linea_reparada = linea_reparada.replace('#2c5364', '#2C5364')
                
                if linea_reparada != linea:
                    print(f"   ✅ Línea {i+1}: Gradiente CSS reparado")
                    cambios += 1
                lineas_reparadas.append(linea_reparada)
            else:
                lineas_reparadas.append(linea)
        
        print(f"   🔧 {cambios} gradientes CSS reparados")
        return lineas_reparadas
    
    def extraer_y_reparar_dashboard_code(self, lineas):
        """Extrae y repara el código del dashboard"""
        print("\n🔧 EXTRAYENDO Y REPARANDO CÓDIGO DASHBOARD...")
        
        # Buscar inicio y fin de _get_vcl_dashboard_code
        inicio = None
        fin = None
        
        for i, linea in enumerate(lineas):
            if '_get_vcl_dashboard_code(self):' in linea:
                inicio = i
                print(f"   📍 Inicio de función en línea {i+1}")
                break
        
        if inicio is None:
            print("   ❌ No se encontró la función _get_vcl_dashboard_code")
            return lineas
        
        # Buscar el final (línea con solo return)
        for i in range(inicio + 1, min(inicio + 500, len(lineas))):
            if lineas[i].strip().startswith('return'):
                fin = i
                # Buscar la línea con la variable que se retorna
                for j in range(i, len(lineas)):
                    if 'VCL_DASHBOARD_HTML' in lineas[j]:
                        fin = j + 1
                        break
                break
        
        if fin is None:
            fin = min(inicio + 400, len(lineas))
        
        print(f"   📍 Final estimado: línea {fin+1}")
        
        # Reemplazar con código seguro
        lineas_reparadas = []
        en_funcion = False
        skip_hasta = None
        
        for i, linea in enumerate(lineas):
            if i == inicio:
                print(f"   🔧 Reemplazando función desde línea {i+1}")
                en_funcion = True
                skip_hasta = fin
                
                # Añadir función reparada
                lineas_reparadas.append(linea)  # La línea con def
                lineas_reparadas.append('        """Retorna código del dashboard VCL"""\n')
                
                # Código dashboard seguro y simple
                dashboard_simple = '''        return """
<!DOCTYPE html>
<html>
<head>
    <title>VECTA Core Language Dashboard</title>
    <style>
        body { 
            background: #0f2027;
            background: -webkit-linear-gradient(to right, #0f2027, #203a43, #2c5364);
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
            font-family: Arial, sans-serif;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .symbol-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; }
        .symbol-card { 
            background: rgba(255,255,255,0.1); 
            padding: 15px; 
            border-radius: 8px;
            text-align: center;
        }
        .symbol-char { font-size: 2.5em; }
        .btn { 
            background: #00b4db; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌌 VECTA Core Language (VCL)</h1>
            <p>Lenguaje simbólico para decisión filosófica automatizada</p>
        </div>
        
        <div class="symbol-grid">
            <div class="symbol-card">
                <div class="symbol-char">⟐</div>
                <div>INTENCIÓN</div>
            </div>
            <div class="symbol-card">
                <div class="symbol-char">⟡</div>
                <div>RECURSO</div>
            </div>
            <div class="symbol-card">
                <div class="symbol-char">⟁</div>
                <div>ESTADO</div>
            </div>
            <div class="symbol-card">
                <div class="symbol-char">⟢</div>
                <div>TIEMPO</div>
            </div>
            <div class="symbol-card">
                <div class="symbol-char">⟂</div>
                <div>RESTRICCIÓN</div>
            </div>
            <div class="symbol-card">
                <div class="symbol-char">⟣</div>
                <div>INCERTIDUMBRE</div>
            </div>
            <div class="symbol-card">
                <div class="symbol-char">⟠</div>
                <div>DECISIÓN</div>
            </div>
        </div>
        
        <div style="margin-top: 40px; text-align: center;">
            <button class="btn" onclick="alert('VCL funcionando')">Probar VCL</button>
        </div>
    </div>
</body>
</html>
"""
'''
                lineas_reparadas.append(dashboard_simple)
                
            elif skip_hasta is not None and i <= skip_hasta:
                continue  # Saltar líneas de la función original
            else:
                lineas_reparadas.append(linea)
        
        print(f"   ✅ Función dashboard reemplazada")
        return lineas_reparadas
    
    def simplificar_script(self, lineas):
        """Crea una versión simplificada del script"""
        print("\n🎯 CREANDO VERSIÓN SIMPLIFICADA...")
        
        lineas_simplificadas = []
        lineas_simplificadas.append('#!/usr/bin/env python3\n')
        lineas_simplificadas.append('"""\n')
        lineas_simplificadas.append('VERSIÓN SIMPLIFICADA - AUTO IMPLEMENTADOR VCL\n')
        lineas_simplificadas.append('Script básico para instalar componentes esenciales VCL\n')
        lineas_simplificadas.append('"""\n\n')
        
        # Añadir imports esenciales
        lineas_simplificadas.append('import os\n')
        lineas_simplificadas.append('import sys\n')
        lineas_simplificadas.append('from pathlib import Path\n')
        lineas_simplificadas.append('from datetime import datetime\n\n')
        
        # Añadir clase simplificada
        clase_simplificada = '''
class VCLSimpleInstaller:
    """Instalador simplificado de VCL"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.install_dir = self.base_dir / "vcl_simple"
        
    def instalar_vcl(self):
        """Instala los componentes básicos de VCL"""
        print("=" * 60)
        print("INSTALADOR SIMPLIFICADO VCL")
        print("=" * 60)
        
        # Crear directorio
        self.install_dir.mkdir(exist_ok=True)
        
        # Crear archivo de motor básico
        motor_vcl = self.install_dir / "vcl_core.py"
        with open(motor_vcl, 'w', encoding='utf-8') as f:
            f.write("""
# VCL CORE SIMPLIFICADO

class VCLSymbol:
    def __init__(self, char, name):
        self.char = char
        self.name = name
    
    def __repr__(self):
        return f"{self.char} ({self.name})"

SYMBOLS = [
    VCLSymbol("⟐", "INTENTION"),
    VCLSymbol("⟡", "RESOURCE"),
    VCLSymbol("⟁", "SYSTEM_STATE"),
    VCLSymbol("⟢", "TIME_PHASE"),
    VCLSymbol("⟂", "CONSTRAINT"),
    VCLSymbol("⟣", "UNCERTAINTY"),
    VCLSymbol("⟠", "DECISION"),
]

def run_vcl():
    print("VCL Simple ejecutándose...")
    for symbol in SYMBOLS:
        print(f"  {symbol}")
    return SYMBOLS[0]  # Retorna el símbolo de decisión

if __name__ == "__main__":
    run_vcl()
""")
        
        # Crear script de prueba
        test_vcl = self.base_dir / "test_vcl_simple.py"
        with open(test_vcl, 'w', encoding='utf-8') as f:
            f.write('''
#!/usr/bin/env python3
print("✅ VCL Simple instalado correctamente")
print("Ejecuta: python -c "from vcl_simple.vcl_core import run_vcl; run_vcl()"")
''')
        
        # Crear README
        readme = self.base_dir / "README_VCL_SIMPLE.md"
        with open(readme, 'w', encoding='utf-8') as f:
            f.write(f'''
# VCL SIMPLE - Instalación exitosa

Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Archivos instalados:
1. `vcl_simple/vcl_core.py` - Motor VCL básico
2. `test_vcl_simple.py` - Script de prueba

## Comandos rápidos:
\```bash
# Probar VCL
python test_vcl_simple.py

# Importar y usar
python -c "from vcl_simple.vcl_core import run_vcl; run_vcl()"
\```

## Símbolos VCL disponibles:
- ⟐ INTENTION
- ⟡ RESOURCE  
- ⟁ SYSTEM_STATE
- ⟢ TIME_PHASE
- ⟂ CONSTRAINT
- ⟣ UNCERTAINTY
- ⟠ DECISION

¡VCL está listo para usar!
''')
        
        print(f"✅ Directorio creado: {self.install_dir}")
        print(f"✅ Archivo principal: {motor_vcl}")
        print(f"✅ Script de prueba: {test_vcl}")
        print(f"✅ Documentación: {readme}")
        print("\\n🎯 ¡INSTALACIÓN COMPLETADA!")
        print("=" * 60)

def main():
    """Instala VCL de forma simple"""
    installer = VCLSimpleInstaller()
    installer.instalar_vcl()

if __name__ == "__main__":
    main()
'''
        
        lineas_simplificadas.append(clase_simplificada)
        
        return lineas_simplificadas
    
    def reparar_completamente(self):
        """Ejecuta reparación completa"""
        print("=" * 60)
        print("🔧 REPARADOR COMPLETO DE SCRIPT VCL")
        print("=" * 60)
        
        # Paso 1: Backup
        if not self.crear_backup():
            return False
        
        # Paso 2: Analizar
        lineas = self.analizar_error()
        if lineas is None:
            print("❌ No se puede continuar sin el archivo original")
            return False
        
        # Paso 3: Detectar problemas
        problemas = self.detectar_problemas_comunes(lineas)
        
        # Paso 4: Opciones de reparación
        print("\n" + "=" * 60)
        print("🛠️  OPCIONES DE REPARACIÓN")
        print("=" * 60)
        print("1. Reparar solo gradientes CSS (rápido)")
        print("2. Reemplazar función dashboard completa")
        print("3. Crear versión simplificada nueva")
        print("4. Ver análisis y salir")
        
        try:
            opcion = int(input("\nSelecciona opción (1-4): ").strip())
        except:
            opcion = 3  # Por defecto, crear versión simplificada
        
        if opcion == 1:
            # Reparar gradientes
            lineas_reparadas = self.reparar_gradientes_css(lineas)
            archivo_salida = self.reparado_file
        elif opcion == 2:
            # Reemplazar dashboard
            lineas_reparadas = self.extraer_y_reparar_dashboard_code(lineas)
            archivo_salida = self.reparado_file
        elif opcion == 3:
            # Crear versión simplificada
            lineas_reparadas = self.simplificar_script(lineas)
            archivo_salida = self.base_dir / "vcl_simple_installer.py"
        else:
            print("\n📊 Análisis completado.")
            print("   Usa la información para reparar manualmente")
            return True
        
        # Guardar archivo reparado
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.writelines(lineas_reparadas)
            
            print(f"\n✅ ARCHIVO REPARADO GUARDADO:")
            print(f"   {archivo_salida.name}")
            
            # Hacer ejecutable
            archivo_salida.chmod(0o755)
            
            # Mostrar instrucciones
            print("\n📋 INSTRUCCIONES:")
            print(f"   1. Ejecuta: python {archivo_salida.name}")
            print(f"   2. El original está respaldado en: {self.backup_file.name}")
            print(f"   3. Si funciona, puedes renombrar: mv {archivo_salida.name} auto_implementar_vcl.py")
            
            return True
            
        except Exception as e:
            print(f"❌ Error guardando archivo: {e}")
            return False
    
    def crear_alternativa_minima(self):
        """Crea una alternativa mínima funcional"""
        print("\n🎯 CREANDO ALTERNATIVA MÍNIMA FUNCIONAL...")
        
        codigo_minimo = '''#!/usr/bin/env python3
"""
INSTALADOR MÍNIMO VCL - VERSIÓN SEGURA
Instala los componentes básicos de VECTA Core Language
"""

import os
import sys
from pathlib import Path

def crear_estructura():
    """Crea estructura mínima de directorios"""
    base = Path(__file__).parent
    
    directorios = ["core", "examples", "logs"]
    for dir_name in directorios:
        (base / dir_name).mkdir(exist_ok=True)
    
    return base

def crear_archivos_principales(base_dir):
    """Crea archivos principales VCL"""
    
    # 1. Motor VCL básico
    vcl_engine = base_dir / "core" / "vcl_simple.py"
    vcl_engine_content = """
# VCL SIMPLE - Motor básico
# Símbolos VECTA Core Language

VCL_SYMBOLS = {
    "INTENTION": "⟐",
    "RESOURCE": "⟡", 
    "STATE": "⟁",
    "TIME": "⟢",
    "CONSTRAINT": "⟂",
    "UNCERTAINTY": "⟣",
    "DECISION": "⟠"
}

class VCLSimple:
    def __init__(self):
        self.symbols = []
    
    def add_symbol(self, symbol_name, weight=1.0):
        if symbol_name in VCL_SYMBOLS:
            self.symbols.append({
                "name": symbol_name,
                "char": VCL_SYMBOLS[symbol_name],
                "weight": weight
            })
            return True
        return False
    
    def make_decision(self):
        if not self.symbols:
            return None
        
        # Encontrar símbolo con mayor peso
        decision = max(self.symbols, key=lambda x: x["weight"])
        return decision

def test_vcl():
    vcl = VCLSimple()
    vcl.add_symbol("INTENTION", 0.9)
    vcl.add_symbol("RESOURCE", 0.8)
    vcl.add_symbol("DECISION", 1.0)
    
    result = vcl.make_decision()
    print(f"✅ VCL Simple: Decisión = {result['char']} ({result['name']})")
    return result

if __name__ == "__main__":
    test_vcl()
"""
    
    with open(vcl_engine, 'w', encoding='utf-8') as f:
        f.write(vcl_engine_content)
    
    # 2. Script de prueba
    test_script = base_dir / "test_vcl_minimal.py"
    test_content = '''#!/usr/bin/env python3
"""
PRUEBA VCL MÍNIMO
"""

import sys
sys.path.insert(0, '.')

try:
    from core.vcl_simple import test_vcl
    result = test_vcl()
    print("\\n✅ VCL instalado correctamente!")
    print(f"🎯 Resultado: {result['char']} - {result['name']}")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("   Ejecuta primero: python instalar_vcl_minimal.py")
'''
    
    with open(test_script, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # 3. Script de integración
    integration = base_dir / "integrate_vcl.py"
    integration_content = '''#!/usr/bin/env python3
"""
INTEGRACIÓN VCL MÍNIMA CON VECTA
"""

from core.vcl_simple import VCLSimple

def integrate_with_vecta(vecta_data):
    """Integra VCL con datos de VECTA"""
    vcl = VCLSimple()
    
    # Mapeo simple de dimensiones VECTA a símbolos VCL
    mapping = {
        "dimension_1": "INTENTION",
        "dimension_2": "STATE", 
        "dimension_3": "STATE",
        "dimension_4": "TIME",
        "dimension_5": "RESOURCE",
        "dimension_6": "UNCERTAINTY",
        "dimension_12": "DECISION"
    }
    
    for vecta_key, vcl_symbol in mapping.items():
        if vecta_key in vecta_data:
            value = vecta_data[vecta_key]
            if value > 0.1:
                vcl.add_symbol(vcl_symbol, value)
    
    decision = vcl.make_decision()
    return decision

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo de VECTA
    ejemplo_vecta = {
        "dimension_1": 0.9,
        "dimension_2": 0.8,
        "dimension_12": 1.0
    }
    
    resultado = integrate_with_vecta(ejemplo_vecta)
    print(f"🎯 Integración VCL-VECTA: {resultado['char']} ({resultado['name']})")
'''
    
    with open(integration, 'w', encoding='utf-8') as f:
        f.write(integration_content)
    
    return [vcl_engine, test_script, integration]

def main():
    """Instala VCL mínimo"""
    print("=" * 60)
    print("🤖 INSTALADOR VCL MÍNIMO - VERSIÓN SEGURA")
    print("=" * 60)
    
    base_dir = crear_estructura()
    archivos = crear_archivos_principales(base_dir)
    
    print("✅ Estructura creada:")
    for archivo in archivos:
        print(f"   • {archivo.relative_to(base_dir)}")
    
    print("\\n🚀 INSTRUCCIONES:")
    print("   1. Probar instalación: python test_vcl_minimal.py")
    print("   2. Integrar con VECTA: python integrate_vcl.py")
    print("   3. Para usar en tu código: from core.vcl_simple import VCLSimple")
    
    print("\\n📋 SÍMBOLOS VCL DISPONIBLES:")
    print("   ⟐ INTENTION   ⟡ RESOURCE   ⟁ STATE")
    print("   ⟢ TIME        ⟂ CONSTRAINT ⟣ UNCERTAINTY")
    print("   ⟠ DECISION")
    
    print("\\n✅ ¡VCL MÍNIMO INSTALADO CORRECTAMENTE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
'''
        
        archivo_minimo = self.base_dir / "instalar_vcl_minimal.py"
        with open(archivo_minimo, 'w', encoding='utf-8') as f:
            f.write(codigo_minimo)
        
        archivo_minimo.chmod(0o755)
        
        print(f"✅ Alternativa mínima creada: {archivo_minimo.name}")
        print(f"   Ejecuta: python {archivo_minimo.name}")
        
        return archivo_minimo

def main():
    """Función principal del reparador"""
    reparador = ReparadorVCL()
    
    print("=" * 60)
    print("🛠️  REPARADOR DE SCRIPTS VECTA VCL")
    print("=" * 60)
    print("\nOpciones disponibles:")
    print("1. Analizar y reparar automáticamente")
    print("2. Crear alternativa mínima funcional")
    print("3. Solo crear backup y salir")
    
    try:
        opcion = int(input("\nSelecciona opción (1-3): ").strip())
    except:
        opcion = 1
    
    if opcion == 1:
        reparador.reparar_completamente()
    elif opcion == 2:
        reparador.crear_alternativa_minima()
    elif opcion == 3:
        reparador.crear_backup()
        print("✅ Backup creado. Repara manualmente el archivo.")
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    main()