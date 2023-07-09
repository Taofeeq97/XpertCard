# Third-party imports
from rest_framework import serializers
from rest_framework.reverse import reverse

# Local imports
from .models import ExpertCard, CompanyAddress, ActivityLog
from .utils import generate_qr_code
from admin_account.models import CustomAdminUser
from admin_account.serializers import CreateCustomAdminUserSerializer


class CompanyAddressSerializer(serializers.ModelSerializer):
    retrieve_update_delete_url=serializers.SerializerMethodField()

    class Meta:
        model = CompanyAddress
        fields = ('address_title', 'retrieve_update_delete_url', 'company_address', 'city', 'country', 'latitude', 'longitude')
    
    def validate_address_title(self, value):
        if CompanyAddress.objects.filter(address_title=value).exists():
            raise serializers.ValidationError('Inputed company title already exists')
        return value
    
    def validate(self, attrs):
        latitude = attrs['latitude']
        longitude = attrs['longitude']
        if CompanyAddress.active_objects.filter(latitude=latitude, longitude=longitude).exists():
            raise serializers.ValidationError('A company already exist in this same latitude and longitude')
        return super().validate(attrs)

    def get_retrieve_update_delete_url(self, obj):
        request = self.context.get('request')
        url= reverse('company_address_detail_create_update_delete', args=[str(obj.slug)], request=request)
        return url


class ExpertCardSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    retrieve_update_delete_url = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = ExpertCard
        fields = ('retrieve_update_delete_url', 'full_name', 'first_name', 'middle_name', 'last_name', 'email',
                  'profile_picture', 'qr_code', 'role', 'tribe', 'company_address', 'address', 'city', 'country',
                  'phone_number', 'created_date')
        read_only_fields = ('qr_code', 'address',)
        extra_kwargs = {
            'company_address': {'write_only': True},
            'created_date': {'read_only': True},
            'qr_code': {'read_only': True},       
        }

    def get_created_date(self, obj):
        date = obj.created_date
        refined_date = date.date().isoformat()
        return refined_date

    def validate_email(self, value):
        if not value.endswith(('afexafricaexchange.com', 'afexafrica', 'afexnigeria.com')):
            raise serializers.ValidationError('Invalid email format')
        return value

    def get_address(self, obj):
        address_id = obj.company_address.id
        comp_address = CompanyAddress.objects.get(id=address_id)
        serializer = CompanyAddressSerializer(comp_address, context=self.context)
        return serializer.data['retrieve_update_delete_url']

    def get_full_name(self, obj):
        first_name = obj.first_name.capitalize()
        middle_name = obj.middle_name.capitalize() if obj.middle_name else ""
        last_name = obj.last_name.upper()
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        return full_name
    
    def get_retrieve_update_delete_url(self, obj):
        request = self.context.get('request')
        url= reverse('expert_card_detail_create_update_delete', args=[str(obj.id)], request=request)
        return url

    def create(self, validated_data):
        qr_code = generate_qr_code(validated_data)
        validated_data['qr_code']=qr_code
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)
        email = validated_data.get('email', instance.email)
        city = validated_data.get('city', instance.city)
        country = validated_data.get('country', instance.country)
        phone_number = validated_data.get('phone_number', instance.phone_number)
        role = validated_data.get('phone_number', instance.role)
        tribe = validated_data.get('phone_number', instance.tribe)
        updated_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'city': city,
            'country': country,
            'phone_number': phone_number,
            'tribe':tribe,
            'role':role
        }
        qr_code = generate_qr_code(updated_data)
        validated_data['qr_code'] = qr_code
        return super().update(instance, validated_data)


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



