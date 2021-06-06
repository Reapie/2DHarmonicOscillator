import pygame

from vectormath import Vector2
import math

FPS = 60
size = (width, height) = (1920, 1080)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 64, 255)

paused = False
grabbed = False
last_pos = Vector2(0, 0)
pos_save_freq = 3

pygame.init()
pygame.display.set_caption("2D Harmonic Oscillator")
center = Vector2(width / 2, height / 2)
paint_area = pygame.display.set_mode(size)
trace_area = pygame.surface.Surface(size)
clock = pygame.time.Clock()
pos = Vector2(int(width / 2), int(height / 4))

trajectory = []

# --- Physical Units --- 
v = Vector2(60, 0)   # initial speed in pixel per second
k = 2    # spring constant in newton / pixel
v_loss = 0  # velocity loss per second in %
spring_default_length = (height / 4)
m = 10   # mass in kg
# --- --- --- --- --- 

def spring():
    global v
    kv = center - pos   # get direction of center relative to object
    spring_length = math.hypot(kv.x, kv.y)
    kv.normalize()  # scale to length of 1
    
    d = spring_length - spring_default_length
    kv *= (k * d) / m

    v += kv

def move():
    global pos, v, last_pos
    v = v * (1 - adjust_for_framerate(v_loss / 100))
    last_pos = pos.copy()
    pos += adjust_for_framerate(v)
    

def draw():
    # Draw trajectory
    for i in range(len(trajectory) - 1):
        pygame.draw.aaline(paint_area, BLUE, trajectory[i], trajectory[i + 1])
    # draw line from middle to object
    pygame.draw.aaline(paint_area, WHITE, center, pos)
    # Draw actual object
    pygame.draw.circle(paint_area, BLUE, pos, 15, 15)
        

def adjust_for_framerate(value):    # instead of once per frame once per second
    return value / FPS

def main():
    global pos, grabbed, paused, last_pos, v
    pos_save_count = 3  # save every nth point
    is_running = True  # run condition
    while is_running:  # main loop
        # repaint with black
        paint_area.fill(BLACK)
        # Show where middle is!
        pygame.draw.rect(paint_area, WHITE, pygame.Rect(center[0] - 5, center[1] - 5, 10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                print("Quitting")
            # Hold mouse to grab
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                trajectory.clear()
                grabbed = not grabbed
            # Toggle pause with K_SPACE
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                trajectory.clear()
                paused = not paused
        
        # actual movement
        if not grabbed and not paused:
            spring()
            move()
        elif grabbed:
            last_pos = pos.copy()
            pos = Vector2(pygame.mouse.get_pos())
            v = (pos - last_pos) * FPS  # is adjusted in move

        # save trajectory
        if (False):     # limit?
            trajectory.pop(0)
        if (pos_save_count == 0):
            trajectory.append(last_pos)
        pos_save_count = (pos_save_count - 1) % pos_save_freq

        draw()

        # update the paint_area every 1/fps seconds
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()