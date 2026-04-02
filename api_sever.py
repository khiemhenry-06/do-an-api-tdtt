from fastapi import FastAPI, HTTPException
import uvicorn
import threading
from api_AI import ImageAnalyzer 

app = FastAPI()             # Tạo ứng dụng FastAPI
api_ai = ImageAnalyzer()    # Khởi tạo module AI để phân tích ảnh

@app.get("/")
async def root(): # Endpoint gốc trả về thông tin về API và các endpoint khác
    return {
        "system": "Đây là hệ thống API demo với FastAPI.",
        "ai image": "Module AI sử dụng mô hình Salesforce/blip-image-captioning-base để phân tích ảnh và tạo mô tả ngắn nhất.",
        "ai translate": "Module AI sử dụng mô hình Helsinki-NLP/opus-mt-en-vi để dịch từ tiếng Anh sang tiếng Việt.",
        "endpoints": {
            "root": "/",
            "health": "/health",
            "generate": "/generate"
        }
    }

@app.get("/health")
def health():    # Endpoint kiểm tra sức khỏe của hệ thống AI
    if api_ai.health_check():
        return {
            "status": "ok",
            "message": "Hệ thống AI đã tải thành công và đang hoạt động!"
        }
    else:
        raise HTTPException(
            status_code=503,
            detail="AI chưa được nạp thành công hoặc đang gặp lỗi."
        )

@app.post("/generate")  
async def generate(data: dict): # Endpoint nhận dữ liệu ảnh và trả về phân tích hoặc lỗi nếu có
    if "image_bytes" not in data:
        return {"error": "Thiếu 'image_bytes' trong yêu cầu."}

    try:
        image_bytes = bytes(data["image_bytes"])
        caption = api_ai.analyze_image(image_bytes)
        return {"Phân tích ảnh thành công": caption}
    except Exception as e:
        return {"error": f"Lỗi khi phân tích ảnh: {str(e)}"}


def run_server(): # Hàm chạy server FastAPI trên cổng 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__": # Chạy server trong một luồng riêng để không bị chặn
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    print("API đang chạy trên http://0.0.0.0:8000")