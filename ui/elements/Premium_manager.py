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

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QLabel
from PyQt6.QtGui import QFont

from ui.styles.ButtonStyler import ButtonStyler 
from ui.styles.InputFieldStyler import InputFieldStyler 

from core.general.Network_utils import check_promo
from core.general.User import UserIDManager

class PremiumManager:
    def __init__(self, layout, widgets_to_hide, widgets_to_show_on_back, vpn_is_active_ref, connect_button, disconnect_button):
        self.layout = layout
        self.widgets_to_hide = widgets_to_hide
        self.widgets_to_show_on_back = widgets_to_show_on_back
        self.vpn_is_active_ref = vpn_is_active_ref

        self.connect_button = connect_button
        self.disconnect_button = disconnect_button
        
        self.input_field = None
        self.activate_button = None
        self.back_button = None
        self.spacer = None

    def activate_premium(self):
        for widget in self.widgets_to_hide:
            widget.hide()

        self.input_field = QLineEdit()
        InputFieldStyler.apply_style(self.input_field)
        self.layout.addWidget(self.input_field)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(self.spacer)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: black;")  
        self.layout.addWidget(self.status_label)

        self.activate_button = QPushButton()
        ButtonStyler.apply_neon_style(
        self.activate_button, 
        text="Активировать",
        base_color="#7e57c2",  # Фиолетовый
        glow_color="#b388ff",  # Светло-фиолетовое свечение
        text_color="#ffffff",
        hover_color="#9575cd"  # Средний фиолетовый при наведении
        )
       
        self.activate_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.activate_button.clicked.connect(self.handle_activation)
        self.layout.addWidget(self.activate_button)

        self.back_button = QPushButton("Назад")
        ButtonStyler.apply_neon_style(
        self.back_button, 
        text="Назад",
        base_color="#ff4081",  # Неоново-розовый
        glow_color="#ff80ab",  # Светло-розовое свечение
        text_color="#ffffff", 
        hover_color="#f50057"  # Ярко-розовый при наведении
        )

        self.back_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)


    def handle_activation(self):
        activation_key = self.input_field.text().strip() 
        if activation_key:
            response = check_promo(activation_key)
            if response['success'] == True:
                auth = [
                    f"{response['data']['login']}".strip(), 
                    f"{response['data']['password']}".strip()
                ]       
                user = UserIDManager()
                user.apply_auth(auth[0], auth[1])

                self.status_label.setText("Успешно активировано!")
                self.status_label.setStyleSheet("color: green;")  
            else:
                self.status_label.setText("Ошибка активации.")
                self.status_label.setStyleSheet("color: red;") 

            self.input_field.clear()  
        else:
            self.status_label.setText("Поле ввода пустое!")
            self.status_label.setStyleSheet("color: red;") 

    def go_back(self):
        if self.input_field:
            self.layout.removeWidget(self.input_field)
            self.input_field.deleteLater()
        if self.activate_button:
            self.layout.removeWidget(self.activate_button)
            self.activate_button.deleteLater()
        if self.back_button:
            self.layout.removeWidget(self.back_button)
            self.back_button.deleteLater()
        if self.spacer:
            self.layout.removeItem(self.spacer)
        if self.status_label:
            self.status_label.hide()

        for widget in self.widgets_to_show_on_back:
            widget.show()
        if self.vpn_is_active_ref():
            self.disconnect_button.show()
            self.connect_button.hide()
        else:
            self.connect_button.show()
            self.disconnect_button.hide()