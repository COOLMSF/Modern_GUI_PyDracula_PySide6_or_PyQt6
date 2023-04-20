# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import re
import platform
import pyqtgraph as pg

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "PyDracula - Modern GUI"
        description = "PyDracula APP - Theme with colors based on Dracula for Python."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        
        
        # init slot
        self.ui.pushButton_choose_dir.clicked.connect(self.buttonClick)
        self.ui.pushButton_export_report.clicked.connect(self.buttonClick)
        self.ui.pushButton_gen_graph.clicked.connect(self.buttonClick)
        self.ui.pushButton_start_analysis.clicked.connect(self.buttonClick)
        self.ui.pushButton_start_analysis.clicked.connect(self.buttonClick)


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        
        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            
        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")
            
            
        # self made
        if btnName == "pushButton_choose_dir":
            self.pushButton_choose_source_data_dir_clicked()
        
        if btnName == "pushButton_export_report":
            box = QMessageBox()
            box.setWindowTitle("Done")
            box.setText("Report saved to out.txt")
            box.exec()
        
        if btnName == "pushButton_start_analysis":
            print("start analysis")
            self.pushButton_start_analysis_clicked()
        
        if btnName == "pushButton_gen_graph":
            self.pushButton_gen_graph_clicked()

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
            
    def import_dir(self) -> str:
        fdlg = QFileDialog()
        fdlg.setFileMode(QFileDialog.FileMode.Directory)
        
        if fdlg.exec():
            #接受选中文件的路径，默认为列表
            filenames = fdlg.selectedFiles()
            #列表中的第一个元素即是文件路径，以只读的方式打开文件
            return filenames[0]


    def pushButton_choose_source_data_dir_clicked(self):
        dirname = self.import_dir()
        
        if len(dirname) < 1 or not os.path.isdir(dirname):
            msgBox = QMessageBox()
            msgBox.setText("Invalid directory")
            # msgBox.buttonClicked.connect(msgButtonClick)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.StandardButton.Ok:
               self.pushButton_model_train.setEnabled(True)
               # print('OK clicked')
               pass
           
        self.ui.lineEdit_choose_dir.setText(dirname)
        
    def pushButton_start_analysis_clicked(self):
        # remove blank char in list
        
        print(os.getcwd())
        
        f = open("out.txt", "r")
        lines = f.readlines()
        
        count = 0
        row = 0
        for line in lines:
            if "Language" in line or "Sum" in line or "─" in line or "━" in line:
                continue
            c = line.split('│')
            pattern = re.compile(r'.*[a-zA-Z0-9]+')
            
            for i in c:
                if not pattern.match(i):
                    continue
                else:
                    col = count % 7
                    if col == 0 and count >= 7:
                        row = row + 1
                    print(row, col, i)
                    self.ui.tableWidget.setItem(row+1, col, QTableWidgetItem(i))
                    
                    count = count + 1
                    
    def pushButton_gen_graph_clicked(self):
        # self.ui.plotWidget.clear()
        # y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2]
        # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # self.ui.plotWidget.addItem()
        # bar = pg.BarGraphItem(x = x, height = y1, width = 0.6, brush ='g')
        
        # plot = pg.plot()
        # plot.addItem(bar)
        
        # layout = QLayout()
        # self.ui.plotWidget.setLayout(layout)
        
        pass
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
