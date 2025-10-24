from django import forms
from .models import PrintRequest


class PrintRequestForm(forms.ModelForm):
    class Meta:
        model = PrintRequest
        fields = ['file', 'deadline', 'copies', 'notes']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'copies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 50,
                'value': 1
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any special instructions (optional)...'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt'
            })
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (50MB limit)
            if file.size > 52428800:
                raise forms.ValidationError('File size must be less than 50MB')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
            ext = file.name.lower().split('.')[-1]
            if f'.{ext}' not in allowed_extensions:
                raise forms.ValidationError('Only PDF, DOC, DOCX, and TXT files are allowed')
        
        return file
