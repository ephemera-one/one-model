import bpy

bpy.ops.preferences.addon_install(overwrite=True, filepath="addons/sverchok.zip")
bpy.ops.preferences.addon_enable(module="sverchok-master")
bpy.ops.wm.save_userpref()
