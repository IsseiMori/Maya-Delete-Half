#deleteHalf.py 2017 Issei Mori
#Python script for Autodesk Maya to delete the faces on the half side
"""
1.Place this file into the scripts folder,
2.Paste the code below in your python Script Editor

import deleteHalf
reload(deleteHalf)
deleteHalf.Window()

3.Click "Save Script to Shell" in the Script Editor menu bar to save this script in your shellf
"""

from maya import cmds

#Delete the faces on the negative side of the palne
def deleteHalf(nodes = None, plane = "yz", isRightSide = True):
    #if no object is selected, return error
    if not nodes:
        nodes = cmds.ls(sl = True)

    if not nodes:
        cmds.error("No object is selected")

    #Find out the element number to check depends on plane
    if plane == "xy": #z value
        start = 2
    elif plane == "yz": #x value
        start = 0
    elif plane == "xz": #y value
        start = 1
    else:
        cmds.error("Unknown axis")

    #for loop for every object selected
    for node in nodes:
        #convert object to faces
        faces = cmds.polyListComponentConversion(node, toFace = True)
        cmds.select(faces)        
        faces = cmds.ls(sl = True, fl = True)

        #list of deleting faces
        deletingFaces = []

        #Check each face
        for face in faces:
            #convert face to vertices
            vertices = cmds.polyListComponentConversion(face, fromFace = True, toVertex = True)
            cmds.select(vertices)
            vertices = cmds.ls(sl = True, fl = True)
            
            #for loop for every vertex in the face
            for vertex in vertices:
                #Store world coordinate of the vertex
                ws = cmds.xform(vertex, q = True, t = True, ws = True)

                #add to the deletingFaces list if the vertex is in the deleting side
                if (ws[start] > 0 and isRightSide) or (ws[start] < 0 and not isRightSide):
                    deletingFaces.append(face)
                    break

        #delete all the deleting faces
        cmds.delete(deletingFaces)

class Window(object):
    def __init__(self):
        self.name = "deleteHalf"
        #close the current window if the same name window exists
        if cmds.window(self.name, query = True, exists = True):
            cmds.deleteUI(self.name)

        #open window
        window = cmds.window(self.name)

        #build UI
        self.buildUI()

        #show window
        cmds.showWindow()
        cmds.window(window, edit = True, height = 100, width = 200)
    
    def buildUI(self):
        #set up column
        column = cmds.columnLayout()

        #radio button for axis
        cmds.frameLayout(label = "Choose the mirroring plane")
        cmds.gridLayout(numberOfColumns = 3, cellWidth = 50)
        cmds.radioCollection()
        self.xyPlane = cmds.radioButton(label = "xy")
        self.yzPlane = cmds.radioButton(label = "yz", select = True)
        self.xzPlane = cmds.radioButton(label = "xz")

        cmds.setParent(column)
        cmds.frameLayout(label = "Choose the side to be deleted")
        cmds.gridLayout(numberOfColumns = 2, cellWidth = 70)
        cmds.radioCollection()
        self.left = cmds.radioButton(label = "Negative")
        self.right = cmds.radioButton(label = "Positive", select = True)

        #run button
        cmds.button(label = "Delete", command = self.onApplyClick)

    def onApplyClick(self, *args):
        if cmds.radioButton(self.xyPlane, q = True, select = True):
            plane = "xy"
        elif cmds.radioButton(self.yzPlane, q = True, select = True):
            plane = "yz"
        else:
            plane = "xz"
        
        if cmds.radioButton(self.right, q = True, select = True):
            isRightSide = True
        else:
            isRightSide = False

        #run deleteHalf method
        deleteHalf(plane = plane, isRightSide = isRightSide)

        #close window to end
        cmds.deleteUI(self.name)