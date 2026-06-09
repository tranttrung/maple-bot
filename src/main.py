import time
import keyboard
import threading
import sys
import os
from controller import Controller
from vision import Vision

# Global flag for the kill switch
running = False

def emergency_stop():
    global running
    print("\n[!] EMERGENCY STOP TRIGGERED. Stopping the bot...")
    running = False

def start_bot():
    global running
    print("\n[*] Starting the bot...")
    running = True

def get_config_path():
    # If running as a PyInstaller executable
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        return os.path.join(base_dir, 'config.json')
    else:
        # If running from source code
        return "src/config.json"

def main():
    global running
    
    # Initialize modules
    config_path = get_config_path()
    try:
        ctrl = Controller(config_path)
    except FileNotFoundError:
        print(f"[!] Error: Could not find config file at {config_path}")
        print("Make sure config.json is in the correct folder.")
        time.sleep(5)
        return

    vis = Vision()
    
    print("========================================")
    print("MapleStory Auto Patrol Bot Initialized")
    print("Press 'F10' to START the bot.")
    print("Press 'F12' to STOP the bot (Kill Switch).")
    print("========================================\n")

    # Set up hotkeys
    keyboard.add_hotkey('f12', emergency_stop)
    keyboard.add_hotkey('f10', start_bot)
    
    # Variables for logic state
    direction = "right"
    last_buff_time = 0
    buff_cooldown = ctrl.config["delays"]["buff_cooldown"]
    walk_time = ctrl.config["patrol"]["walk_time_before_turn"]

    try:
        while True:
            # Wait until user presses F10 to start
            if not running:
                time.sleep(0.1)
                continue
            
            # 1. State: Buffing
            current_time = time.time()
            if current_time - last_buff_time > buff_cooldown:
                print("[State] Auto Buffing")
                ctrl.buff_1()
                last_buff_time = current_time
                time.sleep(1) # wait for animation
                continue

            # 2. State: Vision / Health Check
            # In a full implementation, you would capture screen, check HP bar here
            # and call ctrl.potion_hp() if needed.
            # screen_img = vis.capture_screen()
            # if is_hp_low(screen_img): ctrl.potion_hp()
            
            # 3. State: Patrol & Attack
            print(f"[State] Patrolling {direction} and Attacking")
            
            # Walk a bit
            if direction == "right":
                ctrl.walk_right(duration=0.5)
            else:
                ctrl.walk_left(duration=0.5)
            
            # Attack a few times
            ctrl.attack()
            time.sleep(0.1)
            ctrl.attack()
            
            # Very basic patrol logic without vision (since minimap coords need actual game to test)
            # Switch direction occasionally
            if random.random() < 0.2: # 20% chance to turn around after each attack cycle
                direction = "left" if direction == "right" else "right"
                print(f"[State] Turning around to {direction}")
            
            # Prevent high CPU usage
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Bot terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Bot shutdown complete.")

if __name__ == "__main__":
    # We need random here for the basic patrol logic demo
    import random
    main()
