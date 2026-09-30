"""
Vector Icon Generator using QPainter & QPixmap.
Provides high-res crisp icons for Lock, Key, Copy, Refresh, Swap, etc.
"""

from typing import Tuple
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF
from ui.assets.theme import AppColors


class IconFactory:
    """Generates programmatically drawn crisp QIcons."""

    @staticmethod
    def _create_pixmap(size: int = 32) -> Tuple[QPixmap, QPainter]:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        return pixmap, painter

    @classmethod
    def lock_icon(cls, color_str: str = AppColors.CYAN, size: int = 32) -> QIcon:
        pixmap, painter = cls._create_pixmap(size)
        color = QColor(color_str)
        pen = QPen(color, 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        # Draw lock shackle
        painter.drawArc(int(size * 0.3), int(size * 0.15), int(size * 0.4), int(size * 0.45), 0, 180 * 16)
        # Draw body
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(int(size * 0.2), int(size * 0.45), int(size * 0.6), int(size * 0.45), 4, 4)

        painter.end()
        return QIcon(pixmap)

    @classmethod
    def key_icon(cls, color_str: str = AppColors.VIOLET, size: int = 32) -> QIcon:
        pixmap, painter = cls._create_pixmap(size)
        color = QColor(color_str)
        pen = QPen(color, 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        # Draw key head circle
        painter.drawEllipse(QPointF(size * 0.35, size * 0.35), size * 0.2, size * 0.2)
        # Draw key stem
        painter.drawLine(int(size * 0.5), int(size * 0.5), int(size * 0.8), int(size * 0.8))
        # Draw key teeth
        painter.drawLine(int(size * 0.7), int(size * 0.7), int(size * 0.8), int(size * 0.6))
        painter.drawLine(int(size * 0.78), int(size * 0.78), int(size * 0.88), int(size * 0.68))

        painter.end()
        return QIcon(pixmap)

    @classmethod
    def copy_icon(cls, color_str: str = AppColors.TEXT_PRIMARY, size: int = 32) -> QIcon:
        pixmap, painter = cls._create_pixmap(size)
        color = QColor(color_str)
        pen = QPen(color, 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        # Background sheet
        painter.drawRoundedRect(int(size * 0.3), int(size * 0.15), int(size * 0.55), int(size * 0.6), 3, 3)
        # Foreground sheet
        painter.drawRoundedRect(int(size * 0.15), int(size * 0.3), int(size * 0.55), int(size * 0.6), 3, 3)

        painter.end()
        return QIcon(pixmap)

    @classmethod
    def swap_icon(cls, color_str: str = AppColors.CYAN, size: int = 32) -> QIcon:
        pixmap, painter = cls._create_pixmap(size)
        color = QColor(color_str)
        pen = QPen(color, 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        # Right arrow
        painter.drawLine(int(size * 0.2), int(size * 0.35), int(size * 0.8), int(size * 0.35))
        painter.drawLine(int(size * 0.6), int(size * 0.2), int(size * 0.8), int(size * 0.35))
        painter.drawLine(int(size * 0.6), int(size * 0.5), int(size * 0.8), int(size * 0.35))

        # Left arrow
        painter.drawLine(int(size * 0.8), int(size * 0.65), int(size * 0.2), int(size * 0.65))
        painter.drawLine(int(size * 0.4), int(size * 0.5), int(size * 0.2), int(size * 0.65))
        painter.drawLine(int(size * 0.4), int(size * 0.8), int(size * 0.2), int(size * 0.65))

        painter.end()
        return QIcon(pixmap)
