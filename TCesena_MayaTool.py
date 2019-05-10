"""
Mass Shading Tool created by Tristan Cesena
Description: This tool allows for the user to quickly select and customize primitive maya objects of their choosing.
Once an object is created the user is allowed to create a random cluster of 25 clones of their object. The objects within the cluster have randomized scale,rotation and translation.
With the shader section, users can quickly create a pre-determined set of basic lambert shaders and then randomly assign them to their new cluster.
Once shading is finished, the user can select from a list of pre-set terrains to test their object cluster with a simple animation.
This simple animation involves the cluster falling down onto the newly created terrain and seeing how their active rigidbodies interact with the terrain's passive rigidbody.
"""
import maya.cmds as mc
import random as random
import math as math
import os
import sys
import OptionsWindowBaseClass

home = os.getenv("HOME")
print home


def MassShadingTool():
    win = TCesena_MayaTool()
    win.create()

class TCesena_MayaTool(OptionsWindowBaseClass.OptionsWindow):
    def __init__(self):
        OptionsWindowBaseClass.OptionsWindow.__init__(self)
        self.title = "Mass Shading Tool"
        self.size = (600,600)
        self.bgc = [0.0,0.3,0.3]
        
    def commandMenu(self):
        mc.text(label = "Object Creation",fn = "boldLabelFont")
        self.objectSelectionMenu = mc.optionMenu( label = "Select a Shape:")
        mc.menuItem( label = "Please Select")
        mc.menuItem( label = "Sphere")
        mc.menuItem( label = "Cube")
        mc.menuItem( label = "Cylinder")
        mc.menuItem( label = "Cone")
        mc.menuItem( label = "Torus")
        self.objectSubFloat = mc.intFieldGrp(label = "SubDivisions (X and Y)",numberOfFields = 2, value1=0, value2 =0)

        self.radiusFloat = mc.intSliderGrp(label = "Radius (Except Cube)",field = True, minValue = 0, maxValue = 5, value = 0)
        self.widthFloat = mc.intSliderGrp(label = "Width (Cube Only)",field = True, minValue = 0, maxValue = 5, value = 0)
        self.depthFloat = mc.intSliderGrp(label = "Depth (Cube Only)",field = True, minValue = 0, maxValue = 5, value = 0)
        self.heightFloat = mc.intSliderGrp(label = "Height (Cube Only)",field = True, minValue = 0, maxValue = 5, value = 0)

        mc.button(label = "Create Selected Object", bgc = [0.0,0.0,0.3], c = self.createItem)
        self.objectCount = mc.intSliderGrp(label = "Number of Objects", field = True, minValue = 0, maxValue = 50, value = 0)
        mc.button(label = "Scatter Objects", bgc = [0.0,0.0,0.3], c = self.Scatter)

        mc.separator(height = 20, style = "in")

        mc.text(label = "Shading Section",fn = "boldLabelFont")
        mc.button(label = "Create Shaders", bgc = [0.0,0.0,0.3], c = self.createShaders)
        mc.button(label = "Bake Objects", bgc = [0.0,0.0,0.3], c = self.bake_objects)
        mc.button(label = "Bake Shaders", bgc = [0.0,0.0,0.3], c = self.bake_shaders)
        mc.button(label = "Randomly Assign Shaders", bgc = [0.0,0.0,0.3], c = self.randomize_assign)

        mc.separator(height = 20, style = "in")
        
        mc.text(label = "Terrain Section",fn = "boldLabelFont")
        self.terrainBox = mc.textField(text = "Nothing Selected")
        mc.button(label = "Browse",bgc = [0.0,0.0,0.3], c = self.getTerrain)
        mc.button(label = "Import",bgc = [0.0,0.0,0.3], c = self.importTerrain)

        
        mc.button(label = "Add Dynamics", bgc = [0.0,0.0,0.3], c = self.addDynamics)

        mc.separator(height = 20, style = "in")
        mc.text(label = "Animation Section", fn = "boldLabelFont")
        mc.button(label = "Play Animation", bgc = [0.0,0.0,0.3], c = self.playAnimation)
    
    def createItem(self,*args):
        self.item = mc.optionMenu(self.objectSelectionMenu, query = True, value = True)        
        if self.item == "Sphere":
            self.xSubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value1= True)
            self.ySubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value2= True)
            self.radiusInput = mc.intSliderGrp(self.radiusFloat, query = True, value = True)
            mc.polySphere(n = "mySphere",sx = self.xSubInput, sy = self.ySubInput, r = self.radiusInput)
        elif self.item == "Cube":
            self.xSubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value1= True)
            self.ySubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value2= True)
            self.widthInput = mc.intSliderGrp(self.widthFloat, query = True, value = True)
            self.depthInput = mc.intSliderGrp(self.depthFloat, query = True, value = True)
            self.heightInput = mc.intSliderGrp(self.heightFloat, query = True, value = True)
            mc.polyCube(n = "myCube", sx = self.xSubInput, sy = self.ySubInput, w = self.widthInput, d = self.depthInput, h = self.heightInput)
        elif self.item == "Cylinder":
            self.xSubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value1= True)
            self.ySubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value2= True)
            self.radiusInput = mc.intSliderGrp(self.radiusFloat, query = True, value = True)
            mc.polyCylinder(n = "myCylinder",sx = self.xSubInput, sy = self.ySubInput, r = self.radiusInput)
        elif self.item == "Cone":
            self.xSubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value1= True)
            self.ySubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value2= True)
            self.radiusInput = mc.intSliderGrp(self.radiusFloat, query = True, value = True)
            mc.polyCone(n = "myCone",sx = self.xSubInput, sy = self.ySubInput, r = self.radiusInput)
        elif self.item == "Torus":
            self.xSubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value1= True)
            self.ySubInput = mc.intFieldGrp(self.objectSubFloat, query = True, value2= True)
            self.radiusInput = mc.intSliderGrp(self.radiusFloat, query = True, value = True)
            mc.polyTorus(n = "myTorus",sx = self.xSubInput, sy = self.ySubInput, r = self.radiusInput)
            
    getSelectedObjects = []
    getSelectedShaders = []

    def createShaders(self,*args):
        self.red_lambert = mc.shadingNode("lambert", asShader = True)
        mc.setAttr(( self.red_lambert + ".color"), 1.0,0.0,0.0, type = 'double3')
    
        self.yellow_lambert = mc.shadingNode("lambert", asShader = True)
        mc.setAttr(( self.yellow_lambert + ".color"), 1.0,1.0,0.0, type = 'double3')
    
        self.green_lambert = mc.shadingNode("lambert", asShader = True)
        mc.setAttr(( self.green_lambert + ".color"), 0.0,1.0,0.0, type = 'double3')
    
        self.cyan_lambert = mc.shadingNode("lambert", asShader = True)
        mc.setAttr(( self.cyan_lambert + ".color"), 0.0,1.0,1.0, type = 'double3')
    
        self.blue_lambert = mc.shadingNode("lambert", asShader = True)
        mc.setAttr(( self.blue_lambert + ".color"), 0.0,0.0,1.0, type = 'double3')
    
        self.pink_lambert = mc.shadingNode("lambert", asShader = True)
        mc.setAttr(( self.pink_lambert + ".color"), 1.0,0.0,1.0, type = 'double3')
            
    def bake_objects(self,*args):
        self.objects = mc.ls(sl=True)
        del self.getSelectedObjects[:]
        for self.item in self.objects:
            self.getSelectedObjects.append(self.item)
        print self.getSelectedObjects
    
    def bake_shaders(self,*args):
        self.shaders = mc.ls(sl=True)
        del self.getSelectedShaders[:]
        for self.item in self.shaders:
            self.getSelectedShaders.append(self.item)
        print self.getSelectedShaders
    
    def randomize_assign(self,*args):
        self.shaderCount = len(self.getSelectedShaders)
        for self.item in self.getSelectedObjects:
            self.randNumber = random.random()
            self.roundNumber = math.floor(self.randNumber*(self.shaderCount))
            self.intNumber = int(self.roundNumber)
            mc.select(self.item)
            self.shaderName = self.getSelectedShaders[self.intNumber]
            mc.hyperShade( assign=self.shaderName)
        mc.select(clear=True)
 
    def Scatter(self,*args):
        self.result = mc.ls(orderedSelection = True)
        self.transformName = self.result[0]
        self.instanceGroupName = mc.group(empty = True, name = self.transformName +'_duplicate_grp#')
        self.objectInput = mc.intSliderGrp(self.objectCount,query = True, value = True)
        for i in range(0,self.objectInput):
            self.instanceResult = mc.duplicate(self.transformName, name = self.transformName + '_child#')
            mc.parent( self.instanceResult, self.instanceGroupName )
        
            self.xTrans = random.uniform( -50 , 50 )
            self.yTrans = random.uniform( 0 , 50 )
            self.zTrans = random.uniform( -50 , 50 )
        
            mc.move( self.xTrans, self.yTrans, self.zTrans, self.instanceResult )
    
            self.xRot = random.uniform( 0, 360 )
            self.yRot = random.uniform( 0, 360 )
            self.zRot = random.uniform( 0, 360 )
    
            mc.rotate( self.xRot, self.yRot, self.zRot, self.instanceResult )
    
            self.scalingFactor = random.uniform( 0.3, 1.5 )
    
            mc.scale( self.scalingFactor, self.scalingFactor, self.scalingFactor, self.instanceResult )

            mc.xform( self.instanceGroupName, centerPivots=True )
            
    def addDynamics(self,*args):
        for i in self.scene_before:
            self.obj = mc.listRelatives(i, p = True)
            mc.select(self.obj)
            mc.rigidBody( active = True, mass = 10, initialVelocity = (0.0,0.0,0.0), bounciness = 1, dynamicFriction = 0.8, damping = 0.2)
            self.G = mc.gravity(directionX = 0.0, directionY = -1.0, directionZ = 0.0, magnitude = 100)
            mc.connectDynamic(*self.obj, f = self.G)
            
    def playAnimation(self,*args):
        mc.playbackOptions(edit = True, animationStartTime = 1, animationEndTime = 100, minTime = 0, maxTime = 100, fps = 60)
        mc.playblast(f = "Animation Test")

    def getTerrain(self,*args):
        self.mbFilter = "*.mb"
        self.terrainName = mc.fileDialog2(caption = "Select Terrain",fileFilter = self.mbFilter, okCaption = "Choose",fileMode = 1)[0]
        mc.textField(self.terrainBox,edit = True, text = str(self.terrainName))
        
    def importTerrain(self,*args):
        self.scene_before = mc.ls(type = "mesh")
        print self.scene_before
        mc.file(self.terrainName,i = True)
        self.scene_after = mc.ls(type = "mesh")
        print self.scene_after
        self.newObj = list(set(self.scene_after) - set(self.scene_before))
        print self.newObj
        mc.select(self.newObj)
        self.groundRS = mc.rigidSolver(create = True, name = "rigidSolver1", s = 1.0, ct = 1.0)
        self.groundRB = mc.rigidBody(passive = True, solver = "rigidSolver1", bounciness = 0.5, damping = 0.8, staticFriction = 1.0)
        mc.select(clear = True)
        
        

MassShadingTool()

#Select/Create Shape function
"""
the createItem definition takes the selection that the user made from the drop-down menu and creates the assigned object
with the available attributes the user also defined.
"""
#Bake Objects/Shaders Functions
"""
The createShaders definition creates 6 pre-determined lambert shaders that are later used when assigning to objects.
The bake_objects and bake_shaders definitions add the selected objects and shaders to empty arrays.
The randomize_assign definition uses random and math modules to randomly assign the objects of the shader array to the objects of the object array.
"""
#Scatter Function
"""
The scatter definition takes the object the user created and creates a cluster-like formation with 50 clones of said object.
Rotation,Translation, and Scale are each randomized for each clone.
"""
#Dynamics Function
"""
The addDyanmics definition takes all of the objects in the scene, at this point would be the cluster, and applies active rigidbodies to them.
Finally gravity is added to the objects so the user can see the interaction between the ground and objects when they hit the play button.
"""
#Animation Function
"""
The play Animation definition pre-sets the playback options for the animation created from addDynamics.
It also playblasts the animation and saves it out as a video for the user to see with no viewport lag.
"""
#Terrain Functions
"""
The getTerrain definition allows the user to select any .mb of their choosing that they may already have to use as the ground terrain for the scene.
The importTerrain definition imports the user's selected .mb file and imports it. As the object is imported it applies a passive rigidbody to it.
"""
