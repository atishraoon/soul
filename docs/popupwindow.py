import pygame
import pygame_gui
from settings import *

class PopupWindow:
    def __init__(self, manager, position, size, title, message):
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
                html_text=f"<font color='{BUTTON_TEXT_COLOR}'>{message}</font>",
                relative_rect=pygame.Rect((10, 30), (size[0] - 20, size[1] - 120)),
                manager=manager,
                container=self.window,
                object_id="#popup_text"
            )

            # Calculate button positions
            button_y = size[1] - 80
            button_width = UI_BUTTON_WIDTH
            button_height = UI_BUTTON_HEIGHT
            button_spacing = UI_BUTTON_SPACING
            
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

    def kill(self):
        """Destroys the pop-up window and its elements."""
        try:
            self.window.kill()
        except AttributeError:
            pass  # Window was already destroyed





# ---------------------------------- alert popup ------------------------------------

class AlertPopup:
    def __init__(self, manager, position, size, title, message):
        """
        Creates a simple alert pop-up window with a message and close button.
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

            # Keep the close button enabled
            self.window.set_blocking(True)

            # Message text box - takes up most of the window space
            self.text_box = pygame_gui.elements.UITextBox(
                html_text=f"<font color='{BUTTON_TEXT_COLOR}'>{message}</font>",
                relative_rect=pygame.Rect((10, 30), (size[0] - 20, size[1] - 120)),
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
    def __init__(self, manager, position, size, title, message):
        """
        Creates a simple alert pop-up window with just a message (no buttons).
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

            # Hide the close button
            if hasattr(self.window, 'close_window_button'):
                self.window.set_blocking(False)

            # Message text box - takes up most of the window space
            self.text_box = pygame_gui.elements.UITextBox(
                html_text=f"<font color='{BUTTON_TEXT_COLOR}'>{message}</font>",
                relative_rect=pygame.Rect((10, 30), (size[0] - 20, size[1] - 40)),
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