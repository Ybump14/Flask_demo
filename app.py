import os

import requests
from flask import Flask, request, session
from flask import render_template

import controller

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

request_headers = controller.request_headers()


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginNum = request.form.get("loginNum")
        password = controller.pwd_encode(request.form.get("password"))
        url = "/api/staff/login.json"
        data = {
            "loginNum": loginNum,
            "password": password
        }
        r = requests.post(url=request_headers['url'] + url, json=data)
        res = controller.get_response(r.json())
        if r.status_code == 200:
            if res['code'] == 0:
                session['token'] = res['data']['token']
                session['staffId'] = res['data']['id']
                session['deptId'] = res['data']['departmentId']
                return render_template("index.html", msg=res['msg'], loginNum=loginNum)
            else:
                if "验证码错误" in res['msg']:
                    return render_template("login.html", msg="错误次数过多，请10分钟后再试")
                else:
                    return render_template("login.html", msg=res['msg'], loginNum=loginNum)
        else:
            return render_template("login.html", msg="无法连接到服务器")
    else:
        return render_template("login.html", msg="")


@app.route("/getWorkType", methods=['POST'])
def getWorkType():
    url = "/api/app/workType/list.json"
    data = {
        "offset": 0,
        "curStaffId": session.get('staffId'),
        "max": 9999,
        "deptId": session.get('deptId'),
        "sort": "id"
    }
    request_headers["headers"]["Authorization"] = session.get('token')
    r = requests.post(url=request_headers['url'] + url, json=data, headers=request_headers['headers'])
    res = controller.get_response(r.json())
    if r.status_code == 200:
        if res['code'] == 0:
            session['workTypes'] = res['data']['list']
            return render_template("dayreport.html", workTypes=session['workTypes'])
        else:
            return render_template("dayreport.html", msg=res['msg'])
    else:
        return render_template("dayreport.html", msg="服务器出现异常，请稍后再试")


@app.route("/report", methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        reportType = request.values.get("reportType")
        receiverIds = request.values.get("receiverIds")
        request_headers["headers"]["Authorization"] = session.get('token')
        url = "/api/app/workReport/save.json"
        data = {
            "content": content,
            "reporterId": session.get('staffId'),
            "curStaffId": session.get('staffId'),
            "receiverIds": [receiverIds],
            "images": [],
            "reportType": reportType,
            "title": title
        }
        r = requests.post(url=request_headers['url'] + url, json=data, headers=request_headers['headers'])
        res = controller.get_response(r.json())
        if r.status_code == 200:
            if res['code'] == 0:
                return render_template("report.html", msg="提交成功")
            else:
                return render_template("report.html", msg=res['msg'])
        else:
            return render_template("report.html", msg="服务器出现异常，请稍后再试")

    else:
        return render_template("report.html")


@app.route("/dayreport", methods=['GET', 'POST'])
def dayreport():
    if request.method == 'POST':
        workTypes = request.form.get("workTypes")
        content = request.form.get("content")
        receiverIds = request.values.get("receiverIds")
        request_headers["headers"]["Authorization"] = session.get('token')
        url = "/api/app/workReport/save.json"
        data = {
            "receiverIds": [receiverIds],
            "images": [],
            "content": content,
            "reporterId": session.get('staffId'),
            "workTypes": [workTypes],
            "reportType": 0,
            "curStaffId": session.get('staffId')
        }
        r = requests.post(url=request_headers["url"] + url, json=data, headers=request_headers["headers"])
        res = controller.get_response(r.json())
        if r.status_code == 200:
            if res['code'] == 0:
                return render_template("dayreport.html", msg='提交成功', workTypes=session.get('workTypes'))
            else:
                return render_template("dayreport.html", msg=res['code'], workTypes=session.get('workTypes'))
        else:
            return render_template("dayreport.html", msg="服务器出现异常，请稍后再试")
    else:
        return render_template("dayreport.html", msg='')


@app.route("/backup", methods=['GET', 'POST'])
def backup():
    return render_template("index.html")


@app.route("/getReport", methods=['GET', 'POST'])
def getReport():
    return render_template("report.html")


@app.route("/loginout", methods=['GET', 'POST'])
def loginout():
    session.clear()
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
