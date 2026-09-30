"""
Design System, Color Palette, and QSS Stylesheet Definitions.
"""

from PySide6.QtGui import QFont, QColor


class AppColors:
    # Main Backgrounds
    BG_DARK = "#0F172A"          # Midnight Deep Slate
    BG_SURFACE = "#1E293B"       # Card Surface
    BG_CARD_ELEVATED = "#273549"  # Higher elevation card
    BG_INPUT = "#0F172A"         # Input field background

    # Brand & Accent Colors
    CYAN = "#06B6D4"             # Electric Cyan
    CYAN_HOVER = "#22D3EE"
    VIOLET = "#8B5CF6"           # Neon Violet
    VIOLET_HOVER = "#A78BFA"
    EMERALD = "#10B981"          # Emerald Green
    ROSE = "#F43F5E"             # Rose Red / Alert

    # Text Colors
    TEXT_PRIMARY = "#F8FAFC"     # Slate 50
    TEXT_SECONDARY = "#94A3B8"   # Slate 400
    TEXT_MUTED = "#64748B"       # Slate 500

    # Borders & Dividers
    BORDER_DEFAULT = "#334155"
    BORDER_FOCUSED = "#06B6D4"

    # QColor instances for custom widget painting
    Q_BG_DARK = QColor("#0F172A")
    Q_CYAN = QColor("#06B6D4")
    Q_VIOLET = QColor("#8B5CF6")
    Q_EMERALD = QColor("#10B981")
    Q_TEXT_PRIMARY = QColor("#F8FAFC")
    Q_TEXT_MUTED = QColor("#64748B")


class AppFonts:
    @staticmethod
    def title_font(size: int = 20) -> QFont:
        font = QFont("Segoe UI", size)
        font.setBold(True)
        return font

    @staticmethod
    def header_font(size: int = 14) -> QFont:
        font = QFont("Segoe UI", size)
        font.setWeight(QFont.Weight.DemiBold)
        return font

    @staticmethod
    def body_font(size: int = 10) -> QFont:
        return QFont("Segoe UI", size)

    @staticmethod
    def mono_font(size: int = 11) -> QFont:
        return QFont("Consolas", size)


class AppStyles:
    @staticmethod
    def get_application_stylesheet() -> str:
        return f"""
        QMainWindow {{
            background-color: {AppColors.BG_DARK};
        }}
        
        QWidget {{
            color: {AppColors.TEXT_PRIMARY};
            font-family: 'Segoe UI', system-ui, sans-serif;
            font-size: 13px;
        }}
        
        /* Tab Widget Styling */
        QTabWidget::pane {{
            border: 1px solid {AppColors.BORDER_DEFAULT};
            border-radius: 12px;
            background-color: {AppColors.BG_SURFACE};
            top: -1px;
        }}
        
        QTabBar::tab {{
            background-color: {AppColors.BG_DARK};
            color: {AppColors.TEXT_SECONDARY};
            border: 1px solid {AppColors.BORDER_DEFAULT};
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 10px 24px;
            margin-right: 4px;
            font-weight: 600;
        }}
        
        QTabBar::tab:selected {{
            background-color: {AppColors.BG_SURFACE};
            color: {AppColors.CYAN};
            border-top: 2px solid {AppColors.CYAN};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {AppColors.BG_CARD_ELEVATED};
            color: {AppColors.TEXT_PRIMARY};
        }}
        
        /* Text Editors */
        QTextEdit, QPlainTextEdit, QLineEdit {{
            background-color: {AppColors.BG_INPUT};
            color: {AppColors.TEXT_PRIMARY};
            border: 1.5px solid {AppColors.BORDER_DEFAULT};
            border-radius: 8px;
            padding: 10px;
            selection-background-color: {AppColors.VIOLET};
        }}
        
        QTextEdit:focus, QPlainTextEdit:focus, QLineEdit:focus {{
            border: 1.5px solid {AppColors.CYAN};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {AppColors.CYAN};
            color: #000000;
            border: none;
            border-radius: 8px;
            padding: 9px 18px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {AppColors.CYAN_HOVER};
        }}
        
        QPushButton:pressed {{
            background-color: {AppColors.CYAN};
        }}
        
        QPushButton#secondaryButton {{
            background-color: {AppColors.BG_CARD_ELEVATED};
            color: {AppColors.TEXT_PRIMARY};
            border: 1px solid {AppColors.BORDER_DEFAULT};
        }}
        
        QPushButton#secondaryButton:hover {{
            background-color: {AppColors.BORDER_DEFAULT};
            color: {AppColors.CYAN};
        }}
        
        QPushButton#accentButton {{
            background-color: {AppColors.VIOLET};
            color: #FFFFFF;
        }}
        
        QPushButton#accentButton:hover {{
            background-color: {AppColors.VIOLET_HOVER};
        }}
        
        /* Slider */
        QSlider::groove:horizontal {{
            height: 6px;
            background: {AppColors.BORDER_DEFAULT};
            border-radius: 3px;
        }}
        
        QSlider::sub-page:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {AppColors.CYAN}, stop:1 {AppColors.VIOLET});
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background: {AppColors.TEXT_PRIMARY};
            border: 2px solid {AppColors.CYAN};
            width: 18px;
            margin-top: -6px;
            margin-bottom: -6px;
            border-radius: 9px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {AppColors.CYAN};
            border: 2px solid {AppColors.TEXT_PRIMARY};
        }}
        
        /* SpinBox */
        QSpinBox {{
            background-color: {AppColors.BG_INPUT};
            color: {AppColors.CYAN};
            border: 1.5px solid {AppColors.BORDER_DEFAULT};
            border-radius: 6px;
            padding: 6px 10px;
            font-weight: bold;
            font-size: 14px;
        }}
        
        QSpinBox:focus {{
            border-color: {AppColors.CYAN};
        }}

        /* Table Widget */
        QTableWidget {{
            background-color: {AppColors.BG_INPUT};
            color: {AppColors.TEXT_PRIMARY};
            gridline-color: {AppColors.BORDER_DEFAULT};
            border: 1px solid {AppColors.BORDER_DEFAULT};
            border-radius: 8px;
            selection-background-color: {AppColors.BG_CARD_ELEVATED};
        }}
        
        QHeaderView::section {{
            background-color: {AppColors.BG_SURFACE};
            color: {AppColors.TEXT_SECONDARY};
            padding: 8px;
            font-weight: bold;
            border: none;
            border-bottom: 1px solid {AppColors.BORDER_DEFAULT};
        }}
        
        /* Scrollbar */
        QScrollBar:vertical {{
            border: none;
            background: {AppColors.BG_DARK};
            width: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {AppColors.BORDER_DEFAULT};
            min-height: 20px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {AppColors.CYAN};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """
