from flask import Flask, request, render_template
import pickle
import re
from logger import logger  # ✅ Import the advanced logger

app = Flask(__name__)

logger.info(f"Flask Server Started!")


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
    return 'Vulnerable' if prediction == 1 else 'Safe'

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ''
    if request.method == 'POST':
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        logger.info(f"Prediction request from IP: {user_ip}, Browser: {user_agent}")

        try:
            code = request.form['code']
            logger.info(f"Code received (preview): {code[:80].replace(chr(10), ' ')}...")
            cleaned_code = preprocess_code(code)

            vectorized_code = vectorizer.transform([cleaned_code])
            logger.info(f"Vectorized code: {vectorized_code}")

            prediction = get_prediction(vectorized_code)
            logger.info(f"Prediction result: {prediction}")

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            prediction = f"Error: {str(e)}"

    logger.info(f"==================== Open Home Page ====================")

    return render_template('index.html', prediction=prediction)

@app.errorhandler(Exception)
def handle_error(e):
    logger.exception("Unhandled application error")
    return render_template('index.html', prediction=f"Error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True)
