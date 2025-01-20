import threading
import time
import zipfile
from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash, send_from_directory, send_file

app = Flask(__name__)
app.secret_key = "123456"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

import os

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # 确保上传目录存在


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return f"登录用户名是：{username}<br><b><a href='/logout'>点击这里注销</a></b><br><b><a href='/main'>进入主页</a></b>"
    else:
        return "您暂未登录，<br><a href='/login'><b>点击这里登录</b></a>"


@app.route('/main')
def main():
    if 'username' in session:
        username = session['username']
        # 获取上传文件夹的绝对路径
        upload_folder_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        files = os.listdir(upload_folder_path) if os.path.exists(upload_folder_path) else []
        return render_template('main.html', username=username, files=files)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '123':
            session['username'] = username
            session['password'] = password
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误，请重新输入。')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/result/', methods=['POST', 'GET'])
def result():
    if request.method == 'GET':
        return redirect(url_for('error', message='请求格式错误！'))
    elif request.method == 'POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('success', message='登录成功！'))
        return redirect(url_for('error', message='用户名或密码错误！'))


@app.route('/error/')
def error():
    message = request.args.get('message', '发生错误')
    return render_template('error.html', message=message)


@app.route('/test/error/')
def test_error():
    return redirect(url_for('error', message="自定义异常信息！"))


@app.route('/success/')
def success():
    message = request.args.get('message', '操作成功')
    return render_template('success.html', message=message)


@app.route('/test/success/')
def test_success():
    return redirect(url_for('success', message="自定义成功信息！"))


@app.route("/set")
def set_cookie():
    resp = make_response(render_template('success.html'))
    resp.set_cookie("aaa_key", "aaa_value", max_age=3600)
    return resp


@app.route("/get")
def get_cookie():
    return request.cookies.get("aaa_key")


@app.route("/delete")
def delete_cookie():
    resp = make_response(render_template('success.html'))
    resp.delete_cookie("aaa_key")
    return resp


# 提取文件验证和重命名功能
def process_file(f):
    if not f:
        return None, "没有上传的文件"

    filename, ext = os.path.splitext(f.filename)

    # 检查文件名部分是否为空
    if not filename:
        return None, "文件名无效：文件名前不能是空的"

    # 用当前日期和时间重命名文件
    new_filename = filename + datetime.now().strftime('%Y%m%d_%H%M%S') + ext
    return new_filename, None  # 返回重命名后的文件名


# 定义文件上传路由
@app.route('/uploader', methods=['POST'])
def uploader():
    files = request.files.getlist('upload_files')

    if not files:
        flash('没有上传的文件')
        return redirect(url_for('error', message='没有上传的文件'))

    successful_files = []
    failed_files = []

    # 处理每个上传的文件
    for f in files:
        new_filename, error_message = process_file(f)
        if error_message:
            failed_files.append((f.filename, error_message))
        else:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            successful_files.append(new_filename)

    # 提供上传结果反馈
    if successful_files:
        flash(f'文件上传成功：{", ".join(successful_files)}')
    if failed_files:
        flash(f'上传失败的文件：{", ".join([f"{filename} ({msg})" for filename, msg in failed_files])}')

    return redirect(url_for('main'))


# 定义文件下载路由
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# 定义文件删除路由
@app.route('/delete/<filename>', methods=['POST', 'GET'])
def delete_file(filename):
    upload_folder_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    file_path = os.path.join(upload_folder_path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'{filename} 删除成功！')
    else:
        flash(f'文件 {filename} 不存在或已被删除！')
    return redirect(url_for('main'))

# 删除临时ZIP文件的后台任务
def delete_zip_file(zip_path):
    try:
        time.sleep(2)  # 给文件传输足够时间
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print(f"临时ZIP文件 {zip_path} 已删除")
    except Exception as e:
        print(f"删除ZIP文件失败: {str(e)}")


# 定义文件的批量操作
@app.route('/batch_action', methods=['POST'])
def batch_action():
    selected_files = request.form.getlist('selected_files')
    action = request.form.get('action')
    upload_folder_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])

    if not selected_files:
        flash("未选择任何文件")
        return redirect(url_for('main'))

    if action == 'delete':
        for filename in selected_files:
            file_path = os.path.join(upload_folder_path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        flash("文件已删除")
        return redirect(url_for('main'))

    elif action == 'download':
        if len(selected_files) == 1:
            # 单个文件，直接下载
            return send_from_directory(app.config['UPLOAD_FOLDER'], selected_files[0], as_attachment=True)
        else:
            # 多个文件，打包成ZIP下载
            zip_filename = datetime.now().strftime('%Y%m%d_%H%M%S') + ".zip"
            zip_path = os.path.join(upload_folder_path, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for filename in selected_files:
                    file_path = os.path.join(upload_folder_path, filename)
                    if os.path.exists(file_path):
                        zipf.write(file_path, filename)

            try:
                # 发送打包的ZIP文件
                response = send_file(zip_path, as_attachment=True)

                # 在后台异步删除ZIP文件
                threading.Thread(target=delete_zip_file, args=(zip_path,)).start()

                return response

            except Exception as e:
                # 错误处理
                flash(f"文件操作失败: {str(e)}")
                return redirect(url_for('main'))

    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
