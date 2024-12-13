from flask import Blueprint, render_template, request, jsonify
import re
import os

# Create a new blueprint for the personal info redactor
redactor_app = Blueprint('redactor_app', __name__)

# Define regex patterns for detecting personal information
EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_PATTERN = r'\+?[1-9][0-9]{1,14}'
NAME_PATTERN = r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'  # Basic name detection (Firstname Lastname)

# Function to redact personal information in the document text
def redact_personal_info(text):
    # Redact email addresses
    text = re.sub(EMAIL_PATTERN, '[REDACTED EMAIL]', text)
    # Redact phone numbers
    text = re.sub(PHONE_PATTERN, '[REDACTED PHONE]', text)
    # Redact names (basic approach, can be improved)
    text = re.sub(NAME_PATTERN, '[REDACTED NAME]', text)
    return text

# Route to display the redaction page
@redactor_app.route("/redactor", methods=["GET", "POST"])
def redactor():
    if request.method == "POST":
        # Process the uploaded file
        file = request.files.get('file')
        if file:
            file_content = file.read().decode('utf-8')  # Assuming it's a text file
            redacted_content = redact_personal_info(file_content)

            # Save redacted file
            # Use os.path.join() for cross-platform compatibility
            output_file_path = os.path.join(os.getcwd(), 'captured_images', 'redacted_file.txt')
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            with open(output_file_path, 'w') as output_file:
                output_file.write(redacted_content)

            return jsonify({"message": "File redacted successfully!", "redacted_file": output_file_path})
        else:
            return jsonify({"message": "No file uploaded!"}), 400
    return render_template("redactor.html")
