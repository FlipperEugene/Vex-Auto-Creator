import pygame
import math

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Autonomous Creator")

TARGET_FPS = 10

FIELD_WIDTH = 366
FIELD_HEIGHT = 366
Starting_Red = True

if Starting_Red:
    STARTING_PLACE_X = 75  # robot placement from the left of the field
    STARTING_PLACE_Y = 0  # robot placement from the bottem of the field
    AUTONOMOUS_FILENAME = "autonomousRed.af"
if not Starting_Red:
    STARTING_PLACE_X = 76  # robot placement from the left of the field
    STARTING_PLACE_Y = 330  # robot placement from the bottem of the field
    AUTONOMOUS_FILENAME = "autonomousBlue.af"
ROBOT_WIDTH = 32  # robot width in cm
ROBOT_HEIGHT = 36  # robot Height in cm
ROBOT_COLOR = (255, 255, 255)

BACKGROUND_PATH = "Field.jpeg"

TYPE_NORMAL = 1
TYPE_ACTION = 2

FIELD_IMAGE = pygame.transform.scale(pygame.image.load(BACKGROUND_PATH), (int(FIELD_WIDTH), int(FIELD_HEIGHT)))

screen = pygame.display.set_mode((int(FIELD_WIDTH), int(FIELD_HEIGHT)))


class Point:
    def __init__(self, position, type_):
        self.position = position
        self.type_ = type_

    def distance_to(self, other):
        return math.hypot(self.position[0] - other.position[0], self.position[1] - other.position[1])

    def angle_to(self, other):
        return math.atan2(other.position[0] - self.position[0], other.position[1] - self.position[1])


points = [Point((STARTING_PLACE_X + (ROBOT_HEIGHT / 2), STARTING_PLACE_Y + (ROBOT_WIDTH / 2)), TYPE_NORMAL)]

distances = []
angles = []


def write_autonomous_to_file(file_path, distances, angles):
    with open(file_path, "w") as file:
        for distance, angle in zip(distances, angles):
            if Starting_Red:
                file.write(f"{round(distance, 3)}|{round(angle, 3)}\n")
            if not Starting_Red:
                file.write(f"{round(distance, 3)}|{round(angle / math.degrees(180), 3)}\n")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not points:
                continue

            new_point = Point(event.pos, TYPE_NORMAL)
            last_point = points[-1]
            distance = last_point.distance_to(new_point)
            angle_from_last_point_to_current_point = last_point.angle_to(new_point)
            if event.button == 1:
                distances.append(distance)
                angles.append(math.degrees(angle_from_last_point_to_current_point))
                new_point.type_ = TYPE_NORMAL
            elif event.button == 3:
                distances.append(distance)
                angles.append(math.degrees(angle_from_last_point_to_current_point + math.pi))
                new_point.type_ = TYPE_ACTION
            points.append(new_point)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                write_autonomous_to_file(AUTONOMOUS_FILENAME, distances, angles)

    # Draw the resized image on the screen
    screen.blit(FIELD_IMAGE, (0, 0))
    pygame.draw.rect(screen, ROBOT_COLOR,
                     (STARTING_PLACE_X, STARTING_PLACE_Y, ROBOT_HEIGHT, ROBOT_WIDTH))
    # Draw points as circles on the image
    for point in points:
        if point.type_ == TYPE_NORMAL:
            color = (255, 0, 0)
        elif point.type_ == TYPE_ACTION:
            color = (255, 255, 0)
        pygame.draw.circle(screen, color, point.position, 5)

    pygame.display.flip()

    # Limit frames per second
    clock.tick(TARGET_FPS)

pygame.quit()
