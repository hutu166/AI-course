from flask import Flask, request, render_template, jsonify, redirect, Blueprint, session

import os
from .db import db
from chat import views as chatViews, util


# 蓝图，下面注解本来是@app.route("/") 都要改成@views.route
system_bp = Blueprint('system', __name__)
# system_bp = Blueprint('system', __name__, template_folder='templates', static_folder='static')


def to_user_json(user):
    return {
        "id": user[0],
        "email": user[1],
        "firstName": user[3],
        "lastName": user[4],
        "role": user[5]
    }

@system_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']  # 获取上传的文件

    print(os.path.join(os.path.dirname(__file__), '../static', file.filename))
    file.save(os.path.join(os.path.dirname(__file__), '../static', file.filename))  # static是默认的静态资源目录
    return util.success(file.filename)

@system_bp.route("/login", methods=['POST'])
def login_method():
    session['chat_history'] = []
    email = request.json.get('email')
    password = request.json.get('password')
    role = request.json.get('role')
    results = db.fetchall('SELECT * FROM sys_user where email = ? and password = ? and role=?', (email, password,role,))
    if len(results) == 0:
        return util.error()
    else:
        return util.success(to_user_json(results[0]))

@system_bp.route("/register", methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')
    role = request.json.get('role')

    results = db.fetchall('SELECT * FROM sys_user where email = ?', (email,))
    if len(results) > 0:
        return error('Email already exists')

    db.execute('INSERT INTO sys_user (email, password, first_name, last_name,role) VALUES (?,?,?,?,?)',
                          (email, password, firstName, lastName,role))
    return util.success()

@system_bp.route("/courses", methods=['GET'])
def courses():
    userId = request.args.get('userId')
    query_complete = request.args.get('query_complete')

    complete_course_map = {} # course_id -> complete_state
    if userId is not None:
        complete_course = db.fetchall('SELECT * FROM course_completion where user_id = ?', (userId,))
        for row in complete_course:
            course_id = row[2]
            complete_course_map[course_id] = row

    results = db.fetchall('SELECT * FROM course')
    course_list = []
    for row in results:
        is_complete = 'N'
        code = ''
        recommend = ''
        completion_data = complete_course_map.get(str(row[0]))
        if completion_data is not None:
            code = completion_data[3]
            recommend = completion_data[4]
            is_complete = completion_data[5]

        course_list.append({
            "id": row[0],
            "name": row[1],
            "lecture_md": util.md_to_html(row[3]),
            "task_desc": util.md_to_html(row[4]),
            "dataset_file": row[5],
            "is_complete": is_complete,
            "code": code,
            "recommend": util.md_to_html(recommend)
        })
    return util.success(course_list)


@system_bp.route("/removeCourse", methods=['DELETE'])
def removeCourse():
    id = request.json.get('id')
    db.execute('delete from course where id=?', (id,))
    return util.success()


@system_bp.route("/complete", methods=['POST'])
def complete_progress():
    courseId = request.json.get('courseId')
    db.execute("update course_completion set state='Y' where course_id=?", (courseId,))
    return util.success()


@system_bp.route("/course/progress", methods=['GET'])
def course_progress():
    complete_list = db.fetchall("""select a.name,b.recommend from 
course a join course_completion b
on a.id=b.course_id""")
    total_num = db.fetchone("select count(*) from course")
    progress = complete_list / total_num
    print(progress)
    return util.success(progress)
