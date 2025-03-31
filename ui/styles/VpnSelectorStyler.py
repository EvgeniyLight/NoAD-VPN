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

# from PyQt6.QtWidgets import QComboBox, QApplication
# from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QBrush
# from PyQt6.QtCore import Qt, QTimer, QPointF

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QLinearGradient, QRadialGradient
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF, QPoint
import random
import math

class StyledComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hovered = False
        self._particles = []
        self._mouse_pos = QPointF()
        self._glow_intensity = 0
        
        self.setMinimumHeight(40)  
        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(30)
        
        self.setStyleSheet("""
            StyledComboBox {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(50, 15, 80, 0.8),
                    stop:1 rgba(30, 5, 50, 0.9)
                );
                color: #f0e4ff;
                border: 1px solid #9c4dff;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 120px;
                selection-background-color: #b388ff;
            }
            StyledComboBox:hover {
                border: 1px solid #d1b3ff;
            }
            StyledComboBox::drop-down {
                border: none;
                width: 20px;
                background: transparent;
            }
            QAbstractItemView {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 20, 90, 0.95),
                    stop:1 rgba(40, 10, 70, 0.95)
                );
                border: 1px solid #7e57c2;
                selection-background-color: #9c27b0;
            }
        """)

    def enterEvent(self, event):
        self._hovered = True
        self._mouse_pos = event.position()
        self.generate_particles()

    def leaveEvent(self, event):
        self._hovered = False

    def mouseMoveEvent(self, event):
        self._mouse_pos = event.position()
        if self._hovered and random.random() > 0.5:
            self.generate_particles()

    def generate_particles(self):
        shapes = ['sparkle', 'micro_circle', 'soft_glow']
        for _ in range(random.randint(1, 2)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.1, 0.8)
            
            self._particles.append({
                'pos': QPointF(self._mouse_pos),
                'velocity': QPointF(math.cos(angle)*speed, math.sin(angle)*speed),
                'size': random.uniform(1.5, 3.5),
                'shape': random.choice(shapes),
                'life': random.uniform(0.4, 0.9),
                'max_life': random.uniform(0.8, 1.2),
                'color': self.generate_particle_color(),
                'glow': random.uniform(0.3, 0.7)
            })

    def generate_particle_color(self):
        hue = random.uniform(250, 320)  
        return QColor.fromHsvF(
            hue/360,
            random.uniform(0.6, 0.8),
            random.uniform(0.9, 1.0),
            random.uniform(0.2, 0.4)
        )

    def update_particles(self):
        for p in self._particles:
            p['life'] -= 0.01  
            p['velocity'] *= 0.75 
        
        self._particles = [
            p for p in self._particles 
            if p['life'] > 0.001 and  
            self.rect().contains(p['pos'].toPoint())
        ]

    def update_glow(self):
        if self._hovered:
            self._glow_intensity = min(1.0, self._glow_intensity + 0.05)
        else:
            self._glow_intensity = max(0.0, self._glow_intensity - 0.03)

    def update_animations(self):
        self.update_glow()
        self.update_particles()
        if self._hovered or self._particles or self._glow_intensity > 0:
            self.update()

    def draw_particle(self, painter, particle):
        path = QPainterPath()
        size = particle['size']
        center = particle['pos']
        life_ratio = particle['life'] / particle['max_life']
        
        if particle['shape'] == 'sparkle':
            for i in range(4):
                angle = math.pi * i / 2
                p1 = center + QPointF(math.cos(angle)*size, math.sin(angle)*size)
                p2 = center + QPointF(math.cos(angle+math.pi/4)*size*0.3, 
                                    math.sin(angle+math.pi/4)*size*0.3)
                if i == 0:
                    path.moveTo(p1)
                else:
                    path.lineTo(p1)
                path.lineTo(p2)
            path.closeSubpath()
            
        elif particle['shape'] == 'micro_circle':
            path.addEllipse(center, size/2, size/2)
            
        else:  
            gradient = QRadialGradient(center, size*2)
            color = QColor(particle['color'])
            color.setAlphaF(color.alphaF() * life_ratio)
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, QColor(0,0,0,0))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center, size, size)
            return

        color = QColor(particle['color'])
        color.setAlphaF(color.alphaF() * life_ratio)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._glow_intensity > 0:
            rect = self.rect()
            gradient = QLinearGradient(
                float(rect.left()), float(rect.top()),
                float(rect.right()), float(rect.bottom())
            )
            gradient.setColorAt(0, QColor(180, 130, 255, int(30*self._glow_intensity)))
            gradient.setColorAt(1, QColor(100, 70, 255, int(50*self._glow_intensity)))

            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 6, 6)

        for p in sorted(self._particles, key=lambda x: -x['pos'].y()):
            self.draw_particle(painter, p)