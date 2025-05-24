from PyQt5 import QtWidgets, QtCore, QtGui

class ImageLabel(QtWidgets.QLabel):
    """自定义图片显示控件"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("border: 0px; padding: 0px; margin: 0px;")
        self.setAlignment(QtCore.Qt.AlignCenter)
        
    def paintEvent(self, event):
        """重写绘制事件"""
        if self.pixmap():
            painter = QtGui.QPainter(self)
            pixmap = self.pixmap().scaled(
                self.size(),
                QtCore.Qt.KeepAspectRatioByExpanding,
                QtCore.Qt.SmoothTransformation
            )
            # 计算绘制区域
            x = (self.width() - pixmap.width()) // 2
            y = (self.height() - pixmap.height()) // 2
            painter.drawPixmap(x, y, pixmap)
        else:
            super().paintEvent(event)



class Ui_MainWindow(object):

    # 修改后的display_image方法
    def display_image(self):
        pixmap = QtGui.QPixmap(self.image_path)
        if not pixmap.isNull():
            self.label_image.setPixmap(pixmap)  # 直接设置原始图片
            self.label_image.update()  # 强制刷新显示
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("建筑安全评估系统")
        MainWindow.resize(1000, 700)
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font: 12pt "微软雅黑";
                color: #333333;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                background: white;
            }
            QPushButton {
                font: bold 12pt "微软雅黑";
                color: white;
                background-color: #4CAF50;
                border-radius: 8px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QGroupBox {
                font: bold 14pt "微软雅黑";
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
                background-color: #ffffff;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 主布局
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)


        # 左侧区域
        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(20, 20, 20, 20)

        # 图片显示区域

        # self.label_image = QtWidgets.QLabel()
        # self.label_image.setFixedSize(600, 450)  # 固定尺寸
        # 在UI初始化时使用自定义控件
        self.label_image = ImageLabel()  # 替换原来的QLabel
        self.label_image.setFixedSize(600, 450)

        self.label_image.setStyleSheet("""
            QLabel {
                border: 2px dashed #cccccc;
                background-color: #ffffff;
                padding: 0px;               /* 移除内边距 */
                margin: 0px;                /* 移除外边距 */
            }
        """)
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        left_layout.addWidget(self.label_image)

        # 按钮区域（居中显示）
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)  # 关键：设置布局居中对齐


        self.pushButton_upload = QtWidgets.QPushButton("上传图片")
        self.pushButton_upload.setFixedSize(150, 40)
        self.pushButton_upload.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
        """)
        button_layout.addWidget(self.pushButton_upload)
        left_layout.addLayout(button_layout)

        # 右侧区域
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setSpacing(15)

        self.info_group = QtWidgets.QGroupBox("建筑描述(可选)")
        self.info_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding-top: 25px;  /* 为标题留出空间 */
            }
            QGroupBox::title {
                subcontrol-origin: content;
                subcontrol-position: top left;
                position: relative;
                left: 20px;  /* 相对左侧偏移 */
                top: -10px;  /* 相对顶部偏移 */
                background-color: #ffffff;
            }
        """)
        info_layout = QtWidgets.QFormLayout()
        info_layout.setSpacing(10)
        info_layout.setContentsMargins(20, 60, 20, 20)

        self.lineEdit_name = QtWidgets.QLineEdit()
        self.lineEdit_name.setPlaceholderText("请输入建筑名称")
        info_layout.addRow("名称：", self.lineEdit_name)

        self.lineEdit_address = QtWidgets.QLineEdit()
        self.lineEdit_address.setPlaceholderText("请输入建筑地址")
        info_layout.addRow("地址：", self.lineEdit_address)

        self.lineEdit_height = QtWidgets.QLineEdit()
        self.lineEdit_height.setPlaceholderText("请输入高度/层数")
        info_layout.addRow("高度/层数：", self.lineEdit_height)

        self.lineEdit_type = QtWidgets.QLineEdit()
        self.lineEdit_type.setPlaceholderText("请输入结构类型")
        info_layout.addRow("结构类型：", self.lineEdit_type)

        self.lineEdit_year = QtWidgets.QLineEdit()
        self.lineEdit_year.setPlaceholderText("请输入建成年代")
        info_layout.addRow("建成年代：", self.lineEdit_year)

        self.lineEdit_usage = QtWidgets.QLineEdit()
        self.lineEdit_usage.setPlaceholderText("请输入使用情况")
        info_layout.addRow("使用情况：", self.lineEdit_usage)

        self.lineEdit_repair = QtWidgets.QLineEdit()
        self.lineEdit_repair.setPlaceholderText("请输入维修记录")
        info_layout.addRow("维修记录：", self.lineEdit_repair)

        self.lineEdit_disaster = QtWidgets.QLineEdit()
        self.lineEdit_disaster.setPlaceholderText("请输入灾害记录")
        info_layout.addRow("灾害记录：", self.lineEdit_disaster)

        self.info_group.setLayout(info_layout)
        right_layout.addWidget(self.info_group)

        button_layout = QtWidgets.QHBoxLayout()
        self.pushButton_analyze = QtWidgets.QPushButton("安全分析")
        self.pushButton_analyze.setStyleSheet("""
            QPushButton {
                background-color: #ff5722;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #e64a19;
            }
        """)
        self.pushButton_analyze.setFixedSize(200, 50)
        button_layout.addWidget(self.pushButton_analyze)

        self.pushButton_save = QtWidgets.QPushButton("保存报告")
        self.pushButton_save.setStyleSheet("""
            QPushButton {
                background-color: #9e9e9e;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #757575;
            }
        """)
        self.pushButton_save.setFixedSize(150, 50)
        button_layout.addWidget(self.pushButton_save)
        right_layout.addLayout(button_layout)

        # 添加到主布局
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        #报告区域
        self.textEdit_report = QtWidgets.QTextEdit()
        self.textEdit_report.setReadOnly(True)
        self.textEdit_report.setMinimumSize(600, 450)  # 设置最小尺寸
        self.textEdit_report.setStyleSheet("""
            QTextEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 10px;
                background-color: #ffffff;
                font: 11pt "Courier New";
            }
        """)
        main_layout.addWidget(self.textEdit_report)

        MainWindow.setCentralWidget(self.centralwidget)
