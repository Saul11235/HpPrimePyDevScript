#
#SCRIPT CREADO POR Edwin Saul Pareja @Saul11235
#
#Este script ordena todos los archivos del repositorio en un programa
#listo para ser ejecutado en una HP prime

from os import listdir,getcwd,path,system,chdir
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
#
# VARIABLES DE USO PARA ORGANIZAR LA INFORMACION
#
#---------------------------------------------------------------------
#direcciones de los archivos considerados
DireccionesVariables=[] #lista con direcciones de archivos de variables
DireccionesFunciones=[] #lista con direcciones de archivos de funciones
DireccionesVistas=[]    #lista con direcciones de archivos de vistas
PosicionVistaStart=0    #posicion respecto a DireccionesVistas
HayVistaStart=False     #hay vista de inicio
DireccionesIconos=[]    #lista con direcciones de Iconos
NombresIconos=[]        #lista con los nombres de los iconos
DireccionesImagenes=[]  #lista con direcciones de imagenes
NombresImagenes=[]      #nombre de las imagenes importadas
#----------------------------------------------------------------------
#variables que solo consideraran 
ArgumentosFunciones=[]  #argumentos fun(Arg1,Arg2,Arg3)
CodigoFunciones=[]      #codigo original de los achivos
CodigoVariables=[]      #codigo original
CodigoVistas=[]         #codigo original
CodigoIconos=[]         #cofigo generado algoritmo
#----------------------------------------------------------------------
#Lineas generadas del programa generado


#---------------------------------------------------------------------
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
def CortarCadenaInicio(CadenaOriginal,Cuanto): #corta un string
    cortar=Cuanto
    if type(Cuanto)==str:
        cortar=len(Cuanto)
    longitud=len(CadenaOriginal)
    return (CadenaOriginal[cortar:longitud])
#--------------------------------------------------------------------
def CortarCadenaFinal(CadenaOriginal,Cuanto): #corta un string
    cortar=Cuanto
    if type(Cuanto)==str:
        cortar=len(Cuanto)
    longitud=len(CadenaOriginal)
    return (CadenaOriginal[0:longitud-cortar])
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
#---------------------------------------------------------------------
def obtenerSVG(): #Devuelve archivos svg para ser renderizados
    listaResultados=[]
    listaSubarchivos=obtenerSubarchivos()
    for x in listaSubarchivos:
        if TieneFinal(x,".svg"):
            NombrePNG=CortarCadenaFinal(x,"svg")+"png"
            try:
                listaSubarchivos.index(NombrePNG)
            except:    
                listaResultados.append(x)
    return listaResultados            
#---------------------------------------------------------------------
def obtenerParaICON(): #Devuelve los archivos par ser ICON
    listaResultados=[]
    for x in obtenerSubarchivos():
        if TieneFinal(x,".png") and TieneInicio(x,"ICON-"):
            listaResultados.append(x)
    return listaResultados            
#---------------------------------------------------------------------
def obtenerImagenesParaImportar(): #devuelve imagenes para importar
    listaResultados=[]
    for x in obtenerSubarchivos():
        if not(TieneInicio(x,"ICON-")) and (TieneFinal(x,".png") or TieneFinal(x,"jpg")):
            listaResultados.append(x)
    return listaResultados            
#---------------------------------------------------------------------
def obtenerScriptsRun(): #Devuelve los scripts para ejecutar al momento de considerar
    listaResultados=[]
    for x in obtenerSubarchivos():
        if TieneInicio(x,"Run-") and TieneFinal(x,".py"):
            listaResultados.append(x)
    return listaResultados            
#---------------------------------------------------------------------
def obtenerArchivosParaConsiderar(): #Devuelve los scripts para devolver archivos a considerar
    listaResultados=[]
    for x in obtenerSubarchivos():
        if not(TieneInicio(x,"Run-")) and not(TieneInicio(x,"ICON-")) and not(TieneFinal(x,".svg")) and not(TieneFinal(x,".png")) and not(TieneFinal(x,".jpg")):
            listaResultados.append(x)
    return listaResultados
#---------------------------------------------------------------------
def CifradoICON(origen):
    #cifra contenido y devuelve el contenido en formato ICON
    return "xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo "
#---------------------------------------------------------------------
def ObtenerRutaCompleta(archivo):
    #entregar nombre con nombre completo de ruta
    return getcwd()+"\\"+archivo
#---------------------------------------------------------------------
def RegistrarIcono(nombreicono):
    #DireccionesIconos=[] #lista con direcciones de Iconos
    #NombresIconos=[]     #lista con los nombres de los iconos
    #CodigoIconos=[]         #cofigo generado algoritmo
    #registra un icono en la "BD" del script
    DireccionesIconos.append(ObtenerRutaCompleta(nombreicono))
    NombresIconos.append(CortarCadenaFinal(CortarCadenaInicio(nombreicono,"ICON-"),".png"))
    CodigoIconos.append(CifradoICON(nombreicono))
#---------------------------------------------------------------------
def RegistrarImagen(nombreimagen):
    #direcciones de los archivos considerados
    #DireccionesImagenes=[]#lista con direcciones de imagenes
    #NombresImagenes=[] #nombres de los archivos para importar
    DireccionesImagenes.append(ObtenerRutaCompleta(nombreimagen))
    NombresImagenes.append(nombreimagen)
#---------------------------------------------------------------------
def RegistrarCodigo(nombreArchivo):
    #direcciones de los archivos considerados
    #DireccionesVariables=[] #lista con dirs de variables
    #DireccionesFunciones=[] #lista con dirs de funciones
    #DireccionesVistas=[]    #lista con dirs de vistas
    #PosicionVistaStart=0    #posicion resp DireccionesVistas
    #HayVistaStart=False     #hay vista de inicio
    #ArgumentosFunciones=[]  #argumentos fun(Arg1,Arg2,Arg3)
    #CodigoFunciones=[]      #codigo original de los achivos
    #CodigoVariables=[]      #codigo original
    #CodigoVistas=[]         #codigo original
    pass
#---------------------------------------------------------------------
def CicloRegistroArchivos(): #registra los archivos en el repositorio actual
    #paso 1. ejecutar todos los archivos Run- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
    for x in obtenerScriptsRun():
        print("   >> Ejecutar: "+str(x))
        codigo="" # <-- codigo del script
        archivo=open(x,"r")
        for y in archivo.readlines():
            codigo=codigo+str(y)
        exec(codigo)
    #Paso 2.-convertir todos los archivos svg en png XXXXXXXXXXXXXXXXXXXXXXXXX        
    for x in obtenerSVG():
        print("   >> renderizar SVG: "+str(x))
        system('inkscape --export-type="png" "'+str(x)+'"')
    #Paso 3.- convierte en condigo de ICON XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    for x in obtenerParaICON():
        print("   >> Generar ICON: "+str(x))
        RegistrarIcono(x)
    #Paso 4.- importar imagen XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
    for x in obtenerImagenesParaImportar():
        print("   >> Importar imagen: "+str(x))
        RegistrarImagen(x)
    #Paso 5.- ingresar archivos de codigo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        
    for x in obtenerArchivosParaConsiderar():
        print("   >> Archivo parar considerar: "+str(x))
    #Paso 6.- ingresar a subcarpetas XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    for x in obtenerSubcarpetas():
        print("\n >>> Entrando a subcarpetas: "+str(x))
        chdir(x)
        CicloRegistroArchivos()
        chdir("..")
# Modo terminal_________
if __name__=="__main__":
    #rutina comando
    print("\n>>> Generar Programa Para HpPrime")
    entrada=input("> enter para continuar otro valor para salir")
    if entrada=="":
        #Geprintnerar programa
        print(" Directorio Actual > "+getcwd() )
        CicloRegistroArchivos()

