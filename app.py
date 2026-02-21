import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from sklearn import preprocessing # Required for normalization

app = Flask(__name__)

# Load your .keras model
try:
    model = load_model('ids_trained_model.keras')
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])

def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    try:
        # Read CSV directly into memory
        df = pd.read_csv(file)
        
        # Ensure only numeric data is processed
        # Logic Preservation: Select features in the correct order (69 fields)
        features = df.select_dtypes(include=[np.number]).values
        
        # Batch Normalization (Critical for accuracy)
        features_normalized = preprocessing.normalize(features)
        
        # Batch Prediction
        predictions = model.predict(features_normalized)
        
        # Calculate results
        total_points = len(predictions)
        attack_count = np.sum(predictions > 0.5)
        benign_count = total_points - attack_count
        
        attack_pct = (attack_count / total_points) * 100
        benign_pct = (benign_count / total_points) * 100
        
        return jsonify({
            'status': 'success',
            'total_rows': int(total_points),
            'attack_percentage': f"{attack_pct:.2f}%",
            'benign_percentage': f"{benign_pct:.2f}%",
            'attack_count': int(attack_count),
            'benign_count': int(benign_count)
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Processing Error: {str(e)}"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        raw_input = data.get('row_data')
        
        # 1. Parse the raw string into a list of floats
        # Replaces tabs/spaces/newlines with commas for uniform splitting
        clean_input = raw_input.replace('\t', ',').replace(' ', ',').replace('\n', ',')
        features = [float(x) for x in clean_input.split(',') if x.strip()]
        
        # 2. Convert to Numpy and Reshape
        # Neural networks expect a 2D array: (batch_size, number_of_features)
        features_np = np.array(features).reshape(1, -1)
        
        # ---------------------------------------------------------
        # CRITICAL FIX: LOGIC PRESERVATION (NORMALIZATION)
        # ---------------------------------------------------------
        # We must use the same normalization technique used in your training script
        features_normalized = preprocessing.normalize(features_np)
        
        # 3. Prediction
        prediction = model.predict(features_normalized)
        probability = float(prediction[0][0])
        
        # Logic: 0.5 threshold for sigmoid binary classification
        result = "ATTACK" if probability > 0.97 else "BENIGN"
        
        return jsonify({
            'status': 'success',
            'prediction': result,
            'confidence': f"{probability * 100:.2f}%",
            'is_attack': result == "ATTACK"
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Preprocessing Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
