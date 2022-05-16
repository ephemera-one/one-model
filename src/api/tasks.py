from tempfile import NamedTemporaryFile

import requests
from django.core.files import File
from one_model import celery_app

from .models import BlenderProject, GeneratorTask


@celery_app.task
def generator_task(id: str, project_id: str, data: str, file_format: str):
    import bpy

    def clean_blocks():
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)

    # Needed for refreshing data in Blender
    def update_data(filepath, data):
        print("Updating data")

        bpy.ops.wm.open_mainfile(filepath=filepath)

        bpy.data.texts["data.csv"].from_string(data)

        bpy.ops.wm.save_as_mainfile(filepath=filepath)

        bpy.ops.wm.window_close()

    generator_task = GeneratorTask.objects.get(pk=id)
    generator_task.status = GeneratorTask.RUNNING
    generator_task.save()

    project_file = BlenderProject.objects.get(pk=project_id).file

    bpy.context.scene.render.engine = "CYCLES"

    update_data(project_file.path, data)

    bpy.ops.wm.open_mainfile(filepath=project_file.path)
    bpy.ops.preferences.addon_enable(module="sverchok-master")

    s_nodes = bpy.data.node_groups[0]

    text_in = s_nodes.nodes["Text in+"]
    text_in.reload()

    with NamedTemporaryFile() as t_file:

        tmp_name = f"{t_file.name}.png"

        bpy.context.scene.render.filepath = tmp_name
        bpy.ops.render.render(write_still=True)

        output_file = File(open(tmp_name, "rb"))

        generator_task.output_file.save(
            f"living_nft_{generator_task.id}.{file_format}",
            output_file,
        )  # TODO: Move file prefix to settings

        generator_task.status = GeneratorTask.COMPLETED
        generator_task.save()

    callback_url = generator_task.callback_url

    if callback_url:
        requests.patch(
            callback_url,
            {"image_url": generator_task.output_file.url, "status": "generated"},
        )

    clean_blocks()

    bpy.ops.wm.window_close()

    # bpy.ops.wm.read_factory_settings()
