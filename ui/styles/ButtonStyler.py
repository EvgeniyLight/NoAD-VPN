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
from PyQt6.QtGui import QColor

class ButtonStyler:
    @staticmethod
    def apply_neon_style(button, text, 
                        base_color="#7e57c2",
                        glow_color="#b388ff",
                        text_color="#ffffff",
                        hover_color="#9575cd",
                        padding="12px 24px",
                        border_radius="6px",
                        font_size="16px"):
        
        button.setText(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({hex_to_rgb(base_color)}, 0.3);
                color: {text_color};
                padding: {padding};
                border-radius: {border_radius};
                font-size: {font_size};
                font-weight: 500;
                border: 1px solid {base_color};
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: rgba({hex_to_rgb(hover_color)}, 0.5);
                border: 1px solid {glow_color};
            }}
            QPushButton:pressed {{
                background-color: rgba({hex_to_rgb(base_color)}, 0.7);
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(glow_color))
        shadow.setOffset(0, 0)
        button.setGraphicsEffect(shadow)

def hex_to_rgb(hex_color):
    """Конвертирует hex в rgb строку"""
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))