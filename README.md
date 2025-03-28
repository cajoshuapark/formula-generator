# game-translator
game script translator for indie game devs

Command for running the backend
0. create virtual environtmnet
python -m venv venv

1. Start virtual env:
source venv/bin/activate

2. Download requirements
pip install -r requirements.txt

3. download postgresql
    - create a user and password and make a database called formula
    - sudo -u postgres psql
    - ALTER USER postgres WITH PASSWORD 'your_new_password';
    - CREATE DATABASE formula;
    - quit 

4. create a file named .env and add these codes into it and change the password to your password. also get deepseek api key. you can use my openai key for now
DATABASE_URL=postgresql://postgres:password@localhost/formula
DEEPSEEK_API_KEY=

5. Run python app.py to run the backend. 

6. testing database interaction


TESTING
open a new terminal while running the backend and copy this into terminal to test api call
*** run python reset.py to resest the database before you start testing. 

1. create formula test

curl -X POST http://localhost:5000/create-formula \
-H "Content-Type: application/json" \
-d '{
  "top_note": {
    "Citrus": [
      {"Lemon": "8%"},
      {"Bergamot": "7%"}
    ]
  },
  "body_note": {
    "Floral": [
      {"Orris": "6%"},
      {"Jasmine": "2%"},
      {"Jasmine": "4%"}
    ]
  },
  "base_note": {
    "Woody": [
      {"Vetiver": "3%"}
    ]
  }
}'

2. scrape website information
curl -X POST http://127.0.0.1:5000/update-website-content -H "Content-Type: application/json" -d '{"url": "https://aromahazelyang.wpcomstaging.com/"}'

3. chatbot feature
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"message": "Tell me about this website","session_id" :"testingid"}'  
