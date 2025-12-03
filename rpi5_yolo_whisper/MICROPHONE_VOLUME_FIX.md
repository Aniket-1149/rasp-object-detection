# 🎤 Microphone Volume Fix

## Problem: "VAD filter removed all audio"

This means your microphone volume is too low. The Voice Activity Detection (VAD) thinks you're not speaking.

---

## ✅ Quick Fix: Increase Microphone Volume

### Method 1: Using alsamixer (Recommended)

```bash
alsamixer
```

1. Press **F4** to switch to "Capture" view (microphone input)
2. You'll see your microphone device (e.g., "Mic")
3. Use **↑ arrow key** to increase volume to **80-90%**
4. Press **Esc** to exit

**Visual guide:**
```
┌─────────────────────────────────┐
│ Capture                         │
│ ┌───────┐                       │
│ │███████│ 85%  ← Aim for this   │
│ │███████│                       │
│ │███████│                       │
│ └───────┘                       │
│   Mic                           │
└─────────────────────────────────┘
```

### Method 2: Using amixer command

```bash
# Check current volume
amixer get Mic

# Set to 90%
amixer set Mic 90%

# Or set capture volume
amixer set Capture 90%
```

### Method 3: Using pavucontrol (if installed)

```bash
sudo apt-get install pavucontrol
pavucontrol
```

- Go to "Input Devices" tab
- Increase slider to 90-100%

---

## 🧪 Test After Adjusting

```bash
cd ~/rasp-object-detection/rpi5_yolo_whisper
source venv/bin/activate

# Quick mic test - should be LOUDER now
arecord -d 3 test.wav && aplay test.wav

# Test with voice recognition
python test_voice.py
```

**Expected output:**
```
Testing Microphone...
🎤 Testing microphone recording (2 seconds)...
   Say something!
✅ Recording successful!
   Max amplitude: 0.1486  ← Should be > 0.05
✅ Audio level looks good!
```

If amplitude is still < 0.05, increase volume more!

---

## 🔧 Alternative: Disable VAD Filter

If you can't increase mic volume, you can disable the VAD filter temporarily to test.

Edit `whisper_stt.py`, change line ~168:

```python
# From:
vad_filter=True,

# To:
vad_filter=False,  # Disable VAD if mic is very quiet
```

**Note:** This is not recommended long-term as it may transcribe background noise.

---

## 📊 Microphone Volume Levels

| Max Amplitude | Status | Action |
|--------------|---------|---------|
| > 0.10 | ✅ Excellent | Perfect for voice commands |
| 0.05 - 0.10 | ✅ Good | Should work fine |
| 0.02 - 0.05 | ⚠️ Low | Increase volume with alsamixer |
| < 0.02 | ❌ Too Low | VAD will filter it out |

Your test showed: **0.0079** → Too low! Increase to at least 0.05.

---

## 🎯 Step-by-Step Fix

1. **Open alsamixer:**
   ```bash
   alsamixer
   ```

2. **Press F4** (switch to Capture)

3. **Find your USB microphone:**
   - Look for "USB PnP Sound Device" or "Mic"

4. **Increase volume:**
   - Press **↑** arrow key multiple times
   - Aim for 80-90% (shown as percentage)

5. **Save and exit:**
   - Press **Esc**
   - Settings auto-save

6. **Test immediately:**
   ```bash
   arecord -d 3 test_loud.wav
   # SPEAK LOUDLY during recording
   aplay test_loud.wav
   # Should hear yourself clearly
   ```

7. **Run voice test again:**
   ```bash
   python test_voice.py
   ```

---

## 🔊 Pro Tips

1. **Speak clearly and loudly** during tests
2. **Get closer to mic** (10-15cm is optimal)
3. **Reduce background noise** (turn off fans, music, etc.)
4. **Check mic isn't muted:**
   - In alsamixer, look for "MM" under mic (means muted)
   - Press **M** key to unmute (should show "00" instead)

---

## ✅ Success Criteria

After adjusting volume, you should see:

```bash
python test_voice.py
```

Output:
```
Testing Microphone...
✅ Recording successful!
   Max amplitude: 0.1234  ← HIGHER now!
✅ Audio level looks good!

Testing Speech Recognition...
✅ Transcription: 'hello world'  ← YOUR WORDS!

📊 Test Summary
Speech: ✅ PASS  ← Should pass!
```

---

## 🆘 Still Not Working?

If amplitude is still too low after increasing volume:

1. **Try different USB port** on Raspberry Pi
2. **Check USB mic LED** (if it has one) - should be lit
3. **Test with different application:**
   ```bash
   arecord -D hw:0,0 -f cd -d 5 test_hw.wav
   aplay test_hw.wav
   ```
4. **Verify mic is detected:**
   ```bash
   arecord -l
   # Should show: USB PnP Sound Device at hw:0,0
   ```

---

**TL;DR:** Run `alsamixer`, press F4, increase Mic to 80-90%, test with `python test_voice.py` 🎤
