# Deployment Guide for AlmaLinux + Virtualmin
## Deploying AI Video Generator to nova.apilageai.lk

---

## Prerequisites on Server

1. **Python 3.9 or higher**
2. **FFmpeg** (required for video processing)
3. **System dependencies for Manim**

---

## Step-by-Step Deployment Instructions

### 1. Connect to Your Server and Navigate to Project

```bash
# SSH into your server (if not already connected)
ssh your_username@nova.apilageai.lk

# Navigate to the public_html folder where your project is
cd ~/public_html
# or the full path based on Virtualmin setup:
cd /home/your_domain/public_html
```

### 2. Install System Dependencies

```bash
# Install FFmpeg and required libraries
sudo dnf install -y ffmpeg ffmpeg-devel
sudo dnf install -y cairo cairo-devel pango pango-devel
sudo dnf install -y python3-devel gcc gcc-c++
sudo dnf install -y libffi-devel openssl-devel
```

### 3. Set Up Python Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 4. Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# If you encounter any issues, install manually:
pip install Flask==3.0.0
pip install google-generativeai==0.8.3
pip install gTTS==2.5.0
pip install python-dotenv==1.0.0
pip install manim==0.18.0
pip install pydub==0.25.1
pip install gunicorn  # Production WSGI server
```

### 5. Verify Environment Variables

Ensure your `.env` file has all required credentials:

```bash
# View current .env file
cat .env

# Your .env should contain:
# GEMINI_API_KEY=your_actual_key
# ELEVENLABS_API_KEY=your_key (optional)
# AUTH_CODE=your_auth_code
# API_KEY=your_api_key
# FLASK_ENV=production
# DEBUG=False
```

### 6. Create Required Directories

```bash
# Create necessary directories for the application
mkdir -p media/videos/generated/480p15
mkdir -p media/images
mkdir -p media/texts
mkdir -p uploads
mkdir -p videos
mkdir -p static
mkdir -p templates

# Set proper permissions
chmod 755 media uploads videos
chmod 755 media/videos/generated/480p15
```

### 7. Test the Application Locally First

```bash
# Test if the app runs correctly
python app.py

# Or test with the WSGI entry point
python wsgi.py

# If successful, press Ctrl+C to stop
```

### 8. Set Up with Gunicorn (Recommended for Production)

Create a systemd service file for automatic startup:

```bash
sudo nano /etc/systemd/system/video-generator.service
```

Add the following content (adjust paths to match your setup):

```ini
[Unit]
Description=AI Video Generator Flask Application
After=network.target

[Service]
Type=notify
User=your_username
Group=your_username
WorkingDirectory=/home/your_domain/public_html
Environment="PATH=/home/your_domain/public_html/venv/bin"
ExecStart=/home/your_domain/public_html/venv/bin/gunicorn \
    --bind 127.0.0.1:5000 \
    --workers 2 \
    --timeout 300 \
    --worker-class sync \
    wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+X, then Y, then Enter).

### 9. Start and Enable the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start the service
sudo systemctl start video-generator

# Enable on boot
sudo systemctl enable video-generator

# Check status
sudo systemctl status video-generator
```

### 10. Configure Virtualmin/Apache Reverse Proxy

Now configure your domain to proxy requests to the Gunicorn server:

**Option A: Using Virtualmin Web UI**

1. Log into Virtualmin
2. Go to: **Server Configuration → Website Options**
3. Add a proxy pass configuration

**Option B: Manual Apache Configuration**

Edit your domain's Apache configuration:

```bash
sudo nano /etc/httpd/conf.d/nova.apilageai.lk.conf
```

Add the following inside your `<VirtualHost>` block:

```apache
<VirtualHost *:80>
    ServerName nova.apilageai.lk
    ServerAlias www.nova.apilageai.lk
    
    # Proxy configuration
    ProxyPreserveHost On
    ProxyPass /static/ !
    ProxyPass /media/ !
    ProxyPass /uploads/ !
    ProxyPass /videos/ !
    
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    # Serve static files directly from Apache
    Alias /static /home/your_domain/public_html/static
    Alias /media /home/your_domain/public_html/media
    Alias /uploads /home/your_domain/public_html/uploads
    Alias /videos /home/your_domain/public_html/videos
    
    <Directory /home/your_domain/public_html/static>
        Require all granted
    </Directory>
    
    <Directory /home/your_domain/public_html/media>
        Require all granted
    </Directory>
    
    <Directory /home/your_domain/public_html/uploads>
        Require all granted
    </Directory>
    
    <Directory /home/your_domain/public_html/videos>
        Require all granted
    </Directory>
    
    # Increase timeout for video generation
    ProxyTimeout 600
    
    ErrorLog /var/log/httpd/nova.apilageai.lk_error.log
    CustomLog /var/log/httpd/nova.apilageai.lk_access.log combined
</VirtualHost>
```

### 11. Restart Apache

```bash
# Test Apache configuration
sudo apachectl configtest

# If OK, restart Apache
sudo systemctl restart httpd
```

### 12. Configure Firewall (if needed)

```bash
# Allow HTTP and HTTPS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 13. Set Up SSL/HTTPS (Recommended)

```bash
# Install certbot
sudo dnf install -y certbot python3-certbot-apache

# Get SSL certificate
sudo certbot --apache -d nova.apilageai.lk -d www.nova.apilageai.lk
```

---

## Verification Steps

### 1. Check if Application is Running

```bash
# Check service status
sudo systemctl status video-generator

# Check if port 5000 is listening
sudo netstat -tlnp | grep 5000

# Check application logs
sudo journalctl -u video-generator -f
```

### 2. Test the Website

Open your browser and visit:
- `http://nova.apilageai.lk` (or `https://` if SSL configured)
- `http://nova.apilageai.lk/health` - Should show health check status
- `http://nova.apilageai.lk/api-docs` - API documentation

### 3. Monitor Logs

```bash
# Application logs
sudo journalctl -u video-generator -f

# Apache logs
sudo tail -f /var/log/httpd/nova.apilageai.lk_error.log
sudo tail -f /var/log/httpd/nova.apilageai.lk_access.log
```

---

## Troubleshooting

### Issue: "Module not found" errors

```bash
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart video-generator
```

### Issue: FFmpeg not found

```bash
which ffmpeg
# If not found, install:
sudo dnf install -y ffmpeg
```

### Issue: Permission denied errors

```bash
# Set proper ownership
sudo chown -R your_username:your_username /home/your_domain/public_html
chmod -R 755 /home/your_domain/public_html
chmod -R 775 media uploads videos
```

### Issue: Port 5000 already in use

```bash
# Find what's using the port
sudo lsof -i :5000

# Kill the process or change port in service file
```

### Issue: Videos not generating

Check:
1. GEMINI_API_KEY is valid in `.env`
2. FFmpeg is installed: `ffmpeg -version`
3. Manim is installed: `manim --version`
4. Check logs: `sudo journalctl -u video-generator -f`

---

## Quick Start Commands (Summary)

```bash
# Navigate to project
cd ~/public_html

# Activate virtual environment
source venv/bin/activate

# Start application (for testing)
python wsgi.py

# Or start the service (production)
sudo systemctl start video-generator
sudo systemctl status video-generator

# Check logs
sudo journalctl -u video-generator -f

# Restart after changes
sudo systemctl restart video-generator
```

---

## Maintenance

### Update the Application

```bash
cd ~/public_html
source venv/bin/activate
git pull  # If using git
pip install -r requirements.txt --upgrade
sudo systemctl restart video-generator
```

### Monitor Disk Space

```bash
# Video files can be large, monitor disk usage
df -h
du -sh media/ uploads/ videos/
```

### Clean Old Videos

```bash
# Remove videos older than 7 days
find uploads/ -name "*.mp4" -mtime +7 -delete
find media/videos/ -name "*.mp4" -mtime +7 -delete
```

---

## Important Notes

1. **Security**: Your API keys are sensitive - ensure `.env` is not publicly accessible
2. **Performance**: Video generation is CPU-intensive - consider server resources
3. **Storage**: Videos can consume significant disk space - implement cleanup routines
4. **Timeouts**: Increase Apache/Gunicorn timeouts for long video generation
5. **Monitoring**: Set up monitoring for the service and disk space

---

## Support

If you encounter issues:
1. Check logs: `sudo journalctl -u video-generator -f`
2. Verify dependencies: `pip list`
3. Test locally: `python wsgi.py`
4. Check Apache config: `sudo apachectl configtest`

Your application should now be live at **https://nova.apilageai.lk** 🚀
