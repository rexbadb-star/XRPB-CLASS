import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = 'XRPB_SECRET_KEY' 

def get_db_connection():
    conn = sqlite3.connect('database.db')
    # Biar hasil query berbentuk dictionary (bisa dipanggil pake nama kolom)
    conn.row_factory = sqlite3.Row 
    return conn

# ... (Kode /login, /, /logout, /jadwal yang lama biarkan tetap ada) ...

@app.route('/absensi', methods=['GET', 'POST'])
def absensi():
    if 'user' not in session:
        return redirect('/login')
        
    conn = get_db_connection()

    # Jika user menekan tombol "Kirim Absen" (POST)
    if request.method == 'POST':
        nama_siswa = request.form['nama']
        ket = request.form['keterangan']
        
        # Perintah SQL untuk simpan data (CREATE)
        conn.execute('INSERT INTO absensi (nama, keterangan) VALUES (?, ?)',
                     (nama_siswa, ket))
        conn.commit() # Simpan permanen
        conn.close()
        return redirect('/absensi')

    # Jika user hanya melihat halaman (GET) (READ)
    daftar_absen = conn.execute('SELECT * FROM absensi ORDER BY tanggal DESC').fetchall()
    conn.close()
    
    return render_template('absensi.html', data_absen=daftar_absen)

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

@app.route('/')
def home():
    
    if 'user' not in session:
        return redirect('/login') 
    
    
    return render_template('index.html', nama=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None) 
    return redirect('/login')

@app.route('/jadwal')
def jadwal():
    
    if 'user' not in session:
        return redirect('/login')
    return render_template('jadwal.html')

@app.route('/seragam')
def seragam():
    if 'user' not in session:
        return redirect('/login')
    return "Seragam Harian: Senin Putih Abu, Selasa Pramuka" 

if __name__ == '__main__':
    app.run(debug=True)
