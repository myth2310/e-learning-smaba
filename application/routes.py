from application import app
from flask import Flask,render_template,request, redirect,url_for,flash,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import os
from werkzeug.utils import secure_filename

app.secret_key = 'your_secret_key'

app.config['UPLOAD_FILE_MATERI'] = 'application/static/materi/'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'e-learning-smaba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

#Admin Page
@app.route('/home')
def home():
    if 'islogin' in session:
         return render_template('admin/index.html')
    else:
        return redirect(url_for('login'))

@app.route('/data-siswa')
def dataSiswa():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('''
            SELECT users.*, kelas.kelas,jurusan.jurusan
            FROM users 
            LEFT JOIN kelas ON kelas.id_kelas = users.id_kelas
            LEFT JOIN jurusan ON users.id_jurusan = jurusan.id_jurusan
            WHERE users.level = 'Siswa'
        ''')
        siswa = curl.fetchall() 
        return render_template('admin/siswa.html',siswa=siswa)
    else:
        return redirect(url_for('login'))

@app.route('/data-guru')
def dataGuru():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('''
                SELECT users.*, mapel.mapel
                FROM users 
                LEFT JOIN mapel ON mapel.id_mapel = users.id_mapel
                WHERE users.level = 'Guru'
            ''')
        guru = curl.fetchall() 
        return render_template('admin/guru.html',guru=guru)
    else:
        return redirect(url_for('login'))
    
@app.route('/data-admin')
def dataAdmin():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE level = 'Admin' ")
        admin = curl.fetchall()
        return render_template('admin/admin.html',admin=admin)
    else:
        return redirect(url_for('login'))
   
@app.route('/form-registrasi')
def formRegistrasi():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM mapel")
        mapel = curl.fetchall()

        curl.execute("SELECT * FROM kelas")
        kelas = curl.fetchall()

        curl.execute("SELECT * FROM jurusan")
        jurusan = curl.fetchall()
        return render_template('admin/formRegistrasi.html',kelas=kelas,mapel=mapel,jurusan=jurusan)
    else:
        return redirect(url_for('login'))
    
@app.route('/kelas')
def kelas():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('''
                SELECT kelas.*, jurusan.jurusan
                FROM kelas 
                LEFT JOIN jurusan ON kelas.id_jurusan = jurusan.id_jurusan
            ''')
        kelas = curl.fetchall()

        curl.execute("SELECT * FROM jurusan")
        jurusan = curl.fetchall()
        return render_template('admin/kelas.html',kelas=kelas,jurusan=jurusan)
    else:
        return redirect(url_for('login'))
   
@app.route('/mapel')
def mapel():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('''
                SELECT mapel.*, jurusan.jurusan
                FROM mapel
                LEFT JOIN jurusan ON mapel.id_jurusan = jurusan.id_jurusan
            ''')
        mapel = curl.fetchall()

        curl.execute("SELECT * FROM jurusan")
        jurusan = curl.fetchall()
        return render_template('admin/mapel.html',mapel=mapel,jurusan=jurusan)
    else:
        return redirect(url_for('login'))

@app.route('/jurusan')
def jurusan():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM jurusan")
        jurusan = curl.fetchall()
        return render_template('admin/jurusan.html',jurusan=jurusan)
    else:
        return redirect(url_for('login'))

@app.route('/jadwal')
def jadwal():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM kelas")
        kelas = curl.fetchall()

        curl.execute('''
                SELECT users.*, mapel.mapel
                FROM users 
                LEFT JOIN mapel ON mapel.id_mapel = users.id_mapel
                WHERE users.level = 'Guru'
            ''')
        guru = curl.fetchall() 

        curl.execute("SELECT * FROM mapel")
        mapel = curl.fetchall()

        curl.execute('''
                SELECT jadwal.*, mapel.mapel,kelas.kelas,users.nama
                FROM jadwal 
                LEFT JOIN mapel ON mapel.id_mapel = jadwal.id_mapel
                LEFT JOIN kelas ON kelas.id_kelas = jadwal.id_kelas
                LEFT JOIN users ON users.id_user = jadwal.id_user
            ''')
        data = curl.fetchall() 

        return render_template('admin/jadwal.html',kelas=kelas,mapel=mapel,guru=guru,data=data)
    else:
        return redirect(url_for('login'))

#Page Guru
@app.route('/tema-soal')
def temaSoal():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM kategori WHERE id_user = %s",(session['id_user'],))
        kategori = curl.fetchall()
        return render_template('guru/tema.html',kategori=kategori)
    else:
        return redirect(url_for('login'))

@app.route('/soal')
def soal():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM kategori WHERE id_user = %s",(session['id_user'],))
        kategori = curl.fetchall()
        return render_template('guru/soal.html',kategori=kategori)
    else:
        return redirect(url_for('login'))

@app.route('/tinjau-soal/<int:id_kategori>')
def tinjauSoal(id_kategori):
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM soal WHERE id_kategori = %s", (id_kategori,))
        soal = curl.fetchall()

        query = '''
                SELECT kategori.*
                FROM kategori 
                LEFT JOIN soal ON soal.id_kategori = kategori.id_kategori
                WHERE kategori.id_kategori = %s
            '''
        curl.execute(query, (id_kategori,))
        detail = curl.fetchone()
        return render_template('guru/tinjau.html', soal=soal,detail=detail)
    else:
        return redirect(url_for('login'))

@app.route('/form-soal')
def formSoal():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM kategori WHERE id_user = %s",(session['id_user'],))
        kategori = curl.fetchall()
        return render_template('guru/formSoal.html',kategori=kategori)
    else:
        return redirect(url_for('login'))
        
@app.route('/materi')
def materi():
    if 'islogin' in session:
        id_user = session.get('id_user')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM kelas")
        kelas = curl.fetchall()

        materi = '''
            SELECT materi.*, mapel.mapel,kelas.kelas
            FROM materi 
            LEFT JOIN mapel ON mapel.id_mapel = materi.id_mapel
            LEFT JOIN kelas ON kelas.id_kelas = materi.id_kelas
            WHERE materi.id_user = %s
        '''
        curl.execute(materi,(id_user,))
        data = curl.fetchall()

        query = '''
            SELECT users.*, mapel.mapel
            FROM users 
            LEFT JOIN mapel ON mapel.id_mapel = users.id_mapel
            WHERE users.id_user = %s
        '''
        curl.execute(query,(id_user,))
        mapel = curl.fetchone()
        
        return render_template('guru/materi.html',kelas=kelas,mapel=mapel,data=data)
    else:
        return redirect(url_for('login'))

#Page Siswa
@app.route('/daftar-materi')
def daftarMateri():
    if 'islogin' in session:
        id_user = session.get('id_user')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query ='''
            SELECT jadwal.*,mapel.mapel,kelas.kelas
            FROM jadwal 
            LEFT JOIN users ON jadwal.id_kelas = users.id_kelas
            LEFT JOIN mapel ON jadwal.id_mapel = mapel.id_mapel
            LEFT JOIN kelas ON kelas.id_kelas = jadwal.id_kelas
            WHERE users.id_user = %s
        '''
        curl.execute(query, (id_user,))


        curl.execute(query, (id_user,))

        data = curl.fetchall()
        print(data)

        return render_template('siswa/materi.html',data=data)
    else:
        return redirect(url_for('login'))

@app.route('/<int:id_mapel>')
def viewMateri(id_mapel):
    if 'islogin' in session:
        id_user = session.get('id_user')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = '''
            SELECT materi.*
            FROM materi 
            LEFT JOIN users ON materi.id_kelas = users.id_kelas
            LEFT JOIN kelas ON materi.id_kelas = kelas.id_kelas
            WHERE users.id_kelas = materi.id_kelas
            AND users.id_user = %s
        '''
        curl.execute(query, (id_user,))
        data = curl.fetchall()
       
        guru = '''
            SELECT materi.*,users.nama,mapel.mapel
            FROM materi 
            LEFT JOIN users ON materi.id_user = users.id_user
            LEFT JOIN mapel ON materi.id_mapel = mapel.id_mapel
        '''
        curl.execute(guru)
        dataGuru = curl.fetchone()
        print(dataGuru)
        return render_template('siswa/detailMateri.html',data=data,dataGuru=dataGuru)
    else:
        return redirect(url_for('login'))

@app.route('/view/<int:id_materi>')
def view_pdf(id_materi):
    if 'islogin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT file FROM materi WHERE id_materi = %s", (id_materi,))
        pdf_filename = cur.fetchone()
        cur.execute("SELECT materi FROM materi WHERE id_materi = %s", (id_materi,))
        materi = cur.fetchone()
        cur.close()
        return render_template('siswa/viewPdf.html', pdf=pdf_filename,materi=materi)
    else:
        return redirect(url_for('login'))

@app.route('/ujian')
def ujian():
    if 'islogin' in session:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM kategori ")
        kategori = curl.fetchall()
        return render_template('siswa/ujian.html')
    else:
        return redirect(url_for('login'))

#Action Guru
@app.route('/insert-kategori', methods=['POST'])
def insertKategori():
    id_user = session(['id_user'])
    kategori = request.form['kategori']
    tanggal = request.form['tanggal']
    time_start = request.form['time_start']
    time_done = request.form['time_done']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO kategori (id_user,kategori,tanggal,time_start,time_done) VALUES (%s,%s,%s,%s,%s)",(id_user,kategori,tanggal,time_start,time_done))
    mysql.connection.commit()
    return redirect(url_for('temaSoal'))

@app.route('/insert-soal', methods=['POST'])
def insertSoal():
    id_kategori = request.form['id_kategori']
    pertanyaan = request.form['pertanyaan']
    jawaban_a = request.form['jawaban_a']
    jawaban_b = request.form['jawaban_b']
    jawaban_c = request.form['jawaban_c']
    jawaban_d = request.form['jawaban_d']
    correct = request.form['correct']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO soal (id_kategori, pertanyaan, jawaban_a, jawaban_b, jawaban_c, jawaban_d, correct) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id_kategori, pertanyaan, jawaban_a, jawaban_b, jawaban_c, jawaban_d, correct))
    mysql.connection.commit()
    return redirect(url_for('soal'))

def generate_slug(text):
    text = text.lower()
    text = ''.join(e for e in text if (e.isalnum() or e == ' '))
    text = text.replace(' ', '-')
    return text

@app.route('/insert-materi',methods=['POST', 'GET'])
def insertMateri():
    id_user = session['id_user']
    materi = request.form['materi']
    materi_slug = generate_slug(materi)
    id_kelas = request.form['id_kelas']
    id_mapel = request.form['id_mapel']
    link = request.form['link']
    file = request.files['file']
    date = request.form['date']

    if file:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(app.config['UPLOAD_FILE_MATERI'])
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
    else:
        filename = None

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO materi (id_user,id_kelas,id_mapel,materi,materi_slug,date,link,file) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" ,(id_user,id_kelas,id_mapel,materi,materi_slug,date,link,filename))  
    mysql.connection.commit()
    flash('Materi berhasil disimpan')
    return redirect(url_for('materi'))


#Action Admin
@app.route('/insert-user', methods=['POST'])
def insertUser():
    nama = request.form['nama']
    email = request.form['email']
    status = request.form['status']
    level = request.form['level']
    id_mapel = request.form['id_mapel']
    id_jurusan = request.form['id_jurusan']
    id_kelas = request.form['id_kelas']
    password = request.form['password'] 
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (nama,email,status,level,id_mapel,id_jurusan,id_kelas,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(nama,email,status,level,id_mapel,id_jurusan,id_kelas,hashed_password))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/insert-kelas',methods=['POST'])
def insertKelas():
    id_jurusan = request.form['id_jurusan']
    kelas = request.form['kelas']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO kelas (id_jurusan,kelas) VALUES (%s,%s)" ,(id_jurusan,kelas))  
    mysql.connection.commit()
    return redirect(url_for('kelas'))

@app.route('/insert-mapel',methods=['POST','GET'])
def insertMapel():
    mapel= request.form['mapel']
    id_jurusan = request.form['id_jurusan']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO mapel (mapel,id_jurusan) VALUES (%s,%s)", (mapel, id_jurusan))
    mysql.connection.commit()
    return redirect(url_for('mapel'))

@app.route('/insert-jurusan',methods=['POST','GET'])
def insertJurusan():
    jurusan= request.form['jurusan']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO jurusan (jurusan) VALUES (%s)", (jurusan,))
    mysql.connection.commit()
    return redirect(url_for('jurusan'))

@app.route('/insert-jadwal', methods=['POST'])
def insertJadwal():
    hari = request.form['hari']
    id_mapel = request.form['id_mapel']
    id_kelas = request.form['id_kelas']
    id_user = request.form['id_user']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO jadwal (hari, id_mapel, id_kelas,id_user) VALUES (%s, %s, %s,%s)",(hari, id_mapel, id_kelas,id_user))
    mysql.connection.commit()
    return redirect(url_for('jadwal'))


#Auth/Login
@app.route('/action-login', methods=['GET', 'POST'])
def actionLogin():
    if 'islogin' in session:
        return redirect(url_for('home'))
    if request.method == 'POST' and 'nama' in request.form and 'password' in request.form:
        nama = request.form['nama']
        password = request.form['password'] 
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE nama = %s', (nama,))
        account = cursor.fetchone()
        if account and check_password(password, account['password']):
            session['islogin'] = True
            session['id_user'] = account['id_user']
            session['nama'] = account['nama']
            session['level'] = account['level']
           
            if account['level'] == 'Admin':
                return redirect(url_for('home'))
            elif account['level'] == 'Guru':
                return redirect(url_for('home'))
            elif account['level'] == 'Siswa':
                return redirect(url_for('home'))
        else:
            flash("User Tidak Ditemukan atau Password Salah")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

def check_password(input_password, stored_password):
    hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
    return hashed_input_password == stored_password

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))