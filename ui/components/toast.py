"""
Toast Notification Widget.
Provides pop-up animated feedback (e.g., "Copied to clipboard").
"""

from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor
from ui.assets.theme import AppColors


class ToastNotification(QLabel):
    """Floating Toast Message Notification widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {AppColors.EMERALD};
                color: #000000;
                font-weight: bold;
                border-radius: 20px;
                padding: 10px 24px;
                font-size: 13px;
            }}
        """)

        # Opacity animation for fade in / fade out
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(300)

        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._fade_out)

        self.hide()

    def show_message(self, message: str, duration_ms: int = 2000):
        """Displays toast message with smooth fade in, then auto hides."""
        self.setText(message)
        self.adjustSize()

        # Position centered at bottom of parent window
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = parent_rect.height() - self.height() - 40
            self.move(x, y)

        self.show()

        # Fade in
        self.fade_anim.stop()
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

        # Schedule fade out
        self.hide_timer.start(duration_ms)

    def _fade_out(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(self.hide)
        self.fade_anim.start()
