from flask import request, jsonify
from models import db, Formula
from deepseek_utils import generate_deepseek_formulas,chatbot_response
from datetime import datetime
import uuid 
from scrape_web import scrape_website

def create_formula():
    data = request.get_json()
    top_note = data['top_note']
    body_note = data['body_note']
    base_note = data['base_note']

    # Generate translations using the prepared inputs.
    generated_formulas = generate_deepseek_formulas(top_note, body_note,base_note)
    formula = Formula(
        top_note = top_note,
        base_note = base_note,
        body_note = body_note,
        formulas = generated_formulas,
        created_at=datetime.utcnow()
    )
    db.session.add(formula)
    db.session.commit()
    return jsonify({
        "message": "formulas created successfully",
        "formula": {
            "top_note": formula.top_note,
            "base_note": formula.base_note,
            "body_note": formula.body_note,
            "formulas": formula.formulas,
            "created_at": formula.created_at
        }
    }), 201


def chat():
    """API endpoint for chatbot interaction."""
    data = request.get_json()
    user_message = data["message"]

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Assign a session ID (create new if missing)
    session_id = data["session_id"]
    if not session_id:
        session_id = str(uuid.uuid4())

    response = chatbot_response(user_message, session_id)
    
    return jsonify({"response": response, "session_id": session_id})


def update_website_content():
    """API route to scrape and update website content."""
    data = request.get_json()
    url = data["url"]

    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = scrape_website(url)
    return jsonify({"message": result})