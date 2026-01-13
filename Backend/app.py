import os  # 'Import' must be lowercase 'import'
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
# Ensure gemini.py exists in the same directory and has analyze_question_paper defined
from gemini import analyze_question_paper 

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
CORS(app)

print("CWD:", os.getcwd())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # Added error handling for missing JSON or incorrect Content-Type
    data = request.get_json(force=True, silent=True)
    
    if not data:
        return jsonify({"error": "Invalid JSON or empty request"}), 400

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "difficulty_score": 0,
            "topics": {}
        })

    try:
        result = analyze_question_paper(text)
        return jsonify(result)
    except Exception as e:
        # Use a logging tool or keep print for local debugging
        print(f"ANALYSIS ERROR: {e}")
        return jsonify({
            "error": "Analysis failed",
            "difficulty_score": 0,
            "topics": {}
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)