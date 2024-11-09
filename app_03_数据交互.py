import pymysql
from flask import Flask, request

app = Flask(__name__)


def db_exectuor():
    return pymysql.connect(host='1.94.147.176',
                           user='root',
                           password='kjiolluy711',
                           db='shop',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/users')
def show_users():
    connection = db_exectuor()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tbl_user")
        result = cursor.fetchall()
    return result


@app.route('/users/<int:user_id>')
def show_user_by_id(user_id):
    connection = db_exectuor()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tbl_user WHERE user_id = %s", [user_id])
        result = cursor.fetchone()
    return result


# @app.route('/update_user/<int:id>', methods=['GET','POST'])
# def update_user(id):
#     username = request.form['username']
#     email = request.form['email']
#     connection = db_exectuor()
#     with connection.cursor() as cursor:
#         sql = "UPDATE tbl_user SET user_name=%s, user_age=%s, user_gender=%s WHERE id=%s"
#         cursor.execute(sql, (username, email, id))
#     connection.commit()
#     return 'User updated successfully'
#     # return redirect(url_for('show_users'))


@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    connection = db_exectuor()
    with connection.cursor() as cursor:
        sql = "DELETE FROM tbl_user WHERE user_id=%s"
        cursor.execute(sql, (id,))
    connection.commit()
    return 'User deleted successfully'
    # return redirect(url_for('show_users'))


if __name__ == '__main__':
    app.run(debug=True)
