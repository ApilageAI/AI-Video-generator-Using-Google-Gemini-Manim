# Application Management Commands

## Service Control

### Stop the service
```bash
sudo systemctl stop video-generator
```

### Start the service
```bash
sudo systemctl start video-generator
```

### Restart the service
```bash
sudo systemctl restart video-generator
```

### Check service status
```bash
sudo systemctl status video-generator
```

### Enable auto-start on boot
```bash
sudo systemctl enable video-generator
```

### Disable auto-start on boot
```bash
sudo systemctl disable video-generator
```

---

## View Logs

### View real-time logs
```bash
sudo journalctl -u video-generator -f
```

### View last 100 log lines
```bash
sudo journalctl -u video-generator -n 100 --no-pager
```

### View Apache error logs
```bash
sudo tail -f /var/log/httpd/nova_error.log
```

### View Apache access logs
```bash
sudo tail -f /var/log/httpd/nova_access.log
```

---

## Update Workflow

### Quick restart after code changes
```bash
cd /home/nova/public_html
sudo systemctl restart video-generator
```

### Full update with dependency installation
```bash
# Stop service
sudo systemctl stop video-generator

# Navigate to project directory
cd /home/nova/public_html

# Activate virtual environment
source venv/bin/activate

# Update dependencies (if requirements.txt changed)
pip install -r requirements.txt

# Restart service
sudo systemctl start video-generator

# Verify it's running
sudo systemctl status video-generator
```

### Update from Git repository
```bash
# Stop service
sudo systemctl stop video-generator

# Pull latest changes
cd /home/nova/public_html
git pull

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start video-generator
```

---

## Apache Management

### Restart Apache
```bash
sudo systemctl restart httpd
```

### Test Apache configuration
```bash
sudo httpd -t
```

### View Apache status
```bash
sudo systemctl status httpd
```

---

## Testing & Debugging

### Test if Flask app responds locally
```bash
curl http://127.0.0.1:5000/health
```

### Test from outside
```bash
curl https://nova.apilageai.lk/health
```

### Run app directly for debugging (stop service first)
```bash
# Stop the service
sudo systemctl stop video-generator

# Run directly
cd /home/nova/public_html
source venv/bin/activate
python3 wsgi.py

# Press Ctrl+C to stop, then restart service
sudo systemctl start video-generator
```

### Check if port 5000 is listening
```bash
sudo netstat -tlnp | grep 5000
```

### Check installed Python packages
```bash
cd /home/nova/public_html
source venv/bin/activate
pip list
```

---

## Maintenance

### Check disk space
```bash
df -h
```

### Check video storage usage
```bash
du -sh /home/nova/public_html/uploads
du -sh /home/nova/public_html/media
```

### Clean old videos (older than 7 days)
```bash
find /home/nova/public_html/uploads -name "*.mp4" -mtime +7 -delete
find /home/nova/public_html/media/videos -name "*.mp4" -mtime +7 -delete
```

### Check service logs for errors
```bash
sudo journalctl -u video-generator -p err -n 50
```

---

## File Permissions

### Fix permissions if needed
```bash
cd /home/nova/public_html
sudo chown -R nova:nova .
chmod 755 media uploads videos
chmod 755 media/videos/generated/480p15
```

---

## Emergency Commands

### Force stop the service
```bash
sudo systemctl kill video-generator
```

### Reload systemd after service file changes
```bash
sudo systemctl daemon-reload
```

### View service configuration
```bash
cat /etc/systemd/system/video-generator.service
```

### Edit service configuration
```bash
sudo nano /etc/systemd/system/video-generator.service
# After editing:
sudo systemctl daemon-reload
sudo systemctl restart video-generator
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Stop | `sudo systemctl stop video-generator` |
| Start | `sudo systemctl start video-generator` |
| Restart | `sudo systemctl restart video-generator` |
| Status | `sudo systemctl status video-generator` |
| Logs | `sudo journalctl -u video-generator -f` |
| Test health | `curl http://127.0.0.1:5000/health` |

---

## Common Issues

### Issue: Service won't start
```bash
# Check logs for errors
sudo journalctl -u video-generator -n 50 --no-pager

# Test dependencies
cd /home/nova/public_html
source venv/bin/activate
python3 -c "import flask, manim; print('OK')"
```

### Issue: Videos not generating
```bash
# Check if FFmpeg is installed
which ffmpeg
ffmpeg -version

# Check if worker is running
sudo journalctl -u video-generator -f
# Then try generating a video from web interface
```

### Issue: Port already in use
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>
```

---

## Application Info

- **Project Path:** `/home/nova/public_html`
- **Virtual Environment:** `/home/nova/public_html/venv`
- **Service Name:** `video-generator`
- **Port:** `5000` (internal)
- **Domain:** `https://nova.apilageai.lk`
- **User:** `nova`
- **Python Version:** Check with `python3 --version`

---

**Last Updated:** January 27, 2026
