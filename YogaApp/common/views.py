from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from YogaApp.common.models import Booking, Review, Goal
from .forms import YogaClassBookingForm, ReviewForm, GoalForm
from YogaApp.yoga_classes.models import YogaClass


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = YogaClassBookingForm
    template_name = 'yoga_classes/booking_form.html'

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        yoga_class = form.cleaned_data['yoga_class']
        booking.booking_date = yoga_class.schedule

        if Booking.objects.filter(yoga_class=yoga_class).count() >= 20:
            form.add_error('yoga_class', 'Sorry, this class is fully booked. Please select another class.')
            return self.form_invalid(form)

        if Booking.objects.filter(user=self.request.user, yoga_class=yoga_class).exists():
            form.add_error('yoga_class', 'You have already booked this class!')
            return self.form_invalid(form)

        booking.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        yoga_class_id = self.request.GET.get('yoga_class') or self.kwargs.get('yoga_class_id')
        kwargs['yoga_class_id'] = yoga_class_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        yoga_class_id = self.request.GET.get('yoga_class') or self.kwargs.get('yoga_class_id')
        yoga_classes = YogaClass.objects.all()

        context['yoga_classes'] = yoga_classes
        if yoga_class_id:
            context['selected_yoga_class'] = get_object_or_404(YogaClass, pk=yoga_class_id)
            context['selected_schedule'] = context['selected_yoga_class'].schedule
        else:
            context['selected_yoga_class'] = None
            context['selected_schedule'] = None
        return context

    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.request.user.pk})


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('review_list')


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    ordering = ['-review_date']


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('review_list')


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('review_list')


class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'goals/goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/goal_form.html'
    success_url = reverse_lazy('goal_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/goal_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goal_list')


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goal_list')


class MarkGoalCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
        goal.is_completed = True
        goal.save()
        return redirect('goal_list')









