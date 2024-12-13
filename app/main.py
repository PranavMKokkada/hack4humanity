from flask import Flask, render_template
from camera_scanner import camera_app
from chatbot import chatbot_app  # Import chatbot as a Blueprint
from personal_info_redactor import redactor_app

app = Flask(__name__)

# Register blueprints for camera scanning, chatbot, and personal info redactor
app.register_blueprint(camera_app, url_prefix='/camera')
app.register_blueprint(chatbot_app, url_prefix='/chat')
app.register_blueprint(redactor_app, url_prefix='/redactor')

# Route for the home page (index.html)
@app.route("/")
def index():
    return render_template("index.html")

# Route to render the personal info redactor page (redactor.html)
# This will now work when you navigate to /redactor on your site
@app.route("/redactor")
def redactor():
    return render_template("redactor.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")