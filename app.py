from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'XRPB_SECRET_KEY'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', nama=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == 'XRPB-CLASS' and pw == 'ketua_ganteng':
            session['user'] = user
            return redirect('/')
        elif user == 'Adminpanel123' and pw == 'rahasia_dong':
            session['user'] = user
            return redirect('/')
        else:
            return render_template('login.html', error="Username atau Password Salah!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/absensi', methods=['GET', 'POST'])
def absensi():
    if 'user' not in session:
        return redirect('/login')
    conn = get_db_connection()
    if request.method == 'POST':
        nama_siswa = request.form['nama']
        ket = request.form['keterangan']
        conn.execute('INSERT INTO absensi (nama, keterangan) VALUES (?, ?)', (nama_siswa, ket))
        conn.commit()
        conn.close()
        return redirect('/absensi')
    daftar_absen = conn.execute('SELECT * FROM absensi ORDER BY tanggal DESC').fetchall()
    conn.close()
    return render_template('absensi.html', data_absen=daftar_absen)

@app.route('/hapus_absen/<int:id>')
def hapus_absen(id):
    if 'user' in session and session['user'] == 'Adminpanel123':
        conn = get_db_connection()
        conn.execute('DELETE FROM absensi WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect('/absensi')
    return "Akses Ditolak", 403

@app.route('/jadwal')
def jadwal():
    if 'user' not in session: return redirect('/login')
    return render_template('jadwal.html')

@app.route('/seragam')
def seragam():
    if 'user' not in session: return redirect('/login')
    return render_template('seragam.html')

if __name__ == '__main__':
    app.run(debug=True)


