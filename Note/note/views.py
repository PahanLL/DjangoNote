from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Note, Group
from .forms import NoteForm, GroupForm

@login_required
def note_list(request):
    notes = Note.objects.filter(created_by=request.user)
    groups = Group.objects.filter(created_by=request.user)
    return render(request, 'note_list.html', {'notes': notes, 'groups': groups})

@login_required
def note_edit(request, pk):
    note = Note.objects.get(id=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            return redirect('note:note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'note_edit.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = Note.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'note_confirm_delete.html', {'note': note})

@login_required
def group_new(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            return redirect('note:note_list')
    else:
        form = GroupForm()
    return render(request, 'group_new.html', {'form': form})

@login_required
def note_add(request, pk=None):
    if pk:
        group = Group.objects.get(id=pk)
    else:
        group = None
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.group = group
            note.created_by = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'note_add.html', {'form': form})

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
            return redirect('note:note_list')
    else:
        form = NoteForm()
    return render(request, 'note_add.html', {'form': form})

@login_required
def group_delete(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('note:note_list')
    return redirect('note:note_list')
