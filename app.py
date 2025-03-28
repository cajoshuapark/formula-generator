from flask import Flask
from models import db
from routes import create_formula, chat, update_website_content
from config import Config
from flask_cors import CORS  # Import CORS

# Initialize Flask app and database
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS for all routes
db.init_app(app)

with app.app_context():
    db.create_all()  # Creates tables based on models

app.add_url_rule('/create-formula', 'create-formula', create_formula, methods=['POST'])
app.add_url_rule('/chat', 'chat', chat, methods=['POST'])
app.add_url_rule('/update-website-content', 'update-website-content', update_website_content, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
