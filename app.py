#!/usr/bin/env python3
"""
Kling AI Video Generator - Flask Web API with Web Interface
Cloud-based service for iOS with web frontend
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import json
import base64
import time
import jwt
import requests
from pathlib import Path
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration from environment variables
KLING_ACCESS_KEY = os.getenv('KLING_ACCESS_KEY')
KLING_SECRET_KEY = os.getenv('KLING_SECRET_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Create temp directory for files
UPLOAD_FOLDER = tempfile.mkdtemp()
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class KlingVideoGenerator:
    def __init__(self):
        self.kling_access_key = KLING_ACCESS_KEY
        self.kling_secret_key = KLING_SECRET_KEY
        self.anthropic_api_key = ANTHROPIC_API_KEY
        self.kling_base_url = "https://api-singapore.klingai.com"
        self.anthropic_base_url = "https://api.anthropic.com/v1/messages"
        
        self.criteria = {
            "camera_movement": "Start a few feet back, then move toward the product at an angle",
            "scene_style": "Natural and realistic setting",
            "lighting": "Well-lit with soft natural lighting",
            "focus": "Keep product in focus throughout",
        }
    
    def generate_jwt_token(self):
        """Generate JWT token for Kling AI authentication"""
        headers = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "iss": self.kling_access_key,
            "exp": int(time.time()) + 1800,
            "nbf": int(time.time()) - 5
        }
        token = jwt.encode(payload, self.kling_secret_key, algorithm="HS256", headers=headers)
        return token
    
    def encode_image(self, image_path):
        """Convert image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def get_image_media_type(self, image_path):
        """Determine media type from file extension"""
        extension = Path(image_path).suffix.lower()
        media_types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'
        }
        return media_types.get(extension, 'image/jpeg')
    
    def analyze_product_image(self, image_path):
        """Use Claude to analyze product and generate prompt"""
        print("🔍 Analyzing product image...")
        
        base64_image = self.encode_image(image_path)
        media_type = self.get_image_media_type(image_path)
        
        system_prompt = f"""You are an expert at analyzing product images and creating optimal video generation prompts for TikTok shop product showcases.

Your task is to analyze the product image and generate a detailed prompt for Kling AI's image-to-video generation with the following criteria:

CAMERA MOVEMENT: {self.criteria['camera_movement']}
SCENE STYLE: {self.criteria['scene_style']}
LIGHTING: {self.criteria['lighting']}
FOCUS: {self.criteria['focus']}

Analyze the product and provide:
1. Product type and key features
2. Optimal product placement in frame
3. Ideal background/setting for this product
4. Complete Kling AI prompt optimized for the "elements" feature

Respond in JSON format:
{{
  "product_type": "description of product",
  "key_features": ["feature1", "feature2"],
  "placement": "where product should be positioned",
  "background": "description of ideal background",
  "kling_prompt": "complete prompt for Kling AI with camera movements and scene description"
}}"""

        headers = {
            "x-api-key": self.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1500,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_image}},
                    {"type": "text", "text": "Analyze this product image and generate an optimal Kling AI video prompt."}
                ]
            }],
            "system": system_prompt
        }
        
        response = requests.post(self.anthropic_base_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        content_text = result['content'][0]['text'].strip()
        
        # Clean markdown
        if content_text.startswith('```json'):
            content_text = content_text[7:]
        if content_text.startswith('```'):
            content_text = content_text[3:]
        if content_text.endswith('```'):
            content_text = content_text[:-3]
        content_text = content_text.strip()
        
        analysis = json.loads(content_text)
        print("✅ Analysis complete!")
        return analysis
    
    def create_video_task(self, base64_image, prompt, max_retries=3):
        """Create video generation task with retry logic"""
        print("🎥 Creating video task...")
        
        for attempt in range(max_retries):
            try:
                token = self.generate_jwt_token()
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model_name": "kling-v1",
                    "image": base64_image,
                    "prompt": prompt,
                    "duration": "5",
                    "mode": "std",
                    "aspect_ratio": "9:16"
                }
                
                response = requests.post(
                    f"{self.kling_base_url}/v1/videos/image2video",
                    headers=headers, json=payload, timeout=60
                )
                
                if response.status_code == 429 and attempt < max_retries - 1:
                    wait_time = 60 * (attempt + 1)
                    print(f"⏳ Rate limit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                result = response.json()
                
                task_id = result.get('data', {}).get('task_id') or result.get('task_id')
                if not task_id:
                    raise Exception("No task_id in response")
                
                print(f"✅ Task created: {task_id}")
                return task_id
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    wait_time = 60 * (attempt + 1)
                    print(f"⏳ Rate limit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise
    
    def wait_for_video(self, task_id, max_wait=600):
        """Poll for video completion"""
        print("⏳ Waiting for video...")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            token = self.generate_jwt_token()
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.get(
                f"{self.kling_base_url}/v1/videos/{task_id}",
                headers=headers, timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            status = result.get('data', {}).get('task_status') or result.get('status')
            
            if status in ['succeed', 'completed']:
                video_url = (
                    result.get('data', {}).get('task_result', {}).get('videos', [{}])[0].get('url') or
                    result.get('data', {}).get('videos', [{}])[0].get('url') or
                    result.get('video_url')
                )
                if not video_url:
                    raise Exception("No video URL in response")
                print("✅ Video ready!")
                return video_url
            elif status in ['failed', 'error']:
                raise Exception(f"Video generation failed: {result.get('message', 'Unknown error')}")
            
            print(f"⏳ Status: {status}... ({int(time.time() - start_time)}s)")
            time.sleep(10)
        
        raise TimeoutError("Video generation timed out")
    
    def download_video(self, video_url, output_path):
        """Download video"""
        print("💾 Downloading video...")
        response = requests.get(video_url, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Saved to {output_path}")

# Initialize generator
generator = KlingVideoGenerator()

@app.route('/')
def index():
    """Serve the web interface"""
    # Serve index.html if it exists in the same directory
    if os.path.exists('index.html'):
        return send_from_directory('.', 'index.html')
    else:
        return jsonify({
            "status": "online",
            "service": "Kling AI Video Generator",
            "version": "1.0",
            "message": "Upload index.html to use the web interface, or use the API directly at /generate"
        })

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files like test.html, debug.html, etc."""
    # Only serve .html, .css, .js files for security
    if filename.endswith(('.html', '.css', '.js')):
        if os.path.exists(filename):
            return send_from_directory('.', filename)
    return jsonify({"error": "File not found"}), 404

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Kling AI Video Generator",
        "version": "1.0"
    })

@app.route('/generate', methods=['POST'])
def generate_video():
    """Generate video from uploaded image"""
    try:
        # Check if image was uploaded
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Save uploaded image
        filename = secure_filename(file.filename)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        image_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(image_path)
        
        print(f"📸 Image received: {filename}")
        
        # Analyze product
        analysis = generator.analyze_product_image(image_path)
        
        # Generate video
        base64_image = generator.encode_image(image_path)
        task_id = generator.create_video_task(base64_image, analysis['kling_prompt'])
        video_url = generator.wait_for_video(task_id)
        
        # Download video
        video_filename = f"{timestamp}_video.mp4"
        video_path = os.path.join(UPLOAD_FOLDER, video_filename)
        generator.download_video(video_url, video_path)
        
        # Clean up image
        os.remove(image_path)
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "video_url": f"/download/{video_filename}",
            "message": "Video generated successfully!"
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_video_file(filename):
    """Download generated video"""
    try:
        video_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        if not os.path.exists(video_path):
            return jsonify({"error": "Video not found"}), 404
        
        return send_file(video_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Check if API keys are set
    if not all([KLING_ACCESS_KEY, KLING_SECRET_KEY, ANTHROPIC_API_KEY]):
        print("❌ ERROR: API keys not set!")
        print("Set these environment variables:")
        print("  KLING_ACCESS_KEY")
        print("  KLING_SECRET_KEY")
        print("  ANTHROPIC_API_KEY")
        exit(1)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
