# challenges/forms.py
from django import forms
from .models import MonthlyChallenge

class MonthlyChallengeForm(forms.ModelForm):
    class Meta:
        model = MonthlyChallenge
        fields = ['month', 'challenge_text']

    def clean_month(self):
        month = self.cleaned_data.get('month')
        if not month.isalpha():
            raise forms.ValidationError('Month name should contain only letters.')
        return month.capitalize()