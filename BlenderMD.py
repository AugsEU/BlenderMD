bl_info = {
    "name": "Export BMD with SuperBMD",
    "author": "Augs",
    "version": (2, 1, 3),
    "blender": (2, 71, 0),
    "location": "File > Export > Gamecube/Wii model (.bmd)",
    "description": "This script allows you do export bmd files quickly using SuperBMD directly from blender",
    "warning": "Might break, doing this mostly for my own convinience",
    "category": "Import-Export"
}

import bpy
import os

from bpy_extras.io_utils import ExportHelper
from bpy.props import (BoolProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    )

class ExportBMD(bpy.types.Operator, ExportHelper):
    """Save an BMD Mesh file"""
    bl_idname = "export_mesh.bmd"
    bl_label = "Export BMD Mesh"
    filter_glob = StringProperty(
        default="*.bmd",
        options={'HIDDEN'},
    )

    check_extension = True
    filename_ext = ".bmd"
	
    rot = BoolProperty(
        name="Rotate",
        description="Use Z as up instead of Y",
        default=True,
        )
		
    OtherParams = StringProperty(
        name="Other parameters",
        description="stuff like -t -s that you add to the cmd command",
        default="",
    )
	
    SuperPath = StringProperty(
        name="SuperBMDPath",
        description="The path of folder containing SuperBMD.exe",
        default="C:\\Users\\August\\Downloads\\Sunshine ROM hacking\\SuperBMD\\", #bad!!! must find better way
    )	
	
	#To do: add material presets
	
    def execute(self, context):        # execute() is called by blender when running the operator.
        FBXPath = (self.filepath[:-3] + "fbx") #dodgy hey, changed file extension
        bpy.ops.export_scene.fbx(filepath=FBXPath, path_mode='ABSOLUTE') #Export out model as fbx
        Parameters = "" #Stuff like mat and that
        if(self.rot):
            Parameters = "--rotate"
        Parameters = Parameters + self.OtherParams
        os.chdir(self.SuperPath) #Change path
        os.system("SuperBMD.exe " + '"' + FBXPath + '" ' + Parameters)
        os.system("del " + '"' + FBXPath + '"') #delete fbx
        return {'FINISHED'}            # this lets blender know the operator finished successfully.
	


def register():
    bpy.utils.register_class(ExportBMD)
    bpy.types.INFO_MT_file_export.append(menu_func)

def menu_func(self, context):
    self.layout.operator(ExportBMD.bl_idname, text="Gamecuebe/Wii model (.bmd)")
    
def unregister():
    bpy.utils.unregister_class(ExportBMD)
    bpy.types.INFO_MT_file_export.remove(menu_func)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()