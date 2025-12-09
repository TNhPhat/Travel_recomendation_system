# 🌍 Travel Recommendation API

API cung cấp gợi ý địa điểm dựa trên:

* Tag người dùng chọn
* Tag trích xuất từ prompt bằng Gemini
* Cosine similarity
* Sentiment score
* MMR (Maximal Marginal Relevance) để đa dạng kết quả

---

# 🚀 1. Chuẩn bị môi trường

## **Yêu cầu**
- Python 3.8+
- pip hoặc conda
- File `requirements.txt`
- Folder `model/` có chứa các file model
- API key từ Google Gemini

## **Bước 1: Cài đặt dependencies**

```bash
pip install -r requirements.txt
```

## **Bước 2: Tải folder model từ Google Drive**

Folder `model/` chứa các file cần thiết:
- `model.safetensors` - Model neural network
- `config.json` - Cấu hình model
- `scaler.pt` - Feature scaler
- `optimizer.pt` - Optimizer state
- `scheduler.pt` - Learning rate scheduler
- `trainer_state.json` - Trạng thái huấn luyện
- `rng_state.pth` - Random state

**Download link Google Drive:**
```
[Thay thế URL này bằng link Google Drive của bạn]
https://drive.google.com/drive/folders/FOLDER_ID
```

### Cách tải xuống:
1. Truy cập link Google Drive ở trên
2. Click phải vào folder `model` → chọn "Download" (hoặc Ctrl + Shift + D)
3. Chờ file tải xuống (thường là file .zip)
4. Giải nén file vào thư mục root của project
5. Kiểm tra cấu trúc folder:
```
Travel_recomendation_system/
├── model/
│   ├── model.safetensors
│   ├── config.json
│   ├── scaler.pt
│   ├── optimizer.pt
│   ├── scheduler.pt
│   ├── trainer_state.json
│   └── rng_state.pth
├── src/
├── data/
├── requirements.txt
└── readme.md
```

## **Bước 3: Cấu hình API Key**

Tạo file `.env` trong thư mục root project:

```env
GEMINI_API_KEY=your_api_key_here
```

Lấy API key từ [Google AI Studio](https://aistudio.google.com/apikey)

## **Bước 4: Chạy server FastAPI**

### **Tùy chọn A: Chạy với HTTP (phát triển)**

```bash
fastapi dev src/main.py
```

hoặc

```bash
uvicorn src.main:app --reload
```

Server sẽ chạy tại: `http://localhost:8000`

### **Tùy chọn B: Chạy với HTTPS (production)**

#### **Bước 4.1: Tự generate SSL Certificate**

Chạy lệnh sau để tạo certificate và key file:

```bash
# Tạo thư mục certs nếu chưa có
mkdir certs

# Generate private key
openssl genrsa -out certs/key.pem 2048

# Generate self-signed certificate (hiệu lực 365 ngày)
openssl req -new -x509 -key certs/key.pem -out certs/cert.pem -days 365 -subj "/C=VN/ST=HCM/L=HCM/O=Travel/CN=localhost"
```

**Kết quả sẽ có 2 file:**
- `certs/key.pem` - Private key
- `certs/cert.pem` - SSL Certificate

#### **Bước 4.2: Chạy server với HTTPS**

```bash
uvicorn src.main:app --reload --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem --host 0.0.0.0 --port 8443
```

Server sẽ chạy tại: `https://localhost:8443`

### **Truy cập dokumentasi API:**

- **Swagger UI (HTTP)**: http://localhost:8000/docs
- **ReDoc (HTTP)**: http://localhost:8000/redoc
- **Swagger UI (HTTPS)**: https://localhost:8443/docs
- **ReDoc (HTTPS)**: https://localhost:8443/redoc

> **Lưu ý:** Nếu dùng certificate self-signed, trình duyệt sẽ cảnh báo. Chọn "Tiếp tục truy cập" để tiếp tục.
---

# 📌 2. Gọi API

## **Endpoint**

```
POST /location_recomendation/recomendation/
```

## **Payload**

```json
{
  "users": [
    {
      "prompt": "tôi muốn đi biển",
      "chosen_tags": ["beach", "seafood"]
    },
    {
      "prompt": "thích chụp ảnh",
      "chosen_tags": ["view", "nature"]
    }
  ],
  "number_of_places": 10
}
```

## **Response**

```json
{
  "recommendations": ["id_23","id_10","id_4","id_8"]"
}
```

---

# 🧪 3. Gọi API từ nhiều ngôn ngữ

---

# 💙 3.1 Kotlin (Android)

Dùng Retrofit:

```kotlin
data class UserPreference(
    val prompt: String,
    val chosen_tags: List<String>
)

data class GroupRequest(
    val users: List<UserPreference>
)

interface ApiService {
    @POST("location_recomendation/recomendation/")
    suspend fun getRecommendation(
        @Body request: GroupRequest
    ): Response<Map<String, String>>
}

val retrofit = Retrofit.Builder()
    .baseUrl("http://10.0.2.2:8000/") // Emulator Android
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(ApiService::class.java)

suspend fun callApi() {
    val body = GroupRequest(
        users = listOf(
            UserPreference("muốn đi biển", listOf("beach"))
        )
    )
    val response = api.getRecommendation(body)
    println(response.body())
}
```

---

# ⚡ 3.2 Next.js (TypeScript)

Trong Next.js app router (`app/page.tsx`):

```ts
async function getRecommendation() {
  const res = await fetch("http://localhost:8000/location_recomendation/recomendation/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      users: [
        { prompt: "đi biển", chosen_tags: ["beach"] }
      ]
    })
  });

  const data = await res.json();
  console.log(data);
}
```

Hoặc trong API route (`app/api/test/route.ts`):

```ts
export async function POST() {
  const response = await fetch("http://localhost:8000/location_recomendation/recomendation/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      users: [{ prompt: "đi biển", chosen_tags: ["beach"] }]
    })
  });

  return Response.json(await response.json());
}
```

---

# 🎨 3.3 React TSX (Frontend)

```tsx
import { useState } from "react";

export default function Recommend() {
  const [result, setResult] = useState("");

  const callApi = async () => {
    const res = await fetch(
      "http://localhost:8000/location_recomendation/recomendation/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          users: [
            { prompt: "muốn đi biển", chosen_tags: ["beach", "food"] }
          ]
        })
      }
    );

    const data = await res.json();
    setResult(data.recommendations);
  };

  return (
    <div>
      <button onClick={callApi}>Get Recommendation</button>
      <p>Kết quả: {result}</p>
    </div>
  );
}
```

---

# 🟧 3.4 NestJS (Node.js)

### Tạo service call API

```ts
import { Injectable } from '@nestjs/common';
import fetch from 'node-fetch';

@Injectable()
export class RecommendationService {
  async getRecommendation() {
    const res = await fetch("http://localhost:8000/location_recomendation/recomendation/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        users: [
          { prompt: "đi biển", chosen_tags: ["beach"] }
        ]
      })
    });

    return await res.json();
  }
}
```

### Dùng trong controller:

```ts
@Get("recommend")
async recommend() {
  return this.service.getRecommendation();
}
```

---

# 📘 4. Kiểm tra API Docs

FastAPI tự sinh docs:

### Swagger UI

```
http://localhost:8000/docs
```

### ReDoc UI

```
http://localhost:8000/redoc
```

---

# 🧩 5. Ghi chú

* API chỉ trả về danh sách **id** địa điểm
* Nếu muốn trả full thông tin → sửa `return` trong router
* Kotlin android emulator dùng `10.0.2.2` thay cho `localhost`

---


