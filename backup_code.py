@app.route('/log')
def log():
	if 'user' is session:
		user_session - escape(session['user']).capitalize()
		return render_template('login.html', user_session=user_session)
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None

	if 'user' is session:
		return redirect(url_for('login'))
	if request.methods == 'POST':
		user_form = request.form['user']
		password_form = request.form['password']
		cur.execute("SELECT COUNT(1) FROM user_admin WHERE user = %s;", [user_form])
		if cur.fetchone()[0]:
			cur.execute(" SELECT password FROM user_admin WHERE user = %s;", [user_form])
			for row in cur.fetchall():
				if md5(password_form).hexdigest() == row[0]:
					session['user'] = request.form['user']
					return redirect(url_for('admin'))
				else:
					error = "Ulangi !!!"
		else:
			error = "Ulangi !!!"
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('index'))




	form = LoginForm()
	if form.validate_on_submit():

		login_user(user)

		flask.flash('Logged in successfully.')

		next = flask.request.args.get('next')

		if not is_safe_url(next):
			return flask.abort(400)

		return flask.redirect(next or flask.url_for('admin'))



@app.route('/home')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return "hello Boos!"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()



    {% if session['logged_in'] %}
<p>You're logged in already!'</p>
{% else %}
<hr>
    <div class="row">   
            <div class="col-md-6 col-md-offset-3">
                <form action="/login" method="POST">
                    
                   
                    <div class="input-group">
                        <span class="input-group-addon" id="basic-addon3">
                       
                        Username</span>
                        <input class="form-control" type="username" name="username" placeholder="Username" id="user" aria-describedby="basic-addon3">
                    </div>
                    <br>
                    <div class="input-group">
                        <span class="input-group-addon" id="basic-addon3">
                       
                        Password</span>
                        <input  class="form-control" id="pass"  aria-describedby="basic-addon3" type="password" name="password" placeholder="Password">
                    </div>
                    <br>
                    <input type="Submit" value="Login" class="btn btn-default btn-sm">
                </form>
            </div>
        </div>
        <hr>

{% endif %}


if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('admin.html')


error = None
	if 'username' in session:
		return redirect(url_for('admin'))
	if request.method == 'POST':
		username_form = request.form['username']
		password_form = request.form['password']
		user = db


if form.validate() == False:
			return render_template('login_admin.html', form=form)
		else:
			session['username'] = form.username.data
			return redirect(url_for('admin'))

	elif request.method == 'GET':
		return render_template('login_admin.html', form=form)


		_nim = request.form['nim']
	_nama_mhs = request.form['nama']
	_angkatan = request.form['angkatan']
	_tahun = request.form['Tlulus']
	_prodi = request.form['jurusan']
	_judul = request.form['judul']
	_kata_kunci = request.form['kunci']
	_intisari = request.form['Isari']
	_pembimbing = request.form['PBimbing']
	_password = request.form['pas']
	_file_doc = request.form['file']


def __init__(self, nim, nama_mhs, angkatan, tahun, prodi, judul, kata_kunci, intisari, pembimbing, password, file_doc):
        self.nim = nim
        self.nama_mhs = nama_mhs
        self.angkatan = angkatan
        self.tahun = tahun
        self.prodi = prodi
        self.judul = judul
        self.kata_kunci = kata_kunci
        self.intisari = intisari
        self.pembimbing = pembimbing
        self.password = password
        self.file_doc = file_doc


!! file index.html lama 
        {% for doc in data %}
	<div class="col-md-8">
    	<h3>Judul : <a href="{{ url_for('detil_doc', nim=doc.nim, judul=doc.judul) }}">  {{ doc.judul }} </a></h3>
    	<p>Prodi : {{ doc.prodi }} | Tahun : {{ doc.tahun }} </p>
    	<hr>
 	</div>
   	{% endfor %}

!! footer, belum terpakai, blum bermanfaat
<div class="col-md-12">
    <footer class="footer">
      <div class="container">
        <p class="text-muted">Copy right SISTEM Arsip Document STMIK AKAKOM</p>
      </div>
    </footer>
    </div>

!! Pesan error
    {% if error %}
		<div class="alert alert-danger"> <strong>{{ error }}</strong></div>
	{% endif %}



	 nim = nim, 
							  intisari = intisari, 
							  tahun = tahun, 
							  nama_mhs = nama,
							  jurusan = jurusan,
							  pembimbing = dos_pembimbing,
							  kata_kunci = kunci_kata,
							  file1 = file_doc1,
							  file2 = file_doc2,
							  file3 = file_doc3,
							  file4 = file_doc4,
							  file5 = file_doc5


from cassandra.cluster import Cluster



cluster = Cluster(['172.17.0.2'])
sesi = cluster.connect()
sesi.execute("USE project")




Dokumen.objects( prodi=request.form['jurusan_mhs'], 
							nim=request.form['nim_mhs']).update(
							nama_mhs=request.form['nama_mhs'],
							judul=request.form['judul_doc']
							)


							kata_kunci=request.form['kunci_kata'],
							intisari=request.form['intisari_doc'],
							pembimbing=request.form['pembimbing_mhs']


delet = DELETE FROM dokumen WHERE prodi ="Teknik Informatika" AND nim=14231112;

@app.route('/respon_delet', methods=['GET','POST'])
def respon_delet():
	return render_template("data_doc.html", delet=delet) 
