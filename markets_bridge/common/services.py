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
    venv_path = '~/ozon-inloader/venv/bin/activate'
    activate_command = f'. {venv_path} && '
    file_path = '~/ozon-inloader/src/main.py'
    arguments = (f'--category_id {external_category_id}',)
    command = activate_command + f'python {file_path} ' + ' '.join(arguments)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
