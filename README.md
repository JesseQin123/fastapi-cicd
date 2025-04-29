# FastAPI Image Generation Service

A FastAPI-based image generation service that integrates with the Replicate API to create AI-generated images.

## Project Structure

```
.
├── app/
│   └── main.py          # FastAPI main application
├── .env                 # Environment variables (create locally)
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
├── example_client.py    # Example client implementation
└── README.md           # Project documentation
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Replicate
- Python-dotenv
- Requests

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/JesseQin123/fastapi-cicd.git
cd fastapi-cicd
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuring Replicate API Token

### Local Development Setup

1. Create a `.env` file in the project root:
```bash
touch .env
```

2. Add your Replicate API token to the `.env` file:
```
REPLICATE_API_TOKEN=your_replicate_api_token_here
```

Note: Make sure to add `.env` to your `.gitignore` file to prevent committing sensitive information to the repository.

### GitHub Actions Setup

To configure the Replicate API token as a GitHub secret:

1. Navigate to your GitHub repository
2. Go to "Settings" -> "Secrets and variables" -> "Actions"
3. Click "New repository secret"
4. Set name as: `REPLICATE_API_TOKEN`
5. Enter your Replicate API token as the value
6. Click "Add secret"

Example GitHub Actions workflow using the secret:

```yaml
name: Your Workflow Name

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      env:
        REPLICATE_API_TOKEN: ${{ secrets.REPLICATE_API_TOKEN }}
      run: |
        # Your test commands here
```

## Running the Service

1. Start the FastAPI server:
```bash
python app/main.py
```
The server will run at http://localhost:8000

2. Generate images using the example client:
```bash
python example_client.py
```

Generated images will be saved in the `generated_images` directory.

## API Endpoints

### Generate Image

- **URL**: `/generate-image`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "prompt": "your image generation prompt"
  }
  ```
- **Response**: Returns a list of base64-encoded images

## Using the Example Code

The `example_client.py` provides a complete example of:
- Sending image generation requests
- Handling API responses
- Saving generated images

You can modify the `prompt` variable to generate different images:

```python
prompt = """your custom prompt here"""
generate_image(prompt)
```

## Security Best Practices

1. Never hardcode API tokens in your code
2. Ensure `.env` is included in `.gitignore`
3. Use environment variables or secure key management services in production
4. Rotate API tokens periodically

## Troubleshooting

If you encounter issues:
1. Verify your `REPLICATE_API_TOKEN` is correctly set
2. Ensure the FastAPI server is running
3. Check all dependencies are properly installed
4. Verify network connectivity

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
