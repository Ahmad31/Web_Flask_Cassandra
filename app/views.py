from app import app, login_manager 
from flask import Flask, abort, render_template, session, redirect, url_for, escape, request, flash, g, Response
from .models import db, Dokumen
from .forms import LoginAdminForm
from cassandra.cluster import Cluster
from datetime import datetime

cluster = Cluster(['172.17.0.2'])
sesi = cluster.connect()
sesi.execute("USE project")


@app.route('/detil/<judul>-<nim>')
def detil_doc(nim, judul):
	detil = Dokumen.objects(nim = nim).allow_filtering()
	return render_template("document.html", detil=detil)

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/form_search')
def form_search():
	data = Dokumen.objects().all()
	return render_template("form_search.html", data=data)

@app.route('/search', methods=['GET','POST'])
def search():
	""" cari, query cari """
	cari_judul = sesi.execute(" SELECT * FROM dokumen WHERE judul LIKE  '%{}%'".format(request.form['cari']))
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

@app.route('/login')
def login():
	return render_template("login.html")

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
			doc = Dokumen( nim=request.form['nim'],
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

	return redirect(url_for('data_doc'))

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

@app.route('/data_doc', methods = ['GET','POST'])
def data_doc():
	now = datetime.now()
	now = now.strftime("%Y")
	angkatan_date = reversed(range(int(now)-10, int(now)+1))
	tahun_date = reversed(range(int(now)-10, int(now)+1))
	data_ti = Dokumen.objects.filter(prodi='Teknik Informatika').allow_filtering()
	data_si = Dokumen.objects.filter(prodi='Sistem Informasi').allow_filtering()
	data_tk = Dokumen.objects.filter(prodi='Teknik Komputer').allow_filtering()
	data_mi = Dokumen.objects.filter(prodi='Management Informatika').allow_filtering()
	data_ka = Dokumen.objects.filter(prodi='Komputer Akutansi').allow_filtering()

	return render_template("data_doc.html", data_ti=data_ti, data_si=data_si, data_tk=data_tk, data_mi=data_mi, data_ka=data_ka, date1=angkatan_date, date2=tahun_date)


@app.route('/edit_doc/<nim>', methods = ['GET','POST'])
def edit_doc(nim):
	now = datetime.now()
	now = now.strftime("%Y")
	angkatan_date = reversed(range(int(now)-10, int(now)+1))
	tahun_date = reversed(range(int(now)-10, int(now)+1))
	view_doc = Dokumen.objects(nim = nim).allow_filtering()
	return render_template("edit_doc.html", view_doc=view_doc, date1=angkatan_date, date2=tahun_date) 

@app.route('/respon_edit', methods=['GET','POST'])
def respon_edit():
	if request.method == 'POST':
		if not request.form['nama_m']:
			error = "Masukkan Data dengan komplit dan sesuai!"
		else:
			data = Dokumen.objects(prodi='Teknik Informatika', nim=request.form['nim_mhs']).update(
									nama_mhs=request.form['nama_m'],
									angkatan=request.form['angkatan_mhs'],
									tahun=request.form['tlulus_mhs'],
									judul=request.form['judul_doc'],
									kata_kunci=request.form['kunci_kata'],
									intisari=request.form['intisari_doc'],
									pembimbing=request.form['pembimbing_mhs']
									)
			error = "Maaf Isi Data Secara Lengkap"
			return redirect(url_for('data_doc'))

	return redirect(url_for('data_doc'))

@app.route('/delete_doc/<nim>', methods=['GET','POST'])
def delete_doc(nim):
	return render_template("delete_doc.html", nim=nim) 

@app.route('/respon_delet', methods=['GET','POST'])
def respon_delet():
	return render_template("data_doc.html", delet=delet) 
