from googletrans import Translator

import trafilatura
from sentence_transformers import SentenceTransformer

from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load your XGBoost model
model = joblib.load('model/best_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    prediction_result = "Phishing" # or it will be "Legitimate"
    if 'htmlFile' not in request.files:
        return "No file part"
    
    file = request.files['htmlFile']

    if file.filename == '':
        return "No selected file"

    # Save the uploaded file to a temporary location
    file_path = 'test/' + file.filename
    file.save(file_path)

    # START of the business logic here
    # Perform prediction using the file_path with your XGBoost model
    # Replace the following line with your actual prediction logic
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html = file.read()
    except:
        with open(file_path, 'r', encoding='windows-1252') as file:
            html = file.read()
    extracted_html= trafilatura.extract(html)
    #we found our best model with sbert embedding model and xgb
    embedding_model = SentenceTransformer("sentence-transformers/bert-base-nli-mean-tokens",device="cuda")
    translator = Translator()
    max_chars = 4900
    if(len(extracted_html)>max_chars):
        chunks = [extracted_html[j:j + max_chars] for j in range(0, len(extracted_html), max_chars)]
        translated_text = ' '.join([translator.translate(chunk, dest='en').text for chunk in chunks])
    else:
        translated_text = translator.translate(extracted_html).text

    encoded_html=embedding_model.encode(translated_text)
    encoded_html = encoded_html.reshape(1, -1)

    predict = model.predict(encoded_html)
    if(predict==0):
        prediction_result = "Legitimate"

    return f"{file_path} is {prediction_result}"

if __name__ == '__main__':
    app.run(debug=True, port=5050)