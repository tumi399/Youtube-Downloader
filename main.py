import ctypes
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "YouTubeDownloader.App"
    )

    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent
    icon_path = base_dir / "assets" / "icons" / "app.ico"

    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.setWindowIcon(QIcon(str(icon_path)))
    window.show()

    sys.exit(app.exec())