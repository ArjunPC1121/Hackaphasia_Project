from flask import Flask,jsonify, render_template, Response, url_for,request
import pandas as pd
from sklearn.calibration import LabelEncoder
from utilities.quiz import recommend_by_difficulty
from utilities.scholarship import train,scholarship
from utilities.translator import translate_and_speak
from utilities.bot import start_gui
import threading
import time
import requests
import joblib
app = Flask(__name__)

api_url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"

# Global variable to store the latest fact
latest_fact = "Fetching the first fact..."

def fetch_fact():
    """
    Periodically fetch jokes or facts from the API and update the global variable.
    """
    global latest_fact
    while True:
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            latest_fact = data.get('joke', "Could not retrieve a fact.")
        except requests.RequestException as e:
            latest_fact = f"Error retrieving fact: {e}"
        time.sleep(60)  # Wait 60 seconds before fetching the next fact

# Start the background thread
def start_background_thread():
    thread = threading.Thread(target=fetch_fact, daemon=True)
    thread.start()


@app.route("/fact")
def get_fact():
    """
    API endpoint to get the latest fact.
    """
    return jsonify({"fact": latest_fact})

dataset = pd.read_csv("categorized_courses.csv")
dataset.drop_duplicates(inplace=True)
dataset['course_difficulty'] = dataset['course_difficulty'].fillna('Beginner')  # Default to Beginner
dataset['course_difficulty'] = dataset['course_difficulty'].str.capitalize()

careerdf=pd.read_csv("Expanded_Career_Counselling.csv")

def run_tkinter_gui():
    start_gui()

tkinter_thread = threading.Thread(target=run_tkinter_gui, daemon=True)


@app.route("/")
@app.route("/home")
def home():
    tkinter_thread.start()
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/quizzes")
def quiz():
    recommended_courses = recommend_by_difficulty(dataset, 'Beginner')
    print(recommended_courses.to_dict(orient='records'))  # Debugging step
    return render_template("quiz.html", recommended_courses=recommended_courses.to_dict(orient='records'))

@app.route("/options")
def options():
    return render_template("options.html")

@app.route("/translate", methods=["GET", "POST"])
def translate_page():
    if request.method == "GET":
        return render_template("translator.html")
    elif request.method == "POST":
        data = request.get_json()
        text = data.get('text')
        language = data.get('language')

        # Call the translation function
        translated_text = translate_and_speak(text, language)

        # Return the translated text as JSON
        return jsonify({'translated_text': translated_text})
    
@app.route("/courses")
def courses():
    
    return render_template("courses.html")

@app.route("/gtBeg",methods=['GET'])
def gtBeg():
  
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    if not category or not difficulty:
        return "Missing parameters", 400

    course_recomm = recommend_by_difficulty(dataset, difficulty, category)
    return render_template("course_recomm.html", course_recomm=course_recomm)


@app.route("/scholarship")
def scholarship_page():
    return render_template("scholarship.html")

@app.route("/eligibility",methods=['POST'])
def eligibility():
    cgpa=request.form.get("cgpa")
    income=request.form.get("income")
    citizen=request.form.get("citizen")
    degree=request.form.get("degree")
    arg_list=train()
    res=scholarship(arg_list[0],arg_list[1],arg_list[2],cgpa,income,citizen,degree)
    return render_template("eligibility.html",res=res)

model = joblib.load('career_counseling_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')
train_encoder= joblib.load('target_encoder.pkl')
@app.route("/fillCounselForm")
def fillCounselForm():
    return render_template("careerCounsel.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form data
        input_data = request.form.to_dict()

        # Prepare the data for prediction
        features = pd.DataFrame([input_data])  # Convert input to DataFrame

        # Encode categorical data
        for column, encoder in label_encoders.items():
            if column in features.columns:
                features[column] = encoder.transform(features[column])

        # Predict the next step
        prediction = model.predict(features)

        # Decode the prediction to the original label
        decoded_prediction = train_encoder.inverse_transform(prediction)

        # Return the result
        return f"<h3>Recommended Next Step: {decoded_prediction[0]}</h3>"

    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"
    

if __name__ == "__main__":
    app.run(debug=True)
