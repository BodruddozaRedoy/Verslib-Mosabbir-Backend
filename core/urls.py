from django.contrib import admin
from django.urls import path
from Files.views import *
from Files.admin import *
from Accounts.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path('api/files/', FileByCategoryAPIView.as_view(), name='svg-list'),
    path('api/files/<int:pk>/copy/', CopySVG.as_view(), name='svg-download'),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/files/<int:pk>/', SVGImageDetailView.as_view(), name='svg-detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
