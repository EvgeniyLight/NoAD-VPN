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

from core.general.statistics.statistics import run_once_per_day
from core.general.AppUpdater import AppUpdater
from core.general.Data_loader import get_dont_show_update, get_dont_show_warning
from core.general.Network_utils import open_telegram_link

from ui.styles.VpnSelectorStyler import StyledComboBox
from ui.styles.PremiumButtonStyler import PremiumButtonStyler
from ui.styles.SupportLabelStyler import SupportLabelStyler
from ui.styles.CryptoLabelStyler import CryptoLabelStyler
from ui.styles.StatusLabelStyler import StatusLabelStyler 
from ui.styles.ButtonStyler import ButtonStyler 

from ui.elements.UpdateNotificationWidget import UpdateNotificationWidget
from ui.elements.Premium_manager import PremiumManager
from ui.elements.AdGuard import AdBlockerSwitch
from ui.elements.NeonWarningOverlay import NeonWarningOverlay

from ui.handlers.VPNListHandler import VPNListHandler
from ui.handlers.CopyHandler import copy_to_clipboard
from ui.handlers.VPNDialogHandler import VPNDialogHandler
from ui.handlers.VpnManager import VPNManager


from constants.constants import CURRENT_VERSION, BTC_ADDR, TETHER_TRC20_ADDR, CURRENCY

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QBrush
from PyQt6.QtCore import Qt

class VPNWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.vpnIsActive = False

        self.setWindowTitle("NoAD VPN")
        self.setFixedSize(400, 500)
        self.setStyleSheet("color: white; font-family: Arial, sans-serif;")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        run_once_per_day()
        updater = AppUpdater(CURRENT_VERSION)
        update_data = updater.check_for_updates()

        if update_data and get_dont_show_update() != True:
            update_widget = UpdateNotificationWidget(update_data)
            update_widget.exec() 

        self.support_label = QLabel()
        SupportLabelStyler.apply_style(self.support_label)
        self.support_label.linkActivated.connect(open_telegram_link) 

        self.btc_label = CryptoLabelStyler.create_crypto_label(self, CURRENCY['BTC'], BTC_ADDR)
        self.btc_label.mousePressEvent = lambda event: copy_to_clipboard(self.status_label, CURRENCY['BTC'], BTC_ADDR)

        self.usdt_label = CryptoLabelStyler.create_crypto_label(self, CURRENCY['USDT_TRC20'], TETHER_TRC20_ADDR)
        self.usdt_label.mousePressEvent = lambda event: copy_to_clipboard(self.status_label, CURRENCY['USDT_TRC20'], TETHER_TRC20_ADDR)

        self.adblocker_switch = AdBlockerSwitch()

        self.status_label = QLabel()
        StatusLabelStyler.apply_style(self.status_label, "Статус: Отключен.")

        self.connect_button = QPushButton()
        ButtonStyler.apply_neon_style(
        self.connect_button, 
        text="Подключиться",
        base_color="#7e57c2",  
        glow_color="#b388ff",   
        text_color="#ffffff",
        hover_color="#9575cd"  
        )

        self.disconnect_button = QPushButton()
        ButtonStyler.apply_neon_style(
        self.disconnect_button, 
        text="Отключиться",
        base_color="#ff4081", 
        glow_color="#ff80ab",  
        text_color="#ffffff", 
        hover_color="#f50057" 
        )

        self.disconnect_button.setEnabled(False)
        
        self.vpn_select = StyledComboBox()
        VPNListHandler.load_and_format_vpn_list(self.vpn_select)

        self.premium_button = QPushButton(" ★ Премиум ★ ")
        self.widgets_to_hide = [
            self.usdt_label,
            self.btc_label,
            self.support_label,
            self.status_label,
            self.vpn_select,
            self.premium_button,
            self.connect_button,
            self.disconnect_button,
            self.adblocker_switch
        ]
        self.widgets_to_show_on_back = self.widgets_to_hide.copy()
        self.premium_manager = PremiumManager(
            layout=self.layout,
            widgets_to_hide=self.widgets_to_hide,
            widgets_to_show_on_back=self.widgets_to_show_on_back,
            vpn_is_active_ref=lambda: self.vpnIsActive,
            connect_button=self.connect_button,
            disconnect_button=self.disconnect_button,
        )

        self.premium_button.clicked.connect(self.premium_manager.activate_premium) 
        PremiumButtonStyler.apply_style(self.premium_button)
        self.layout.addWidget(self.premium_button)

        self.layout.addWidget(self.support_label)
        self.layout.addWidget(self.btc_label)
        self.layout.addWidget(self.usdt_label)
        self.layout.addWidget(self.adblocker_switch)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.vpn_select)
        self.layout.addWidget(self.connect_button)
        self.layout.addWidget(self.disconnect_button)

        self.disconnect_button.hide()

        self.vpn_dialog_handler = None
        self.initialize_vpn_dialog_handler()

        self.setLayout(self.layout)
        
        self.vpn_manager = VPNManager(
            layout=self.layout,
            status_label=self.status_label,
            connect_button=self.connect_button,
            disconnect_button=self.disconnect_button,
            vpn_select=self.vpn_select,
            premium_button=self.premium_button,
            usdt_label=self.usdt_label,
            btc_label=self.btc_label,
            support_label=self.support_label,
            vpn_is_active_ref=self.set_vpn_is_active,
            adBlocker=self.adblocker_switch
        )

        self.connect_button.clicked.connect(self.vpn_manager.handle_connect)
        self.disconnect_button.clicked.connect(self.vpn_manager.handle_disconnect)
        
        dont_show_warning = get_dont_show_warning()
        if dont_show_warning != True:
            self.show_warning()
    
    def initialize_vpn_dialog_handler(self):
        self.vpn_dialog_handler = VPNDialogHandler(
            layout=self.layout,
            usdt_label=self.usdt_label,
            btc_label=self.btc_label,
            support_label=self.support_label,
            status_label=self.status_label,
            vpn_select=self.vpn_select,
            connect_button=self.connect_button,
            premium_button=self.premium_button,
            adBlocker=self.adblocker_switch
        )
        self.vpn_select.mousePressEvent = self.vpn_dialog_handler.show_vpn_dialog

    def set_vpn_is_active(self, value):
            self.vpnIsActive = value


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Основной градиентный фон (темный с фиолетовым оттенком)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(30, 5, 50))   # Темно-фиолетовый
        gradient.setColorAt(1, QColor(10, 0, 20))    # Почти черный
        
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Добавляем неоновые элементы на фон
        self._draw_neon_grid(painter)
        self._draw_neon_glow(painter)
    
    def _draw_neon_grid(self, painter):
        """Рисуем сетку с неоновым свечением"""
        pen = painter.pen()
        pen.setColor(QColor(100, 50, 150, 30))  # Фиолетовый с прозрачностью
        pen.setWidth(1)
        painter.setPen(pen)
        
        # Вертикальные линии
        for x in range(0, self.width(), 20):
            painter.drawLine(x, 0, x, self.height())
        
        # Горизонтальные линии
        for y in range(0, self.height(), 20):
            painter.drawLine(0, y, self.width(), y)

    def _draw_neon_glow(self, painter):
        """Добавляем эффекты неонового свечения"""
        # Горизонтальное свечение внизу
        glow_gradient = QLinearGradient(0, self.height()-50, 0, self.height())
        glow_gradient.setColorAt(0, QColor(150, 0, 255, 50))  # Фиолетовый
        glow_gradient.setColorAt(1, Qt.GlobalColor.transparent)
        
        painter.setBrush(QBrush(glow_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, self.height()-50, self.width(), 50)
        
        # Вертикальное свечение по бокам
        side_gradient = QLinearGradient(0, 0, 50, 0)
        side_gradient.setColorAt(0, QColor(150, 0, 255, 30))
        side_gradient.setColorAt(1, Qt.GlobalColor.transparent)
        
        painter.setBrush(QBrush(side_gradient))
        # Левый бок
        painter.drawRect(0, 0, 50, self.height())
        # Правый бок (зеркально)
        painter.translate(self.width(), 0)
        painter.scale(-1, 1)
        painter.drawRect(0, 0, 50, self.height())


    def show_warning(self):
        # Создаем и показываем оверлей
        self.overlay = NeonWarningOverlay(self)
        self.overlay.setGeometry(self.rect())  # Занимает всю область окна
        
        # При изменении размера окна обновляем размер оверлея
        self.resizeEvent = lambda event: self.overlay.setGeometry(self.rect())
        
        self.overlay.show()