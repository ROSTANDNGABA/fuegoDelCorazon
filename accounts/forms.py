from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresse email',
            'id': 'email'
        })
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'id': 'password1'
        })
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe',
            'id': 'password2'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur',
                'id': 'username'
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Cette adresse email est déjà utilisée.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Les deux mots de passe ne correspondent pas.')
        
        return password2

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Critères de validation personnalisés
        errors = []
        
        # Longueur minimale
        if len(password) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caractères")
        
        # Vérifier s'il contient une majuscule
        if not any(c.isupper() for c in password):
            errors.append("Le mot de passe doit contenir au moins une majuscule")
        
        # Vérifier s'il contient une minuscule
        if not any(c.islower() for c in password):
            errors.append("Le mot de passe doit contenir au moins une minuscule")
        
        # Vérifier s'il contient un chiffre
        if not any(c.isdigit() for c in password):
            errors.append("Le mot de passe doit contenir au moins un chiffre")
        
        # Vérifier s'il contient un caractère spécial
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            errors.append("Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&* etc.)")
        
        # Vérifier que ce n'est pas entièrement numérique
        if password.isdigit():
            errors.append("Le mot de passe ne peut pas être entièrement numérique.")
        
        if errors:
            raise ValidationError(errors)
        
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # S'assurer que l'email est bien sauvegardé
        if 'email' in self.cleaned_data:
            user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
