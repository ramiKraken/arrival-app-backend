from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

app = FastAPI()

# Allow your Vue app to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change "*" to your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a folder to save uploaded images locally for now
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/confirm")
async def upload_location_data(
    latitude: str = Form(...),
    longitude: str = Form(...),
    timestamp: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        # 1. Read the image file
        contents = await image.read()
        
        # 2. Create a unique filename using the timestamp
        safe_time = timestamp.replace(":", "-").replace(" ", "_")
        filename = f"{safe_time}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # 3. Save the file to disk
        with open(file_path, "wb") as f:
            f.write(contents)
            
        # 4. Print to terminal to verify it works
        print(f"✅ Received Data:")
        print(f"   Location: {latitude}, {longitude}")
        print(f"   Time: {timestamp}")
        print(f"   Image saved to: {file_path}")

        # 5. Return success to the Vue app
        return {
            "status": "success",
            "message": "Data and image received",
            "data": {
                "lat": latitude,
                "lng": longitude,
                "time": timestamp,
                "saved_image": filename
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))