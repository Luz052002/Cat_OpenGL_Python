import glfw
import pyrr
from PIL import Image
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import numpy as np

texture_list=['whiteCat.jpg', 'blackCat.jpg']

# ... (resto de tu código, omitido para brevedad)
# Lista de módulos que deseas verificar
modulos = ['pygame', 'pygame.locals', 'OpenGL.GL', 'OpenGL.GLU']

for modulo in modulos:
    if modulo in sys.modules:
        print(f"El módulo {modulo} se importó correctamente.")
    else:
        print(f"El módulo {modulo} no se importó.")

vertices = (
    #CABEZA DEL GATO
    (-1.8, 3, 0), #0
    (-2, 2, 0), #1
    (-1.4, 2.4, 0), #2
    (-1.8, 1, 0), #3
    (-1.4, 0.8, 0), #4
    (-1, 0.6, 0), #5
    (-0.6, 0.8, 0), #6
    (-0.2, 1, 0), #7
    (0, 2, 0), #8
    (-0.2, 3, 0), #9
    (-0.6, 2.4, 0), #10
    (-1, 2.4, 0), #11
    (-1.2, 1.2, 0), #12
    (-0.8, 1.2, 0), #13
    (-1, 1, 0), # 14 
    (-0.4, 1.6, 0), # 15
    (-1.6, 1.6, 0), #16
    
    #CUERPO DEL GATO
    (-1.8, 0, 0), #17
    (-1.2, -1.6, 0), #18
    (-1.4, -2, 0), #19
    (-1, -2, 0), #20
    (-0.6, -2, 0), #21
    (0.2, -2, 0), #22
    (0.6, -0.6, 0), #23
    (-0.2, 0, 0), #24
    (-0.4, 0.4, 0), #25
    (-0.8, -1.6, 0), #26
    (-1, -1.4, 0), #27
    
    #COLITA DEL GATO
    (1.2, -1, 0), #28
    (0.86, 0.35, 0), #29
    (1.4, 0.6, 0), #30
    (0.8, 0.6, 0), #31
    (0.8, -1.2, 0), #32
    (0.4, -1.4, 0), #33
)

edges = (
    #CABEZA DEL GATO
    (0, 2),
    (0, 1),
    (1, 2),
    (3, 1),
    (3, 2),
    (3, 5),
    (3, 12),
    (5, 14),
    (7, 5),
    (7, 13),
    (7, 10),
    (7, 8),
    (9, 8),
    (9, 10),
    (10, 8),
    (11, 2),
    (11, 10),
    (11, 12),
    (11, 13),
    (13, 12),
    (12, 16),
    (13, 15),
    (14, 12),
    (14, 13),
    
    #CUERPO DEL GATO
    (4, 17),
    (4, 27),
    (6, 25),
    (6, 27),
    (19, 18),
    (19, 20),
    (20, 17),
    (20, 24),
    (21, 20),
    (21, 26),
    (21, 22),
    (23, 22),
    (23, 26),
    (23, 25),
    (24, 25),
    (27, 18),
    (27, 26),
    
    #COLITA DEL GATO
    (28, 22),
    (28, 32),
    (28, 29),
    (29, 31),
    (30, 29),
    (31, 30),
    (31, 29),
    (31, 32),
    (32, 33)
)

surfaces ={ #Cuadrantes
    (2,16,12,11), #R16
    (11,13,15,10), #R17
    (4,17,18,27), #R18
    (4,27,6,5), #R19
    (6,27,26,24), #R20
    (24,26,23,25), #R21
    (23,26,21,22),  #R22
    (12,3,5,14), #R4
    (14,5,7,13), #R4.1
    (27,18,20,26) #R10
}

triangles = {
    (0,1,2), #R1
    (1,3,2), #R2
    (16,3,12), #R3
    (12,14,13), #R5
    (11,12,13), #R6
    (13,7,15), #R7
    (10,7,8), #R8
    (10,8,9), #R9
    (18,19,20), #R11
    (26,20,21), #R12
    (33,22,28), #R13
    (31,32,28), #R14
    (31,29,30) #R15
}

def load_texture(image_path):
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    
    image_data = np.array(list(image.getdata()), np.uint8)
    
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    return textureID

def Cube(white_cat_texture, black_cat_texture):
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, white_cat_texture)
    glBegin(GL_TRIANGLES)
    for triangle in triangles:
        glTexCoord2f(0, 0); glVertex3fv(vertices[triangle[0]])
        glTexCoord2f(1, 0); glVertex3fv(vertices[triangle[1]])
        glTexCoord2f(0, 1); glVertex3fv(vertices[triangle[2]])
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, black_cat_texture)
    glBegin(GL_QUADS)
    for surface in surfaces:
        glTexCoord2f(0, 0); glVertex3fv(vertices[surface[0]])
        glTexCoord2f(1, 0); glVertex3fv(vertices[surface[1]])
        glTexCoord2f(1, 1); glVertex3fv(vertices[surface[2]])
        glTexCoord2f(0, 1); glVertex3fv(vertices[surface[3]])
        
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(85, (display[0] / display[1]), 0.1, 50.0)

    white_cat_texture = load_texture("whiteCat.jpg")
    black_cat_texture = load_texture("blackCat.jpg")

    glTranslatef(0.0, 0.0, -5)
    
    glClearColor(0.53, 0.81, 0.92, 1.0)
    
    # Enable lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Define light properties
    glLightfv(GL_LIGHT0, GL_POSITION, np.array([0.5, 0.5, 1.0, 0.0], dtype='float32')) 
    glLightfv(GL_LIGHT0, GL_AMBIENT, np.array([0.5, 0.5, 0.5, 1.0], dtype='float32')) 
    glLightfv(GL_LIGHT0, GL_DIFFUSE, np.array([1.0, 1.0, 1.0, 1.0], dtype='float32'))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube(white_cat_texture, black_cat_texture)
        
        pg.display.flip()
        pg.time.wait(10)

main()