import pygame
import pygame_gui


class Register:
    def __init__(self, manager, position, size, on_submit ):
        self.manager = manager
        self.on_submit = on_submit
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(position, size),
            manager=manager,
            window_display_title="Register"
        )

        if hasattr(self.window, 'close_window_button'):
                self.window.set_blocking(False)
        
        # Create form elements
        self.purpose_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 50, 300, 30),
            manager=manager,
            container=self.window,
            placeholder_text="Purpose"
        )
        
        self.username_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 100, 300, 30),
            manager=manager,
            container=self.window,
            placeholder_text="Username"
        )
        
        self.password_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 150, 300, 30),
            manager=manager,
            container=self.window,
            placeholder_text="Password"
        )
        self.password_field.set_text_hidden(True)
        
        self.submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(150, 200, 100, 40),
            text="Submit",
            manager=manager,
            container=self.window
        )
    
    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.submit_button:
                    purpose = self.purpose_field.get_text()
                    username = self.username_field.get_text()
                    password = self.password_field.get_text()
                    if purpose and username and password: 
                        if callable(self.on_submit):  
                            self.on_submit(purpose, username, password) 

                            
    # def handle_events(self, event):
    #     if event.type == pygame.USEREVENT:
    #         if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
    #             if event.ui_element == self.submit_button:
    #                 purpose = self.purpose_field.get_text()
    #                 username = self.username_field.get_text()
    #                 password = self.password_field.get_text()
    #                 self.on_submit(purpose, username, password)
    
    def kill(self):
        self.window.kill()