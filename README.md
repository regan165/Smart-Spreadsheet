# Smart-Spreadsheet

## How to Use the App

### Prerequisites

Ensure you have the following installed:
- Python 3.12.4
- pip 24.0 
- Docker (optional, for running with Docker)

### Installation

Clone the repository:
- `git clone https://github.com/regan165/Smart-Spreadsheet.git`
- `cd smart-spreadsheet`

#### Using Virtual Environment (Optional but Recommended)

Create and activate a virtual environment:
- `python3 -m venv capix_env`
- `source capix_env/bin/activate`  # On Windows, use `capix_env\Scripts\activate`

Install the required packages:
- `pip install -r requirements.txt`

### Running the App

#### Running with Python

Start the Flask app:
- `python app.py`

Access the app:
- Open your browser and go to `http://localhost:8080/`.

#### Running with Docker

Build the Docker image:
- `docker build -t smart-spreadsheet .`

Run the Docker container:
- `docker run -p 8080:8080 smart-spreadsheet`

Access the app:
- Open your browser and go to `http://localhost:8080/`.

### Using the App

#### Upload Excel/CSV Files
- Provide your OpenAI API key.
- Choose the Excel or CSV files you want to upload.
- Click the "Upload" button.

#### Ask Questions
- Once the files are uploaded, you can ask questions about the data.
- Enter your question in the provided input field and click "Ask".
- The app will process the question and display the answer.
