# MapleStory Auto Patrol Bot

Công cụ tự động hóa hỗ trợ tuần tra và đánh quái trong game MapleStory trên nền tảng Windows.
Bot kết hợp việc gửi phím (Hardware/DirectX input qua `pydirectinput`) và nhận diện hình ảnh màn hình cơ bản (OpenCV) để điều hướng nhân vật.

> **⚠️ CẢNH BÁO QUAN TRỌNG VỀ ANTI-CHEAT:**
> Các server MapleStory chính thức thường tích hợp hệ thống chống gian lận cực mạnh. Hãy cân nhắc kỹ trước khi sử dụng bot này trên tài khoản chính của bạn vì nguy cơ bị khóa tài khoản (ban) vĩnh viễn là rất cao.

---

## 📥 Cài đặt và Tải về

Bạn **không cần** phải cài đặt Python hay thư viện phức tạp nếu dùng file `.exe` đã được đóng gói sẵn.

1. Vào trang GitHub của Repository này, chuyển sang tab **Actions**.
2. Bấm vào tiến trình **Build Windows Executable** mới nhất có dấu tick xanh ✅.
3. Cuộn xuống dưới cùng ở phần **Artifacts**, tải về file `MapleBot-Windows`.
4. Giải nén file vừa tải, bạn sẽ nhận được `MapleBot.exe` và `config.json`.

---

## ⚙️ Cấu hình (Config)

Mở file `config.json` bằng Notepad hoặc bất kỳ trình soạn thảo văn bản nào để tùy chỉnh cấu hình phím cho khớp với setting trong game của bạn:

```json
{
  "key_bindings": {
    "attack": "ctrl",       // Phím đánh thường
    "jump": "alt",          // Phím nhảy
    "potion_hp": "pageup",  // Phím bơm máu
    "potion_mp": "pagedown",// Phím bơm mana
    "buff_1": "insert",     // Phím kỹ năng buff
    "move_left": "left",    // Mũi tên trái
    "move_right": "right"   // Mũi tên phải
  },
  "delays": {
    "attack_cooldown": 0.5,
    "buff_cooldown": 120.0, // Thời gian (giây) để tự bấm buff lại
    "min_random_delay": 0.05,
    "max_random_delay": 0.15
  }
}
```

---

## 🚀 Hướng dẫn Sử dụng

1. **Chuẩn bị Game:**
   - Mở MapleStory.
   - Chuyển game sang **Chế độ cửa sổ (Windowed Mode)** để bot nhận diện màn hình tốt hơn.
   - Đưa nhân vật của bạn ra bãi quái.

2. **Chạy Bot:**
   - Đảm bảo file `config.json` nằm **cùng một thư mục** với `MapleBot.exe`.
   - Bấm đúp chuột phải vào `MapleBot.exe` -> Chọn **Run as Administrator** (Điều này bắt buộc để thư viện có thể gửi phím vào trong game thay vì bị hệ thống chặn).

3. **Điều khiển Bot:**
   - Khi cửa sổ đen (Terminal) hiện lên chữ *MapleStory Auto Patrol Bot Initialized*.
   - Bạn chuyển sang cửa sổ game MapleStory.
   - Nhấn phím **F10** để BẮT ĐẦU kích hoạt Auto.
   - Nhấn phím **F12** bất kỳ lúc nào để DỪNG KHẨN CẤP (Kill Switch).

---

## 🛠 Nếu bạn muốn tự chạy từ Source Code (Dành cho Developer)

Nếu bạn không muốn dùng file `.exe` mà muốn tự vọc code và tùy biến thêm (ví dụ gắn thêm template hình ảnh quái vật):

1. Cài đặt Python (phiên bản 3.10 trở lên).
2. Chạy Command Prompt dưới quyền Administrator và di chuyển vào thư mục code.
3. Cài đặt thư viện: `pip install -r requirements.txt`
4. Chạy bot: `python src/main.py`
Hoặc bạn cũng có thể tự build file `.exe` bằng cách chạy file `build_windows.bat`.
