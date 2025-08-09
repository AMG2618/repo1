from flask import Flask
from flask import url_for
from flask import request
from werkzeug.utils import redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def homepage():
    login = url_for("login")
    inregistrare = url_for("inregistrare")
    return render_template('homepage.html', login = login, inregistrare = inregistrare)
#
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return f'Post {post_id}'
#
# @app.route('/projects/')
# def projects():
#     return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/user/<int:id>')
def profile(id):
    connection = sqlite3.connect('BD/medici.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM medici where id = '{id}'")
    rows = cursor.fetchall()
    out = 0
    for row in rows:
        print(row)
        out = row
        id, user, parola, nume, prenume, colegiu = row
    edit = url_for("edit_user", id=id)
    return render_template('user/show.html', id=id, user=user, nume=nume, prenume=prenume, colegiu=colegiu, edit=edit )

def getuserid(user):
    connection = sqlite3.connect('BD/medici.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM medici where user = '{user}'")
    rows = cursor.fetchall()
    out = 0
    for row in rows:
        print(row)
        out = int(row[0])
    connection.close()
    return out

def valid_login(user, password):
    connection = sqlite3.connect('BD/medici.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM medici where user = '{user}' and parola = '{password}'")
    rows = cursor.fetchall()
    out = 0
    for row in rows:
        print(row)
        out = int(row[0])
    connection.close()
    return out

def log_the_user_in(id):
    return redirect(url_for('profile', id=id))

@app.route('/login', methods=['POST', 'GET'])
def login():
    eroare = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            id=getuserid(request.form['username'])
            return log_the_user_in(id)
        else:
            eroare = 'User sau parola incorecte!'
    return render_template('login.html', error=eroare)

@app.route('/inregistrare', methods=['POST', 'GET'])
def inregistrare():
    error = None
    if request.method == 'POST':
        user = request.form['user']
        parola = request.form['parola']
        nume = request.form['nume']
        prenume = request.form['prenume']
        colegiu = request.form['colegiu']
        connection = sqlite3.connect('BD/medici.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM medici where user = '{user}'")
        rows = cursor.fetchall()
        out=0
        for row in rows:
            print(row)
            out = int(row[0])
        # connection.close()
        if out > 0:
            return render_template('user/inregistrare.html', error= 'Utilizatorul exista deja in baza de date')

        sql_script = f"""
               INSERT INTO medici (user, parola, nume, prenume, colegiu) 
               VALUES ("{user}", "{parola}", "{nume}", "{prenume}", "{colegiu}")"""
        cursor.execute(sql_script)
        connection.commit()
        rows = cursor.fetchall()
        connection.close()
        return redirect(url_for('profile', id=id))
    return render_template('user/inregistrare.html', error=error)

from flask import render_template

@app.route('/admin/listusers')
def listusers():
    connection = sqlite3.connect('BD/medici.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medici")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append(row)
        print(row)
        id = row[0]
    print (str(users))
    connection.close()
    return render_template('user/list.html', users = users)

@app.route('/admin/user/<int:id>/delete')
def delete_user(id):
    connection = sqlite3.connect('BD/medici.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM medici where id = '{id}'")
    connection.commit()
    rows = cursor.fetchall()
    connection.close()
    return redirect(url_for('listusers'))

@app.route('/admin/user/<int:id>/edit')
def edit_user(id):
    connection = sqlite3.connect('BD/medici.db')
    cursor = connection.cursor()
    sql_script = f"SELECT * FROM medici WHERE id = {id}"
    cursor.execute(sql_script)
    connection.commit()
    rows = cursor.fetchall()
    connection.close()
    out = 0
    for row in rows:
        print(row)
        out = row
        id, user, parola, nume, prenume, colegiu = row
    return render_template('user/edit.html', user=out)
    # return render_template('user/show.html', id=id, user=user, nume=nume, prenume=prenume, colegiu=colegiu )

@app.route('/update_user', methods=['POST'])
def update_user():
    id = request.form['id']
    user = request.form['user']
    parola = request.form['parola']
    nume = request.form['nume']
    prenume = request.form['prenume']
    colegiu = request.form['colegiu']
    connection = sqlite3.connect('BD/medici.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE medici SET user = ?, parola = ?, nume = ?, prenume = ?, colegiu = ?   WHERE id = ?", (user, parola, nume, prenume, colegiu, id))
    connection.commit()
    connection.close()

    return redirect(url_for('profile', id=id))

if __name__ == '__main__':
    app.run(debug=True)