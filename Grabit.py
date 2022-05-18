import maya.cmds as cmds
import pymel.core as pm

'''
Components need to be selected in the correct order:
first select the wrist IK control
second the object Joint
then the object Locator for the Aim constraint

'''
# Grab the selection and put it in a list variable called itemJoint
itemJoint = cmds.ls(sl=True)
 
#create an unambiguous control made of two circles crossing eachother
circle1 = cmds.circle(normal=[0,1,1], n = 'Circle1', r = 2)

circle2 = cmds.circle(normal=[0,1,-1], n = 'Circle2', r = 2)

Control1 = cmds.group(em = True, name = 'Item_Base_Ctrl')

# hiding the base control for the object as it causes too many problems when used
cmds.hide(Control1, rh=True)

cmds.parent(circle2[0] + 'Shape', Control1, s = True, r = True)

cmds.parent(circle1[0] + 'Shape', Control1, s = True, r = True)

cmds.delete(circle1[0])

cmds.delete(circle2[0]) 

cmds.select(clear=True)

cmds.select(Control1)

itemPad = cmds.group(Control1, n='Item_Base_Pad')

# relocate and parent the base control to the staffs base joint
padParent = cmds.parentConstraint(itemJoint[1], itemPad)

cmds.delete(itemPad + '_parentConstraint1')

cmds.parentConstraint(Control1, itemJoint[1])

itemAimPad = cmds.group(em=True, n='Item_Locator_Pad')

cmds.pointConstraint(itemJoint[2], itemAimPad)

cmds.delete(itemAimPad + '_pointConstraint1')

#put the locator component in a pad
cmds.parent( itemJoint[2], itemAimPad)

cmds.aimConstraint(itemJoint[2], itemPad, mo=True, n='Item_Aim_Constraint')

# create a circle control for the staffs aim constraint, and place it in the aimControl variable
aimControl = cmds.circle(normal=[0, 1, 0], n='Item_Aim_Ctrl')

# relocate aimControl, parent and hide the locator under it
cmds.pointConstraint(itemAimPad, aimControl)

cmds.delete(aimControl[0] + '_pointConstraint1')

cmds.parent(itemAimPad, aimControl)

#create a pad for the aim control and place it in the aimCtrlPad variable
aimCtrlPad = cmds.group(em=True, n='Item_Aim_Pad')

cmds.pointConstraint(aimControl, aimCtrlPad)

cmds.delete(aimCtrlPad + '_pointConstraint1')

cmds.parent(aimControl, aimCtrlPad)

#create a locator, reposition it to the staffs base joint and put in the baseLocator variable
baseLocator = cmds.spaceLocator(n='Item_Base')

cmds.parentConstraint(itemJoint[1], baseLocator,)

cmds.delete(str(baseLocator[0]) + '_parentConstraint1')

#parent the baseLocator to the selected wrist component with a parent constraint
cmds.parentConstraint(itemJoint[0], baseLocator, mo=True)

#parent the item base control pad to the base locator with a point constraint and name the parent node holdConstraint
cmds.pointConstraint(baseLocator, itemPad, mo=True, n='holdConstraint')

cmds.select(itemJoint[0])

#make the baseLacator a string and put it in the wristIKStr variable
wristIKStr = str(baseLocator[0])

# add an attribute to the wrist component that switches the holdConstraint node on and off allowing the staff to be "let go"
cmds.addAttr(at='int', dv = 0, k=True, max = 1, ln='wristParent', proxy = 'holdConstraint.' + wristIKStr + 'W0')

#parent the aim control pad to the Wrist IK for ease of use, need to expand upon this in later versions
cmds.parentConstraint(itemJoint[0], aimCtrlPad, mo=True)

#Hide the base locator
cmds.hide(baseLocator[0], returnHidden=True)

#Hide the pad for the aim locator
cmds.hide(itemAimPad, returnHidden=True)



