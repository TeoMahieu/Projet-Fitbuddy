import google.generativeai as genai

# Clé API (stocke-la en variable d'environnement pour plus de sécurité)
API_KEY = "AIzaSyAfibHeAZuqFSTez1Ub4urfJzBwmcrPGNc"
genai.configure(api_key=API_KEY)

def get_fitness_recommendation(age, weight, goal):
    # Construire un prompt optimisé
    prompt = f"""
    Je suis un utilisateur de {age} ans, pesant {weight} kg, et mon objectif est {goal}.
    Peux-tu me proposer un plan d'entraînement ?
    """

    # Appel à l'API Gemini
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    return response.text  # Renvoie la réponse générée par Gemini

# Test
print(get_fitness_recommendation(25, 70, "prise de masse"))
