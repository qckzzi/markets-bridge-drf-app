import os
import subprocess

from common.models import (
    CategoryMatching,
)


def get_recipient_category_id_by_category_mathing_id(category_mathing_id):
    return CategoryMatching.objects.only(
        'recipient_category_id',
    ).get(
        pk=category_mathing_id,
    ).recipient_category_id


# TODO: Удалить эту порнографию, Markets-Bridge не должен знать о сторонних сервисах
def update_recipient_attributes(external_category_id: int):
    path = os.getenv('OZON_INLOADER_PATH')
    venv_path = f'{path}/venv/bin/activate'
    activate_command = f'. {venv_path} && '
    file_path = f'{path}/src/main.py'
    arguments = (f'--category_id {external_category_id}',)
    command = activate_command + f'python {file_path} ' + ' '.join(arguments)
    subprocess.run(command, shell=True)
