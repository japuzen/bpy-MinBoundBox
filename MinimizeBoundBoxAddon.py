bl_info = {
    "name": "Minimize Bounding Box",
    "description": "Minimizes the bounding box of selected objects",
    "author": "Johnathan Apuzen",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Object > Minimize Bounding Box",
    "category": "Object",
}

import bpy
import random
from math import radians
from math import isclose

'''****************************************
CUSTOM FUNCTIONS
****************************************'''
#Make obj the only object selected
def selectOneObject(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

#create and return a decimated copy of object with the minimum decimation ratio that doesn't change bounding box size
def createDecimatedCopy(obj):
    #create copy
    selectOneObject(obj)
    bpy.ops.object.duplicate()
    #add decimate modifier to copy
    objDup = bpy.context.selected_objects[0]
    selectOneObject(objDup)
    bpy.ops.object.modifier_add(type='DECIMATE')
    
    oldDimensions = list(obj.dimensions)#store values of old dimensions
    boundBoxChangeFlag = False
    ratioList = list(range(1,100))
    
    #Find minimum decimate ratio that doesn't affect bounding box
    #check halfway of range, if bound box changes check higher half, if not check lower half
    #determines ideal ratio in less steps than brute force (checking every ratio from 0.99 - 0.01)
    while len(ratioList) > 1:
        midIndex = len(ratioList)//2
        bpy.context.object.modifiers["Decimate"].ratio = ratioList[midIndex] * 0.01
        bpy.context.evaluated_depsgraph_get().update()
        
        for i in range(3):
            #Check if dimensions are within 0.5% of each other
            if not isclose(oldDimensions[i], objDup.dimensions[i], rel_tol=0.005):
                boundBoxChangeFlag = True
                break
        
        if boundBoxChangeFlag:
            ratioList = ratioList[midIndex:]
        else:
            ratioList = ratioList[:midIndex]
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")    
    return objDup

#Finds the degree rotation along 1 axis that minimizes an object's volume
#Checks 0-90 degrees at a specified increment
def alignAxis(obj, axis, minVol):
    rotFinal = 0
    increment = 1/2#degree increments to check, 1/2 = check every half degree
    
    selectOneObject(obj)
    
    for i in range(1, int(90 / increment) + 1):
        obj.rotation_euler[axis] = radians(1 * increment)
        bpy.ops.object.transform_apply(location = False, rotation = True, scale = False)
        objVol = obj.dimensions.x * obj.dimensions.y * obj.dimensions.z
        
        if objVol < minVol:
            minVol = objVol
            rotFinal = i * increment
    
    obj.rotation_euler[axis] = radians(rotFinal - 90)
    bpy.ops.object.transform_apply(location = False, rotation = True, scale = False)
    
    return minVol, rotFinal

'''****************************************
MAIN FUNCTION
****************************************'''
class MinimizeBoundingBox(bpy.types.Operator):
    """Minimize the bounding box volume of selected objects"""
    bl_idname = "object.minimize_bounding_box"
    bl_label = "Minimize Bounding Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.ops.object.transform_apply(location = False, rotation = True, scale = False)
        selected_objects = list(bpy.context.selected_objects) #List of initially selected objects
        for obj in selected_objects:
            objDup = createDecimatedCopy(obj)
            
            numTrials = 5
            trials = [] #list of trial stats [minVol, rotInitialList, rotFinalList] for each trial
            #Each trial starts with a random rotation, and ends with min bound box and rotations that lead to final min bound box
            for trial in range(numTrials):        
                #create trial part
                selectOneObject(objDup)
                bpy.ops.object.duplicate()
                objTrial = bpy.context.selected_objects[0]
                
                #Initial random rotation
                selectOneObject(objTrial)
                bpy.ops.object.randomize_transform(random_seed = random.randint(1,10000),use_loc=False, rot=(3.14159, 3.14159, 3.14159), use_scale=False)
                #record initial rotation, recorded in *EULER*
                rotInitialList = [objTrial.rotation_euler[0], objTrial.rotation_euler[1], objTrial.rotation_euler[2]]
                bpy.ops.object.transform_apply(location = False, rotation = True, scale = False)
                
                rotFinalList = []
                minVol = objTrial.dimensions.x * objTrial.dimensions.y * objTrial.dimensions.z
                #Run align axis on XYZ twice to get min bound box
                #Record rotations made
                for i in range(2):
                    rotationList = []
                    for axis in range(3):
                        minVol, rotFinal = alignAxis(objTrial, axis, minVol)
                        rotationList.append(rotFinal)
                    rotFinalList.append(rotationList)
                
                finalVol = objTrial.dimensions.x * objTrial.dimensions.y * objTrial.dimensions.z
                trials.append([finalVol, rotInitialList, rotFinalList])
                #delete trial part
                bpy.ops.object.delete(use_global=False)
                
            
            #delete decimated copy
            selectOneObject(objDup)
            bpy.ops.object.delete(use_global=False)
            
            #determine which trial has least final vol
            minVol = trials[0][0]
            bestTrial = trials[0]
            for trial in trials:
                if trial[0] < minVol:
                    minVol = trial[0]
                    bestTrial = trial
            
            #apply rotations to original obj
            selectOneObject(obj)
            #initial rotation
            for axis in range(3):
                obj.rotation_euler[axis] = bestTrial[1][axis]
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = False)
            #final rotations
            for rotation in bestTrial[2]:
                for axis in range(3):
                    obj.rotation_euler[axis] = radians(rotation[axis])
                bpy.ops.object.transform_apply(location = False, rotation = True, scale = False)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MinimizeBoundingBox.bl_idname)


def register():
    bpy.utils.register_class(MinimizeBoundingBox)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MinimizeBoundingBox)
    bpy.types.VIEW3D_MT_object.remove(menu_func)