# -*- coding: utf-8 -*-
import os
import shutil

def limpiar_lib_obsoleto():
    base_path = os.path.dirname(os.path.abspath(__file__))
    lib_path = os.path.join(base_path, 'lib')
    
    if not os.path.exists(lib_path):
        print("[ERROR] No se encuentra la carpeta 'lib'")
        return

    # LISTA DE LIBRERÍAS OBSOLETAS O INNECESARIAS EN PY3
    obsoletos = ['future', 'urllib3', 'chardet', 'six', 'requests']

    print("--- INICIANDO LIMPIEZA DE LIBRERÍAS (LIB) ---")
    
    eliminados = 0
    for folder in obsoletos:
        target = os.path.join(lib_path, folder)
        if os.path.exists(target):
            try:
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
                print("[ELIMINADO] Librería: %s" % folder)
                eliminados += 1
            except Exception as e:
                print("[ERROR] No se pudo eliminar %s: %s" % (folder, e))

    print("-" * 40)
    print("LIMPIEZA FINALIZADA. Se eliminaron %d elementos." % eliminados)

if __name__ == '__main__':
    limpiar_lib_obsoleto()