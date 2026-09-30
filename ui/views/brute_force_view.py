"""
Brute-Force Cracker & Frequency Analysis View.
Provides automated key discovery when the secret key K is UNKNOWN.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QProgressBar, QApplication
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

from core.caesar_cipher import CaesarCipher
from ui.assets.theme import AppColors, AppFonts
from ui.assets.icons import IconFactory
from ui.components.animated_card import AnimatedCard


class BruteForceView(QWidget):
    """View tab for cracking unknown Caesar ciphers without knowing key K."""

    toast_requested = Signal(str)
    apply_key_requested = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Header Explanatory Card
        header_card = AnimatedCard(self, hover_color=AppColors.VIOLET)
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(14, 12, 14, 12)

        title = QLabel("🔍 مستكشف المفتاح المجهول (Automated Key Cracker & Finder)")
        title.setFont(AppFonts.header_font(13))
        title.setStyleSheet(f"color: {AppColors.VIOLET};")

        desc = QLabel(
            "💡 **الهدف من هذه ال:**\n"
            "إذا وصلت إليك رسالة مشفرة **ولا تعرف قيمة المفتاح K**، "
            "ضع الرسالة المشفرة في الصندوق أدناه واضغط على (بدء التخمين الذكي). "
            "سيقوم التطبيق بتجربة جميع الاحتمالات الـ 26 الممكنة لمفتاح الإزاحة K في جزء من الثانية، "
            "وتحليل الكلمات إحصائياً للكشف عن المعنى الأصلي والمفتاح K الصحيح!"
        )
        desc.setFont(AppFonts.body_font(10))
        desc.setStyleSheet(f"color: {AppColors.TEXT_PRIMARY}; line-height: 1.4;")
        desc.setWordWrap(True)

        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        layout.addWidget(header_card)

        # Input Box Container
        input_card = AnimatedCard(self, hover_color=AppColors.CYAN)
        input_layout = QVBoxLayout(input_card)

        input_header = QHBoxLayout()
        lbl_input = QLabel("أدخل الرسالة المشفرة مجهولة المفتاح:")
        lbl_input.setFont(AppFonts.header_font(11))
        lbl_input.setStyleSheet(f"color: {AppColors.CYAN};")

        btn_sample = QPushButton("تحميل نموذج مشفر تجريبي")
        btn_sample.setObjectName("secondaryButton")
        btn_sample.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sample.clicked.connect(self._load_sample_ciphertext)

        btn_analyze = QPushButton("بدء التخمين الذكي 🚀")
        btn_analyze.setObjectName("accentButton")
        btn_analyze.setIcon(IconFactory.key_icon("#FFFFFF", 20))
        btn_analyze.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_analyze.clicked.connect(self._run_brute_force)

        input_header.addWidget(lbl_input)
        input_header.addStretch()
        input_header.addWidget(btn_sample)
        input_header.addWidget(btn_analyze)

        self.cipher_input = QTextEdit()
        self.cipher_input.setMaximumHeight(85)
        self.cipher_input.setPlaceholderText("ضع النص المشفر هنا... مثلاً: WKH TXLFN EURZQ IRZ MXPSV RYHU WKH ODCB GRJ")
        self.cipher_input.setFont(AppFonts.mono_font(11))
        # Live calculation while typing
        self.cipher_input.textChanged.connect(self._run_brute_force)

        input_layout.addLayout(input_header)
        input_layout.addWidget(self.cipher_input)

        layout.addWidget(input_card)

        # Table Results Container
        table_card = AnimatedCard(self, hover_color=AppColors.CYAN)
        table_layout = QVBoxLayout(table_card)

        table_header = QHBoxLayout()
        lbl_results = QLabel("نتائج الاحتمالات الـ 26 مرتبة حسب نسبة النجاح:")
        lbl_results.setFont(AppFonts.header_font(11))

        table_header.addWidget(lbl_results)
        table_header.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["المفتاح K", "نسبة المطابقة", "الدرجة", "النص الفعلي الناتج", "إجراء"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 95)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(4, 160)
        self.table.setMinimumHeight(320)  # Ensure table has explicit visible height
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        table_layout.addLayout(table_header)
        table_layout.addWidget(self.table)

        layout.addWidget(table_card, stretch=1)

    def _load_sample_ciphertext(self):
        # Sample encrypted with K=3
        sample = "WKH TXLFN EURZQ IRZ MXPSV RYHU WKH ODCB GRJ"
        self.cipher_input.setPlainText(sample)
        self._run_brute_force()
        self.toast_requested.emit("تم تحميل نص مشفر تجريبي وتشغيل التخمين!")

    def _run_brute_force(self):
        text = self.cipher_input.toPlainText().strip()
        if not text:
            self.table.setRowCount(0)
            return

        candidates = CaesarCipher.brute_force(text)
        self.table.setRowCount(len(candidates))

        for row, item in enumerate(candidates):
            self.table.setRowHeight(row, 36)
            key_val = item['key']
            decrypted_text = item['decrypted']

            # Key K Item
            k_item = QTableWidgetItem(f"K = {key_val}")
            k_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            k_item.setFont(AppFonts.header_font(11))

            if item.get('is_best_match', False):
                k_item.setBackground(QColor(AppColors.EMERALD))
                k_item.setForeground(QColor("#000000"))

            # Confidence Progress Bar
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(int(item['confidence']))
            progress_bar.setTextVisible(True)

            if item['confidence'] > 70:
                progress_bar.setStyleSheet(f"""
                    QProgressBar {{
                        border: 1px solid {AppColors.BORDER_DEFAULT};
                        border-radius: 5px;
                        text-align: center;
                        color: #FFFFFF;
                        font-weight: bold;
                        background: {AppColors.BG_INPUT};
                    }}
                    QProgressBar::chunk {{
                        background-color: {AppColors.EMERALD};
                        border-radius: 4px;
                    }}
                """)
            else:
                progress_bar.setStyleSheet(f"""
                    QProgressBar {{
                        border: 1px solid {AppColors.BORDER_DEFAULT};
                        border-radius: 5px;
                        text-align: center;
                        color: {AppColors.TEXT_SECONDARY};
                        background: {AppColors.BG_INPUT};
                    }}
                    QProgressBar::chunk {{
                        background-color: {AppColors.VIOLET};
                        border-radius: 4px;
                    }}
                """)

            # Score Item
            score_item = QTableWidgetItem(str(item['score']))
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            score_item.setFont(AppFonts.mono_font(10))

            # Decrypted Text Candidate
            dec_item = QTableWidgetItem(decrypted_text)
            dec_item.setFont(AppFonts.mono_font(11))

            # Transfer Button
            btn_use = QPushButton("استخدم K في الرئيسية ➔")
            btn_use.setObjectName("secondaryButton")
            btn_use.setCursor(Qt.CursorShape.PointingHandCursor)
            # Bind text payload and key
            btn_use.clicked.connect(lambda checked=False, t=text, k=key_val: self._transfer_key(t, k))

            self.table.setItem(row, 0, k_item)
            self.table.setCellWidget(row, 1, progress_bar)
            self.table.setItem(row, 2, score_item)
            self.table.setItem(row, 3, dec_item)
            self.table.setCellWidget(row, 4, btn_use)

        self.table.viewport().update()

    def _transfer_key(self, ciphertext: str, key: int):
        self.apply_key_requested.emit(ciphertext, key)
