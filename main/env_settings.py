import os 

GROQ_API_KEY = 'your_api_key'

db_path = 'sqlite:///database/example.db'
model_name = "llama-3.1-70b-versatile"

def env_init():
    os.environ['GROQ_API_KEY']=GROQ_API_KEY
 