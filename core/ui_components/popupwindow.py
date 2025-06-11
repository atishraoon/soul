import pygame
import pygame_gui
from ..settings import Settings

class PopupWindow:
    def __init__(self, manager, position, size, title, message):
        self.settings = Settings()
        """
        Creates a pop-up window with a message and Yes/No buttons.
        """
        try:
            # Create the window
            self.window = pygame_gui.elements.UIWindow(
                rect=pygame.Rect(position, size),
                manager=manager,
                window_display_title=title,
                resizable=False,
                object_id="#popup_window" 
            )

            # Hide the close button
            if hasattr(self.window, 'close_window_button'):
                self.window.close_window_button.hide()
                self.window.close_window_button.disable()

            self.window.set_blocking(True)

            # Message text box
            self.text_box = pygame_gui.elements.UITextBox(
                html_text=f"<font color='{self.settings.BUTTON_TEXT_COLOR}'>{message}</font>",
                relative_rect=pygame.Rect((10, 30), (size[0] - 20, size[1] - 120)),
                manager=manager,
                container=self.window,
                object_id="#popup_text"
            )

            # Calculate button positions
            button_y = size[1] - 80
            button_width = self.settings.UI_BUTTON_WIDTH
            button_height = self.settings.UI_BUTTON_HEIGHT
            button_spacing = self.settings.UI_BUTTON_SPACING
            
            # Yes button
            self.yes_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((size[0] // 2) - (button_width + button_spacing // 2), button_y),
                    (button_width, button_height)
                ),
                text='Yes',
                manager=manager,
                container=self.window,
                object_id="#yes_button"
            )
            
            # No button
            self.no_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    ((size[0] // 2) + (button_spacing // 2), button_y),
                    (button_width, button_height)
                ),
                text='No',
                manager=manager,
                container=self.window,
                object_id="#no_button"
            )

        except Exception as e:
            print(f"Error creating popup window: {e}")
            raise

    def process_event(self, event):
        """Handle button click events"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.yes_button:
                print("yes")
                return "yes"
            elif event.ui_element == self.no_button:
                print("no")
                return "no"
        return None

    def kill(self):
        """Destroys the pop-up window and its elements."""
        try:
            self.window.kill()
        except AttributeError:
            pass  # Window was already destroyed