from flask import Flask, jsonify, request, render_template, redirect, url_for
import openai

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
