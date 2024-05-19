import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key_path=("/home/flask/openai_api_key")

#SAQ Grader
@app.route("/saq", methods =("GET", "POST"))
def gradeSAQ():
    if request.method == "POST":
        prompt = request.form["PROMPT"]
        responseToPrompt = request.form["RESPONSE"]
        gptResponse = openai.ChatCompletion.create(
            model = "ft:gpt-3.5-turbo-0613:personal::8Ar7ZOuA",
            messages =[
                {"role": "system", "content": "You are an AI assistant that grades student responses. The student will give you the prompt that they responded to, and their response. Grade their response according to this rubric: Criterion A) 0-1 points (or NR): A response that earns 0 points is one that does not give an answer relevant to the prompt and/or one that does not give any true and correct evidence, ie. an example about why their claim is correct. A response that earns 1 point is one that gives an answer relevant to the prompt that also uses at least one piece of evidence about a real-world thing that happened relating to the prompt and could but doesn't have to give some reasoning as to why it is correct. A response that earns the score NR is one that is empty."},
                {"role": "user", "content": "The prompt is: " + prompt + ". The student response is: " + responseToPrompt}]
)
        resp = gptResponse.choices[0].message

        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt="Give me a sample AP Short Answer Question response, a maximum of four sentences, that would earn 1/1 point that answers all parts of the following prompt: " + prompt,
            temperature=0.6,
            max_tokens=1500  # Adjust the max tokens as needed
        )
        has_sample = response.choices[0].text

        return render_template("saq.html", resp=resp, has_sample=has_sample)
    return render_template("saq.html", resp = None)

#SAQ question generation
@app.route("/e", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # Handle POST request
        animal = request.form["animal"]
        quiz_questions = generate_quiz_questions(animal) # generating quiz questions through other methods
        return render_template("index.html", quiz_questions=quiz_questions)

    # Handle GET request (this part is missing in your code)
    return render_template("index.html", quiz_questions=None)

#generating prompt for SAQ generator
def generate_prompt(animal):
        return f"""
Suggest three AP style short answer free response questions that have to do with {animal.capitalize()}.
Format your response as follows. Be sure to include the AP Syntax (Either "Identify ONE..." or "Explain ONE...")
1. Question 1:
2. Question 2:
3. Question 3:"""


# display ads.txt for google adsense crawler
@app.route("/ads.txt")
def adstxt():
    return render_template("ads.txt")

# generating actual questions for SAQ generator
def generate_quiz_questions(x):
    prompt = generate_prompt(x)
    
    # Make the API call with the prompt
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.6,
        max_tokens=150  # Adjust the max tokens as needed
    )
    
    # Extract and return the generated quiz questions
    quiz_questions = response.choices[0].text
    return quiz_questions

#navigation page
@app.route("/")
def functione():
    return render_template("i.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
