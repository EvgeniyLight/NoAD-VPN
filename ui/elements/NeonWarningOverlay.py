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
    QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsOpacityEffect, QCheckBox
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPainter, QFont


class NeonWarningOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_effects()
        
    def setup_ui(self):
        # Настройки оверлея
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Основной контейнер
        container = QWidget(self)
        container.setObjectName("warningContainer")
        container.setMinimumSize(350, 300)
        
        # Стиль с цветными границами вместо теней
        container.setStyleSheet("""
            #warningContainer {
                background-color: #1a1a2e;
                border-radius: 15px;
                border: 2px solid #4e00b8;
            }
            QLabel {
                color: white;
                font-size: 14px;
                padding: 10px;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #ff00ff;
            }
            QPushButton {
                background-color: #16213e;
                color: white;
                border: 1px solid #00ffff;
                border-radius: 10px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0f3460;
                border: 1px solid #ff00ff;
            }
        """)
        
        # Элементы интерфейса
        title = QLabel("ВНИМАНИЕ", container)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Увеличиваем жирность заголовка через QFont
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(16)
        title.setFont(title_font)
        
        message = QLabel(
    "Для работы с торрентами рекомендуем использовать только премиум-локации VPN.\n\n"
    "Бесплатные серверы часто ограничивают P2P-трафик и могут блокировать "
    "соединение при обнаружении torrent-активности.\n\n"
    "Премиум-подписка обеспечит стабильный доступ без ограничений.",
    container
)
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.dont_show_checkbox = QCheckBox("Больше не показывать это уведомление")
        self.dont_show_checkbox.setChecked(False)

        button = QPushButton("Я понимаю", container)
        button.clicked.connect(self.close)
        
        # Разметка
        layout = QVBoxLayout(container)
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
        layout.addWidget(self.dont_show_checkbox)
        layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Центрируем контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container, 0, Qt.AlignmentFlag.AlignCenter)
        
    def save_dont_show_flag(self, dont_show_checkbox):
        import os, json
        from constants.constants import USER_INFO_PATH
        if os.path.exists(USER_INFO_PATH): 
            try:
                with open(USER_INFO_PATH, "r") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                data = {}
        else:
            data = {}
        data["dont_show_warning"] = dont_show_checkbox

        with open(USER_INFO_PATH, "w") as f: 
            json.dump(data, f, indent=4)

    def setup_effects(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        
    def showEvent(self, event):
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        super().showEvent(event)
        
    def close(self):
        self.save_dont_show_flag(self.dont_show_checkbox.isChecked())

        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(super().close)
        self.animation.start()
        
    def paintEvent(self, event):
        # Сплошной фон вместо прозрачного
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 220))