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

from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from ui.styles.ListWidgetStyler import ListWidgetStyler  

class VPNDialogHandler:
    def __init__(self, layout, usdt_label, btc_label, support_label, status_label,
                 vpn_select, connect_button, premium_button, adBlocker):
        self.layout = layout
        self.usdt_label = usdt_label
        self.btc_label = btc_label
        self.support_label = support_label
        self.status_label = status_label
        self.vpn_select = vpn_select
        self.connect_button = connect_button
        self.premium_button = premium_button
        self.adBlocker = adBlocker
        self.vpn_list_widget = None

    def show_vpn_dialog(self, event):
        self.usdt_label.hide()
        self.btc_label.hide()
        self.support_label.hide()
        self.status_label.hide()
        self.vpn_select.hide()
        self.connect_button.hide()
        self.premium_button.hide()
        self.adBlocker.hide()

        self.vpn_list_widget = QListWidget()
        for index in range(self.vpn_select.count()):
            item = QListWidgetItem(self.vpn_select.itemText(index))
            item.setData(Qt.ItemDataRole.UserRole, index)  
            self.vpn_list_widget.addItem(item)

        ListWidgetStyler.apply_style(self.vpn_list_widget)

        self.layout.addWidget(self.vpn_list_widget)
        self.vpn_list_widget.itemClicked.connect(self.on_vpn_selected)

    def on_vpn_selected(self, item):
        selected_index = item.data(Qt.ItemDataRole.UserRole)
        self.vpn_select.setCurrentIndex(selected_index)

        if self.vpn_list_widget:
            self.vpn_list_widget.hide()
            self.layout.removeWidget(self.vpn_list_widget)
            self.vpn_list_widget.deleteLater()  

        self.usdt_label.show()
        self.btc_label.show()
        self.support_label.show()
        self.status_label.show()
        self.vpn_select.show()
        self.connect_button.show()
        self.premium_button.show()
        self.adBlocker.show()