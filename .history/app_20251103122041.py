import numpy as np
import pandas as pd 
from flask import Flask, request, jsonify, render_template, send_file, make_response
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import warnings
from io import BytesIO
warnings.filterwarnings('ignore')
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from report import create_report 
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()

    # Generate PDF report as a BytesIO object
    pdf_buffer = create_report(data)

    # Send PDF as preview (not forced download)
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=DG_Foundation_Report.pdf'
    return response
    
    

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)