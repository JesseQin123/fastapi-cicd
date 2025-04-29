from fastapi import FastAPI, HTTPException
import uvicorn
import replicate
import os
from pydantic import BaseModel
import base64
from typing import List
from dotenv import load_dotenv
from pathlib import Path
import requests

# Get the project root directory
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'

# Load environment variables from .env file
print("Loading .env from:", env_path)
load_dotenv(env_path)

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
        api_token = os.getenv("REPLICATE_API_TOKEN")
        print("Debug - api_token=", api_token)
        if not api_token:
            raise HTTPException(status_code=500, detail="REPLICATE_API_TOKEN not set")

        # Initialize Replicate client
        client = replicate.Client(api_token=api_token)

        # Run the model
        output = client.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": request.prompt}
        )

        print("Debug - Replicate output type:", type(output))
        print("Debug - Replicate output:", output)

        # Convert images to base64
        base64_images = []
        for url in output:
            # Download image from URL
            response = requests.get(url)
            response.raise_for_status()
            # Convert to base64
            base64_str = base64.b64encode(response.content).decode('utf-8')
            base64_images.append(base64_str)

        return ImageResponse(images=base64_images)

    except Exception as e:
        print("Debug - Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

