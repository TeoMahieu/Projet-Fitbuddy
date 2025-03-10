import genkit as gk
import google.generativeai as genai
import boto3  # Pour DynamoDB
import json
import os

# 🔐 Clé API Gemini (stocke-la en variable d'environnement pour la sécurité)
API_KEY = os.getenv("GEMINI_API_KEY")  # Change ton API_KEY ici
genai.configure(api_key=API_KEY)

# 📊 Connexion à DynamoDB (AWS)
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("fitbuddy_gamification")

# 🎮 Système de Gamification : Calcul des points
def calculate_points(training_data):
    base_points = training_data["duration"] * 10  # 10 points par minute
    if training_data["intensity"] == "high":
        base_points *= 1.5  # Bonus pour haute intensité
    return int(base_points)

# 🔍 Génération de défis personnalisés avec Gemini
def generate_challenge(user_performance):
    prompt = f"""
    L'utilisateur a complété {user_performance['workouts']} séances cette semaine.
    Propose un défi motivant et fun qui l'incite à s'améliorer.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text  # Réponse générée par Gemini

# 📊 Sauvegarde des points et progression dans DynamoDB
def save_progress(user_id, training_data):
    points = calculate_points(training_data)

    # Mise à jour des points et ajout du suivi
    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET points = points + :val, workouts = workouts + :one",
        ExpressionAttributeValues={":val": points, ":one": 1}
    )
    return points

# 🔮 Analyse avec Genkit.IA (prédiction de la progression)
def analyze_progress(user_id):
    user_data = table.get_item(Key={"user_id": user_id}).get("Item", {})
    
    model = gk.load_model("fitness_progress_model")  # Modèle IA Genkit entraîné
    prediction = model.predict({"points": user_data["points"], "workouts": user_data["workouts"]})
    
    return f"Si tu continues à ce rythme, tu atteindras ton objectif en {prediction['weeks']} semaines !"

# 🏋️ Génération d'un plan d'entraînement avec Gemini
def get_fitness_recommendation(user_id, age, weight, goal):
    prompt = f"""
    Je suis un utilisateur de {age} ans, pesant {weight} kg, et mon objectif est {goal}.
    Peux-tu me proposer un plan d'entraînement personnalisé ?
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    # Sauvegarde de la recommandation dans DynamoDB
    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET last_recommendation = :val",
        ExpressionAttributeValues={":val": response.text}
    )
    
    return response.text

# 🚀 Fonction principale : Enregistrer l'entraînement, générer un défi et analyser la progression
def process_training(user_id, training_data):
    points = save_progress(user_id, training_data)
    challenge = generate_challenge({"workouts": training_data["workouts"]})
    analysis = analyze_progress(user_id)

    return {
        "message": "Entraînement enregistré !",
        "points": points,
        "new_challenge": challenge,
        "progress_analysis": analysis
    }

# 🔥 Test
if __name__ == "__main__":
    user_id = "user_123"
    training_data = {"duration": 30, "intensity": "high", "workouts": 5}
    
    result = process_training(user_id, training_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
