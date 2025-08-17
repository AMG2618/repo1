from datetime import datetime

from flask import Flask, session
from flask import url_for
from flask import request
from werkzeug.utils import redirect
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = 'atasamente'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    # import os
    # assert os.path.exists("cert.pem"), "cert.pem nu există!"
    # assert os.path.exists("key.pem"), "key.pem nu există!"
    #app.run(ssl_context=('cert.pem', 'key.pem'))
    pass

from project_p1.fisiere import fisiere
app.register_blueprint(fisiere)

@app.route('/')
def homepage():
    login = url_for("login")
    inregistrare = url_for("inregistrare")
    return render_template('homepage.html', login = login, inregistrare = inregistrare)

@app.route('/user/<int:id>')
def profile(id):
    incarca = url_for("fisiere.incarcare", id_medic=id)
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, user, parola, nume, prenume, colegiu FROM medici where id = '{id}'")
    rows = cursor.fetchall()
    out = 0
    for row in rows:
        print(row)
        out = row
        id, user, parola, nume, prenume, colegiu = row
    print(f'profile out id={id}')
    print(f'profile out user={user}')
    edit = url_for("edit_user", id=id)
    viza = url_for("cerere_viza", id_medic=id)
    logout = url_for("logout")
    fisiere_medic = url_for("fisiere.afiseaza_documente_medic", id_medic=id)
    return render_template('user/show.html', id=id, user=user, nume=nume, prenume=prenume, colegiu=colegiu, edit=edit, incarca = incarca, logout=logout, viza=viza, fisiere_medic=fisiere_medic)

def getuserid(user):
    connection = sqlite3.connect('medici.db')
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
    connection = sqlite3.connect('medici.db')
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

@app.route('/logout')
def logout():
    # logout user
    session.pop('username', None)
    return redirect(url_for('homepage'))

@app.route('/inregistrare', methods=['POST', 'GET'])
def inregistrare():
    error = None
    if request.method == 'POST':
        user = request.form['user']
        parola = request.form['parola']
        nume = request.form['nume']
        prenume = request.form['prenume']
        colegiu = request.form['colegiu']
        connection = sqlite3.connect('medici.db')
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
        cursor.execute(f"SELECT id FROM medici where user = '{user}'")
        connection.commit()
        rows = cursor.fetchall()
        out=0
        for row in rows:
            print(row)
            out = int(row[0])
        id = out
        connection.commit()
        rows = cursor.fetchall()
        print(rows)
        connection.close()
        # return redirect(url_for('profile', id=id))
        return redirect(url_for('login'))
    return render_template('user/inregistrare.html', error=error)

from flask import render_template

@app.route('/admin/listusers') # pentru admin
def listusers():
    connection = sqlite3.connect('medici.db')
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
    url_admin = url_for('admin')
    return render_template('user/list.html', users = users, url_admin=url_admin)

@app.route('/admin/user/<int:id>/delete') # pentru admin
def delete_user(id):
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM medici where id = '{id}'")
    connection.commit()
    rows = cursor.fetchall()
    connection.close()
    return redirect(url_for('listusers'))

@app.route('/admin/user/<int:id>/edit')
def edit_user(id):
    connection = sqlite3.connect('medici.db')
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

@app.route('/update_user', methods=['POST'])
def update_user():
    id = request.form['id']
    user = request.form['user']
    parola = request.form['parola']
    nume = request.form['nume']
    prenume = request.form['prenume']
    colegiu = request.form['colegiu']
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE medici SET user = ?, parola = ?, nume = ?, prenume = ?, colegiu = ?   WHERE id = ?", (user, parola, nume, prenume, colegiu, id))
    connection.commit()
    connection.close()

    return redirect(url_for('profile', id=id))

@app.route('/viza/<int:id_medic>')
def cerere_viza(id_medic):
    today = datetime.today().strftime('%Y-%m-%d')
    print("Today's date:", today)
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    sql_script = f"""SELECT id, id_medic, nume, continut, tip, emc, data FROM fisiere WHERE id_medic={id_medic} and tip="diploma_emc" and data >= DATE('now', '-366 days') and id_cerere_viza = 0"""
    cursor.execute(sql_script)
    connection.commit()
    rows = cursor.fetchall()
    fisiere = []
    total_emc=0
    for row in rows:
        print(row)
        out = row
        fisiere.append(row)
        id, id_medic, nume, continut, tip, emc, data = row
        total_emc=total_emc+int(emc)
    # print(f'profile out id={id}')
    print(f'profile out id_medic={id_medic}')
    connection.close()
    viza = url_for("trimitecerereviza", id_medic=id_medic)
    logout = url_for("logout")
    incarcare = url_for("fisiere.incarcare", id_medic=id_medic)
    pagina_medic = url_for("profile", id=id_medic)
    return render_template('user/viza.html', fisiere=fisiere, total_emc=total_emc, incarcare=incarcare, viza=viza, pagina_medic=pagina_medic)

@app.route('/trimitecerereviza/<int:id_medic>')
def trimitecerereviza(id_medic):
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    sql_script = f"""SELECT id, id_medic, nume, continut, tip, emc, data, id_cerere_viza FROM fisiere WHERE id_medic={id_medic} and tip="diploma_emc" and data >= DATE('now', '-366 days') and id_cerere_viza = 0"""
    cursor.execute(sql_script)
    connection.commit()
    rows = cursor.fetchall()
    fisiere = []
    total_emc = 0
    for row in rows:
        print(row)
        out = row
        fisiere.append(row)
        id, id_medic, nume, continut, tip, emc, data, id_cerere_viza = row
        total_emc = total_emc + int(emc)
    if total_emc < 48:
        return render_template('user/viza.html', fisiere=fisiere, total_emc=total_emc, error="Nu aveti suficiente puncte EMC! Limita este 48 de puncte EMC pentru a putea solicita viza de libera practica.")
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    sql_script = f"""INSERT INTO cerere_viza (id_medic, data) VALUES ({id_medic}, DATE('now'))"""
    cursor.execute(sql_script)
    connection.commit()
    id_cerere_viza = cursor.lastrowid
    connection.close()
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    # sql_script = f"""UPDATE fisiere WHERE id_medic={id_medic} and tip="diploma_emc" and data >= DATE('now', '-366 days') and id_cerere_viza= 0 SET id_cerere_viza = {id_cerere_viza}"""
    sql_script = f"""UPDATE fisiere SET id_cerere_viza = {id_cerere_viza} WHERE id_medic={id_medic} and tip="diploma_emc" and data >= DATE('now', '-366 days') and id_cerere_viza = 0"""
    cursor.execute(sql_script)
    connection.commit()
    connection.close()
    return render_template('user/trimitecerereviza.html', id_medic=id_medic, id_cerere_viza=id_cerere_viza)

@app.route('/cerere_viza/<int:id_medic>', methods=['POST'])
def cerere_viza_post(id_medic):
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    sql_script = f"""INSERT INTO cerere_viza (id_medic, data) VALUES ({id_medic}, DATE('now'))"""
    cursor.execute(sql_script)
    connection.commit()
    connection.close()
    return redirect(url_for('cerere_viza', id_medic=id_medic))
# creaza formularul de cerere viza si scade numarul de EMC-uri
@app.route('/cerere_viza')
def cerere_viza_get():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = session['username']
    id_medic = getuserid(user)
    if id_medic == 0:
        return redirect(url_for('login'))
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    sql_script = f"""SELECT id, id_medic, nume, continut, tip, emc, data, id_cerere_viza FROM fisiere WHERE id_medic={id_medic} and tip="diploma_emc" and data >= DATE('now', '-366 days') and id_cerere_viza = 0"""
    cursor.execute(sql_script)
    connection.commit()
    rows = cursor.fetchall()
    fisiere = []
    total_emc = 0
    for row in rows:
        print(row)
        out = row
        fisiere.append(row)
        id, id_medic, nume, continut, tip, emc, data = row
        total_emc = total_emc + int(emc)
    # print(f'profile out id={id}')
    print(f'profile out id_medic={id_medic}')
    connection.close()
    viza = url_for("trimitecerereviza", id_medic=id_medic)
    logout = url_for("logout")
    incarcare = url_for("fisiere.incarcare", id_medic=id_medic)
    pagina_medic = url_for("profile", id=id_medic)
    return render_template('user/viza.html', fisiere=fisiere, total_emc=total_emc, incarcare=incarcare, viza=viza, pagina_medic=pagina_medic)

#afiseaza toate cererile de viza pentru administrator
@app.route('/admin/cereri_viza')
def cereri_viza():
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    sql_script = f"""SELECT id, id_medic, data FROM cerere_viza"""
    cursor.execute(sql_script)
    connection.commit()
    rows = cursor.fetchall()
    cereri = []
    for row in rows:
        print(row)
        out = row
        cereri.append(row)
        id, id_medic, data = row
    # print(f'profile out id={id}')
    print(f'cereri_viza out id_medic={id_medic}')
    connection.close()
    for cerere in cereri:
        print(f'Cerere ID: {cerere[0]}, Medic ID: {cerere[1]}, Data: {cerere[2]}')
    return render_template('admin/cereri_viza.html', cereri=cereri)

# pagina logare administrator
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    eroare = None
    if request.method == 'POST':
        user = request.form['username']
        parola = request.form['password']
        if user == 'admin' and parola == 'admin':
            url_listusers = url_for('listusers')
            url_fisiere = url_for("fisiere.afiseaza_documente")
            url_cereri_viza = url_for("cereri_viza")
            return render_template('admin/admin.html', error=eroare, url_listusers=url_listusers, url_fisiere=url_fisiere, url_cereri_viza=url_cereri_viza)
        else:
            eroare = 'User sau parola incorecte!'
    return render_template('admin/login.html', error=eroare)

# @app.route('/admin')
# def admin_home():
#     if 'username' not in session:
#         return redirect(url_for('admin_login'))
#     user = session['username']
#     if user != 'admin':
#         return redirect(url_for('admin_login'))
#     return render_template('admin/home.html')





# if __name__ == '__main__':
#     cerere_viza()
#     app.run(ssl_context=('cert.pem', 'key.pem'), host='localhost', port=4443, debug=True)
