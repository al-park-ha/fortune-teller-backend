from flask import Flask, render_template, request, json, jsonify, Response
import json
import os
import openai
from waitress import serve

app = Flask(__name__)
openai.organization = "org-0DYWEhC6WTA27oVGeBLqkEMX"
openai.api_key = "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"
openai.Model.list()


# openai.Model.retrieve("text-davinchi-003")
# openai.Completion.create(
#     model="text-davinci-003",
#     prompt="Say this is a test",
#     max_tokens=7,
#     temperature=0
# )


@app.route('/test', methods=['POST'])
def give_answer():
    data = request.get_json()
    gender = data['gender']
    mbti = data['mbti']
    birth_year = data['birth_year']
    birth_month = data['birth_month']
    birth_day = data['birth_day']
    status_type = data['status_type']
    detail_type = data['detail_type']
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt="%s년 %s월 %s일에 태어난 %s %s가 취업 준비 중 코딩 테스트에서 계속 떨어집니다. "
               "이 %s의 별자리와 mbti를 고려하여 장점을 칭찬해주고, 취업과 관련해서 따뜻한 조언을 "
               "'별자리'라는 말 없이 200자 내로 문장이 완성되도록 해주세요. " % (birth_year, birth_month, birth_day, mbti, gender, gender),
        max_tokens=700,
        temperature=0
    )
    # return completion.get('choices')[0].get('text')
    return completion


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
