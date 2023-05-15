import maya.cmds as cmds

def colorWindow():
	if cmds.window ('UIcolorOverride' , exists = True):
		cmds.deleteUI ('UIcolorOverride') 
	
	cmds.window('UIcolorOverride' , widthHeight=(120, 120) , title = 'Color Override')
	cmds.frameLayout('Color Override')
	cmds.button( label='disable' , backgroundColor = [1, 1, 1] , command = ('changeColor(0)'))
	cmds.button( label='', backgroundColor = [1, 1, 0] , command = ('changeColor(17)'))
	cmds.button( label='', backgroundColor = [0.1, 0.4, 0.2] , command = ('changeColor(7)'))
	cmds.button( label='', backgroundColor = [0, 1, 0] , command = ('changeColor(14)'))
	cmds.button( label='', backgroundColor = [0.2, 1, 0.6] , command = ('changeColor(19)'))
	cmds.button( label='', backgroundColor = [0.7, 0.3, 0.3] , command = ('changeColor(10)'))
	cmds.button( label='', backgroundColor = [1, 0, 0] , command = ('changeColor(13)'))
	cmds.button( label='', backgroundColor = [1, 0.8, 0.8] , command = ('changeColor(20)'))
	cmds.button( label='', backgroundColor = [0.2, 0, 0.6] , command = ('changeColor(5)'))
	cmds.button( label='', backgroundColor = [0, 0, 1] , command = ('changeColor(6)'))
	cmds.button( label='', backgroundColor = [0.1, 1, 1] , command = ('changeColor(18)'))
	cmds.button( label='', backgroundColor = [1, 0, 1] , command = ('changeColor(9)'))
	
	cmds.showWindow('UIcolorOverride')

def changeColor(nColor):
	objs = cmds.ls(selection = True , transforms = True )
	#print objs
		
	for o in objs:
		if nColor == 0:
			cmds.setAttr(o + '.overrideEnabled', 0)
		else:
			cmds.setAttr(o + '.overrideEnabled', 1)
		
		cmds.setAttr(o + ".overrideColor", nColor)
		
	cmds.select( deselect = True )
			
colorWindow()