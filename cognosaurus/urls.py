from django.urls import include, path
from rest_framework import routers
from cognosaurus.api.views import CognateViewSet


router = routers.DefaultRouter()
router.register(r"words", CognateViewSet, basename="word")

urlpatterns = [
    path("", include(router.urls)),
]
