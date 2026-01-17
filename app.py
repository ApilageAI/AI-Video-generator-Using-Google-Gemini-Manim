from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
import os
import json
import traceback
import threading
import queue
import uuid
import time
from datetime import datetime
from functools import wraps
from utils import render_video_audio_first

app = Flask(__name__)

# ============== CORS CONFIGURATION ==============
# Allow cross-origin requests from any domain for API endpoints
CORS_ORIGINS = '*'  # Change to specific domain in production if needed

def add_cors_headers(response):
    """Add CORS headers to response."""
    response.headers['Access-Control-Allow-Origin'] = CORS_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response

@app.after_request
def after_request(response):
    """Add CORS headers to all responses."""
    return add_cors_headers(response)

@app.before_request
def handle_preflight():
    """Handle CORS preflight OPTIONS requests."""
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)

VIDEOS_FILE = 'videos.json'
VIDEOS_DIR = 'media/videos/generated/480p15'
UPLOADS_DIR = 'uploads'
JOBS_FILE = 'jobs.json'


def pick_most_recent_upload_mp4(prefer_final: bool = True):
    """Pick the most recent MP4 in uploads/, preferring *_final.mp4 when present."""
    if not os.path.exists(UPLOADS_DIR):
        return None

    mp4_files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith('.mp4')]
    if not mp4_files:
        return None

    def ctime(name: str) -> float:
        return os.path.getctime(os.path.join(UPLOADS_DIR, name))

    if prefer_final:
        final_files = [f for f in mp4_files if f.endswith('_final.mp4')]
        if final_files:
            final_files.sort(key=ctime, reverse=True)
            return final_files[0]

    mp4_files.sort(key=ctime, reverse=True)
    return mp4_files[0]

# ============== JOB QUEUE SYSTEM ==============
# Thread-safe queue for video generation jobs
job_queue = queue.Queue()

# Dictionary to store job status (thread-safe with lock)
jobs_lock = threading.Lock()
jobs = {}

# Worker thread running flag
worker_running = False
worker_thread = None


def load_jobs():
    """Load jobs from file on startup."""
    global jobs
    if os.path.exists(JOBS_FILE):
        try:
            with open(JOBS_FILE, 'r') as f:
                jobs = json.load(f)
        except Exception as e:
            # If the file is corrupted, quarantine it and start fresh.
            try:
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                os.replace(JOBS_FILE, f"{JOBS_FILE}.corrupt_{ts}.bak")
            except Exception:
                pass
            print(f"[WARN] Failed to load jobs.json (resetting): {e}")
            jobs = {}
            save_jobs()
    return jobs


def save_jobs():
    """Save jobs to file."""
    with jobs_lock:
        try:
            with open(JOBS_FILE, 'w') as f:
                json.dump(jobs, f, indent=2)
        except Exception as e:
            print(f"Error saving jobs: {e}")


def get_job(job_id):
    """Get job by ID."""
    with jobs_lock:
        return jobs.get(job_id)


def update_job(job_id, **kwargs):
    """Update job status."""
    with jobs_lock:
        if job_id in jobs:
            jobs[job_id].update(kwargs)
            jobs[job_id]['updated_at'] = datetime.now().isoformat()
    save_jobs()


def create_job(topic):
    """Create a new job and add to queue."""
    job_id = str(uuid.uuid4())
    
    with jobs_lock:
        # Count pending jobs for queue position
        pending_count = sum(1 for j in jobs.values() if j.get('status') == 'pending')
        
        jobs[job_id] = {
            'id': job_id,
            'topic': topic,
            'status': 'pending',  # pending, processing, completed, failed
            'queue_position': pending_count + 1,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'video_url': None,
            'error': None,
            'progress': 'Waiting in queue...'
        }
    
    save_jobs()
    
    # Add to processing queue
    job_queue.put(job_id)
    
    return job_id


def process_job(job_id):
    """Process a single video generation job using AUDIO-FIRST workflow."""
    job = get_job(job_id)
    if not job:
        return
    
    topic = job['topic']
    try:
        update_job(job_id, status='processing', progress='Generating narration audio first...')
        print(f"[JOB {job_id[:8]}] Processing with AUDIO-FIRST workflow: {topic}")
        
        # ===== AUDIO-FIRST (SEGMENTED) WORKFLOW =====
        # 1) Generate narration script (no templates)
        # 2) Split into segments
        # 3) Generate TTS audio per segment to get exact timings
        # 4) Generate + render Manim per segment, matching segment duration
        # 5) Mux each segment and concatenate into final MP4

        update_job(job_id, progress='Generating full video (segmented audio+video sync)...')

        # Run the full production pipeline
        video_path, voice_script, subtitles = render_video_audio_first(topic)
        
        if not video_path or not os.path.exists(video_path):
            update_job(job_id, status='failed', error='Video rendering failed')
            return
        
        # Find the uploaded video from uploads folder
        upload_filename = pick_most_recent_upload_mp4(prefer_final=True)
        
        # Use upload URL if available
        if upload_filename:
            video_url = f"/uploads/{upload_filename}"
            video_filename = upload_filename
        else:
            video_filename = os.path.basename(video_path)
            video_url = f"/videos/{video_filename}"
        
        video_title = topic[:47] + ('...' if len(topic) > 47 else '')
        
        # Update job as completed
        update_job(
            job_id, 
            status='completed', 
            video_url=video_url,
            video_filename=video_filename,
            subtitles=subtitles,
            progress='Completed!'
        )
        
        print(f"[JOB {job_id[:8]}] Completed: {video_url}")
        
    except Exception as e:
        error_msg = str(e)[:500]
        print(f"[JOB {job_id[:8]}] Failed: {error_msg}")
        update_job(job_id, status='failed', error=error_msg, progress='Failed')


def worker():
    """Background worker that processes jobs from the queue."""
    global worker_running
    print("[WORKER] Video generation worker started")
    
    while worker_running:
        try:
            # Wait for a job with timeout (so we can check worker_running)
            try:
                job_id = job_queue.get(timeout=1)
            except queue.Empty:
                continue
            
            # Update queue positions for remaining jobs
            with jobs_lock:
                pending_jobs = [(jid, j) for jid, j in jobs.items() if j.get('status') == 'pending']
                for idx, (jid, _) in enumerate(pending_jobs):
                    jobs[jid]['queue_position'] = idx + 1
            
            # Process the job
            process_job(job_id)
            
            job_queue.task_done()
            
        except Exception as e:
            print(f"[WORKER] Error: {e}")
            traceback.print_exc()
    
    print("[WORKER] Video generation worker stopped")


def start_worker():
    """Start the background worker thread."""
    global worker_running, worker_thread
    
    if worker_thread is None or not worker_thread.is_alive():
        worker_running = True
        worker_thread = threading.Thread(target=worker, daemon=True)
        worker_thread.start()
        print("[WORKER] Background worker started")


def stop_worker():
    """Stop the background worker thread."""
    global worker_running
    worker_running = False
    if worker_thread:
        worker_thread.join(timeout=5)

def load_videos():
    """Load videos directly from uploads folder."""
    videos = []
    
    if os.path.exists(UPLOADS_DIR):
        mp4_files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith('.mp4')]
        final_files = {f for f in mp4_files if f.endswith('_final.mp4')}

        # Sort newest first (ctime)
        mp4_files.sort(key=lambda x: os.path.getctime(os.path.join(UPLOADS_DIR, x)), reverse=True)

        for filename in mp4_files:
            # Hide segment/intermediate outputs when a final render exists.
            if '_seg' in filename:
                continue
            if filename.endswith('_av.mp4'):
                base = filename[:-len('_av.mp4')]
                if f"{base}_final.mp4" in final_files:
                    continue

            filepath = os.path.join(UPLOADS_DIR, filename)
            stat = os.stat(filepath)
                
                # Extract title from filename (remove timestamp and extension)
                # Format: MathExplanationScene_20251209_095730.mp4
            title = filename.replace('.mp4', '')
            if title.endswith('_final'):
                title = title[:-len('_final')]
            elif title.endswith('_av'):
                title = title[:-len('_av')]
                if '_' in title:
                    parts = title.rsplit('_', 2)  # Split from right to get base name
                    if len(parts) >= 3:
                        title = parts[0]  # Get the scene name part
                
            videos.append({
                'title': title[:50] + ('...' if len(title) > 50 else ''),
                'url': f'/uploads/{filename}',
                'filename': filename,
                'subtitles': '',
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'size': stat.st_size
            })
    
    return videos

def save_videos(videos):
    """Save videos to JSON file."""
    try:
        with open(VIDEOS_FILE, 'w') as f:
            json.dump(videos, f, indent=2)
    except Exception as e:
        print(f"Error saving videos: {e}")

def sync_videos_with_filesystem():
    """
    Get all videos from uploads folder.
    No JSON sync needed - reads directly from filesystem.
    """
    return load_videos()

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api-docs')
def api_docs():
    """Serve API documentation page."""
    return render_template('api-docs.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate a new video from text input."""
    data = request.get_json()
    text_input = data.get('text', '').strip()

    print(f"\n{'='*50}")
    print(f"[GENERATE REQUEST]")
    print(f"Topic: '{text_input}'")
    print(f"{'='*50}\n")

    if not text_input:
        return jsonify({'error': 'No text provided. Please enter a topic.'}), 400

    if len(text_input) < 3:
        return jsonify({'error': 'Please provide a more detailed description.'}), 400

    if len(text_input) > 500:
        return jsonify({'error': 'Description is too long. Please keep it under 500 characters.'}), 400

    try:
        # Audio-first generation to match narration timing
        print(f"Generating audio-first video for: {text_input}")
        video_path, voice_script, subtitles = render_video_audio_first(text_input)

        if not video_path or not os.path.exists(video_path):
            return jsonify({'error': 'Video was generated but file not found.'}), 500

        # Prefer *_final.mp4 so users see the real final render.
        upload_filename = pick_most_recent_upload_mp4(prefer_final=True)
        
        # Use upload URL if available, otherwise use original video path
        if upload_filename:
            video_url = f"/uploads/{upload_filename}"
            video_filename = upload_filename
        else:
            video_filename = os.path.basename(video_path)
            video_url = f"/videos/{video_filename}"
        
        # Create a clean title
        video_title = text_input[:47] + ('...' if len(text_input) > 47 else '')

        print(f"Video generated successfully: {video_filename}")

        # Return the video URL and subtitles
        resp = jsonify({
            'video_url': video_url,
            'subtitles': subtitles,
            'title': video_title
        })
        resp.headers['Cache-Control'] = 'no-store'
        return resp

    except Exception as e:
        error_message = str(e)
        print(f"Error generating video: {error_message}")
        print(traceback.format_exc())
        
        # Provide user-friendly error messages
        if "syntax" in error_message.lower():
            return jsonify({'error': 'There was a problem with the generated animation code. Please try again or use a different description.'}), 500
        elif "timeout" in error_message.lower():
            return jsonify({'error': 'Video rendering took too long. Please try a simpler topic.'}), 500
        elif "manim" in error_message.lower():
            return jsonify({'error': 'Animation rendering failed. Please try again with a different topic.'}), 500
        else:
            return jsonify({'error': f'An error occurred: {error_message[:200]}'}), 500

@app.route('/videos')
def get_videos():
    """Get list of all videos."""
    try:
        # Sync with filesystem to catch any orphaned files
        videos = sync_videos_with_filesystem()
        resp = jsonify(videos)
        resp.headers['Cache-Control'] = 'no-store'
        return resp
    except Exception as e:
        print(f"Error loading videos: {e}")
        return jsonify([])

@app.route('/videos/<filename>')
def get_video(filename):
    """Serve a video file."""
    # Security: prevent directory traversal
    if '..' in filename or '/' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    video_path = os.path.join(VIDEOS_DIR, filename)
    
    if os.path.exists(video_path):
        return send_from_directory(
            os.path.abspath(VIDEOS_DIR), 
            filename,
            mimetype='video/mp4'
        )
    else:
        return jsonify({'error': 'Video not found'}), 404


@app.route('/uploads/<filename>')
def get_upload(filename):
    """Serve a video file from uploads folder."""
    # Security: prevent directory traversal
    if '..' in filename or '/' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    upload_path = os.path.join(UPLOADS_DIR, filename)
    
    if os.path.exists(upload_path):
        return send_from_directory(
            os.path.abspath(UPLOADS_DIR), 
            filename,
            mimetype='video/mp4'
        )
    else:
        return jsonify({'error': 'Upload not found'}), 404


@app.route('/api/uploads', methods=['GET'])
def api_uploads():
    """
    Get list of all uploaded videos in the uploads/ folder.
    
    Query params:
    - limit: max number of videos (default 50)
    - offset: pagination offset (default 0)
    """
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    uploads = []
    if os.path.exists(UPLOADS_DIR):
        for filename in sorted(os.listdir(UPLOADS_DIR), reverse=True):
            if filename.endswith('.mp4'):
                filepath = os.path.join(UPLOADS_DIR, filename)
                stat = os.stat(filepath)
                uploads.append({
                    'filename': filename,
                    'url': f'/uploads/{filename}',
                    'full_url': request.host_url.rstrip('/') + f'/uploads/{filename}',
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
    
    # Apply pagination
    paginated = uploads[offset:offset + limit]
    
    return jsonify({
        'success': True,
        'total': len(uploads),
        'limit': limit,
        'offset': offset,
        'uploads': paginated
    })

@app.route('/health')
def health_check():
    """Health check endpoint."""
    with jobs_lock:
        pending = sum(1 for j in jobs.values() if j.get('status') == 'pending')
        processing = sum(1 for j in jobs.values() if j.get('status') == 'processing')
    
    return jsonify({
        'status': 'ok',
        'videos_count': len(load_videos()),
        'queue_pending': pending,
        'queue_processing': processing,
        'worker_running': worker_running
    })


# ============== API ENDPOINTS ==============

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """
    API endpoint to submit a video generation request.
    Returns a job ID that can be used to check status.
    
    Request body:
    {
        "topic": "Explain the Pythagorean theorem"
    }
    
    Response:
    {
        "success": true,
        "job_id": "uuid-string",
        "message": "Video generation queued",
        "queue_position": 1
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        topic = data.get('topic', '').strip()
        
        # Validation
        if not topic:
            return jsonify({
                'success': False,
                'error': 'Topic is required'
            }), 400
        
        if len(topic) < 3:
            return jsonify({
                'success': False,
                'error': 'Topic must be at least 3 characters'
            }), 400
        
        if len(topic) > 500:
            return jsonify({
                'success': False,
                'error': 'Topic must be less than 500 characters'
            }), 400
        
        # Create job and add to queue
        job_id = create_job(topic)
        job = get_job(job_id)
        
        print(f"[API] New job created: {job_id[:8]} - {topic[:50]}")
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Video generation queued',
            'queue_position': job['queue_position'],
            'status_url': f'/api/status/{job_id}',
            'video_url': f'/api/video/{job_id}'
        })
        
    except Exception as e:
        print(f"[API] Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/status/<job_id>', methods=['GET'])
def api_status(job_id):
    """
    Check the status of a video generation job.
    
    Response:
    {
        "success": true,
        "job": {
            "id": "uuid-string",
            "status": "processing",  // pending, processing, completed, failed
            "queue_position": 1,     // only if pending
            "progress": "Rendering video...",
            "video_url": "/videos/xxx.mp4",  // only if completed
            "error": "...",          // only if failed
            "created_at": "2025-12-07T...",
            "updated_at": "2025-12-07T..."
        }
    }
    """
    job = get_job(job_id)
    
    if not job:
        return jsonify({
            'success': False,
            'error': 'Job not found'
        }), 404
    
    # Build response based on status
    response = {
        'success': True,
        'job': {
            'id': job['id'],
            'topic': job['topic'],
            'status': job['status'],
            'progress': job.get('progress', ''),
            'created_at': job['created_at'],
            'updated_at': job.get('updated_at', job['created_at'])
        }
    }
    
    if job['status'] == 'pending':
        response['job']['queue_position'] = job.get('queue_position', 0)
    
    if job['status'] == 'completed':
        response['job']['video_url'] = job.get('video_url')
        response['job']['video_filename'] = job.get('video_filename')
        response['job']['subtitles'] = job.get('subtitles', '')
    
    if job['status'] == 'failed':
        response['job']['error'] = job.get('error', 'Unknown error')
    
    return jsonify(response)


@app.route('/api/video/<job_id>', methods=['GET'])
def api_video(job_id):
    """
    Get video details for a completed job.
    If video is ready, returns video URL.
    If not ready, returns current status.
    """
    job = get_job(job_id)
    
    if not job:
        return jsonify({
            'success': False,
            'error': 'Job not found'
        }), 404
    
    if job['status'] == 'completed':
        return jsonify({
            'success': True,
            'ready': True,
            'video_url': job.get('video_url'),
            'video_filename': job.get('video_filename'),
            'full_url': request.host_url.rstrip('/') + job.get('video_url', ''),
            'subtitles': job.get('subtitles', ''),
            'topic': job['topic']
        })
    
    elif job['status'] == 'failed':
        return jsonify({
            'success': False,
            'ready': False,
            'error': job.get('error', 'Video generation failed')
        }), 500
    
    else:
        return jsonify({
            'success': True,
            'ready': False,
            'status': job['status'],
            'progress': job.get('progress', ''),
            'queue_position': job.get('queue_position', 0) if job['status'] == 'pending' else None
        })


@app.route('/api/queue', methods=['GET'])
def api_queue():
    """
    Get current queue status.
    
    Response:
    {
        "success": true,
        "queue": {
            "pending": 5,
            "processing": 1,
            "completed_today": 10
        },
        "jobs": [...]  // list of pending/processing jobs
    }
    """
    with jobs_lock:
        pending_jobs = [j for j in jobs.values() if j.get('status') == 'pending']
        processing_jobs = [j for j in jobs.values() if j.get('status') == 'processing']
        
        # Sort pending jobs by queue position
        pending_jobs.sort(key=lambda x: x.get('queue_position', 999))
    
    return jsonify({
        'success': True,
        'queue': {
            'pending': len(pending_jobs),
            'processing': len(processing_jobs),
            'total_jobs': len(jobs)
        },
        'pending_jobs': [
            {
                'id': j['id'],
                'topic': j['topic'][:50] + ('...' if len(j['topic']) > 50 else ''),
                'queue_position': j.get('queue_position', 0),
                'created_at': j['created_at']
            } for j in pending_jobs[:10]  # Return max 10 pending jobs
        ],
        'processing_jobs': [
            {
                'id': j['id'],
                'topic': j['topic'][:50] + ('...' if len(j['topic']) > 50 else ''),
                'progress': j.get('progress', ''),
                'created_at': j['created_at']
            } for j in processing_jobs
        ]
    })


@app.route('/api/cancel/<job_id>', methods=['POST', 'DELETE'])
def api_cancel(job_id):
    """
    Cancel a pending job.
    Only pending jobs can be cancelled.
    """
    job = get_job(job_id)
    
    if not job:
        return jsonify({
            'success': False,
            'error': 'Job not found'
        }), 404
    
    if job['status'] != 'pending':
        return jsonify({
            'success': False,
            'error': f"Cannot cancel job with status '{job['status']}'. Only pending jobs can be cancelled."
        }), 400
    
    update_job(job_id, status='cancelled', progress='Cancelled by user')
    
    return jsonify({
        'success': True,
        'message': 'Job cancelled'
    })


@app.route('/api/videos', methods=['GET'])
def api_videos():
    """
    Get list of all generated videos.
    
    Query params:
    - limit: max number of videos (default 50)
    - offset: pagination offset (default 0)
    """
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    videos = load_videos()
    
    # Apply pagination
    paginated = videos[offset:offset + limit]
    
    # Add full URLs
    for video in paginated:
        video['full_url'] = request.host_url.rstrip('/') + video.get('url', '')
    
    return jsonify({
        'success': True,
        'total': len(videos),
        'limit': limit,
        'offset': offset,
        'videos': paginated
    })

# Ensure media directories exist on startup
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

if __name__ == '__main__':
    # Load existing jobs
    load_jobs()
    
    # Initial sync of videos
    sync_videos_with_filesystem()
    print(f"Starting server with {len(load_videos())} videos in gallery")
    
    # Start the background worker for processing jobs
    start_worker()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5002, use_reloader=False)
else:
    # When running with gunicorn, also start worker
    load_jobs()
    sync_videos_with_filesystem()
    start_worker()
    print(f"[GUNICORN] Started with {len(load_videos())} videos, worker running: {worker_running}")
