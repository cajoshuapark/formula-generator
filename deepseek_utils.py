import json
from config import Config  # Import the Config class
from openai import OpenAI
import re
from models import ChatMessage, Formula, db
from models import db, WebsiteContent


def generate_deepseek_formulas(top_note, body_note, base_note):
    client = OpenAI(api_key=Config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    with open("/Users/cajoshuapark/Dev/work/formula/data/Natural_Ingredient_CA.json", "r") as file:
        ingredients_data_CA = json.load(file)
    
    with open("/Users/cajoshuapark/Dev/work/formula/data/Natural_Ingredient_BT.json", "r") as file:
        ingredients_data_BT = json.load(file)
    
    with open("/Users/cajoshuapark/Dev/work/formula/data/example_formulas.json", "r") as file:
        example_formulas = json.load(file)

    messages = [
        {
            "role": "system",
            "content": f"You are a perfume formula generator. Given a set of top, body, and base notes, generate five unique perfume formulas using available ingredients. this is am example formula: {example_formulas} "
        },
        {
            "role": "user",
            "content": f"Ingredients: {ingredients_data_CA} {ingredients_data_BT}\nTop Note: {top_note}\nBody Note: {body_note}\nBase Note: {base_note}\nGenerate 1 perfume formula using the notes provided. You will have to combine ingredients to create those notes. This is the example format you should be returning: {example_formulas}. Make sure you have 5-6 ingrdients in top node, 10 in body, and 6-7 ingredients in base notes. make sure to include the name, variant, carrier, preservation and description fields as well. Make sure to return a JSON format, this is crucial."
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",  
            messages=messages,
            max_tokens=8000,
        )
        
        content = response.choices[0].message.content.strip()
        messages2 = [
                {
                    "role": "system",
                    "content": f"you are a json expert who can fix wrong json format"
                },
                {
                    "role": "user",
                    "content": f"make sure this json is correct and if not fix it and return a valid json format: {content}"
                }
            ]
        response = client.chat.completions.create(
            model="deepseek-reasoner",  
            messages=messages2,
            max_tokens=8000,
        )
        
        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        json_match = re.search(r'(\{.*?\}|\[.*?\])', content, re.DOTALL)

        
        if json_match:
            content = json_match.group(0)
        else:
            raise ValueError("No valid JSON detected in response.")
        try:
            generated_formulas = json.loads(content)
        except json.JSONDecodeError as e:
            return {"error": "Invalid JSON response from DeepSeek loading.", "response": content}
        
        try:
            return generated_formulas
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: {e}")
            return {"error": "Invalid JSON response from DeepSeek.", "response": content}

    except Exception as e:
        return {"error": str(e)}
    

def chatbot_response(user_message, session_id):
    """Generate chatbot response efficiently without storing duplicate website info."""
    client = OpenAI(api_key=Config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    # Fetch previous messages to maintain context
    previous_messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
    
    # Fetch website content once
    website_entry = WebsiteContent.query.first()
    website_content = website_entry.content if website_entry else None

    messages = []
    
    # Only include website content if it's the first message in the session
    if not previous_messages and website_content:
        messages.append({"role": "system", "content": f"You are a chatbot for a website. Here is the website content: {website_content}"})

    for msg in previous_messages:
        messages.append({"role": "user", "content": msg.user_message})
        messages.append({"role": "assistant", "content": msg.bot_response})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=100
        )

        bot_response = response.choices[0].message.content.strip()

        # Save chat history
        chat_entry = ChatMessage(session_id=session_id, user_message=user_message, bot_response=bot_response)
        db.session.add(chat_entry)
        db.session.commit()

        return bot_response

    except Exception as e:
        return {"error": str(e)}
