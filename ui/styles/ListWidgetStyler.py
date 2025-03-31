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

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QVariantAnimation, pyqtProperty
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QListWidget

class ListWidgetStyler:
    @staticmethod
    def apply_style(list_widget):
        list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        list_widget.setStyleSheet("""
            QListWidget {
                background-color: #121212;
                border: 1px solid #333;
                border-radius: 4px;
                outline: none;
            }
            
            QListWidget::item {
                height: 50px;
                margin: 2px;
                background: #1E1E1E;
                border-radius: 3px;
                color: #EEE;
                border: 1px solid transparent;
            }
            
            QListWidget::item:hover {
                background: #2A2A2A;
                border: 1px solid #9C27B0;
            }
            
            QListWidget::item:selected {
                background: #9C27B0;
                color: white;
            }
            
            QScrollBar:vertical {
                background: #1E1E1E;
                width: 8px;
            }
            
            QScrollBar::handle:vertical {
                background: #9C27B0;
                min-height: 20px;
                border-radius: 4px;
            }
        """)
        
        ListWidgetAnimator.setup_animations(list_widget)

class ListWidgetAnimator:
    @staticmethod
    def setup_animations(list_widget):
        class AnimatedItem:
            def __init__(self, item):
                self.item = item
                self._bg_color = QColor("#1E1E1E")
                
                self.hover_anim = QVariantAnimation()
                self.hover_anim.setDuration(200)
                self.hover_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
                self.hover_anim.valueChanged.connect(self.update_color)
                
            @pyqtProperty(QColor)
            def bgColor(self):
                return self._bg_color
                
            @bgColor.setter
            def bgColor(self, color):
                self._bg_color = color
                self.item.setBackground(color)
                
            def update_color(self, color):
                self.bgColor = color
                
            def start_hover_anim(self, hover):
                if hover:
                    self.hover_anim.setStartValue(QColor("#1E1E1E"))
                    self.hover_anim.setEndValue(QColor("#2D2D2D"))
                else:
                    self.hover_anim.setStartValue(QColor("#2D2D2D"))
                    self.hover_anim.setEndValue(QColor("#1E1E1E"))
                self.hover_anim.start()
        
        original_method = list_widget.__class__.itemFromIndex
        
        def patched_itemFromIndex(self, index):
            item = original_method(self, index)
            if not hasattr(item, '_animator'):
                item._animator = AnimatedItem(item)
            return item
            
        list_widget.__class__.itemFromIndex = patched_itemFromIndex
        
        def enter_event(event):
            item = list_widget.itemAt(event.pos())
            if item and hasattr(item, '_animator'):
                item._animator.start_hover_anim(True)
            return QListWidget.mouseMoveEvent(list_widget, event)
            
        def leave_event(event):
            for i in range(list_widget.count()):
                item = list_widget.item(i)
                if hasattr(item, '_animator'):
                    item._animator.start_hover_anim(False)
            return QListWidget.leaveEvent(list_widget, event)
            
        list_widget.mouseMoveEvent = enter_event
        list_widget.leaveEvent = leave_event