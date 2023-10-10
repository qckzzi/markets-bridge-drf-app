class BaseEnumerate:
    """Базовый класс для перечислений."""

    labels = dict()

    @classmethod
    def get_choices(cls):
        return cls.labels.items()
