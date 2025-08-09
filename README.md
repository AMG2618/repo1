# 🩺 Platformă Flask pentru Medici – Gestionare Documente și Cereri EMC

Această aplicație web construită cu **Python și Flask** permite medicilor să își creeze conturi, să încarce documente profesionale și să genereze cereri de viză anuală EMC. De asemenea, oferă funcționalități administrative pentru gestionarea utilizatorilor și a documentelor.

## 🚀 Funcționalități principale

### Pentru medici:
- ✅ **Autentificare și înregistrare**: Creare cont și login securizat
- 📤 **Încărcare documente**: Upload fișiere relevante (PDF, imagini etc.)
- 📂 **Vizualizare documente**: Listare și acces la fișierele proprii
- ✏️ **Editare profil**: Actualizare detalii cont (nume, email, parolă etc.)
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

1. Clonează proiectul:
   ```bash
   git clone https://github.com/nume-utilizator/proiect-medici.git
   cd proiect-medici
