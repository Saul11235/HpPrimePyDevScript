#
#SCRIPT CREADO POR Edwin Saul Pareja @Saul11235
#
#Este script ordena todos los archivos del repositorio en un programa
#listo para ser ejecutado en una HP prime

from os import listdir,getcwd,path,system,chdir
from platform import system as platsys
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
class ClaseAnalisis:
    def __init__(self):
        self.__VaciarMemoria()
        #direcciones de los archivos considerados
    def __VaciarMemoria(self):    
        self.__DireccionesVariables=[] #lista con direcciones de archivos de variables
        self.__DireccionesFunciones=[] #lista con direcciones de archivos de funciones
        self.__DireccionesVistas=[]    #lista con direcciones de archivos de vistas
        self.__PosicionVistaStart=0    #posicion respecto a DireccionesVistas
        self.__HayVistaStart=False     #hay vista de inicio
        self.__DireccionesIconos=[]    #lista con direcciones de Iconos
        self.__NombresIconos=[]        #lista con los nombres de los iconos
        self.__DireccionesImagenes=[]  #lista con direcciones de imagenes
        self.__NombresImagenes=[]      #nombre de las imagenes importadas
        #----------------------------------------------------------------------
        #variables que solo consideraran 
        self.__ArgumentosFunciones=[]  #argumentos fun(Arg1,Arg2,Arg3)
        self.__CodigoFunciones=[]      #codigo original de los achivos
        self.__CodigoVariables=[]      #codigo original
        self.__CodigoVistas=[]         #codigo original
        self.__CodigoIconos=[]         #cofigo generado algoritmo

    #---------------------------------------------------------------------
    def __TieneFinal (self,nombreArchivo,cadenaFinal):
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
    def __TieneInicio(self,nombreArchivo,CadenaInicio):
        #Detecta el inicio de una cadena de texto 
        if len(nombreArchivo)<len(CadenaInicio):
            return(False)
        else:
            cadena=nombreArchivo[0:len(CadenaInicio)]
            if cadena==CadenaInicio:return(True)
            else:return(False)
    #--------------------------------------------------------------------
    def __CortarCadenaInicio(self,CadenaOriginal,Cuanto): #corta un string
        cortar=Cuanto
        if type(Cuanto)==str:
            cortar=len(Cuanto)
        longitud=len(CadenaOriginal)
        return (CadenaOriginal[cortar:longitud])
    #--------------------------------------------------------------------
    def __CortarCadenaFinal(self,CadenaOriginal,Cuanto): #corta un string
        cortar=Cuanto
        if type(Cuanto)==str:
            cortar=len(Cuanto)
        longitud=len(CadenaOriginal)
        return (CadenaOriginal[0:longitud-cortar])
    #--------------------------------------------------------------------
    def __esNombreReservado(self,nombreArchivo):
        #verifica si esta el la lista de excepciones
        #valores a no tomar en cuenta
        ListaExcepciones=["README.md",".gitignore",".git", "LICENSE","pycache","GEN-HP-PRIME.py","icon.png","GENER-HP-PRIME"]
        try:
            ListaExcepciones.index(nombreArchivo)
            return True
        except:
            return False
    #-------------------------------------------------------------------
    def __filtrarNombre(self,nombre):
        #devuelve True si es un nombre que se puede ingresar
        #devuelve False si no se debe ingresar al programa
        #cambiar la estension si se usa otro editor diferente a vim
        if self.__TieneFinal(nombre,".swp") or self.__esNombreReservado(nombre) or self.__TieneInicio(nombre,"NoCons-"):
            return False #No incluir
        else:
            return True #si incluir
    #-------------------------------------------------------------------
    # Devuelve todos los archivos y subcarpetas de una carpeta
    def __contenidosCarpetas(self):
        listaNombres=[] #lista de nombres a considerar
        for x in listdir():
            if self.__filtrarNombre(x):
                listaNombres.append(x)
        #separar los nombres
        return(listaNombres)
    #--------------------------------------------------------------------
    def __obtenerSubcarpetas(self): #devuelve nombre de subcarpetas
        listaNombres=self.__contenidosCarpetas()
        listaResultados=[]
        for x in listaNombres:
            if path.isdir(x):
                listaResultados.append(x)
        return(listaResultados)    
    #--------------------------------------------------------------------
    def __obtenerSubarchivos(self): #devuelve el nombre de los subarchivos
        listaNombres=self.__contenidosCarpetas()
        listaResultados=[]
        for x in listaNombres:
            if not(path.isdir(x)):
                listaResultados.append(x)
        return(listaResultados)            
    #---------------------------------------------------------------------
    def __obtenerSVG(self): #Devuelve archivos svg para ser renderizados
        listaResultados=[]
        listaSubarchivos=self.__obtenerSubarchivos()
        for x in listaSubarchivos:
            if self.__TieneFinal(x,".svg"):
                NombrePNG=self.__CortarCadenaFinal(x,"svg")+"png"
                try:
                    listaSubarchivos.index(NombrePNG)
                except:    
                    listaResultados.append(x)
        return listaResultados            
    #---------------------------------------------------------------------
    def __obtenerParaICON(self): #Devuelve los archivos par ser ICON
        listaResultados=[]
        for x in self.__obtenerSubarchivos():
            if self.__TieneFinal(x,".png") and self.__TieneInicio(x,"ICON-"):
                listaResultados.append(x)
        return listaResultados            
    #---------------------------------------------------------------------
    def __obtenerImagenesParaImportar(self): #devuelve imagenes para importar
        listaResultados=[]
        for x in self.__obtenerSubarchivos():
            if not(self.__TieneInicio(x,"ICON-")) and (self.__TieneFinal(x,".png") or self.__TieneFinal(x,"jpg")):
                listaResultados.append(x)
        return listaResultados            
    #---------------------------------------------------------------------
    def __obtenerScriptsRun(self): #Devuelve los scripts para ejecutar al momento de considerar
        listaResultados=[]
        for x in self.__obtenerSubarchivos():
            if self.__TieneInicio(x,"Run-") and self.__TieneFinal(x,".py"):
                listaResultados.append(x)
        return listaResultados            
    #---------------------------------------------------------------------
    def __obtenerArchivosParaConsiderar(self): #Devuelve los scripts para devolver archivos a considerar
        listaResultados=[]
        for x in self.__obtenerSubarchivos():
            if not(self.__TieneInicio(x,"Run-")) and not(self.__TieneInicio(x,"ICON-")) and not(self.__TieneFinal(x,".svg")) and not(self.__TieneFinal(x,".png")) and not(self.__TieneFinal(x,".jpg")):
                listaResultados.append(x)
        return listaResultados
    #---------------------------------------------------------------------
    def __CifradoICON(self,origen):
        #cifra contenido y devuelve el contenido en formato ICON
        return "xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo "
    #---------------------------------------------------------------------
    def __ObtenerRutaCompleta(self,archivo):
        #entregar nombre con nombre completo de ruta
        return getcwd()+"\\"+archivo
    #---------------------------------------------------------------------
    def __RegistrarIcono(self,nombreicono):
        #DireccionesIconos=[] #lista con direcciones de Iconos
        #NombresIconos=[]     #lista con los nombres de los iconos
        #CodigoIconos=[]         #cofigo generado algoritmo
        #registra un icono en la "BD" del script
        self.__DireccionesIconos.append(self.__ObtenerRutaCompleta(nombreicono))
        self.__NombresIconos.append(self.__CortarCadenaFinal(self.__CortarCadenaInicio(nombreicono,"ICON-"),".png"))
        self.__CodigoIconos.append(self.__CifradoICON(nombreicono))
    #---------------------------------------------------------------------
    def __RegistrarImagen(self,nombreimagen):
        #direcciones de los archivos considerados
        #DireccionesImagenes=[]#lista con direcciones de imagenes
        #NombresImagenes=[] #nombres de los archivos para importar
        self.__DireccionesImagenes.append(self.__ObtenerRutaCompleta(nombreimagen))
        self.__NombresImagenes.append(nombreimagen)
    #---------------------------------------------------------------------
    def __RegistrarCodigo(self,nombreArchivo):
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
    def CicloRegistroArchivos(self): #registra los archivos en el repositorio actual
        #paso 1. ejecutar todos los archivos Run- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
        for x in self.__obtenerScriptsRun():
            print("   >> Ejecutar: "+str(x))
            codigo="" # <-- codigo del script
            archivo=open(x,"r")
            for y in archivo.readlines():
                codigo=codigo+str(y)
            exec(codigo)
        #Paso 2.-convertir todos los archivos svg en png XXXXXXXXXXXXXXXXXXXXXXXXX        
        for x in self.__obtenerSVG():
            print("   >> renderizar SVG: "+str(x))
            system('inkscape --export-type="png" "'+str(x)+'"')
        #Paso 3.- convierte en condigo de ICON XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        for x in self.__obtenerParaICON():
            print("   >> Generar ICON: "+str(x))
            self.__RegistrarIcono(x)
        #Paso 4.- importar imagen XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
        for x in self.__obtenerImagenesParaImportar():
            print("   >> Importar imagen: "+str(x))
            self.__RegistrarImagen(x)
        #Paso 5.- ingresar archivos de codigo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        
        for x in self.__obtenerArchivosParaConsiderar():
            print("   >> Archivo parar considerar: "+str(x))
        #Paso 6.- ingresar a subcarpetas XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        for x in self.__obtenerSubcarpetas():
            print("\n >>> Entrando a subcarpetas: "+str(x))
            chdir(x)
            self.CicloRegistroArchivos()
            chdir("..")
#=====================================================================================
class ClaseTerminal:
    #----------------------------------------------------
    def __init__(self,objetoAnalisis):
        self.objeto=objetoAnalisis
        self.directorio=getcwd() 
        self.nombrePaquete="PAQUETEE"
        self.__comandoAnterior=""
        self.__comtandoTrasAnterior=""
        self.__comandoNuevo=True #ojo si se pone enter dos veces el comando es salir
        pass
    #----------------------------------------------------
    def __limpiar(self):
        if platsys()=="Windows": system("cls")
        else: system("clear")
    #---------------------------------------------------
    def __cabeceraConsola(self):
        self.__limpiar()
        print("""
      ((((      GEN-HP-PRIME
      ((((      by/por Edwin Saul / @Saul11235
      ))))      
    _ .---.     NAME PACKAGE /NOMBRE PAQUETE:
   ( |`---'|    """ +self.nombrePaquete+ """
    \|     |    
    : .___, :   For/Para Hp Prime
     `-----'
                UBICACION/DIRECTORY
                """+self.directorio+"""

                """)
    #---------------------------------------------------
    def COMANDO_SALIR(self):self.__limpiar();exit()
    def COMANDO_VIFM(self):system("vifm "+self.directorio)
        
    def LanzarConsola(self):
        while True:
            self.__cabeceraConsola()
            comando=input("\n >> ")
            if comando=="q":
                self.COMANDO_SALIR()
            elif comando=="f":
                system("vifm "+self.directorio)
            elif comando=="r":
                self.objeto.CicloRegistroArchivos()

# Modo terminal_________
if __name__=="__main__":
    #rutina comando
    Analisis=ClaseAnalisis()
    Terminal=ClaseTerminal(Analisis)
    Terminal.LanzarConsola()
        


