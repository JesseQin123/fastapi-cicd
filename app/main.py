from fastapi import FastAPI, HTTPException
import uvicorn
import replicate
import os
from pydantic import BaseModel
import base64
from typing import List

app = FastAPI()

class ImageRequest(BaseModel):
    prompt: str

class ImageResponse(BaseModel):
    images: List[str]  # Base64 encoded images

@app.get("/")
async def read_root():
    return {"message": "Hello, World, Jesse! You see the 'CICD FastAPI'"}

@app.post("/generate-image")
async def generate_image(request: ImageRequest):
    try:
        # Check if API token is set
        if not os.getenv("REPLICATE_API_TOKEN"):
            raise HTTPException(status_code=500, detail="REPLICATE_API_TOKEN not set")

        # Initialize Replicate client
        client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

        # Run the model
        output = client.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": request.prompt}
        )

        # Convert images to base64
        base64_images = []
        for image in output:
            # Since the output is already bytes, we can encode it directly
            base64_str = base64.b64encode(image).decode('utf-8')
            base64_images.append(f"data:image/webp;base64,{base64_str}")

        return ImageResponse(images=base64_images)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

