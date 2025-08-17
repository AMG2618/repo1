# 🩺 Platformă Flask pentru Medici – Gestionare Documente și Cereri EMC

Această aplicație web construită cu **Python și Flask** permite medicilor să își creeze conturi, să încarce documente profesionale și să genereze cereri de viză anuală EMC. De asemenea, oferă funcționalități administrative pentru gestionarea utilizatorilor și a documentelor.

## 🚀 Funcționalități principale

### Pentru medici:
- ✅ **Autentificare și înregistrare**: Creare cont și login securizat
- 📤 **Încărcare documente**: Upload fișiere relevante (PDF, imagini etc.)
- 📂 **Vizualizare documente**: Listare și acces la fișierele proprii
- ✏️ **Editare profil**: Actualizare detalii cont (user, parola, nume, prenume si colegiu)
- 📄 **Cerere viză EMC**:
- 📄 **Descărcare documente**.
- 📄 **Pagina EMC**:
  - Afișare punctaj EMC acumulat în ultimul an
  - Generare **cerere viză anuală EMC** dacă sunt îndeplinite condițiile (≥ 48 puncte)

### Pentru administrator:
- 👥 **Gestionare utilizatori**:
        - Vizualizare, editare și ștergere conturi
- 📁 **Acces la toate documentele** încărcate de medici
- 📝 **Vizualizare cereri de viză EMC** generate de utilizatori

## 🛠️ Tehnologii folosite

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML, CSS
- **Bază de date**: SQLite
- **Autentificare**: Session
- **Upload fișiere**: Flask-Uploads / Werkzeug

## 📦 Instalare locală
1. Asigură-te că ai instalat Python 3.x și pip.
2. Clonează repository-ul:
    ```bash
   git clone https://github.com/AMG2618/repo1.git project_p1
   cd project_p1
3. Creeaza baza de date:
    ```bash
    python create_db.py
