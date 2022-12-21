import sys
from PyQt5 import QtWidgets,QtGui
import sqlite3
import hashlib

class pencere(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()
		self.init_ui()
		self.baglanti()

	def baglanti(self):

		con = sqlite3.connect("kullanicilar.db")
		self.cursor = con.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS kullanicilar (kullanici_adi TEXT,parola TEXT)")
		con.commit()

	def init_ui(self):
		
		self.kullanici_adi = QtWidgets.QLineEdit()
		self.parola = QtWidgets.QLineEdit()
		self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
		self.giris = QtWidgets.QPushButton("giriş")
		self.kayit = QtWidgets.QPushButton("kayıt")
		self.sil = QtWidgets.QPushButton("kayıt sil")
		self.temizle = QtWidgets.QPushButton("temizle")
		self.yazi_alani = QtWidgets.QLabel("")
		self.info1 = QtWidgets.QLabel("kullanıcı adı giriniz : ")
		self.info2 = QtWidgets.QLabel("şifre giriniz : ")


		vbox = QtWidgets.QVBoxLayout()
		vbox.addStretch()
		vbox.addWidget(self.info1)
		vbox.addWidget(self.kullanici_adi)
		vbox.addWidget(self.info2)
		vbox.addWidget(self.parola)
		vbox.addStretch()
		vbox.addWidget(self.giris)
		vbox.addWidget(self.kayit)
		vbox.addWidget(self.sil)
		vbox.addWidget(self.temizle)
		vbox.addWidget(self.yazi_alani)
		vbox.addStretch()
		hbox = QtWidgets.QHBoxLayout()
		hbox.addStretch()
		hbox.addLayout(vbox)
		hbox.addStretch()
		self.setLayout(hbox) 

		self.giris.clicked.connect(self.islem)
		self.temizle.clicked.connect(self.temiz)
		self.kayit.clicked.connect(self.kayit_ol)
		self.sil.clicked.connect(self.silme)


		self.setGeometry(450,100,600,600)
		self.show()

	def islem(self):

		adi = self.kullanici_adi.text()
		parola = self.parola.text()
		self.cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND parola = ?",(adi,parola))
		sonuc = self.cursor.fetchall()
		if len(sonuc) == 0:
			self.yazi_alani.setText("böyle bir kullanıcı bulunamadı ")
		else:
			self.yazi_alani.setText("giriş yapıldı")

	def temiz(self):
		self.kullanici_adi.clear()
		self.parola.clear()
		self.yazi_alani.clear()

	def kayit_ol(self):
		isim = self.kullanici_adi.text()
		sifre = self.parola.text()
		sifre = hashlib.md5(sifre.encode("utf-8")).hexdigest()
		con = sqlite3.connect("kullanicilar.db")
		cursor = con.cursor()
		cursor.execute("INSERT INTO kullanicilar VALUES (?,?)",(isim,sifre))
		con.commit()
		self.yazi_alani.setText("kullanıcı eklendi")

	def silme(self):

		isim = self.kullanici_adi.text()
		sifre = self.parola.text()
		sifre = hashlib.md5(sifre.encode("utf-8")).hexdigest()
		con = sqlite3.connect("kullanicilar.db")
		cursor = con.cursor()
		cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND parola = ?",(isim,sifre))
		veri = cursor.fetchall()
		if len(veri) == 0:
			self.yazi_alani.setText("böyle bir kullanıcı bulunamadı")
		else:
			cursor.execute("DELETE FROM kullanicilar WHERE kullanici_adi = ?",(isim,))
			con.commit()
			self.yazi_alani.setText("silme işlemi başarılı")





app = QtWidgets.QApplication(sys.argv)
pencere = pencere()
sys.exit(app.exec_())

