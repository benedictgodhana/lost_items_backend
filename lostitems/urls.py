from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LostItemViewSet, total_lost_items, csrf_token, ClaimViewSet

from . import views

router = DefaultRouter()
router.register(r'lostitems', LostItemViewSet)
router.register(r'claims', ClaimViewSet)  # Register the ClaimViewSet with the router

urlpatterns = [
    path('', include(router.urls)),
    path('api/total_lost_items/', total_lost_items, name='total-lost-items'),
    path('csrf/', csrf_token, name='csrf_token'),
    path('total_lost_items/', views.total_lost_items, name='total-lost-items'),
    path('api/claim/', views.claim_lost_item, name='claim-lost-item'),
]
