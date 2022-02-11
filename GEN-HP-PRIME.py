#
#SCRIPT CREADO POR Edwin Saul Pareja @Saul11235
#
#Este script ordena todos los archivos del repositorio en un programa
#listo para ser ejecutado en una HP prime

from os import listdir
#--------------------------------------------------------------------
#Archivo que navega al momento de unir los archivos 
#--------------------------------------------------------------------
def esArchivoEditado (nombreArchivo):
    #Ojo solo funciona con vim u otros editores que usen *.swp
    if len(nombreArchivo)<4:
        return(False)
    else:
        reves=nombreArchivo[::-1]
        if reves[0]=="p" and reves[1]=="w" and reves[2]=="s" and reves[3]==".":return(True)
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
def pideNoSerConsiderada(nombreArchivo):
    #solo si un archivo o carpeta no quiere ser considerado 
    #Es decir si su nombre comienza con  --->>>>     NoCons-
    if len(nombreArchivo)<7:
        return(False)
    else:
        nom=nombreArchivo
        if nom[0]=="N" and nom[1]=="o" and nom[2]=="C" and nom[3]=="o" and nom[4]=="n" and nom[5]=="s" and nom[6]=="-":return(True)
        else:return(False)
#-------------------------------------------------------------------
def filtrarNombre(nombre):
    #devuelve True si es un nombre que se puede ingresar
    #devuelve False si no se debe ingresar al programa
    if esArchivoEditado(nombre) or esNombreReservado(nombre) or pideNoSerConsiderada(nombre):
        return False #No incluir
    else:
        return True #si incluir
#-------------------------------------------------------------------
def navegar():
    listaNombres=[] #lista de nombres a considerar
    for x in listdir():
        if filtrarNombre(x):
            listaNombres.append(x)
    #separar los nombres
    print(listaNombres)
#--------------------------------------------------------------------
# Modo terminal_________
if __name__=="__main__":
    #rutina comando
    print("\n>>> Generar Programa Para HpPrime")
    entrada=input("> enter para continuar otro valor para salir")
    if entrada=="":
        #Generar programa
        navegar()


