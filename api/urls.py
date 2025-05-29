from django.urls import path
from .views import BankWebhookView, OrganizationBalanceView, OrganizationListCreateView

urlpatterns = [
    path('webhook/bank', BankWebhookView.as_view(), name='bank-webhook'),
    path('organizations/<str:inn>/balance/', OrganizationBalanceView.as_view(), name='organization-balance'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organizations-list-create'),
]
