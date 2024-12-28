import os
import google.generativeai as genai

# Function to generate a response
def GenerateResponse(input_text, api_key):
    # Ensure API key is configured
    genai.configure(api_key=api_key)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 3000,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    # Generate content
    prompt = f"""
    "you are a Nutrition Chatbot reply accordingly!",
        "input: who are you",
        "output: I am a Nutrition chatbot.",
        "input: what all you do",
        "output: I can provide personalized dietary advice, meal planning, nutrition tracking, and health insights to help users achieve their wellness goals.",
        f"input: {input_text}",
        "output: """

    response = model.generate_content([prompt])

    return response.text
