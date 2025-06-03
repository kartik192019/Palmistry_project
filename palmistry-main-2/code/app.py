from flask import Flask, render_template, request, send_from_directory
import os
from read_palm import main  # Import the main function from your read_palm.py file

app = Flask(__name__)

# Set the directory to serve the result image from
RESULTS_FOLDER = os.path.join(os.getcwd(), 'results')

# Ensure the 'results' directory exists
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

# Define the main route to render the upload form
@app.route('/')
def home():
    return render_template('index.html')  # Assuming you have an HTML file for uploading

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    file = request.files['file']  # Assuming your HTML form has a 'file' input field
    filename = file.filename
    file_path = os.path.join(RESULTS_FOLDER, filename)

    # Save the uploaded file temporarily
    file.save(file_path)

    # Call the main function from read_palm.py to process the image
    # This is where you call your existing palmistry processing logic
    try:
        # Process the file and generate the result.jpg
        result_path = os.path.join(RESULTS_FOLDER, 'result.jpg')
        main(file_path)  # Pass the saved file path to main() function for processing
        return render_template('result.html')  # Assuming this is where you display the result page
    except Exception as e:
        return f"Error processing image: {e}", 500

# Route to serve the result image (result.jpg)
@app.route('/result-image')
def result_image():
    # Send the result.jpg file from the results directory
    return send_from_directory(RESULTS_FOLDER, 'result.jpg')

# Route to display the result page
@app.route('/result')
def result():
    return render_template('result.html')  # This page would display the result image

if __name__ == '__main__':
    app.run(port=5000)