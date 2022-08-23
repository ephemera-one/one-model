import bpy

bpy.context.scene.render.engine = "CYCLES"

bpy.ops.wm.open_mainfile(filepath="blender_projects/test/nature_cognita_v45.blend")
bpy.ops.preferences.addon_enable(module="sverchok-master")

with open("blender_projects/test/data2.csv", "r") as f:
    print(bpy.data.texts["data.csv"].as_string())
    data = f.read()
    print(data)
    bpy.data.texts["data.csv"].from_string(data)

s_nodes = bpy.data.node_groups[0]
text_in = s_nodes.nodes["Text in+"]

text_in.reload()

bpy.ops.render.render(write_still=True)
