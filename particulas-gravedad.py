import pygame
import random
import math
import numpy as np

reloj = pygame.time.Clock()
fps = 165
dt = 1/fps
G = 10

tamano_ventana_x = 1024
tamano_ventana_y = 720
color_fondo = (255,255,255)
centro = (tamano_ventana_x/2,
          tamano_ventana_y/2)

x1 = 150
y1 = 255
vx1 = -200
vy1 = 23
x2 = 650
y2 = 150
vx2 = 287
vy2 = -134

radio = 10
grosor_particulas = 2


lados_rect = (tamano_ventana_x-tamano_ventana_x*0.2, 
               tamano_ventana_y-tamano_ventana_y*0.2)
caja = (centro[0]- lados_rect[0]/2,     #distancia con eje y
        centro[1]-lados_rect[1]/2,      #distancia con eje x (QUE ESTÁ ARRIBA)
        lados_rect[0], lados_rect[1])   #ancho y alto
grosor_caja = 5

color_caja = (0,0,0)


def velocidades (x, y, vx, vy, ax, ay):
    velocidad = abs(vx) + abs(vy)
    vnorm = 1-np.exp(-0.001 * velocidad)
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    
    if (x <= caja[0] + grosor_caja + radio or
        x >= caja[0] + caja[2] - grosor_caja -radio):
        if velocidad <= 5000:
            vx = vx * -1#1.2
        else:
            vx = -vx
    
    if (y <= caja[1] + grosor_caja + radio or
        y >= caja[1] + caja[3] - grosor_caja - radio):
        if velocidad <= 5000:
            vy = vy * -0.99 #1.2
        else:
            vy = -vy  
    return(x, y, vx, vy, vnorm)


pygame.init()
screen = pygame.display.set_mode([tamano_ventana_x, tamano_ventana_y])
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    dx = x2-x1
    dy = y2-y1
    distancia = (dx**2 + dy**2)

    if distancia >= 200:
        gravedad = (G /distancia ** 1.15) * 200000
        ax1 = gravedad * dx 
        ay1 = gravedad * dy 
        ax2 = -gravedad * dx 
        ay2 = -gravedad * dy 
    else:
        ax1 = ax2 = ay1 = ay2 = 0

    x1, y1, vx1, vy1, vnorm1 = velocidades(x1, y1, vx1, vy1, ax1, ay1)
    x2, y2, vx2, vy2, vnorm2 = velocidades(x2, y2, vx2, vy2, ax2, ay2)   
    
    
    #Gravedad global
    gravedadG1 = (G / (caja[1] + caja[3]-y1) ** 1.01) * 300
    gravedadG2 = (G / (caja[1] + caja[3]-y2) ** 1.01) * 300

    ag1 = gravedadG1 * (caja[1] + caja[3]-y1)
    ag2 = gravedadG2 * (caja[1] + caja[3]-y2)
    
    if y1 <= caja[1]+caja[3]-radio-grosor_caja:
        vy1 += ag1 * dt
    if y2 <= caja[1] + caja[3]-radio-grosor_caja:
        vy2 += ag2 * dt
    
    
    #Rozamiento
    vx1 *= 0.999
    vy1 *= 0.999
    vx2 *= 0.999
    vy2 *= 0.999
    
    
    #Gravedad global
    #if y1 <= caja[1] + caja[3] - radio - grosor_caja:
    #    vy1 += 24
    #if y2 <= caja[1] + caja[3] - radio - grosor_caja:    
    #    vy2 += 24
    
    
    screen.fill(color_fondo)
    pygame.draw.circle(screen, (vnorm1 * 255, 0,255-(vnorm1 * 255)), (x1,y1), radio)
    pygame.draw.circle(screen, (vnorm2 * 255, 0,255-(vnorm1 * 255)), (x2,y2), radio)
    pygame.draw.rect(screen, color_caja, caja, grosor_caja)
    pygame.display.flip() #"Flip" es update, no girar
    reloj.tick(fps)
pygame.quit()


