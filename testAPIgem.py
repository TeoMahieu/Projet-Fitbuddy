import google.generativeai as genai

# 🔑 Configure l'API Gemini
genai.configure(api_key="AIzaSyAfibHeAZuqFSTez1Ub4urfJzBwmcrPGNc")

# Charger le modèle
model = genai.GenerativeModel("gemini-2.0-flash")

# Envoyer une requête
response = model.generate_content("Quels exercices recommandes-tu pour la prise de masse ?")

# Afficher la réponse
print(response.text)
