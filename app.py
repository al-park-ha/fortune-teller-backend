# -*- coding: utf-8 -*-

from flask import Flask, request
from waitress import serve
import openai

import config

app = Flask(__name__)
openai.organization = "org-0DYWEhC6WTA27oVGeBLqkEMX"
openai.api_key = config.openai_key


def translate_status(status_type):
    if status_type == "연애":
        return "연애 관계에서"
    elif status_type == "취업":
        return "취업과 관련해서"
    else: # 건강
        return "건강과 관련해서"


def translate_detail(status_type, detail_type):
    if status_type == "연애":
        if detail_type == "싸운":
            return "연인과 크고 작은 싸움을 하였다고 합니다."
        elif detail_type == "사귄지 얼마 안된":
            return "연인과 사귄지 얼마 안되었다고 합니다."
        elif detail_type == "짝사랑중인":
            return "한 사람을 짝사랑 중이라고 합니다."
        elif detail_type == "연애상대 찾는중인":
            return "연애 상대를 찾고 중이라고 합니다."
        elif detail_type == "복잡한":
            return "복잡한 심정이라고 합니다."
        elif detail_type == "얼마전에 헤어진":
            return "연인과 얼마 전에 헤어졌다고 합니다."
        elif detail_type == "약혼한":
            return "연인과 약혼한 사이라고 합니다."
        elif detail_type == "결혼한":
            return "연인과 결혼한 사이라고 합니다."
        else:  # 사귀는중인
            return "연인과 잘 사귀는 중이라고 합니다."
    elif status_type == "취업":
        if detail_type == "코테를 자꾸 떨어지는":
            return "기업들의 코딩 테스트에 자꾸 불합격한다고 합니다."
        elif detail_type == "서류를 자꾸 떨어지는":
            return "기업들의 서류 심사에 자꾸 불합격한다고 합니다."
        elif detail_type == "면접에서 자꾸 떨어지는":
            return "기업들의 면접 심사에서 자꾸 불합격한다고 합니다."
        elif detail_type == "지원안한":
            return "아직 아무 기업에도 지원을 안 한 상태라고 합니다."
        elif detail_type == "지원하기 싫은":
            return "힘이 들어 기업들에 지원을 하기 싫은 상태라고 합니다."
        elif detail_type == "현 직장에 불만족인":
            return "현재 직장을 다니고 있는데 불만족한다고 합니다."
        elif detail_type == "결과 기다리는":
            return "결과를 기다리는 중이라고 합니다."
        elif detail_type == "이직하고 싶은":
            return "현재 직장을 다니고 있는데 다른 기업으로 이직하고 싶다고 합니다."
        elif detail_type == "연봉이 너무 낮은":
            return "현재 직장을 다니고 있는데 연봉이 너무 낮아서 불만이라고 합니다."
        else:  # 현 상태에 만족중인
            return "현재 상태에 너무나도 만족중이라고 합니다."
    else:  # 건강
        if detail_type == "건강함":
            return "매우 건강한 상태라고 합니다."
        elif detail_type == "눈이 피로한":
            return "눈이 자주 피로하다고 합니다."
        elif detail_type == "손목이 아픈":
            return "손목이 자주 아프다고 합니다."
        elif detail_type == "허리가 아픈":
            return "허리가 자주 아프고 불편하다고 합니다."
        elif detail_type == "머리가 아픈":
            return "머리가 자주 아프고 지끈거린다고 합니다."
        elif detail_type == "소화불량인":
            return "소화가 잘 안되고 위나 장이 힘들다고 합니다."
        elif detail_type == "정신적으로 힘든":
            return "정신적으로 힘든 시기를 보내고 있다고 합니다."
        else:  # 행복한
            return "정신적으로 매우 행복한 시기를 보내고 있다고 합니다."


@app.route('/', methods=['POST'])
def give_answer():
    data = request.get_json()
    gender = data['gender']
    if gender == "선택안함":
        gender = "누군가"
    mbti = data['mbti']
    if mbti == "선택안함":
        mbti = "mbti를 모르는 상황"
    birth_year = data['birth_year']
    birth_month = data['birth_month']
    birth_day = data['birth_day']
    status_type = data['status_type']
    detail_type = data['detail_type']

    request_status_type = translate_status(status_type)
    request_detail_type = translate_detail(status_type, detail_type)

    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt="%s년 %s월 %s일에 태어난 %s인 %s가 %s %s "
               "이 %s의 별자리와 mbti를 고려하여 장점을 칭찬해주고, %s에 관련해서 따뜻한 조언을 "
               "'%s'와 '자리'라는 말 없이 200자 내로 문장이 끝나도록 해주세요. "
               % (birth_year, birth_month, birth_day, mbti, gender, request_status_type, request_detail_type, gender, status_type, mbti),
        max_tokens=700,
        temperature=0,
        n=3
    )

    sentences = completion.get('choices')[0].get('text').split('.')
    sen_len = len(sentences)
    ret = ""
    for i in range(sen_len-1):
        ret += sentences[i]

    return ret


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
