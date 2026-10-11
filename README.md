# ▶ YouTube Downloader

Ứng dụng desktop tải video & âm thanh từ YouTube với giao diện hiện đại, được xây dựng bằng **Python** + **PySide6** + **yt-dlp**.

---

## ✨ Tính năng

- 🎬 **Tải video MP4** với chất lượng tùy chọn: 1080p, 720p, 480p, 360p hoặc chất lượng tốt nhất
- 🎵 **Xuất âm thanh MP3** (192kbps) trực tiếp từ video YouTube
- 🎞️ **Tải video-only** (không có âm thanh) theo độ phân giải mong muốn
- 🔍 **Phân tích video** trước khi tải: xem tiêu đề, thời lượng, thumbnail và các độ phân giải khả dụng
- 📁 **Tùy chỉnh thư mục lưu** và tự động ghi nhớ vào `config.json`
- 📊 **Thanh tiến trình real-time**: hiển thị phần trăm, tốc độ tải, ETA
- 🪟 **Giao diện Frameless** phong cách macOS, hỗ trợ kéo thả cửa sổ
- 🔒 **An toàn khi đóng**: tự động hủy tiến trình đang tải trước khi thoát

---

## 🖼️ Giao diện

```
┌─────────────────────────────────────┐
│ ● ● ●                               │
│                                     │
│    ▶  YouTube Downloader           │
│    Phần mềm tải video & âm thanh    │
│                                     │
│  🔗 URL VIDEO                      │
│  [ https://youtube.com/watch?v=... ]│
│  [        Phân tích        ]        │
│                                     │
│  ┌──────────────────────────────┐   │
│  │ 🖼 Thumbnail  Tiêu đề video  │   │
│  │              HD 1080p • 5:32 │   │
│  └──────────────────────────────┘   │
│                                     │
│  [Format: MP4 ▾] [Quality: 1080p ▾] │
│                                     │
│  Sẵn sàng                      0%   │
│  [████████████████████] 100%        │
│                                     │
│  LOG                      0 lines   │
│  ┌──────────────────────────────┐   │
│  │ [INFO] Đang phân tích...     │   │
│  └──────────────────────────────┘   │
│                                     │
│ [ /path/to/downloads ] [📁Chọn...] │
│  [       ⭳  TẢI XUỐNG       ]       │
└─────────────────────────────────────┘
```

---

## 🗂️ Cấu trúc dự án

```
youtube_downloader/
├── main.py                  # Điểm khởi động ứng dụng
├── config.json              # Lưu đường dẫn thư mục tải về
├── requirements.txt         # Các thư viện Python cần thiết
├── YouTubeDownloader.spec   # Cấu hình đóng gói PyInstaller
│
├── core/
│   └── downloader.py        # Luồng tải xuống (InfoFetcherThread, DownloadWorkerThread)
│
├── ui/
│   ├── main_window.py       # Cửa sổ chính & toàn bộ logic UI
│   └── styles.py            # QSS stylesheet của ứng dụng
│
├── utils/
│   ├── helpers.py           # Đọc/ghi config.json
│   └── paths.py             # Hỗ trợ đường dẫn (tương thích PyInstaller)
│
├── assets/
│   └── icons/
│       └── app.ico          # Icon ứng dụng
│
└── bin/
    ├── ffmpeg.exe           # FFmpeg (xử lý hậu kỳ audio/video)
    ├── ffprobe.exe
    └── ffplay.exe
```

---

## ⚙️ Yêu cầu hệ thống

- **OS:** Windows 10/11
- **Python:** 3.10+ *(chỉ cần nếu chạy từ source)*

---

## 🚀 Cài đặt & Chạy

Có **2 cách** để sử dụng ứng dụng:

---

### ⚡ Cách 1 — Tải file `.exe` dùng ngay (Khuyến nghị)

> Không cần cài Python hay bất kỳ thư viện nào.

1. Vào trang **[Releases](https://github.com/your-username/youtube_downloader/releases/latest)**
2. Tải file **`YouTubeDownloader.exe`** về máy
3. Double-click để chạy — xong! 🎉

> **Lưu ý:** Lần đầu chạy Windows Defender có thể cảnh báo SmartScreen. Nhấn **"More info" → "Run anyway"** để tiếp tục (file hoàn toàn an toàn vì được đóng gói từ source code này).

---

### 🐍 Cách 2 — Chạy từ Source Code (dành cho developer)

**Yêu cầu:** Python 3.10+

#### Bước 1 — Clone dự án

```bash
git clone https://github.com/your-username/youtube_downloader.git
cd youtube_downloader
```

#### Bước 2 — Tạo môi trường ảo (khuyến nghị)

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Bước 3 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

#### Bước 4 — Chạy ứng dụng

```bash
python main.py
```

---

## 🛠️ Công nghệ sử dụng

| Thư viện | Phiên bản | Mục đích |
|---|---|---|
| [PySide6](https://pypi.org/project/PySide6/) | 6.11.2 | Framework giao diện đồ họa (Qt6) |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 2026.8.19 | Engine tải video YouTube |
| [Requests](https://pypi.org/project/requests/) | 2.34.2 | Tải thumbnail từ URL |
| [FFmpeg](https://ffmpeg.org/) | — | Xử lý, ghép, chuyển đổi audio/video |

---

## 📋 Hướng dẫn sử dụng

1. **Dán URL** video YouTube vào ô nhập liệu.
2. Nhấn **"Phân tích"** — ứng dụng sẽ lấy thông tin video (tiêu đề, thời lượng, thumbnail, độ phân giải khả dụng).
3. Chọn **Format** (MP4 / MP3 / Video only) và **Quality** mong muốn.
4. Chọn **thư mục lưu** file (hoặc gõ trực tiếp đường dẫn).
5. Nhấn **"⭳ TẢI XUỐNG"** và theo dõi tiến trình trong thanh log.

