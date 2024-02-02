import pygame
import math

clock = pygame.time.Clock()

pygame.init()


pygame.display.set_caption("Autonomous Creator")
"""
Left Click normal point
Right Click Backwards point
CTRL Left Click Intake on and go to point
CTRL Right Click Intake off and go to point

"""



TARGET_FPS = 10

FIELD_WIDTH = 366
FIELD_HEIGHT = 366
Starting_Red = True

if Starting_Red:
    STARTING_PLACE_X = 75  # robot placement from the left of the field
    STARTING_PLACE_Y = 0  # robot placement from the bottem of the field
    AUTONOMOUS_FILENAME = "autonomousRed.af"
else:
    STARTING_PLACE_X = 76  # robot placement from the left of the field
    STARTING_PLACE_Y = 330  # robot placement from the bottem of the field
    AUTONOMOUS_FILENAME = "autonomousBlue.af"

ROBOT_WIDTH = 32  # robot width in cm
ROBOT_HEIGHT = 36  # robot Height in cm
ROBOT_COLOR = (255, 255, 255)

BACKGROUND_PATH = "Field.jpeg"
is_exe = False
if is_exe:
    BACKGROUND_PATH = "_internal/Field.jpeg"
TYPE_NORMAL = 1
TYPE_REVERSE = 2
TYPE_PICKUP = 3
TYPE_PICKUP_STOP = 4

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


def write_autonomous_to_file_from_points(file_path, points):
    with open(file_path, "w") as file:
        cumulative_angle = 0  # Initialize cumulative angle
        for i, point in enumerate(points):
            if i == 0:
                continue
            last_point = points[i - 1]
            distance = last_point.distance_to(point)
            angle_from_last_point_to_current_point = last_point.angle_to(point)
            cumulative_angle += angle_from_last_point_to_current_point
            if point.type_ == TYPE_NORMAL:
                angle_from_last_point_to_current_point += 0
            elif point.type_ == TYPE_REVERSE:
                angle_from_last_point_to_current_point -= math.pi
                distance = distance * -1
            elif point.type_ == TYPE_PICKUP:
                file.write("intake_in\n")


            if Starting_Red:
                file.write(f"{round(distance, 3)}|{round(math.degrees(angle_from_last_point_to_current_point), 2)}\n")
            if not Starting_Red:
                file.write(f"{round(distance, 3)}|{round(math.degrees(angle_from_last_point_to_current_point) - 180, 3)}\n")
            if point.type_ == TYPE_PICKUP_STOP:
                file.write("intake_stop\n")

running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            new_point = Point(event.pos, TYPE_NORMAL)
            if keys[pygame.K_LCTRL]:
                if event.button == 1:
                    new_point.type_ = TYPE_PICKUP
                elif event.button == 3:
                    new_point.type_ = TYPE_PICKUP_STOP
            else:
                if event.button == 1:
                    new_point.type_ = TYPE_NORMAL
                elif event.button == 3:
                    new_point.type_ = TYPE_REVERSE
            points.append(new_point)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                write_autonomous_to_file_from_points(AUTONOMOUS_FILENAME, points)
            elif event.key == pygame.K_b:
                write_autonomous_to_file_from_points(AUTONOMOUS_FILENAME, points)

    # Draw the field image on the screen
    screen.blit(FIELD_IMAGE, (0, 0))
    pygame.draw.rect(screen, ROBOT_COLOR,
                     (STARTING_PLACE_X, STARTING_PLACE_Y, ROBOT_HEIGHT, ROBOT_WIDTH))
    # Draw points as circles on the image
    for point in points:
        if point.type_ == TYPE_NORMAL:
            color = (255, 0, 0)
        elif point.type_ == TYPE_REVERSE:
            color = (255, 255, 0)
        elif point.type_ == TYPE_PICKUP:
            color = (0, 255, 255)
        elif point.type_ == TYPE_PICKUP_STOP:
            color = (255, 0, 255)
        else:
            color = (255, 255, 255)
        pygame.draw.circle(screen, color, point.position, 5)

    pygame.display.flip()

    # Limit frames per second
    clock.tick(TARGET_FPS)

pygame.quit()
