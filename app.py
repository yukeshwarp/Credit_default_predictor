from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Azure endpoint URL and authentication key
Endpoint = "https://credit-endpoint-1-64baceca.eastus.inference.ml.azure.com/score"
Auth_key = "mklqY8WbYbezmnFs2iwVMG9PpRI1c4on"

@app.route('/', methods=['POST', 'GET'])
def home():
    # Pass 'enumerate' to the template
    return render_template('Index.html', enumerate=enumerate)

@app.route('/predict', methods=['POST'])
def predict():
    # Collect data from form
    data_row = []

    for i in range(23):
        feature_value = int(request.form.get(f'feature_{i}'))
        data_row.append(feature_value)

    # Prepare data InputData for API
    InputData = {
        "input_data": {
            "columns": list(range(23)),
            "index": [0],
            "data": [data_row]
        }
    }

    # Set headers with bearer token
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {Auth_key}'}

    try:
        # Make request to Azure endpoint
        response = requests.post(url=Endpoint, json=InputData, headers=headers)
        print("Response content:", response.content)  # Print response content for debugging

        # Process prediction result
        if response.status_code == 200:
            prediction = response.json()
            return render_template('Index.html', prediction=prediction, enumerate=enumerate)
        else:
            error_message = f"Error: {response.status_code}. Prediction failed."
            return render_template('Index.html', error_message=error_message, enumerate=enumerate)
    except Exception as e:
        error_message = str(e)
        return render_template('Index.html', error_message=error_message, enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)
