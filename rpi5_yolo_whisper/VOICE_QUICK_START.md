# 🚀 Quick Start - Voice Command Debugging

## Update Code First
```bash
cd ~/rasp-object-detection
git fetch origin
git reset --hard origin/main
cd rpi5_yolo_whisper
source venv/bin/activate
```

---

## Step 1: Test Voice Panel Display (30 seconds)

```bash
python test_gui_voice_panel.py
```

**What you should see:**
- Window opens
- "🎤 Voice Status" panel visible
- Click "Start Simulation" → Colors change every 2 seconds
- Green → Yellow → Orange → Blue → Green → Gray

**If this doesn't work:** Tkinter issue, reinstall with `sudo apt-get install python3-tk`

---

## Step 2: Test Voice Components (2 minutes)

```bash
python test_voice.py
```

**What it tests:**
1. ✅ Imports (sounddevice, faster-whisper)
2. ✅ Microphone (records 2 seconds)
3. ✅ Speech recognition (say something)

**Expected output:**
```
Testing Imports...
✅ sounddevice imported
✅ soundfile imported
✅ faster-whisper imported
...
Testing Microphone...
🎤 Testing microphone recording (2 seconds)...
   Say something!
✅ Recording successful!
   Max amplitude: 0.XXXX
✅ Audio level looks good!
...
Testing Speech Recognition...
🎤 Recording for 3 seconds...
   Say something like 'detect' or 'start'
✅ Transcription: 'YOUR WORDS HERE'
```

**If tests fail:** See what failed and fix that specific component

---

## Step 3: Run Main GUI

```bash
python gui_mobile_detector.py
```

---

## Common Fixes

### Voice panel not showing?
```bash
sudo apt-get install python3-tk python3-pil.imagetk
```

### Voice not working?
```bash
pip install --upgrade sounddevice soundfile faster-whisper
```

### Microphone test?
```bash
arecord -d 3 test.wav && aplay test.wav
```

---

## Where is Voice Status Panel?

In the GUI, it's located:
```
┌─────────────────────────┐
│   Title                 │
├─────────────────────────┤
│   Video Feed            │
├─────────────────────────┤
│   Controls              │
├─────────────────────────┤
│   Settings              │
├─────────────────────────┤
│   Statistics            │
├─────────────────────────┤
│  🎤 Voice Status        │  ← HERE!
│  ┌───────────────────┐  │
│  │ Green/Yellow text │  │
│  └───────────────────┘  │
├─────────────────────────┤
│   Status Bar            │
└─────────────────────────┘
```

The text changes color:
- **Gray**: OFF
- **Green**: Listening for IRIS
- **Yellow**: IRIS detected
- **Orange**: Recording
- **Blue**: Processing
- **Green**: Success
- **Red**: Error

---

## Test Sequence

1. **Run:** `python test_gui_voice_panel.py`
   - ✅ Voice panel shows? → Proceed to step 2
   - ❌ Doesn't show? → Reinstall python3-tk

2. **Run:** `python test_voice.py`
   - ✅ All tests pass? → Proceed to step 3
   - ❌ Some fail? → Fix that component first

3. **Run:** `python gui_mobile_detector.py`
   - ✅ See voice panel? → Try voice commands
   - ❌ Don't see it? → Check terminal for errors

4. **Click** "🎤 Voice Control: ON"
   - ✅ Button turns green? → Say "IRIS"
   - ❌ Stays red? → Check terminal errors

5. **Say** "IRIS"
   - ✅ Status turns yellow? → Say "DETECT"
   - ❌ Nothing happens? → Check `test_voice.py` results

---

## Debug Info to Share

If it still doesn't work, run these and share output:

```bash
# Test results
python test_voice.py > debug_voice.txt 2>&1

# Audio devices
arecord -l > debug_audio.txt

# Python packages
pip list | grep -E "sound|whisper|faster" > debug_packages.txt

# Share these 3 files
cat debug_voice.txt
cat debug_audio.txt
cat debug_packages.txt
```

---

**Most common issue:** Voice panel IS there, but you need to **scroll down** to see it! It's below Statistics.

**Second most common:** Microphone not configured. Run `alsamixer` and ensure mic isn't muted (F4 to see capture devices).
