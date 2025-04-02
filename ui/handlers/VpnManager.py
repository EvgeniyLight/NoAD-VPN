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

from core.general.Network_utils import get_sitekey, check_internet_connection
from core.general.Vpn_manager import disconnect_vpn
from core.general.ConfigManager import ConfigManager
from core.general.VPNConnectionThread import VPNConnectionThread

from ui.elements.Captcha import CaptchaWidget
from ui.handlers.ConnectionHandler import ConnectionHandler

from PyQt6.QtCore import QTimer


class VPNManager:
    def __init__(self, layout, status_label, connect_button, disconnect_button, vpn_select, premium_button,
                 usdt_label, btc_label, support_label, vpn_is_active_ref, adBlocker):
        self.layout = layout
        self.status_label = status_label
        self.connect_button = connect_button
        self.disconnect_button = disconnect_button
        self.vpn_select = vpn_select
        self.premium_button = premium_button
        self.usdt_label = usdt_label
        self.btc_label = btc_label
        self.support_label = support_label
        self.adBlocker = adBlocker

        self.vpnIsActive = vpn_is_active_ref
        self.captcha_widget = None
        self.connection_handler = None
        self.vpn_thread = None

        self.animation_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_status)

    def animate_status(self):
        dots = "." * (self.animation_index % 3 + 1)
        self.status_label.setText(f"Статус: Подключение{dots}")
        self.animation_index += 1

    def handle_connect(self):
        self.connect_button.hide()
        self.premium_button.hide()

        if not check_internet_connection():
            self.status_label.setText("Статус: Нет доступа в интернет.")
            self.connect_button.show()
            self.premium_button.show()
            return

        self.animation_index = 0
        self.timer.start(500)  
        
        selected_vpn = self.vpn_select.currentData()

        cm = ConfigManager()
        isAvaible = cm.checking_VPN_upToDate(selected_vpn)
        self.connection_handler = ConnectionHandler(self)

        if isAvaible:
            self.vpn_thread = VPNConnectionThread(selected_vpn)
            self.vpn_thread.connection_finished.connect(self.connection_handler.on_connection_finished)
            self.vpn_thread.connection_failed.connect(self.connection_handler.on_connection_failed)
            self.vpn_thread.start()
            self.vpnIsActive(True)
            self.vpn_select.setEnabled(False)

        elif isAvaible is None:
            vpn_info = cm.read_vpn_info(selected_vpn)
            url = vpn_info['link']
            if url == 'SKIP':
                self.status_label.setText("Статус: Подключение отменено.")
                self.connect_button.show()
                self.premium_button.show()
                self.timer.stop() 
                return  
                
            isConfigAuth = vpn_info['isConfigAuth']
            login = cm.generate_random_string(11)
            password = login
            sitekey = get_sitekey(url)

            self.captcha_widget = CaptchaWidget(
                sitekey=sitekey,
                login=login,
                password=password,
                url=url,
                isConfigAuth=isConfigAuth
            )

            self.layout.addWidget(self.captcha_widget)

            self.usdt_label.hide()
            self.btc_label.hide()
            self.support_label.hide()
            self.status_label.hide()
            self.vpn_select.hide()
            self.premium_button.hide()
            self.adBlocker.hide()

            self.captcha_widget.request_success.connect(
                lambda: self.update_vpn_hide_captcha(selected_vpn, login, password)
            )
            self.captcha_widget.back_requested.connect(self.handle_captcha_back)
            self.vpnIsActive(True)
            self.vpn_select.setEnabled(False)

    def handle_disconnect(self):
        disconnect_vpn()
        self.status_label.setText("Статус: Отключен.")
        self.disconnect_button.hide()
        self.connect_button.show()
        self.vpnIsActive(False)
        self.vpn_select.setEnabled(True)

    def update_vpn_hide_captcha(self, selected_vpn, login, password):
        cm = ConfigManager()
        self.connection_handler = ConnectionHandler(self)

        cm.update_vpn_info(selected_vpn, login, password)

        self.vpn_thread = VPNConnectionThread(selected_vpn)
        self.vpn_thread.connection_finished.connect(self.connection_handler.on_connection_finished)
        self.vpn_thread.connection_failed.connect(self.connection_handler.on_connection_failed)
        self.vpn_thread.start()

        self.captcha_widget.hide()

        self.usdt_label.show()
        self.btc_label.show()
        self.support_label.show()
        self.status_label.show()
        self.vpn_select.show()
        self.premium_button.show()
        self.adBlocker.show()

    def handle_captcha_back(self):
        if self.timer.isActive():
            self.timer.stop()
            self.animation_index = 0

        self.usdt_label.show()
        self.btc_label.show()
        self.support_label.show()
        self.status_label.show()
        self.vpn_select.show()
        self.premium_button.show()
        self.adBlocker.show()
        
        if self.captcha_widget:
            self.layout.removeWidget(self.captcha_widget)
            self.captcha_widget.deleteLater()
            self.captcha_widget = None
        
        self.vpnIsActive(False)
        self.connect_button.show()
        self.vpn_select.setEnabled(True)
        self.status_label.setText("Статус: Отключен.")