from flask import Flask, render_template, request
import os
import google.generativeai as generative_ai
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv(".env.local")

app = Flask(__name__)

# Set your Gemini API key from the .env.local file
api_key = os.getenv("GOOGLE_API_KEY")  # Ensure this key exists in .env.local

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env.local")

generative_ai.configure(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    reviewed_code = None
    if request.method == "POST":
        code_to_review = request.form.get("code")

        if code_to_review:
            try:
                # Gemini API interaction
                model = generative_ai.GenerativeModel('gemini-pro')
                prompt = f"""Review the following code and provide suggestions for improvement:

python
{code_to_review}
"""

                response = model.generate_content(prompt)

                reviewed_code = response.text  # Get the response text

            except Exception as e:
                reviewed_code = f"Error during code review: {str(e)}"

    return render_template("index.html", reviewed_code=reviewed_code)

if __name__ == "__main__":
    app.run(debug=True)
