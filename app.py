from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from extractor import ExcelTableExtractor
from openai import OpenAI
import logging
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

load_dotenv()  # Load environment variables from .env file

# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat(role, query, history):
    # Ensure history is within limits
    if len(history) > 10:
        history = history[:1] + history[-9:]
    history.append({"role": "user", "content": query})

    completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=history,
        temperature=0.2,
        max_tokens=1000  # Adjust max tokens if needed
    )
    result = completion.choices[0].message.content
    history.append({"role": "assistant", "content": result})
    return result, history

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    if 'files' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files selected for uploading"}), 400

    extractor = ExcelTableExtractor()
    csv_contents = []

    for file in files:
        if file.filename == '':
            continue
        file_path = os.path.join('/tmp', secure_filename(file.filename))
        file.save(file_path)
        sheet = extractor.open_file(file_path)
        tables = extractor.extract_tables(sheet)
        dataframes = extractor.to_dataframes(tables)
        csv_contents.extend([extractor.clean_csv_content(df.to_csv(index=False)) for df in dataframes])

    # Limit the length of the summary prompt
    summary_prompt = "As a financial analyst, provide a structured summary analysis of the following data in 1000 characters or less. Highlight key financial metrics and trends:\n"
    for csv_content in csv_contents:
        if len(summary_prompt) + len(csv_content) > 1500:  # Adjust limit as needed
            break
        summary_prompt += csv_content + "\n"

    # Initialize history with the summary prompt
    history = [{"role": "system", "content": "You are a financial analyst. Your task is to analyze the data provided and give clear, concise, and structured financial insights."},
               {"role": "user", "content": summary_prompt}]
    
    summary_response, history = chat("system", summary_prompt, history)

    return jsonify({
        "summary": summary_response,
        "history": history
    })

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    history = request.json.get('history', [])

    if not question:
        return jsonify({"error": "No question provided"}), 400

    prompt = f"As a financial analyst, answer the following question based on the provided data: {question}"
    response, history = chat("user", prompt, history)
    return jsonify({'answer': response, 'history': history})

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, port=5000)  # Make sure the port matches your frontend requests
