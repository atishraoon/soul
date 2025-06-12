import pygame
import pygame_gui
from ..settings import *
 
class HomeScreen:  
    def __init__(self, manager, screen_dimensions, username, current_level, health , purpose_reached , strength , stamina , iq):
        self.settings = Settings()
        self.manager = manager
        self.screen_width, self.screen_height = screen_dimensions
        self.username = username
        self.current_level = current_level
        self.current_health = health
        self.current_strength = strength
        self.current_stamina = stamina
        self.current_iq = iq  
        self.purpose_reached = purpose_reached 
        self.create_ui()

    def create_ui(self):
        # ------------------------------------- nav bar ------------------------------------------------

        # Top left - Level indicator
        self.level_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (20, 20),  # Positioned top left with some padding
                (100, 30)
            ),
            text=f"Level {self.current_level}",
            manager=self.manager
        )

        # Top right - Welcome message
        self.welcome_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (self.screen_width - 220, 20),  # Positioned top right
                (200, 30)
            ),
            text=f"Welcome, {self.username}!",
            manager=self.manager
        )

        # Horizontal line below the header
        self.line = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (0, 60),  # Positioned below the labels
                (self.screen_width, 1)  # Thin line spanning full width
            ),
            starting_height=0,
            manager=self.manager
        )
        # Set the line color to white
        self.line.background_colour = pygame.Color(255, 255, 255)

        # ----------------------------------------  all buttons ------------------------------------------

        # Calculate button positions (add this above button creation)
        button_width = 150
        button_height = 150
        num_buttons = 5
        total_buttons_width = num_buttons * button_width
        available_space = self.screen_width - total_buttons_width
        button_spacing = available_space // (num_buttons + 1)  # Equal spacing on both sides and between

        # Create buttons
        button_data = [
            ("Daily", "daily_button"),
            ("Quest", "quest_button"),
            ("Inventory", "inventory_button"),
            ("Skill", "skill_button"),
            ("Help", "help_button")
        ]

        for i, (text, attr_name) in enumerate(button_data):
            x_pos = button_spacing + i * (button_width + button_spacing)
            setattr(self, attr_name, pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (x_pos, 100), 
                    (button_width, button_height)
                ),
                text=text,
                manager=self.manager
            ))

        # --------------------------------- profile status --------------------------------------------------

        self.status_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, 100 + button_height + 20 + 20),  
                (self.screen_width, 30)  # Full width
            ),
            text=f"PLAYER / {self.username} / STATUS /",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(
                class_id="@status_labels",
                object_id="#player_status"
            )
        )

        self.boost_buttons = {}
        self.button_height = 30
 
        attributes = ["HEALTH", "STRENGTH", "STAMINA", "IQ"]
        margin_left_right = 15
        current_y = 100 + button_height + 20 + 20 + 40

        
        self.attribute_values = {
            "health": float(self.current_health),  
            "strength": float(self.current_strength), 
            "stamina": float(self.current_stamina), 
            "iq": float(self.current_iq),  
            "purpose": float(self.purpose_reached)
        }

        for attr in attributes:
            # Create container panel with side margins
            container = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(
                    (margin_left_right, current_y),  # Add left margin
                    (self.screen_width - 2 * margin_left_right, 40)  # Reduce width by both margins
                ),
                manager=self.manager
            )
            setattr(self, f"{attr.lower()}_container", container)

            # Attribute Label (position relative to container)
            label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (20, 5),
                    (100, 30)
                ),
                text=f"{attr}:",
                manager=self.manager,
                container=container
            )
            setattr(self, f"{attr.lower()}_label", label)

            # Progress Bar (adjust width to account for margins)
            progress_bar = pygame_gui.elements.UIProgressBar(
                relative_rect=pygame.Rect(
                    (130, 10),
                    (self.screen_width - 300 - 2 * margin_left_right, 20)
                ),
                manager=self.manager,
                container=container
            )
            setattr(self, f"{attr.lower()}_bar", progress_bar)
            
            # Set initial progress from our dictionary
            progress_bar.set_current_progress(self.attribute_values[attr.lower()])

            # Boost Button (position relative to container)
            boost_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (container.rect.width - 150, 5),  # Position from right edge of container
                    (120, 30)
                ),
                text="BOOST",
                manager=self.manager,
                container=container
            )
            setattr(self, f"boost_{attr.lower()}_button", boost_button)
            self.boost_buttons[attr.lower()] = boost_button

            current_y += 50

        # ------------------------------------- progress -----------------------------------------------
        self.progress_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, current_y + 10),  # Position below last attribute bar with 10px margin
                (self.screen_width, 30)
            ),
            text=f"PROGRESS / STATUS / PLAYER / {self.username}",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(
                class_id="@progress_labels",
                object_id="#player_progress"
            )
        )

        # -------------------------------------- progress toward your goal --------------------------------

        self.purpose_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (10, current_y + 60),  # 10px left margin
                (self.screen_width - 20, 40)  # 10px right margin (total 20px reduction)
            ),
            manager=self.manager
        )

        # Purpose Label - fixed container reference
        self.purpose_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (10, 5),  # 10px from left edge of container
                (150, 30)  # Wider to fit "PURPOSE REACHED"
            ),
            text="PURPOSE REACHED:",
            manager=self.manager,
            container=self.purpose_container
        )

        # Purpose Progress Bar - adjusted width for container margins
        self.purpose_bar = pygame_gui.elements.UIProgressBar(
            relative_rect=pygame.Rect(
                (170, 10),  # 170 = label width (150) + label margin (10) + spacing (10)
                (self.purpose_container.rect.width - 310, 20)  # Accounts for both margins
            ),
            manager=self.manager,
            container=self.purpose_container
        )

        # Set the initial purpose progress value
        self.purpose_bar.set_current_progress(self.attribute_values["purpose"])

        # Purpose Button - fixed container reference and positioning
        self.purpose_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.purpose_container.rect.width - 130, 5),  # 130 = button width (120) + right margin (10)
                (120, 30)
            ),
            text="Goal",
            manager=self.manager,
            container=self.purpose_container
)

    # ---------------------------------- return buttons as reference -------------------------------------
    def get_purpose_button(self):
        return self.purpose_button

    def get_daily_button(self):
        """Return the help button reference."""
        return self.daily_button

    def get_quest_button(self):
        """Return the greet button reference."""
        return self.quest_button

    def get_inventory_button(self):
        return self.inventory_button

    def get_skill_button(self):
        return self.skill_button

    def get_help_button(self):
        return self.help_button

    def get_health_button(self):
        return self.boost_buttons["health"]

    def get_strength_button(self):
        return self.boost_buttons["strength"]

    def get_stamina_button(self):
        return self.boost_buttons["stamina"]

    def get_iq_button(self):
        return self.boost_buttons["iq"]

    # ----------------------------------------------- boost attributes -------------------------------
    def boost_attribute(self, attribute_name):
        """Increase the specified attribute by 10 points (max 100)"""
        if attribute_name in self.attribute_values:
            new_value = min(100.0, self.attribute_values[attribute_name] + 10.0)
            self.attribute_values[attribute_name] = new_value
            getattr(self, f"{attribute_name}_bar").set_current_progress(new_value)
            
            # Update the label to show current/max (e.g. "60.0/100.0")
            label = getattr(self, f"{attribute_name}_label")
            # label.set_text(f"{attribute_name}: {new_value:.1f}/100.0")