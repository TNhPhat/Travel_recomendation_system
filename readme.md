# Travel Recommendation API

A production-ready intelligent travel recommendation system powered by machine learning, natural language processing, and real-time sentiment analysis. This API serves personalized location recommendations to an Android mobile application through secure RESTful endpoints.

## Overview

This system combines advanced ML techniques to deliver contextual travel recommendations:

- **AI-Powered Tag Extraction**: Leverages Google Gemini to extract user preferences from natural language prompts
- **Semantic Matching**: Utilizes cosine similarity on multi-dimensional tag embeddings for accurate preference alignment
- **Sentiment Analysis**: Real-time Vietnamese sentiment analysis using fine-tuned transformers (ViSoBERT)
- **Diversification**: Implements MMR (Maximal Marginal Relevance) to ensure recommendation variety
- **Group Intelligence**: Aggregates preferences across multiple users for optimized group travel planning
- **Smart Scheduling**: AI-driven itinerary generation using orienteering problem optimization

## Architecture

### Core Components

```
┌─────────────────────┐
│   Android Client    │ (HTTPS/SSL Required)
└──────────┬──────────┘
           │
           │ TLS 1.2+
           │
┌──────────▼───────────┐
│   FastAPI Server     │
├──────────────────────┤
│  • Routers           │
│  • Authentication    │
│  • Request Validation│
└──────────┬───────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼────┐   ┌────▼─────┐
│ ML/NLP │   │ Firestore│
│Services│   │ Database │
└────────┘   └──────────┘
```

### Technology Stack

- **Framework**: FastAPI (Python 3.14+)
- **ML Models**: 
  - Sentiment Analysis: ViSoBERT (Vietnamese-optimized BERT)
  - NLP: Google Gemini 2.5 Flash
- **Database**: Google Cloud Firestore (real-time sync)
- **Computation**: PyTorch, NumPy, Pandas
- **Infrastructure**: Uvicorn ASGI server

## Features

### 1. Personalized Recommendations
- Tag-based preference matching across 100+ travel attributes
- Natural language understanding of user intentions
- Weighted scoring combining relevance and sentiment

### 2. Group Travel Planning
- Multi-user preference aggregation using RMS (Root Mean Square) weighting
- Democratic voting system for destination selection
- Automated schedule generation respecting constraints (opening hours, travel time, user preferences)

### 3. Real-Time Sentiment Analysis
- Vietnamese language sentiment scoring (-1 to +1 scale)
- Live review monitoring with automatic location score updates
- Firestore integration for instant data synchronization

### 4. Intelligent Scheduling
- Constraint-based itinerary optimization
- Geographic clustering to minimize travel time
- Time-aware planning (opening hours, travel duration, buffer times)

## Security & Android Integration

### SSL/TLS Configuration

**This API is designed to communicate with an Android mobile application and requires strict SSL/TLS implementation for production deployment.**

#### Creating Self-Signed Certificates (Testing Only)

**⚠️ WARNING**: Self-signed certificates are for **development and testing purposes ONLY**. Never use them in production as they don't provide real security and will trigger warnings in browsers and Android apps.

For local testing, you can generate a self-signed SSL certificate:

**Using OpenSSL** (Linux/macOS/Windows with Git Bash):

```bash
# Generate private key and self-signed certificate (valid for 365 days)
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem \
  -out cert.pem \
  -days 365 \
  -subj "/C=VN/ST=HoChiMinh/L=HoChiMinh/O=TestOrg/CN=localhost"
```

**Running with Self-Signed Certificate**:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 \
  --ssl-keyfile=key.pem \
  --ssl-certfile=cert.pem
```


## Installation

### Prerequisites

- Python 3.12 or higher (tested with Python 3.14)
- Google Cloud account with Firestore enabled
- Google Gemini API key
- Pre-trained sentiment analysis model
- OpenSSL (for generating test SSL certificates)

**Note**: The `requirements.txt` file is auto-generated from `pyproject.toml`. If you need to modify dependencies, edit `pyproject.toml` and regenerate using:

```bash
uv pip compile pyproject.toml -o requirements.txt
```

### Step 1: Clone Repository

```bash
git clone https://github.com/TNhPhat/Travel_recomendation_system
cd Travel_recomendation_system
```

### Step 2: Install Dependencies

Using `uv` (recommended):
```bash
uv pip install -r requirements.txt
```

Or using pip:
```bash
pip install -r requirements.txt
```

### Step 3: Download Pre-trained Model

Download the sentiment analysis model files from Google Drive:

**Download Link**: [https://drive.google.com/drive/folders/1lPENYX3rcT5eNceKz_GBoWGT66LrzLlP?usp=sharing](https://drive.google.com/drive/folders/1lPENYX3rcT5eNceKz_GBoWGT66LrzLlP?usp=sharing)

Extract and place the `model/` folder in the project root:

```
Travel_recomendation_system/
├── model/
│   ├── model.safetensors      # Neural network weights
│   ├── config.json            # Model configuration
│   ├── scaler.pt              # Feature scaler
│   ├── optimizer.pt           # Optimizer state
│   ├── scheduler.pt           # Learning rate scheduler
│   ├── trainer_state.json     # Training state
│   └── rng_state.pth          # Random state
├── src/
├── data/
└── ...
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

To obtain a Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

### Step 5: Setup Firebase Credentials(provided in the submission files)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Navigate to Project Settings → Service Accounts
4. Click "Generate New Private Key"
5. Download the JSON file
6. Rename it to `serviceAccountKey.json`
7. Place it in the project root directory

## Running the API

### Development Mode (HTTP - Testing Only)

```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Access the interactive API documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Testing Mode (HTTPS with Self-Signed Certificate)

For testing Android app integration locally with SSL:

```bash
# First, generate self-signed certificates (see SSL Configuration section above)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 \
  --ssl-keyfile=key.pem \
  --ssl-certfile=cert.pem
```

Access the API:
- Swagger UI: `https://localhost:8443/docs` (you'll see a security warning - this is expected)
- From Android emulator: `https://10.0.2.2:8443/`
- From physical Android device: `https://YOUR_LOCAL_IP:8443/`

**Find your local IP**:
- Windows: `ipconfig` (look for IPv4 Address)
- Linux/macOS: `ifconfig` or `ip addr`

## API Endpoints

### Sentiment Analysis

#### POST `/analyze`
Analyzes sentiment of Vietnamese text reviews.

**Request**:
```json
{
  "text": "Địa điểm này rất đẹp và yên tĩnh, phù hợp để thư giãn"
}
```

**Response**:
```json
{
  "sentiment_score": 0.87
}
```

### Tag Extraction

#### POST `/tag_extraction`
Extracts weighted travel preference tags from natural language.

**Request**:
```json
{
  "prompt": "Tôi muốn đi du lịch biển, thích hoạt động mạo hiểm và ẩm thực địa phương",
  "chosen_tags": ["bãi biển", "ẩm thực đường phố"]
}
```

**Response**:
```json
{
  "tag": {
    "bãi biển": 1.0,
    "ẩm thực đường phố": 1.0,
    "thích phiêu lưu / mạo hiểm": 0.95,
    "ẩm thực đặc sản": 0.90
  }
}
```

### Recommendations

#### POST `/personal_recomendation_by_tag_dict`
Get personalized location recommendations based on tag preferences.

**Request**:
```json
{
  "tag_dict": {
    "bãi biển": 1.0,
    "yên tĩnh": 0.8,
    "ẩm thực đặc sản": 0.9
  },
  "number_of_places": 5,
  "destination": "Đà Nẵng"
}
```

**Response**:
```json
{
  "recommendations": ["loc_001", "loc_045", "loc_023", "loc_067", "loc_012"],
  "match_score": [0.92, 0.88, 0.85, 0.83, 0.81]
}
```

#### POST `/group_recomendation_by_user_data`
Aggregate multiple users' preferences for group travel.

**Request**:
```json
{
  "users": [
    {
      "prompt": "Tôi thích núi non và thiên nhiên",
      "chosen_tags": ["núi non", "công viên quốc gia"]
    },
    {
      "prompt": "Muốn đi biển và ăn hải sản",
      "chosen_tags": ["bãi biển", "nhà hàng"]
    }
  ],
  "number_of_places": 10
}
```

**Response**:
```json
{
  "recommendations": ["loc_088", "loc_034", ...]
}
```

#### POST `/get_schedule`
Generate optimized travel itinerary from voted locations.

**Request**:
```json
{
  "VoteList": {
    "loc_001": 5,
    "loc_034": 3,
    "loc_088": 4
  },
  "start_time": "2026-01-15T08:00:00.000000Z",
  "end_time": "2026-01-15T20:00:00.000000Z"
}
```

**Response**:
```json
{
  "schedule": [
    {
      "id": "loc_001",
      "start_time": "2026-01-15T08:00:00.000000Z",
      "end_time": "2026-01-15T10:30:00.000000Z"
    },
    {
      "id": "loc_088",
      "start_time": "2026-01-15T11:15:00.000000Z",
      "end_time": "2026-01-15T13:00:00.000000Z"
    }
  ]
}
```

## Algorithm Details

### Recommendation Scoring

The final recommendation score combines semantic similarity and sentiment analysis:

```
recommendation_score = 0.7 × cosine_similarity + 0.3 × sentiment_score
```

**Components**:
- **Cosine Similarity**: Measures alignment between user preferences and location tags (tag embeddings in 100+ dimensional space)
- **Sentiment Score**: Aggregated from real-time user reviews (-1 to +1 scale)

### MMR (Maximal Marginal Relevance)

Ensures diversity in recommendations to avoid redundant suggestions:

```
MMR = λ × Sim(location, query) - (1 - λ) × max(Sim(location, selected_locations))
```

- **λ (lambda)**: Balances relevance vs. diversity (typically 0.7-0.9)
- Higher λ → More relevant but potentially similar results
- Lower λ → More diverse but potentially less relevant results

### Group Preference Aggregation

Uses RMS (Root Mean Square) to combine multiple users' tag vectors:

```
RMS_weight = sqrt((vector₁² + vector₂² + ... + vectorₙ²) / n)
```

This approach gives more influence to strong preferences while maintaining democratic fairness.

## Project Structure

```
Travel_recomendation_system/
├── src/
│   ├── main.py                      # FastAPI application entry point
│   ├── routers/
│   │   ├── sentiment_router.py      # Sentiment analysis endpoints
│   │   ├── recomendation_router.py  # Recommendation endpoints
│   │   └── tag_extraction_router.py # Tag extraction endpoints
│   ├── service/
│   │   ├── sentiment_service.py     # ViSoBERT sentiment analysis
│   │   ├── embedding_service.py     # Tag embedding operations
│   │   ├── recomendation_service.py # Core recommendation logic
│   │   ├── geminiAPI_service.py     # Google Gemini integration
│   │   └── firestore_service.py     # Database operations
│   └── utils/
│       └── contants.py              # Configuration and tag definitions
├── model/                           # Pre-trained sentiment model
├── data/                            # Dataset files (optional)
├── serviceAccountKey.json           # Firebase credentials (not in repo)
├── .env                             # Environment variables (not in repo)
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata
└── README.md
```

## Database Schema

### Firestore Collections

#### `locations`
Stores travel destination information.

```typescript
{
  id: string,              // Unique location identifier
  name: string,            // Location name
  address: string,         // Full address
  coordinates: string,     // GPS coordinates (lat,lng)
  city: string,            // City name
  province: string,        // Province/state
  category: string,        // Location category
  description: string,     // Detailed description
  opening_hour: string,    // Operating hours
  label: string,           // Serialized tag weights
  sentiment_sum: number,   // Cumulative sentiment score
  num_reviews: number,     // Total review count
  sentiment_score: number  // Average sentiment (sum/count)
}
```

#### `reviews`
Stores user reviews with sentiment analysis.

```typescript
{
  id: string,              // Review identifier
  locationId: string,      // Reference to location
  sentimentScore: number,  // Analyzed sentiment (-1 to 1)
  text: string,            // Review content
  timestamp: timestamp     // Review creation time
}
```

### Real-Time Synchronization

The API maintains a live listener on the `reviews` collection. When new reviews are added or modified, sentiment scores are automatically recalculated and propagated to the `locations` collection, ensuring recommendation freshness.

## Tag System

The system uses **100+ hierarchical tags** across multiple domains:

- **Activity**: Cultural/Historic, Nature/Outdoor, Entertainment, Gastronomy
- **Budget**: Price levels from budget to luxury
- **Social Context**: Group types, crowd preferences
- **Amenities**: Facilities, accessibility features
- **Tourism Type**: Eco-tourism, wellness, adventure, etc.
- **Time**: Seasonal preferences, time of day
- **Experience**: User preference profiles

See [`src/utils/contants.py`](src/utils/contants.py) for the complete tag taxonomy.

## Performance Considerations

- **Model Loading**: Sentiment model loads once at startup (~2-3 seconds)
- **Tag Embedding**: O(n) where n = number of tags (< 1ms for 100 tags)
- **Cosine Similarity**: O(m × d) where m = locations, d = dimensions (< 10ms for 1000 locations)
- **MMR Selection**: O(k × m) where k = top_k results (< 50ms for k=10, m=1000)
- **Firestore Queries**: Typically < 100ms with proper indexing

**Optimization Tips**:
- Use caching for frequently accessed locations
- Implement request rate limiting
- Consider batch processing for group recommendations
- Pre-compute embeddings for static tag combinations

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'torch'`
**Solution**: Ensure PyTorch is installed with the correct CUDA version if using GPU.

**Issue**: `google.auth.exceptions.DefaultCredentialsError`
**Solution**: Verify `serviceAccountKey.json` exists and has correct permissions.

**Issue**: `API key not valid` (Gemini)
**Solution**: Check `.env` file contains valid `GEMINI_API_KEY`.

**Issue**: SSL handshake failures from Android
**Solution**: 
- For Android Emulator, the host machine IP is: 10.0.2.2
- Verify certificate chain is complete
- Check Android app's Network Security Configuration
- Ensure TLS 1.2+ is enabled on server

### Logs and Debugging

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Monitor Firestore operations:
```python
firestore_service.db.set_debug(True)
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use type hints where applicable
- Add docstrings to all public functions
- Write unit tests for new features

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Acknowledgments

- **ViSoBERT**: Vietnamese sentiment analysis model by 5CD-AI
- **Google Gemini**: Natural language understanding capabilities
- **FastAPI**: Modern Python web framework
- **Transformers**: Hugging Face transformer implementations

## Contact & Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact the development team
