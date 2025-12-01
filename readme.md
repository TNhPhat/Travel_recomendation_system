# 🌍 Travel Recommendation API

API cung cấp gợi ý địa điểm dựa trên:

* Tag người dùng chọn
* Tag trích xuất từ prompt bằng Gemini
* Cosine similarity
* Sentiment score
* MMR (Maximal Marginal Relevance) để đa dạng kết quả

---

# 🚀 1. Cách chạy FastAPI

## **Yêu cầu**
requirements.txt

## **Cài đặt**

```bash
pip install -r requirements.txt
```

## **Chạy server**

```bash
uvicorn src.main:app --reload
```

### Mặc định server sẽ chạy tại:

```
http://localhost:8000
```
## **API_KEY**
Thêm file .env vào folder root sau đó thêm gemini_api_key để sử dụng:
```bash
GEMINI_API_KEY=xxxxxxx
```
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
  ]
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


