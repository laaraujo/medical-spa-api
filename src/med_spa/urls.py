from django.urls import include, path
from rest_framework.routers import DefaultRouter

from med_spa import views

router = DefaultRouter()
router.register(r"services", views.ServiceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]