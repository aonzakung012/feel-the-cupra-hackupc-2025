import pygame
import requests
import sys

# Game settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60
API_URL = "http://localhost:5000/state"
POLL_INTERVAL = 0.5  # seconds between API polls

# Physics settings (pixels per second squared)
THRUST_ACC = 400     # upward thrust acceleration when focused (gravity always applies)
GRAVITY_ACC = 300    # downward gravity acceleration

# Cube properties
CUBE_SIZE = 50
START_X = SCREEN_WIDTH // 2 - CUBE_SIZE // 2
START_Y = SCREEN_HEIGHT - CUBE_SIZE


def get_state():
    """Fetch the current state from the API endpoint."""
    try:
        response = requests.get(API_URL, timeout=0.2)
        if response.status_code == 200:
            data = response.json()
            return data.get("state", "Relaxed")
    except requests.RequestException:
        pass
    return "Relaxed"


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Focus vs Relax Cube")
    clock = pygame.time.Clock()

    cube_x = START_X
    cube_y = START_Y
    velocity = 0.0
    state = "Relaxed"
    poll_timer = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 100.0  # delta time in seconds
        poll_timer += dt

        # Poll API at fixed intervals
        if poll_timer >= POLL_INTERVAL:
            state = get_state()
            poll_timer -= POLL_INTERVAL

        # Always apply gravity, and add thrust when focused
        acceleration = -GRAVITY_ACC
        if state == "Focused":
            acceleration += THRUST_ACC

        # Update physics (velocity and position)
        velocity += acceleration * dt
        cube_y -= velocity * dt  # subtract because y=0 at top of screen

        # Clamp cube within screen bounds
        if cube_y < 0:
            cube_y = 0
            velocity = 0
        elif cube_y > SCREEN_HEIGHT - CUBE_SIZE:
            cube_y = SCREEN_HEIGHT - CUBE_SIZE
            velocity = 0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background and cube
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (200, 100, 50), (cube_x, int(cube_y), CUBE_SIZE, CUBE_SIZE))

        # Display current state
        font = pygame.font.Font(None, 36)
        text = font.render(f"State: {state}", True, (200, 200, 200))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
