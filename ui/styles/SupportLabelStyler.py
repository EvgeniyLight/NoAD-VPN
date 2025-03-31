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

from constants.constants import TG_LINK

from PyQt6.QtCore import Qt


class SupportLabelStyler:
    @staticmethod
    def apply_style(label):
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setText(f'Поддержка:<br><a href="{TG_LINK}" style="color: #00FFFF;">Мы в Telegram, где и промокоды</a>')
        label.setOpenExternalLinks(False)  
        label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            background-color: transparent; 
            color: #FFFFFF;
        """)