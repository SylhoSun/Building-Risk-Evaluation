import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from ui_main import Ui_MainWindow
from llm_analyzer import analyze_building  # 调用 Gemini API 的分析模块
from report_saver import save_report

class MainApp(Ui_MainWindow):
    def __init__(self, window):
        self.window = window
        super().setupUi(window)  # 初始化 UI
        self.image_path = None

        # 按钮绑定事件
        self.pushButton_upload.clicked.connect(self.upload_image)
        self.pushButton_analyze.clicked.connect(self.analyze_image)
        self.pushButton_save.clicked.connect(self.save_report)

    def upload_image(self):
        """上传图片并显示在界面上"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.window, "选择街景图片", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.image_path = file_path
            # 显示图片（缩放以适应显示区域）
            pixmap = QPixmap(file_path).scaled(
                400, 300, aspectRatioMode=1, transformMode=1  # 保持比例缩放
            )
            self.label_image.setPixmap(pixmap)

    def analyze_image(self):
        """调用 Gemini API 分析图片并生成报告"""
        if not self.image_path:
            QMessageBox.warning(self.window, "警告", "请先上传图片")
            return

        # 收集用户输入的描述信息
        description = {
            "name": self.lineEdit_name.text().strip() or "未填写",
            "address": self.lineEdit_address.text().strip() or "未填写",
            "height": self.lineEdit_height.text().strip() or "未填写",
            "type": self.lineEdit_type.text().strip() or "未填写",
            "built_year": self.lineEdit_year.text().strip() or "未填写",
            "usage": self.lineEdit_usage.text().strip() or "未填写",
            "repair_history": self.lineEdit_repair.text().strip() or "未填写",
            "disaster_history": self.lineEdit_disaster.text().strip() or "未填写",
        }

        try:
            # 调用 LLM 分析模块
            report = analyze_building(self.image_path, description)

            # 检查返回值是否为错误信息
            if isinstance(report, str) and "错误" in report:
                raise ValueError(report)  # 将错误信息重新抛出

            # 显示分析结果
            self.textEdit_report.setPlainText(report)

        except ValueError as e:
            # 参数验证错误
            self.show_error(f"输入错误：{e}")

        except Exception as e:
            # 其他未知错误
            self.show_error(f"分析失败：{e}")
            print(f"[未知错误] {e}")  # 打印详细日志便于调试

    def show_error(self, message):
        """弹窗+报告框显示分析失败信息"""
        QMessageBox.critical(self.window, "分析失败", message)
        self.textEdit_report.setPlainText("分析失败，请检查日志。")

    def save_report(self):
        """保存评估报告"""
        content = self.textEdit_report.toPlainText()
        if not content:
            QMessageBox.warning(self.window, "警告", "没有报告内容可保存")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self.window, "保存评估报告", "", "Markdown Files (*.md);;Text Files (*.txt)"
        )
        if save_path:
            try:
                save_report(save_path, content)  # 调用保存函数
                QMessageBox.information(self.window, "提示", "报告保存成功")
            except Exception as e:
                QMessageBox.critical(self.window, "保存失败", f"无法保存报告：{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    mainApp = MainApp(window)
    window.show()
    sys.exit(app.exec_())