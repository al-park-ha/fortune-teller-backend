from flask import Flask, render_template, request
import os
import openai

openai.api_key = os.getenv("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")
openai.Model.retrieve("text-davinchi-003")

app = Flask(__name__)


@app.route('/', methods='POST')
def give_answer():
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt="Say this is a test",
        max_tokens=7,
        temperature=0
    )
    return completion
