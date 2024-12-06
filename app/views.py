from django.shortcuts import render, redirect
from app.models import Folder, File
import uuid
from urllib.parse import urlencode
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


def shared_file(request):
    if request.method == 'POST':
        share_option = request.POST.get("shareOption")
        file_id = request.POST.get("file_id")
        emails = request.POST.get("emails", "").strip()
        redirect_url = request.META.get('HTTP_REFERER', '/')
        redirect_url = "/".join(redirect_url.split("/")[:-1])

     
        if not emails:
            is_public = make_public_file(file_id=file_id)
            params = {
                "link" : f" http://127.0.0.1:8000/file/access/{file_id}"
            }

            if not is_public:
                params['error'] ='Could not make file public',
                     
            query_string = urlencode(params)
            return redirect(f"{redirect_url}?{query_string}")
            
        
    return redirect('/')


def make_public_file(file_id):
    file = get_file_by_id(file_id=file_id).first()
    if not filter:
        return False
    file.visibility = 'public'
    file.save()
    return True

def file_access(request,id):
    files = get_file_by_id(file_id=id)
    if not files:
        return render(request, 'index.html', { 'error': "not such file."})
    return render(request, 'index.html', { 'files': files,"is_file_shared":True})

def get_file_by_id(file_id):
    return File.objects.filter(id=file_id)