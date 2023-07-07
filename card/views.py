from django.shortcuts import render
from .models import CompanyAddress, ExpertCard, ActivityLog
from .serializer import CompanyAddressSerializer, ExpertCardSerializer, ActivityLogSerializer
from rest_framework import generics, status
from .pagination import StandardResultPagination
from rest_framework.response import Response
from .activitylogmixin import ActivityLogMixin, ActivityLogCreateMixin
from .permissions import AdminOrTrustedUserOnly
# Create your views here.


class CompanyAddressListApiView(AdminOrTrustedUserOnly,  generics.ListAPIView):
    pagination_class= StandardResultPagination
    queryset = CompanyAddress.active_objects.all()
    serializer_class = CompanyAddressSerializer


class CompanyAddressCreateApiView(AdminOrTrustedUserOnly, generics.CreateAPIView):
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
    

class ExpertCardListApiView(AdminOrTrustedUserOnly,  generics.ListAPIView):
    queryset=ExpertCard.active_objects.filter(is_deleted = False).order_by('-created_date')
    pagination_class = StandardResultPagination
    serializer_class = ExpertCardSerializer

class ExpertCardCreateApiView(AdminOrTrustedUserOnly, ActivityLogCreateMixin, generics.CreateAPIView):
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
    queryset = ExpertCard.objects.filter(is_deleted = False)
    serializer_class = ExpertCardSerializer
    lookup_field = 'email'
    lookup_url_kwarg = 'expert_email'

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
    

class ActivityLogAPIView(AdminOrTrustedUserOnly, generics.ListAPIView):
    pagination_class = StandardResultPagination
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    




        