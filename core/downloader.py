
import os
import yt_dlp

from PySide6.QtCore import QThread, Signal
from utils.paths import resource_path


class InfoFetcherThread(QThread):
    info_fetched = Signal(dict)
    fetch_failed = Signal(str)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'ffmpeg_location': str(resource_path('bin')),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.info_fetched.emit(info)

        except Exception as e:
            self.fetch_failed.emit(str(e))


class DownloadWorkerThread(QThread):
    progress_changed = Signal(float, str, str)
    status_changed = Signal(str)
    log_message = Signal(str)
    finished_success = Signal(str)
    download_failed = Signal(str)

    def __init__(
        self,
        url: str,
        format_type: str,
        quality: str,
        download_dir: str
    ):
        super().__init__()

        self.url = url
        self.format_type = format_type
        self.quality = quality
        self.download_dir = download_dir
        self._is_cancelled = False

        # Đường dẫn FFmpeg dùng được khi chạy Python
        # và khi đóng gói bằng PyInstaller.
        self.ffmpeg_dir = resource_path('bin')

    def cancel(self):
        self._is_cancelled = True

    def progress_hook(self, d):
        if self._is_cancelled:
            raise Exception("Tải xuống đã bị hủy bởi người dùng.")

        if d['status'] == 'downloading':
            total_bytes = (
                d.get('total_bytes')
                or d.get('total_bytes_estimate')
                or 0
            )
            downloaded = d.get('downloaded_bytes', 0)

            percent = (
                downloaded / total_bytes * 100
                if total_bytes > 0
                else 0
            )

            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')

            self.progress_changed.emit(percent, speed, eta)
            self.status_changed.emit("Đang tải về...")

        elif d['status'] == 'finished':
            self.status_changed.emit(
                "Đang xử lý hậu kỳ (FFmpeg)..."
            )
            self.log_message.emit(
                "[INFO] Đang đóng gói / xử lý file..."
            )

    def run(self):
        try:
            os.makedirs(self.download_dir, exist_ok=True)

            outtmpl = os.path.join(
                self.download_dir,
                '%(title)s.%(ext)s'
            )

            # Các tùy chọn dùng chung cho mọi chế độ.
            common_opts = {
                'outtmpl': outtmpl,
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': str(self.ffmpeg_dir),
            }

            # 1. Tải và chuyển đổi âm thanh MP3.
            if self.format_type == "MP3":
                ydl_opts = {
                    **common_opts,
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

            # 2. Chỉ tải video, không lấy âm thanh.
            elif self.format_type == "Video only":
                height = self.quality.replace('p', '')

                fmt_str = (
                    f'bestvideo[height<={height}]/bestvideo'
                    if height.isdigit()
                    else 'bestvideo'
                )

                ydl_opts = {
                    **common_opts,
                    'format': fmt_str,
                }

            # 3. Tải video kèm âm thanh, xuất MP4.
            else:
                height = self.quality.replace('p', '')

                if height.isdigit():
                    fmt_str = (
                        f'bestvideo[height<={height}]'
                        f'+bestaudio/'
                        f'best[height<={height}]'
                    )
                else:
                    fmt_str = 'bestvideo+bestaudio/best'

                ydl_opts = {
                    **common_opts,
                    'format': fmt_str,
                    'merge_output_format': 'mp4',
                }

            self.log_message.emit(
                f"[INFO] Bắt đầu xử lý: "
                f"{self.format_type} ({self.quality})"
            )

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            if self._is_cancelled:
                self.download_failed.emit(
                    "Tải xuống đã bị hủy bởi người dùng."
                )
                return

            self.finished_success.emit(self.download_dir)

        except Exception as e:
            self.download_failed.emit(str(e))
