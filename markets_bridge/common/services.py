from common.models import (
    CategoryMatching,
    SystemEnvironment,
)


def get_recipient_category_id_by_category_mathing_id(category_mathing_id):
    return CategoryMatching.objects.only(
        'recipient_category_id',
    ).get(
        pk=category_mathing_id,
    ).recipient_category_id


def get_system_environments():
    return SystemEnvironment.objects.all()

def create_characteristic_matchings_by_category_and_matching():
    ...
# category_matching_id = request.POST
# category_matching = CategoryMatching.objects.get()
# recipient_characteristic_ids = Characteristic.objects.filter(
#     categories=instance.recipient_category_id,
# ).values_list(
#     'id',
#     flat=True,
# )
#
# char_matching_list = [
#     CharacteristicMatching(category_matching_id=instance.id, recipient_characteristic_id=char_id)
#     for char_id in recipient_characteristic_ids
# ]
#
# created_char_mathing_list = CharacteristicMatching.objects.bulk_create(char_matching_list)
#
# for char_mathing in created_char_mathing_list:
#     recipient_char_value_ids = CharacteristicValue.objects.filter(
#         characteristic_id=char_mathing.recipient_characteristic_id,
#     ).values_list(
#         'id',
#         flat=True,
#     )
#
#     char_value_mathing_list = [
#         CharacteristicValueMatching(
#             characteristic_matching_id=char_mathing.id,
#             recipient_characteristic_value_id=value_id,
#         )
#         for value_id in recipient_char_value_ids
#     ]
#
#     CharacteristicValueMatching.objects.bulk_create(char_value_mathing_list)
