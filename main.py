from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from face_swapper import swap_face
from models import ProcessedImage
import os
import requests
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/swap_faces_file/")
async def swap_faces(source_image: UploadFile = File(...), target_image: UploadFile = File(...)):
    source_image_path = f'./images/{source_image.filename}'
    target_image_path = f'./images/{target_image.filename}'
    with open(source_image_path, 'wb') as source_image_file:
        source_image_file.write(await source_image.read())
    with open(target_image_path, 'wb') as target_image_file:
        target_image_file.write(await target_image.read())


    output_image = f'processed_{source_image.filename}+{target_image.filename}'
    output_image_path = f'./images/processed_{source_image.filename}+{target_image.filename}'

    swap_face(source_image.filename, target_image.filename, output_image)
    
    with open(output_image_path, "rb") as img_file:
        result_image = img_file.read()



    processed_image = await ProcessedImage.create(
        source_image=source_image_path,
        target_image=target_image_path,
        processed_image=output_image_path
    )
    
    # os.remove(source_image_path)
    # os.remove(target_image_path)
    # os.remove(output_image_path)
    
    return Response(content=result_image, media_type="image/jpeg")    



@app.post("/swap_faces_url/")
async def swap_faces_url(source_image: str, target_image: str):

    response = requests.get(source_image)
    source_image_path = f'./images/{response.url.split("/")[-1]}.jpg'
    with open(source_image_path, 'wb') as source_image_file:
        source_image_file.write(response.content)

    response = requests.get(target_image)
    target_image_path = f'./images/{response.url.split("/")[-1]}.jpg'
    with open(target_image_path, 'wb') as target_image_file:
        target_image_file.write(response.content)

    output_image = f'processed_{source_image_path.split("/")[-1]}+{target_image_path.split("/")[-1]}'
    output_image_path = f'./images/processed_{source_image_path.split("/")[-1]}+{target_image_path.split("/")[-1]}'

    swap_face(source_image_path.split("/")[-1], target_image_path.split("/")[-1], output_image)

    with open(output_image_path, "rb") as img_file:
        result_image = img_file.read()

    processed_image = await ProcessedImage.create(
        source_image=source_image_path,
        target_image=target_image_path,
        processed_image=output_image_path
    )


    # os.remove(source_image_path)
    # os.remove(target_image_path)
    # os.remove(output_image_path)
    

    return Response(content=result_image, media_type="image/jpeg") 