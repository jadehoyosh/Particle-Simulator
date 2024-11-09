import pygame
import random
import math
from particles.particle import Particle
from movement.collisions import Collision

(width, height) = (1280, 720)
background_color = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Simualtor')

# Initialize font
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Create multiple particles
number_of_particles = 0
my_particles = []

selected_particle = None
spawn_particles = False
spawn_delay = 10
spawn_counter = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = Particle.findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                spawn_particles = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                spawn_particles = False
                

    if spawn_particles:
        spawn_counter += 1
        if spawn_counter >= spawn_delay:
            number_of_particles += 1
            size = random.randint(10,20)
            x = random.randint(size, width - size)
            y = random.randint(size, height - size)
    
            particle = Particle((x, y), size, width, height)
            particle.speed = random.random()
            particle.angle = random.uniform(0, math.pi*2)

            my_particles.append(particle)

            spawn_counter = 0


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
            collision = Collision(particle, particle2)

            if collision.checkCollision():
                collision.handleCollision()
        particle.display(screen)

    # Render and display the particle count
    particle_count_text = font.render(f"Particles: {len(my_particles)}", True, (0,0,0))
    screen.blit(particle_count_text, (10,10))

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0,0,0))
    screen.blit(fps_text, (10,40))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

