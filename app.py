from flask import Flask, render_template, request
import os
import openai

openai.api_key = os.getenv("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")
openai.Model.retrieve("text-davinchi-003")

app = Flask(__name__)
openai.Completion.create(
    model="text-davinci-003",
    prompt="Say this is a test",
    max_tokens=7,
    temperature=0
)


@app.route('/', methods='POST')
def give_answer():
    gender = request.form['gender']
    mbti = request.form['mbti']
    birth = request.form['birth']
    status_type = request.form['status_type']
    detail_type = request.form['detail_type']
    return gender + ' ' + mbti + ' ' + birth + ' ' + status_type + ' ' + detail_type
