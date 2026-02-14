from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from profiles.forms import StudentProfileForm
from .forms import CustomUserCreationForm


class CustomLogoutView(LogoutView):
    next_page = '/'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('profiles:create_profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

@login_required
def create_profile(request):
    # Vérifier si l'utilisateur a déjà un profil
    try:
        existing_profile = StudentProfile.objects.get(user=request.user)
        messages.info(request, "Vous avez déjà un profil !")
        return redirect('home')
    except StudentProfile.DoesNotExist:
        # Créer un nouveau profil
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Profil créé avec succès !")
                return redirect('home')
        else:
            form = StudentProfileForm()
        
        return render(request, 'accounts/create_profile_simple.html', {
            'form': form
        })
