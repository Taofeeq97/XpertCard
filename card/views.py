# Standard library imports
from django.db.models import Q

# Third-party imports
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend
)
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.text import slugify
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

# Local application or project-specific imports
from .activitylogmixin import ActivityLogMixin
from .document import ExpertCardDocument
from .models import ActivityLog, CompanyAddress, ExpertCard
from .pagination import StandardResultPagination, ActivityLogPagination
from .permissions import AdminOrTrustedUserOnly
from .serializer import (
    ActivityLogSerializer,
    CompanyAddressSerializer,
    ExpertCardIdsSerializer,
    ExpertCardSerializer,
)
from .utils import generate_qr_code, create_vcf_file

# Create your views here.


class CompanyAddressListApiView(generics.ListAPIView):
    """
    An endpoint to access Company Address List
    Authentication is required

    """
    pagination_class= StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    queryset = CompanyAddress.active_objects.all()
    serializer_class = CompanyAddressSerializer


class CompanyAddressCreateApiView(generics.CreateAPIView):
    """
    -An endpoint to create A company Address
    -Authentication is required

    """
    queryset = CompanyAddress.objects.all()
    pagination_class = StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = CompanyAddressSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            "message": "Address created successfully",
        }
        return Response(response, status=status.HTTP_201_CREATED)
    

class CompanyAddressDetailUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint to Access, Update or Delete A company Address instance
    Authentication is required

    """
    queryset = CompanyAddress.active_objects.all()
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = CompanyAddressSerializer
    lookup_url_kwarg = 'company_address_slug'
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        # Check if the address_title field is present in validated_data
        if 'address_title' in serializer.validated_data:
            new_address_title = serializer.validated_data['address_title']
            expert_cards = ExpertCard.objects.filter(company_address=instance)
            expert_cards.update(address_title=new_address_title)

            # Generate QR code for each updated ExpertCard associated with the new card title
            for expert_card in expert_cards:
                data = {
                    'first_name': expert_card.first_name,
                    'last_name': expert_card.last_name,
                    'email': expert_card.email,
                    'address_title': new_address_title,
                    'role': expert_card.role,
                    'phone_number': expert_card.phone_number,
                }

                card_vcf = create_vcf_file(data=data)
                expert_card.card_vcf.save(f"{slugify(expert_card.email)}.vcf", card_vcf, save=False)
                expert_card.save()  # Save each individual expert_card

        return Response(serializer.data, status=status.HTTP_200_OK)


    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=['is_deleted', 'is_active'])
        response = {
            "message": 'Address deleted successfully'
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    

class ActiveExpertCardListApiView(generics.ListAPIView):
    """
    An endpoint to Access ExpertCard List
    Authentication is required

    """
    queryset=ExpertCard.active_objects.filter(is_deleted = False).order_by('-created_date')
    pagination_class = StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = ExpertCardSerializer


class ExpertCardFilter(rest_framework.FilterSet):
    card_type = rest_framework.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ExpertCard
        fields = ['card_type']


class ExpertCardListApiView(generics.ListAPIView):
    """
    An endpoint to access the ExpertCard List.
    Authentication is required.
    with search functionalities using first name, last_name, email, or card_type
    """
    queryset = ExpertCard.objects.filter(is_deleted=False).order_by('-created_date')
    pagination_class = StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = ExpertCardSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ExpertCardFilter
    search_fields = ['first_name', 'last_name', 'email']


class ExpertCardCreateApiView(ActivityLogMixin, generics.CreateAPIView):
    """
    An endpoint to create Expertcard
    Authentication is required

    """
    queryset = ExpertCard.objects.all()
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = ExpertCardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Call the _create_activity_log method to create the activity log
        self._create_activity_log(serializer.instance, request)
        response = {
            "message": "Expert card created successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class ExpertCardRetrieveUpdateDeleteApiView(ActivityLogMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint to Access, Update or Delete A Expertcard instance
    Authentication is required

    """
    queryset = ExpertCard.objects.filter(is_deleted = False)
    serializer_class = ExpertCardSerializer
    permission_classes = [AdminOrTrustedUserOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'expert_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer=serializer)
        # Call the _create_activity_log method to create the activity log
        self._update_activity_log(serializer.instance, request)
        response = {
            "message":'Expertcard Updated Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields = ['is_deleted', 'is_active'])
        # Call the _create_activity_log method to create the activity log
        self._delete_activity_log(instance, request)
        response = {
            "message": "Expertcard deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class BulkActivateExpertCardApiView(generics.UpdateAPIView):
    """
    An endpoint to Bulk Update cards
    Authentication is required
    """
    queryset = ExpertCard.objects.all()
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = ExpertCardIdsSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expert_card_ids = serializer.validated_data['expert_card_ids']
        expert_cards = ExpertCard.objects.filter(id__in=expert_card_ids)
        expert_cards.update(is_active=True)
        response = {
            "message": "Cards Activated Successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class ActivityLogAPIView(generics.ListAPIView):
    """
    An endpoint to Access Activity log list
    Authentication is required

    """
    pagination_class = StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    queryset = ActivityLog.objects.filter(status='Success', action_type__in=['Create', 'Update', 'Delete'])
    serializer_class = ActivityLogSerializer


# class VCardAPIView(generics.RetrieveAPIView):
#     queryset = ExpertCard.objects.all()
#     serializer_class = ExpertCardSerializer

#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()

#         # Generate the vCard content
#         vcard = f"BEGIN:VCARD\nVERSION:3.0\n" \
#                 f"N:{instance.last_name};{instance.first_name}\n" \
#                 f"EMAIL:{instance.email}\n" \
#                 f"TEL:{instance.phone_number}\n" \
#                 f"ORG:AFEX,{instance.address_title}\n" \
#                 f"TITLE:{instance.role}\n" \
#                 f"END:VCARD"
#         print(vcard)
#         response = Response(vcard, content_type='text/vcard')
#         response['Content-Disposition'] = f'attachment; filename="{instance.email}.vcf"'
#         return response
    




















# class ExpertCardTestListApiView(DocumentViewSet):
#     document = ExpertCardDocument
    
#     """
#     An endpoint to access the ExpertCard List with Elasticsearch Func.
#     Authentication is required.
#     """

#     filter_backends = [
#         FilteringFilterBackend,
#         OrderingFilterBackend,
#         CompoundSearchFilterBackend,
#     ]

#     # Define the filtering fields
#     filter_fields = {
#         'first_name': 'first_name.raw',
#         'last_name': 'last_name.raw',
#         'email': 'email.raw',
#     }

#     # Define the ordering fields
#     ordering_fields = {
#         'first_name': 'first_name',
#         'last_name': 'last_name',
#         'created_date': 'created_date',
#     }

#     # Define the search fields
#     search_fields = (
#         'first_name',
#         'last_name',
#         'profile_picture',
#         'role',
#         'tribe',
#         'qr_code',
#         'company_address',
#         'city',
#         'country',
#         'phone_number'
#     )

#     def list(self, request, *args, **kwargs):
#         # Get the search query from the request
#         query = request.query_params.get('query')

#         # Build the Elasticsearch DSL search query
#         search = self.document.search()

#         # Apply filters based on query parameters
#         if query:
#             search = search.query(
#                 Q('multi_match', query=query, fields=['first_name', 'last_name', 'email'])
#             ).suggest(
#                 'first_name_suggest', query, completion={'field': 'first_name.suggest'}
#             ).suggest(
#                 'last_name_suggest', query, completion={'field': 'last_name.suggest'}
#             ).suggest(
#                 'email_suggest', query, completion={'field': 'email.suggest'}
#             )

#         # Execute the search and return the results
#         response = search.execute()
#         results = [hit.to_dict() for hit in response.hits]

#         serializer = ExpertCardElasticSearchSerializer(data=results, context={'request': request}, many=True)
#         serializer.is_valid(raise_exception=True)
#         serialized_data = serializer.data

#         return Response(serialized_data)




