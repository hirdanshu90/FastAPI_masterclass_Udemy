import shutil
from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix='/file',
    tags=['file']
)

# Using this, one can load a very small file as it is stored in memory.
@router.post('/file')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {
        'lines': lines
    }
    
# This is for larger files.
@router.post('/uploadFile')
def get_uploadfile(uploadfile: UploadFile = File(...)):
    path = f"files/{uploadfile.filename}"
    with open(path, w+b) as buffer:
        shutil.copyfileobj(uploadfile.file,buffer)
    return {
        'filename': path,
        'type': uploadfile.content_type 
    }
     