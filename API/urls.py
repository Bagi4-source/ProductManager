from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = routers.DefaultRouter()
router.register('products', views.ProductsView)

urlpatterns = [
    path('', include(router.urls)),
    path('get_products/', views.GetProductsView.as_view(), name='get_products'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token)
]
urlpatterns.extend(staticfiles_urlpatterns())
