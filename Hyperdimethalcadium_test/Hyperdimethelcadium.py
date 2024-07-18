
import tkinter as tk
from tkinter import messagebox
import pygame
import random

def show_warning():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    response = messagebox.askyesno(
        title="User Account Control",
        message="Do you want to allow this app to make changes to your device?\n\n"
                "Publisher: Unknown\n"
                "File origin: Unknown\n",
        icon="warning"
    )
    if response:
        root.destroy()
        # Proceed with Pygame screen melter effect
        proceed_with_action()
    else:
        root.destroy()

def proceed_with_action():
    pygame.init()

    # Get screen dimensions
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h

    # Set the dimensions of the window to match the screen size
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Screen Melter")

    # Fill the screen with random colors
    for x in range(screen_width):
        for y in range(screen_height):
            screen.set_at((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    pygame.display.flip()

    # Function to melt the screen
    def melt_screen():
        melting = True
        while melting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    melting = False

            for x in range(screen_width):
                for y in range(screen_height - 1, 0, -1):
                    screen.set_at((x, y), screen.get_at((x, y - 1)))

            pygame.display.flip()
            pygame.time.delay(10)

        pygame.quit()  # Properly quit Pygame

    melt_screen()

if __name__ == "__main__":
    show_warning()
