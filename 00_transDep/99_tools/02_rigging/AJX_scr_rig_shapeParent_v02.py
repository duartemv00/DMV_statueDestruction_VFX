#a�ade el nodo shape del �ltimo objeto selecionado al resto de objetos.
import maya.cmds as cmds
selectObj = []
shapeInst = []
listShapes = []
typeShape = ''
deleteNull = ''

selectObj = cmds.ls(selection = True)            #Todos los objetos selecionados
shapeInst = cmds.listRelatives(selectObj[len (selectObj) - 1])    #Recoge el shape del �ltimo objeto seleccionado   
listShapes = [selectObj[len (selectObj) - 1]]        #a�ade el �ltimo objeto seleccionado a la lista de shapes

    
for i in range (len (selectObj) - 2):    #Instancia el objeto final tantas veces como objetos haya selecionados menos uno y los a�ade a la lista de shapes              
    cloneInstance = cmds.instance(selectObj[len (selectObj) - 1])
    listShapes.append (cloneInstance)    #a�ade los objeto instanciados o a la lista de shapes

print listShapes
print selectObj   
for j in range (len (listShapes)):                      #Emparenta el shape de los objetos instanciados al resto de objetos seleccionados
    shape = cmds.listRelatives(listShapes[j] , f = 1)
    
#    typeShape = cmds.listRelatives(selectObj[j] , shapes = True)    #Si el objeto seleccionado al que se le a�adir� el shape instanciado tiene un nodo de tipo shape lo elimina
#    if typeShape != None:
#        deleteNull = cmds.createNode( 'transform',  n = 'delete')    #Crea un GRP
#        cmds.parent((cmds.listRelatives(selectObj[j] , f = 1)) , deleteNull , shape = True, relative = True)    #a�ade el shape el GRP
#        cmds.delete (deleteNull)        #Elimina el GRP con el shape que se hab�a a�adido

       
    cmds.select(shape)
    cmds.parent(shape , selectObj[j] , shape = True, relative = True)
    if cmds.objectType(selectObj[j]) == 'joint':
    	print selectObj[j]
    	cmds.setAttr(selectObj[j] + '.drawStyle', 2)
    	
    cmds.delete(listShapes[j])                          #Borra el nodo de transformaci�n de los objetos instanciaods