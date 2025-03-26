"""
URL mappings for the venue app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from venue import views

router = DefaultRouter()
router.register('venues', views.VenueViewSet)

app_name = 'venue'

urlpatterns = [
    path('', include(router.urls)),
]
