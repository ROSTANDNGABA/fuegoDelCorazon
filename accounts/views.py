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

    def form_invalid(self, form):
        # Vérifier si l'utilisateur existe mais le mot de passe est incorrect
        username = form.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                # L'utilisateur existe mais le mot de passe est incorrect
                messages.error(self.request, "Mot de passe incorrect. Veuillez réessayer.")
            except User.DoesNotExist:
                # L'utilisateur n'existe pas
                messages.error(self.request, "Ce nom d'utilisateur n'existe pas. Veuillez créer un compte.")
        else:
            messages.error(self.request, "Veuillez entrer un nom d'utilisateur.")
        
        return super().form_invalid(form)

    def form_valid(self, form):
        # Laisser Django gérer la connexion normalement
        response = super().form_valid(form)
        
        # Après connexion réussie, vérifier le profil et rediriger si nécessaire
        user = form.get_user()
        print(f"Utilisateur connecté: {user.username}")
        
        try:
            profile = StudentProfile.objects.get(user=user)
            print(f"Profil trouvé: {profile}")
            
            # Vérifier si le profil est complet
            if profile.age and profile.gender and profile.field_of_study:
                print("Profil complet, redirection vers home")
                messages.success(self.request, f"Bienvenue {user.username} !")
                return redirect('home')
            else:
                print("Profil incomplet, redirection vers édition")
                messages.info(self.request, "Veuillez compléter votre profil pour continuer.")
                return redirect('profiles:edit_profile')
        except StudentProfile.DoesNotExist:
            print("Aucun profil, redirection vers création")
            messages.info(self.request, "Bienvenue ! Veuillez créer votre profil pour continuer.")
            return redirect('profiles:create_profile')
        
        return response

class CustomLogoutView(LogoutView):
    next_page = '/accounts/login/'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:create_profile')

    def form_valid(self, form):
        try:
            print("Début de form_valid dans SignUpView")
            response = super().form_valid(form)
            print("Utilisateur créé avec succès")
            login(self.request, self.object)
            print("Utilisateur connecté avec succès")
            return response
        except Exception as e:
            print(f"Erreur dans SignUpView.form_valid: {e}")
            import traceback
            traceback.print_exc()
            raise

    def form_invalid(self, form):
        print("Formulaire invalide dans SignUpView")
        print(f"Erreurs du formulaire: {form.errors}")
        return super().form_invalid(form)

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
