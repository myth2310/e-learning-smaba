from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'e-learning-smaba'
mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
        
    # Migrasi Data
    cur = mysql.connection.cursor()

    #Users
    cur.execute("DELETE FROM hasil_ujian")
    cur.execute("ALTER TABLE hasil_ujian DROP id_ujian")
    cur.execute("ALTER TABLE hasil_ujian ADD  id_ujian INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    mysql.connection.commit()