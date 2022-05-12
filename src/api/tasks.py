import uuid
from tempfile import NamedTemporaryFile

import requests
from django.core.files import File
from one_model import celery_app

from .models import BlenderProject, GeneratorTask


# Needed for refreshing data in Blender
def update_data(filepath, data, bpy):
    print("Updating data")

    bpy.ops.wm.open_mainfile(filepath=filepath)

    bpy.data.texts["data.csv"].from_string(data)

    bpy.ops.wm.save_as_mainfile(filepath=filepath)

    bpy.ops.wm.window_close()


@celery_app.task
def generator_task(id: str, project_id: str, data: str, file_format: str):
    generator_task = GeneratorTask.objects.get(pk=id)
    generator_task.status = GeneratorTask.RUNNING
    generator_task.save()

    project_file = BlenderProject.objects.get(pk=project_id).file

    import bpy

    bpy.context.scene.render.engine = "CYCLES"

    update_data(project_file.path, data, bpy)

    bpy.ops.wm.open_mainfile(filepath=project_file.path)
    bpy.ops.preferences.addon_enable(module="sverchok-master")

    s_nodes = bpy.data.node_groups[0]

    text_in = s_nodes.nodes["Text in+"]
    text_in.reload()

    with NamedTemporaryFile() as t_file:

        tmp_name = f"{t_file.name}.png"

        bpy.context.scene.render.filepath = tmp_name
        bpy.ops.render.render(write_still=True)

        bpy.ops.wm.window_close()

        output_file = File(open(tmp_name, "rb"))

        generator_task.output_file.save(f"{uuid.uuid4()}.{file_format}", output_file)
        generator_task.status = GeneratorTask.COMPLETED
        generator_task.save()

        requests.patch(
            generator_task.callback_url,
            {"image_url": generator_task.output_file.url, "status": "generated"},
        )
