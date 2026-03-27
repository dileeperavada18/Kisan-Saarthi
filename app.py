from flask import render_template
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
import base64
import io
import os
import requests
from datetime import datetime
from PIL import Image

app = Flask(__name__)
CORS(app)


# API Keys - Set these as environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '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')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', 'sk_11f111575d8a09b12b5eee68327fb2954a9020059aacbdf0')

# Configure Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ElevenLabs voice IDs for multilingual support
# Using multilingual v2 model
ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam - multilingual voice

# Language codes for Gemini prompts
LANGUAGE_NAMES = {
    'english': 'English',
    'hindi': 'Hindi (हिंदी)',
    'telugu': 'Telugu (తెలుగు)',
    'tamil': 'Tamil (தமிழ்)',
    'kannada': 'Kannada (ಕನ್ನಡ)',
    'marathi': 'Marathi (मराठी)'
}

# Agricultural dataset for offline recommendations
CROP_ISSUES_DB = {
    'wheat': {
        'yellow_leaves': 'Nitrogen deficiency. Apply 50kg Urea per acre.',
        'brown_spots': 'Leaf rust detected. Spray Propiconazole fungicide.',
        'wilting': 'Check irrigation. May indicate root rot or water stress.'
    },
    'rice': {
        'yellow_leaves': 'Nitrogen deficiency or Bacterial Leaf Blight. Apply Urea.',
        'brown_spots': 'Brown spot disease. Use Mancozeb fungicide.',
        'stunted_growth': 'Check for stem borer infestation.'
    },
    'tomato': {
        'yellow_leaves': 'Fusarium wilt or nutrient deficiency. Check soil pH.',
        'black_spots': 'Early blight. Apply Chlorothalonil fungicide.',
        'curled_leaves': 'Possible virus infection or aphid infestation.'
    },
    'cotton': {
        'yellow_leaves': 'Verticillium wilt. Crop rotation recommended.',
        'pink_bollworm': 'Apply Emamectin Benzoate insecticide.',
        'wilting': 'Check for root diseases and soil drainage.'
    }
}

def get_offline_recommendation(crop, question):
    """Get recommendation from static dataset"""
    crop = crop.lower()
    question_lower = question.lower()
    
    if crop in CROP_ISSUES_DB:
        for key, solution in CROP_ISSUES_DB[crop].items():
            if any(word in question_lower for word in key.split('_')):
                return f"📊 Dataset Recommendation: {solution}"
    
    return f"Based on our database, for {crop} cultivation, ensure proper irrigation, balanced fertilization (NPK 120:60:40), and regular pest monitoring."

def get_ai_recommendation(question, crop, support_types, image_base64, language):
    """Get AI-powered recommendation using Google Gemini"""
    try:
        # Initialize Gemini model with vision capability
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Build the prompt in the requested language
        lang_name = LANGUAGE_NAMES.get(language, 'English')
        
        prompt = f"""You are an expert agricultural advisor helping Indian farmers. 

Farmer's Question: {question}
Crop: {crop}
Support Areas: {', '.join(support_types) if support_types else 'General advice'}

IMPORTANT: Respond ONLY in {lang_name} language. 

Provide practical, actionable advice including:
1. Problem diagnosis
2. Immediate actions to take
3. Recommended treatments (fertilizers/pesticides with specific names and dosages)
4. Preventive measures for future
5. Relevant government schemes (PM-KISAN, Soil Health Card, etc.) if applicable

Keep the response farmer-friendly, clear, and under 300 words."""

        # Prepare content
        if image_base64:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            prompt += "\n\nPlease analyze the uploaded crop image carefully and provide specific recommendations based on what you observe (leaf color, spots, wilting, etc.)."
            
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        return f"AI service error: {str(e)}. Please check your Google API key and try again."

def generate_audio(text, language):
    """Generate high-quality audio using ElevenLabs API"""
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        # ElevenLabs multilingual v2 model supports all Indian languages
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            audio_buffer = io.BytesIO(response.content)
            audio_buffer.seek(0)
            return audio_buffer
        else:
            print(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Audio generation error: {str(e)}")
        return None

@app.route('/api/query', methods=['POST'])
def process_query():
    """Main endpoint to process agricultural queries"""
    try:
        data = request.json
        
        question = data.get('question', '')
        crop = data.get('crop', 'general')
        language = data.get('language', 'english')
        support_types = data.get('supportTypes', [])
        image_base64 = data.get('image', '')
        mode = data.get('mode', 'Offline')
        
        # Get offline recommendation
        offline_result = get_offline_recommendation(crop, question)
        
        # Get AI recommendation if mode is Online
        online_result = ""
        if mode == "Online":
            online_result = get_ai_recommendation(
                question, crop, support_types, image_base64, language
            )
        else:
            online_result = "AI mode disabled. Switch to 'Online' mode for AI-enhanced recommendations."
        
        response = {
            'success': True,
            'offline_recommendation': offline_result,
            'online_recommendation': online_result,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio_endpoint():
    """Generate audio for text response"""
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'english')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        audio_buffer = generate_audio(text, language)
        
        if audio_buffer:
            return send_file(
                audio_buffer,
                mimetype='audio/mpeg',
                as_attachment=True,
                download_name=f'response_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp3'
            )
        else:
            return jsonify({'success': False, 'error': 'Audio generation failed'}), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
