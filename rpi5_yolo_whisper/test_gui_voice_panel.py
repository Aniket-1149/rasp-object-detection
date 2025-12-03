"""
Simple GUI test to verify voice status panel displays
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

def create_test_gui():
    """Create a simple GUI with voice status panel"""
    root = tk.Tk()
    root.title("Voice Status Panel Test")
    root.geometry("600x400")
    root.configure(bg='#1e1e1e')
    
    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')
    
    bg_dark = '#1e1e1e'
    bg_medium = '#2d2d2d'
    fg_light = '#ffffff'
    
    style.configure('Dark.TFrame', background=bg_dark)
    style.configure('Medium.TFrame', background=bg_medium)
    style.configure('Info.TLabel', background=bg_medium, foreground=fg_light, 
                   font=('Arial', 11))
    
    # Main frame
    main_frame = ttk.Frame(root, style='Dark.TFrame', padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title = ttk.Label(
        main_frame,
        text="Voice Status Panel Test",
        font=('Arial', 16, 'bold'),
        background=bg_dark,
        foreground=fg_light
    )
    title.pack(pady=10)
    
    # Voice Status Panel
    voice_status_frame = ttk.LabelFrame(
        main_frame,
        text="🎤 Voice Status",
        padding="10",
        style='Medium.TFrame'
    )
    voice_status_frame.pack(fill=tk.X, pady=10)
    
    voice_status_label = ttk.Label(
        voice_status_frame,
        text="Voice control is OFF",
        style='Info.TLabel',
        font=('Arial', 12, 'bold'),
        foreground='#8a8a8a'
    )
    voice_status_label.pack(fill=tk.X, pady=5)
    
    # Control buttons
    button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
    button_frame.pack(fill=tk.X, pady=10)
    
    def start_simulation():
        """Simulate voice states"""
        states = [
            ("🎤 Listening for 'IRIS'...", '#00ff00'),
            ("✅ IRIS detected! Say your command...", '#ffff00'),
            ("🎙️ Recording command...", '#ff9900'),
            ("⚙️ Processing speech...", '#0099ff'),
            ("✅ Heard: 'detect'", '#00ff00'),
            ("Voice control is OFF", '#8a8a8a')
        ]
        
        def update_states():
            for text, color in states:
                voice_status_label.config(text=text, foreground=color)
                time.sleep(2)
        
        threading.Thread(target=update_states, daemon=True).start()
    
    start_btn = tk.Button(
        button_frame,
        text="▶ Start Simulation",
        command=start_simulation,
        bg='#107c10',
        fg='white',
        font=('Arial', 11, 'bold'),
        padx=20,
        pady=10
    )
    start_btn.pack(pady=5)
    
    quit_btn = tk.Button(
        button_frame,
        text="❌ Quit",
        command=root.quit,
        bg='#d13438',
        fg='white',
        font=('Arial', 11, 'bold'),
        padx=20,
        pady=10
    )
    quit_btn.pack(pady=5)
    
    # Instructions
    instructions = ttk.Label(
        main_frame,
        text="Click 'Start Simulation' to see voice status changes",
        style='Info.TLabel',
        foreground='#8a8a8a'
    )
    instructions.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("="*60)
    print("Voice Status Panel Test")
    print("="*60)
    print("This will open a GUI window to test the voice status display")
    print("Click 'Start Simulation' to see the voice states change")
    print("="*60)
    
    try:
        create_test_gui()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
