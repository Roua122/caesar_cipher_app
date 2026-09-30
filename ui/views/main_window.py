"""
Main Application Shell Window.
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ui.assets.theme import AppColors, AppFonts, AppStyles
from ui.assets.icons import IconFactory
from ui.components.toast import ToastNotification
from ui.views.encrypt_decrypt_view import EncryptDecryptView
from ui.views.brute_force_view import BruteForceView


class MainWindow(QMainWindow):
    """Main Application Window containing header and tabbed views."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("General Caesar Cipher Studio | برنامج تشفير قيصر الاحترافي")
        self.resize(1100, 750)
        self.setMinimumSize(900, 650)

        # Apply global stylesheet
        self.setStyleSheet(AppStyles.get_application_stylesheet())

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(20, 16, 20, 20)
        root_layout.setSpacing(16)

        # Header Bar
        header_layout = QHBoxLayout()

        icon_label = QLabel()
        icon_label.setPixmap(IconFactory.lock_icon(AppColors.CYAN, 40).pixmap(40, 40))

        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        main_title = QLabel("CAESAR CIPHER STUDIO")
        main_title.setFont(AppFonts.title_font(18))
        main_title.setStyleSheet(f"color: {AppColors.CYAN}; letter-spacing: 1px;")

        sub_title = QLabel("General Additive Cipher Cryptographic Visualizer & Cracker")
        sub_title.setFont(AppFonts.body_font(10))
        sub_title.setStyleSheet(f"color: {AppColors.TEXT_MUTED};")

        title_box.addWidget(main_title)
        title_box.addWidget(sub_title)

        header_layout.addWidget(icon_label)
        header_layout.addLayout(title_box)
        header_layout.addStretch()

        root_layout.addLayout(header_layout)

        # Tab Views Container
        self.tabs = QTabWidget()
        self.tabs.setCursor(Qt.CursorShape.PointingHandCursor)

        self.tab_encrypt = EncryptDecryptView(self)
        self.tab_brute = BruteForceView(self)

        self.tabs.addTab(self.tab_encrypt, "🔒 Encrypt & Decrypt")
        self.tabs.addTab(self.tab_brute, "🚀 Brute-Force Cracker")

        root_layout.addWidget(self.tabs)

        # Toast Overlay Notification
        self.toast = ToastNotification(self)

        # Connect signals
        self.tab_encrypt.toast_requested.connect(self.toast.show_message)
        self.tab_brute.toast_requested.connect(self.toast.show_message)
        self.tab_brute.apply_key_requested.connect(self._handle_apply_key_from_brute)

    def _handle_apply_key_from_brute(self, ciphertext: str, key: int):
        """Switches to Tab 1, sets Decrypt mode, and transfers ciphertext and key K."""
        self.tab_encrypt.set_text_and_decrypt(ciphertext, key)
        self.tabs.setCurrentIndex(0)
        self.toast.show_message(f"تم تطبيق المفتاح K = {key} والانتقال لشاشة فك التشفير!")

    def resizeEvent(self, event):
        """Ensure floating toast repositions cleanly on window resize."""
        super().resizeEvent(event)
        if self.toast.isVisible():
            parent_rect = self.rect()
            x = (parent_rect.width() - self.toast.width()) // 2
            y = parent_rect.height() - self.toast.height() - 40
            self.toast.move(x, y)
