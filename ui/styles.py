# ui/styles.py

MAIN_STYLE = """
/* Toàn bộ cửa sổ chính */
QWidget#CentralWidget {
    background-color: #13151f;
    border-radius: 28px;
    border: 1px solid #23273a;
}

/* Các nhãn text */
QLabel {
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

QLabel#SubTitle {
    color: #8b92a5;
    font-size: 13px;
}

QLabel#FieldLabel {
    color: #cad0e0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* Ô nhập liệu URL */
QLineEdit#UrlInput {
    background-color: #1d2030;
    border: 1px solid #282c42;
    border-radius: 12px;
    padding: 10px 16px;
    color: #ffffff;
    font-size: 14px;
    selection-background-color: #ff2b42;
}
QLineEdit#UrlInput:focus {
    border: 1px solid #ff2b42;
}

/* Nút Phân tích */
QPushButton#AnalyzeButton {
    background-color: #272b3f;
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #333852;
}
QPushButton#AnalyzeButton:hover {
    background-color: #323750;
}
QPushButton#AnalyzeButton:pressed {
    background-color: #1e2130;
}
QPushButton#AnalyzeButton:disabled {
    background-color: #1c1e2b;
    color: #555b70;
    border: 1px solid #232636;
}

/* Card thông tin Video */
QFrame#InfoCard {
    background-color: #1d2030;
    border-radius: 16px;
    border: 1px solid #282c40;
}

/* ComboBox Lựa chọn */
QComboBox {
    background-color: #1d2030;
    border: 1px solid #2d3247;
    border-radius: 12px;
    padding: 8px 14px;
    color: #ffffff;
    font-size: 13px;
    font-weight: 500;
}
QComboBox:hover {
    border: 1px solid #3d4461;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left-width: 0px;
}
QComboBox QAbstractItemView {
    background-color: #1d2030;
    border: 1px solid #2d3247;
    border-radius: 8px;
    selection-background-color: #ff2b42;
    selection-color: #ffffff;
    color: #ffffff;
    outline: none;
    padding: 4px;
}

/* Thanh Tiến Trình */
QProgressBar {
    background-color: #1d2030;
    border-radius: 5px;
    height: 9px;
    text-align: right;
}
QProgressBar::chunk {
    background-color: #ff2343;
    border-radius: 5px;
}

/* Hộp Console Log */
QFrame#LogFrame {
    background-color: #151824;
    border-radius: 14px;
    border: 1px solid #222638;
}
QTextEdit#LogConsole {
    background: transparent;
    border: none;
    color: #9299ab;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    line-height: 1.4;
}

/* Nút Tải Xuống Chính */
QPushButton#DownloadButton {
    background-color: #ff1c3e;
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
    border-radius: 14px;
    padding: 14px;
    border: none;
}
QPushButton#DownloadButton:hover {
    background-color: #ff3352;
}
QPushButton#DownloadButton:pressed {
    background-color: #d61330;
}
QPushButton#DownloadButton:disabled {
    background-color: #3b2028;
    color: #7d4d56;
}

/* Ô hiển thị thư mục lưu trữ */
QLineEdit#PathInput {
    background-color: #1a1d2c;
    border: 1px solid #282c42;
    border-radius: 10px;
    padding: 8px 12px;
    color: #cad0e0;
    font-size: 12px;
}
QLineEdit#PathInput:focus {
    border: 1px solid #ff2b42;
}

/* Nút Duyệt thư mục [...] */
QPushButton#BrowseButton {
    background-color: #272b3f;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    border-radius: 10px;
    padding: 8px 12px;
    border: 1px solid #333852;
}
QPushButton#BrowseButton:hover {
    background-color: #343952;
    border: 1px solid #454c6e;
}
QPushButton#BrowseButton:pressed {
    background-color: #1e2130;
}
"""
# Thêm đoạn này vào cuối file ui/styles.py

MAIN_STYLE += """
/* Nút điều khiển macOS dots */
QPushButton#CloseButton {
    background-color: #ff5f56;
    border-radius: 6px;
    border: none;
    color: #4a0002;
    font-size: 8px;
    font-weight: bold;
    text-align: center;
}
QPushButton#CloseButton:hover {
    background-color: #ff3b30;
    color: #4a0002;
}
QPushButton#CloseButton:pressed {
    background-color: #bf2d24;
}

QPushButton#MinimizeButton {
    background-color: #ffbd2e;
    border-radius: 6px;
    border: none;
    color: #593b00;
    font-size: 9px;
    font-weight: bold;
    text-align: center;
}
QPushButton#MinimizeButton:hover {
    background-color: #e0a322;
}

QPushButton#ZoomButton {
    background-color: #27c93f;
    border-radius: 6px;
    border: none;
}
"""