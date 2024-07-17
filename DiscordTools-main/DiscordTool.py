from dhooks import Webhook
import pygame
import os
import pyttsx3

# Get the webhook URL from the user
WEBHOOK_URL = input("Enter the Webhook URL: ")
webhook = Webhook(WEBHOOK_URL)

# Display the options to the user
print("1. Send message")
print("2. Spam server")
print("3. FakeBot")

# Get the user's choice
num = input("Enter your choice: ")

# Handle the user's choice
if num == '1':
    # Option 1: Send a single message
    msg = input("Enter your message: ")
    webhook.send(msg)
elif num == '2':
    # Option 2: Spam the server
    try:
        msg = input("Enter your message: ")
        spam_count = int(input("Enter the number of times to send the message: "))
        for _ in range(spam_count):
            webhook.send(msg)
        print(f"Sent '{msg}' {spam_count} times.")
    except KeyboardInterrupt:
        print("\nSpamming stopped.")
    except ValueError:
        print("Invalid number of times entered. Please enter an integer.")
elif num == '3':
    # Option 3: Run the FakeBot app
    class FakeBotApp:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("FakeBot")
            self.clock = pygame.time.Clock()  # Clock object to control frame rate
            self.is_running = True

            # Load FakeBot images
            self.fakebot_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'fakebot.png'))
            self.fakebot_rect = self.fakebot_image.get_rect()
            self.fakebot_rect.center = (400, 300)  # Initial position

            self.webhook_url = WEBHOOK_URL  # Replace with your Discord webhook URL
            self.hook = Webhook(self.webhook_url)

            # Initialize pyttsx3 for text-to-speech
            self.engine = pyttsx3.init()

            # Input box parameters
            self.input_box = pygame.Rect(100, 100, 600, 50)
            self.font = pygame.font.Font(None, 32)
            self.text = ''

        def draw_animation(self):
            self.screen.fill((255, 255, 255))  # Fill background with white
            pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)  # Draw input box
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
            self.screen.blit(self.fakebot_image, self.fakebot_rect)  # Draw FakeBot image
            pygame.display.flip()

        def send_discord_message(self, message):
            try:
                self.hook.send(message)
                print(f"Message sent to Discord: {message}")
                self.say_message_sent()
            except Exception as e:
                print(f"Error sending message to Discord: {e}")

        def say_message_sent(self):
            text_to_speak = "Message sent!"
            self.engine.say(text_to_speak)
            self.engine.runAndWait()

        def handle_click(self, pos):
            if self.fakebot_rect.collidepoint(pos):
                self.send_discord_message(self.text)
                self.text = ''  # Clear input after sending

        def run_animation(self):
            while self.is_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            self.handle_click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.send_discord_message(self.text)
                            self.text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode

                self.draw_animation()  # Draw FakeBot and input box on the screen
                self.clock.tick(60)  # Limit frame rate to 60 FPS

            pygame.quit()  # Quit Pygame when animation loop ends
            self.engine.stop()  # Stop pyttsx3 engine

    if __name__ == "__main__":
        app = FakeBotApp()
        app.run_animation()
else:
    print("Invalid choice. Please enter 1, 2, or 3.")
