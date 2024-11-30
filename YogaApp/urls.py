from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('YogaApp.common.urls')),
    path('accounts/', include('YogaApp.accounts.urls')),
    path('yoga_classes/', include('YogaApp.yoga_classes.urls')),
]
