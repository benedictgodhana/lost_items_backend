from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LostItemViewSet
from .views import csrf_token


router = DefaultRouter()
router.register(r'lostitems', LostItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('csrf/', csrf_token, name='csrf_token'),

]

