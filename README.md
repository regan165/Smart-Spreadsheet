How to Use the App

Prerequisites

Ensure you have the following installed:
Python 3.7+
pip (Python package installer)

Installation

Clone the repository:
git clone https://github.com/your-repo/smart-spreadsheet.git
cd smart-spreadsheet

Create and activate a virtual environment (optional but recommended):
python -m venv capix_env
source capix_env/bin/activate  # On Windows, use `capix_env\Scripts\activate`

Install the required packages:
pip install -r requirements.txt

Running the App

Start the Flask app:
python app.py

Access the app:
Open your browser and go to http://127.0.0.1:5000/.

Using the App

Upload Excel/CSV files:
Provide your OpenAI API key.
Choose the Excel or CSV files you want to upload.
Click the "Upload" button.

Ask Questions:
Once the files are uploaded, you can ask questions about the data.
Enter your question in the provided input field and click "Ask".
The app will process the question and display the answer.

Troubleshooting
If you encounter issues during file upload or API interactions, ensure your files are correctly formatted and your OpenAI API key is valid.
Check the console for error messages and logs for more detailed debugging information.

Deployment
For deploying the app, you can use Docker or any cloud service like AWS, Heroku, etc. Ensure to configure the environment variables and secure your API keys properly.


