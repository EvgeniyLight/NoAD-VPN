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

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class StatusLabelStyler:
    @staticmethod
    def apply_style(label, text, font_size=18, font_weight="bold", color="#FFFFFF", alignment=Qt.AlignmentFlag.AlignBottom):
        label.setText(text)
        label.setAlignment(alignment)
        label.setStyleSheet(f"""
            font-size: {font_size}px; 
            font-weight: {font_weight}; 
            color: {color};
        """)