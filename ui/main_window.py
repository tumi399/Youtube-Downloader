import os
import requests
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QProgressBar, QTextEdit,
    QFrame, QFileDialog, QGraphicsDropShadowEffect
)

from ui.styles import MAIN_STYLE
from core.downloader import InfoFetcherThread, DownloadWorkerThread
from utils.helpers import load_download_path, save_download_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setFixedSize(480, 830)  # Tăng chiều cao để vừa ô input mới
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.old_pos = None
        self.current_info = None
        self.log_line_count = 0

        # Đọc đường dẫn từ config.json
        self.download_path = load_download_path()

        self.setup_ui()
        self.setStyleSheet(MAIN_STYLE)

    def setup_ui(self):
        container = QWidget(self)
        container.setObjectName("CentralWidget")
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(28, 20, 28, 28)
        main_layout.setSpacing(12)

        # 1. Các nút điều khiển cửa sổ macOS (Close, Minimize, Zoom)
        dot_layout = QHBoxLayout()
        dot_layout.setSpacing(8)

        # Nút Đóng (Màu đỏ)
        self.btn_close = QPushButton()
        self.btn_close.setObjectName("CloseButton")
        self.btn_close.setFixedSize(12, 12)
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.setToolTip("Đóng ứng dụng")
        self.btn_close.clicked.connect(self.close_application)

        # Nút Thu nhỏ xuống Taskbar (Màu vàng)
        self.btn_minimize = QPushButton()
        self.btn_minimize.setObjectName("MinimizeButton")
        self.btn_minimize.setFixedSize(12, 12)
        self.btn_minimize.setCursor(Qt.PointingHandCursor)
        self.btn_minimize.setToolTip("Thu nhỏ")
        self.btn_minimize.clicked.connect(self.showMinimized)

        # Nút Xanh lá (Giữ nguyên phong cách macOS)
        self.btn_zoom = QPushButton()
        self.btn_zoom.setObjectName("ZoomButton")
        self.btn_zoom.setFixedSize(12, 12)

        dot_layout.addWidget(self.btn_close)
        dot_layout.addWidget(self.btn_minimize)
        dot_layout.addWidget(self.btn_zoom)
        dot_layout.addStretch()
        main_layout.addLayout(dot_layout)

        # 2. Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(4)

        title_h_layout = QHBoxLayout()
        title_h_layout.setAlignment(Qt.AlignCenter)
        title_h_layout.setSpacing(8)

        yt_icon = QLabel("▶")
        yt_icon.setStyleSheet("color: #ff1c3e; font-size: 20px; font-weight: bold;")
        title_text = QLabel("YouTube Downloader")
        title_text.setStyleSheet("font-size: 22px; font-weight: 800;")
        title_h_layout.addWidget(yt_icon)
        title_h_layout.addWidget(title_text)

        sub_title = QLabel("Phần mềm tải video & âm thanh chất lượng cao")
        sub_title.setObjectName("SubTitle")
        sub_title.setAlignment(Qt.AlignCenter)

        header_layout.addLayout(title_h_layout)
        header_layout.addWidget(sub_title)
        main_layout.addLayout(header_layout)

        # 3. URL Input
        url_label_layout = QHBoxLayout()
        url_label_layout.setSpacing(6)
        link_icon = QLabel("🔗")
        link_icon.setStyleSheet("font-size: 13px;")
        url_title = QLabel("URL VIDEO")
        url_title.setObjectName("FieldLabel")
        url_label_layout.addWidget(link_icon)
        url_label_layout.addWidget(url_title)
        url_label_layout.addStretch()
        main_layout.addLayout(url_label_layout)

        self.url_input = QLineEdit()
        self.url_input.setObjectName("UrlInput")
        self.url_input.setPlaceholderText("https://youtube.com/watch?v=...")
        main_layout.addWidget(self.url_input)

        self.btn_analyze = QPushButton("Phân tích")
        self.btn_analyze.setObjectName("AnalyzeButton")
        self.btn_analyze.clicked.connect(self.start_analyze)
        main_layout.addWidget(self.btn_analyze)

        # 4. Info Card
        self.info_card = QFrame()
        self.info_card.setObjectName("InfoCard")
        info_layout = QHBoxLayout(self.info_card)
        info_layout.setContentsMargins(12, 12, 12, 12)
        info_layout.setSpacing(12)

        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(110, 68)
        self.thumb_label.setStyleSheet("background-color: #12141d; border-radius: 8px;")
        self.thumb_label.setAlignment(Qt.AlignCenter)
        self.thumb_label.setText("▶")

        meta_layout = QVBoxLayout()
        meta_layout.setSpacing(4)
        self.video_title = QLabel("Chưa có video nào được chọn")
        self.video_title.setWordWrap(True)
        self.video_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #ffffff;")

        tag_layout = QHBoxLayout()
        tag_layout.setSpacing(6)
        self.badge_quality = QLabel("HD 1080p")
        self.badge_quality.setStyleSheet(
            "background-color: #432a18; color: #ff9f43; font-size: 11px; "
            "font-weight: 700; border-radius: 4px; padding: 2px 6px;"
        )
        self.duration_label = QLabel("• --:--")
        self.duration_label.setStyleSheet("color: #8b92a5; font-size: 12px;")
        tag_layout.addWidget(self.badge_quality)
        tag_layout.addWidget(self.duration_label)
        tag_layout.addStretch()

        meta_layout.addWidget(self.video_title)
        meta_layout.addLayout(tag_layout)
        info_layout.addWidget(self.thumb_label)
        info_layout.addLayout(meta_layout)
        main_layout.addWidget(self.info_card)

        # 5. Dropdown
        dropdown_layout = QHBoxLayout()
        dropdown_layout.setSpacing(10)

        self.combo_format = QComboBox()
        self.combo_format.addItems(["Format: MP4", "Format: MP3", "Format: Video only"])
        self.combo_format.currentIndexChanged.connect(self.on_format_changed)

        self.combo_quality = QComboBox()
        self.combo_quality.addItems(["Quality: 1080p", "Quality: 720p", "Quality: 480p", "Quality: 360p", "Quality: Best"])

        dropdown_layout.addWidget(self.combo_format, 1)
        dropdown_layout.addWidget(self.combo_quality, 1)
        main_layout.addLayout(dropdown_layout)

        # 6. Status & Progress
        status_row = QHBoxLayout()
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setStyleSheet("color: #8b92a5; font-size: 13px;")
        self.percent_label = QLabel("0%")
        self.percent_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        status_row.addWidget(self.percent_label)
        main_layout.addLayout(status_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 7. Log Frame
        log_frame = QFrame()
        log_frame.setObjectName("LogFrame")
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(12, 8, 12, 8)
        log_layout.setSpacing(4)

        log_head = QHBoxLayout()
        lbl_log_title = QLabel("LOG")
        lbl_log_title.setStyleSheet("font-size: 11px; font-weight: 700; color: #6f778d;")
        self.lbl_lines = QLabel("0 lines")
        self.lbl_lines.setStyleSheet("font-size: 11px; color: #555c70;")
        log_head.addWidget(lbl_log_title)
        log_head.addStretch()
        log_head.addWidget(self.lbl_lines)

        self.log_console = QTextEdit()
        self.log_console.setObjectName("LogConsole")
        self.log_console.setReadOnly(True)

        log_layout.addLayout(log_head)
        log_layout.addWidget(self.log_console)
        main_layout.addWidget(log_frame)

        # =========================================================
        # 8. MỤC MỚI: Ô NHẬP & CHỌN THƯ MỤC LƯU (Ngay trên nút tải)
        # =========================================================
        path_layout = QHBoxLayout()
        path_layout.setSpacing(8)

        self.path_input = QLineEdit()
        self.path_input.setObjectName("PathInput")
        self.path_input.setText(self.download_path)
        self.path_input.setPlaceholderText("Đường dẫn thư mục lưu file...")
        self.path_input.textChanged.connect(self.on_path_manually_edited)

        self.btn_browse = QPushButton("📁 Chọn...")
        self.btn_browse.setObjectName("BrowseButton")
        self.btn_browse.clicked.connect(self.choose_directory)

        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(self.btn_browse)
        main_layout.addLayout(path_layout)
        # =========================================================

        # 9. Nút Tải Xuống
        self.btn_download = QPushButton("  ⭳  TẢI XUỐNG")
        self.btn_download.setObjectName("DownloadButton")
        self.btn_download.clicked.connect(self.start_download)
        main_layout.addWidget(self.btn_download)

        self.setCentralWidget(container)

    def close_application(self):
        """Hủy tiến trình tải nếu đang chạy trước khi đóng cửa sổ"""
        if hasattr(self, 'downloader') and self.downloader.isRunning():
            self.downloader.cancel()
            self.downloader.wait(1000)
        self.close()
    # --- Xử lý đường dẫn & Config ---
    def choose_directory(self):
        """Mở hộp thoại chọn thư mục và lưu vào config.json"""
        initial_dir = self.path_input.text().strip()
        if not os.path.exists(initial_dir):
            initial_dir = os.getcwd()

        selected_dir = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu tải về", initial_dir)
        if selected_dir:
            self.download_path = os.path.abspath(selected_dir)
            self.path_input.setText(self.download_path)
            save_download_path(self.download_path)
            self.append_log(f"[CONFIG] Đã đổi thư mục lưu: {self.download_path}")

    def on_path_manually_edited(self, new_path: str):
        """Khi người dùng gõ tay hoặc dán đường dẫn trực tiếp"""
        cleaned_path = new_path.strip()
        if cleaned_path:
            self.download_path = cleaned_path
            save_download_path(self.download_path)

    # --- Di chuyển cửa sổ Frameless ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def append_log(self, text: str):
        self.log_console.append(text)
        self.log_line_count += 1
        self.lbl_lines.setText(f"{self.log_line_count} lines")

    def on_format_changed(self):
        is_audio = "MP3" in self.combo_format.currentText()
        self.combo_quality.setEnabled(not is_audio)

    def start_analyze(self):
        url = self.url_input.text().strip()
        if not url:
            self.append_log("[ERROR] Vui lòng nhập link YouTube hợp lệ!")
            return

        self.btn_analyze.setEnabled(False)
        self.status_label.setText("Đang lấy thông tin...")
        self.append_log(f"[INFO] Bắt đầu phân tích: {url}")

        self.fetcher = InfoFetcherThread(url)
        self.fetcher.info_fetched.connect(self.on_info_fetched)
        self.fetcher.fetch_failed.connect(self.on_info_failed)
        self.fetcher.start()

    def on_info_fetched(self, info: dict):
        self.btn_analyze.setEnabled(True)
        self.current_info = info
        self.status_label.setText("Đã sẵn sàng")

        title = info.get("title", "Không rõ tiêu đề")
        self.video_title.setText(title)

        duration = info.get("duration", 0)
        minutes = duration // 60
        seconds = duration % 60
        self.duration_label.setText(f"• {minutes:02d}:{seconds:02d}")

        formats = info.get("formats", [])
        heights = sorted(list({f.get("height") for f in formats if f.get("height")}), reverse=True)
        if heights:
            self.badge_quality.setText(f"HD {heights[0]}p")
            self.combo_quality.clear()
            for h in heights:
                self.combo_quality.addItem(f"Quality: {h}p")
            self.combo_quality.addItem("Quality: Best")

        thumb_url = info.get("thumbnail")
        if thumb_url:
            try:
                res = requests.get(thumb_url, timeout=5)
                if res.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(res.content)
                    scaled = pixmap.scaled(110, 68, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                    
                    rounded = QPixmap(110, 68)
                    rounded.fill(Qt.transparent)
                    painter = QPainter(rounded)
                    painter.setRenderHint(QPainter.Antialiasing)
                    path = QPainterPath()
                    path.addRoundedRect(0, 0, 110, 68, 8, 8)
                    painter.setClipPath(path)
                    painter.drawPixmap(0, 0, scaled)
                    painter.end()

                    self.thumb_label.setPixmap(rounded)
            except Exception:
                pass

        self.append_log(f"[INFO] Phân tích hoàn tất: {title[:40]}...")

    def on_info_failed(self, error: str):
        self.btn_analyze.setEnabled(True)
        self.status_label.setText("Lỗi lấy dữ liệu")
        self.append_log(f"[ERROR] Không thể lấy thông tin: {error}")

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.append_log("[ERROR] Chưa có URL video!")
            return

        # Đảm bảo lấy đường dẫn mới nhất từ ô input
        save_dir = self.path_input.text().strip()
        if not save_dir:
            self.append_log("[ERROR] Thư mục lưu không được để trống!")
            return

        fmt = self.combo_format.currentText().replace("Format: ", "").strip()
        qty = self.combo_quality.currentText().replace("Quality: ", "").strip()

        self.btn_download.setEnabled(False)
        self.btn_analyze.setEnabled(False)
        self.progress_bar.setValue(0)
        self.percent_label.setText("0%")

        self.downloader = DownloadWorkerThread(url, fmt, qty, save_dir)
        self.downloader.progress_changed.connect(self.on_download_progress)
        self.downloader.status_changed.connect(self.status_label.setText)
        self.downloader.log_message.connect(self.append_log)
        self.downloader.finished_success.connect(self.on_download_success)
        self.downloader.download_failed.connect(self.on_download_error)
        self.downloader.start()

    def on_download_progress(self, percent: float, speed: str, eta: str):
        int_val = int(percent)
        self.progress_bar.setValue(int_val)
        self.percent_label.setText(f"{int_val}%")
        self.append_log(f"[INFO] Tốc độ: {speed} | Đã tải: {int_val}%")

    def on_download_success(self, path: str):
        self.status_label.setText("Hoàn thành!")
        self.percent_label.setText("100%")
        self.progress_bar.setValue(100)
        self.btn_download.setEnabled(True)
        self.btn_analyze.setEnabled(True)
        self.append_log(f"[SUCCESS] Tải hoàn tất! Lưu tại: {path}")

    def on_download_error(self, error: str):
        self.status_label.setText("Gặp lỗi khi tải")
        self.btn_download.setEnabled(True)
        self.btn_analyze.setEnabled(True)
        self.append_log(f"[ERROR] Thất bại: {error}")