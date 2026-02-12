from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import StudentProfile
from .forms import StudentProfileForm

@login_required
def view_profile(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
        return render(request, 'profiles/view_profile.html', {'profile': profile})
    except StudentProfile.DoesNotExist:
        return redirect('accounts:create_profile')

@login_required
def edit_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:view_profile')
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'profiles/edit_profile.html', {'form': form})

def view_other_profile(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(StudentProfile, user=other_user)
    
    # Calculer la compatibilité avec l'utilisateur connecté
    from matching.views import calculate_compatibility
    compatibility_score = calculate_compatibility(request.user, other_user)
    
    context = {
        'other_user': other_user,
        'profile': profile,
        'compatibility_score': round(compatibility_score, 2)
    }
    return render(request, 'profiles/view_other_profile.html', context)
