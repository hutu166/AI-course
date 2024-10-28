from flask import Flask, request, render_template, jsonify, redirect,Blueprint,session
from . import gpt4_client
from .util import success, error,parse_csv_dataset
from system.db import db
import os
import shutil
import subprocess

# 蓝图，下面注解本来是@app.route("/") 都要改成@views.route
chat_bp = Blueprint('chat', __name__)

def chat_result(messages):

    answer = response.choices[0].message.content.strip()
    return answer


@chat_bp.route("/addCourse", methods=['POST'])
def addCourse():
    name = request.json.get('name')
    outline = request.json.get('outline')

    lectureResult = get_gpt4_answer(outline + ".Based on the previous outline, generate a course introduction for me.")
    taskDesc = get_gpt4_answer(outline + ".Based to the previous outline, generate a study assignment and Sample Dataset  for me after class.")
    taskResult, dataset, csv_filename = parse_csv_dataset(taskDesc)
    with open(csv_filename, 'w', encoding='utf-8') as f:
        f.write(dataset)

    db.execute('INSERT INTO course (name, outline, lecture_pdf, task_desc, dataset_file) VALUES (?,?,?,?,?)',
               (name, outline, lectureResult, taskResult, csv_filename))
    return success()


@chat_bp.route("/completion", methods=['POST'])
def chat_completion():
    type = request.json.get('type')
    inquiry = request.json.get('inquiry')
    courseId = request.json.get('courseId')
    user_id = request.json.get('user_id')

    print("chat completion...")

    content = ''
    if type == 0:
        content = inquiry
    else:
        result = db.fetchone('select * from course where id = ?', (courseId,))
        lecture_pdf = result[3]
        task_desc = result[4]
        dataset = result[5]
        if type == '1':
            content = f'({lecture_pdf}), Summarize the previous content'
        elif type == '2':
            content = f'({lecture_pdf}), Create a study plan based on the previous content'
        elif type == '3':
            r = db.fetchone('select * from course_completion where user_id = ? and course_id = ?', (user_id, courseId,))
            code = r[3]
            content = 'Analyzing the code: ('+code+')'

    return jsonify({
        "answer": get_gpt4_answer(content)
    })

@chat_bp.route("/runcode", methods=['POST'])
def runcode():
    userId = request.json.get('userId')
    courseId = request.json.get('courseId')
    code = request.json.get('code')
    py_file = f'./static/code-{userId}-{courseId}.py'

    with open(py_file, 'w', encoding='utf-8') as f:
        f.write('# coding=utf-8\n')
        f.write(code)

    recommend = get_gpt4_answer(f'"{code}" Give me some advice on the recommend about this python code.')
    db.execute("delete from course_completion where user_id=? and course_id=?", (userId, courseId))
    db.execute("insert into course_completion (user_id, course_id, code, recommend) values (?,?,?,?)",
               (userId, courseId, code, recommend))

    # run python code
    result = subprocess.run(['python', py_file], capture_output=True, text=True, encoding='utf-8')
    if result.returncode == 0:
        return success(result.stdout)
    else:  # error
        return error(result.stderr)

def get_gpt4_answer(content):
    print("Getting GPT-4 answer...")
    completion = gpt4_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": content
            }
        ]
    )
    print(completion)
    return completion.choices[0].message.content

