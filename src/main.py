import time
import keyboard
import threading
import sys
import os
import random
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
    climb_duration = ctrl.config["delays"]["climb_duration"]
    
    # Patrol boundaries from minimap
    x_min = ctrl.config["patrol"]["minimap_x_min"]
    x_max = ctrl.config["patrol"]["minimap_x_max"]
    y_min = ctrl.config["patrol"]["minimap_y_min"]
    y_max = ctrl.config["patrol"]["minimap_y_max"]
    
    # Track last known player position
    last_player_pos = None
    stuck_counter = 0

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
                time.sleep(1)
                continue

            # 2. State: Minimap Wayfinding
            screen_img = vis.capture_screen()
            minimap_img = vis.extract_minimap(screen_img, ctrl.config["regions"]["minimap"])
            player_pos = vis.find_player_on_minimap(minimap_img)
            
            if player_pos:
                p_x, p_y = player_pos
                
                # Kiểm tra có bị kẹt không (vị trí không thay đổi sau nhiều vòng lặp)
                if last_player_pos:
                    dx = abs(p_x - last_player_pos[0])
                    dy = abs(p_y - last_player_pos[1])
                    if dx < 3 and dy < 3:
                        stuck_counter += 1
                    else:
                        stuck_counter = 0
                
                last_player_pos = (p_x, p_y)
                
                # Nếu bị kẹt quá lâu (> 10 vòng lặp), thử nhảy hoặc đổi hướng
                if stuck_counter > 10:
                    print(f"[Patrol] STUCK detected at ({p_x},{p_y})! Trying to escape...")
                    ctrl.jump()
                    time.sleep(0.3)
                    direction = "left" if direction == "right" else "right"
                    stuck_counter = 0
                    continue
                
                # Logic trục Y: Trèo thang lên nếu nhân vật ở quá thấp, rớt xuống nếu quá cao
                if p_y > y_max:
                    print(f"[Patrol] Player too low (Y:{p_y} > {y_max}). Climbing ladder...")
                    ctrl.climb_ladder(duration=climb_duration)
                    time.sleep(0.5)
                    continue
                elif p_y < y_min:
                    print(f"[Patrol] Player too high (Y:{p_y} < {y_min}). Dropping down...")
                    ctrl.drop_down()
                    time.sleep(0.5)
                    continue
                
                # Logic trục X: Quay đầu khi đụng mép trái/phải
                if direction == "right" and p_x > x_max:
                    print(f"[Patrol] Reached right boundary (X:{p_x}). Turning left.")
                    direction = "left"
                elif direction == "left" and p_x < x_min:
                    print(f"[Patrol] Reached left boundary (X:{p_x}). Turning right.")
                    direction = "right"
                
                print(f"[Patrol] Pos=({p_x},{p_y}) Dir={direction}")
            else:
                print("[Vision] Cannot find player on minimap. Patrolling blind.")
            
            # 3. State: Patrol & Attack
            # Di chuyển theo hướng hiện tại
            if direction == "right":
                ctrl.walk_right(duration=0.5)
            else:
                ctrl.walk_left(duration=0.5)
            
            # Tấn công trong khi di chuyển
            ctrl.attack()
            time.sleep(0.1)
            ctrl.attack()
            
            # Prevent high CPU usage
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Bot terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Bot shutdown complete.")

if __name__ == "__main__":
    main()
