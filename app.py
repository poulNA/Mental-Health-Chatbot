from flask import Flask, jsonify, request, render_template, redirect, url_for
import matplotlib.pyplot as plt
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

completed = {}
tasks = {}
daily_points = { 'Sunday': 0, 'Monday': 0, 'Tuesday': 10, 'Wednesday': 5, 'Thursday': 7, 'Friday': 1, 'Saturday': 2 }

tasks = get_tasks(10)


@app.route("/<task_desc>")
def complete_tasks(task_desc): # pass in by task description from front end
        keys_to_delete = [(key, value) for key, value in tasks.items() if value == task_desc]

        # Delete the items based on the keys in the list
        for (key, value) in keys_to_delete:
            completed[key] = value
            del tasks[key]
        return render_template("home.html", data = tasks, points = get_points())

def graph(daily_points):
    days = list(daily_points.keys())
    points = list(daily_points.values())
    plt.plot(days, points, label='Points', color='blue', marker='o')

    # Add labels and a legend
    plt.xlabel('Weekly')
    plt.ylabel('Points')
    plt.title('Scatter Plot of Points')
    plt.legend()

    # Save the plot
    plt.savefig('plots/plot.png')
    # Show the plot
    # plt.show()

def get_points():
    p = 0
    for key in completed.keys():
        p += int(key)
    return p

@app.route("/")
def home():
    return render_template("home.html", data = tasks, points = get_points())
