"""
URL mappings for the group app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from group import views

router = DefaultRouter()
router.register('groups', views.GroupViewSet)

app_name = 'group'

urlpatterns = [
    path('', include(router.urls)),
]
