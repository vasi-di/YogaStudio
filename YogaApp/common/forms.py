from .models import Booking, Review, Goal, YogaClass
from django import forms


class YogaClassBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['yoga_class', 'booking_date']

    def __init__(self, *args, **kwargs):
        yoga_class_id = kwargs.pop('yoga_class_id', None)
        super().__init__(*args, **kwargs)

        if yoga_class_id:
            self.fields['yoga_class'].initial = YogaClass.objects.get(id=yoga_class_id)
        else:
            self.fields['yoga_class'].queryset = YogaClass.objects.all()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['yoga_class', 'rating', 'comments']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'yoga_class': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['yoga_class'].queryset = YogaClass.objects.all()
        self.fields['yoga_class'].label_from_instance = (
            lambda obj: f"{obj.name} - {obj.level}"
        )


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['description', 'target_date', 'is_completed']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



