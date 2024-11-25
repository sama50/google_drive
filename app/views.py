from django.shortcuts import render, redirect
from app.models import Folder, File
import uuid
# Create your views here.

def home(request):
    user_id = 1
    folders = Folder.objects.filter(parent=None,owner_id=user_id)
    return render(request,'index.html',{"folders":folders})


def get_folders(request, folder_id):
    user_id = 1
    print(request.path)
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name', None)
        create_folder(
            folder_name=folder_name, 
            parent_folder_id=folder_id,  # Use the current folder ID as parent
            owner_id=user_id
        )
    parent_folders = Folder.objects.filter(id=folder_id)
    folders = Folder.objects.filter(parent_id=folder_id)
    files = File.objects.filter(folder_id=folder_id)
    return render(request, 'index.html', {"folders": folders, 'files': files,"folder_id":folder_id,'path':parent_folders.first()})

def create_folder(folder_name, parent_folder_id, owner_id):
    print("==========================")
    print(folder_name)
    if not folder_name:
        return
    
    # If parent_folder_id is None or an invalid UUID, set it to None
    try:
        parent = Folder.objects.get(id=parent_folder_id) if parent_folder_id else None
    except (Folder.DoesNotExist, ValueError):
        parent = None
    
    Folder.objects.create(
        name=folder_name, 
        owner_id=owner_id, 
        parent=parent
    )


def upload_file(request):
    if request.method == 'POST':
        # Retrieve the uploaded file
        file_name = request.POST.get('file_name',None)   # The file input name in the form
        folder_id = request.POST.get('folder_id')  # Additional hidden input
        file = request.FILES.get('file')
        user_id = 1
        print(file_name)
        print(folder_id)
        if file_name:
            file = File(folder_id=folder_id,owner_id=user_id,file=file,name=file_name)
            file.save()
            return redirect('/')   

    return redirect('/')