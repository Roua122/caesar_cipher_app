"""
Interactive Encrypt / Decrypt Primary View.
Provides clear explicit mode selection between Encrypting a new message vs
Decrypting an existing ciphertext message.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QSlider, QSpinBox, QApplication, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from core.caesar_cipher import CaesarCipher
from core.validator import CipherValidator
from ui.assets.theme import AppColors, AppFonts
from ui.assets.icons import IconFactory
from ui.components.animated_card import AnimatedCard
from ui.components.cipher_wheel import CipherWheelWidget


class EncryptDecryptView(QWidget):
    """Primary interactive view for Encrypting or Decrypting messages."""

    toast_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_encrypt_mode = True
        self.shift_key = 3

        self._setup_ui()
        self._update_mode_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(20)

        # Left Column: Input, Mode Switcher, and Output
        left_col = QVBoxLayout()

        # Mode Selection Header Card
        mode_card = AnimatedCard(self, hover_color=AppColors.CYAN)
        mode_layout = QVBoxLayout(mode_card)
        mode_layout.setContentsMargins(14, 12, 14, 12)

        mode_header_label = QLabel("اختر العملية المطلوبة (Select Action):")
        mode_header_label.setFont(AppFonts.header_font(12))
        mode_header_label.setStyleSheet(f"color: {AppColors.TEXT_PRIMARY};")

        btn_row = QHBoxLayout()

        self.btn_mode_encrypt = QPushButton("🔒 تشفير نص جديد (Encrypt)")
        self.btn_mode_encrypt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_mode_encrypt.setFixedHeight(40)
        self.btn_mode_encrypt.setFont(AppFonts.header_font(11))
        self.btn_mode_encrypt.clicked.connect(lambda: self._set_mode(True))

        self.btn_mode_decrypt = QPushButton("🔓 فك تشفير نص مشفر (Decrypt)")
        self.btn_mode_decrypt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_mode_decrypt.setFixedHeight(40)
        self.btn_mode_decrypt.setFont(AppFonts.header_font(11))
        self.btn_mode_decrypt.clicked.connect(lambda: self._set_mode(False))

        btn_row.addWidget(self.btn_mode_encrypt)
        btn_row.addWidget(self.btn_mode_decrypt)

        mode_layout.addWidget(mode_header_label)
        mode_layout.addLayout(btn_row)

        left_col.addWidget(mode_card)

        # Input Card
        input_card = AnimatedCard(self, hover_color=AppColors.CYAN)
        input_card_layout = QVBoxLayout(input_card)

        input_header_layout = QHBoxLayout()
        self.input_title = QLabel("1. أدخل النص الاصلي للتشفير:")
        self.input_title.setFont(AppFonts.header_font(11))

        btn_sample = QPushButton("نص تجريبي Sample")
        btn_sample.setObjectName("secondaryButton")
        btn_sample.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sample.clicked.connect(self._load_sample_text)

        btn_clear = QPushButton("مسح Clear")
        btn_clear.setObjectName("secondaryButton")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self._clear_input)

        input_header_layout.addWidget(self.input_title)
        input_header_layout.addStretch()
        input_header_layout.addWidget(btn_sample)
        input_header_layout.addWidget(btn_clear)

        self.input_text_edit = QTextEdit()
        self.input_text_edit.setFont(AppFonts.mono_font(11))
        self.input_text_edit.textChanged.connect(self._on_input_changed)

        self.lbl_stats = QLabel("عدد الأحرف: 0")
        self.lbl_stats.setStyleSheet(f"color: {AppColors.TEXT_MUTED}; font-size: 11px;")

        input_card_layout.addLayout(input_header_layout)
        input_card_layout.addWidget(self.input_text_edit)
        input_card_layout.addWidget(self.lbl_stats)

        left_col.addWidget(input_card)

        # Output Card
        output_card = AnimatedCard(self, hover_color=AppColors.VIOLET)
        output_card_layout = QVBoxLayout(output_card)

        output_header_layout = QHBoxLayout()
        self.output_title = QLabel("3. النتيجة المشفرة:")
        self.output_title.setFont(AppFonts.header_font(11))

        btn_copy = QPushButton("نسخ النتيجة Copy")
        btn_copy.setObjectName("accentButton")
        btn_copy.setIcon(IconFactory.copy_icon("#FFFFFF", 20))
        btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy.clicked.connect(self._copy_output)

        output_header_layout.addWidget(self.output_title)
        output_header_layout.addStretch()
        output_header_layout.addWidget(btn_copy)

        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setFont(AppFonts.mono_font(11))

        output_card_layout.addLayout(output_header_layout)
        output_card_layout.addWidget(self.output_text_edit)

        left_col.addWidget(output_card)

        # Right Column: Animated Cipher Wheel & Shift Key K Controls
        right_col = QVBoxLayout()

        wheel_card = AnimatedCard(self, hover_color=AppColors.VIOLET)
        wheel_card_layout = QVBoxLayout(wheel_card)
        wheel_card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wheel_title = QLabel("عجلة التشفير التفاعلية (Caesar Wheel)")
        wheel_title.setFont(AppFonts.header_font(12))
        wheel_title.setStyleSheet(f"color: {AppColors.TEXT_PRIMARY};")
        wheel_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cipher_wheel = CipherWheelWidget(self, size=290)
        self.cipher_wheel.set_shift_key(self.shift_key, animated=False)

        wheel_card_layout.addWidget(wheel_title)
        wheel_card_layout.addWidget(self.cipher_wheel)

        # Shift Key Controls Box
        key_controls_layout = QVBoxLayout()

        key_label_row = QHBoxLayout()
        lbl_key_heading = QLabel("2. حدد قيمة مفتاح الإزاحة (Shift Key K):")
        lbl_key_heading.setFont(AppFonts.header_font(11))
        lbl_key_heading.setStyleSheet(f"color: {AppColors.CYAN};")

        self.key_spinbox = QSpinBox()
        self.key_spinbox.setRange(0, 25)
        self.key_spinbox.setValue(self.shift_key)
        self.key_spinbox.valueChanged.connect(self._on_key_spinbox_changed)

        key_label_row.addWidget(lbl_key_heading)
        key_label_row.addStretch()
        key_label_row.addWidget(self.key_spinbox)

        # Key Slider
        self.key_slider = QSlider(Qt.Orientation.Horizontal)
        self.key_slider.setRange(0, 25)
        self.key_slider.setValue(self.shift_key)
        self.key_slider.valueChanged.connect(self._on_key_slider_changed)

        # Quick Preset Buttons
        presets_layout = QHBoxLayout()
        lbl_preset = QLabel("اختيارات سريعة:")
        lbl_preset.setStyleSheet(f"color: {AppColors.TEXT_MUTED}; font-size: 11px;")
        presets_layout.addWidget(lbl_preset)

        for k_val in [3, 5, 13]:
            btn_preset = QPushButton(f"K = {k_val}" + (" (ROT13)" if k_val == 13 else ""))
            btn_preset.setObjectName("secondaryButton")
            btn_preset.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_preset.clicked.connect(lambda checked=False, k=k_val: self.set_key_value(k))
            presets_layout.addWidget(btn_preset)

        key_controls_layout.addLayout(key_label_row)
        key_controls_layout.addWidget(self.key_slider)
        key_controls_layout.addLayout(presets_layout)

        wheel_card_layout.addLayout(key_controls_layout)

        right_col.addWidget(wheel_card)

        # Add columns to main layout
        main_layout.addLayout(left_col, stretch=3)
        main_layout.addLayout(right_col, stretch=2)

    def _set_mode(self, encrypt_mode: bool):
        """Switches between Encrypt Mode and Decrypt Mode cleanly."""
        self.is_encrypt_mode = encrypt_mode
        self._update_mode_ui()
        self._update_transformation()

    def _update_mode_ui(self):
        if self.is_encrypt_mode:
            # Active Encrypt Styling
            self.btn_mode_encrypt.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppColors.CYAN};
                    color: #000000;
                    border: none;
                    border-radius: 6px;
                }}
            """)
            self.btn_mode_decrypt.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppColors.BG_INPUT};
                    color: {AppColors.TEXT_SECONDARY};
                    border: 1px solid {AppColors.BORDER_DEFAULT};
                    border-radius: 6px;
                }}
            """)

            self.input_title.setText("1. أدخل النص الأصلي المراد تشفيره (Plaintext Input):")
            self.input_title.setStyleSheet(f"color: {AppColors.CYAN};")
            self.input_text_edit.setPlaceholderText("اكتب النص العادي بالإنجليزية هنا... مثلاً: HELLO WORLD")

            self.output_title.setText("3. النتيجة المشفرة بعد الإزاحة (Encrypted Ciphertext):")
            self.output_title.setStyleSheet(f"color: {AppColors.VIOLET};")
        else:
            # Active Decrypt Styling
            self.btn_mode_decrypt.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppColors.VIOLET};
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                }}
            """)
            self.btn_mode_encrypt.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppColors.BG_INPUT};
                    color: {AppColors.TEXT_SECONDARY};
                    border: 1px solid {AppColors.BORDER_DEFAULT};
                    border-radius: 6px;
                }}
            """)

            self.input_title.setText("1. أدخل النص المشفر المراد فك تشفيره (Ciphertext Input):")
            self.input_title.setStyleSheet(f"color: {AppColors.VIOLET};")
            self.input_text_edit.setPlaceholderText("اكتب النص المشفر بالإنجليزية هنا... مثلاً: KHOOR ZRUOG")

            self.output_title.setText("3. النص الأصلي المحلول بعد فك التشفير (Decrypted Plaintext):")
            self.output_title.setStyleSheet(f"color: {AppColors.CYAN};")

    def set_key_value(self, k: int):
        """Sets key K from external calls (slider, spinbox, or tab 2)."""
        self.key_spinbox.setValue(k)

    def set_text_and_decrypt(self, ciphertext: str, key: int):
        """Called from Brute Force view to import ciphertext and key K directly."""
        self._set_mode(False)  # Decrypt Mode
        self.set_key_value(key)
        self.input_text_edit.setPlainText(ciphertext)

    def _on_key_spinbox_changed(self, val: int):
        self.shift_key = val
        self.key_slider.blockSignals(True)
        self.key_slider.setValue(val)
        self.key_slider.blockSignals(False)

        self.cipher_wheel.set_shift_key(val, animated=True)
        self._update_transformation()

    def _on_key_slider_changed(self, val: int):
        self.shift_key = val
        self.key_spinbox.blockSignals(True)
        self.key_spinbox.setValue(val)
        self.key_spinbox.blockSignals(False)

        self.cipher_wheel.set_shift_key(val, animated=True)
        self._update_transformation()

    def _on_input_changed(self):
        text = self.input_text_edit.toPlainText()
        stats = CipherValidator.get_alphabet_stats(text)
        self.lbl_stats.setText(
            f"عدد الأحرف الكلي: {stats['total']} | الأحرف الأبجدية: {stats['alpha']} | الأرقام: {stats['digits']} | الفواصل: {stats['symbols'] + stats['spaces']}"
        )
        self._update_transformation()

    def _update_transformation(self):
        input_text = self.input_text_edit.toPlainText()
        if not input_text:
            self.output_text_edit.clear()
            return

        if self.is_encrypt_mode:
            res = CaesarCipher.encrypt(input_text, self.shift_key)
        else:
            res = CaesarCipher.decrypt(input_text, self.shift_key)

        self.output_text_edit.setPlainText(res)

    def _load_sample_text(self):
        if self.is_encrypt_mode:
            sample = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        else:
            sample = "WKH TXLFN EURZQ IRZ MXPSV RYHU WKH ODCB GRJ"
        self.input_text_edit.setPlainText(sample)
        self.toast_requested.emit("تم تحميل نص تجريبي!")

    def _clear_input(self):
        self.input_text_edit.clear()

    def _copy_output(self):
        out = self.output_text_edit.toPlainText()
        if out:
            QApplication.clipboard().setText(out)
            self.toast_requested.emit("تم نسخ النتيجة للحافظة! 📋")
