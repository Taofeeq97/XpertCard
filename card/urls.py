from django.urls import path
from . import views



urlpatterns = [
    path('company_address/', views.CompanyAddressListApiView.as_view(), name='company_address_list'),
    path('company_address/create/', views.CompanyAddressCreateApiView.as_view(), name='company_address_create'),
    path('company_address/<slug:company_address_slug>/', views.CompanyAddressDetailUpdateDeleteApiView.as_view(), name='company_address_detail_create_update_delete'),
    path('expert_cards/', views.ExpertCardListApiView.as_view(), name='expert_card_list'),
    # path('expert_cards/list/', views.ExpertCardTestListApiView.as_view({'get': 'list'}), name='expert_card_list'),
    path('expert_cards/active/', views.ActiveExpertCardListApiView.as_view(), name='expert_card_list'),
    # path('expert_cards/inactive/', views.InctiveExpertCardListApiView.as_view(), name='expert_card_list'),
    path('expert_cards/create/', views.ExpertCardCreateApiView.as_view(), name='expert_card_create'),
    path('expert_cards/bulk_activate/', views.BulkActivateExpertCardApiView.as_view(), name='expert_card_create'),
    path('expert_cards/<int:expert_id>/', views.ExpertCardRetrieveUpdateDeleteApiView.as_view(), name='expert_card_detail_create_update_delete'),
    path('activity_log/', views.ActivityLogAPIView.as_view(), name='activity_log'),
    path('expertcard_vcf/<int:pk>/', views.VCardAPIView.as_view(), name='vcard_view'),
    
]

