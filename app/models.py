from app import db
from app import app
from werkzeug import generate_password_hash, check_password_hash


class Document(db.Model):
    __table_name__ = 'document'

    nim = db.columns.Integer(primary_key=True)
    prodi = db.columns.Text(primary_key=True)
    tahun = db.columns.Date(primary_key=True, clustering_order="DESC")
    judul = db.columns.Text(primary_key=True)
    nama_mhs = db.columns.Text()
    angkatan = db.columns.Date()
    intisari = db.columns.Text()
    kata_kunci = db.columns.Text()
    pembimbing = db.columns.Text()
    file_doc = db.columns.Text()
    password = db.columns.Text()

    def __repr__(self):
        return '<Document %r>' % (self.nim, self.nama_mhs, self.angkatan, self.tahun, self.prodi, self.judul, self.kata_kunci, self.intisari, self.pembimbing, self.password, self.file_doc)

class User_admin(db.Model):
    __table_name__ = "user_admin"
    username = db.columns.Text(primary_key=True)
    password = db.columns.Text(primary_key=True)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User_admin %r>' % (self.username, self.password)






