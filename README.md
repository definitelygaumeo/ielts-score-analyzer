# 🎓 IELTS Score Analyzer

> AI-Powered Document Summarizer & Learning Recommendations

Ứng dụng Windows Desktop phân tích điểm IELTS và đưa ra đề xuất cải thiện sử dụng AI (GPT-4, Claude, Gemini).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 📊 **Phân tích điểm** | Nhập điểm 4 kỹ năng → Tính điểm tổng thể |
| 💪 **Điểm mạnh/yếu** | Tự động xác định kỹ năng mạnh & cần cải thiện |
| 🎯 **Đề xuất cải thiện** | Gợi ý cụ thể cho từng kỹ năng yếu |
| 📌 **Action Items** | Kế hoạch hành động 1-3 tháng |
| 🤖 **AI Analysis** | Tích hợp GPT-4/Claude/Gemini cho phân tích sâu |
| 📥 **Xuất báo cáo** | Export file báo cáo đầy đủ |
| ⚙️ **Settings** | Lưu trữ API keys an toàn |

## 📸 Screenshots

```
┌──────────────────────────────────────────────────────────────┐
│  🎓 IELTS Score Analyzer                      [⚙️ Cài Đặt]  │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌────────────────────────────────────┐ │
│  │ 📝 Nhập Điểm    │  │ 📊 Kết Quả │ 🎯 Đề Xuất │ 🤖 AI  │ │
│  │                 │  │                                    │ │
│  │ Listening: 7.5  │  │     Điểm Tổng Thể: 6.5            │ │
│  │ Speaking:  6.5  │  │     Good User - Thành thạo        │ │
│  │ Reading:   5.5  │  │                                    │ │
│  │ Writing:   5.0  │  │  ✓ Nghe: 7.5 - Xuất sắc           │ │
│  │                 │  │  ⚠ Viết: 5.0 - Cần cải thiện      │ │
│  │ [🔍 PHÂN TÍCH]  │  │                                    │ │
│  └─────────────────┘  └────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- Windows 10/11

### Cách 1: Cài đặt tự động
```bash
# Clone repository
git clone https://github.com/definitelygaumeo/ielts-score-analyzer.git
cd ielts-score-analyzer

# Chạy script cài đặt
install_dependencies.bat
```

### Cách 2: Cài đặt thủ công
```bash
pip install -r requirements.txt
```

## 💻 Sử dụng

### Chạy ứng dụng
```bash
python ielts_analyzer_app.py
```

Hoặc double-click vào `run_app.bat`

### Cấu hình AI (tùy chọn)
1. Mở ứng dụng → Click **⚙️ Cài Đặt**
2. Nhập API key của AI bạn muốn sử dụng:
   - **OpenAI**: https://platform.openai.com/api-keys
   - **Anthropic**: https://console.anthropic.com/
   - **Google Gemini**: https://aistudio.google.com/apikey
3. Chọn AI Model → Click **Lưu Cài Đặt**

## 📁 Cấu trúc thư mục

```
ielts-analyzer/
├── ielts_analyzer_app.py    # 🖥️ Ứng dụng chính
├── run_app.bat              # ▶️ Script chạy app
├── install_dependencies.bat # 📦 Script cài đặt
├── requirements.txt         # 📋 Dependencies
├── test_gemini.py          # 🧪 Test Gemini API
├── index.html              # 🌐 Web version (standalone)
├── app.py                  # 🌐 Flask backend
└── templates/
    └── index.html          # 🌐 Flask template
```

## 🤖 AI Models hỗ trợ

| Provider | Models | Ghi chú |
|----------|--------|---------|
| OpenAI | GPT-4, GPT-3.5 Turbo | Ổn định, chất lượng cao |
| Anthropic | Claude 3 Sonnet, Haiku | Phân tích sâu |
| Google | Gemini Pro, Flash | Miễn phí |

## 📋 Ví dụ Output

Khi nhập điểm:
- **Listening**: 7.5
- **Speaking**: 6.5  
- **Reading**: 5.5
- **Writing**: 5.0

**Kết quả:**
> *"Học viên Nguyễn Văn A đạt điểm IELTS tổng thể 6.5. Có khả năng Nghe và Nói tốt với điểm nổi bật ở kỹ năng Nghe (7.5). Tuy nhiên, Đọc và Viết còn hạn chế do có thể chưa thường xuyên luyện tập các kỹ năng này."*

**Đề xuất:**
- 📖 **Reading**: Đọc sách báo tiếng Anh hàng ngày
- ✍️ **Writing**: Viết nhật ký bằng tiếng Anh, học cấu trúc bài luận IELTS

## 🛠️ Build executable

Để tạo file .exe chạy độc lập:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed ielts_analyzer_app.py
```

File exe sẽ ở thư mục `dist/`

## 📄 License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo Pull Request hoặc Issue.

## 📧 Liên hệ

Nếu có câu hỏi, vui lòng tạo Issue trên GitHub.

---

⭐ Nếu thấy hữu ích, hãy star repo này!

