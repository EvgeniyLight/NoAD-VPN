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

class ConnectionHandler:
    def __init__(self, vpn_window):
        self.vpn_window = vpn_window

    def on_connection_finished(self):
        self.vpn_window.premium_button.show()
        self.vpn_window.timer.stop()
        self.vpn_window.status_label.setText("Статус: Подключено!")
        self.vpn_window.disconnect_button.show()
        self.vpn_window.disconnect_button.setEnabled(True)

    def on_connection_failed(self, error_message):
        self.vpn_window.premium_button.show()
        self.vpn_window.timer.stop()
        if error_message == "error connecting":
            self.vpn_window.status_label.setText("Статус: Ошибка подключения.")
        else:
            self.vpn_window.status_label.setText(f"Статус: Ошибка: {error_message}")
        self.vpn_window.vpn_select.setEnabled(True)
        self.vpn_window.connect_button.show()