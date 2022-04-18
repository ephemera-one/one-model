import uuid
from tempfile import NamedTemporaryFile

from django.core.files import File
from one_model import celery_app

from .models import BlenderProject, GeneratorTask


@celery_app.task
def generator_task(id: str, project_id: str, data: str, file_format: str):
    generator_task = GeneratorTask.objects.get(pk=id)
    generator_task.status = GeneratorTask.RUNNING
    generator_task.save()

    project_file = BlenderProject.objects.get(pk=project_id).file

    import bpy

    bpy.ops.wm.open_mainfile(filepath=project_file.path)
    bpy.ops.preferences.addon_enable(module="sverchok-master")

    bpy.data.texts["data.csv"].from_string(data)

    s_nodes = bpy.data.node_groups[0]

    text_in = s_nodes.nodes["Text in+"]
    text_in.reload()

    with NamedTemporaryFile() as t_file:

        tmp_name = f"{t_file.name}.png"

        bpy.context.scene.render.filepath = tmp_name
        bpy.ops.render.render(write_still=True)

        output_file = File(open(tmp_name, "rb"))

        generator_task.output_file.save(f"{uuid.uuid4()}.{file_format}", output_file)
        generator_task.status = GeneratorTask.COMPLETED
        generator_task.save()
