from flask import Flask, jsonify, request, render_template, redirect, url_for
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

key = os.getenv('KEY')
openai.api_key = key

self_prompt = "You are a helpful assistant that provides detailed advice."

def get_response(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": self_prompt},
        {"role": "user", "content": prompt},
    ])
    return response


def get_tasks(number):
    if number < 1:
        return {}
    response = get_response("Can you give me {} tasks, ranging from small acts of kindess to self-care acts, and assign them 1 to 10 points each, where the higher the points the harder the task is or the more impact the task has. Return the result as json ONLY (and do not say anything else except the json) since I need to parse the output for use in my app, with the keys being the points, and the values being the task themselves.".format(number))
    a = response['choices'][0]['message']['content']
    return json.loads(a)

tasks = {}
#tasks = get_tasks(10)
total_point = 0

@app.route("/")
def home():
    #d = get_tasks(5)
    d = {
        '1': 'Smile at Stranger',
        '2': 'Hold the door open for someone',
        '3': 'Send a thoughtful message to a friend or family member',
        '5': 'Volunteer at a local charity',
        '10': 'Take a day off to focus on self-care'
    }
    return render_template("home.html", data = d)


