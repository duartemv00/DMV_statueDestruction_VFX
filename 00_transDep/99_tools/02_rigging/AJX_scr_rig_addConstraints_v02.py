#Tool AJX para añadir constraints
#Con la opción Apply SKIN añade o elimina los constraints en los joints de tipo Skin seleccionados o, en el caso de no tener ningún joint selecionado, añade o elimina los constraints en todo el sistema SKIN
#Restringe solo los ejes selecionados
#Cuando no hay ningún eje selecionado elimina los constraints de todos los objetos seleccionados
#Selecionar primero el/los target y despué sel objeto al que se quiere añadir el constraint
#Adaptado al pipeline AJXrigging => Añade el constraint al padre directo del último objeto selecionado, el cual será el grupo Auto. Si no existe... lo crea
#Divide el peso de influencia de cada target según el número de targets selecionados
#La opción Path añade un pathAnimation con frontAxis Z. Seleccionar opción Y cuando la spline está alineada a los ejes XZ del mundo. Seleccionar opción Z cuando la spline está alineada a los ejes YZ del mundo.
#La opción Aim añade un aimConstraint. AimVector será el seleccionado y los otros dos ejes serán donde se añadirán las restricciones.Las opciones None en UpVector y WorldUpVector no añaden ningún tipo de UpVector en el pathAnimation

import maya.cmds as cmds

def filterNameObj(nameObj):
	if (nameObj.find(':')) != -1:
		#print nameObj
		obj = nameObj.split(':' )
		#print obj[1]
		partsObj = obj[1].split("_")
		return  partsObj
		
	else:	
		partsObj = nameObj.split("_")
		return  partsObj
		
def messageCheckAddConstraint(messageErrorAddConstraint):
    #print messageErrorRigPipe
        
    if cmds.window ('windowCheckAddConstraint' , exists = True):
        cmds.deleteUI ('windowCheckAddConstraint') 
        
    windowCheckAddConstraint = cmds.window('windowCheckAddConstraint' , widthHeight=(225, 225))
    scrollLayout = cmds.scrollLayout()
    
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 5 )
    
    for o in messageErrorAddConstraint:
    	cmds.frameLayout(o)
    
    cmds.showWindow(windowCheckAddConstraint)
		
#Función que añade el constraint según la configuarción del UI		
def addSkinConstraint():
	global listMistakes
	listMistakes = ['Contraints applied']
	
	#Crea y recoge todas las variables 						
	allObjects = cmds.ls(selection = True)
	
	valueCBskin = cmds.checkBox('CBskin' , q = True , value = True)
	
	valueCBoffset = cmds.checkBox('CBoffset' , q = True , value = True)
	
	valueCBx = cmds.checkBox('CBx' , q = True , value = True)
	
	valueCBy = cmds.checkBox('CBy' , q = True , value = True)
	
	valueCBz = cmds.checkBox('CBz' , q = True , value = True)
	
	valueCBpans = cmds.checkBox('CBpans' , q = True , value = True)
	
	valueCBpns = cmds.checkBox('CBpns' , q = True , value = True)
	
	valueCBons = cmds.checkBox('CBons' , q = True , value = True)
	
	valueCBsns = cmds.checkBox('CBsns' , q = True , value = True)
	
	#------------recoge los datos para el path constraint---------------	
	valueCBpathns = cmds.checkBox('CBpathns' , q = True , value = True)
	
	valueRCpathUpAxis = cmds.radioCollection('RCpathUpAxis' , q = True , sl = True)
	
	#------------recoge los datos para el aim constraint---------------
	valueCBans = cmds.checkBox('CBans' , q = True , value = True)
	
	valueRCaimVector = cmds.radioCollection('RBaimVector' , q = True , sl = True)
	
	valueRCupVector = cmds.radioCollection('RBaimUpAxis' , q = True , sl = True)
	
	valueRCupType = cmds.radioCollection('RBaimUpType' , q = True , sl = True)
	
	
	#Si no hay objetos seleccionados y la casilla Skin está activada, selecciona todos los objetos d ela escena
	if allObjects == [] and valueCBskin == True:
		cmds.select( all = True )
		allObjects = cmds.ls(selection = True , dag = True , transforms = True)
	
	#Guarda en una lista los ejes que no se añadirán al constraint. OJO!!!! Los joints jerarquiezados al grupo sýmmetry del lado derecho tiene los ejes volteados ==> Problema con el constraint en posición
	skipAxis = []
	
	if valueCBx == False:
		skipAxis.append('x')
		
	if valueCBy == False:
		skipAxis.append('y')
		
	if valueCBz == False:
		skipAxis.append('z')		

#-------------------------------------------------------------------------------------------------	
	#Si la casilla Skin está activada busca los target de los joints de tipo Skin añadidos en la lista allObjects
	if valueCBskin == True:
		for obj in allObjects:
			objFiltered = filterNameObj(obj)
			listJntSkin = []
			target = ''
		
			if objFiltered[0] == 'skin' or objFiltered[0] == "skn":
				if obj.find('End') == -1:
					listJntSkin.append(obj)
					#print obj
					
					if cmds.objExists('jnt_' + objFiltered[1] + '_' + objFiltered[2]) == True:
						target = ('jnt_' + objFiltered[1] + '_' + objFiltered[2])
						partName = 'jnt'
					
					if cmds.objExists('ctl_' + objFiltered[1] + '_' + objFiltered[2]) == True:
						target = ('ctl_' + objFiltered[1] + '_' + objFiltered[2])
						partName = 'ctl'
						
					if cmds.objExists('cik_' + objFiltered[1] + '_' + objFiltered[2]) == True:
						target = ('cik_' + objFiltered[1] + '_' + objFiltered[2])
						partName = 'cik'
						
					if cmds.objExists('ckf_' + objFiltered[1] + '_' + objFiltered[2]) == True:
						target = ('cfk_' + objFiltered[1] + '_' + objFiltered[2])
						partName = 'cfx'
						
					if cmds.objExists('main_' + objFiltered[1] + '_' + objFiltered[2]) == True:
						target = ('main_' + objFiltered[1] + '_' + objFiltered[2])
						partName = 'main'
						
					#Si no hay ningún eje seleccionado elimina todos los constraints
					try:
						if skipAxis != ['x' , 'y' , 'z']:
							if valueCBpans == True:
								cmds.parentConstraint(target , obj , n = ('pans_' + objFiltered[1] + '_' +  partName + objFiltered[1].upper() + objFiltered[2] + 'To' + objFiltered[0] + objFiltered[1].upper() + objFiltered[2]) , mo = valueCBoffset , st = skipAxis , sr = skipAxis)
									
							if valueCBpns == True:
								cmds.pointConstraint(target , obj , n = ('pns_' + objFiltered[1] + '_' +  partName + objFiltered[1].upper() + objFiltered[2] + 'To' + objFiltered[0] + objFiltered[1].upper() + objFiltered[2]) , mo = valueCBoffset , sk = skipAxis)
								
							if valueCBons == True:
								cmds.orientConstraint(target , obj , n = ('ons_' + objFiltered[1] + '_' +  partName + objFiltered[1].upper() + objFiltered[2] + 'To' + objFiltered[0] + objFiltered[1].upper() + objFiltered[2]) , mo = valueCBoffset ,sk = skipAxis)
								
							if valueCBsns == True:
								cmds.scaleConstraint(target , obj , n = ('sns_' + objFiltered[1] + '_' +  partName + objFiltered[1].upper() + objFiltered[2] + 'To' + objFiltered[0] + objFiltered[1].upper() + objFiltered[2]) , mo = valueCBoffset , sk = skipAxis)
								
						else:
							cmds.select(listJntSkin)
							cmds.delete(constraints = True)
							global listMistakes
							listMistakes = ['Constraints removed']
					except:
						global listMistakes
						listMistakes.append(obj)
	
#-----------------------------------------------------------------------------------------------------------------------		
	#Si la casilla Skin no está activada añade el contraint el último objeto seleccionado y el resto como target	
	else:		
		if len(allObjects) == 1:
			#Si no hay ningún eje seleccionado elimina todos los constraints
			if skipAxis != ['x' , 'y' , 'z']:
				listMistakes = ['Please, first select targets and after the constrained object']
			else:
				cmds.select(cmds.listRelatives(allObjects[0] , parent = True))
				cmds.delete(constraints = True)
				global listMistakes
				listMistakes = ['Constraints removed']
		else:			
			consObj = allObjects[len(allObjects)-1]
			obj =  cmds.pickWalk (consObj , direction='up')
			objFiltered = filterNameObj(obj[0])

			
#---------------Si no existe el grupo Auto del último objeto selecionado... lo crea			
			if obj[0] != ('grp_' + objFiltered[1] + '_' + objFiltered[2]):
				listNameObj = filterNameObj(consObj)

				#Recoje el padre del OBJ seleccionado, lo selecciona y filtra su nombre
				parentObj = cmds.pickWalk (consObj , direction='up')
				listNameParent = filterNameObj(parentObj[0])
				
				if listNameParent[0] == 'grp' and listNameParent[2].find('auto') != -1:
					#message(o , 3)
					grpAutoAuto = cmds.createNode( 'transform',  n = ('grp_' + listNameParent[1] + '_auto' + (listNameParent[2][0].upper() + listNameParent[2][1:(len(listNameParent[2]))])) , p = parentObj[0]) 
					cmds.xform (grpAutoAuto , t = [0 , 0 , 0] , ro = [0 , 0 , 0])
					cmds.parent (consObj , grpAutoAuto)
						
				else:
					listNameGRP = [listNameObj[1] , ((listNameObj[0][0].upper() + listNameObj[0][1:(len(listNameObj[0]))]) + (listNameObj[1][0].upper() + listNameObj[1][1:(len(listNameObj[1]))]) + listNameObj[2])]
					createGrpRoot(consObj , listNameGRP , parentObj)
					
					#si el objeto es de tipo JNT se resetean sus valores orient y rotate
					typeNode = cmds.nodeType( consObj )
					
					if typeNode == 'joint':
						restJoint(consObj)								
						
				obj = cmds.pickWalk (consObj , direction='up')
#-----------------------------------------------------------------------------------						
			
			Tweight = round((1.0 / ((len(allObjects))-1)),2)
			
			listMistakes.append( 'In ' + consObj)
		
			for i in range (len(allObjects)-1):
				target = allObjects[i]
				targetFiltered = filterNameObj(target)
				
				if valueCBpans == True:
					cmds.parentConstraint(target , obj , n = ('pans_' + objFiltered[1] + '_' +  objFiltered[0] + objFiltered[1].upper() + objFiltered[2] + 'To' + targetFiltered[0] + targetFiltered[1].upper() + targetFiltered[2]) , mo = valueCBoffset , st = skipAxis , sr = skipAxis , weight = Tweight)
											
				if valueCBpns == True:
					cmds.pointConstraint(target , obj , n = ('pns_' + objFiltered[1] + '_' +  objFiltered[0] + objFiltered[1].upper() + objFiltered[2] + 'To' + targetFiltered[0] + targetFiltered[1].upper() + targetFiltered[2]) , mo = valueCBoffset , sk = skipAxis , weight = Tweight)
										
				if valueCBons == True:
					cmds.orientConstraint(target , obj , n = ('ons_' + objFiltered[1] + '_' +  objFiltered[0] + objFiltered[1].upper() + objFiltered[2] + 'To' + targetFiltered[0] + targetFiltered[1].upper() + targetFiltered[2]) , mo = valueCBoffset ,sk = skipAxis , weight = Tweight)
										
				if valueCBsns == True:
					cmds.scaleConstraint(target , obj , n = ('sns_' + objFiltered[1] + '_' +  objFiltered[0] + objFiltered[1].upper() + objFiltered[2] + 'To' + targetFiltered[0] + targetFiltered[1].upper() + targetFiltered[2]) , mo = valueCBoffset , sk = skipAxis , weight = Tweight)
		
				if valueCBpathns == True:
					cmds.pathAnimation(obj , target , n = ('pathns_' + objFiltered[1] + '_' +  objFiltered[0] + objFiltered[1].upper() + objFiltered[2] + 'To' + targetFiltered[0] + targetFiltered[1].upper() + targetFiltered[2]) , follow = True , followAxis = 'Z' , ua = valueRCpathUpAxis , wut = 'vector' , startTimeU = (cmds.playbackOptions(q = True , minTime = True)) , endTimeU = (cmds.playbackOptions(q = True , maxTime = True)))
					
				if valueCBans == True:
					#Crea la variable para objectUp añadiendo el mismo objeto al que se le añade el constraint. En el caso de que el usuario seleccione Obj esta variable será intercambiada por el nombre del target que la tool crea como upObject
					grpTagetUpVector = consObj
					
					#recoge el valor del aimVector
					if valueRCaimVector == 'X':
						valueRCaimVector = [1 , 0 , 0]
						skipAxis = ['x']
					if valueRCaimVector == 'Y':
						valueRCaimVector = [0 , 1 , 0]
						skipAxis = ['y']
					if valueRCaimVector == 'Z':
						valueRCaimVector = [0 , 0 , 1]
						skipAxis = ['z']
						
					#recoge el valor del UpVector
					if valueRCupVector == 'None':
						valueRCupVector = [0 , 0 , 0]
					if valueRCupVector == 'X':
						valueRCupVector = [1 , 0 , 0]
					if valueRCupVector == 'Y':
						valueRCupVector = [0 , 1 , 0]
					if valueRCupVector == 'Z':
						valueRCupVector = [0 , 0 , 1]
						
					#recoge el valor del UpType
					if valueRCupType == 'None':
						valueRCupType = 'none'
					if valueRCupType == 'World':
						valueRCupType = 'vector'
					if valueRCupType == 'Obj':
						valueRCupType = 'object'
						
						#Crea el objeto upVector
						listNameParent = filterNameObj(consObj)
						
						grpTagetUpVector = cmds.createNode( 'transform',  n = ('grp_' + listNameParent[1] + '_targetUpVector' + listNameParent[0] + (listNameParent[2][0].upper() + listNameParent[2][1:(len(listNameParent[2]))])) , p = consObj) 
						cmds.xform (grpTagetUpVector , t = valueRCupVector , ro = [0 , 0 , 0])
						cmds.setAttr(grpTagetUpVector + '.displayHandle' , 1)
							
					cmds.aimConstraint(target , obj , n = ('ans_' + objFiltered[1] + '_' +  objFiltered[0] + objFiltered[1].upper() + objFiltered[2] + 'To' + targetFiltered[0] + targetFiltered[1].upper() + targetFiltered[2]) , mo = valueCBoffset , sk = skipAxis , aim = valueRCaimVector , upVector = valueRCupVector , worldUpType = valueRCupType , worldUpObject = grpTagetUpVector , weight = Tweight)
		
	print listMistakes
	cmds.select( deselect = True )	
	messageCheckAddConstraint(listMistakes)	
	
#resetea los valores jointOrient y rotate    
def restJoint(jnt):
	print jnt
	cmds.setAttr (jnt + '.rotateX' , 0)
	cmds.setAttr (jnt + '.jointOrientX' , 0)
	cmds.setAttr (jnt + '.rotateY' , 0)
	cmds.setAttr (jnt + '.jointOrientY' , 0)
	cmds.setAttr (jnt + '.rotateZ' , 0)
	cmds.setAttr (jnt + '.jointOrientZ' , 0)
	
#Crea los grupos	
def createGrpRoot(obj , namesGRP , parentObj):
	print "-------Freeze objetcs--------"
	grpAuto = ''
	grpRoot = ''
	
	grpRoot = cmds.createNode( 'transform',  n = ('grp_' + namesGRP[0] + '_root' + namesGRP[1]) , p = obj)
	#grpRoot = ('grp_' + namesGRP[0] + '_root' + namesGRP[1]) 
	cmds.xform (grpRoot , t = [0 , 0 , 0] , ro = [0 , 0 , 0])
	print grpRoot
	
	cmds.createNode( 'transform',  n = ('grp_' + namesGRP[0] + '_auto' + namesGRP[1]) , p = grpRoot) 
	grpAuto = ('grp_' + namesGRP[0] + '_auto' + namesGRP[1])
	cmds.xform (grpAuto , t = [0 , 0 , 0] , ro = [0 , 0 , 0])
	print grpAuto
	
	#desemparenta el grupo ROOT y AUTO 
	cmds.parent (grpRoot, world = True )  
	
	#Emparenta el objeto selecionado al grupoAUTO y el grupoROOT al padre del objeto seleccionado
	cmds.parent (obj , grpAuto)
	
	if parentObj[0] != obj:
		cmds.parent (grpRoot , parentObj[0])  
		
#Crea la ventana			
def UIaddSkinConstraint():

    if cmds.window ('UIaddSkinConstraint' , exists = True):
        cmds.deleteUI ('UIaddSkinConstraint') 
          
    cmds.window('UIaddSkinConstraint' , widthHeight = (200, 200) , title = 'Add constraints to skin')
    
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 2 )
    cmds.rowLayout( numberOfColumns = 2 ) 
    cmds.separator( style = 'single' , width = 40 )
    CBskin = cmds.checkBox ('CBskin' , value = False , label = 'Apply to SKIN' , width = 200 )
    
    cmds.setParent( '..' )
    cmds.separator( style = 'none' , height = 2 )
    cmds.rowLayout( numberOfColumns = 2 , backgroundColor = [0.5, 0.5, 0.5]) 
    cmds.separator( style = 'single' , width = 40 )
    CBoffset = cmds.checkBox ('CBoffset' , value = False , label = 'Maintain OFFSET' , backgroundColor = [0.5, 0.5, 0.5] , width = 500) 

    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 5 )
    cmds.rowLayout( numberOfColumns = 6 ) 
    cmds.separator( style = 'single' , width = 25 ) 
    CBx = cmds.checkBox ('CBx' , value = True , label = 'X' , backgroundColor = [1, 0, 0])
    cmds.separator( style = 'single' , width = 25 )
    CBy = cmds.checkBox ('CBy' , value = True , label = 'Y' , backgroundColor = [0, 1, 0])
    cmds.separator( style = 'single' , width = 25 )
    CBz = cmds.checkBox ('CBz' , value = True , label = 'Z' , backgroundColor = [0, 0, 1])
    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 10 )
    cmds.rowLayout( numberOfColumns = 3 )  
    CBpans = cmds.checkBox ('CBpans' , value = True , label = 'Parent')
    cmds.separator( style = 'single' , width = 50 )
    CBpns = cmds.checkBox ('CBpns' , value = False , label = 'Point')
    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 1 )
    cmds.rowLayout( numberOfColumns = 3 ) 
    CBons = cmds.checkBox ('CBons' , value = False , label = 'Orient')
    cmds.separator( style = 'single' , width = 50 )
    CBsns = cmds.checkBox ('CBsns' , value = False , label = 'Scale')
    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 10 )
    cmds.rowLayout( numberOfColumns = 5 , backgroundColor = [0.5, 0.5, 0.5] , width = 500) 
    CBpathns = cmds.checkBox ('CBpathns' , value = False , label = 'Path')
    cmds.separator( style = 'single' , width = 20 )
    cmds.text( label='UpAxis:' )
    RCpathUpAxis = cmds.radioCollection ('RCpathUpAxis')
    cmds.radioButton ('X')
    cmds.radioButton ('Y' , sl = True)

    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 10 )
    cmds.rowLayout( numberOfColumns = 7) 
    CBans = cmds.checkBox ('CBans' , value = False , label = 'Aim')
    cmds.separator( style = 'single' , width = 20 )
    cmds.text( label='AimVector:' )
    RBaimUpAxis = cmds.radioCollection ('RBaimVector')
    cmds.radioButton ('X' , sl = True)
    cmds.radioButton ('Y')
    cmds.radioButton ('Z')
    
    cmds.setParent( '..')
    cmds.columnLayout()
    cmds.rowLayout( numberOfColumns = 7) 
    cmds.separator( style = 'single' , width = 67 )
    cmds.text( label='UpVector:' )
    RBaimUpAxis = cmds.radioCollection ('RBaimUpAxis')
    cmds.radioButton ('X')
    cmds.radioButton ('Y')
    cmds.radioButton ('Z')
    cmds.radioButton ('None' , sl=True)
    
    cmds.setParent( '..')
    cmds.columnLayout()
    cmds.rowLayout( numberOfColumns = 7) 
    cmds.separator( style = 'single' , width = 43 )
    cmds.text( label='WorldUpType:' )
    RBaimUpType = cmds.radioCollection ('RBaimUpType')
    cmds.radioButton ('Obj')
    cmds.radioButton ('World')
    cmds.radioButton ('None' , sl=True)
    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 15 ) 
    cmds.rowLayout( numberOfColumns = 3 )
    cmds.separator( style = 'single' , width = 25 )
    cmds.button( label = 'ADD CONSTRAINTS', height = 18 , width = 120 , backgroundColor = [0.5, 0.5, 0.5] , command = 'addSkinConstraint()')
    
    cmds.showWindow('UIaddSkinConstraint')
    
UIaddSkinConstraint()