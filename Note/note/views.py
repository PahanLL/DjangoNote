from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Note, Group, UserProfile
from django.contrib.auth import update_session_auth_hash, get_user_model
from .forms import NoteForm, GroupForm, DateRangeForm, EmploymentStatusForm, ProfilePhotoForm, UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist


import logging

# Logging
logger = logging.getLogger(__name__)

# Method to create a new note
@login_required
def note_list(request):
    groups = Group.objects.filter(created_by=request.user)  # фильтруем группы по текущему пользователю
    date_form = DateRangeForm(request.POST or None)
    groups_notes = {}
    if date_form.is_valid():
        start_date = date_form.cleaned_data.get("start_date")
        end_date = date_form.cleaned_data.get("end_date")
        for group in groups:
            notes = group.notes.filter(created_at__range=[start_date, end_date])
            if notes:
                groups_notes[group] = notes
    else:
        for group in groups:
            groups_notes[group] = group.notes.all()

    return render(request, "note_list.html", {"date_form": date_form, "groups_notes": groups_notes})

# Method to edit a note
@login_required
def note_edit(request, pk):
    note = Note.objects.get(id=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            logger.info('Note edited successfully.')
            return redirect('note:note_list')
    else:
        form = NoteForm(instance=note)
    logger.info('Rendering note edit.')
    return render(request, 'note_edit.html', {'form': form})

# Method to delete a new note
@login_required
def note_delete(request, pk):
    note = Note.objects.get(pk=pk)
    if request.method == 'POST':
        note.delete()
        logger.info('Note deleted successfully.')
        return redirect('note:note_list')
    logger.info('Rendering note delete.')
    return redirect('note:note_list')

# Method to create a new group
@login_required
def group_new(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            logger.info('Group created successfully.')
            return redirect('note:note_list')
    else:
        form = GroupForm()
    logger.info('Rendering group new.')
    return render(request, 'group_new.html', {'form': form})

# Method to add a note to a group
@login_required
def group_note_add(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.group = group
            note.created_by = request.user
            note.save()
            logger.info('Note added to group successfully.')
            return redirect('note:note_list')
    else:
        form = NoteForm()
    logger.info('Rendering group note add.')
    return render(request, 'note_add.html', {'form': form})

# Method to delete a group
@login_required
def group_delete(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        group.delete()
        logger.info('Group deleted successfully.')
        return redirect('note:note_list')
    logger.info('Rendering group delete.')
    return redirect('note:note_list')

# Method to view a profile
@login_required
def profile_view(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    if not profile:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            logger.info('Profile updated successfully.')
            return redirect('note:profile_view')
    else:
        form = UserProfileForm(instance=profile)

    password_form = PasswordChangeForm(request.user)

    logger.info('Rendering profile view.')
    return render(request, 'profile.html', {
        'form': form,
        'password_form': password_form,
        'profile': profile
    })

# Method to upload a profile photo
@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.userprofile
            profile.profile_photo = form.cleaned_data['profile_photo']
            profile.save()
            logger.info('Photo uploaded successfully.')
            return redirect('note:profile_view')
    else:
        form = ProfilePhotoForm()
    return render(request, 'profile.html', {'form': form})

# Method to delete a profile photo
@login_required
def photo_delete(request, pk):
    try:
        photo = UserProfile.objects.get(user=request.user).profilephoto_set.get(pk=pk)
        photo.delete()
        logger.info('Photo deleted successfully.')
        return redirect('note:profile_view')
    except ObjectDoesNotExist:
        return redirect('note:profile_view')

# Method to update employment status
@login_required
def employment_status_update(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = EmploymentStatusForm(request.POST, instance=profile)
            if form.is_valid():
                profile.employment_status = form.cleaned_data['employment_status']
                profile.save()
                logger.info('Employment status updated successfully.')
                return redirect('note:profile_view')
        else:
            form = EmploymentStatusForm(instance=profile)
        return render(request, 'profile.html', {'form': form})
    except ObjectDoesNotExist:
        return render(request, '404.html')

# Method to change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            logger.info('Your password was successfully updated!')
            return redirect('profile_view')
        else:
            logger.error('Password change failed.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile.html', {'form': form})

# Method to delete a user
@login_required
def profile_delete(request, pk):
    User = get_user_model()
    user = User.objects.get(pk=pk)
    if request.user == user:
        if request.method == 'POST':
            user.delete()  
            logger.info('User deleted successfully.')
            return redirect('logout')
        else:
            return render(request, 'login.html')
    else:
        return redirect('login')

# Method to search notes
@login_required
def search_notes(request):
    query = request.GET.get('q')
    groups = Group.objects.all()
    date_form = DateRangeForm(request.POST or None)
    groups_notes = {}

    if query:
        q = Q(title__icontains=query) | Q(content__icontains=query)
        groups_notes = {group: group.notes.filter(q) for group in groups}
    else:
        for group in groups:
            groups_notes[group] = group.notes.all()

    return render(request, "note_list.html", {"date_form": date_form, "groups_notes": groups_notes})

