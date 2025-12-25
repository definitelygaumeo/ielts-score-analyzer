"""
Script kiểm tra Gemini API Key
Chạy: python test_gemini.py
"""

import sys

def test_gemini_api():
    print("=" * 50)
    print("🔍 Kiểm tra Google Gemini API")
    print("=" * 50)
    
    # Nhập API key
    api_key = input("\n📝 Nhập Gemini API Key: ").strip()
    
    if not api_key:
        print("❌ Chưa nhập API key!")
        return
    
    try:
        from google import genai
        print("\n✅ Thư viện google-genai đã cài đặt")
    except ImportError:
        print("\n❌ Chưa cài thư viện. Chạy: pip install google-genai")
        return
    
    # Tạo client
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Kết nối thành công")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return
    
    # Liệt kê models
    print("\n📋 Danh sách models khả dụng:")
    print("-" * 40)
    
    available_models = []
    try:
        for model in client.models.list():
            if hasattr(model, 'name'):
                name = model.name
                if 'gemini' in name.lower():
                    available_models.append(name)
                    print(f"  • {name}")
    except Exception as e:
        print(f"❌ Lỗi liệt kê models: {e}")
    
    if not available_models:
        print("  ⚠️ Không tìm thấy model Gemini nào!")
        print("  Có thể API key chưa được kích hoạt hoặc không hợp lệ.")
        return
    
    # Thử generate content
    print("\n🧪 Thử tạo nội dung...")
    print("-" * 40)
    
    test_prompt = "Xin chào! Trả lời ngắn gọn: 1+1=?"
    
    for model_name in available_models[:3]:
        print(f"\n  Thử model: {model_name}")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=test_prompt
            )
            if response and response.text:
                print(f"  ✅ Thành công! Response: {response.text[:100]}")
                print(f"\n🎉 Model hoạt động: {model_name}")
                print(f"📝 Hãy dùng model này trong ứng dụng!")
                return model_name
        except Exception as e:
            print(f"  ❌ Lỗi: {str(e)[:80]}")
    
    print("\n⚠️ Không có model nào hoạt động!")
    print("Vui lòng kiểm tra lại API key hoặc thử tạo key mới.")

if __name__ == "__main__":
    working_model = test_gemini_api()
    print("\n" + "=" * 50)
    input("Nhấn Enter để thoát...")

