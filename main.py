#better desmos defeater

#Stuff you need to worry about

image_location = r'C:\Users\61490\Documents\Math\20210218_192347.jpg'

image_height = 30
image_width = 40

window_height = 700
window_width = 933

frames_per_second = 40





'''
INSTRUCTIONS:
To move around, use WASD
To zoom in and out, use Q and E

When you zoom in and out, pygame compresses the image and it gets blurrier.
The program will automatically sharpen the image every now and again, but
to do it manually press X

Click on two points to create a line between them
Press Z to undo

Press C to copy all of the lines on the screen. These can be pasted
straight into desmos
'''







#Stuff you dont need to worry about


import pygame
from pygame.locals import *
import pyperclip

pygame.init()
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Desmos")

class Screen:
  def __init__(self,width,height):
    self.width = width
    self.height = height
    self.image_width = image_width
    self.image_height = image_height
    self.top_corner_coordinate = [0,0]
    
    self.beginning_points = {}
    self.ending_points = {}
    
    self.resetcounter = 0
    self.resetthreshold = 40
    
    self.load_image()
    self.size_surface()
    
    self.mode = 0

  def load_image(self):
    self.surface = pygame.image.load(image_location)
    self.resetcounter = 0


  def size_surface(self):
    if self.resetcounter > self.resetthreshold:
      self.load_image()
    self.surface = pygame.transform.scale(self.surface,(self.width,self.height))
    self.resetcounter += 1
    

  def pygame_point_to_coordinate(self, pgx, pgy):
    x = self.image_width*(pgx-self.top_corner_coordinate[0])/self.width - (self.image_width/2)
    y = self.image_height*(-(pgy-self.top_corner_coordinate[1]))/self.height + (self.image_height/2)
    return x,y

  def coordinate_to_pygame_point(self, x, y):
    pgx = self.width* (x+(self.image_width/2)) /self.image_width + self.top_corner_coordinate[0]
    pgy = self.height*(-y+(self.image_height/2))/self.image_height + self.top_corner_coordinate[1]
    return pgx,pgy

  def add_point(self,x,y):
    if not self.mode:
      self.beginning_points[len(self.ending_points)] = x,y
      self.mode = 1
    else:
      self.ending_points[len(self.ending_points)] = x,y
      self.mode = 0
      
    
      

  def delete_last_point(self):
    self.mode = 0
    last_point = max(map(len,(self.beginning_points,self.ending_points)))-1
    try:
      del self.beginning_points[last_point]
    except Exception as e:
      pass
    try:
      del self.ending_points[last_point]
    except Exception as e:
      pass


  def generate_equations(self):
    eqs = []
    for key in self.ending_points:
      p1 = self.beginning_points[key]
      p2 = self.ending_points[key]
      if p1[0] != p2[0]:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        c = p1[1] - m * p1[0]
        x = [p1[0],p2[0]]
        maxx,minx = max(x),min(x)
        eqs.append(rf'y={round(m,4)}x{["-","+"][c>=0]}{abs(round(c,4))}\left\{{{round(minx,2)}<x<{round(maxx,2)}\right\}}')
      else:
        x = p1[0]
        y = (p1[1],p2[1])
        miny,maxy=min(y),max(y)
        eqs.append(rf'x={round(x,2)}\left\{{{round(miny,2)}<y<{round(maxy,2)}\right\}}')
    return '\n'.join(eqs)

  def handle_keys(self):
    keys=pygame.key.get_pressed()
    if keys[K_a]:
      self.top_corner_coordinate[0] += 5
    if keys[K_d]:
      self.top_corner_coordinate[0] -= 5   
    if keys[K_w]:
      self.top_corner_coordinate[1] += 5
    if keys[K_s]:
      self.top_corner_coordinate[1] -= 5
    if keys[K_q]:
      self.inflate(1.02)
    if keys[K_e]:
      self.inflate(0.98)

  def inflate(self,value):
    self.width = int(self.width * value)
    self.height = int(self.height * value)
    self.top_corner_coordinate[0] = int(self.top_corner_coordinate[0] * value)
    self.top_corner_coordinate[1] = int(self.top_corner_coordinate[1] *  value)
    self.size_surface()

  def blit(self, displaysurface):
    displaysurface.blit(self.surface,self.top_corner_coordinate)
    for point in self.beginning_points:
      pygame.draw.circle(displaysurface,(255,255,0),(bp:=self.coordinate_to_pygame_point(*self.beginning_points[point])),1)
      if point in self.ending_points:
        pygame.draw.circle(displaysurface,(255,255,0),(ep:=self.coordinate_to_pygame_point(*self.ending_points[point])),1)
        pygame.draw.line(displaysurface,(255,255,0),bp,ep,1)
    

      
      
screen = Screen(window_width,window_height)


while 1:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      
      
    if event.type == MOUSEBUTTONDOWN:
      initial_pos = pygame.mouse.get_pos()
      pos = screen.pygame_point_to_coordinate(*initial_pos)
      screen.add_point(*pos)
      
    if event.type == KEYDOWN:
      if event.key == K_z:
        screen.delete_last_point()

      if event.key == K_c:
        pyperclip.copy(screen.generate_equations())

      if event.key == K_x:
        screen.load_image()
        screen.size_surface()


  displaysurface.fill((0,0,0))
  screen.handle_keys()
  screen.blit(displaysurface)
    
  pygame.display.update()
  FramePerSec.tick(frames_per_second)
