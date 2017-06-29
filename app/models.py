from app import db
from app import app
from werkzeug import generate_password_hash, check_password_hash


class Dokumen(db.Model):
    __table_name__ = 'dokumen'

    nim = db.columns.Integer(primary_key=True)
    prodi = db.columns.Text(primary_key=True)
    tahun = db.columns.Integer()
    judul = db.columns.Text()
    nama_mhs = db.columns.Text()
    angkatan = db.columns.Integer()
    intisari = db.columns.Text()
    kata_kunci = db.columns.Text()
    pembimbing = db.columns.Text()
    file1 = db.columns.Text()
    file2 = db.columns.Text()
    file3 = db.columns.Text()
    file4 = db.columns.Text()
    file5 = db.columns.Text()
    password = db.columns.Text()

    def __repr__(self):
        return '<Dokumen %r>' % (self.nim, self.nama_mhs, self.angkatan, self.tahun, self.prodi, self.judul, self.kata_kunci, self.intisari, self.pembimbing, self.password, self.file1, self.file2, self.file3, self.file4, self.file5)

class User_admin(db.Model):
    __table_name__ = "user_admin"
    username = db.columns.Text(primary_key=True)
    password = db.columns.Text(primary_key=True)
    alamat = db.columns.Text()

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User %r>' % (self.username, self.password, self.alamat)






