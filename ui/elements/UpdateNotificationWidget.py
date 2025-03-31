# NoAD VPN - the program uses ovpn to connect to vpn and also automatically updates authorization data for public configs
# Copyright (C) 2025 Evgeniy Light
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from constants.constants import TG_LINK, BASE_SERVER_URL, CURRENT_VERSION

from core.general.AppUpdater import AppUpdater

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QCheckBox
from PyQt6.QtCore import Qt, QEventLoop, QUrl
from PyQt6.QtGui import QDesktopServices


class UpdateNotificationWidget(QWidget):
    def __init__(self, update_data, parent=None):
        super().__init__(parent)
        self.update_data = update_data
        self.init_ui()
        self.loop = QEventLoop()

    def init_ui(self):
        self.setWindowTitle("Доступно обновление")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                color: #ECF0F1;
                font-family: "Segoe UI";
                font-size: 14px;
            }
            QLabel {
                color: #ECF0F1;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #27AE60;
            }
            QPushButton, QLabel#update_button {
                background-color: #34495E;
                color: #ECF0F1;
                border: 1px solid #27AE60;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                text-align: center;
            }
            QPushButton:hover, QLabel#update_button:hover {
                background-color: #27AE60;
            }
            QPushButton:pressed, QLabel#update_button:pressed {
                background-color: #2ECC71;
            }
            QLabel#support {
                font-size: 12px;
                color: #27AE60;
            }
            QLabel#support a {
                color: #2ECC71;
                text-decoration: none;
            }
            QLabel#support a:hover {
                text-decoration: underline;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("Доступно обновление")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        update_text = QLabel(
            f"Версия: <b>{self.update_data['latest_version']}</b><br><br>"
            f"Что нового:<br>{self.update_data['changelog']}"
        )
        update_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        update_text.setWordWrap(True)
        layout.addWidget(update_text)

        update_button = QLabel(f'<a href="{BASE_SERVER_URL}" style="color: #ECF0F1; text-decoration: none;">Обновить</a>')
        update_button.setObjectName("update_button")
        update_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        update_button.setOpenExternalLinks(False)  

        def open_link(event):
            QDesktopServices.openUrl(QUrl(BASE_SERVER_URL))

        update_button.mousePressEvent = open_link
        layout.addWidget(update_button)

        cancel_button = QPushButton("Обновить позже")
        cancel_button.clicked.connect(self.on_cancel_clicked)
        layout.addWidget(cancel_button)

        self.dont_show_checkbox = QCheckBox("Больше не показывать это уведомление")
        self.dont_show_checkbox.setChecked(False)
        layout.addWidget(self.dont_show_checkbox)

        support_label = QLabel()
        support_label.setObjectName("support")
        support_label.setText(
            'Поддержка:<br>'
            f'<a href="{TG_LINK}" style="color: #2ECC71;">Мы в Telegram, где и промокоды</a>'
        )
        support_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        support_label.setOpenExternalLinks(True)
        layout.addWidget(support_label)

        self.setLayout(layout)

    def on_cancel_clicked(self):
        au = AppUpdater(CURRENT_VERSION)
        au.save_dont_show_flag(self.dont_show_checkbox.isChecked())
        self.loop.quit()
        QApplication.quit()

    def exec(self):
        self.show()
        self.loop.exec()  

    def closeEvent(self, event):
        self.loop.quit()  
        QApplication.quit() 
        event.accept()