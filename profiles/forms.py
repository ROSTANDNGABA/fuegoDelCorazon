from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['photo', 'age', 'gender', 'field_of_study', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['age'].required = True
        self.fields['field_of_study'].required = True
