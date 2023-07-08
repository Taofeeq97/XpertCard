# Django imports
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

# Local imports
from .models import ExpertCard, CompanyAddress



@registry.register_document
class ExpertCardDocument(Document):
    class Index:
        name = 'xpertcards_index'

    first_name = fields.TextField(attr='first_name')
    last_name = fields.TextField(attr='last_name')
    email = fields.TextField(attr='email')
    profile_picture = fields.FileField(attr='profile_picture')
    role = fields.TextField(attr='role', default='')
    qr_code = fields.FileField(attr='qr_code')
    tribe = fields.TextField(attr='tribe')
    company_address = fields.ObjectField(properties={
        'address_title': fields.TextField(),
        'slug': fields.TextField(),
        'company_address': fields.TextField(),
        'city': fields.TextField(),
        'country': fields.TextField(),
        'latitude': fields.TextField(),
        'longitude': fields.TextField(),
    })
    city = fields.TextField(attr='city')
    country = fields.TextField(attr='country')
    phone_number = fields.TextField(attr='phone_number.as_national')

    class Django:
        model = ExpertCard

    def get_queryset(self):
        return super().get_queryset().select_related('company_address')

    def get_instances_from_related(self, related_instance):
        # Override this method to return the related instance(s) for serialization
        if isinstance(related_instance, CompanyAddress):
            return related_instance
        return super().get_instances_from_related(related_instance)