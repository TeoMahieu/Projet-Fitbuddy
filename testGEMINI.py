import genkit as gk
genkit.configure(api_key="AIzaSyAfibHeAZuqFSTez1Ub4urfJzBwmcrPGNc")

# Données utilisateur (déjà sélectionnées)
age = 25
poids = 70  # en kg
objectif = "prise de masse"

# Création du prompt
prompt = f"""
Je suis un coach de salle de sport. Un utilisateur a les caractéristiques suivantes :
- Âge : {age} ans
- Poids : {poids} kg
- Objectif : {objectif}

Donne-moi un programme d'entraînement personnalisé sur 1 semaine, avec des recommandations alimentaires.
"""

# Appel à Genkit.AI avec Gemini 2.0 Flash
response = genkit.chat(model="gemini-2.0-flash", prompt=prompt)

# Affichage du programme généré
print("💪 Programme personnalisé :")
print(response)
    
    return response.text  # Renvoie la réponse générée par Gemini

# Test
print(get_fitness_recommendation(25, 70, "prise de masse"))
