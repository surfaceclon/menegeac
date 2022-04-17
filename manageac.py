import sys
import pyperclip
import random
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class invite(QWidget):
    def __init__(self, parent=None):
        super(invite, self).__init__(parent)
        self.resize(400, 200)
        self.setFixedSize(self.size())
        self.setWindowTitle('MENEGEACC')
        self.setStyleSheet(
            'background-color: #000000;\n'
        )

        self.toptext = QLabel(self)
        self.toptext.setGeometry(150, 10, 100, 30)
        self.toptext.setText('LOGIN')
        self.toptext.setStyleSheet(
            'color: #F0FFFF;\n'
            'font-size: 20px;\n'
            'font-weight: bold;\n'
        )

        self.loginfield = QLineEdit(self)
        self.loginfield.setGeometry(65, 50, 250, 30)
        self.loginfield.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )

        self.pasfield = QLineEdit(self)
        self.pasfield.setEchoMode(QLineEdit.Password)
        self.pasfield.setGeometry(65, 90, 250, 30)
        self.pasfield.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )

        self.okbut = QPushButton(self)
        self.okbut.setGeometry(85, 130, 90, 30)
        self.okbut.setText('OK')
        self.okbut.setStyleSheet(
            'background: #FF8C00;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )
        self.okbut.clicked.connect(self.loginaccountstepOne)

        self.creatbut = QPushButton(self)
        self.creatbut.setGeometry(210, 130, 90, 30)
        self.creatbut.setText('CREAT')
        self.creatbut.setStyleSheet(
            'background: #FF8C00;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )
        self.creatbut.clicked.connect(self.createtables)

        self.infotext = QLabel(self)
        self.infotext.setGeometry(110, 160, 170, 30)
        self.infotext.setStyleSheet(
            'color: #F0FFFF;\n'
            'font-size: 20px;\n'
            'font-weight: bold;\n'
        )

    # clear field
    def clearfields(self):
        self.loginfield.clear()
        self.pasfield.clear()
    
    # Creat table pas,log and table data user in db
    def createtables(self):
        con = sqlite3.connect('menegeac.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS logindetails(
                loginpass TEXT
            );
        """)
        con.commit()
        login = self.loginfield.text()
        password = self.pasfield.text()
        datapl = [(password + login)]
        pl = password + login
        drop = []
        cur.execute("SELECT * FROM logindetails")
        for dates in cur.fetchall():
            for dat in dates:
                drop.append(dat)
        if pl in drop:
            self.infotext.setText('  LOGIN USED')
            self.clearfields()
        else:
            cur.execute("""
                    INSERT INTO logindetails VALUES(?)
                """, datapl)
            con.commit()
            self.infotext.setText('CREAT ACCOUNT')
            self.clearfields()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS %s(
                    acc TEXT,
                    log TEXT,
                    pas TEXT,
                    link TEXT,
                    number TEXT,
                    notes TEXT
                );
            """ % (str(pl)))
            con.commit()

    # Login in account step one
    def loginaccountstepOne(self):
        cheklogin = len(self.loginfield.text())
        chekpassword = len(self.pasfield.text())
        if cheklogin == 0:
            self.infotext.setText('  INPUT ERROR')
            self.clearfields()
        elif chekpassword == 0:
            self.infotext.setText('  INPUT ERROR')
        else:
            login = self.loginfield.text()
            password = self.pasfield.text()
            pl = password + login
            self.clearfields()
            self.loginaccountstepTwo(pl)

    # Login in account step two
    def loginaccountstepTwo(self, pl):
        con = sqlite3.connect('menegeac.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM logindetails")
            drop = []
            for i in cur.fetchall():
                for j in i:
                    drop.append(j)
            if pl in drop:
                self.infotext.setText('  FOUND IT OK')
                self.openwin(pl)
            else:
                self.infotext.setText('   NOT FOUND')
        except sqlite3.Error:
            self.infotext.setText('   NOT FOUND')

    # Open main window user record
    def openwin(self, pl):
        self.opwin = TwoWindow(pl)
        self.opwin.show()

class TwoWindow(QWidget):
    def __init__(self, pl):
        super().__init__()
        self.pl = pl
        self.setGeometry(400, 180, 890, 400)
        self.setFixedSize(self.size())
        self.setWindowTitle('MENEGEACC')
        self.setStyleSheet(
            'background-color: #000000;\n'
        )
        self.lists = QListWidget(self)
        self.lists.setGeometry(20, 25, 150, 350)
        self.lists.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )
        self.lists.itemClicked.connect(self.clickacc)

        #LineEdit
        self.acctx = QLineEdit(self)
        self.acctx.setGeometry(200, 40, 250, 30)
        self.acctx.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )
        
        self.logtx = QLineEdit(self)
        self.logtx.setGeometry(200, 90, 250, 30)
        self.logtx.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )

        self.pastx = QLineEdit(self)
        self.pastx.setGeometry(200, 140, 250, 30)
        self.pastx.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )

        self.lintx = QLineEdit(self)
        self.lintx.setGeometry(200, 190, 250, 30)
        self.lintx.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )

        self.numtx = QLineEdit(self)
        self.numtx.setGeometry(200, 240, 250, 30)
        self.numtx.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )

        self.nottx = QLineEdit(self)
        self.nottx.setGeometry(200, 290, 250, 30)
        self.nottx.setStyleSheet(
            'background: #F0FFFF;\n'
            'border-radius: 10px;\n'
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )
        # Buttons
        self.clear = QPushButton(self)
        self.clear.setGeometry(470, 40, 90, 30)
        self.clear.setText('CLEAR')
        self.clear.setStyleSheet(
            'background: #00FF7F;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.clear.clicked.connect(self.clearfield)

        self.logcop = QPushButton(self)
        self.logcop.setGeometry(470, 90, 90, 30)
        self.logcop.setText('LOGIN COPY')
        self.logcop.setStyleSheet(
            'background: #FF8C00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.logcop.clicked.connect(self.logcopy)

        self.pascop = QPushButton(self)
        self.pascop.setGeometry(470, 140, 90, 30)
        self.pascop.setText('PASS COPY')
        self.pascop.setStyleSheet(
            'background: #FF8C00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.pascop.clicked.connect(self.pascopy)

        self.lincop = QPushButton(self)
        self.lincop.setGeometry(470, 190, 90, 30)
        self.lincop.setText('LINK COPY')
        self.lincop.setStyleSheet(
            'background: #FF8C00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.lincop.clicked.connect(self.linkcopy)

        self.numcop = QPushButton(self)
        self.numcop.setGeometry(470, 240, 90, 30)
        self.numcop.setText('NUMBER COPY')
        self.numcop.setStyleSheet(
            'background: #FF8C00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.numcop.clicked.connect(self.numcopy)

        self.notcop = QPushButton(self)
        self.notcop.setGeometry(470, 290, 90, 30)
        self.notcop.setText('NOTES COPY')
        self.notcop.setStyleSheet(
            'background: #FF8C00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.notcop.clicked.connect(self.notcopy)

        self.leftlab = QLabel(self)
        self.leftlab.setGeometry(580, 35, 250, 290)
        self.leftlab.setStyleSheet(
            'background: #DCDCDC;\n'
            'border-radius: 10px;\n'
        )

        self.editlab = QLabel(self.leftlab)
        self.editlab.setGeometry(100, 0, 35, 30)
        self.editlab.setStyleSheet(
            'font-size: 15px;\n'
            'font-weight: bold;\n'
        )
        self.editlab.setText('EDIT')

        self.updatebut = QPushButton(self.leftlab)
        self.updatebut.setGeometry(20, 55, 210, 30)
        self.updatebut.setText('UPDATE')
        self.updatebut.setStyleSheet(
            'background: #00FF7F;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.updatebut.clicked.connect(self.update)

        self.writechangebut = QPushButton(self.leftlab)
        self.writechangebut.setGeometry(20, 95, 210, 30)
        self.writechangebut.setText('WRITE DATA')
        self.writechangebut.setStyleSheet(
            'background: #FFFF00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.writechangebut.clicked.connect(self.writechange)

        self.genpasbut = QPushButton(self.leftlab)
        self.genpasbut.setGeometry(20, 135, 210, 30)
        self.genpasbut.setText('GENERATE PASSWORD')
        self.genpasbut.setStyleSheet(
            'background: #FFFF00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.genpasbut.clicked.connect(self.generatepass)

        self.delaccbut = QPushButton(self.leftlab)
        self.delaccbut.setGeometry(20, 175, 210, 30)
        self.delaccbut.setText('DELLET ACCOUNT')
        self.delaccbut.setStyleSheet(
            'background: #FFFF00;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.delaccbut.clicked.connect(self.delleteacc)

        self.delmainacc = QPushButton(self.leftlab)
        self.delmainacc.setGeometry(20, 215, 210, 30)
        self.delmainacc.setText('DELLET MAIN ACCOUNT')
        self.delmainacc.setStyleSheet(
            'background: #FF4500;\n'
            'border-radius: 10px;\n'
            'font-size: 11px;\n'
            'font-weight: bold;\n'
        )
        self.delmainacc.clicked.connect(self.delletemainacc)

        self.info = QLabel(self)
        self.info.setGeometry(200, 340, 250, 30)
        self.info.setStyleSheet(
            'color: #FF4500;\n'
            'font-size: 22px;\n'
            'font-weight: bold;\n'
        )
        
    # Clear field
    def clearfield(self):
        listfield = [self.acctx, self.logtx, self.pastx, self.lintx, self.numtx, self.nottx]
        for clr in listfield:
            clr.clear()

    # List account
    def listbox(self):
        con = sqlite3.connect('menegeac.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM %s" % self.pl)
        self.LIS = []
        for lts in cur.fetchall():
            self.LIS.append(lts[0])
        self.lists.clear()
        self.lists.addItems(self.LIS)

    def clickacc(self, item):
        beforclick = item.text()
        self.clearfield()
        con = sqlite3.connect('menegeac.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM '{}' WHERE acc = '{}'".format(self.pl, beforclick))
        drop = []
        for dates in cur.fetchall():
            for date in dates:
                drop.append(date)
        self.clearfield()
        self.acctx.setText(beforclick)
        self.logtx.setText(drop[1])
        self.pastx.setText(drop[2])
        self.lintx.setText(drop[3])
        self.numtx.setText(drop[4])
        self.nottx.setText(drop[5])

    # Update
    def update(self):
        self.clearfield()
        self.listbox()

    # Write or cange
    def writechange(self):
        ac = self.acctx.text()
        lo = self.logtx.text()
        pa = self.pastx.text()
        li = self.lintx.text()
        nu = self.numtx.text()
        no = self.nottx.text()
        con = sqlite3.connect('menegeac.db')
        cur = con.cursor()
        cur.execute("""
            INSERT INTO '{}' VALUES('{}','{}','{}','{}','{}','{}')
                """.format(self.pl, ac, lo, pa, li, nu, no))
        con.commit()
        self.clearfield()
        self.update()


    # Generate password
    def generatepass(self):
        length = 22
        digits='1234567890'
        leters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        leters_2='abcdefghijklmnopqrstuvwxyz'
        symbols='!@#$%^&*()-+'
        password=''
        var=[digits,leters,leters_2,symbols]
        if length<12:
            return 0
        else:
            password+=random.choice(digits)
            password+=random.choice(leters)
            password+=random.choice(leters_2)
            password+=random.choice(symbols)
            while len(password)<length:
                password+=random.choice(var[random.randint(0,3)])
            self.pastx.clear()
            self.pastx.setText(password)

    # Dellet account
    def delleteacc(self):
        con = sqlite3.connect('menegeac.db')
        cur = con.cursor()
        cur.execute("DELETE FROM '{}' WHERE acc = '{}'".format(self.pl, self.acctx.text()))
        con.commit()
        self.clearfield()
        self.update()

    # Dellete main account
    def delletemainacc(self):
        con = sqlite3.connect('menegeac.db')
        cur = con.cursor()
        cur.execute("DELETE FROM logindetails WHERE loginpass='{}'".format(self.pl))
        cur.execute("DELETE FROM '{}'".format(self.pl))
        con.commit()
        self.clearfield()
        self.lists.clear()
        self.info.setText('ACCOUNT DELLETE')

    # Block copy
    def logcopy(self):
        pyperclip.copy(self.logtx.text())

    def pascopy(self):
        pyperclip.copy(self.pastx.text())

    def linkcopy(self):
        pyperclip.copy(self.lintx.text())

    def numcopy(self):
        pyperclip.copy(self.numtx.text())

    def notcopy(self):
        pyperclip.copy(self.nottx.text())


def main():
    app = QApplication(sys.argv)
    ex = invite()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()