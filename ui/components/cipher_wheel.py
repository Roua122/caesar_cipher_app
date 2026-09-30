"""
Interactive Animated Caesar Cipher Wheel Widget.
Renders concentric outer (Plaintext) and inner (Ciphertext) alphabet rings.
Smoothly animates rotation of the inner wheel when the shift key 'k' changes.
"""

import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QConicalGradient
from ui.assets.theme import AppColors


class CipherWheelWidget(QWidget):
    """Custom Animated Wheel depicting the physical Caesar Cipher Disk."""

    def __init__(self, parent=None, size: int = 320):
        super().__init__(parent)
        self.setMinimumSize(size, size)

        self._shift_key = 0
        self._rotation_angle = 0.0

        # Animation Setup for smooth rotation transition
        self.anim = QPropertyAnimation(self, b"rotationAngle")
        self.anim.setDuration(400)  # ms
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def getRotationAngle(self) -> float:
        return self._rotation_angle

    def setRotationAngle(self, angle: float):
        self._rotation_angle = angle
        self.update()  # Trigger repaint

    rotationAngle = Property(float, getRotationAngle, setRotationAngle)

    def set_shift_key(self, key: int, animated: bool = True):
        """Sets target shift key (0..25) and triggers rotation animation."""
        target_key = key % 26
        target_angle = (target_key / 26.0) * 360.0

        if animated:
            self.anim.stop()
            self.anim.setStartValue(self._rotation_angle)
            self.anim.setEndValue(target_angle)
            self.anim.start()
        else:
            self._rotation_angle = target_angle
            self.update()

        self._shift_key = target_key

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        side = min(rect.width(), rect.height())
        center_x = rect.width() / 2.0
        center_y = rect.height() / 2.0

        # Save coordinate space and center painter at origin
        painter.translate(center_x, center_y)

        radius_outer = side * 0.44
        radius_inner = side * 0.32
        radius_center = side * 0.18

        # --- 1. Outer Ring (Background & Outer Border) ---
        painter.setPen(QPen(QColor(AppColors.BORDER_DEFAULT), 2))
        painter.setBrush(QBrush(QColor(AppColors.BG_SURFACE)))
        painter.drawEllipse(QPointF(0, 0), radius_outer, radius_outer)

        # Draw Outer Alphabet (Plaintext - Fixed Outer Ring)
        font_outer = QFont("Consolas", int(side * 0.045), QFont.Weight.Bold)
        painter.setFont(font_outer)

        for i in range(26):
            # Angle in radians (top = -90 deg)
            angle_deg = -90.0 + (i / 26.0) * 360.0
            angle_rad = math.radians(angle_deg)

            x = (radius_outer - side * 0.05) * math.cos(angle_rad)
            y = (radius_outer - side * 0.05) * math.sin(angle_rad)

            char = chr(ord('A') + i)
            painter.setPen(QPen(QColor(AppColors.CYAN)))

            # Draw letter centered at (x, y)
            text_rect = QRectF(x - 12, y - 12, 24, 24)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, char)

        # --- 2. Inner Ring (Ciphertext - Rotating Inner Disk) ---
        painter.save()
        # Rotate painter by animation angle
        painter.rotate(self._rotation_angle)

        painter.setPen(QPen(QColor(AppColors.CYAN), 1.5))
        painter.setBrush(QBrush(QColor(AppColors.BG_CARD_ELEVATED)))
        painter.drawEllipse(QPointF(0, 0), radius_inner, radius_inner)

        font_inner = QFont("Consolas", int(side * 0.04), QFont.Weight.Bold)
        painter.setFont(font_inner)

        for i in range(26):
            angle_deg = -90.0 + (i / 26.0) * 360.0
            angle_rad = math.radians(angle_deg)

            x = (radius_inner - side * 0.05) * math.cos(angle_rad)
            y = (radius_inner - side * 0.05) * math.sin(angle_rad)

            char = chr(ord('A') + i)
            painter.setPen(QPen(QColor(AppColors.VIOLET)))

            text_rect = QRectF(x - 12, y - 12, 24, 24)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, char)

        # Center Knob / Core
        painter.setPen(QPen(QColor(AppColors.BORDER_DEFAULT), 2))
        painter.setBrush(QBrush(QColor(AppColors.BG_DARK)))
        painter.drawEllipse(QPointF(0, 0), radius_center, radius_center)

        # Display current Shift Key K in center knob
        painter.setPen(QPen(QColor(AppColors.TEXT_PRIMARY)))
        font_key = QFont("Segoe UI", int(side * 0.06), QFont.Weight.Bold)
        painter.setFont(font_key)

        rect_key = QRectF(-radius_center, -radius_center + 2, radius_center * 2, radius_center * 1.3)
        painter.drawText(rect_key, Qt.AlignmentFlag.AlignCenter, f"K = {self._shift_key}")

        font_label = QFont("Segoe UI", int(side * 0.028))
        painter.setFont(font_label)
        painter.setPen(QPen(QColor(AppColors.TEXT_MUTED)))
        rect_sub = QRectF(-radius_center, radius_center * 0.2, radius_center * 2, radius_center * 0.6)
        painter.drawText(rect_sub, Qt.AlignmentFlag.AlignCenter, "SHIFT")

        painter.restore()

        # --- 3. Top Pointer Marker (Indicates top shift alignment) ---
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(AppColors.CYAN)))
        # Pointer triangle at top
        top_y = -radius_outer - 4
        pointer_points = [
            QPointF(0, top_y + 12),
            QPointF(-8, top_y),
            QPointF(8, top_y)
        ]
        painter.drawPolygon(pointer_points)

        painter.end()
