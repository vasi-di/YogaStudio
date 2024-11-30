from django.views.generic import ListView, DetailView
from .models import YogaClass, Instructor


class YogaClassListView(ListView):
    model = YogaClass
    template_name = 'yoga_classes/class_list.html'
    context_object_name = 'classes'


class YogaClassDetailView(DetailView):
    model = YogaClass
    template_name = 'yoga_classes/class_detail.html'
    context_object_name = 'yoga_class'


class InstructorListView(ListView):
    model = Instructor
    template_name = 'yoga_classes/instructor_list.html'
    context_object_name = 'instructors'
