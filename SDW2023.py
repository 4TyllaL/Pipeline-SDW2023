import pandas as pd
import openai
import requests
import json

# URL da API SDW 2023
sdw_2023_api_url = 'https://sdw-2023-prd.up.railway.app'

# Carregar os dados do CSV
df = pd.read_csv('SDW2023.csv')

# Obter a lista de IDs de usuário
user_ids_list = df['UserID'].tolist()

# Função para buscar um usuário por ID
def fetch_user_by_id(id):
    response = requests.get(f'{sdw_2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

# Filtrar os usuários válidos
valid_users = [user_info for user_id in user_ids_list if (user_info := fetch_user_by_id(user_id)) is not None]

# Definir a chave da API OpenAI
openai.api_key = "chave_de_api_aqui"

# Função para gerar notícias AI
def generate_ai_news(user_info):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em marketing bancário."
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user_info['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

# Iterar pelos usuários válidos e gerar notícias para cada um
for user_info in valid_users:
    news_message = generate_ai_news(user_info)
    print(news_message)
    user_info['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news_message
    })
