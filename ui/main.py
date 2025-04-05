import sys
import os

# Get the root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIR = os.path.join(ROOT_DIR, 'core')
sys.path.append(CORE_DIR)

LEVEL_FILE = os.path.join(ROOT_DIR, 'core', 'level.json')


import pygame
import pygame_gui
import json
from settings import *
from popupwindow import PopupWindow, AlertPopup
from level import LevelManager
from first import RegisterUI
from home import HomeScreen
import time


class PygameWindow:
    def __init__(self):
        pygame.init()
        self.levelfile = LEVEL_FILE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Game state
        self.username = ""
        self.running = True
        self.attempt_count = 0 
        self.current_level = 1  
        self.next_level = self.current_level + 1
        self.current_popup_id = 0
        self.popup_window = None
        self.in_register = False
        self.home_screen = None
        self.show_home_time = 0
        self.home_screen_active = False  # Track if home screen is active
        
        # Initialize UI
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        
        # Level management
        self.level_manager = LevelManager(self.levelfile)
        
        # Start with the first level
        self.load_level_data()

    # --------------------------------------- home page --------------------------------------------------
    def show_home_screen(self, username):
        """Show the home screen with greeting"""
        self.home_screen = HomeScreen(self.manager, (WIDTH, HEIGHT), username , self.current_level)
        self.show_home_time = time.time()
        self.home_screen_active = True

    def hide_home_screen(self):
        """Hide the home screen"""
        if self.home_screen:
            self.home_screen.welcome_label.kill()
            self.home_screen.home_label.kill()
            self.home_screen.greet_button.kill()
            self.home_screen = None
            self.home_screen_active = False

    # ----------------------------------------- register --------------------------------------
    def handle_registration_submit(self, purpose, username, password):
        """Handle registration form submission"""
        print(f"Registration submitted - Purpose: {purpose}, Username: {username}")
        self.username = username
        self.register_ui.kill()
        self.in_register = False
        self.show_home_screen(username)

    # ------------------------------------------------ popup / alert -----------------------------------------
    def create_popup_window(self, title, message):
        """Create a new popup window"""
        if self.popup_window:
            self.close_popup()
            
        self.popup_window = PopupWindow(
            manager=self.manager,
            position=(WIDTH // 2 - POPUP_WIDTH // 2, 
                     HEIGHT // 2 - POPUP_HEIGHT // 2),
            size=(POPUP_WIDTH, POPUP_HEIGHT),    
            title=title,
            message=message
        )
        self.current_popup_id += 1

    def create_alert_popup(self, title, message):
        """Create a new alert popup (no buttons)"""
        if self.popup_window:
            self.close_popup()
            
        self.popup_window = AlertPopup(
            manager=self.manager,
            position=(WIDTH // 2 - POPUP_WIDTH // 2, 
                     HEIGHT // 2 - POPUP_HEIGHT // 2),
            size=(POPUP_WIDTH, POPUP_HEIGHT),
            title=title,
            message=message
        )
        self.current_popup_id += 1 

    def close_popup(self):
        """Close the current popup window"""
        if self.popup_window:
            self.popup_window.kill()
            self.popup_window = None

    # ------------------------------------------------------ load json file -------------------------
    def load_level_data(self):
        """Load and display data for the current level"""
        level_data = self.level_manager.get_level_data(self.current_level)
        if level_data:
            self.create_popup_window(
                title=level_data["title"],
                message=level_data["messages"]
            )
    
    # ------------------------------------------ on quit ------------------------------------------
    def show_quit_warning(self):
        """Show the quit warning using AlertPopup with close button"""
        self.create_alert_popup(
            title="Warning! Attempt {}".format(self.attempt_count),
            message="You are not allowed to exit\n\n"
                    "You must complete the game\n\n"
                    "The system will exit automatically\n"
                    "without infecting your device"
        )
        self.attempt_count += 1 
        self.current_popup_id = 0

    # ------------------------------------------------- all events --------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.show_quit_warning()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.running = False
            
            # Process events for both manager and registration UI if active
            self.manager.process_events(event)
            if self.in_register:
                self.register_ui.handle_events(event)
            elif self.home_screen_active:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        
                        if event.ui_element == self.home_screen.daily_button:
                            print(f"daily button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.quest_button:
                            print(f"quest button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.inventory_button:
                            print(f"inventory button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.skill_button:
                            print(f"skill button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.help_button:
                            print(f"help button pressed by {self.home_screen.username}")


                        elif event.ui_element == self.home_screen.boost_health_button:
                            print(f"boost_health button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.boost_strength_button:
                            print(f"boost_strength button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.boost_stamina_button:
                            print(f"boost_stamina button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.boost_iq_button:
                            print(f"boost_iq-level button pressed by {self.home_screen.username}")
                        elif event.ui_element == self.home_screen.purpose_button:
                            print(f"purpose-level button pressed by {self.home_screen.username}")
                       
 
                        
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.popup_window and hasattr(self.popup_window, 'yes_button'):
                        self.handle_popup_buttons(event)
                
                # Handle window close event
                elif event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                    if self.popup_window and event.ui_element == self.popup_window.window:
                        self.close_popup()
                        if not self.username:  
                            self.__init__()  
                            self.load_level_data()

    # ----------------------------------------- handle pop events -------------------------
    def handle_popup_buttons(self, event):
        """Handle popup button interactions (only for popups with buttons)"""
        if event.ui_element == self.popup_window.yes_button:
            print(f"Yes clicked - Current popup ID: {self.current_popup_id}")
            if self.current_level == 0:  # Quit warning
                self.running = False
            elif self.current_level == 1:  # First level
                self.close_popup()
                # Create and show registration window
                self.register_ui = RegisterUI(
                    manager=self.manager,
                    position=(WIDTH // 2 - POPUP_WIDTH // 2, HEIGHT // 2 - POPUP_HEIGHT // 2),
                    size=(POPUP_WIDTH, POPUP_HEIGHT),
                    on_submit=self.handle_registration_submit
                )
                self.in_register = True
        
        elif event.ui_element == self.popup_window.no_button:
            print(f"No clicked - Current popup ID: {self.current_popup_id}")
            if self.current_level == 0:  
                # Check if we have a username (user is registered)
                if hasattr(self, 'username') and self.username:  # If username exists
                    self.close_popup()
                    self.show_home_screen(self.username)  # Go to home page
                else:
                    # Do nothing - popup stays open
                    pass
            elif self.current_level == 1:
                # Do nothing - popup stays open
                pass
            else:
                self.close_popup()

    # ------------------------------------------- update instance -----------------------------------
    def update(self):
        """Update game state and graphics"""
        self.screen.fill(BACKGROUND_COLOR)
        self.manager.update(pygame.time.Clock().tick(60) / 1000.0)
        
               
        self.manager.draw_ui(self.screen)
        pygame.display.flip()

    # ------------------------------------------ main running ------------------------------------------
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
        pygame.quit()

if __name__ == "__main__":
    game = PygameWindow()
    game.run()