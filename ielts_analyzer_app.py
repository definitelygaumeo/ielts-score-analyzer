"""
IELTS Score Analyzer - Windows Desktop Application
AI Document Summarizer with Settings for API Keys
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Try PyQt6 first, fall back to PyQt5
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget,
        QGroupBox, QFormLayout, QDoubleSpinBox, QMessageBox,
        QDialog, QDialogButtonBox, QComboBox, QCheckBox, QFrame,
        QScrollArea, QFileDialog, QProgressBar, QSplitter
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
    from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
    PYQT_VERSION = 6
except ImportError:
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget,
            QGroupBox, QFormLayout, QDoubleSpinBox, QMessageBox,
            QDialog, QDialogButtonBox, QComboBox, QCheckBox, QFrame,
            QScrollArea, QFileDialog, QProgressBar, QSplitter
        )
        from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings
        from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
        PYQT_VERSION = 5
    except ImportError:
        print("Please install PyQt6: pip install PyQt6")
        sys.exit(1)


# =============================================================================
# CONSTANTS & DATA
# =============================================================================

APP_NAME = "IELTS Score Analyzer"
APP_VERSION = "1.0.0"
CONFIG_FILE = "ielts_analyzer_config.json"

BAND_DESCRIPTIONS = {
    9: "Expert User - Thành thạo hoàn toàn",
    8: "Very Good User - Rất thành thạo",
    7: "Good User - Thành thạo",
    6: "Competent User - Đủ năng lực",
    5: "Modest User - Khiêm tốn",
    4: "Limited User - Hạn chế",
    3: "Extremely Limited - Rất hạn chế",
    2: "Intermittent User - Không ổn định",
    1: "Non User - Không sử dụng được"
}

SKILL_NAMES = {
    'listening': 'Nghe (Listening)',
    'speaking': 'Nói (Speaking)',
    'reading': 'Đọc (Reading)',
    'writing': 'Viết (Writing)'
}

RECOMMENDATIONS = {
    'listening': {
        'low': [
            "Nghe podcast tiếng Anh hàng ngày (BBC Learning English, IELTS Liz)",
            "Xem phim/series có phụ đề tiếng Anh, dần bỏ phụ đề",
            "Luyện nghe với bài test IELTS Listening từ Cambridge",
            "Tập nghe các giọng khác nhau: British, American, Australian"
        ],
        'medium': [
            "Nghe TED Talks, documentaries để tăng độ khó",
            "Practice note-taking khi nghe academic lectures",
            "Làm quen với tất cả dạng câu hỏi IELTS Listening"
        ],
        'high': [
            "Nghe tin tức quốc tế hàng ngày (BBC, CNN)",
            "Thử thách với academic lectures từ Coursera, edX"
        ]
    },
    'speaking': {
        'low': [
            "Thực hành nói mỗi ngày, tự ghi âm và nghe lại",
            "Sử dụng app Cambly, iTalki để luyện với native speakers",
            "Học topic thường gặp trong IELTS Speaking Part 1, 2, 3",
            "Xây dựng vocabulary theo chủ đề với collocations"
        ],
        'medium': [
            "Tập trả lời Part 2 với cue card trong 2 phút",
            "Cải thiện pronunciation và connected speech",
            "Học cách phát triển ý tưởng và đưa ví dụ"
        ],
        'high': [
            "Thực hành tranh luận các chủ đề phức tạp",
            "Học idioms, phrasal verbs nâng cao"
        ]
    },
    'reading': {
        'low': [
            "Đọc báo tiếng Anh hàng ngày (The Guardian, BBC News)",
            "Học kỹ năng skimming và scanning",
            "Xây dựng vocabulary qua đọc và ghi chép từ mới",
            "Sử dụng Kindle với dictionary tích hợp"
        ],
        'medium': [
            "Làm quen với các dạng bài Reading IELTS",
            "Đọc academic articles và research papers",
            "Tập đọc nhanh trong thời gian giới hạn"
        ],
        'high': [
            "Đọc tài liệu chuyên ngành phức tạp",
            "Cải thiện tốc độ đọc mà vẫn hiểu sâu nội dung"
        ]
    },
    'writing': {
        'low': [
            "Viết nhật ký bằng tiếng Anh mỗi ngày",
            "Học cấu trúc bài luận IELTS Task 1 và Task 2",
            "Luyện viết câu phức với linking words",
            "Nhờ giáo viên chữa bài và học từ feedback"
        ],
        'medium': [
            "Tập phân tích đề và lập dàn ý trước khi viết",
            "Học paraphrase và sử dụng synonyms đa dạng",
            "Viết 2-3 bài essay mỗi tuần"
        ],
        'high': [
            "Viết bài luận phức tạp với nhiều góc nhìn",
            "Cải thiện academic vocabulary"
        ]
    }
}

# =============================================================================
# STYLES
# =============================================================================

STYLESHEET = """
QMainWindow {
    background-color: #1e3a5f;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

QTabWidget::pane {
    border: none;
    background: #f5f7fa;
    border-radius: 10px;
}

QTabBar::tab {
    background: #3d5a80;
    color: white;
    padding: 12px 25px;
    margin-right: 3px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background: #ee6c4d;
}

QTabBar::tab:hover:!selected {
    background: #4a6fa5;
}

QGroupBox {
    background: white;
    border: 2px solid #e0e5ec;
    border-radius: 12px;
    margin-top: 15px;
    padding: 20px;
    font-weight: bold;
    color: #1e3a5f;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 20px;
    padding: 0 10px;
    color: #1e3a5f;
}

QLabel {
    color: #293241;
}

QLineEdit, QDoubleSpinBox, QComboBox {
    padding: 10px 15px;
    border: 2px solid #e0e5ec;
    border-radius: 8px;
    background: #fafbfc;
    color: #293241;
    selection-background-color: #ee6c4d;
}

QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border-color: #ee6c4d;
    background: white;
}

QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    width: 25px;
    border-radius: 4px;
}

QPushButton {
    padding: 12px 25px;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    color: white;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ee6c4d, stop:1 #f4a261);
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f4a261, stop:1 #ee6c4d);
}

QPushButton:pressed {
    background: #d95d3f;
}

QPushButton#secondaryBtn {
    background: #3d5a80;
}

QPushButton#secondaryBtn:hover {
    background: #4a6fa5;
}

QPushButton#settingsBtn {
    background: #2a9d8f;
}

QPushButton#settingsBtn:hover {
    background: #3ab5a6;
}

QTextEdit {
    border: 2px solid #e0e5ec;
    border-radius: 10px;
    padding: 15px;
    background: white;
    color: #293241;
    line-height: 1.6;
}

QScrollArea {
    border: none;
    background: transparent;
}

QProgressBar {
    border: none;
    border-radius: 5px;
    background: #e0e5ec;
    height: 10px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ee6c4d, stop:1 #f4a261);
    border-radius: 5px;
}

QCheckBox {
    spacing: 10px;
    color: #293241;
}

QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border-radius: 5px;
    border: 2px solid #e0e5ec;
    background: white;
}

QCheckBox::indicator:checked {
    background: #ee6c4d;
    border-color: #ee6c4d;
}

QDialog {
    background: #f5f7fa;
}
"""

# Dark Mode Stylesheet
DARK_STYLESHEET = """
QMainWindow {
    background-color: #1a1a2e;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #e0e0e0;
}

QTabWidget::pane {
    border: none;
    background: #16213e;
    border-radius: 10px;
}

QTabBar::tab {
    background: #0f3460;
    color: #e0e0e0;
    padding: 12px 25px;
    margin-right: 3px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background: #e94560;
}

QTabBar::tab:hover:!selected {
    background: #1a4a7a;
}

QGroupBox {
    background: #16213e;
    border: 2px solid #0f3460;
    border-radius: 12px;
    margin-top: 15px;
    padding: 20px;
    font-weight: bold;
    color: #e94560;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 20px;
    padding: 0 10px;
    color: #e94560;
}

QLabel {
    color: #e0e0e0;
}

QLineEdit, QDoubleSpinBox, QComboBox {
    padding: 10px 15px;
    border: 2px solid #0f3460;
    border-radius: 8px;
    background: #1a1a2e;
    color: #e0e0e0;
    selection-background-color: #e94560;
}

QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border-color: #e94560;
    background: #16213e;
}

QComboBox::drop-down {
    border: none;
    background: #0f3460;
}

QComboBox QAbstractItemView {
    background: #16213e;
    color: #e0e0e0;
    selection-background-color: #e94560;
}

QPushButton {
    padding: 12px 25px;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    color: white;
    background: #e94560;
}

QPushButton:hover {
    background: #ff6b6b;
}

QPushButton:pressed {
    background: #c73e54;
}

QPushButton#secondaryBtn {
    background: #0f3460;
}

QPushButton#secondaryBtn:hover {
    background: #1a4a7a;
}

QPushButton#settingsBtn {
    background: #533483;
}

QPushButton#settingsBtn:hover {
    background: #6a4a9e;
}

QTextEdit {
    border: 2px solid #0f3460;
    border-radius: 10px;
    padding: 15px;
    background: #16213e;
    color: #e0e0e0;
}

QScrollArea {
    border: none;
    background: transparent;
}

QProgressBar {
    border: none;
    border-radius: 5px;
    background: #0f3460;
    height: 10px;
}

QProgressBar::chunk {
    background: #e94560;
    border-radius: 5px;
}

QCheckBox {
    spacing: 10px;
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border-radius: 5px;
    border: 2px solid #0f3460;
    background: #1a1a2e;
}

QCheckBox::indicator:checked {
    background: #e94560;
    border-color: #e94560;
}

QDialog {
    background: #16213e;
}

QScrollBar:vertical {
    background: #1a1a2e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #0f3460;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #e94560;
}
"""


# =============================================================================
# SETTINGS DIALOG
# =============================================================================

class SettingsDialog(QDialog):
    """Settings dialog for API keys and preferences"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cài Đặt - Settings")
        self.setFixedSize(550, 600)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        # Main style for dialog
        self.setStyleSheet("""
            QDialog {
                background: #2d3748;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #f6ad55;
                border: 2px solid #4a5568;
                border-radius: 8px;
                margin-top: 12px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                background: #2d3748;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # ===== Header =====
        header = QLabel("Cài Đặt Ứng Dụng")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #f6ad55; padding: 5px;")
        layout.addWidget(header)
        
        # ===== API Keys Section =====
        api_group = QGroupBox("API Keys")
        api_layout = QVBoxLayout(api_group)
        api_layout.setSpacing(10)
        api_layout.setContentsMargins(12, 20, 12, 12)
        
        # Common styles
        label_style = "color: #e2e8f0; font-size: 12px; font-weight: bold;"
        input_style = """
            QLineEdit {
                background: #1a202c;
                color: #ffffff;
                border: 2px solid #4a5568;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }
            QLineEdit:focus { border-color: #f6ad55; }
        """
        btn_style = """
            QPushButton {
                background: #4a5568;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { background: #718096; }
            QPushButton:checked { background: #ed8936; }
        """
        
        # OpenAI
        lbl1 = QLabel("OpenAI API Key:")
        lbl1.setStyleSheet(label_style)
        api_layout.addWidget(lbl1)
        
        row1 = QHBoxLayout()
        self.openai_key = QLineEdit()
        self.openai_key.setPlaceholderText("sk-...")
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key.setStyleSheet(input_style)
        self.openai_key.setFixedHeight(36)
        row1.addWidget(self.openai_key)
        
        self.show_openai_btn = QPushButton("Show")
        self.show_openai_btn.setCheckable(True)
        self.show_openai_btn.setFixedSize(55, 36)
        self.show_openai_btn.setStyleSheet(btn_style)
        self.show_openai_btn.toggled.connect(self.toggle_openai_visibility)
        row1.addWidget(self.show_openai_btn)
        api_layout.addLayout(row1)
        
        # Anthropic
        lbl2 = QLabel("Anthropic API Key:")
        lbl2.setStyleSheet(label_style)
        api_layout.addWidget(lbl2)
        
        row2 = QHBoxLayout()
        self.anthropic_key = QLineEdit()
        self.anthropic_key.setPlaceholderText("sk-ant-...")
        self.anthropic_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.anthropic_key.setStyleSheet(input_style)
        self.anthropic_key.setFixedHeight(36)
        row2.addWidget(self.anthropic_key)
        
        self.show_anthropic_btn = QPushButton("Show")
        self.show_anthropic_btn.setCheckable(True)
        self.show_anthropic_btn.setFixedSize(55, 36)
        self.show_anthropic_btn.setStyleSheet(btn_style)
        self.show_anthropic_btn.toggled.connect(self.toggle_anthropic_visibility)
        row2.addWidget(self.show_anthropic_btn)
        api_layout.addLayout(row2)
        
        # Gemini
        lbl3 = QLabel("Google Gemini API Key:")
        lbl3.setStyleSheet(label_style)
        api_layout.addWidget(lbl3)
        
        row3 = QHBoxLayout()
        self.gemini_key = QLineEdit()
        self.gemini_key.setPlaceholderText("AIza...")
        self.gemini_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_key.setStyleSheet(input_style)
        self.gemini_key.setFixedHeight(36)
        row3.addWidget(self.gemini_key)
        
        self.show_gemini_btn = QPushButton("Show")
        self.show_gemini_btn.setCheckable(True)
        self.show_gemini_btn.setFixedSize(55, 36)
        self.show_gemini_btn.setStyleSheet(btn_style)
        self.show_gemini_btn.toggled.connect(self.toggle_gemini_visibility)
        row3.addWidget(self.show_gemini_btn)
        api_layout.addLayout(row3)
        
        layout.addWidget(api_group)
        
        # ===== AI Provider Section =====
        ai_group = QGroupBox("AI Provider")
        ai_layout = QVBoxLayout(ai_group)
        ai_layout.setContentsMargins(12, 20, 12, 12)
        
        ai_label = QLabel("Chọn AI Model:")
        ai_label.setStyleSheet(label_style)
        ai_layout.addWidget(ai_label)
        
        self.ai_provider = QComboBox()
        self.ai_provider.addItems([
            "Không sử dụng AI (Rule-based)",
            "OpenAI GPT-4",
            "OpenAI GPT-3.5 Turbo",
            "Anthropic Claude 3 Sonnet",
            "Anthropic Claude 3 Haiku",
            "Google Gemini Pro",
            "Google Gemini Flash"
        ])
        self.ai_provider.setStyleSheet("""
            QComboBox {
                background: #1a202c;
                color: #ffffff;
                border: 2px solid #4a5568;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }
            QComboBox:hover { border-color: #f6ad55; }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox QAbstractItemView {
                background: #2d3748;
                color: #ffffff;
                selection-background-color: #ed8936;
            }
        """)
        self.ai_provider.setFixedHeight(36)
        ai_layout.addWidget(self.ai_provider)
        
        layout.addWidget(ai_group)
        
        # ===== General Settings =====
        general_group = QGroupBox("Cài Đặt Chung")
        general_layout = QVBoxLayout(general_group)
        general_layout.setContentsMargins(12, 20, 12, 12)
        general_layout.setSpacing(8)
        
        checkbox_style = """
            QCheckBox {
                color: #e2e8f0;
                font-size: 12px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #4a5568;
                border-radius: 4px;
                background: #1a202c;
            }
            QCheckBox::indicator:checked {
                background: #ed8936;
                border-color: #ed8936;
            }
        """
        
        self.auto_save = QCheckBox("Tự động lưu kết quả")
        self.auto_save.setChecked(True)
        self.auto_save.setStyleSheet(checkbox_style)
        general_layout.addWidget(self.auto_save)
        
        self.dark_mode = QCheckBox("Chế độ tối (Dark Mode)")
        self.dark_mode.setStyleSheet(checkbox_style)
        general_layout.addWidget(self.dark_mode)
        
        layout.addWidget(general_group)
        
        # ===== Buttons =====
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setFixedHeight(42)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #4a5568;
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 25px;
            }
            QPushButton:hover { background: #718096; }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Lưu Cài Đặt")
        save_btn.setFixedHeight(42)
        save_btn.setStyleSheet("""
            QPushButton {
                background: #ed8936;
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 25px;
            }
            QPushButton:hover { background: #f6ad55; }
        """)
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def get_config_path(self):
        """Get config file path in user's app data"""
        if sys.platform == 'win32':
            config_dir = Path(os.environ.get('APPDATA', '')) / 'IELTSAnalyzer'
        else:
            config_dir = Path.home() / '.ielts_analyzer'
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / CONFIG_FILE
    
    def load_settings(self):
        """Load settings from config file"""
        config_path = self.get_config_path()
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.openai_key.setText(config.get('openai_api_key', ''))
                self.anthropic_key.setText(config.get('anthropic_api_key', ''))
                self.gemini_key.setText(config.get('gemini_api_key', ''))
                self.ai_provider.setCurrentIndex(config.get('ai_provider_index', 0))
                self.auto_save.setChecked(config.get('auto_save', True))
                self.dark_mode.setChecked(config.get('dark_mode', False))
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to config file"""
        config = {
            'openai_api_key': self.openai_key.text(),
            'anthropic_api_key': self.anthropic_key.text(),
            'gemini_api_key': self.gemini_key.text(),
            'ai_provider_index': self.ai_provider.currentIndex(),
            'ai_provider': self.ai_provider.currentText(),
            'auto_save': self.auto_save.isChecked(),
            'dark_mode': self.dark_mode.isChecked()
        }
        
        config_path = self.get_config_path()
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            QMessageBox.information(
                self, 
                "Thành công", 
                "✅ Đã lưu cài đặt thành công!"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Lỗi", 
                f"❌ Không thể lưu cài đặt:\n{str(e)}"
            )
    
    def toggle_openai_visibility(self, checked):
        """Toggle OpenAI key visibility"""
        if checked:
            self.openai_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_openai_btn.setText("🙈 Ẩn")
        else:
            self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_openai_btn.setText("👁️ Hiện")
    
    def toggle_anthropic_visibility(self, checked):
        """Toggle Anthropic key visibility"""
        if checked:
            self.anthropic_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_anthropic_btn.setText("🙈 Ẩn")
        else:
            self.anthropic_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_anthropic_btn.setText("👁️ Hiện")
    
    def toggle_gemini_visibility(self, checked):
        """Toggle Gemini key visibility"""
        if checked:
            self.gemini_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_gemini_btn.setText("🙈 Ẩn")
        else:
            self.gemini_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_gemini_btn.setText("👁️ Hiện")
    
    def get_settings(self):
        """Return current settings as dict"""
        return {
            'openai_api_key': self.openai_key.text(),
            'anthropic_api_key': self.anthropic_key.text(),
            'gemini_api_key': self.gemini_key.text(),
            'ai_provider_index': self.ai_provider.currentIndex(),
            'ai_provider': self.ai_provider.currentText(),
            'auto_save': self.auto_save.isChecked(),
            'dark_mode': self.dark_mode.isChecked()
        }


# =============================================================================
# AI ANALYSIS WORKER
# =============================================================================

class AIAnalysisWorker(QThread):
    """Background worker for AI analysis"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, scores, student_name, settings):
        super().__init__()
        self.scores = scores
        self.student_name = student_name
        self.settings = settings
    
    def run(self):
        try:
            self.progress.emit(20)
            
            # Get AI provider settings
            provider_index = self.settings.get('ai_provider_index', 0)
            
            if provider_index == 0:
                # Rule-based only
                analysis = self.analyze_rule_based()
            else:
                # Try AI analysis
                self.progress.emit(40)
                analysis = self.analyze_with_ai(provider_index)
            
            self.progress.emit(100)
            self.finished.emit(analysis)
            
        except Exception as e:
            self.error.emit(str(e))
    
    def analyze_rule_based(self):
        """Rule-based IELTS analysis"""
        scores = self.scores
        student_name = self.student_name
        
        # Calculate overall
        total = sum(scores.values())
        overall = round((total / 4) * 2) / 2
        
        # Create skill array
        skills = [
            {'name': 'listening', 'score': scores['listening'], 'label': SKILL_NAMES['listening']},
            {'name': 'speaking', 'score': scores['speaking'], 'label': SKILL_NAMES['speaking']},
            {'name': 'reading', 'score': scores['reading'], 'label': SKILL_NAMES['reading']},
            {'name': 'writing', 'score': scores['writing'], 'label': SKILL_NAMES['writing']}
        ]
        
        # Sort and categorize
        sorted_skills = sorted(skills, key=lambda x: x['score'], reverse=True)
        strengths = [s for s in sorted_skills if s['score'] >= overall]
        weaknesses = [s for s in sorted_skills if s['score'] < overall]
        
        # Generate summary
        summary = f"Học viên {student_name} đạt điểm IELTS tổng thể {overall}. "
        
        if strengths:
            strength_names = [s['label'].split(' ')[0] for s in strengths]
            summary += f"Có khả năng {' và '.join(strength_names)} tốt"
            if strengths[0]['score'] >= 7:
                summary += f" với điểm nổi bật ở kỹ năng {strengths[0]['label'].split(' ')[0]} ({strengths[0]['score']})."
            else:
                summary += "."
        
        if weaknesses:
            weakness_names = [w['label'].split(' ')[0] for w in weaknesses]
            summary += f" Tuy nhiên, {' và '.join(weakness_names)} còn hạn chế do chưa thường xuyên luyện tập."
        
        # Generate recommendations
        recommendations = []
        for skill in weaknesses:
            level = 'high' if skill['score'] >= 7 else ('medium' if skill['score'] >= 5 else 'low')
            recs = RECOMMENDATIONS[skill['name']][level]
            recommendations.append({
                'skill': skill['label'],
                'score': skill['score'],
                'items': recs
            })
        
        # Action items
        action_items = []
        if weaknesses:
            weakest = weaknesses[-1]
            action_items.append(
                f"Ưu tiên cải thiện {weakest['label'].split(' ')[0]} "
                f"(hiện tại: {weakest['score']}, mục tiêu: {min(9, weakest['score'] + 1)})"
            )
        
        action_items.extend([
            f"Đặt mục tiêu đạt {min(9, overall + 0.5)} trong 3 tháng",
            "Luyện tập 2 tiếng mỗi ngày với kỹ năng yếu",
            "Làm mock test 2 tuần/lần để theo dõi tiến độ"
        ])
        
        band = int(overall)
        band_desc = BAND_DESCRIPTIONS.get(max(1, min(9, band)), "")
        
        return {
            'student_name': student_name,
            'overall': overall,
            'band_description': band_desc,
            'skills': skills,
            'strengths': [{'skill': s['label'], 'score': s['score']} for s in strengths],
            'weaknesses': [{'skill': w['label'], 'score': w['score']} for w in weaknesses],
            'summary': summary,
            'recommendations': recommendations,
            'action_items': action_items,
            'ai_analysis': None,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def analyze_with_ai(self, provider_index):
        """Analyze with AI (GPT-4 or Claude)"""
        base_analysis = self.analyze_rule_based()
        
        prompt = f"""Bạn là chuyên gia tư vấn IELTS. Phân tích điểm IELTS của học viên:

Tên: {self.student_name}
Listening: {self.scores['listening']}
Speaking: {self.scores['speaking']}
Reading: {self.scores['reading']}
Writing: {self.scores['writing']}

Đưa ra:
1. Nhận xét tổng thể (2-3 câu)
2. Điểm mạnh và yếu
3. Đề xuất cụ thể để cải thiện kỹ năng yếu
4. Kế hoạch học tập 1-3 tháng

Trả lời ngắn gọn, thực tế bằng tiếng Việt."""

        ai_response = None
        
        try:
            if provider_index in [1, 2]:  # OpenAI
                ai_response = self.call_openai(prompt, provider_index)
            elif provider_index in [3, 4]:  # Anthropic
                ai_response = self.call_anthropic(prompt, provider_index)
            elif provider_index in [5, 6]:  # Google Gemini
                ai_response = self.call_gemini(prompt, provider_index)
        except Exception as e:
            ai_response = f"⚠️ Không thể kết nối AI: {str(e)}"
        
        base_analysis['ai_analysis'] = ai_response
        return base_analysis
    
    def call_openai(self, prompt, provider_index):
        """Call OpenAI API"""
        try:
            from openai import OpenAI
            
            api_key = self.settings.get('openai_api_key', '')
            if not api_key:
                return "⚠️ Chưa cấu hình OpenAI API Key. Vào Settings để thêm."
            
            client = OpenAI(api_key=api_key)
            model = "gpt-4" if provider_index == 1 else "gpt-3.5-turbo"
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia tư vấn IELTS."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return "⚠️ Chưa cài đặt thư viện OpenAI. Chạy: pip install openai"
        except Exception as e:
            return f"⚠️ Lỗi OpenAI: {str(e)}"
    
    def call_anthropic(self, prompt, provider_index):
        """Call Anthropic API"""
        try:
            from anthropic import Anthropic
            
            api_key = self.settings.get('anthropic_api_key', '')
            if not api_key:
                return "⚠️ Chưa cấu hình Anthropic API Key. Vào Settings để thêm."
            
            client = Anthropic(api_key=api_key)
            model = "claude-3-sonnet-20240229" if provider_index == 3 else "claude-3-haiku-20240307"
            
            response = client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except ImportError:
            return "⚠️ Chưa cài đặt thư viện Anthropic. Chạy: pip install anthropic"
        except Exception as e:
            return f"⚠️ Lỗi Anthropic: {str(e)}"
    
    def call_gemini(self, prompt, provider_index):
        """Call Google Gemini API using new google-genai package"""
        try:
            from google import genai
            from google.genai import types
            
            api_key = self.settings.get('gemini_api_key', '')
            if not api_key:
                return "⚠️ Chưa cấu hình Google Gemini API Key. Vào Settings để thêm."
            
            # Create client with API key
            client = genai.Client(api_key=api_key)
            
            # First, try to list available models
            available_models = []
            try:
                for model in client.models.list():
                    if hasattr(model, 'name') and 'gemini' in model.name.lower():
                        available_models.append(model.name)
            except:
                pass
            
            # If we found available models, use the first one that supports generation
            if available_models:
                # Prefer flash models for speed
                preferred_order = ['flash', '2.0', '1.5', 'pro']
                sorted_models = []
                for pref in preferred_order:
                    for m in available_models:
                        if pref in m.lower() and m not in sorted_models:
                            sorted_models.append(m)
                
                # Add remaining models
                for m in available_models:
                    if m not in sorted_models:
                        sorted_models.append(m)
                
                models_to_try = sorted_models[:5]  # Try first 5
            else:
                # Fallback to known model names
                models_to_try = [
                    "models/gemini-2.0-flash-exp",
                    "models/gemini-1.5-flash",
                    "models/gemini-1.5-pro",
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-flash",
                    "gemini-1.5-pro"
                ]
            
            # Try each model until one works
            last_error = None
            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    if response and response.text:
                        return response.text
                except Exception as e:
                    last_error = e
                    continue
            
            # If all models failed, show available models info
            models_info = ", ".join(available_models[:5]) if available_models else "Không tìm thấy"
            return f"⚠️ Không thể kết nối Gemini.\nModels khả dụng: {models_info}\nLỗi: {str(last_error)}"
            
        except ImportError:
            return "⚠️ Chưa cài đặt thư viện Google GenAI. Chạy: pip install google-genai"
        except Exception as e:
            return f"⚠️ Lỗi Google Gemini: {str(e)}"


# =============================================================================
# MAIN WINDOW
# =============================================================================

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"🎓 {APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1100, 750)
        self.current_analysis = None
        self.settings = self.load_settings()
        
        self.setup_ui()
        self.apply_theme()
    
    def load_settings(self):
        """Load settings from config file"""
        if sys.platform == 'win32':
            config_dir = Path(os.environ.get('APPDATA', '')) / 'IELTSAnalyzer'
        else:
            config_dir = Path.home() / '.ielts_analyzer'
        
        config_path = config_dir / CONFIG_FILE
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {}
    
    def setup_ui(self):
        """Setup the user interface"""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QWidget()
        self.header_widget = header  # Store reference for theme switching
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #1e3a5f, stop:0.5 #3d5a80, stop:1 #98c1d9);
            padding: 20px;
        """)
        header_layout = QHBoxLayout(header)
        
        title_label = QLabel("🎓 IELTS Score Analyzer")
        title_label.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: white;
        """)
        
        subtitle = QLabel("AI-Powered Document Summarizer")
        subtitle.setStyleSheet("color: #e0fbfc; font-size: 11pt;")
        
        title_container = QVBoxLayout()
        title_container.addWidget(title_label)
        title_container.addWidget(subtitle)
        
        settings_btn = QPushButton("⚙️ CÀI ĐẶT")
        settings_btn.setMinimumHeight(45)
        settings_btn.setMaximumWidth(150)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: #2a9d8f;
                color: white;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #3ab5a6;
            }
            QPushButton:pressed {
                background: #1e7d72;
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        header_layout.addWidget(settings_btn)
        
        main_layout.addWidget(header)
        
        # Content area with tabs
        content = QWidget()
        self.content_widget = content  # Store reference for theme switching
        content.setStyleSheet("background: #f5f7fa;")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Left panel - Input
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        input_group = QGroupBox("📝 Nhập Điểm IELTS")
        input_layout = QFormLayout(input_group)
        input_layout.setSpacing(15)
        
        # Student info
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Nhập tên học viên...")
        input_layout.addRow("👤 Tên học viên:", self.student_name)
        
        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("Mã học viên (tùy chọn)")
        input_layout.addRow("🆔 Mã học viên:", self.student_id)
        
        # Score inputs
        self.listening_score = QDoubleSpinBox()
        self.listening_score.setRange(0, 9)
        self.listening_score.setSingleStep(0.5)
        self.listening_score.setDecimals(1)
        input_layout.addRow("🎧 Listening:", self.listening_score)
        
        self.speaking_score = QDoubleSpinBox()
        self.speaking_score.setRange(0, 9)
        self.speaking_score.setSingleStep(0.5)
        self.speaking_score.setDecimals(1)
        input_layout.addRow("🗣️ Speaking:", self.speaking_score)
        
        self.reading_score = QDoubleSpinBox()
        self.reading_score.setRange(0, 9)
        self.reading_score.setSingleStep(0.5)
        self.reading_score.setDecimals(1)
        input_layout.addRow("📖 Reading:", self.reading_score)
        
        self.writing_score = QDoubleSpinBox()
        self.writing_score.setRange(0, 9)
        self.writing_score.setSingleStep(0.5)
        self.writing_score.setDecimals(1)
        input_layout.addRow("✍️ Writing:", self.writing_score)
        
        # AI option
        self.use_ai = QCheckBox("🤖 Sử dụng AI để phân tích (cần API key)")
        input_layout.addRow(self.use_ai)
        
        left_layout.addWidget(input_group)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        left_layout.addWidget(self.progress)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("🔍 PHÂN TÍCH")
        analyze_btn.setMinimumHeight(50)
        analyze_btn.setStyleSheet("""
            QPushButton {
                background: #ee6c4d;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background: #f4a261;
            }
            QPushButton:pressed {
                background: #d95d3f;
            }
        """)
        analyze_btn.clicked.connect(self.analyze)
        
        reset_btn = QPushButton("🔄 LÀM MỚI")
        reset_btn.setMinimumHeight(50)
        reset_btn.setStyleSheet("""
            QPushButton {
                background: #3d5a80;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background: #4a6fa5;
            }
            QPushButton:pressed {
                background: #2d4a70;
            }
        """)
        reset_btn.clicked.connect(self.reset_form)
        
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(analyze_btn)
        left_layout.addLayout(btn_layout)
        
        left_layout.addStretch()
        
        # Export button
        export_btn = QPushButton("📥 XUẤT BÁO CÁO")
        export_btn.setMinimumHeight(45)
        export_btn.setStyleSheet("""
            QPushButton {
                background: #2a9d8f;
                color: white;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
            }
            QPushButton:hover {
                background: #3ab5a6;
            }
            QPushButton:pressed {
                background: #1e7d72;
            }
        """)
        export_btn.clicked.connect(self.export_report)
        left_layout.addWidget(export_btn)
        
        left_panel.setMaximumWidth(400)
        content_layout.addWidget(left_panel)
        
        # Right panel - Results
        self.results_tabs = QTabWidget()
        
        # Dark theme style for text areas
        text_area_style = """
            QTextEdit {
                background: #1a202c;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 8px;
                padding: 10px;
                font-size: 11pt;
            }
        """
        
        # Summary tab
        summary_tab = QWidget()
        summary_layout = QVBoxLayout(summary_tab)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet(text_area_style)
        self.results_text.setPlaceholderText(
            "Kết quả phân tích sẽ hiển thị ở đây...\n\n"
            "📝 Nhập điểm IELTS 4 kỹ năng và nhấn 'Phân Tích' để bắt đầu."
        )
        summary_layout.addWidget(self.results_text)
        
        self.results_tabs.addTab(summary_tab, "📊 Kết Quả")
        
        # Recommendations tab
        rec_tab = QWidget()
        rec_layout = QVBoxLayout(rec_tab)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setStyleSheet(text_area_style)
        rec_layout.addWidget(self.recommendations_text)
        
        self.results_tabs.addTab(rec_tab, "🎯 Đề Xuất")
        
        # AI Analysis tab
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        
        self.ai_text = QTextEdit()
        self.ai_text.setReadOnly(True)
        self.ai_text.setStyleSheet(text_area_style)
        self.ai_text.setPlaceholderText(
            "Phân tích AI sẽ hiển thị ở đây...\n\n"
            "Bật tùy chọn 'Sử dụng AI' và cấu hình API key trong Settings."
        )
        ai_layout.addWidget(self.ai_text)
        
        self.results_tabs.addTab(ai_tab, "🤖 AI Analysis")
        
        content_layout.addWidget(self.results_tabs, 1)
        
        main_layout.addWidget(content, 1)
        
        # Status bar
        self.statusBar().showMessage("Sẵn sàng | Ready")
        self.statusBar().setStyleSheet("background: #1e3a5f; color: white; padding: 5px;")
    
    def apply_theme(self):
        """Apply light or dark theme based on settings"""
        is_dark = self.settings.get('dark_mode', False)
        if is_dark:
            self.setStyleSheet(DARK_STYLESHEET)
            # Update header for dark mode
            if hasattr(self, 'header_widget'):
                self.header_widget.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                    padding: 20px;
                """)
            if hasattr(self, 'content_widget'):
                self.content_widget.setStyleSheet("background: #1a1a2e;")
        else:
            self.setStyleSheet(STYLESHEET)
            if hasattr(self, 'header_widget'):
                self.header_widget.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #1e3a5f, stop:0.5 #3d5a80, stop:1 #98c1d9);
                    padding: 20px;
                """)
            if hasattr(self, 'content_widget'):
                self.content_widget.setStyleSheet("background: #f5f7fa;")
    
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self)
        if dialog.exec():
            self.settings = dialog.get_settings()
            self.apply_theme()
            self.statusBar().showMessage("✅ Đã cập nhật cài đặt")
    
    def analyze(self):
        """Analyze IELTS scores"""
        name = self.student_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập tên học viên!")
            return
        
        scores = {
            'listening': self.listening_score.value(),
            'speaking': self.speaking_score.value(),
            'reading': self.reading_score.value(),
            'writing': self.writing_score.value()
        }
        
        # Check if all scores are 0
        if all(v == 0 for v in scores.values()):
            QMessageBox.warning(self, "Thiếu điểm", "Vui lòng nhập điểm cho ít nhất một kỹ năng!")
            return
        
        # Update settings with AI preference
        settings = self.settings.copy()
        if not self.use_ai.isChecked():
            settings['ai_provider_index'] = 0
        
        # Show progress
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.statusBar().showMessage("🔄 Đang phân tích...")
        
        # Run analysis in background
        self.worker = AIAnalysisWorker(scores, name, settings)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_analysis_complete)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()
    
    def on_analysis_complete(self, analysis):
        """Handle analysis completion"""
        self.current_analysis = analysis
        self.progress.setVisible(False)
        self.statusBar().showMessage("✅ Phân tích hoàn tất!")
        
        # Display results
        self.display_results(analysis)
    
    def on_analysis_error(self, error_msg):
        """Handle analysis error"""
        self.progress.setVisible(False)
        self.statusBar().showMessage("❌ Lỗi phân tích")
        QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi:\n{error_msg}")
    
    def display_results(self, analysis):
        """Display analysis results - Dark theme compatible"""
        # Summary tab with dark theme colors
        html = f"""
        <div style="font-family: Segoe UI; line-height: 1.8; padding: 10px; color: #e2e8f0;">
            <h2 style="color: #f6ad55; border-bottom: 3px solid #ed8936; padding-bottom: 10px;">
                📊 Kết Quả Phân Tích IELTS
            </h2>
            
            <div style="background: #2d3748; 
                        color: white; padding: 25px; border-radius: 12px; 
                        text-align: center; margin: 20px 0; border: 2px solid #4a5568;">
                <div style="font-size: 14pt; color: #a0aec0;">Điểm Tổng Thể</div>
                <div style="font-size: 48pt; font-weight: bold; color: #f6ad55;">{analysis['overall']}</div>
                <div style="font-size: 11pt; color: #a0aec0;">{analysis['band_description']}</div>
            </div>
            
            <h3 style="color: #f6ad55;">📈 Chi Tiết Điểm:</h3>
            <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
        """
        
        for skill in analysis['skills']:
            bar_width = int((skill['score'] / 9) * 100)
            color = '#48bb78' if skill['score'] >= 7 else ('#f6ad55' if skill['score'] >= 5 else '#fc8181')
            html += f"""
                <tr style="background: #2d3748; border-radius: 8px;">
                    <td style="padding: 12px; font-weight: bold; color: #e2e8f0;">{skill['label']}</td>
                    <td style="padding: 12px; font-size: 18pt; color: {color}; font-weight: bold;">{skill['score']}</td>
                    <td style="padding: 12px; width: 50%;">
                        <div style="background: #1a202c; border-radius: 5px; height: 14px;">
                            <div style="background: {color}; width: {bar_width}%; 
                                        height: 100%; border-radius: 5px;"></div>
                        </div>
                    </td>
                </tr>
            """
        
        html += f"""
            </table>
            
            <h3 style="color: #f6ad55;">📋 Tóm Tắt Đánh Giá:</h3>
            <div style="background: #2d3748; border-left: 4px solid #ed8936; 
                        padding: 15px; border-radius: 8px; margin: 15px 0; color: #e2e8f0;">
                {analysis['summary']}
            </div>
            
            <h3 style="color: #48bb78;">💪 Điểm Mạnh:</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
        """
        
        for s in analysis['strengths']:
            html += f"""
                <li style="background: #2d3748; padding: 12px 15px; color: #e2e8f0;
                           margin: 8px 0; border-radius: 8px; border-left: 4px solid #48bb78;">
                    ✓ {s['skill']}: <strong style="color: #48bb78;">{s['score']}</strong>
                </li>
            """
        
        html += """
            </ul>
            
            <h3 style="color: #fc8181;">📉 Điểm Cần Cải Thiện:</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
        """
        
        for w in analysis['weaknesses']:
            html += f"""
                <li style="background: #2d3748; padding: 12px 15px; color: #e2e8f0;
                           margin: 8px 0; border-radius: 8px; border-left: 4px solid #fc8181;">
                    ⚠ {w['skill']}: <strong style="color: #fc8181;">{w['score']}</strong>
                </li>
            """
        
        html += """
            </ul>
            
            <h3 style="color: #f6ad55;">📌 Kế Hoạch Hành Động:</h3>
            <div style="background: #2d3748; border: 2px solid #ed8936;
                        padding: 20px; border-radius: 12px;">
                <ol style="margin: 0; padding-left: 25px; color: #e2e8f0;">
        """
        
        for action in analysis['action_items']:
            html += f"<li style='margin: 10px 0; color: #e2e8f0;'>{action}</li>"
        
        html += """
                </ol>
            </div>
        </div>
        """
        
        self.results_text.setHtml(html)
        
        # Recommendations tab - with better contrast
        rec_html = """
        <div style="font-family: Segoe UI; line-height: 1.8; padding: 10px;">
            <h2 style="color: #f6ad55; border-bottom: 3px solid #ed8936; padding-bottom: 10px; margin-bottom: 20px;">
                🎯 Đề Xuất Cải Thiện Chi Tiết
            </h2>
        """
        
        for rec in analysis['recommendations']:
            rec_html += f"""
            <div style="background: #2d3748; border-radius: 12px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #ed8936;">
                <h3 style="color: #f6ad55; margin: 0 0 15px 0; font-size: 16px;">
                    📌 {rec['skill']} (Điểm: {rec['score']})
                </h3>
                <ul style="margin: 0; padding-left: 20px;">
            """
            
            for item in rec['items']:
                rec_html += f"""
                    <li style="color: #e2e8f0; margin: 12px 0; padding: 8px 12px; 
                               background: #1a202c; border-radius: 6px; list-style: none;">
                        ✓ {item}
                    </li>
                """
            
            rec_html += "</ul></div>"
        
        rec_html += "</div>"
        self.recommendations_text.setHtml(rec_html)
        
        # AI Analysis tab - with better contrast
        if analysis.get('ai_analysis'):
            ai_html = f"""
            <div style="font-family: Segoe UI; line-height: 1.8; padding: 10px;">
                <h2 style="color: #f6ad55; border-bottom: 3px solid #ed8936; padding-bottom: 10px; margin-bottom: 20px;">
                    🤖 Phân Tích Từ AI
                </h2>
                <div style="background: #2d3748; color: #e2e8f0;
                            padding: 20px; border-radius: 12px; margin: 10px 0;
                            border: 2px solid #4a5568;">
                    {analysis['ai_analysis'].replace(chr(10), '<br>')}
                </div>
            </div>
            """
            self.ai_text.setHtml(ai_html)
        else:
            self.ai_text.setPlaceholderText(
                "Không có phân tích AI.\n\n"
                "Để sử dụng AI:\n"
                "1. Vào Settings (⚙️) và thêm API key\n"
                "2. Bật tùy chọn 'Sử dụng AI để phân tích'\n"
                "3. Nhấn 'Phân Tích' lại"
            )
    
    def reset_form(self):
        """Reset the form"""
        self.student_name.clear()
        self.student_id.clear()
        self.listening_score.setValue(0)
        self.speaking_score.setValue(0)
        self.reading_score.setValue(0)
        self.writing_score.setValue(0)
        self.use_ai.setChecked(False)
        self.results_text.clear()
        self.recommendations_text.clear()
        self.ai_text.clear()
        self.current_analysis = None
        self.statusBar().showMessage("🔄 Đã làm mới form")
    
    def export_report(self):
        """Export analysis report"""
        if not self.current_analysis:
            QMessageBox.warning(self, "Chưa có dữ liệu", "Vui lòng phân tích điểm trước khi xuất báo cáo!")
            return
        
        analysis = self.current_analysis
        
        # Generate report
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           IELTS SCORE ANALYSIS REPORT                        ║
║           BÁO CÁO PHÂN TÍCH ĐIỂM IELTS                       ║
╚══════════════════════════════════════════════════════════════╝

📅 Ngày phân tích: {datetime.now().strftime('%d/%m/%Y %H:%M')}
👤 Học viên: {analysis['student_name']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ĐIỂM TỔNG THỂ: {analysis['overall']}
   {analysis['band_description']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 CHI TIẾT ĐIỂM:
"""
        
        for skill in analysis['skills']:
            bar_length = int(skill['score'] / 9 * 20)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            report += f"   • {skill['label']}: {skill['score']} [{bar}]\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 TÓM TẮT ĐÁNH GIÁ:
{analysis['summary']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 ĐIỂM MẠNH:
"""
        for s in analysis['strengths']:
            report += f"   ✓ {s['skill']}: {s['score']}\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📉 ĐIỂM CẦN CẢI THIỆN:
"""
        for w in analysis['weaknesses']:
            report += f"   ⚠ {w['skill']}: {w['score']}\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 ĐỀ XUẤT CẢI THIỆN:
"""
        for rec in analysis['recommendations']:
            report += f"\n   📌 {rec['skill']}:\n"
            for item in rec['items']:
                report += f"      → {item}\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 KẾ HOẠCH HÀNH ĐỘNG:
"""
        for i, action in enumerate(analysis['action_items'], 1):
            report += f"   {i}. {action}\n"
        
        if analysis.get('ai_analysis'):
            report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 PHÂN TÍCH AI:
{analysis['ai_analysis']}
"""
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Báo cáo được tạo bởi IELTS Score Analyzer - AI Document Summarizer
"""
        
        # Save file dialog
        default_name = f"IELTS_Report_{analysis['student_name']}_{datetime.now().strftime('%Y%m%d')}.txt"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Lưu Báo Cáo",
            default_name,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                QMessageBox.information(self, "Thành công", f"✅ Đã xuất báo cáo:\n{file_path}")
                self.statusBar().showMessage(f"✅ Đã xuất báo cáo: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"❌ Không thể lưu file:\n{str(e)}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set app info
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("IELTS Analyzer")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec() if PYQT_VERSION == 6 else app.exec_())


if __name__ == '__main__':
    main()

