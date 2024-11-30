from django.contrib.auth.views import LogoutView
from django.urls import path, include
from YogaApp.accounts import views
from YogaApp.accounts.views import ProfileDetailView, ProfileDeleteView, ProfileEditView, \
    CustomPasswordChangeView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('profile/<int:pk>/', include([
        path('view/', ProfileDetailView.as_view(), name='profile_detail'),
        path('edit/', ProfileEditView.as_view(), name='profile_edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]))
]