#Crea para los objetos selecionados un grupo ROOT y AUTO para "resetear" los valores de transformacion y rotacion
import maya.cmds as cmds

objs = cmds.ls(selection = True , transforms = True)
parentObj = ''
obj = ''
listNameObj = []
listNameParent = []
grpRoot = ''
grpAuto = ''


#crea el mensaje de error si el objeto no cumple el naming convention
def message(nameObj , value):
	windowMessage = cmds.window( widthHeight=(270, 20) , title = 'GRPRootAuto')

	if value == 1:
		cmds.frameLayout(nameObj + ' has not a correct Naming Convention' )
		
	if value == 2:
		cmds.frameLayout(nameObj + ' has not a correct number of parts')
	
	if value == 3:
		cmds.frameLayout(nameObj + ' has a correct hierarchy')

	cmds.showWindow(windowMessage)
	
#filtra el nombre del objeto. Devuelve una lista con las partes del string
def filterNameObj(nameObj):
	partsObj = nameObj.split("_")
	return  partsObj

#Crea los grupos	
def createGrpRoot(obj , namesGRP , parentObj):
	grpRoot = cmds.createNode( 'transform',  n = ('grp_' + namesGRP[0] + '_root' + namesGRP[1]) , p = obj)
	#grpRoot = ('grp_' + namesGRP[0] + '_root' + namesGRP[1]) 
	cmds.xform (grpRoot , t = [0 , 0 , 0] , ro = [0 , 0 , 0])
	
	cmds.createNode( 'transform',  n = ('grp_' + namesGRP[0] + '_auto' + namesGRP[1]) , p = grpRoot) 
	grpAuto = ('grp_' + namesGRP[0] + '_auto' + namesGRP[1])
	cmds.xform (grpAuto , t = [0 , 0 , 0] , ro = [0 , 0 , 0])
	
	#desemparenta el grupo ROOT y AUTO 
	cmds.parent (grpRoot, world = True )  
	
	#Emparenta el objeto selecionado al grupoAUTO y el grupoROOT al padre del objeto seleccionado
	cmds.parent (obj , grpAuto)
	
	if parentObj[0] != obj:
		cmds.parent (grpRoot , parentObj[0]) 
	
#resetea los valores jointOrient y rotate    
def restJoint(jnt):
	print jnt
	cmds.setAttr (jnt + '.rotateX' , 0)
	cmds.setAttr (jnt + '.jointOrientX' , 0)
	cmds.setAttr (jnt + '.rotateY' , 0)
	cmds.setAttr (jnt + '.jointOrientY' , 0)
	cmds.setAttr (jnt + '.rotateZ' , 0)
	cmds.setAttr (jnt + '.jointOrientZ' , 0)                       
	
#crea los Group ROOT y AUTO a cada objeto selecionado manteniendo la jerarkía inicial
for o in objs:
	if (o.find('_')) != -1:
		listNameObj = filterNameObj(o)
        
		if len(listNameObj) == 3:                      
			#Recoje el padre del OBJ seleccionado, lo selecciona y filtra su nombre
			parentObj = cmds.pickWalk (o , direction='up')
			listNameParent = filterNameObj(parentObj[0])
			
			if listNameParent[0] == 'grp' and listNameParent[2].find('auto') != -1:
				#message(o , 3)
				grpAutoAuto = cmds.createNode( 'transform',  n = ('grp_' + listNameParent[1] + '_auto' + (listNameParent[2][0].upper() + listNameParent[2][1:(len(listNameParent[2]))])) , p = parentObj[0]) 
				#grpAutoAuto = ('grp_' + namesGRP[0] + '_auto' + namesGRP[1])
				print grpAutoAuto
				cmds.xform (grpAutoAuto , t = [0 , 0 , 0] , ro = [0 , 0 , 0])
				cmds.parent (o , grpAutoAuto)
					
			else:
				listNameGRP = [listNameObj[1] , ((listNameObj[0][0].upper() + listNameObj[0][1:(len(listNameObj[0]))]) + (listNameObj[1][0].upper() + listNameObj[1][1:(len(listNameObj[1]))]) + listNameObj[2])]
				createGrpRoot(o , listNameGRP , parentObj)
				
				#si el objeto es de tipo JNT se resetean sus valores orient y rotate
				typeNode = cmds.nodeType( o )
				
				if typeNode == 'joint':
					restJoint(o)
					
		else:
			message(o , 2)
						
	else:
		message(o , 1)
		
cmds.select (objs)