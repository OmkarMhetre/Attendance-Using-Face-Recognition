from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
import sys
import time
from PyQt5.uic import loadUiType
from PyQt5.uic import *
import mysql.connector

import datetime
import time
from PyQt5 import QtCore
import cv2

import numpy as np
import face_recognition
import os
import csv

from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
import mysql.connector
from io import BytesIO
from PIL import Image as PILImage

import res_rc

ui, _ = loadUiType('ui_main_win2.ui')


class Splash(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("splash2.ui", self)
        self.initUI()
        self.setWindowFlag(Qt.FramelessWindowHint)

    def initUI(self):
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def progres(self):
        for i in range(3):
            time.sleep(0.01)
            self.progressBar.setValue(i)


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.capture = None
        self.setupUi(self)
        self.showMaximized()
        self.tabWid.setCurrentIndex(0)
        # self.setFixedWidth(1228)
        # self.setFixedHeight(866)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.minwin.clicked.connect(lambda: self.showMinimized())
        self.closewin.clicked.connect(lambda: self.close())
        self.maxiwin.clicked.connect(lambda: self.restore_or_maximize_window())

        self.login_scr_btn.clicked.connect(self.Open_Login_Tab)
        self.Reg_scr_btn.clicked.connect(self.Open_Reg_Tab)
        self.out_btn.clicked.connect(self.showout)
        self.out_btn.hide()
        self.db.clicked.connect(self.Open_Db_Tab)
        self.db.hide()
        self.Ligin_btn.clicked.connect(self.Log_user)
        self.Reg_Scr_b2.clicked.connect(self.Open_Reg_Tab)
        self.tabWid.tabBar().setVisible(False)
        # ______________________________________ADMIN & ForgotPass_____________________________________________________
        self.adminbtn.clicked.connect(self.showADM)
        self.dlulbtn.clicked.connect(self.dlul)
        self.Ligin_btn_2.clicked.connect(self.adlogin)
        self.dlarbtn.clicked.connect(self.dlal)
        self.logout2.clicked.connect(self.lg2)

        self.FPASS.clicked.connect(self.Fpass)
        self.Resetbtn.clicked.connect(self.Reset)
        self.Save.clicked.connect(self.savepass)

        self.export_2.clicked.connect(self.export)

        # ____________________________________________________________________Reg____________________________________________
        self.logic = 1
        self.value = 1
        self.opencam.clicked.connect(self.onclick)
        # self.Savebtn.clicked.connect(self.exit)
        self.CAPTURE.clicked.connect(self.CAP)
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++DB+++++++++++++++++++++++++++++++++++++++++++++++

        self.READ.clicked.connect(self.READDB)
        self.tableWid.setColumnWidth(0, 300)
        self.tableWid.setColumnWidth(1, 250)
        self.tableWid.setRowHeight(0, 40)
        self.tableWid_2.setColumnWidth(0, 300)
        self.tableWid_2.setColumnWidth(1, 180)
        self.tableWid_2.setColumnWidth(2, 200)
        self.tableWid_2.setColumnWidth(3, 140)
        self.tableWid_2.setColumnWidth(4, 160)
        # self.READDB()
        self.grbtn.setEnabled(False)
        self.grbtn.hide()
        self.out_btn.setEnabled(False)
        self.db.setEnabled(False)
        self.logoutbtn.setEnabled(False)
        self.logoutbtn.hide()
        # ________________________________________________________________OutPutWindow___________________________________________

        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)
        self.imgLabel.mousePressEvent = self.clear_label
        self.ClockInBtn.clicked.connect(self.start_camera)
        self.ClockOutBtn.clicked.connect(self.start_camera2)
        self.closebtn.clicked.connect(self.stop_camera)
        global TimeList1,TimeList2

        # Set up webcam
        self.cap = cv2.VideoCapture(1)
        self.timer = QTimer()
        self.timer2 = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer2.timeout.connect(self.update_frame2)
        self.known_face_encodings = []
        self.known_face_names = []

        # ______________________________________________________________chart___________________________________________
        self.grbtn.clicked.connect(self.showgr)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.logoutbtn.clicked.connect(self.signout)

    def export(self):
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Omkar@123',
            database='face'
        )
        cursor = cnx.cursor()
        cursor.execute("SELECT img, name, time, status, EL FROM att")
        data = cursor.fetchall()

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        # Convert data to a list of lists with header row
        table_data = [column_names]
        for row in data:
            row_data = []

            # Process image column
            image_blob = row[0]
            image = PILImage.open(BytesIO(image_blob))
            image = image.resize((100, 100))  # Resize image as needed
            image_data = BytesIO()
            image.save(image_data, format='PNG')
            image_data.seek(0)
            row_data.append(Image(image_data))

            # Process string columns
            string_columns = [str(cell) for cell in row[1:4]]
            row_data.extend(string_columns)

            # Process integer column
            integer_column = str(row[4])
            row_data.append(integer_column)

            table_data.append(row_data)

        # Define table style
        table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, 'black'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'lightgrey'),
        ])

        # Generate PDF
        desktop_path = os.path.expanduser("~/Desktop")  # Get desktop directory
        pdf_path = os.path.join(desktop_path, "Attendance-report.pdf")  # Output PDF file path
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
        table = Table(table_data)
        table.setStyle(table_style)

        # Add table to the PDF
        elements = [table]
        pdf.build(elements)

        # Close MySQL connection
        cursor.close()
        cnx.close()

    def showADM(self):
        self.tabWid.setCurrentIndex(5)
        self.dlulbtn.setEnabled(False)
        self.dlarbtn.setEnabled(False)
        self.dlarbtn.hide()
        self.dlulbtn.hide()
        self.error3.setText('')


    def adlogin(self):

        un = self.tbad1.text()
        pw = self.tbad2.text()
        if len(un) == 0 or len(pw) == 0:
            self.error3.setText("Please fill-in all input!!")

        else:
            db = mysql.connector.connect(host='localhost', user='root', password='Omkar@123', db='face')
            cursor = db.cursor()
            query = "SELECT * FROM admin WHERE name = %s AND password = %s"
            params = (un, pw)
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Login Output")
                msg_box.setText("Congrats!! You login successfully!!")
                msg_box.setStandardButtons(QMessageBox.Ok)

                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStyleSheet("background-color: rgb(140, 192, 75);")
                msg_box.exec_()
                self.dlulbtn.setEnabled(True)
                self.dlarbtn.setEnabled(True)
                self.logout2.setEnabled(True)
                self.out_btn.setEnabled(True)
                self.db.setEnabled(True)
                self.grbtn.setEnabled(True)
                self.logoutbtn.setEnabled(True)
                self.grbtn.show()
                self.out_btn.show()
                self.db.show()
                self.logoutbtn.show()
                self.dlarbtn.show()
                self.dlulbtn.show()
                self.tbad1.setText('')
                self.tbad2.setText('')


            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Retry")
                msg_box.setText("Retry")
                msg_box.setStandardButtons(QMessageBox.Ok)

                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStyleSheet("background-color: rgb( 199, 5, 61);")
                msg_box.exec_()
                self.tbad1.setText('')
                self.tbad2.setText('')

    def dlul(self):
        self.dlulbtn.setEnabled(True)
        db = mysql.connector.connect(host='localhost', user='root', password='Omkar@123', db='face')
        cursor = db.cursor()
        query = "TRUNCATE TABLE demo;"
        cursor.execute(query)
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Output")
        msg_box.setText("User List Deleted")
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet("background-color: rgb(140, 192, 75);")
        msg_box.exec_()

    def Reset(self):
        email = self.tbemail.text()

        if email:
            # Check if email exists in the database
            connection = mysql.connector.connect(host='localhost',
                                                 database='face',
                                                 user='root',
                                                 password='Omkar@123')
            cursor = connection.cursor()
            query = "SELECT email FROM user WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                self.tbpass.show()
                self.Save.show()
            else:
                QMessageBox.warning(self, 'Error', 'Email not found.')

        else:
            QMessageBox.warning(self, 'Error', 'Please enter your email address.')

    def savepass(self):
        email = self.tbemail.text()
        new_password = self.tbpass.text()

        if email and new_password:
            # Update the password in the database
            connection = mysql.connector.connect(host='localhost',
                                                 database='face',
                                                 user='root',
                                                 password='Omkar@123')
            cursor = connection.cursor()
            query = "UPDATE user SET password = %s WHERE email = %s"
            cursor.execute(query, (new_password, email))


            QMessageBox.warning(self, 'Password Reset', 'Your password has been reset successfully.')
            self.tbemail.clear()
            self.tbpass.hide()
            self.Save.hide()
        else:
            QMessageBox.warning(self, 'Error', 'Please enter your email address and a new password.')
            self.tabWid.setCurrentIndex(5)


    def Fpass(self):
        self.tabWid.setCurrentIndex(6)
        self.tbpass.hide()
        self.Save.hide()


    def dlal(self):
        self.dlulbtn.setEnabled(True)
        db = mysql.connector.connect(host='localhost', user='root', password='Omkar@123', db='face')
        cursor = db.cursor()
        query = "TRUNCATE TABLE demo;"
        cursor.execute(query)
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Output")
        msg_box.setText("Attendance List Deleted")
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet("background-color: rgb(140, 192, 75);")
        msg_box.exec_()

    def lg2(self):
        self.tabWid.setCurrentIndex(0)
        self.tbad1.setText('')
        self.tbad2.setText('')
        self.dlulbtn.setEnabled(False)
        self.dlarbtn.setEnabled(False)
        self.db.hide()
        self.out_btn.hide()
        self.grbtn.hide()
        self.logoutbtn.hide()

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def signout(self):
        self.tabWid.setCurrentIndex(0)
        self.grbtn.setEnabled(False)
        self.out_btn.setEnabled(False)
        self.db.setEnabled(False)
        self.logoutbtn.setEnabled(False)
        self.grbtn.hide()
        self.out_btn.hide()
        self.db.hide()
        self.logoutbtn.hide()


    def showgr(self):
        self.tabWid.setCurrentIndex(4)
        # Create a graphics scene and view
        scene = QGraphicsScene()
        self.graphicsView.setScene(scene)
        # Create a bar chart
        chart = QChart()
        # Retrieve data from MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Omkar@123",
            database="face"
        )
        cursor = db.cursor()
        cursor.execute("SELECT name ,ct FROM  att WHERE ct> 0;")
        data = cursor.fetchall()
        db.close()

        # Create bar series and add bar sets to the series
        bar_series = QBarSeries()
        for name, ct in data:
            bar_set = QBarSet(name)
            bar_set.append(ct)
            bar_series.append(bar_set)
        chart.addSeries(bar_series)

        # Create categories for the bar chart
        categories = []
        for name, ct in data:
            categories.append(name)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)

        # Set chart title and axis labels
        chart.setTitle("Graph")
        chart.setAnimationOptions(QChart.AllAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.createDefaultAxes()

        # Create a chart view and set the chart as the scene for the graphics view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.resize(1000, 700)  # Set the size of the chart view
        self.graphicsView.setSceneRect(0, 0, 1100, 700)  # Set the scene rect of the graphics view
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(chart_view)
        scene.addItem(proxy)

    # ________________________________________read from DB____________________________________________________________________________
    def READDB(self):

        db = mysql.connector.connect(host='localhost', user='root', password='Omkar@123', db='face')
        cursor = db.cursor()
        query = "SELECT * FROM user;"
        cursor.execute(query)
        result = cursor.fetchall()
        self.tableWid.setRowCount(0)

        for row_num, row_data in enumerate(result):

            self.tableWid.insertRow(row_num)
            for column_num, col_data in enumerate(row_data):
                item = str(col_data)
                if (column_num == 0):
                    item = self.getImagLabel(col_data)
                    self.tableWid.setCellWidget(row_num, column_num, item)
                else:
                    self.tableWid.setItem(row_num, column_num, QtWidgets.QTableWidgetItem(item))

        self.tableWid.verticalHeader().setDefaultSectionSize(120)
        self.readdb2()
        db.close()

    def readdb2(self):
        db2 = mysql.connector.connect(host='localhost', user='root', password='Omkar@123', db='face')
        cursor2 = db2.cursor()
        query2 = "SELECT * FROM att"
        cursor2.execute(query2)
        result2 = cursor2.fetchall()
        self.tableWid_2.setRowCount(0)

        for row_num2, row_data2 in enumerate(result2):

            self.tableWid_2.insertRow(row_num2)
            for column_num2, col_data1 in enumerate(row_data2):
                item = str(col_data1)
                if (column_num2 == 0):
                    item = self.getImagLabel2(col_data1)
                    self.tableWid_2.setCellWidget(row_num2, column_num2, item)
                else:
                    self.tableWid_2.setItem(row_num2, column_num2, QtWidgets.QTableWidgetItem(item))

        self.tableWid_2.verticalHeader().setDefaultSectionSize(120)

    def getImagLabel(self, image1):
        imgeLabel = QtWidgets.QLabel()
        imgeLabel.setText("")
        imgeLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image1, 'jpg')
        imgeLabel.setPixmap(pixmap)
        return imgeLabel

    def getImagLabel2(self, image2):
        imgeLabel2 = QtWidgets.QLabel()
        imgeLabel2.setText("")
        imgeLabel2.setScaledContents(True)
        pixmap2 = QtGui.QPixmap()
        pixmap2.loadFromData(image2, 'jpg')
        imgeLabel2.setPixmap(pixmap2)
        return imgeLabel2

    # _______________________________________________________________________________________________________________________
    def onclick(self):
        global cap
        cap = cv2.VideoCapture(1)

        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                if frame is not None:
                    self.displayimg(frame, 1)
                else:
                    print('Frame is None')
                cv2.waitKey()
                # time.sleep(0.01)  # Add delay to reduce processing load

            if self.logic == 2:
                un = self.tb3.text()
                pw = self.tb4.text()
                em = self.tb5.text()

                if len(un) == 0 or len(pw) == 0 or len(em) == 0:
                    self.error2.setText("Please fill-in all input!!")
                else:
                    db = mysql.connector.connect(host='localhost', user='root', password='Omkar@123', db='face')
                    cursor = db.cursor()
                    Name = f'C:/Users/Omkar/Desktop/Face-Reco-Att/face 2/data/%s.jpg' % (un)


                    cv2.imwrite(Name, frame)

                    with open(Name, 'rb') as f:
                        img = f.read()
                    sql = "INSERT INTO user (name,password,email, img) VALUES (%s, %s, %s, %s)"
                    val = (un, pw, em, img)
                    cursor.execute(sql, val)
                    db.commit()

                    self.logic = 1
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setStyleSheet("background-color: rgb(140, 192, 75);")

                    msg.setWindowTitle("Success")
                    msg.setText("Image Captured Successfully")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()

                    self.tb3.setText('')
                    self.tb4.setText('')
                    self.tb5.setText('')
                    self.error2.setText('')
                    self.tabWid.setDocumentMode(True)
                    self.tabWid.setCurrentIndex(2)
                    QSizeGrip(self.size_grip)

                    cap.release()
                    cv2.destroyAllWindows()
                    self.showout()
                    self.grbtn.show()
                    self.out_btn.show()
                    self.db.show()
                    self.logoutbtn.show()

    def CAP(self):
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()

        if len(un) == 0 or len(pw) == 0 or len(em) == 0:
            self.error2.setText("Please fill-in all input!!")
        else:

            self.logic = 2

    def displayimg(self, img, window=1):
        if img is None:
            return

        qformat = QImage.Format_RGBA8888

        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.camout1.setPixmap(QPixmap.fromImage(img))
        self.camout1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def Open_Login_Tab(self):
        self.tabWid.setCurrentIndex(0)

    def Open_Reg_Tab(self):
        self.tabWid.setCurrentIndex(1)


    def showout(self):
        self.tabWid.setCurrentIndex(2)
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Omkar@123',
            database='face'
        )

        cursor = conn.cursor()

        query = "SELECT img, name FROM user;"
        cursor.execute(query)

        results = cursor.fetchall()

        self.known_face_encodings = []
        self.known_face_names = []
        # Loop through each result
        for result in results:
            # Extract the image data and name from the result
            image_data, name = result
            # Convert the binary image data to a NumPy array
            image_np = np.frombuffer(image_data, dtype=np.uint8)

            # Decode the image array into an OpenCV image
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

            # Convert the image to RGB format
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detect and encode faces in the image
            face_locations = face_recognition.face_locations(image_rgb)
            face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

            # Append the face encodings and names to the known_face_encodings and known_face_names lists
            for encoding in face_encodings:
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)

    def start_camera(self,cap):

        self.cap.open(1)


        self.timer.start(33)  # Update frame every 33 ms (approx. 30 fps)


    def stop_camera(self):
        self.cap.release()
        self.timer.stop()
        self.timer2.stop()

    def update_frame(self):
        # self.textB.setText("Loding Plese Wait")
        global date_time_string, name

        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            face_locations = face_recognition.face_locations(rgb_frame)  # Detect faces
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # Encode faces
            face_names = []

            for face_encoding in face_encodings:
                # Compare face encoding with known face encodings
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                color = (0, 255, 0)  # Default color for known faces

                # If there is a match, get the name from known_face_names list
                if True in matches:
                    matched_indices = [i for i, b in enumerate(matches) if b]
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if best_match_index in matched_indices:
                        name = self.known_face_names[best_match_index]

                    if (name != 'unknown'):
                        buttonReply = QMessageBox.question(self, 'Welcome ' + name, 'Are you Clocking In?',
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            self.NameLabel.setText(name)
                            self.StatusLabel.setText('Clocked In')
                            self.HoursLabel.setText('Measuring')
                            self.MinLabel.setText('')

                            self.Time1 = datetime.datetime.now()
                            self.stop_camera()
                            height, width, channels = frame.shape
                            rgb_image = cv2.cvtColor(frame,
                                                     cv2.COLOR_BGR2RGB)  # Convert to RGB for displaying in QLabel
                            qimage = QImage(rgb_image.data, width, height,
                                            QImage.Format_RGB888)  # Create QImage from frame data
                            self.imgLabel.setPixmap(QPixmap.fromImage(qimage))  # Display image in QLabel
                            _, img = cv2.imencode('.jpg', rgb_image)

                            connection = mysql.connector.connect(host='localhost',
                                                                 user='root',
                                                                 password='Omkar@123', database='face')

                            insert = """ INSERT INTO att (img,name,time,status,ct) VALUES (%s,%s,%s,%s,%s) """
                            ct = 0
                            data = (img.tobytes(),name, date_time_string, 'clock In', ct)
                            cursor = connection.cursor()
                            cursor.execute(insert, data)
                            connection.commit()
                            cursor.close()
                            connection.close()

                        else:
                            self.stop_camera()
                            self.NameLabel.setText(name)
                            self.MinLabel.setText('')

                else:
                    color = (0, 0, 255)  # Change color to red for unknown faces
                face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Draw rectangle around faces with respective color
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    # Draw name label above faces
                    cv2.rectangle(frame, (left, top - 30), (right, top), color, cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

            height, width, channels = frame.shape
            rgb_image = cv2.cvtColor(frame,
                                     cv2.COLOR_BGR2RGB)  # Convert to RGB for displaying in QLabel
            qimage = QImage(rgb_image.data, width, height,
                            QImage.Format_RGB888)  # Create QImage from frame data
            self.imgLabel.setPixmap(QPixmap.fromImage(qimage))  # Display image in QLabel
            _, img = cv2.imencode('.jpg', rgb_image)

    def start_camera2(self):

        self.cap.open(1)

        self.timer2.start(33)  # Update frame every 33 ms (approx. 30 fps)


    def update_frame2(self):

        global date_time_string, name, CheckOutTime, CheckInTime

        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            face_locations = face_recognition.face_locations(rgb_frame)  # Detect faces
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # Encode faces
            face_names = []

            for face_encoding in face_encodings:
                # Compare face encoding with known face encodings
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                color = (0, 255, 0)  # Default color for known faces

                # If there is a match, get the name from known_face_names list
                if True in matches:
                    matched_indices = [i for i, b in enumerate(matches) if b]
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if best_match_index in matched_indices:
                        name = self.known_face_names[best_match_index]

                    if (name != 'unknown'):
                        buttonReply = QMessageBox.question(self, 'Welcome ' + name, 'Are you Clocking Out..?',
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")

                            self.NameLabel.setText(name)
                            self.StatusLabel.setText('Clocked Out')
                            self.Time2 = datetime.datetime.now()

                            self.ElapseList(name)
                            self.TimeList2.append(datetime.datetime.now())
                            CheckInTime = self.TimeList1[-1]
                            CheckOutTime = self.TimeList2[-1]
                            self.ElapseHours = (CheckOutTime - CheckInTime)

                            self.MinLabel.setText(
                                "{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60) % 60) + 'm')

                            self.HoursLabel.setText(
                                "{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60 ** 2)) + 'h')

                            self.stop_camera()
                            height, width, channels = frame.shape
                            rgb_image = cv2.cvtColor(frame,
                                                     cv2.COLOR_BGR2RGB)  # Convert to RGB for displaying in QLabel
                            qimage = QImage(rgb_image.data, width, height,
                                            QImage.Format_RGB888)  # Create QImage from frame data

                            self.imgLabel.setPixmap(QPixmap.fromImage(qimage))  # Display image in QLabel
                            _, img = cv2.imencode('.jpg', rgb_image)

                            CheckInTime = self.TimeList1[-1]
                            CheckOutTime = self.TimeList2[-1]
                            ElapseHours = (CheckOutTime - CheckInTime)
                            connection = mysql.connector.connect(host='localhost',
                                                                 user='root',
                                                                 password='Omkar@123', database='face')

                            db_Info = connection.get_server_info()

                            cursor = connection.cursor()
                            cursor.execute("select database();")
                            record = cursor.fetchone()


                            hr = abs(self.ElapseHours.total_seconds() / 60 ** 2)
                            ct1 = round(hr)
                            # min = abs(self.ElapseHours.total_seconds() / 60) % 60
                            self.ElapseHours = (CheckOutTime - CheckInTime)

                            insert = """ INSERT INTO att (img,name,time,status,EL,ct) VALUES (%s,%s,%s,%s,%s,%s) """
                            data = (img.tobytes(), name, date_time_string, 'clock Out', ElapseHours, ct1)
                            cursor = connection.cursor()
                            cursor.execute(insert, data)
                            connection.commit()
                            cursor.close()
                            connection.close()
                        else:
                            self.NameLabel.setText(name)
                            self.StatusLabel.setText("N.A.")
                            self.HoursLabel.setText("N.A.")
                            self.stop_camera()
                else:
                    color = (0, 0, 255)  # Change color to red for unknown faces
                face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Draw rectangle around faces with respective color
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    # Draw name label above faces
                    cv2.rectangle(frame, (left, top - 30), (right, top), color, cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

            height, width, channels = frame.shape
            rgb_image = cv2.cvtColor(frame,
                                     cv2.COLOR_BGR2RGB)  # Convert to RGB for displaying in QLabel
            qimage = QImage(rgb_image.data, width, height,
                            QImage.Format_RGB888)  # Create QImage from frame data

            self.imgLabel.setPixmap(QPixmap.fromImage(qimage))  # Display image in QLabel

    def clear_label(self, event):
        self.imgLabel.clear()
        self.NameLabel.setText('')
        self.StatusLabel.setText('')
        self.HoursLabel.setText('')

    def ElapseList(self, name):
        self.TimeList1 = []
        self.TimeList2 = []

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Omkar@123",
            database="face"
        )
        cursor = connection.cursor()
        query = "SELECT status, time FROM att WHERE name = %s"
        cursor.execute(query, (name,))

        Time1 = datetime.datetime.now()
        Time2 = datetime.datetime.now()

        for row in cursor.fetchall():
            event = row[0]
            timestamp = row[1]

            if event == 'clock In':
                Time1 = datetime.datetime.strptime(timestamp.strftime('%y/%m/%d %H:%M:%S'), '%y/%m/%d %H:%M:%S')
                self.TimeList1.append(Time1)
            elif event == 'clock Out':
                Time2 = datetime.datetime.strptime(timestamp.strftime('%y/%m/%d %H:%M:%S'), '%y/%m/%d %H:%M:%S')
                self.TimeList2.append(Time2)

        cursor.close()
        connection.close()

    def Open_Db_Tab(self):
        self.tabWid.setCurrentIndex(3)
        self.READDB()

    def Log_user(self):
        un = self.tb1.text()
        pw = self.tb2.text()
        if len(un) == 0 or len(pw) == 0:
            self.error1.setText("Please fill-in all input!!")

        else:
            db = mysql.connector.connect(host='localhost', user='root', password='Omkar@123', db='face')
            cursor = db.cursor()
            query = "SELECT * FROM user WHERE name = %s AND password = %s"
            params = (un, pw)
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Login Output")
                msg_box.setText("Congrats!! You login successfully!!")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.setWindowTitle("Login Output")
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStyleSheet("background-color: rgb(140, 192, 75);")
                msg_box.exec_()
                self.tabWid.setCurrentIndex(2)
                self.tb1.setText('')
                self.tb2.setText('')
                self.showout()
                db.close()
                self.grbtn.setEnabled(True)
                self.out_btn.setEnabled(True)
                self.db.setEnabled(True)
                self.logoutbtn.setEnabled(True)
                self.logoutbtn.show()
                self.grbtn.show()
                self.out_btn.show()
                self.db.show()

            else:

                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setWindowTitle("Login Output")
                msg_box.setText("Invalid User..Register for new user!!!")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.setStyleSheet("background-color: rgb(199, 5, 61);")
                msg_box.exec_()
                self.tabWid.setCurrentIndex(1)
                self.tb1.setText('')
                self.tb2.setText('')
                self.error1.setText('')
                db.close()

def main():
    app = QApplication(sys.argv)

    splash = Splash()
    splash.show()
    splash.progres()

    window = MainApp()
    window.show()
    splash.finish(window)
    app.exec_()

if __name__ == '__main__':
    main()