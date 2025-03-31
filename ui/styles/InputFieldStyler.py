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

from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtGui import QFont, QColor

class InputFieldStyler:
    @staticmethod
    def apply_style(input_field, placeholder_text="Введите ваш промокод...", 
                  font_family="Arial", font_size=12):
        # Настройка шрифта
        font = QFont(font_family, font_size)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 105)
        input_field.setFont(font)
        
        # Установка цвета текста и placeholder
        input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(40, 10, 70, 0.7);
                color: #e0e0ff;  /* Светло-фиолетовый текст */
                border: 2px solid #7e57c2;
                border-radius: 8px;
                padding: 10px;
                selection-background-color: #9c27b0;
                selection-color: white;
                min-height: 30px;
            }}
            QLineEdit:focus {{
                border: 2px solid #b388ff;
                background-color: rgba(50, 20, 80, 0.9);
            }}
            QLineEdit:hover {{
                border: 2px solid #9575cd;
            }}
        """)
        
        # Настройка цвета placeholder-текста
        palette = input_field.palette()
        palette.setColor(palette.ColorRole.PlaceholderText, QColor(150, 150, 180))
        input_field.setPalette(palette)
        
        input_field.setPlaceholderText(placeholder_text)
        
        # Добавляем эффект свечения при фокусе
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(156, 39, 176, 150))
        shadow.setOffset(0, 0)
        input_field.setGraphicsEffect(shadow)
        
        # Анимация для эффекта фокуса
        input_field.focusInEvent = lambda event: InputFieldStyler._on_focus(input_field, True)
        input_field.focusOutEvent = lambda event: InputFieldStyler._on_focus(input_field, False)

    @staticmethod
    def _on_focus(input_field, focused):
        shadow = input_field.graphicsEffect()
        if shadow:
            anim = QPropertyAnimation(shadow, b"color")
            anim.setDuration(300)
            
            if focused:
                anim.setStartValue(QColor(156, 39, 176, 50))
                anim.setEndValue(QColor(156, 39, 176, 150))
            else:
                anim.setStartValue(QColor(156, 39, 176, 150))
                anim.setEndValue(QColor(156, 39, 176, 50))
                
            anim.start()