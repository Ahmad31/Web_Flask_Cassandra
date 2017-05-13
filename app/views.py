from app import app, login_manager 
from flask import Flask, abort, render_template, session, redirect, url_for, escape, request, flash, g, Response
from .models import db, Document
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
	return render_template("index.html")

@app.route('/form_search')
def form_search():
	data = Document.objects().all()
	return render_template("form_search.html", data=data)

@app.route('/search', methods=['GET','POST'])
def search():
	""" cari, query cari """
	cari_judul = sesi.execute(" SELECT * FROM document WHERE judul LIKE  '%{}%'".format(request.form['cari']))
	info = request.form['cari']
	return render_template("hasil_search.html", cari_judul=cari_judul, info=info)
	
@app.route('/admin')
def admin():
	if not session.get('logged_in'):
		""" ini adalah coment """
		return render_template("login.html")
	else:
		""" ini juga koment """
    	return render_template("index.html")


@app.route('/login_admin', methods=['POST'])
def login_admin():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return admin()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return admin()


@app.route('/add', methods = ['GET', 'POST'])
def add():

	if request.method == 'POST':
		if not request.form['nim'] or not request.form['judul']:
			error = "Masukkan Data dengan komplit dan sesuai!"
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
							file1=request.form['file_doc1'],
							file2=request.form['file_doc2'],
							file3=request.form['file_doc3'],
							file4=request.form['file_doc4'],
							file5=request.form['file_doc5']
							)
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

