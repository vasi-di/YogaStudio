from django.urls import path, include
from YogaApp.common import views
from YogaApp.common.views import ReviewListView, BookingCreateView, ReviewCreateView, ReviewUpdateView, \
    ReviewDeleteView, GoalListView, GoalCreateView, GoalUpdateView, GoalDeleteView, MarkGoalCompleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('book/', include([
        path('', BookingCreateView.as_view(), name='book_class'),
        path('<int:yoga_class_id>/', BookingCreateView.as_view(), name='book_class'),

        # path('<int:pk>/', BookingCreateView.as_view(), name='create_booking'),
    ])),

    path('reviews/', include([
        path('', ReviewListView.as_view(), name='review_list'),
        path('add/', ReviewCreateView.as_view(), name='add_review'),
        path('edit/<int:pk>/', ReviewUpdateView.as_view(), name='edit_review'),
        path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='delete_review'),
    ])),

    path('goals/', include([
        path('', GoalListView.as_view(), name='goal_list'),
        path('add/', GoalCreateView.as_view(), name='goal_add'),
        path('edit/<int:pk>/', GoalUpdateView.as_view(), name='goal_edit'),
        path('delete/<int:pk>/', GoalDeleteView.as_view(), name='goal_delete'),
        path('<int:pk>/complete/', MarkGoalCompleteView.as_view(), name='goal_mark_complete'),
    ]))
]
