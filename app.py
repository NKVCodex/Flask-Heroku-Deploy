from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt)
    if response.parts:
        generated_text = response.text
    else:
        generated_text = "No response generated. Checking safety ratings..."
        for candidate in response.candidates:
            generated_text += f"\nSafety ratings for candidate: {candidate.safety_ratings}"

    return render_template('result.html', prompt=prompt, generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
