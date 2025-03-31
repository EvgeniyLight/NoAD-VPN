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

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def copy_to_clipboard(status_label, currency, address):
    clipboard = QApplication.clipboard()  
    clipboard.setText(address)  

    original_status = status_label.text()
    status_label.setText(f"Статус: {currency} адрес скопирован!")
    QTimer.singleShot(2000, lambda: status_label.setText(original_status))


    