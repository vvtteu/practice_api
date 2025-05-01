from rest_framework.routers import DefaultRouter
from first_api.views import PerevalViewSet

router = DefaultRouter()
router.register(r'submitData', PerevalViewSet, basename='pereval')

urlpatterns = router.urls

