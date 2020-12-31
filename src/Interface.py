import pygame

weight = 1200
height = 800


class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()
class Buttom(pygame.sprite.Sprite):
    def __init__(self,img1,img2,x,y):
        self.imgnor=img1
        self.imgselec=img2
        self.imgact=self.imgnor
        self.rect=self.imgact.get_rect()
        self.rect.left,self.rect.top=(x,y)

    def update(self,screen,cursor):
        if cursor.colliderect(self.rect):
            self.imgact=self.imgselec
        else:
            self.imgact=self.imgnor
        screen.blit(self.imgact,self.rect)


def run():
    pygame.init()
    screen = pygame.display.set_mode([weight, height])
    pygame.display.set_caption("CIRCUIT DESIGNER 👨🏼💻")
    done = False
    clock = pygame.time.Clock()

    #Create bottom
    simulationnorm=pygame.image.load("simulation.png")
    simulationselec=pygame.image.load("simulation_Selection.png")
    #Create cursor instance
    cursor=Cursor()
    buttom=Buttom(simulationnorm,simulationselec,0,0)
    buttom.update(screen,cursor)
    # Images
    background = pygame.image.load("background.png").convert()
    resistance = pygame.image.load("resistance.png").convert()
    battery = pygame.image.load("battery.png").convert()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #screen.blit(background, [0, 0])
        pygame.display.flip()
    clock.tick(60)
    cursor.update()
    pygame.quit()


run()
