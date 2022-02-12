#
#SCRIPT CREADO POR Edwin Saul Pareja @Saul11235
#
#Este script ordena todos los archivos del repositorio en un programa
#listo para ser ejecutado en una HP prime

from os import listdir,getcwd,path
#--------------------------------------------------------------------
#
# PORQUE UN ENGORROSO SCRIPT?!!!
# Porque este es un largo spaguetti en vez de un elegante repositorio?
# Porque busca ser portable y permitir el trabajo mas ordendo en un repositorio
# y no trabajar con el incomodo editor del Hp.connectivity.kit
#
#--------------------------------------------------------------------
#
#  1.- COMO USAR EL SCRIPT
#  ==========================
#  ejecutar este script en la raiz del repositorio que tenga el codigo 
#  de todas las funciones que se quiera ordenar
#  se creara una carpeta /GENER-HP-PRIME que tendra el procesamiento
#
#  2.- SOBRE LOS NOMBRES Y LAS EXTENSIONES DE LOS ARCHIVOS
#  ==========================================================
#
#  Nombre Inicio archivo:
#             NoCons-XXXXXX     no se considerara
#  Nombre Inicio carpeta
#             NoCons-XXXXXX     no se considerara 
#  
#  Los Archivos que comienzen con Run- tampoco se consderaran pues son
#  Scripts de ejecucion, en caso se quiera ejecutar una funcion automaticamente
#  Al momento de realizar el ordenamiento de los archivos
#
#  Todos los archivos con los siguientes nombres no se consideraran
#      README.md     .gitignore          .git       LICENSE 
#      pycache        GEN-HP-PRIME.py    icon.png   GENER-HP-PRIME
#
#  Todos los archivos con extension *.svg se renderiaran a *.png en su escala
#  por defecto (Sugerencia Editar dimensiones en pixeles usando inkscape)
#  
#  Si un archivo *.png tiene un nombre similar a ICON-XXXX.png sera convertido
#  a un icono identificado como "XXXX"
#
#  Todos los archivos *.jpg siempre se copian al procesamiento
#
#  Todos los archivos *.png siempre se copian al procesamiento si no son tipo ICON
#
#  3.-SCRIPTS DE EJECUCION
#  ========================
#  Se ejecutaran si y solo si comienzan con Run- y son de dominio *.py
#  es decir si su nombre es del tipo  "Run-XXXXX.py" 
#  no se consideraran como datos de procesamiento
#  
#  4.-ARCHIVOS QUE SI SE CONSIDERARAN EN EL PROCEDIMIENTO
#  ======================================================
#  Se asumira que todos los archivos  son de texto plano y parte del codigo excepto:
#        - Los archivos cuyo nombre que comienzen con NoCons- o Run-
#        - Los archivos con las extensones *.swg  *.jpg  *.png
#        - Los archivos cuyo nombre sea alguno descrito en el item 2
#  En UserRPL-no estan definidos por defecto la POO, por lo que la prigramacion sera funcional
#
#  Por defecto cada archivo describira una funcion, o podra declarar variables accesibles por 
#  todas las funciones del repositorio
# 
#  Si un archivo se llama XXXXXX.extension declarara una funcion llamada XXXXX accesible desde
#  cualquier otra funcion del repositorio   
#  para declarar sus argumentos de entrada debe de colocar como primera linea
#     ### Argumento1  Argumento2  Argumento3
#  
#  Para que dicha funcion sea una vista
#     ### VIEW
# 
#  Para que una funcion sea la primera en ser ejecutada
#     ### START
#  
#  Si se deja en blanco se asume que es una funcion sin argumentos   
#  Si hay varias funciones START solo la ultima sigue siendo START y las otras pasan a ser VIEW
#
#  Para declarar un archivo de solo declaracion de datos colocar en la primera linea
#     ##--
#
#
#--------------------------------------------------------------------
def TieneFinal (nombreArchivo,cadenaFinal):
    #Detecta el final de un nombre de archivo o el final de una extension
    if len(nombreArchivo)<len(cadenaFinal):
        return(False)
    else:
        reves=nombreArchivo[::-1]
        cadena=reves[0:len(cadenaFinal)]
        cadenareves=cadena[::-1]
        if cadenareves==cadenaFinal:return(True)
        else:return(False)
#-------------------------------------------------------------------
def TieneInicio(nombreArchivo,CadenaInicio):
    #Detecta el inicio de una cadena de texto 
    if len(nombreArchivo)<len(CadenaInicio):
        return(False)
    else:
        cadena=nombreArchivo[0:len(CadenaInicio)]
        if cadena==CadenaInicio:return(True)
        else:return(False)
#--------------------------------------------------------------------
def esNombreReservado(nombreArchivo):
    #verifica si esta el la lista de excepciones
    #valores a no tomar en cuenta
    ListaExcepciones=["README.md",".gitignore",".git", "LICENSE","pycache","GEN-HP-PRIME.py","icon.png","GENER-HP-PRIME"]
    try:
        ListaExcepciones.index(nombreArchivo)
        return True
    except:
        return False
#-------------------------------------------------------------------
def filtrarNombre(nombre):
    #devuelve True si es un nombre que se puede ingresar
    #devuelve False si no se debe ingresar al programa
    #cambiar la estension si se usa otro editor diferente a vim
    if TieneFinal(nombre,".swp") or esNombreReservado(nombre) or TieneInicio(nombre,"NoCons-"):
        return False #No incluir
    else:
        return True #si incluir
#-------------------------------------------------------------------
# Devuelve todos los archivos y subcarpetas de una carpeta
def contenidosCarpetas():
    listaNombres=[] #lista de nombres a considerar
    for x in listdir():
        if filtrarNombre(x):
            listaNombres.append(x)
    #separar los nombres
    return(listaNombres)
#--------------------------------------------------------------------
def obtenerSubcarpetas(): #devuelve nombre de subcarpetas
    listaNombres=contenidosCarpetas()
    listaResultados=[]
    for x in listaNombres:
        if path.isdir(x):
            listaResultados.append(x)
    return(listaResultados)    
#--------------------------------------------------------------------
def obtenerSubarchivos(): #devuelve el nombre de los subarchivos
    listaNombres=contenidosCarpetas()
    listaResultados=[]
    for x in listaNombres:
        if not(path.isdir(x)):
            listaResultados.append(x)
    return(listaResultados)            
#--------------------------------------------------------------------
def obtenerArchivosNoImagen(): #devuelve Archivos no imagen
    listaResultados=[]
    for x in obtenerSubarchivos():
        if TieneFinal(x,".jpg") or TieneFinal(x,".png") or TieneFinal(x,".svg") :
            pass #si tiene extension entonces no considerar
        else:
            listaResultados.append(x)
    return listaResultados            
#---------------------------------------------------------------------
# Modo terminal_________
if __name__=="__main__":
    #rutina comando
    print("\n>>> Generar Programa Para HpPrime")
    entrada=input("> enter para continuar otro valor para salir")
    if entrada=="":
        #Geprintnerar programa
        print(" Directorio Actual > "+getcwd() )
        print()
        print(obtenerSubcarpetas())
        print(obtenerSubarchivos())
        print(obtenerArchivosNoImagen())
        


