from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import ExpertCard


@registry.register_document
class ExpertCardDocument(Document):
    class Index:
        name = 'expertcard_index'

    class Django:
        model = ExpertCard
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
