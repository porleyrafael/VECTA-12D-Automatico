python -c "
with open('vecta_launcher.py', 'r', encoding='utf-8') as f:
    contenido = f.read()
    
if 'elif opcion == \"7\":' in contenido and 'Salir' in contenido:
    print('OK: Opcion 7 es Salir')
else:
    print('ERROR: No se encontro opcion 7 para Salir')
    
if 'opcion == \"6\"' in contenido and 'META-VECTA' in contenido:
    print('OK: Opcion 6 es META-VECTA')
else:
    print('ADVERTENCIA: Opcion 6 puede no ser META-VECTA')
"