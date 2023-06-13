from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Note, Group
from .forms import NoteForm, GroupForm, DateRangeForm

# Method to get the main page
@login_required
def note_list(request):
    notes = Note.objects.filter(created_by=request.user)
    groups = Group.objects.filter(created_by=request.user)
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            print(f"Filtering notes from {start_date} to {end_date}")
            if start_date and end_date:
                notes = notes.filter(created_at__date__range=(start_date, end_date))
    else:
        form = DateRangeForm()
    return render(request, 'note_list.html', {'notes': notes, 'groups': groups, 'form': form})


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
            return redirect('note:note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'note_edit.html', {'form': form})

# Method to delete a new note
@login_required
def note_delete(request, pk):
    note = Note.objects.get(pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note:note_list')
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
            return redirect('note:note_list')
    else:
        form = GroupForm()
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
            return redirect('note:note_list')
    else:
        form = NoteForm()
    return render(request, 'note_add.html', {'form': form})

# Method to delete a group
@login_required
def group_delete(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('note:note_list')
    return redirect('note:note_list')
