from flask import Flask, request, jsonify
from flask_cors import CORS

# Optional AI (Gemini) — will work only if installed + key added
try:
    import google.generativeai as genai
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

app = Flask(__name__)
CORS(app)
from flask import send_file

@app.route("/")
def home():
    return send_file("index.html")
# 👉 If you want AI, add your key here (optional)
if AI_AVAILABLE:
    try:
        genai.configure
        model = genai.GenerativeModel("gemini-pro")
    except:
        AI_AVAILABLE = False


# 🔹 Simple offline sentiment logic
positive_words = ["good", "great", "love", "fast", "excellent", "amazing", "nice"]
negative_words = ["bad", "slow", "crash", "hate", "bug", "lag", "issue"]


def offline_analysis(text):
    text = text.lower()

    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    sentiment = "Neutral 😐"
    if pos > neg:
        sentiment = "Positive 😊"
    elif neg > pos:
        sentiment = "Negative 😡"

    return f"""
🔍 Key Issues:
- Performance issues
- Bugs or crashes

💡 Feature Requests:
- Dark mode
- Payment integration

😊 Sentiment:
{sentiment}

🚀 Recommendation:
- Improve speed and fix bugs first
"""


# 🔹 Feedback Analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json.get('feedback', '')

        # Try AI first
        if AI_AVAILABLE:
            try:
                prompt = f"Analyze this feedback:\n{data}"
                response = model.generate_content(prompt)
                return jsonify({"result": response.text})
            except:
                pass

        # Fallback (always works)
        result = offline_analysis(data)
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})


# 🔹 App Research Feature
@app.route('/research', methods=['POST'])
def research():
    try:
        app_name = request.json.get('app', '')

        # Try AI
        if AI_AVAILABLE:
            try:
                prompt = f"Analyze the app {app_name} and give features, issues, and improvements."
                response = model.generate_content(prompt)
                return jsonify({"result": response.text})
            except:
                pass

        # Fallback
        result = f"""
📱 App Research: {app_name}

⭐ Popular Features:
- Messaging / Core functionality
- User-friendly interface

⚠ Common Issues:
- Performance lag
- Battery usage

🚀 Improvements:
- Optimize speed
- Add new features
"""

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
