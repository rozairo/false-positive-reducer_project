from flask import Flask, request, render_template
import pickle
import re

app = Flask(__name__)

# Load model and vectorizer
with open('static/model/model.pickle', 'rb') as file:
    rf = pickle.load(file)

with open('static/model/vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)


# Preprocess function
def preprocess_code(code):
    code = str(code)
    code = re.sub(r'/\*.*?\*/', ' ', code, flags=re.DOTALL)
    code = re.sub(r'\s+', ' ', code)
    code = re.sub(r'<.*?>', ' ', code)
    code = re.sub(r'\b(?:package|import|public|class|function|php|<\?php|\?>)\b', ' ', code)
    code = code.lower()
    return code.strip()

# Prediction function
def get_prediction(vectorized_text):
    prediction = rf.predict(vectorized_text)
    if prediction == 1:
        return 'Vulnerable'
    else:
        return 'Safe'

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ''
    if request.method == 'POST':
        try:
            code = request.form['code']
            cleaned_code = preprocess_code(code)
            vectorized_code = vectorizer.transform([cleaned_code])
            prediction = get_prediction(vectorized_code)
        except Exception as e:
            prediction = f"Error: {str(e)}"
    return render_template('index.html', prediction=prediction)

@app.errorhandler(Exception)
def handle_error(e):
    return render_template('index.html', prediction=f"Error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True)
