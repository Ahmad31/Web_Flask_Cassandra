from app import app, login_manager 
from flask import Flask, abort, render_template, session, redirect, url_for, escape, request, flash, g
from flask_login import login_required, login_user, logout_user, current_user
from .models import db, User, Document
from .forms import LoginAdminForm
from cassandra.cluster import Cluster

cluster = Cluster(['172.17.0.2'])
sesi = cluster.connect()
sesi.execute("USE project")


@app.route('/detil/<judul>-<nim>')
def detil_doc(nim, judul):
	detil = Document.objects(nim = nim)
	return render_template("document.html", detil=detil)

@app.route('/')
@app.route('/index')
def index():
	data = Document.objects().all()
	return render_template("index.html", data=data)

@app.route('/search', methods=['GET','POST'])
def search():
	""" cari, query cari """
	cari_judul = sesi.execute(" SELECT judul FROM document WHERE judul LIKE  '%{}%'".format(request.form['cari']))
	hasil = Document.objects.filter(judul=cari_judul)
	return render_template("hasil_search.html", cari_judul=cari_judul)


@app.route('/admin')
def admin():
	if not session.get('logged_in'):
		""" ini adalah coment """
		return render_template("login.html")
	else:
		""" ini juga koment """
    	return render_template("index.html")

@app.route('/login', methods=['POST'])
def admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return admin()

@login_manager.user_loader
def load_login(username):
	return User.get(text(username))

@app.route('/add', methods = ['GET', 'POST'])
def add():

	if request.method == 'POST':
		if not request.form['nim'] or not request.form['judul']:
			flash('Masukkan NIM dan Jurusan')
		else:
			doc = Document( nim=request.form['nim'],
							nama_mhs=request.form['nama'],
							angkatan=request.form['angkatan'],
							tahun=request.form['Tlulus'],
							prodi=request.form['jurusan'],
							judul=request.form['judul'],
							kata_kunci=request.form['kunci'],
							intisari=request.form['Isari'],
							pembimbing=request.form['PBimbing'],
							password=request.form['pas'],
							file_doc=request.form['file'])
			doc.save()

			flash('Sukses menambah data')
			return redirect(url_for('index'))

	return render_template('input_data.html')

@app.route('/userAdd', methods = ['GET', 'POST'])
def addUser():
	if request.method == 'POST':
		if not request.form['username'] or not request.form['password']:
			flash('masukan data')
		else:
			user = User(username=request.form['username'], password=request.form['password'])
			
			user.save()

			flash('yess')	
			return redirect(url_for('index'))

	return render_template('add_user.html')

