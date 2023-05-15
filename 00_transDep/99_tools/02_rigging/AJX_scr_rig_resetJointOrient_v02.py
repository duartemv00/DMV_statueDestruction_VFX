#Tool AJX para resetear los valores del Orient o del Rotate Joint de los joints seleccionados.
#Solo reseteas los valores de los objetos de tipo joint seleccionados
#El botón ORIENT resetea todos los valores y deja el Orient Joint a ZERO
#El botón ROTATE resetea todos los valores y deja el Rotate Joint a ZERO

import maya.cmds as cmds	

orient = 'orient'
rotate = 'rotate'
	
def ZEROrientRotate(attrZERO):
	print 'ZERO Orient or Rotate Joint'
	print attrZERO
	
	objs = cmds.ls(selection = True)

	for o in objs:
		#solo se aplica en objteos tipo Joints
		if cmds.nodeType( o ) == 'joint':
			valueRotate = cmds.xform (o , q = True , ws = True , ro = True )     #recoge el valor global de rotación
			
			#Recoge el padre para poder desemparentarlo y así resetear los valores del rotate correctamente antes de hacer la operación seleccionada.
			parentObj = cmds.pickWalk (o , direction='up')
			
			if parentObj[0] != o:
				cmds.parent( o , world = True )			
				
			cmds.setAttr(o + '.jointOrientX' , valueRotate[0])	
			cmds.setAttr(o + '.jointOrientY' , valueRotate[1])
			cmds.setAttr(o + '.jointOrientZ' , valueRotate[2])
						
			cmds.setAttr(o + '.rotateX' , 0)
			cmds.setAttr(o + '.rotateY' , 0)
			cmds.setAttr(o + '.rotateZ' ,0)
			
			if parentObj[0] != o:							
				cmds.parent( o , parentObj )
			
			#Si se ha seleccionado la opción Orient ZERO se resetean loa valores Orient				
			if attrZERO == 'orient':
				#Recoge los valores el jointOrient
				valueX = cmds.getAttr(o + '.jointOrientX')
				valueY = cmds.getAttr(o + '.jointOrientY')
				valueZ = cmds.getAttr(o + '.jointOrientZ')		
				
				cmds.setAttr(o + '.rotateX' , valueX)	
				cmds.setAttr(o + '.rotateY' , valueY)
				cmds.setAttr(o + '.rotateZ' , valueZ)
					
				cmds.setAttr(o + '.jointOrientX' , 0)
				cmds.setAttr(o + '.jointOrientY' , 0)
				cmds.setAttr(o + '.jointOrientZ' ,0)

	cmds.select(objs)
			
#Crea la ventana			
def UIorientJoint():
    if cmds.window ('UIorientJoint' , exists = True):
        cmds.deleteUI ('UIorientJoint') 
          
    cmds.window('UIorientJoint' , widthHeight = (170, 55) , title = 'ZERO Orient Joint or Rotate')
    
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 15 )
    cmds.rowLayout( numberOfColumns = 4 ) 
    cmds.separator( style = 'single' , width = 10 )
    cmds.button( label = 'ORIENT', height = 18 , width = 70 , backgroundColor = [0.5, 0.5, 0.5] , command = 'ZEROrientRotate(orient)')
    cmds.separator( style = 'single' , width = 10 )
    cmds.button( label = 'ROTATE', height = 18 , width = 70 , backgroundColor = [0.5, 0.5, 0.5] , command = 'ZEROrientRotate(rotate)')
    
    cmds.showWindow('UIorientJoint')
    
UIorientJoint()