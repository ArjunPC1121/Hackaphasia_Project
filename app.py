from flask import Flask,jsonify, render_template, Response, url_for,request
import pandas as pd
from utilities.quiz import recommend_by_difficulty
from utilities.scholarship import train,scholarship
from utilities.translator import translate_and_speak
app = Flask(__name__)

data = pd.read_csv("coursea_data.csv")
data.drop_duplicates(inplace=True)
data['course_difficulty'] = data['course_difficulty'].fillna('Beginner')  # Default to Beginner
data['course_difficulty'] = data['course_difficulty'].str.capitalize()

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/quizzes")
def quiz():
    recommended_courses = recommend_by_difficulty(data, 'Beginner')
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
    #print("Courses")
    return "Courses Page"

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

if __name__ == "__main__":
    app.run(debug=True)
