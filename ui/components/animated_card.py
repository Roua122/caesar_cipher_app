"""
Animated Container Card Widget.
Provides smooth hover animation, rounded corners, and glowing borders.
"""

from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property, QRect
from PySide6.QtGui import QColor
from ui.assets.theme import AppColors


class AnimatedCard(QFrame):
    """Container Card Widget with smooth hover shadow/glow effect."""

    def __init__(self, parent=None, hover_color: str = AppColors.CYAN):
        super().__init__(parent)
        self.setObjectName("animatedCard")
        self.setStyleSheet(f"""
            QFrame#animatedCard {{
                background-color: {AppColors.BG_SURFACE};
                border: 1px solid {AppColors.BORDER_DEFAULT};
                border-radius: 12px;
            }}
        """)

        # Drop Shadow Effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)

        self.hover_color = QColor(hover_color)
        self.normal_shadow_color = QColor(0, 0, 0, 80)

    def enterEvent(self, event):
        """On Mouse Enter: Smoothly illuminate glow shadow."""
        self.shadow.setColor(QColor(self.hover_color.red(), self.hover_color.green(), self.hover_color.blue(), 120))
        self.shadow.setBlurRadius(25)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """On Mouse Leave: Restore subtle shadow."""
        self.shadow.setColor(self.normal_shadow_color)
        self.shadow.setBlurRadius(15)
        super().leaveEvent(event)
