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


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm

    def get_success_url(self):
        # Redirection simple vers home après connexion
        return '/'
    
    def form_valid(self, form):
        try:
            print("Début de form_valid dans CustomLoginView")
            response = super().form_valid(form)
            print("Connexion réussie, redirection vers:", self.get_success_url())
            return response
        except Exception as e:
            print(f"Erreur dans CustomLoginView.form_valid: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def form_invalid(self, form):
        try:
            print("Formulaire invalide dans CustomLoginView")
            print(f"Erreurs du formulaire: {form.errors}")
            return super().form_invalid(form)
        except Exception as e:
            print(f"Erreur dans CustomLoginView.form_invalid: {e}")
            import traceback
            traceback.print_exc()
            raise

class CustomLogoutView(LogoutView):
    next_page = '/accounts/login/'

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
        messages.info(request, "Vous avez déjà un profil ! Vous pouvez le modifier ci-dessous.")
        # Rediriger vers une vue de modification ou afficher le formulaire pré-rempli
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=existing_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour avec succès !")
                return redirect('profiles:view_profile')
        else:
            form = StudentProfileForm(instance=existing_profile)
        
        return render(request, 'accounts/create_profile.html', {
            'form': form, 
            'editing': True,
            'existing_profile': existing_profile
        })
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
        
        return render(request, 'accounts/create_profile.html', {
            'form': form, 
            'editing': False
        })
