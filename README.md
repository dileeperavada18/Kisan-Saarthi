# 🌾 Kisan Call Centre Query Assistant

AI-powered agricultural support system with multilingual text and audio support.

## Features

✅ **Dual Processing Modes**
- Offline: Dataset-based recommendations
- Online: AI-enhanced advice using Claude SonneT

✅ **Multilingual Support**
- Text responses in 6 languages: English, Hindi, Telugu, Tamil, Kannada, Marathi
- Audio output (Text-to-Speech) in all supported languages

✅ **Image Analysis**
- Upload crop images for disease identification
- AI-powered visual analysis of plant health

✅ **Comprehensive Agricultural Support**
- Fertilizer recommendations
- Pesticide guidance
- Disease identification
- Government schemes information

## Tech Stack

**Backend:**
- Flask (Python web framework)
- Google Gemini API (AI recommendations with vision)
- ElevenLabs API (High-quality multilingual TTS)
- Flask-CORS (Cross-origin support)

**Frontend:**
- Pure HTML/CSS/JavaScript
- Glassmorphism design
- Responsive layout

## Setup Instructions

### 1. Clone/Download the Repository

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
GOOGLE_API_KEY=your-google-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
```

**Get your Google AI Studio API key:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

**Get your ElevenLabs API key:**
1. Go to https://elevenlabs.io/
2. Sign up for a free account (10,000 characters/month free)
3. Navigate to Profile → API Keys
4. Copy your API key

> **Note:** The free tier of ElevenLabs provides 10,000 characters per month, which is suitable for testing. For production, consider their paid plans.

### 4. Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 5. Open the Frontend

Simply open `index.html` in your web browser, or serve it using:

```bash
# Using Python's built-in server
python -m http.server 8000

# Then visit http://localhost:8000
```

## API Endpoints

### POST `/api/query`

Process agricultural queries and return recommendations.

**Request Body:**
```json
{
  "question": "Why are my tomato leaves turning yellow?",
  "crop": "tomato",
  "language": "english",
  "supportTypes": ["Disease Identification", "Fertilizer Recommendation"],
  "image": "base64_encoded_image_string",
  "mode": "Online"
}
```

**Response:**
```json
{
  "success": true,
  "offline_recommendation": "Dataset-based advice...",
  "online_recommendation": "AI-powered advice...",
  "timestamp": "2026-02-13T10:30:00"
}
```

### POST `/api/generate-audio`

Generate audio file from text response.

**Request Body:**
```json
{
  "text": "Your agricultural recommendation text",
  "language": "hindi"
}
```

**Response:**
Audio file (MP3 format)

### GET `/health`

Health check endpoint.

## Usage Guide

1. **Enter Your Question**: Describe your agricultural issue
2. **Select Crop**: Choose your crop from the dropdown
3. **Choose Language**: Select your preferred language
4. **Select Support Types**: Check relevant categories
5. **Upload Image** (Optional): Add a photo of affected crops
6. **Choose Mode**:
   - Offline: Quick dataset-based answers
   - Online: Detailed AI-powered analysis
7. **Submit**: Click "Get Solution"
8. **Listen**: Use audio playback buttons for voice responses

## Supported Crops

- Wheat
- Rice
- Maize
- Cotton
- Sugarcane
- Tomato
- Potato
- Onion
- Others

## Language Support

| Language | Text | Audio |
|----------|------|-------|
| English  | ✅   | ✅    |
| Hindi    | ✅   | ✅    |
| Telugu   | ✅   | ✅    |
| Tamil    | ✅   | ✅    |
| Kannada  | ✅   | ✅    |
| Marathi  | ✅   | ✅    |

## Troubleshooting

### "Connection refused" error
- Make sure the backend server is running on port 5000
- Check that CORS is enabled (already configured)

### "AI service unavailable"
- Verify your Google API key in `.env`
- Check API quota at https://console.cloud.google.com/
- Ensure internet connection is active
- Make sure you've enabled Gemini API in Google Cloud Console

### Audio not playing / "Audio generation failed"
- Verify your ElevenLabs API key in `.env`
- Check your character quota at https://elevenlabs.io/
- Free tier limit: 10,000 characters/month
- Ensure text is not empty

### Image upload issues
- Supported formats: JPG, PNG, WebP
- Maximum recommended size: 5MB
- Ensure image is clear and well-lit
- Make sure Pillow library is installed

## Extending the Dataset

Edit the `CROP_ISSUES_DB` dictionary in `app.py` to add more crops and issues:

```python
CROP_ISSUES_DB = {
    'your_crop': {
        'symptom_keyword': 'Recommendation and solution',
        # Add more symptoms...
    }
}
```

## Production Deployment

For production use:

1. **Set DEBUG to False** in `app.py`
2. **Use a production WSGI server** (Gunicorn, uWSGI)
3. **Enable HTTPS** for secure API communication
4. **Add rate limiting** to prevent abuse
5. **Set up monitoring** and logging
6. **Use environment variables** for all sensitive data

Example with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

MIT License

## Support

For issues or questions, please create an issue in the repository.

---

**Built with ❤️ for Indian farmers** 🇮🇳  
**Powered by Google Gemini AI & ElevenLabs**
