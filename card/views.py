# Standard library imports
# from elasticsearch_dsl import Q
from django.db.models import Q

# # Third-party imports
# from django_elasticsearch_dsl_drf.filter_backends import (
#     FilteringFilterBackend,
#     OrderingFilterBackend,
#     CompoundSearchFilterBackend
# )
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import generics, status
from rest_framework.response import Response

# Local application or project-specific imports
from .activitylogmixin import ActivityLogMixin
from .document import ExpertCardDocument
from .models import (
    CompanyAddress,
    ExpertCard,
    ActivityLog
)
from .pagination import StandardResultPagination
from .permissions import AdminOrTrustedUserOnly
from .serializer import (
    CompanyAddressSerializer,
    ExpertCardSerializer,
    ActivityLogSerializer,
)

# Create your views here.


class CompanyAddressListApiView(AdminOrTrustedUserOnly,generics.ListAPIView):
    """
    An endpoint to access Company Address List
    Authentication is required

    """
    pagination_class= StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    queryset = CompanyAddress.active_objects.all()
    serializer_class = CompanyAddressSerializer


class CompanyAddressCreateApiView(AdminOrTrustedUserOnly, generics.CreateAPIView):
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
    

class CompanyAddressDetailUpdateDeleteApiView(AdminOrTrustedUserOnly, generics.RetrieveUpdateDestroyAPIView):
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
        self.perform_update(serializer)
        response = {
            "message": "Address updated successfully",
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=['is_deleted', 'is_active'])
        response = {
            "message": 'Address deleted successfully'
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    

class ActiveExpertCardListApiView(AdminOrTrustedUserOnly, generics.ListAPIView):
    """
    An endpoint to Access ExpertCard List
    Authentication is required

    """
    queryset=ExpertCard.active_objects.filter(is_deleted = False).order_by('-created_date')
    pagination_class = StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = ExpertCardSerializer


class InctiveExpertCardListApiView(AdminOrTrustedUserOnly, generics.ListAPIView):
    """
    An endpoint to Access ExpertCard List
    Authentication is required

    """
    queryset=ExpertCard.objects.filter(is_active=False, is_deleted = False).order_by('-created_date')
    pagination_class = StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = ExpertCardSerializer


class ExpertCardListApiView(AdminOrTrustedUserOnly, generics.ListAPIView):
    """
    An endpoint to access the ExpertCard List.
    Authentication is required.
    with search functionalities usinf first name, last_name or email
    USE "search_query"
    """
    queryset = ExpertCard.objects.filter(is_deleted=False).order_by('-created_date')
    pagination_class = StandardResultPagination
    permission_classes = [AdminOrTrustedUserOnly]
    serializer_class = ExpertCardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search_query')

        if search_query:
            # Apply search filter using Q objects
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        return queryset


class ExpertCardCreateApiView(AdminOrTrustedUserOnly, ActivityLogMixin, generics.CreateAPIView):
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
    serializer_class = ExpertCardSerializer

    def update(self, request, *args, **kwargs):
        expert_card_ids = request.data.get('expert_card_ids', [])
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
    queryset = ActivityLog.objects.filter(status='Success', action_type__in=['Create', 'Update'])
    serializer_class = ActivityLogSerializer
    





















# from django.http import JsonResponse
# from elasticsearch_dsl.query import Q

# from django.http import JsonResponse
# from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet



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




