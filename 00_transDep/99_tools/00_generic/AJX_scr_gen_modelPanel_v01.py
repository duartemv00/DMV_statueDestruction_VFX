import maya.cmds as cmds

#Create a new camera
if (cmds.objExists('myCamera1')) == False:
    cam = cmds.camera (n = 'myCamera1')
    cmds.setAttr ('myCamera1.visibility' , 0)

#Change the viewPort Camera to myCamera1
actualCam = cmds.getPanel (vis = True)
cmds.modelPanel (actualCam[0] , edit = True , camera = cam[0])


def panelPersp():
    cmds.viewSet(p=True)
    
def panelFront():
    cmds.viewSet(f=True)
    
def panelBack():
    cmds.viewSet(b=True)
    
def panelTop():
    cmds.viewSet(t=True)
    
def panelBott():
    cmds.viewSet(bo=True)
    
def panelLeft():
    cmds.viewSet(ls=True)
    
def panelRight():
    cmds.viewSet(rs=True)


#create window
def UImodelPanel():

    if cmds.window ('UImodelPanel' , exists = True):
        cmds.deleteUI ('UImodelPanel') 
          
    cmds.window('UImodelPanel' , widthHeight = (120, 170) , title = "Model Panel")
    
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 5 )
    cmds.rowLayout( numberOfColumns = 2 )
    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 5 ) 
    cmds.rowLayout( numberOfColumns = 2 )
    cmds.separator( style = 'single' , width = 30 )
    cmds.button( label = 'PERSP', height = 18 , width = 40 , backgroundColor = [1, 1, 0] , command = 'panelPersp()')

    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 5 )
    cmds.rowLayout( numberOfColumns = 4 )
    cmds.separator( style = 'single' , width = 5 ) 
    cmds.button( label = 'FRONT', height = 18 , width = 40 , backgroundColor = [1, 0, 0] , command = 'panelFront()') 
    cmds.separator( style = 'single' , width = 5 )
    cmds.button( label = 'BACK', height = 18 , width = 40 , backgroundColor = [1, 0.5, 0.5] , command = 'panelBack()')
    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 5 )
    cmds.rowLayout( numberOfColumns = 4 )
    cmds.separator( style = 'single' , width = 5 ) 
    cmds.button( label = 'TOP', height = 18 , width = 40 , backgroundColor = [0, 1, 0] , command = 'panelTop()') 
    cmds.separator( style = 'single' , width = 5 )
    cmds.button( label = 'BOTT', height = 18 , width = 40 , backgroundColor = [0.5, 1, 0.5] , command = 'panelBott()')
    
    cmds.setParent( '..' )
    cmds.columnLayout()
    cmds.separator( style = 'none' , height = 5 )
    cmds.rowLayout( numberOfColumns = 4 )
    cmds.separator( style = 'single' , width = 5 ) 
    cmds.button( label = 'LEFT', height = 18 , width = 40 , backgroundColor = [0, 0, 1] , command = 'panelLeft()') 
    cmds.separator( style = 'single' , width = 5 )
    cmds.button( label = 'RIGHT', height = 18 , width = 40 , backgroundColor = [0.5, 0.5, 1] , command = 'panelRight()')
    
    cmds.showWindow('UImodelPanel') 
    
UImodelPanel()