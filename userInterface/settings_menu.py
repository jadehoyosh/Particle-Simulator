import pygame
import json

class SettingsMenu:
    def __init__(self, screen):
        self.resolutions = [(800, 600), (1024, 768), (1920, 1080)]
        self.selected_resolution = self.load_settings()
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                return tuple(settings.get("resolution", self.resolutions[0]))
        except FileNotFoundError:
            return self.resolutions[0]

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump({"resolution": self.selected_resolution}, f)
        
    def display_menu(self):
        self.screen.fill(self.BLACK)

        # Calculate the center of the current screen width for dynamic positioning
        screen_center_x = self.screen.get_width() // 2

        # Display each resolution option
        for idx, resolution in enumerate(self.resolutions):
            text = self.font.render(f"{resolution[0]}x{resolution[1]}", True, self.WHITE)
            text_rect = text.get_rect(center=(screen_center_x, 150 + idx * 50))
            self.screen.blit(text, text_rect)

            mouse_pos = pygame.mouse.get_pos()
            if text_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.selected_resolution = resolution
                self.screen = pygame.display.set_mode(self.selected_resolution, pygame.RESIZABLE)
                self.save_settings()
        
        # Display instruction text
        instruction_text = self.font.render("Press ENTER to continue to the simulation", True, self.WHITE)
        instruction_text_rect = instruction_text.get_rect(center=(screen_center_x, self.screen.get_height() - 50))
        self.screen.blit(instruction_text, instruction_text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False  # Exit the program entirely
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Press Enter to confirm settings
                        return True  # Signal to start the simulation
            
            self.display_menu()
            pygame.display.flip()
