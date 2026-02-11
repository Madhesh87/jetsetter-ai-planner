from flask import Flask, render_template, request
from groq import Groq
import os
from dotenv import load_dotenv
import markdown2

# Load variables from .env file
load_dotenv()

# Get the key safely from the environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    plan = ""
    if request.method == "POST":
        city = request.form["city"]
        days = request.form["days"]
        
        prompt = f"Create a {days}-day travel plan for {city}. Use bullet points for activities."

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_content = response.choices[0].message.content
        plan = markdown2.markdown(raw_content)

    return render_template("index.html", plan=plan)

if __name__ == "__main__":
    app.run(debug=True)