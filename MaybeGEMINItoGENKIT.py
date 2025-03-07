import google.generativeai as genai

# Configurer l'API Gemini
genai.configure(api_key="AIzaSyAfibHeAZuqFSTez1Ub4urfJzBwmcrPGNc")
model = genai.GenerativeModel("gemini-2.0-flash")

# Fonction simple pour interagir avec Gemini
def ai_coach(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

# Tester
print(ai_coach("Comment optimiser une séance de musculation ?"))