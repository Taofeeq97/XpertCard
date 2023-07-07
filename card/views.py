from django.shortcuts import render
from .models import CompanyAddress, ExpertCard, ActivityLog
from .serializer import CompanyAddressSerializer, ExpertCardSerializer, ActivityLogSerializer
from rest_framework import generics, status
from .pagination import StandardResultPagination
from rest_framework.response import Response
from .activitylogmixin import ActivityLogMixin, ActivityLogCreateMixin
from .permissions import AdminOrTrustedUserOnly
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from .document import ExpertCardDocument
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
# Create your views here.


class CompanyAddressListApiView(AdminOrTrustedUserOnly,  generics.ListAPIView):
    """
    An endpoint to access Company Address List
    Authentication is required

    """
    pagination_class= StandardResultPagination
    queryset = CompanyAddress.active_objects.all()
    serializer_class = CompanyAddressSerializer


class CompanyAddressCreateApiView(AdminOrTrustedUserOnly, generics.CreateAPIView):
    """
    An endpoint to create A company Address
    Authentication is required

    """
    queryset = CompanyAddress.objects.all()
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
    

class ActiveExpertCardListApiView(AdminOrTrustedUserOnly,  generics.ListAPIView):
    """
    An endpoint to Access ExpertCard List
    Authentication is required

    """
    queryset=ExpertCard.active_objects.filter(is_active=True, is_deleted = False).order_by('-created_date')
    pagination_class = StandardResultPagination
    serializer_class = ExpertCardSerializer


class InctiveExpertCardListApiView(AdminOrTrustedUserOnly,  generics.ListAPIView):
    """
    An endpoint to Access ExpertCard List
    Authentication is required

    """
    queryset=ExpertCard.active_objects.filter(is_active=False, is_deleted = False).order_by('-created_date')
    pagination_class = StandardResultPagination
    serializer_class = ExpertCardSerializer


class ExpertCardListApiView(AdminOrTrustedUserOnly,  generics.ListAPIView):
    """
    An endpoint to Access ExpertCard List
    Authentication is required

    """
    queryset=ExpertCard.active_objects.filter(is_deleted = False).order_by('-created_date')
    pagination_class = StandardResultPagination
    serializer_class = ExpertCardSerializer


# class ExpertCardListApiView(AdminOrTrustedUserOnly, DocumentViewSet):
#     """
#     An endpoint to access the ExpertCard List.
#     Authentication is required.
#     """
#     document = ExpertCardDocument
#     serializer_class = ExpertCardSerializer
#     pagination_class = StandardResultPagination

#     filter_backends = [
#         FilteringFilterBackend,
#         OrderingFilterBackend,
#         SearchFilterBackend,
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
#         'email',
#     )

#     def get_queryset(self):
#         # Get the search query from the request
#         query = self.request.GET.get('query')

#         # Build the Elasticsearch DSL search query
#         search = self.document.search()

#         # Apply filters based on query parameters
#         if query:
#             search = search.query(Q('multi_match', query=query, fields=['first_name', 'last_name', 'email']))

#         # Execute the search and return the queryset
#         response = search.execute()
#         queryset = [hit.to_dict() for hit in response.hits]

#         return queryset
    


class ExpertCardCreateApiView(AdminOrTrustedUserOnly, ActivityLogCreateMixin, generics.CreateAPIView):
    """
    An endpoint to create Expertcard
    Authentication is required

    """
    queryset = ExpertCard.objects.all()
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


class ExpertCardRetrieveUpdateDeleteApiView(AdminOrTrustedUserOnly, ActivityLogMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint to Access, Update or Delete A Expertcard instance
    Authentication is required

    """
    queryset = ExpertCard.objects.filter(is_deleted = False)
    serializer_class = ExpertCardSerializer
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
        response = {
            "message":'Expertcard Updated Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields = ['is_deleted', 'is_active'])
        response = {
            "message": "Expertcard deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class BulkActivateExpertCardApiView(AdminOrTrustedUserOnly, generics.UpdateAPIView):
    """
    An endpoint to Bulk Update cards
    Authentication is required

    """
    queryset = ExpertCard.objects.all()
    serializer_class = ExpertCardSerializer

    def update(self, request, *args, **kwargs):
        # Get the list of expert card IDs from the request data
        expert_card_ids = request.data.get('expert_card_ids', [])
        expert_cards = ExpertCard.objects.filter(id__in=expert_card_ids)
        expert_cards.update(is_active=True)
        response = {
            "message": "Cards Activated Successfully"
        }
        return Response(response, status=status.HTTP_200_OK)
    



class ActivityLogAPIView(AdminOrTrustedUserOnly, generics.ListAPIView):
    """
    An endpoint to Access Activity log list
    Authentication is required

    """
    pagination_class = StandardResultPagination
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    




        