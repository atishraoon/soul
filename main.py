import sys
import time 
import os
import pygame
import pygame_gui

#settings , packages , dll files 
from core.settings import Settings
from core.level import LevelManager
 
#ui components
from core.ui_components.alertpopup import AlertPopup 
from core.ui_components.popupwindow import PopupWindow 
from core.ui_components.register import Register 
from core.ui_components.home import HomeScreen  


#load level file
from pathlib import Path
core_dir = Path(__file__).parent / "core"
display_path = core_dir / "level.json"

class PygameWindow:
    def __init__(self):
        pygame.init()
        
        self.settings = Settings()
        self.level = LevelManager(display_path)

        self.screen = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption(self.settings.TITLE)
        
        # Initialize UI
        self.manager = pygame_gui.UIManager((self.settings.WIDTH, self.settings.HEIGHT))
        
        # Initialize popup-related attributes
        # Game state
        self.username = ""
        self.running = True
        self.attempt_count = 0 
        self.current_level = 1  
        self.next_level = self.current_level + 1
        self.current_popup_id = 0
        self.popup_window = None
        self.in_register = True
        self.home_screen = None
        self.show_home_time = 0
        self.home_screen_active = False


        #load levels
        self.load_level_data()

 

   # ------------------------- home screen / kill other -----------------------------


    def show_home_screen(self, username):
        """Show the home screen with greeting"""
        self.home_screen = HomeScreen(self.manager, (self.settings.WIDTH, self.settings.HEIGHT), username , self.current_level)
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



   # ---------------------------- register ui / handel register -------------------     

    def create_register_popup(self):
        self.register_ui = Register(
            manager=self.manager,
            position=(self.settings.WIDTH // 2 - self.settings.POPUP_WIDTH // 2, self.settings.HEIGHT // 2 - self.settings.POPUP_HEIGHT // 2),
            size=(self.settings.POPUP_WIDTH, self.settings.POPUP_HEIGHT),
            on_submit=self.handle_register_submission
         )
        self.in_register = True


    def handle_register_submission(self, purpose, username, password):
        """Handle register form submission"""
        print(f"Registration submitted:")
        print(f"Purpose: {purpose}")
        print(f"Username: {username}")
        print(f"Password: {password}")  # For debugging (remove in production)
        
        # Store the values
        self.username = username
        self.purpose = purpose
        self.password = password  # Note: Storing passwords in plain text is insecure
        
        # Debug output to verify storage
        print(f"Stored username: {self.username}")
        
        if hasattr(self, 'register_ui'):
            self.register_ui.kill()
            del self.register_ui
        
        self.in_register = False
        
        # Load next content after registration
        self.show_home_screen(self.username)
             

   


    # ----------------------------------- load level ----------------------------------    

    def create_popup_window(self, title, message):
        """Create a new popup window"""
        if self.popup_window:
            self.close_popup()
            
        self.popup_window = PopupWindow(
            manager=self.manager,
            position=(self.settings.WIDTH // 2 - self.settings.POPUP_WIDTH // 2, 
                     self.settings.HEIGHT // 2 - self.settings.POPUP_HEIGHT // 2),
            size=(self.settings.POPUP_WIDTH, self.settings.POPUP_HEIGHT),    
            title=title,
            message=message
        )
        self.current_popup_id += 1

    def load_level_data(self):
        """Load and display data for the current level"""
        level_data = self.level.get_level_data(self.current_level)
        if level_data:
            self.create_popup_window(
                title=level_data["title"],
                message=level_data["messages"]
            )


            
    # ------------------------------ on quit ------------------------------------------
    
    def create_alert_popup(self, title, message):
        """Create a new alert popup (no buttons)"""
        if self.popup_window:
            self.close_popup()
            
        self.popup_window = AlertPopup(
            manager=self.manager,
            position=(self.settings.WIDTH // 2 - self.settings.POPUP_WIDTH // 2, 
                     self.settings.HEIGHT // 2 - self.settings.POPUP_HEIGHT // 2),
            size=(self.settings.POPUP_WIDTH, self.settings.POPUP_HEIGHT),
            title=title,
            message=message
        )
        self.current_popup_id += 1 

    def close_popup(self):
        """Close the current popup window"""
        if self.popup_window:
            self.popup_window.kill()
            self.popup_window = None



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

    # ---------------------------------------- all events --------------------------
   
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.show_quit_warning()
          

            #main key binds to exit the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.running = False
            
            # for popup window close   
            elif event.type == pygame_gui.UI_WINDOW_CLOSE:
                if self.popup_window and event.ui_element == self.popup_window.window:
                    self.close_popup()
                    if self.current_level == 1:
                        self.load_level_data()

                if hasattr(self, 'register_ui') and hasattr(event, 'ui_element') and event.ui_element == self.register_ui.window:
                    self.current_level = 1
                    self.load_level_data()
                    self.create_register_popup()
                    self.in_register = False
                    del self.register_ui 


            # handel register ui popup event
            if hasattr(self, 'register_ui'):
                self.register_ui.handle_events(event)

            # home screen window
            elif self.home_screen_active:
                if event.type == pygame.USEREVENT:
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        
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
                            self.home_screen.boost_attribute("health")
                            print(f"Health boosted to {self.home_screen.attribute_values['health']}")
                        elif event.ui_element == self.home_screen.boost_strength_button:
                            self.home_screen.boost_attribute("strength")
                        elif event.ui_element == self.home_screen.boost_stamina_button:
                            self.home_screen.boost_attribute("stamina")
                        elif event.ui_element == self.home_screen.boost_iq_button:
                            self.home_screen.boost_attribute("iq")
                        elif event.ui_element == self.home_screen.purpose_button:
                            print(f"purpose-level button pressed by {self.home_screen.username}")



             
            # Handle popup button events
            if self.popup_window and isinstance(self.popup_window, PopupWindow):
                result = self.popup_window.process_event(event)
                if self.current_level == 1:
                    if result == "yes":
                        self.close_popup()  
                        print('you completed the first level')
                        self.create_register_popup()
                        self.current_level = 2                        
                    elif result == "no":
                        print("you have to phase consequences for not compeleting level 1")

            # Always pass events to the UI manager
            self.manager.process_events(event)




    # ------------------------------- update instance --------------------------------
    
    def update(self):
        
        """Update game state and graphics"""
        self.screen.fill(self.settings.BACKGROUND_COLOR)
        self.manager.update(pygame.time.Clock().tick(self.settings.FPS) / 1000.0)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()

    # -------------------------------- main running ----------------------------------
    def run(self):
        
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
        pygame.quit()

if __name__ == "__main__":
    game = PygameWindow()
    game.run()