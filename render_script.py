import bpy

bpy.ops.wm.open_mainfile(filepath="blender_projects/test/prototype.blend")
bpy.ops.preferences.addon_enable(module="sverchok-master")

with open("blender_projects/test/data2.csv", "r") as f:
    data = f.read()
    bpy.data.texts["data.csv"].from_string(data)

s_nodes = bpy.data.node_groups[0]
text_in = s_nodes.nodes["Text in+"]

text_in.reload()

bpy.ops.render.render(write_still=True)
