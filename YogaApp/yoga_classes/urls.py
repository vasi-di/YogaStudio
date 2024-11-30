from django.urls import path, include
from .views import YogaClassListView, YogaClassDetailView, InstructorListView

urlpatterns = [
    path('classes/', include([
        path('', YogaClassListView.as_view(), name='class_list'),
        path('<int:pk>/', YogaClassDetailView.as_view(), name='class_detail'),
    ])),
    path('instructors/', InstructorListView.as_view(), name='instructor_list'),
]
