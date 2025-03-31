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

from PyQt6.QtWidgets import QComboBox

from core.general.Data_loader import load_vpn_list

class VPNListHandler:
    @staticmethod
    def load_and_format_vpn_list(vpn_select: QComboBox):
        vpn_list = load_vpn_list()

        for vpn in vpn_list:
            display_text = f"{vpn['location']}"
            if vpn.get('isGold') == "True":
                display_text += " ★ Premium Location ★"
        
            vpn_select.addItem(display_text, vpn["ovpn"])