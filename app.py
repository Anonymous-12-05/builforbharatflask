from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load dataset
data = pd.read_csv("amazon_data_latest.csv")

# Define the scoring parameters and their weights
scoring_parameters = {
    'compliance': {
        'label_compliance': 0.3,
        'display_compliance': 0.3,
    },
    'correctness': {
        'authenticity': 0.4,
        'branding': 0.6,
    },
    'completeness': {
        'attributes': 0.7,
    },
}

def assess_compliance(row):
    required_labels = ['Selling Price', 'Brand Name', 'Product Name']
    required_displays = ['Image', 'Product Description']
    compliance_score = 0
    for label in required_labels:
        if label in row:
            compliance_score += 1 / len(required_labels)
    for display in required_displays:
        if display in row:
            compliance_score += 1 / len(required_displays)
    return int(compliance_score * 10) / 10

def assess_correctness(row):
    authentic_brands = ['Apple', 'Samsung', 'Nike', 'Bosch', 'Johnson & Johnson', 'Carrefour', 'LEGO', 'Adidas', 'Johnson & Johnson', 'MAC cosmetics']
    correctness_score = 0
    if row['Brand Name'] in authentic_brands:
        correctness_score += 1 / 2
    if row['Brand Name'] in row['Product Name']:
        correctness_score += 1 / 2
    return int(correctness_score * 10) / 10

def assess_completeness(row):
    required_attributes = ['Selling Price', 'Brand Name', 'Product Name', 'Image', 'Product Description']
    completeness_score = 0
    for attribute in required_attributes:
        if attribute in row:
            completeness_score += 1 / len(required_attributes)
    return int(completeness_score * 10) / 10

def compute_objective_store(row):
    compliance_score = assess_compliance(row)
    correctness_score = assess_correctness(row)
    completeness_score = assess_completeness(row)
    objective_store = (
        compliance_score * scoring_parameters['compliance']['label_compliance'] +
        correctness_score * scoring_parameters['correctness']['authenticity'] +
        completeness_score * scoring_parameters['completeness']['attributes']
    )
    return objective_store

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    brand_name = request.form['brand_name']
    product_name = request.form['product_name']
    selling_price = request.form['selling_price']
    image = request.form['image']
    product_description = request.form['product_description']
    
    row = {
        'Brand Name': brand_name,
        'Product Name': product_name,
        'Selling Price': selling_price,
        'Image': image,
        'Product Description': product_description
    }
    
    objective_score = compute_objective_store(row)
    
    return render_template('result.html', score=objective_score)

if __name__ == '__main__':
    app.run(debug=True)
