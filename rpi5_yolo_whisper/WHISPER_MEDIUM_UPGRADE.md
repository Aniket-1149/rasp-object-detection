# 🎤 Whisper Medium Model Upgrade - Testing Steps

## ✅ What Changed?

**Updated:** `.env` file - `WHISPER_MODEL=small` → `WHISPER_MODEL=medium`

**Why?** The medium model is much better at handling low-quality audio and will improve voice command transcription accuracy.

---

## 📋 Step-by-Step Testing Instructions

### **Step 1: Pull Latest Changes on Raspberry Pi**

```bash
# SSH into your Raspberry Pi
cd ~/rasp-object-detection
git pull origin main
cd rpi5_yolo_whisper
```

### **Step 2: Activate Virtual Environment**

```bash
source venv/bin/activate
```

### **Step 3: Run the Mobile GUI**

```bash
python gui_mobile_detector.py
```

**⏳ IMPORTANT - First Run Only:**
- The medium model (~1.5GB) will download automatically
- This may take **5-10 minutes** depending on your internet speed
- You'll see download progress in the terminal
- Subsequent runs will be instant (model is cached)

### **Step 4: Test Voice Commands**

Once the GUI opens:

#### Test 1: Start Detection
1. **Say loudly:** "IRIS"
2. **Wait for:**
   - Voice status panel turns **🟢 GREEN** ("Wake word detected!")
   - You hear: "Listening for command"
   - Voice status panel turns **🟠 ORANGE** ("Listening for command...")
3. **Say clearly:** "START"
4. **Expected result:**
   - Detection should start
   - Camera feed shows bounding boxes
   - Voice status panel turns **🔵 BLUE** ("Command: START")

#### Test 2: Stop Detection
1. **Say loudly:** "IRIS"
2. **Wait for:** "Listening for command"
3. **Say clearly:** "STOP"
4. **Expected result:**
   - Detection stops
   - Camera feed continues but no boxes
   - Voice status panel turns **🔵 BLUE** ("Command: STOP")

---

## 🔍 Monitor the Logs

Watch the terminal output for transcription quality:

**Good transcription:**
```
INFO - Segment 0: 'start'
INFO - Transcribed text: 'start'
INFO - ✅ Starting detection via voice command
```

**Failed transcription:**
```
INFO - Segment 0: 'All right.'  ❌ Wrong!
INFO - Transcribed text: 'All right.'
WARNING - ⚠️ Unclear command: 'All right.'
```

---

## 🎯 Expected Improvements

With the **medium model**, you should see:

| Before (Small) | After (Medium) |
|---------------|----------------|
| "START" → "Thank you" ❌ | "START" → "start" ✅ |
| "STOP" → "All right" ❌ | "STOP" → "stop" ✅ |
| Success rate: ~0% | Success rate: ~70-90% |

---

## 💡 Tips for Best Results

### 1. **Increase Microphone Volume** (HIGHLY RECOMMENDED)

Your current mic amplitude is **0.0079** (very low). Increase it:

```bash
# Open audio mixer
alsamixer

# Press F4 (Capture devices)
# Use arrow keys to select USB microphone
# Press UP arrow to increase volume to 80-90%
# Press ESC to exit
```

**Target:** Amplitude should be **> 0.05** for reliable transcription

### 2. **Speak Clearly and Loudly**

- Say "IRIS" **loudly** to activate wake word
- Wait for "Listening for command" audio feedback
- Say "START" or "STOP" **clearly** and **loudly**
- Don't rush - give the system time to process

### 3. **Check Voice Status Panel**

The colored status panel shows:
- 🟢 **GREEN** = Wake word detected
- 🟡 **YELLOW** = Listening for wake word
- 🟠 **ORANGE** = Recording command
- 🔵 **BLUE** = Command processed
- 🔴 **RED** = Error occurred

---

## 🐛 Troubleshooting

### Problem: Model download fails
```bash
# Check internet connection
ping google.com

# Try manual download
python -c "from faster_whisper import WhisperModel; WhisperModel('medium', device='cpu')"
```

### Problem: Commands still not recognized
```bash
# Test microphone volume
python test_voice.py

# Look for "Audio amplitude" - should be > 0.05
# If too low, increase with alsamixer
```

### Problem: "IRIS" not detected
- Wake word detection uses a different model (working fine)
- Issue is only with command transcription after wake word
- Make sure you're saying "START" or "STOP" after "IRIS"

---

## 📊 Test Results Template

Fill this out after testing:

```
Date: ___________
Time: ___________

Test 1: IRIS → START
- Wake word detected: YES / NO
- Audio feedback heard: YES / NO
- Transcription result: "__________"
- Detection started: YES / NO

Test 2: IRIS → STOP
- Wake word detected: YES / NO
- Audio feedback heard: YES / NO
- Transcription result: "__________"
- Detection stopped: YES / NO

Microphone amplitude: _________
Audio quality: Good / Fair / Poor

Notes:
_________________________________
_________________________________
```

---

## 📝 Alternative Commands (Flexible Matching)

The system accepts multiple variations:

**To START:**
- "start"
- "start detection"
- "begin"
- "starred" (common misrecognition)
- "star" (common misrecognition)

**To STOP:**
- "stop"
- "stop detection"
- "end"
- "stopped" (common misrecognition)
- "top" (common misrecognition)

---

## ✅ Success Criteria

You'll know it's working when:
1. ✅ Wake word "IRIS" consistently triggers response
2. ✅ You hear "Listening for command" audio feedback
3. ✅ Terminal logs show correct transcriptions ("start"/"stop")
4. ✅ Detection starts/stops as commanded
5. ✅ Voice status panel shows correct colors

---

## 🚀 Next Steps After Success

Once voice commands work:
1. Test different camera FOV settings
2. Adjust confidence threshold slider
3. Try NMS IoU threshold adjustment
4. Enable auto-announce for detected objects
5. Test session statistics tracking

---

## 📞 If Still Having Issues

Provide these details:
1. Terminal log showing "Segment 0:" transcription
2. Output from `test_voice.py` (mic amplitude)
3. Output from `alsamixer` (current mic volume %)
4. What you said vs. what was transcribed

---

**Good luck! The medium model should significantly improve accuracy! 🎉**
