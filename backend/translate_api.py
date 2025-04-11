from fastapi import FastAPI, Query, HTTPException, Request
from urllib.parse import quote
import logging
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI()

# Configure logging
log_file = "./translate_api.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming requests.
    """
    # Log request details
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

@app.get("/translate")
async def translate(
    action: str = Query(..., description="Action to perform (translate, pronounce, ai, image)"),
    text: str = Query(..., description="The text to process"),
    template: int = Query(None, description="Template number for AI queries (1, 2, 3, or 4)"),
    model: str = Query("chatgpt", description="Model for AI queries (chatgpt, gemini, grok)")
):
    """
    Translate API endpoint that builds and returns URLs based on the input arguments.
    """
    # Log the request parameters
    logging.info(f"Action: {action}, Text: {text}, Template: {template}, Model: {model}")

    # URL-encode the text
    encoded_text = quote(text)

    # Handle different actions
    if action == "pronounce":
        url = f"https://www.google.com/search?q=pronounce+{encoded_text}"
    elif action == "ai":
        # Validate template
        if template not in [1, 2, 3, 4]:
            logging.error("Invalid template provided.")
            raise HTTPException(status_code=400, detail="Invalid template. Must be 1, 2, 3, or 4.")

        # Build the question based on the template
        if template == 1:
            question = f"explain this \"{text}\""
        elif template == 2:
            question = f"what does this mean \"{text}\""
        elif template == 3:
            question = f"translate this in arabic \"{text}\""
        else:
            question = f"\"{text}\""  # Default to just the selected text

        # URL-encode the question
        encoded_question = quote(question)

        # Validate model
        if model not in ["chatgpt", "gemini", "grok", "perplexity"]:
            logging.error("Invalid model provided.")
            raise HTTPException(status_code=400, detail="Invalid model. Must be chatgpt, gemini, grok, or perplexity.")

        # Build the URL based on the model
        if model == "gemini":
            url = f"https://gemini.google.com/?q={encoded_question}"
        elif model == "grok":
            url = f"https://x.com/i/grok?text={encoded_question}"
        elif model == "perplexity":
            url = f"https://www.perplexity.ai/search?q={encoded_question}"
        else:  # Default to chatgpt
            url = f"https://chat.openai.com/?q={encoded_question}"
    elif action == "image":
        url = f"https://www.google.com/search?tbm=isch&q={encoded_text}"
    elif action == "translate":
        url = f"https://translate.google.com/details?sl=en&tl=ar&text={encoded_text}&op=translate"
    else:
        logging.error("Invalid action provided.")
        raise HTTPException(status_code=400, detail="Invalid action. Must be translate, pronounce, ai, or image.")

    # Log the generated URL
    logging.info(f"Generated URL: {url}")

    return {"url": url}

@app.get("/models")
async def get_models():
    """
    Retrieve the list of available AI models.
    """
    models = ["chatgpt", "gemini", "grok", "perplexity"]
    logging.info(f"Retrieved AI models: {models}")
    return {"models": models}