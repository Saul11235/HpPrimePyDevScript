#
#SCRIPT CREADO POR Edwin Saul Pareja @Saul11235
#
#Este script ordena todos los archivos del repositorio en un programa
#listo para ser ejecutado en una HP prime

from os import listdir,getcwd,path,system
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
DireccionesImagenes=[]  #lista con direcciones de imagenes
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
        
        
    pass
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
    for x in obtenerSubarchivos():
        if TieneFinal(x,".svg"):
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
    return "89504E470D0A1A0A0000000D49484452000001180000004108060000000A78BB0700000D57494441547801ECD57B5054E7C106F067AFB0BB8840308AA89950D3228249AD1843304D530CDAD51025DA4CD59924D5A89F97CF0B1F42CC983A8D8A9AD238DFD8449BA8A326C65B2308065B3BA6A3440CA26BC509174551038BBBCA0A8BB0EC9E3DE56C27462EBB7BF676DE65F7FDFDC739EFE579F71C9E23625916144551BE20261D80A2A8C0450B86A2289FA105435194CF487DB9F899AA07A8D7991D8E7962900CA9F14AA76B7D76FABED33113472931225AE6CB2351945FA8AEAEC68D1B37D0D2D26277CC73CF3D8761C386395CE7F6EDDB387BF6ACD3FD66CE9CE9564E9F16CCD6E37771B8ACC5E198D72684F32A9839FF7FDBE998832B86D382A102D6FDFBF7919F9F8F3D7BF6D8CAC59983070F3A2D06AE5C66CD9AE5742D9665DDCAECD382A128CA3B4E9C38813973E640AFD7938EE21231E900144539B677EF5EA8D5EA7E572E1C5A3014E5C7CE9E3D8BF9F3E7836118D251DC22B577836581A3E52D283CDF0A431B83914342F0C68B11183D3C847466CA8B2A6F99B0FBEB665CD37622324C828C71E17865DC008844A4935156AB158B172F86C964221DC56D7D164C9BC98AE95B6EE11FFF363E72B5157F2EBE8B0FE60EC672F563A473535E905F7417D9FB9AC058D987D7769D3260F2336138B26A38942162D211835A6161212E5EBC483A8647FA7C8396EDD4F62897FFE25EC4957BB428D11849E7A63CF4D54523B2F66ABB95CB0FB8E7FBBFBBB5A42306BDC3870F938EE0B15E05D3D86CC1EEAF9BED4E60BBDEC74D057AD2B9290FE51DD5D99EA53DBB4E19D074DF423A66502B2B2B231DC163D29E172EDEE880D5C18BC729BFDA4E3A37E5A18ABA0E87F799AE97E042D798293F0F231D356869B55ADE63150A05424343BB5D93CBE5A48FD0BB60A462E793645211E9DC9487243C9EB354423A65706B6B6B733A262C2C0C5F7CF105A64C9902B1584C3A722FBD128D1FA94088CC7181BC304A493A37E5A11712540EEF8776BD03DCBB40F9B7152B5640AD56FB65B9707AA58A504990352DDAEE04B95484B5AF0D229D9BF210F70C6512FB1F92FF7B251A039512D2312927121313494770A8CFDA5B376B10FE273D0AA21EEF1F573E07570CC72FE2E897ADBF4BFE890207560CEB5522E2AE67BE647214DE9B493F22FD814864FF23E10FA47D5D9474BD65DB7E1F83452F47A1A8A215CD6D0C7E1A23C7F4F1E1880AA35FB540C13DCF5F26A8F0B7732DA8D576DA9EEDD4B103307A7808E9685480903ABA99D8F5A225D2972DA071A532EFD791A46350014A4C3A004551818B160C45513E430B86A2289F91F6BC70F2721B723E6B723AF17C5E1CE9EC1E1B9753E79575C4226070841423A265487F3A0C93C6A8A090BBD7DDDC6FCF3D0347D29254C89B3D186686C59E7F1970ACA2150DF72CB0B2DDC7397A467CCECEEDC1EDE58E868606141616A2B4B4148D8D8D30180CF0B6F3E7CF7B34B7A8A808959595D06AB5E8E8E8F04AA6D0D0500C193204898989983A752AC68D1BC76B5E4E4E0E4E9E3CE9F27EDCBC4D9B36F5792F2F2F0F696969DDAEF5CCD3DCDCCC6B1F3EE7E86BBF5E05D36C645051D78E60E08B73FEE5C43DC4444AF1DE6B8F637E5AA4AD7C5C5177A7D369AEB8C13218DA184CDE508F73B5ED3E3B3BF72EB84AA7D361EDDAB5F8F4D34F61369BE16FCACACA909595652B3E5F3A72E408D6AD5B87D4D4546CD9B20513264C7038BEAEAE0E1515152EEFC3CDB3A7AFF270670FBEF3FADACFBDCF2CE55063B3050BFFDA80CC0F6EC2D861F5C91E0B7634B85D2EBEA2D1686C5FBA8F3FFED82FCB65DBB66D983871A2CFCBE55167CE9CB1EDC9ED1D8C68C1F8D0D1F25664FEE9162C0CEBD5756FE9CD3854D642FA78DD5CBF7E1D93264DC2CD9B374947E9D3CE9D3BB164C912582C16C1F7E6F6E4F6DEBE7D3BE99F4170B4607CECEF978CD8F0A5DEAB6B5EAA3781F56E677984611864646440AFF7EE39BD45A3D160E1C285A46360E9D2A5B874E912E91882A2052380CD057A680DDEFB72B6775A491FA99BDDBB77E3F2E5CBA463D8959B9B0BB3D94C3A862D434E4E0EE91882A2052380369315FB4E1B48C7F0998F3EFA887404BB6EDCB881929212D2311EE2B25CBF7E9D740CC1D08211C8B1F3ADA423F88456ABC5850B1748C7B0EBD8B163A423F472FCF871D21104430B462057B59DA423F8446D6D2D5896251DC3AE9A9A1AD2117AE17EB36021251D80A4D519D11ECDEFB4B0F84A6344D5F726A7639BEE333E39C313836498F2CC000C5492F956E8743ADE63D56A3512131305CDA7D7EB798D1B3060005E7FFD75444545B9B5CFBD7BF7B07FFF7E188D46A7639B9A9A7A5DCBC8C8405C5C5CB76B9B366D72BA16372F3E3EBECF7B7D5D5FBD7A75B7BFABAAAA505050E0749F9EF3F8EE17D40593377BB0C76B6CFC1D8B17DEBB8E6FAFB63B1CC758BDFB951789803FFEF671647795A44C22F2E9EFE4F05C0CBFE2DCB06103727373FD325F686828BEF9E61B8FCB6FE9D2A5484E4E86C9647239D3ECD9B37B5DE35330DCBC993367F2CE989797D7EDEF43870EF12A989EF3F822F3D90B20213211DEFA55A4E0FBE6BC1A8D353306112D17572C58B0807404BB5253533D2E174E5252926D2DEA47B460BCE04E8B45D0FD0628C4B672E94FF47A3DE9087645467AEF0311151545FA387E85168C874AAB1F20BFE8AEA07B3E3B52015548FF7A740B172E844EA7231D83129894740092182B8B7F5E6EC3B18A565CB96542D37D0B3ACC2CEFF90F4C56680D16C17347A82482EF698F42A1E035EED4A953183A7428468C18E1D2FAE1E1E1888D8DC5F3CF3F8FE9D3A7233E3E9EF4912917046DC194688CC8DAABB5154B7F2312914EF0A3989818DE632D160BEAEAEA5CDE43A3D1A0B8B8186BD6ACC1AC59B3B079F366978B8A22434C3A0009EB0EE9F09B8DF5FDB25CFC4D424202542A95207BB12C8B03070E20393919A74F9F267D748A87A02B98BCA37AFCE1D09DAE97957492C0A050283079F26441F7BC73E70ED46A352A2B2B491F9F7222A80AE66CCD03ACD9DF443A46C079E79D7720128904DDB3B5B515999999309BCDA48F1F14AC56AB5BF382AA60B2F735C1CA924E1178C68E1D8B458B1609BE6F4D4D0D76ECD841FAF841412C76AF2A82A6606A1A3B71A6EA01E91801EBC30F3F445A5A9AE0FB7EF2C927A48F4E391034055354D14A3A424093C964282E2EC6DB6FBF2DE8BE1A8D060D0D0DA48F4FD911340553D7D4493A42C093CBE5D8BE7D3B4A4B4B919E9E6E2B1D215CBB768DF4D1293BA4A4030845DFCAF01A37285C8AB77E1581B8C1721E6B5A70F4DB56945F6B277D3CBF92929282929212180C069C3B770E8D8D8DE8ECE45FF066B319656565F8FCF3CF61B55A9D8ED7E974A48F4CD9113405636559A76354216294AD7F9257B9FC20E7D541506FAC4789C648FA887E27222202E9E9E96ECD5DBC7831C68F1F8F65CB96391DCB300CE9A35276884907F027293F53BA542E1CB10878E3C508D2D103D2DCB97305D9C76AB5FAE55AFEC4DD73D18279C4EDBB66B0ACEBF3BEBF67211D3D20D5D7D70BB2CF952B57BA9E3BEBF13ADC3F616565A5209985E6EEB968C13CE2BBEF4DC8DED7046307FFB63EFDDD036CFC52473A7AC0A9ADADC5BC79F304D9ABAAAA0A595959686B6B737B0DA3D18855AB56A1BABA5AA89F4850DCB3B87AF5AACBF3A4A4830B4529E7D7A51F1CD363EBF1BB080B753E9EB1B26869B7923E1A5105050578F3CD37BDBA26C330686969E13D5EA552D9BDA7542A79AD919F9F8FAD5BB7223C3CDCADCC5C5E2EB7A77985C6374B7979399E7AEA29DBEF239148FA1CB36BD72E64646474BB16340533348AFF51CD0C8BE6368674E47EA1B3B313CDCDCD4433C4C6C6DABD171313C37B1DAE208438CBD0A14305F95D7C91C551F173EF424F62D20714CAB32395A423503E3070E0408C1A35CAEEFD949414D211FD3AD3E8D1A3111111E1B3F583A6605E7E5A857045D01C37684C9B360D72B9DCEEFDB4B4345B09F90B2ECB4B2FBD443AC64332990C6AB5DA67EB07CD7F9C422E46D62BD1A463505E249148909B9BEB708C42A140565616E9A80F656767DB32F99377DF7D1752A9D4276B074DC170564D7D0C49234249C7A0BC84FB674D4848703A6EE5CA95484A4A221D1763C68CC1F2E5CB49C7E8253E3EDE67251C5405A30C11A3207B3862A364A4A3501E9A316306DE7FFF7D5E63954A250A0B0B111B1B4B2C2FB7774141812D8B3F5ABF7E3D323333BDBE6E50150CE7C9C7E528DF1887D478FF7CD024FCA79DFAE7491E8AC200FEC8BF60139A186B4893FABEB8685DD89BB61FC301BE851B8C2EF0495CDA4F4135E9C0042C96CDA491348D030C0842406E23839A509062D19CDF480EE71E9ECB3DBF49329944B55A85699A4824D6FFFB160A05349B4D689AF6E333EBBA1E9CCD66D8572C4BC33050A954828C23EB1BF70F8B83789482757306E3FA14EA0587C441DC1391303CCFA35C2EA3DD6EA356AB6DB45C964451846559C143525535D287F419EBCDCE608BB0D1680467EF3B9669BD5E47ABD542A954422E97DBBAE7C17C3EFFF081FB3C81DD7D09FDE295C287D6DC3F0CF1E84F56D6FC3F494393B9D05EB777FDD01AFD92C33F21BD7108FE600AE7E9155E7F8AD90C3BB34E667677B8B883E9CA1AE93805E59CDB6A16D31E84D628E7878BB356E7E9BA2E6CDB8E3EAC77D96C36789CC56211994C26D2DEBEEFC3711C789EB7B8F7682E9E3DD27C3E0F59962108C256BDD8720AA3280A24498A3497A5F1788C4EA7835EAF87D168F4AD59BE2C184208894A22EE0108217F172D1842C8CED0822184ECCC1BBA5D503ABC1148770000000049454E44AE426082"


#---------------------------------------------------------------------

#---------------------------------------------------------------------
def CicloRegistroArchivos(): #registra los archivos en el repositorio actual
    #paso 1. ejecutar todos los archivos Run- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
    for x in obtenerScriptsRun():
        print("\n >>> Ejecutar: "+str(x))
        codigo="" # <-- codigo del script
        archivo=open(x,"r")
        for y in archivo.readlines():
            codigo=codigo+str(y)
        exec(codigo)
    #Paso 2.-convertir todos los archivos svg en png XXXXXXXXXXXXXXXXXXXXXXXXX        
    for x in obtenerSVG():
        print("\n >>> renderizar SVG: "+str(x))
        system('inkscape --export-type="png" "'+str(x)+'"')
    #Paso 3.- convierte en condigo de ICON XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    for x in obtenerParaICON():
        print("\n >>> Generar ICON: "+str(x))
        print(getcwd()+"\\"+str(x))
    #Paso 4.- importar imagen XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
    for x in obtenerImagenesParaImportar():
        print("\n >>> Importar imagen: "+str(x))
    #Paso 5.- ingresar archivos de codigo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        
    for x in obtenerArchivosParaConsiderar():
        print("\n >>> Archivo parar considerar: "+str(x))

# Modo terminal_________
if __name__=="__main__":
    #rutina comando
    print("\n>>> Generar Programa Para HpPrime")
    entrada=input("> enter para continuar otro valor para salir")
    if entrada=="":
        #Geprintnerar programa
        print(" Directorio Actual > "+getcwd() )
        CicloRegistroArchivos()

