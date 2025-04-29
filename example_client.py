import requests
import base64
import os
from datetime import datetime

def generate_image(prompt: str, save_dir: str = "generated_images"):
    """
    Generate image using the FastAPI endpoint and save it locally
    
    Args:
        prompt (str): The image generation prompt
        save_dir (str): Directory to save generated images
    """
    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # API endpoint
    url = "http://localhost:8000/generate-image"
    
    # Request payload
    payload = {
        "prompt": prompt
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Make the API request
        print("Generating the image, please wait ...")
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Get the response data
        data = response.json()
        
        # Save each generated image
        for i, base64_str in enumerate(data.get("images", [])):
            try:
                # Decode base64 string to bytes
                image_bytes = base64.b64decode(base64_str)
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{save_dir}/generated_image_{timestamp}_{i}.webp"
                
                # Save the image
                with open(filename, "wb") as f:
                    f.write(image_bytes)
                print(f"Image saved: {filename}")
            except Exception as img_error:
                print(f"Error processing image {i}: {str(img_error)}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"API Error detail: {e.response.json()}")
            except ValueError:
                print(f"API Error response: {e.response.text}")

if __name__ == "__main__":
    # Your prompt
    prompt = """a beautiful blonde woman with long flowing hair, looking directly at the camera with a charming and captivating smile. She is holding a sign that clearly says "Jesse Qin" in bold letters. The background is softly blurred, cinematic lighting, photorealistic, high detail, 4K, warm tones, shallow depth of field."""
    
    # Generate the image
    generate_image(prompt) 