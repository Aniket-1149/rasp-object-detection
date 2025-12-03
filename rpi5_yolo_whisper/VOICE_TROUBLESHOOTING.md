# 🔧 Voice Command Troubleshooting Guide

## 🐛 Common Issues and Solutions

### Issue 1: Voice Status Panel Not Showing

**Test it:**
```bash
cd ~/rasp-object-detection/rpi5_yolo_whisper
source venv/bin/activate
python test_gui_voice_panel.py
```

This will show a simple GUI with just the voice status panel. If this doesn't work, there's a tkinter issue.

**Expected output:**
- Window opens with "Voice Status Panel Test"
- You see "🎤 Voice Status" section
- Click "Start Simulation" to see status changes

---

### Issue 2: Voice Commands Not Working

**Test components one by one:**

#### Step 1: Test Microphone
```bash
# Record and playback test
arecord -d 3 test.wav
aplay test.wav
```

If you don't hear your voice, microphone isn't working.

#### Step 2: Test All Voice Components
```bash
cd ~/rasp-object-detection/rpi5_yolo_whisper
source venv/bin/activate
python test_voice.py
```

This will test:
1. ✅ All imports (sounddevice, faster-whisper, etc.)
2. ✅ Microphone recording
3. ✅ Speech recognition

**Expected output:**
```
Testing Imports...
✅ sounddevice imported
✅ soundfile imported
✅ faster-whisper imported
...
Testing Microphone...
📋 Available Audio Devices:
  [0] USB PnP Sound Device
...
Testing Speech Recognition...
🎤 Recording for 3 seconds...
   Say something like 'detect' or 'start'
✅ Transcription: 'detect'
```

#### Step 3: Check Audio Devices
```python
python -c "import sounddevice; print(sounddevice.query_devices())"
```

Make sure you see your microphone listed.

---

### Issue 3: Wake Word Not Detected

**Possible causes:**
1. Microphone volume too low
2. Too much background noise
3. Wake word model not loaded

**Test wake word separately:**
```bash
python -c "from offline_wake_word import OfflineWakeWordDetector; d = OfflineWakeWordDetector('iris'); print('Say IRIS now...'); result = d.listen_for_wake_word(); print(f'Detected: {result}')"
```

Say "IRIS" clearly when prompted.

---

### Issue 4: GUI Shows But No Voice Feedback

**Check these:**

1. **Is voice control ON?**
   - Button should say "🎤 Voice Control: ON" (green)
   - Not "🎤 Voice Control: OFF" (red)

2. **Check terminal output:**
   ```bash
   python gui_mobile_detector.py
   ```
   
   Look for logs like:
   ```
   Listening for wake word 'IRIS'...
   ✅ Wake word 'IRIS' detected!
   Recording command...
   Command recognized: 'detect'
   ```

3. **Voice Status Panel location:**
   - Should be between "Statistics" and "Status Bar"
   - Has big bold colored text
   - Changes color when you speak

---

## 🛠️ Fix Common Problems

### Problem: "No module named 'sounddevice'"

```bash
source venv/bin/activate
pip install sounddevice soundfile
```

### Problem: "No module named 'faster_whisper'"

```bash
pip install faster-whisper
```

### Problem: Microphone not found

```bash
# List audio devices
arecord -l

# Test specific device
arecord -D hw:1,0 -d 3 test.wav
```

### Problem: "ALSA lib" errors (can ignore these)

These warnings are normal on Raspberry Pi:
```
ALSA lib confmisc.c:767:(parse_card) cannot find card '0'
```

They don't affect functionality.

### Problem: Low audio volume

```bash
# Increase microphone gain
alsamixer
# Press F4 for Capture, use arrow keys to adjust
```

### Problem: Wake word detector loads but doesn't detect

**Solutions:**
1. Say "IRIS" louder and clearer
2. Reduce background noise
3. Get closer to microphone (5-15cm optimal)
4. Check mic isn't muted in alsamixer

---

## 📊 Debug Checklist

Run through this checklist:

- [ ] `python test_gui_voice_panel.py` shows voice panel ✅
- [ ] `arecord -d 3 test.wav && aplay test.wav` works ✅
- [ ] `python test_voice.py` passes all tests ✅
- [ ] Voice control button turns green when clicked ✅
- [ ] Voice status panel appears below statistics ✅
- [ ] Terminal shows "Listening for wake word..." ✅
- [ ] Saying "IRIS" shows "IRIS detected!" ✅
- [ ] Saying command after IRIS starts/stops detection ✅

---

## 🎤 Optimal Voice Command Usage

### Best Practices:

1. **Environment:**
   - Quiet room (low background noise)
   - Microphone 10-20cm from mouth
   - No loud music or TV

2. **Speaking:**
   - Speak clearly and at normal volume
   - Pause briefly between "IRIS" and command
   - Say: "IRIS" → (wait for yellow status) → "DETECT"

3. **Timing:**
   - Wait for voice status to turn yellow ("IRIS detected!")
   - Then say your command within 3 seconds
   - Don't rush, speak naturally

### Command Examples:

```
You: "IRIS"
GUI: ✅ IRIS detected! Say your command... (Yellow)

You: "DETECT"
GUI: 🎙️ Recording command... (Orange)
GUI: ⚙️ Processing speech... (Blue)
GUI: ✅ Heard: 'detect' (Green)
System: Starts detection
```

---

## 🔍 Advanced Debugging

### Enable verbose logging:

Edit `gui_mobile_detector.py`, change logging level:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Check Whisper model:

```bash
ls -lh ~/.cache/whisper/
# Should see: small.pt or similar
```

### Test faster-whisper separately:

```python
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
print("Model loaded successfully!")
```

---

## 📞 Still Not Working?

If voice commands still don't work after all tests:

1. **Provide this info:**
   ```bash
   # Run and share output:
   python test_voice.py > voice_test_output.txt 2>&1
   
   # Also share:
   arecord -l
   python -c "import sounddevice; print(sounddevice.query_devices())"
   ```

2. **Try USB microphone:**
   - Some built-in mics don't work well
   - USB microphones are more reliable

3. **Check Raspberry Pi audio config:**
   ```bash
   sudo raspi-config
   # Go to: System Options → Audio
   # Make sure correct device is selected
   ```

---

## ✅ Success Criteria

You know it's working when:

1. ✅ Click "Voice Control ON" → Button turns green
2. ✅ Voice Status shows: "🎤 Listening for 'IRIS'..." (Green)
3. ✅ Say "IRIS" → Shows: "✅ IRIS detected! Say your command..." (Yellow)
4. ✅ Say "DETECT" → Shows: "🎙️ Recording..." then "⚙️ Processing..." then "✅ Heard: 'detect'" (Orange → Blue → Green)
5. ✅ Detection starts automatically
6. ✅ Terminal shows all steps in logs

**All these steps should happen within 5-7 seconds total.**

---

## 🎯 Quick Fix Commands

```bash
# Update code
cd ~/rasp-object-detection
git fetch origin
git reset --hard origin/main

# Install/update packages
cd rpi5_yolo_whisper
source venv/bin/activate
pip install --upgrade sounddevice soundfile faster-whisper

# Test GUI panel
python test_gui_voice_panel.py

# Test voice components
python test_voice.py

# Run main app
python gui_mobile_detector.py
```

---

**Need more help?** Share the output of `python test_voice.py` and describe exactly what you see/hear.
