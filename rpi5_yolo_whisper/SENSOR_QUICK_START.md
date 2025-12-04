# 🎯 Quick Setup Summary - Visual Assistance Sensors

## 📦 What's Included

You now have complete integration for:
- **HC-SR04 Ultrasonic Sensor** - Distance measurement (0.5-13 feet)
- **MPU9250 9-Axis IMU** - Fall detection with accelerometer/gyroscope/magnetometer
- **Event System** - For app/SMTP notifications

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Pull Latest Code

```bash
cd ~/rasp-object-detection
git pull origin main
cd rpi5_yolo_whisper
source venv/bin/activate
```

### Step 2: Install Sensor Libraries

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y i2c-tools python3-dev python3-setuptools

# Install pigpio from source (not in Trixie repos)
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
cd ..
rm -rf pigpio-master master.zip

# Install Python packages in venv
pip install smbus2 pigpio

# Enable I2C
sudo raspi-config
# Navigate: Interface Options → I2C → Enable → Finish → Reboot
```

### Step 3: Start pigpio Daemon

```bash
# Start pigpio daemon (runs in background)
sudo pigpiod

# Verify it's running
pgrep pigpiod  # Should show a process ID number
```

**Note:** If you want pigpiod to auto-start on boot, create a systemd service:
```bash
sudo tee /etc/systemd/system/pigpiod.service > /dev/null << 'EOF'
[Unit]
Description=Pigpio daemon
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/bin/pigpiod
ExecStop=/bin/systemctl kill pigpiod
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

### Step 4: Wire Hardware

**CRITICAL: Follow `HARDWARE_SETUP_GUIDE.md` exactly!**

**HC-SR04:**
- VCC → 5V (Pin 2)
- GND → GND (Pin 6)
- TRIG → GPIO23 (Pin 16)
- ECHO → GPIO24 (Pin 18) **⚠️ THROUGH VOLTAGE DIVIDER!**
  - Echo → 1kΩ → GPIO24
  - Echo → 2kΩ → GND

**MPU9250:**
- VCC → 3.3V (Pin 1) **⚠️ NOT 5V!**
- GND → GND (Pin 6)
- SDA → GPIO2 (Pin 3)
- SCL → GPIO3 (Pin 5)

### Step 5: Test Sensors

```bash
# Verify I2C (should show 0x68 or 0x69)
sudo i2cdetect -y 1

# Test ultrasonic (10 seconds)
python test_ultrasonic.py --duration 10

# Test IMU (10 seconds)
python test_mpu9250.py --duration 10

# Calibrate IMU (optional but recommended)
python test_mpu9250.py --calibrate
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `HARDWARE_SETUP_GUIDE.md` | Complete wiring diagrams and pin connections |
| `SENSOR_INTEGRATION_GUIDE.md` | How to integrate sensors with your GUI |
| `test_ultrasonic.py` | Test HC-SR04 distance sensor |
| `test_mpu9250.py` | Test MPU9250 fall detection |
| `ultrasonic_sensor.py` | Ultrasonic sensor module with filtering |
| `fall_detector.py` | Fall detection with state machine |
| `requirements_sensors.txt` | Additional Python dependencies |

---

## 🔗 Integration Examples

### Example 1: Add Distance Announcements

```python
# In gui_mobile_detector.py __init__:
from ultrasonic_sensor import UltrasonicSensor

self.ultrasonic = UltrasonicSensor(trig_pin=23, echo_pin=24)

# In your detection loop:
distance_feet = self.ultrasonic.get_distance_feet()
if distance_feet and distance_feet < 5.0:
    message = f"Obstacle at {distance_feet:.1f} feet"
    threading.Thread(target=self.tts.speak, args=(message,), daemon=True).start()
```

### Example 2: Add Fall Detection

```python
# In gui_mobile_detector.py __init__:
from fall_detector import MPU9250, FallDetector, FallMonitor

self.imu = MPU9250(address=0x68)
self.fall_detector = FallDetector(
    self.imu, 
    tts_callback=lambda msg: threading.Thread(
        target=self.tts.speak, args=(msg,), daemon=True
    ).start()
)
self.fall_monitor = FallMonitor(self.fall_detector, sample_rate=50)
self.fall_monitor.add_fall_callback(self._on_fall_detected)
self.fall_monitor.start()

def _on_fall_detected(self):
    """Handle fall event"""
    logger.warning("🚨 Fall detected!")
    # Emit event for app/SMTP
    self._emit_event('fall_detected', {'severity': 'high'})
```

### Example 3: Event Emission for App

```python
def _emit_event(self, event_type, payload):
    """Write event to file for app to read"""
    import json
    event = {
        'timestamp': time.time(),
        'event': event_type,
        'payload': payload
    }
    with open('/tmp/iris_events.jsonl', 'a') as f:
        f.write(json.dumps(event) + '\n')
```

---

## 🎛️ Configuration (.env)

Add these to your `.env` file:

```bash
# Ultrasonic Sensor
ULTRASONIC_ENABLED=true
ULTRASONIC_TRIG_PIN=23
ULTRASONIC_ECHO_PIN=24
ULTRASONIC_ANNOUNCE_THRESHOLD=5.0  # feet

# Fall Detection
FALL_DETECTION_ENABLED=true
FALL_IMPACT_THRESHOLD=2.5  # g
FALL_ROTATION_THRESHOLD=150  # deg/s

# Events
EVENT_FILE=/tmp/iris_events.jsonl
```

---

## 🧪 Testing Checklist

Before using with blind users:

- [ ] **Ultrasonic readings accurate** (±0.1 feet with tape measure)
- [ ] **Distance announcements not too frequent** (only on significant change)
- [ ] **Fall detection tuned** (no false positives, detects real falls)
- [ ] **TTS clear and non-blocking** (doesn't freeze GUI)
- [ ] **Events written correctly** (check `/tmp/iris_events.jsonl`)
- [ ] **App receives SMTP alerts** (test fall event)
- [ ] **Battery life acceptable** (6-8 hours minimum)
- [ ] **Sensors survive power cycle** (unplug/replug works)

---

## 🔧 Common Issues & Fixes

### "pigpio daemon not running"
```bash
# Start daemon manually
sudo pigpiod

# Verify it's running
pgrep pigpiod
```

### "I2C device not found"
```bash
# Enable I2C
sudo raspi-config  # Interface Options → I2C → Enable

# Verify
sudo i2cdetect -y 1
```

### "Ultrasonic always timeout"
- Check voltage divider on ECHO pin (must reduce 5V to 3.3V)
- Verify TRIG and ECHO not swapped
- Add 10µF capacitor between VCC and GND on sensor

### "Fall always detected"
- Decrease `impact_threshold` in FallDetector
- Run calibration: `python test_mpu9250.py --calibrate`
- Keep IMU flat and still during initialization

### "MPU9250 wrong address"
- Try 0x69 instead of 0x68
- Check AD0 pin connection (GND=0x68, VCC=0x69)

---

## 📊 Expected Performance

| Metric | Value |
|--------|-------|
| Ultrasonic range | 0.5 - 13 feet |
| Ultrasonic accuracy | ±0.1 feet |
| Fall detection latency | 1-2 seconds |
| False positive rate | <5% (after tuning) |
| CPU usage (both sensors) | ~10-15% |
| Additional power | ~0.5W |

---

## 🎯 Next Steps

1. **Complete hardware wiring** (see `HARDWARE_SETUP_GUIDE.md`)
2. **Run test scripts** to verify both sensors
3. **Integrate with GUI** (see `SENSOR_INTEGRATION_GUIDE.md`)
4. **Tune thresholds** for your specific user
5. **Set up app/SMTP** notification system
6. **Test in real-world scenarios** with supervised user

---

## 💡 Pro Tips

- **Ultrasonic mounting**: Chest/waist height, pointing forward
- **IMU mounting**: On belt/body, Z-axis up when standing
- **Fall detection**: Start with higher thresholds, decrease gradually
- **Distance announcements**: Use cooldown (3-5 seconds) to avoid spam
- **Power**: Use 25,000mAh USB-C PD power bank for 8+ hours runtime
- **Testing**: Simulate falls with sensor in hand, not on body!

---

## 📞 Support

For issues or questions:
1. Check `HARDWARE_SETUP_GUIDE.md` for wiring
2. Check `SENSOR_INTEGRATION_GUIDE.md` for code
3. Run test scripts to isolate sensor vs integration issues
4. Check logs for detailed error messages

**Your visual assistance system is ready! 🎉**
