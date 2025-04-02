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

from PyQt6.QtWidgets import (
     QVBoxLayout, QWidget, QPushButton, QLabel, QProgressBar
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QObject, QPropertyAnimation, QEasingCurve, pyqtSlot, QThread, pyqtSignal
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtGui import QColor, QPalette, QPainter

import requests, os, json
from bs4 import BeautifulSoup

from core.general.Network_utils import generate_user_agent
from constants.constants import CONFIG_DIR_PATH, VPN_INFO_PATH

class Bridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None

    @pyqtSlot(str)
    def handle_token(self, token):
        self.token = token
        self.parent().handle_token(token)
    

class RequestWorker(QThread):
    finished = pyqtSignal(int, str)

    def __init__(self, url, data, headers, login, isConfigAuth):
        super().__init__()
        self.url = url
        self.data = data
        self.headers = headers
        self.login = login
        self.isConfigAuth = isConfigAuth

    def abort(self):
            self._abort = True
            self.terminate()

    def run(self):
        try:
            download_link = self.perform_post_request()
            if download_link and self.isConfigAuth == 'True':
                expected_login_part = f"user={self.login}-vpnjantit.com"
                if expected_login_part in download_link:
                    success, message = self.download_file(download_link, self.url)
                    self.finished.emit(200 if success else -1, message)
                else:
                    self.finished.emit(200, "Ссылка не содержит корректный логин.")
            else:
                self.finished.emit(200, "Ссылка для скачивания не найдена.")
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            self.finished.emit(-1, f"Ошибка запроса: {str(e)}")

    def perform_post_request(self):
        response = requests.post(self.url, data=self.data, headers=self.headers)        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            button = soup.find('a', class_='btn btn-primary d-block px-7 mb-4')
            if button and 'href' in button.attrs:
                return button['href']
        
        return None

    def download_file(self, download_link, link):
        try:
            full_download_url = requests.compat.urljoin(self.url, download_link)
            
            file_name = download_link.split('/')[-1]
            file_name = file_name[:40]
            
            if not file_name.endswith('.ovpn'):
                file_name += '.ovpn'
            
            file_path = os.path.join(CONFIG_DIR_PATH, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            with requests.get(full_download_url, stream=True) as file_response:
                file_response.raise_for_status()

                with open(file_path, 'wb') as file:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        file.write(chunk)
            self.update_vpn_info(link, file_name)
            return True, f"Файл успешно скачан: {file_path}"

        except Exception as e:
            print(f"Ошибка при скачивании файла: {str(e)}")
            return False, f"Ошибка при скачивании файла: {str(e)}"

    def update_vpn_info(self, link, ovpn_file_name):
        try:
            with open(VPN_INFO_PATH, 'r', encoding='utf-8') as file:
                vpn_info = json.load(file)            
            updated = False
            for entry in vpn_info:
                if entry.get('link') == link:
                    entry['ovpn'] = ovpn_file_name
                    updated = True
            if updated:
                with open(VPN_INFO_PATH, 'w', encoding='utf-8') as file:
                    json.dump(vpn_info, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при обновлении информации: {str(e)}")

class CaptchaWidget(QWidget):
    request_success = pyqtSignal()  
    back_requested = pyqtSignal()

    def __init__(self, sitekey, login, password, url, isConfigAuth, parent=None):
        super().__init__(parent)
        self.sitekey = sitekey
        self.login = login
        self.password = password
        self.url = url
        self.isConfigAuth = isConfigAuth
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(20, 20, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 255))
        self.setPalette(palette)
        
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        self.browser = QWebEngineView()
        self.bridge = Bridge(self)
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    background-color: #121212;
                    margin: 0;
                    padding: 10px;
                }}
                .cf-turnstile {{
                    margin: 20px auto;
                }}
                #success-message {{
                    color: #9C27B0;
                    text-align: center;
                    font-family: Arial;
                    margin-top: 20px;
                }}
            </style>
            <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        </head>
        <body>
            <div class="cf-turnstile" data-sitekey="{self.sitekey}" data-theme="dark" data-callback="onCaptchaSuccess"></div>
            <div id="success-message"></div>

            <script>
                window.onCaptchaSuccess = function(token) {{
                    if (window.bridge) {{
                        window.bridge.handle_token(token);
                    }} else {{
                        console.error('Мост не инициализирован');
                    }}
                }};
                document.addEventListener("DOMContentLoaded", function() {{
                    new QWebChannel(qt.webChannelTransport, function(channel) {{
                        window.bridge = channel.objects.bridge;
                    }});
                }});
            </script>
        </body>
        </html>
        """
        self.browser.setHtml(html_content, QUrl(self.url))
    
        self.submit_button = QPushButton("Подтвердить")
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.send_post_request)
        self.submit_button.hide()
        self.style_button(self.submit_button, "#9C27B0", "#BA68C8")
        
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.on_back_clicked)
        self.style_button(self.back_button, "#333", "#555")
        
        self.status_label = QLabel("Статус: Ожидание решения капчи...")
        self.status_label.setWordWrap(True)
        self.status_label.setMaximumHeight(50)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #BA68C8;
                font-size: 14px;
                padding: 5px;
                border-radius: 4px;
                background-color: rgba(30, 30, 40, 0.7);
            }
        """)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #9C27B0;
                border-radius: 3px;
                text-align: center;
                background: #121212;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9C27B0, stop:1 #BA68C8
                );
                border-radius: 2px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.setMinimumSize(375, 450)
        self.setMaximumSize(375, 450)
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                border: 1px solid #9C27B0;
                border-radius: 5px;
            }
        """)
        
        self.token = None
        self.worker = None
    
    def style_button(self, button, base_color, hover_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {base_color};
            }}
            QPushButton:disabled {{
                background-color: #333;
                color: #888;
            }}
        """)

    
    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setPen(QColor("#9C27B0"))
        painter.setBrush(QColor("#121212"))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 5, 5)
        
        for i in range(1, 4):
            color = QColor(156, 39, 176, 50 - i*10)
            painter.setPen(color)
            painter.drawRoundedRect(self.rect().adjusted(i, i, -i, -i), 5, 5)


    def handle_token(self, token):
        self.token = token
        self.status_label.setText(f"Статус: Токен получен - {token}")
        self.submit_button.setEnabled(True)
        self.submit_button.show()

    def send_post_request(self):
        if not self.token:
            self.status_label.setText("Ошибка: Токен не получен!")
            return
        
        self.submit_button.hide()

        data = {
            "user": self.login,
            "pass": self.password,
            "cf-turnstile-response": self.token,
        }
        h = generate_user_agent()
        headers = {
            "User-Agent": f"{h}",
            "Referer": self.url,
        }

        self.progress_bar.setVisible(True)
        self.submit_button.setEnabled(False)
        self.status_label.setText("Статус: Отправка запроса...")

        self.worker = RequestWorker(self.url, data, headers, self.login, self.isConfigAuth)
        self.worker.finished.connect(self.on_request_finished)
        self.worker.start()

    def on_request_finished(self, status_code, message):
        self.progress_bar.setVisible(False)
        self.submit_button.setEnabled(True)
        self.status_label.setText(f"Статус: {message}")
        if status_code == 200:
            self.request_success.emit() 

    def on_back_clicked(self):
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.abort()
            
        self.browser.setHtml("")  
        self.token = None
        self.back_requested.emit()
