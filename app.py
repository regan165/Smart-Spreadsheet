import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from extractor import ExcelTableExtractor
import pandas as pd
from openai import OpenAI, AuthenticationError

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Store session data in a lightweight database or improve session management
session_data = {}

def chat(api_key, role, query, history):
    openai_client = OpenAI(api_key=api_key)
    if len(history) > 10:
        history = history[:1] + history[-9:]
    history.append({"role": "user", "content": query})

    completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=history,
        temperature=0.2,
        max_tokens=1000
    )
    result = completion.choices[0].message.content
    history.append({"role": "assistant", "content": result})
    return result, history

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({"error": "No API key provided"}), 403

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files selected for uploading"}), 400

    extractor = ExcelTableExtractor()
    csv_contents = []

    for file in files:
        if file.filename == '':
            continue
        try:
            file_path = os.path.join('/tmp', secure_filename(file.filename))
            file.save(file_path)
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file_path)
                csv_contents.append(extractor.clean_csv_content(df.to_csv(index=False)))
            else:
                workbook = extractor.open_file(file_path)
                for sheetname in workbook.sheetnames:
                    sheet = workbook[sheetname]
                    tables = extractor.extract_tables(sheet)
                    dataframes = extractor.to_dataframes(tables)
                    csv_contents.extend([extractor.clean_csv_content(df.to_csv(index=False)) for df in dataframes])
        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {e}")
            return jsonify({"error": f"Error processing file {file.filename}"}), 500

    session_id = "session"
    session_data[session_id] = {
        'csv_contents': csv_contents,
        'history': [{"role": "system", "content": "You are a financial analyst. Your task is to analyze the data provided and give clear, concise, and structured financial insights."}],
        'api_key': api_key
    }

    return jsonify({"csv_contents": csv_contents})

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    session_id = "session"

    if not session_id or session_id not in session_data:
        return jsonify({"error": "Session expired or not found. Please upload the files again."}), 400

    if not question:
        return jsonify({"error": "No question provided"}), 400

    csv_contents = session_data[session_id]['csv_contents']
    history = session_data[session_id]['history']
    api_key = session_data[session_id]['api_key']

    csv_data = "\n".join(csv_contents)
    prompt = f"Data: {csv_data}\n\nAs a financial analyst, answer the following question based on the provided data. Question: {question}"

    try:
        response, history = chat(api_key, "user", prompt, history)
    except AuthenticationError:
        return jsonify({"error": "Invalid API Keys"}), 401
    except Exception as e:
        logging.error(f"Error during chat completion: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

    session_data[session_id]['history'] = history

    return jsonify({'answer': response, 'csv_contents': csv_contents})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
