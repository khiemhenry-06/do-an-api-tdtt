import requests
import sys


# Cách dùng: python test_api.py <đường_dẫn_ảnh> [đường_dẫn_API]
# Ví dụ: python test_api.py image.jpg https://cawxc-1-54-49-10.run.pinggy-free.link
# nếu không cung cấp đường dẫn API thì mặc định sẽ dùng http://127.0.0.1:8000
if len(sys.argv) < 2:
    print("Cách dùng: python test_api.py <đường_dẫn_ảnh>")
    print("Ví dụ: python test_api.py image.jpg")
    sys.exit(1)


image_path = sys.argv[1] 
LINK = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8000"
API_URL = f"{LINK}/generate"

try:
    # Đọc ảnh và chuyển thành bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Gọi API với dữ liệu ảnh dưới dạng bytes và nhận phản hồi
    response = requests.post(API_URL, json={"image_bytes": list(image_bytes)})

    if response.status_code == 200: # Nếu gọi API thành công
        print(response.json())
    else:                           # Nếu có lỗi khi gọi API
        print(f"Lỗi khi gọi API: {response.status_code}")
        print(response.text)
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy ảnh tại '{image_path}'")
except Exception as e:
    print(f"Lỗi khi đọc ảnh hoặc gọi API: {str(e)}")
    