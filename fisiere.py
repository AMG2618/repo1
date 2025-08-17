import io
from datetime import datetime

from flask import Blueprint, render_template, flash, request, current_app, send_file
import sqlite3, os
from werkzeug.utils import redirect, secure_filename
from flask import url_for



fisiere = Blueprint('fisiere',__name__)

class Fisier():
    def __init__(self, id_medic, nume, continut, tip, emc, data):
        self.id_medic = id_medic
        self.nume = nume
        self.continut = continut
        self.tip = tip
        self.emc = emc
        self.data=data

    # def incarca_document(self, id_medic, nume, continut, tip, emc):
    def incarca_document(self):
        connection = sqlite3.connect('medici.db')
        cursor = connection.cursor()
        sql_script = f"""
                       INSERT INTO fisiere (id_medic, nume, continut, tip, emc, data) 
                       VALUES ("{self.id_medic}", "{self.nume}", "{self.continut}", "{self.tip}", "{self.emc}", "{self.data}")"""

        cursor.execute(sql_script)
        connection.commit()
        rows = cursor.fetchall()
        out=0
        for row in rows:
            print(row)
            out = int(row[0])
        connection.close()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@fisiere.route('/incarcare/<int:id_medic>', methods=['POST', 'GET'])
def incarcare(id_medic):
    error = None
    if request.method == 'POST':
        # tip = request.form['tip']
        # emc = request.files['emc']
        if 'emc' in request.form:
            emc = request.form['emc']
        else:
            emc = "8"  # Avoid KeyError
        if 'tip' in request.form:
            tip = request.form['tip']
        else:
            tip = "emc"  # Avoid KeyError
        print(f'type(request)={type(request)}')
        if 'data' in request.form:
            data = request.form['data']
            if data == "":
                data = datetime.today().strftime('%Y-%m-%d')
        else:
            data = "data"  # Avoid KeyError

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            fisier = Fisier(id_medic=id_medic, nume=filename, continut=file, tip=tip, emc=emc, data=data)
            # id, id_medic, nume, continut, tip, emc)
            if (fisier.incarca_document()):
                return redirect(url_for('profile', id=id_medic))
            # url_viza=url_for('profile', id=id_medic)
            fisiere_medic = url_for("fisiere.afiseaza_documente_medic", id_medic=id_medic)
            pagina_medic = url_for("profile", id=id_medic)
            return render_template('fisier/fisier_incarcat.html', error=error, id_medic=id_medic, filename=filename, tip=tip, fisiere_medic=fisiere_medic, pagina_medic=pagina_medic)

            #return redirect(url_for('download_file', name=filename))
    return render_template('fisier/incarca.html', error=error, id_medic=id_medic)

@fisiere.route('/fisier') # pentru admin
def afiseaza_documente():
    error = None
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, id_medic, nume, continut, tip, emc, data FROM fisiere")
    rows = cursor.fetchall()
    out = 0
    fisiere= []
    for row in rows:
        print(row)
        out = row
        fisiere.append(row)
        id, id_medic, nume, continut, tip, emc, data = row
    print(f'profile out id={id}')
    print(f'profile out id_medic={id_medic}')
    # edit = url_for("edit_user", id=id)
    return render_template('fisier/index.html', fisiere=fisiere)

#afiseaza fisierele incarcate de un medic
@fisiere.route('/fisier/<int:id_medic>')
def afiseaza_documente_medic(id_medic):
    error = None
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, id_medic, nume, continut, tip, emc, data FROM fisiere WHERE id_medic={id_medic}")
    rows = cursor.fetchall()
    out = 0
    fisiere= []
    for row in rows:
        print(row)
        out = row
        fisiere.append(row)
        id, id_medic, nume, continut, tip, emc, data = row
        # print(f'profile out id={id}')
        # print(f'profile out id_medic={id_medic}')
     # edit = url_for("edit_user", id=id)
    pagina_medic = url_for("profile", id=id_medic)
    return render_template('fisier/index_medic.html', fisiere=fisiere, id_medic=id_medic, pagina_medic=pagina_medic)
# download fisier
@fisiere.route('/fisier/download/<int:id_fisier>')
def download_file(id_fisier):
    connection = sqlite3.connect('medici.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, id_medic, nume, continut, tip, emc, data FROM fisiere WHERE id={id_fisier}")
    row = cursor.fetchone()
    if row:
        id, id_medic, nume, continut, tip, emc, data = row
        # Assuming 'continut' is the file content in bytes
        return send_file(io.BytesIO(continut), attachment_filename=nume, as_attachment=True)
    else:
        flash('File not found')
        return redirect(url_for('fisiere.afiseaza_documente'))

