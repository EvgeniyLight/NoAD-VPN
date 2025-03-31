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

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QPoint
from PyQt6.QtGui import (QFont, QColor, QPainter, QLinearGradient, 
                         QPen, QBrush, QConicalGradient)
from PyQt6.QtWidgets import (QPushButton, QGraphicsDropShadowEffect, 
                            QStyle, QStyleOptionButton)


class PremiumButtonStyler:
    @staticmethod
    def apply_style(button, text="PREMIUM"):
        button.setMinimumHeight(45)  
       
        font = QFont("Arial", 12)
        font.setBold(True)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 110)
        button.setFont(font)
        button.setText(text)
        
        button._base_color = QColor("#9c27b0")  
        button._glow_color = QColor("#e91e63")  
        button._text_color = QColor("#ffffff")    
        button._hover_color = QColor("#ffeb3b")   
        
        button.setGraphicsEffect(None)
        
        shadow = QGraphicsDropShadowEffect(button)
        shadow.setBlurRadius(15)
        shadow.setColor(button._glow_color)
        shadow.setOffset(0, 0)
        button.setGraphicsEffect(shadow)
        
        pulse_anim = QPropertyAnimation(shadow, b"blurRadius", button)
        pulse_anim.setDuration(2000)
        pulse_anim.setLoopCount(-1)
        pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        pulse_anim.setStartValue(15)
        pulse_anim.setEndValue(25)
        
        button._shadow = shadow
        button._pulse_anim = pulse_anim
        
        button.paintEvent = lambda e: PremiumButtonStyler._paint_button(button, e)
        pulse_anim.start()
        
        button.enterEvent = lambda e: PremiumButtonStyler._on_hover(button, True)
        button.leaveEvent = lambda e: PremiumButtonStyler._on_hover(button, False)

    @staticmethod
    def _paint_button(button, event):
        painter = QPainter(button)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        opt = QStyleOptionButton()
        button.initStyleOption(opt)
        
        gradient = QLinearGradient(0, 0, button.width(), button.height())
        gradient.setColorAt(0, button._base_color)
        gradient.setColorAt(1, button._glow_color)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(opt.rect, 8, 8)
        
        if opt.state & QStyle.StateFlag.State_MouseOver:
            glow_gradient = QLinearGradient(0, 0, button.width(), button.height())
            glow_gradient.setColorAt(0, QColor(255, 0, 255, 0))
            glow_gradient.setColorAt(1, QColor(0, 255, 0, 255))
            
            painter.setPen(QPen(glow_gradient, 3))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(opt.rect.adjusted(1, 1, -1, -1), 8, 8)
        
        painter.setPen(QPen(button._text_color))
        painter.drawText(opt.rect, Qt.AlignmentFlag.AlignCenter, button.text())

    @staticmethod
    def _on_hover(button, hover):
        if not hasattr(button, '_shadow'):
            return
            
        color_anim = QPropertyAnimation(button._shadow, b"color", button)
        color_anim.setDuration(300)
        color_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if hover:
            color_anim.setStartValue(button._glow_color)
            color_anim.setEndValue(button._hover_color)
        else:
            color_anim.setStartValue(button._hover_color)
            color_anim.setEndValue(button._glow_color)
            
        color_anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)