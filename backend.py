
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename  # Import secure_filename function to safely save the file
from keras.models import load_model
import librosa 
import numpy as np
import os

app = Flask(__name__)
model = load_model('audio_detection_model.h5')

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the filename is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3', 'ogg', 'flac'}  # Add more extensions if needed

def extract_features(audio_file):
    try:
        y, sr = librosa.load(audio_file)

        # Extracting features (similar to the training process)
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_fft=1024, hop_length=256), axis=1)
        chroma_cqt = np.mean(librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=256), axis=1)
        tonnetz = np.mean(librosa.feature.tonnetz(y=y, sr=sr), axis=1)

        features = np.hstack([mfccs, chroma_cqt, tonnetz])

        return features

    except Exception as e:
        print(f"Error processing {audio_file}: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            if allowed_file(uploaded_file.filename):  # Check if the file extension is allowed
                # Save the uploaded file
                filename = secure_filename(uploaded_file.filename)  # Securely get a valid filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(file_path)

                # Extract features from the uploaded file
                features = extract_features(file_path)

                if features is not None:
                    # Reshape the features and prepare them for input to the model
                    features = np.expand_dims(features, axis=0)
                    features = np.expand_dims(features, axis=2)

                    # Make predictions
                    prediction = model.predict(features)

                    # Interpret the predictions
                    if prediction[0][0] > prediction[0][1]:
                        result = "AI-generated speech"
                    else:
                        result = "Human speech"

                    # Delete the uploaded file after processing (optional)
                    # os.remove(file_path)

                    return jsonify({'result': result})
                else:
                    return jsonify({'error': 'Error processing audio file'})
            else:
                return jsonify({'error': 'Unsupported file format'})
        else:
            return jsonify({'error': 'No file uploaded'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
