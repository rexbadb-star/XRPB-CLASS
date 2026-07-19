from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# --- TAMBAHKAN INI ---
app.secret_key = 'XRPB_SECRET_KEY' 


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
