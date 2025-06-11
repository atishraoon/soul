import pygame  
import pygame_gui
from ..settings import Settings 

class AlertPopup:  
    def __init__(self, manager, position, size, title, message, allow_close=True):
        self.settings = Settings()
        """
        Creates a simple alert pop-up window with a message and optional close button.
        """
        try:
            # Create the window
            self.window = pygame_gui.elements.UIWindow(
                rect=pygame.Rect(position, size),
                manager=manager,
                window_display_title=title,
                resizable=False,
                object_id="#alert_popup_window"
            ) 

            # Configure close button behavior
            self.window.set_blocking(True)  # This makes the window modal
            if hasattr(self.window, 'close_window_button'):
                if allow_close:
                    self.window.close_window_button.show()
                else:
                    self.window.close_window_button.hide()

            # Calculate text box size based on whether we have a close button
            text_box_height = size[1] - 40 if allow_close else size[1] - 120

            # Message text box - takes up most of the window space
            self.text_box = pygame_gui.elements.UITextBox(
                html_text=f"<font color='{self.settings.BUTTON_TEXT_COLOR}'>{message}</font>",
                relative_rect=pygame.Rect((10, 30), (size[0] - 20, text_box_height)),
                manager=manager,
                container=self.window,
                object_id="#alert_popup_text"
            )

        except Exception as e:
            print(f"Error creating alert popup window: {e}")
            raise

    def kill(self):
        """Destroys the pop-up window and its elements."""
        try:
            self.window.kill()
        except AttributeError:
            pass  # Window was already destroyed