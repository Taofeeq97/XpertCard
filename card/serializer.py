# Third-party imports
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.utils.text import slugify

# Local imports
from admin_account.models import CustomAdminUser
from admin_account.serializers import CreateCustomAdminUserSerializer
from .models import ExpertCard, CompanyAddress, ActivityLog
from .utils import generate_qr_code, create_vcf_file


class CompanyAddressSerializer(serializers.ModelSerializer):
    retrieve_update_delete_url=serializers.SerializerMethodField()

    class Meta:
        model = CompanyAddress
        fields = ('id','address_title', 'retrieve_update_delete_url', 'company_address', 'city', 'country', 'latitude', 'longitude')
    
    def validate_address_title(self, value):
        if CompanyAddress.objects.filter(address_title=value).exists():
            raise serializers.ValidationError('Inputed company title already exists')
        return value

    def validate(self, attrs):
        latitude = attrs['latitude']
        longitude = attrs['longitude']
        if longitude and not longitude.endswith(('N', 'W', 'S', 'E')):
            raise serializers.ValidationError('Invalid longitude format')
        if latitude and not latitude.endswith(('N', 'W', 'S', 'E')):
            raise serializers.ValidationError('Invalid latitude format')
        if CompanyAddress.active_objects.filter(latitude=latitude, longitude=longitude).exists():
            raise serializers.ValidationError('A company already exist in this same latitude and longitude')
        return super().validate(attrs)

    def get_retrieve_update_delete_url(self, obj):
        request = self.context.get('request')
        url= reverse('company_address_detail_create_update_delete', args=[int(obj.id)], request=request)
        return url


class ExpertCardSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    retrieve_update_delete_url = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = ExpertCard
        fields = ('id', 'retrieve_update_delete_url', 'full_name', 'first_name', 'middle_name', 'last_name', 'email', 'profile_picture', 'role', 'tribe','card_vcf', 'qr_code', 'company_address', 'address', 'address_title', 'card_type', 'phone_number', 'created_date', 'is_active')
        read_only_fields = ('qr_code', 'address', 'card_vcf','is_active', 'address_title')
        extra_kwargs = {
            'company_address': {'write_only': True},
            'created_date': {'read_only': True},
            'qr_code': {'read_only': True},
        }

    def validate_email(self, value):
        if not value.endswith(('afexafricaexchange.com', 'afexafrica.com', 'afexnigeria.com')):
            raise serializers.ValidationError('Invalid email format')
        return value
    
    def get_created_date(self, obj):
        refined_date = obj.created_date.date().isoformat()
        return refined_date
    
    def get_address(self, obj):
        address_id = obj.company_address.id
        try:
            comp_address = CompanyAddress.objects.get(id=address_id)
            serializer = CompanyAddressSerializer(comp_address, context=self.context)
            return serializer.data['retrieve_update_delete_url']
        except CompanyAddress.DoesNotExist:
            return None

    def get_full_name(self, obj):
        first_name = obj.first_name.capitalize()
        middle_name = obj.middle_name.capitalize() if obj.middle_name else ""
        last_name = obj.last_name.capitalize()
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        return full_name
    
    def get_retrieve_update_delete_url(self, obj):
        request = self.context.get('request')
        url= reverse('expert_card_detail_create_update_delete', args=[str(obj.id)], request=request)
        return url

    def create(self, validated_data):
        validated_data['address_title'] = validated_data['company_address'].address_title
        request = self.context.get('request')
        qr_code_image = generate_qr_code(validated_data, request)
        card_vcf = create_vcf_file(validated_data)

        # Save the QR code image in the QR code field
        validated_data['qr_code'] = qr_code_image
        validated_data['card_vcf'] = card_vcf
        return super().create(validated_data)


    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)
        email = validated_data.get('email', instance.email)
        phone_number = validated_data.get('phone_number', instance.phone_number)
        address_title = validated_data.get('address_title', instance.address_title)
        role = validated_data.get('phone_number', instance.role)
        tribe = validated_data.get('phone_number', instance.tribe)
        
        # Prepare the updated_data dictionary
        updated_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'address_title': address_title,
            'tribe': tribe,
            'role': role
        }

        # Update the instance fields with the new data
        instance.first_name = first_name
        instance.last_name = last_name
        instance.email = email
        instance.phone_number = phone_number
        instance.address_title = address_title
        instance.role = role
        instance.tribe = tribe
        card_vcf = create_vcf_file(updated_data)
        instance.card_vcf.save(f"{slugify(email)}.vcf", card_vcf, save=False)
    
        
        # Save the instance with the updated fields
        instance.save()
        return instance


class ActivityLogSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = ('actor','action_type','time_since', 'status', 'content_type','data')

    def get_actor(self, obj):
        actor = obj.actor
        if actor is not None:
            user_id = actor.id
            user = CustomAdminUser.objects.get(id=user_id)
            serializer = CreateCustomAdminUserSerializer(user, context=self.context)
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']
            return first_name + ' ' + last_name
        return None

    def get_content_type(self, obj):
        content_type = obj.content_type
        if content_type is not None:
            return content_type.model
        return None
    

class ExpertCardIdsSerializer(serializers.Serializer):
    expert_card_ids = serializers.ListField(child=serializers.IntegerField())



# class ExpertCardElasticSearchSerializer(serializers.Serializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#     role = serializers.CharField()
#     qr_code = serializers.CharField()
#     profile_picture  = serializers.CharField()
#     tribe = serializers.CharField()
#     company_address = serializers.DictField(child=serializers.CharField())
#     card_type = serializers.CharField()
#     phone_number = serializers.CharField()
#     is_active = serializers.BooleanField()
#     is_deleted = serializers.BooleanField()
#     created_date = serializers.DateTimeField()
#     updated_date = serializers.DateTimeField()

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         request = self.context.get('request')
#         company_address_slug = instance['company_address']['slug']
#         expert_card =ExpertCard.objects.get(email = instance['email'])
#         serialized_expert_card = ExpertCardSerializer(expert_card)
#         company_address = CompanyAddress.objects.get(slug=company_address_slug)
#         serializer = CompanyAddressSerializer(company_address)

#         if request is not None:
#             retrieve_update_delete_url = serializer.data['retrieve_update_delete_url']
#             expertcard_url = serialized_expert_card.data['retrieve_update_delete_url']
#             representation['company_address'] = request.build_absolute_uri(retrieve_update_delete_url)
#             representation['retrieve_update_delete_url'] = request.build_absolute_uri(expertcard_url)
            
#         return representation
    
    
    


