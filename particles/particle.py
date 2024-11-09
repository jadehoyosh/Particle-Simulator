import pygame
import random
import math


drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.002)

def addVectors(pos1, pos2):
    angle1, length1 = pos1
    angle2, length2 = pos2

    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y,x)
    length = math.hypot(x,y)

    return (angle, length)

class Particle:
    def __init__(self, position, size, width, height):
        self.x, self.y = position
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.angle = 0
        self.speed = 0
        self.width = width
        self.height = height

    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > self.width - self.size:
            self.x = 2 * (self.width - self.size) - self.x
            self.angle = -self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity
        
        if self.y > self.height - self.size:
            self.y = 2 * (self.height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

    @staticmethod
    def findParticle(particles, mouseX, mouseY):
        for p in particles:
            if math.hypot(p.x-mouseX, p.y-mouseY) <= p.size:
                return p
        return None 