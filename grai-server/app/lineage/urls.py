from django.urls import path
from rest_framework import routers
from .views import NodeViewSet, EdgeViewSet

app_name = 'graph'

router = routers.SimpleRouter()
router.register("nodes", NodeViewSet, basename='nodes')
router.register("edges", EdgeViewSet, basename='edges')

urlpatterns = router.urls
