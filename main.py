import pygame
import random
import math
from particle import Particle


def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def checkCollision(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dx, dy)
    return distance < (p1.size + p2.size)

def handleCollision(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dx, dy)
    overlap = 0.5 * (distance - p1.size - p2.size)

    # Separate the particles to avoid overlap
    p1.x -= overlap * (dx / distance)
    p1.y -= overlap * (dy / distance)
    p2.x += overlap * (dx / distance)
    p2.y += overlap * (dy / distance)

    # Calculate the collision angle
    collision_angle = math.atan2(dy, dx)

    # Swap speeds along the collision vector
    speed1 = p1.speed
    speed2 = p2.speed
    angle1 = p1.angle
    angle2 = p2.angle

    # Calculate the new speeds and angles after the collision
    p1.angle = 2 * collision_angle - angle1
    p2.angle = 2 * collision_angle - angle2
    p1.speed = speed2
    p2.speed = speed1

(width, height) = (1280, 720)
background_color = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Simualtor')

# Create multiple particles
number_of_particles = 100
my_particles =[]

for n in range(number_of_particles):
    size = random.randint(10,20)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    
    particle = Particle((x, y), size, width, height)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_color)
    
    
    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            if checkCollision(particle, particle2):
                handleCollision(particle, particle2)
        particle.display(screen)

    pygame.display.flip()

pygame.quit()

