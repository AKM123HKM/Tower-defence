import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Grid Lines")

# Load the triangle sprite
triangle_image = pygame.image.load("dir_triangle.png")
triangle_rect = triangle_image.get_rect()

# Define the number of grid lines
rows = 10
cols = 10

# Calculate spacing between grid lines
row_spacing = height // rows
col_spacing = width // cols

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# List to store placed triangles
placed_triangles = []

# List to store rotation angles for each triangle
rotation_angles = []

# Variable to store the index of the selected triangle
selected_triangle_index = None

# Function to rotate a triangle by a given angle
def rotate_triangle(image, angle):
    return pygame.transform.rotate(image, angle)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                # Get the current mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the mouse click is on any placed triangle
                for i, pos in enumerate(placed_triangles):
                    if triangle_rect.collidepoint(mouse_x - pos[0], mouse_y - pos[1]):
                        # Toggle rotation for the selected triangle
                        if i == selected_triangle_index:
                            selected_triangle_index = None
                        else:
                            selected_triangle_index = i
                        break
            elif event.button == 1:  # Left mouse button
                # Get the current mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Calculate current grid position
                grid_pos = (mouse_x // col_spacing, mouse_y // row_spacing)
                # Add triangle to the list of placed triangles
                placed_triangles.append((grid_pos[0] * col_spacing + col_spacing // 2, grid_pos[1] * row_spacing + row_spacing // 2))
                # Add initial rotation angle for the placed triangle
                rotation_angles.append(0)
        elif event.type == pygame.KEYDOWN:
            if selected_triangle_index is not None:
                if event.key == pygame.K_RIGHT:
                    # Rotate the selected triangle clockwise by 90 degrees
                    rotation_angles[selected_triangle_index] -= 90
                elif event.key == pygame.K_LEFT:
                    # Rotate the selected triangle counterclockwise by 90 degrees
                    rotation_angles[selected_triangle_index] += 90

    # Clear the screen
    screen.fill(WHITE)

    # Draw horizontal grid lines
    for i in range(1, rows):
        pygame.draw.line(screen, BLACK, (0, i * row_spacing), (width, i * row_spacing), 1)

    # Draw vertical grid lines
    for j in range(1, cols):
        pygame.draw.line(screen, BLACK, (j * col_spacing, 0), (j * col_spacing, height), 1)

    # Draw placed triangles
    for i, (pos, angle) in enumerate(zip(placed_triangles, rotation_angles)):
        rotated_triangle = rotate_triangle(triangle_image, angle)
        rotated_rect = rotated_triangle.get_rect(center=(pos[0], pos[1]))
        screen.blit(rotated_triangle, rotated_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
