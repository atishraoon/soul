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

#load icon
icon = pygame.image.load("icon.png")  
pygame.display.set_icon(icon)


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
        self.current_daily = 1   
        self.next_daily = self.current_daily + 1

        self.current_popup_id = 0
        self.popup_window = None
        self.in_register = True
        self.home_screen = None
        self.show_home_time = 0
        self.home_screen_active = False


        #load levels
        self.load_level_data()

        #player status
        self.health = 10.0
        self.current_strength = 10.0
        self.current_stamina = 10.0
        self.current_iq = 10.0
        self.purpose_reached = float(self.current_level * 10)
 
   # ------------------------- home screen / kill other -----------------------------

 
    def show_home_screen(self):
        """Show the home screen with greeting"""
        self.home_screen = HomeScreen(self.manager, (self.settings.WIDTH, self.settings.HEIGHT),
         self.username,
         self.current_level,
         self.health,
         self.purpose_reached,
         self.current_strength,
         self.current_stamina,
         self.current_iq, 
        )
        self.show_home_time = time.time()
        self.home_screen_active = True

    def hide_home_screen(self):
        """Hide the home screen and clean up all its UI elements"""
        if self.home_screen:
            # Kill all main elements
            if hasattr(self.home_screen, 'welcome_label'):
                self.home_screen.welcome_label.kill()
            if hasattr(self.home_screen, 'level_label'):
                self.home_screen.level_label.kill()
            if hasattr(self.home_screen, 'line'):
                self.home_screen.line.kill()
            
            # Kill all buttons
            button_names = [
                'daily_button', 'quest_button', 'inventory_button',
                'skill_button', 'help_button', 'purpose_button'
            ]
            for button_name in button_names:
                if hasattr(self.home_screen, button_name):
                    getattr(self.home_screen, button_name).kill()
            
            # Kill status label
            if hasattr(self.home_screen, 'status_label'):
                self.home_screen.status_label.kill()
            
            # Kill all attribute containers and their children
            attributes = ['health', 'strength', 'stamina', 'iq']
            for attr in attributes:
                container_name = f"{attr}_container"
                if hasattr(self.home_screen, container_name):
                    getattr(self.home_screen, container_name).kill()
            
            # Kill progress elements
            if hasattr(self.home_screen, 'progress_label'):
                self.home_screen.progress_label.kill()
            if hasattr(self.home_screen, 'purpose_container'):
                self.home_screen.purpose_container.kill()
            
            # Clear references
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
        self.show_home_screen() 
             

   


    # ---------------------------- load level / daily task --------------------    

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

    #load level     
    def load_level_data(self):
        """Load and display data for the current level"""
        level_data = self.level.get_level_data(self.current_level)
        if level_data:
            self.create_popup_window(
                title=level_data["title"],
                message=level_data["messages"]
            )


    #load daily task     
    def load_daily_data(self):
        """Load and display data for the current level"""
        daily_data = self.level.get_daily_data(self.current_daily)
        if daily_data:
            self.create_alert_popup(
                title=daily_data["title"],
                message=daily_data["messages"]
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
    
           
            # Handle home screen button clicks
            elif event.type == pygame_gui.UI_BUTTON_PRESSED and self.home_screen_active:
                if event.ui_element == self.home_screen.get_daily_button():
                    print('"Daily" button clicked')
                    self.load_daily_data()
                    self.current_daily = self.current_daily+1

                elif event.ui_element == self.home_screen.get_quest_button():
                    print('"Quest" button clicked')
                elif event.ui_element == self.home_screen.get_inventory_button():
                    print('"Inventory" button clicked')
                elif event.ui_element == self.home_screen.get_skill_button():
                    print('"Skill" button clicked')
                elif event.ui_element == self.home_screen.get_help_button():
                    print('"Help" button clicked')          
                elif event.ui_element == self.home_screen.get_purpose_button():
                    print('"Purpose" button clicked')    

                # Handle attribute boost buttons
                elif event.ui_element in self.home_screen.boost_buttons.values():
                    for attr, button in self.home_screen.boost_buttons.items():
                        if event.ui_element == button:
                            print(f'"{attr.capitalize()}" boost button clicked')
                            self.home_screen.boost_attribute(attr)
                                                  

                 
            # Handle popup button events
            if self.popup_window and isinstance(self.popup_window, PopupWindow):
                result = self.popup_window.process_event(event)
                 # Daily task handling
                if self.current_daily > 1:  # Assuming daily tasks start from 1
                    if result == "yes":
                        print('daily task yes button clicked')
                        self.close_popup()
                        
                    elif result == "no":
                        print('daily task no button clicked')
                        self.close_popup()
                        self.health = self.health - 10.00
                        self.hide_home_screen()
                        self.show_home_screen()
                        

                # level handle
                if self.current_level == 1:
                    if result == "yes":
                        self.close_popup()  
                        print('you completed the first level')
                        self.create_register_popup()
                        self.current_level = 2                        
                    elif result == "no":
                        print("fist warning") 

                elif self.current_level == 2:
                    if result == "yes":
                        self.close_popup()  
                        print('level 2 accepted')
                        self.current_level = 3                        
                    elif result == "no":
                        print("fail level 2")


                                     
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