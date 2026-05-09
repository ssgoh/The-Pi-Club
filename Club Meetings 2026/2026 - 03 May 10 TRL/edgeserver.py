from flask import Flask, request, jsonify
from edge_impulse_linux.runner import ImpulseRunner
import os
app = Flask(__name__)
# Use the absolute path we verified yesterday
model_file = '/home/raspberry/model.eim'
# Initialize the runner
runner = ImpulseRunner(model_file)
runner.init()
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = data['features']
        # Run the AI model
        res = runner.classify(features)
        
        # 'result' contains the scores for IDLE and FAN_ON
        predictions = res['result']['classification']
        
        # Pick the label with the highest score
        label = max(predictions, key=predictions.get)
        confidence = predictions[label]
        print(f"Input: {features} -> Prediction: {label} 
({confidence*100:.2f}%)")
        return jsonify({
            "label": label,
            "confidence": predictions  # Returns scores for both classes
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    # Listen on all network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000)
