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

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QCheckBox
from PyQt6.QtGui import QPainter, QColor, QPen, QConicalGradient
from PyQt6.QtCore import Qt, QTimer, QRectF, pyqtSignal, QObject
from threading import Thread
from core.general.AdGuard import activate_deactivation, already_working

class LoadingSpinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_angle)
        self.setFixedSize(75, 37)
        
    def update_angle(self):
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(10, 5, 55, 27)  # Область для рисования
        
        gradient = QConicalGradient(rect.center(), self.angle)
        gradient.setColorAt(0, QColor(255, 0, 255, 150))
        gradient.setColorAt(0.5, QColor(0, 255, 255, 200))
        gradient.setColorAt(1, QColor(255, 0, 255, 150))
        
        pen = QPen(gradient, 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        start_angle = self.angle * 16
        span_angle = 120 * 16  
        painter.drawArc(rect, start_angle, span_angle)
        
        glow_pen = QPen(QColor(200, 200, 255, 50), 8)
        painter.setPen(glow_pen)
        painter.drawArc(rect.adjusted(-2, -2, 2, 2), start_angle, span_angle)

class AdBlockerSwitch(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.signals = ActivationSignals()
        self.signals.finished.connect(self.on_activation_finished)

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)  
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout)

        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Shape.NoFrame)
        self.frame.setStyleSheet("""
        QFrame {
                background-color: rgba(25, 5, 45, 0.7);
                border: 2px solid #9c27b0;
                border-radius: 10px;
            }
        """)
        
        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(15, 10, 15, 10)
        self.frame.setLayout(frame_layout)
        layout.addWidget(self.frame, stretch=1) 
        
        label = QLabel("AdBlocker")
        label.setStyleSheet("""
            QLabel {
                font-size: 21px;
                font-weight: bold;
                color: #e0e0ff;
            }
        """)
        frame_layout.addWidget(label) 
        
        frame_layout.addStretch()

        self.switch = QCheckBox()
        self.switch.setFixedSize(75, 37)
        self.switch.setStyleSheet("""
            QCheckBox {
                background-color: #ff4d4d; 
                border-radius: 18px;
                padding: 3px;
                border: 1px solid #ff6464;
            }
            QCheckBox::indicator {
                width: 31px;
                height: 31px;
                border-radius: 15px;
                background-color: white;
                border: none;
            }
            QCheckBox::indicator:checked {
                margin-left: 37px;
            }
            QCheckBox:checked {
                background-color: #64ff64;
                border: 1px solid #00ff00;
            }
        """)
        frame_layout.addWidget(self.switch) 
        self.switch.stateChanged.connect(self.on_switch_toggled)

        self.loading_spinner = LoadingSpinner(self.frame)
        frame_layout.addWidget(self.loading_spinner)
        self.loading_spinner.hide()

        
        if already_working():
            self.switch.setChecked(True)  
            print("AdBlocker уже активен")


    def on_switch_toggled(self, state):
        self.switch.setEnabled(False)  
        self.show_loading_animation(True)  
        self.run_activation(state)

    def show_loading_animation(self, show):
        if show:
            self.switch.hide()
            self.loading_spinner.show()
            self.loading_spinner.timer.start(30)
        else:
            self.loading_spinner.timer.stop()
            self.loading_spinner.hide()
            self.switch.show()
            self.switch.setEnabled(True)

    def run_activation(self, state):
        self.show_loading_animation(True)
        
        thread = Thread(
            target=self._execute_activation,
            args=(state,)
        )
        thread.daemon = True  
        thread.start()

    def _execute_activation(self, state):
        if state == Qt.CheckState.Checked.value:
            result = activate_deactivation("set") or True  
        else:
            result = activate_deactivation("reset") or True  
        self.signals.finished.emit(result)

    def on_activation_finished(self, result):
        self.show_loading_animation(False)
        if result is False:
            self.switch.setChecked(not self.switch.isChecked())
        
class ActivationSignals(QObject):
    finished = pyqtSignal(bool)
