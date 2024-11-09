import math

class Collision:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def checkCollision(self):
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y

        distance = math.hypot(dx, dy)
        
        return distance < (self.p1.size + self.p2.size)

    def handleCollision(self):

        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        distance = math.hypot(dx, dy)
        overlap = 0.5 * (distance - self.p1.size - self.p2.size)

        self.p1.x -= overlap * (dx / distance)
        self.p1.y -= overlap * (dy / distance)
        self.p2.x += overlap * (dx / distance)
        self.p2.y += overlap * (dy / distance)

        collision_angle = math.atan2(dy, dx)

        speed1 = self.p1.speed
        speed2 = self.p2.speed
        angle1 = self.p1.angle
        angle2 = self.p2.angle

        self.p1.angle = 2 * collision_angle - angle1
        self.p2.angle = 2 + collision_angle - angle2
        self.p1.speed = speed2
        self.p2.speed = speed1