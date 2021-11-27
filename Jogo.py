import cv2 as cv
import mediapipe as mp
import math;
import numpy;
map_face_mesh = mp.solutions.face_mesh;


#Indices do olho esquerdo 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]

# Indices do olho direito
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  


video = cv.VideoCapture(0);

#Detectando marcações faciais
def achandoMarcacoes(video, results, desenhar = False):
    video_altura, video_largura = video.shape[:2];
    mesh_coord = [(int(ponto.x * video_largura), int(ponto.y * video_altura)) for ponto in results.multi_face_landmarks[0].landmark];
    if desenhar :
        [cv.circle(video, p,2, (0,255,0), -1) for p in mesh_coord];

    return mesh_coord;

#Distância euclidina
def distanciaEuclidiana(ponto, ponto1):
    x, y = ponto;
    x1, y1 = ponto1;
    distancia = math.sqrt((x1 - x)**2 +(y1 - y)**2); 

    return distancia;

#Piscada direita
def piscada(img, marcacoes, indice_Direito, indice_Esquerdo):

    #Olho direito
    #linha horizontal
    olho_direitoD = marcacoes[indice_Direito[0]];
    olho_esquerdoD = marcacoes[indice_Direito[8]];

    #linah vertical
    olho_cimaD = marcacoes[indice_Direito[12]];
    olho_baixoD = marcacoes[indice_Direito[4]];

    cv.line(img,olho_direitoD, olho_esquerdoD, (255,0,0), 2)
    cv.line(img, olho_cimaD, olho_baixoD, (255,0,0), 2);

    #Olho esquerdo
    #linha horizontal
    olho_direitoE = marcacoes[indice_Esquerdo[0]];
    olho_esquerdoE = marcacoes[indice_Esquerdo[8]];
    
    #linha vertical
    olho_cimaE = marcacoes[indice_Esquerdo[12]];
    olho_baixoE = marcacoes[indice_Esquerdo[4]];

    cv.line(img, olho_direitoE, olho_esquerdoE, (255,0,0),2);
    cv.line(img, olho_cimaE, olho_baixoE, (255,0,0),2);

    distanciaDir_D = distanciaEuclidiana(olho_direitoD, olho_esquerdoD);
    distanciaEsq_D = distanciaEuclidiana(olho_cimaD, olho_baixoD);

    distanciaDir_E = distanciaEuclidiana(olho_cimaE, olho_baixoE);
    distanciaEsq_E = distanciaEuclidiana(olho_direitoE, olho_esquerdoE);
    
    relacaoDir = distanciaDir_D/distanciaEsq_D;
    relacaoEsq = distanciaEsq_E/distanciaDir_E;

    relacao = (relacaoDir+relacaoEsq)/2;
    return relacao;

import pygame as pg
from pygame import sprite;
from pygame.locals import *;
from sys import exit;
import os;
from random import randrange

pg.init();
pg.mixer.init();

diretorio_principal = os.path.dirname(__file__);
diretorio_imagens = os.path.join(diretorio_principal, 'imagens');
diretorio_sons = os.path.join(diretorio_principal, 'sons');

largura = 640;
altura = 480;

BRANCO = (255,255,255);

tela = pg.display.set_mode((largura, altura));
pg.display.set_caption("Jogo 10");


sprite_sheet = pg.image.load(os.path.join(diretorio_imagens, "dinoSpritesheet.png")).convert_alpha();

som_colisao = pg.mixer.Sound(os.path.join(diretorio_sons, "death_sound.wav"));
som_colisao.set_volume(1);
colidiu = False;
pontos = 0;
def reiniciar_jogo():
    global colidiu, pontos;
    colidiu = False;
    cacto.rect.x = largura;
    dino.rect.y = altura - 64 - 96//2;
    dino.pulo = False;
    pontos=0;

def exibe_mensagem(msg, tamanho, cor):
    fonte = pg.font.SysFont('comicsansms', tamanho, True, False);
    mensagem = f'{msg}';
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado;

class Dino(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self);
        self.imagens_dino = [];
        self.som_pulo = pg.mixer.Sound(os.path.join(diretorio_sons, "jump_sound.wav"));
        self.som_pulo.set_volume(1);

        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32));
            img = pg.transform.scale(img, (32*3, 32*3));
            self.imagens_dino.append(img);

        self.index_lista = 0;
        self.image = self.imagens_dino[self.index_lista];
        self.rect = self.image.get_rect();
        self.mask = pg.mask.from_surface(self.image);
        self.pos_y_inicial = altura - 64 - 96//2;
        self.rect.center = (100,altura - 64);
        self.pulo = False;
    def pular(self):
        self.pulo = True;
        self.som_pulo.play();
        
    def update(self):
        if self.pulo == True:
            if self.rect.y  <= 200:
                self.pulo = False;
            self.rect.y -= 20;
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20;
            else:
                self.rect.y = self.pos_y_inicial;

        if self.index_lista > 2:
            self.index_lista = 0.
        self.index_lista += 0.25;
        self.image = self.imagens_dino[int(self.index_lista)];

class Nunvens(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self);
            self.image = sprite_sheet.subsurface((7*32, 0), (32,32));
            self.image = pg.transform.scale(self.image, (32*3, 32*3));
            self.rect = self.image.get_rect();
            self.rect.center = (100,100);
            self.rect.y = randrange(50, 200, 50);
            self.rect.x = largura - randrange(30, 300, 90);

        def update(self):
            if self.rect.topright[0] < 0: 
                self.rect.x = largura;
                self.rect.y = randrange(50, 200, 50); 

            self.rect.x -= 10;

class Chao(pg.sprite.Sprite):
    def __init__(self, pos_x):
        pg.sprite.Sprite.__init__(self);
        self.image = sprite_sheet.subsurface((6*32,0), (32,32));
        self.image = pg.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect();
        self.rect.y = altura - 64;
        self.rect.x = pos_x * 64;

    def update(self):
        if self.rect.topright[0] < 0: 
            self.rect.x = largura;
        self.rect.x -= 10;

class Cacto(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self);
            self.image = sprite_sheet.subsurface((5*32,0), (32,32));
            self.image = pg.transform.scale(self.image, (32*2, 32*2))
            self.rect = self.image.get_rect();
            self.mask = pg.mask.from_surface(self.image);
            self.rect.center = (largura, altura - 64);

        def update(self):
            if self.rect.topright[0] < 0:
                self.rect.x = largura;
            self.rect.x -= 10;

todas_as_sprites = pg.sprite.Group();
dino = Dino();
todas_as_sprites.add(dino);

for i in range(4):
    nuvem = Nunvens();
    todas_as_sprites.add(nuvem);

for i in range((largura*2)//64):
    chao = Chao(i);
    todas_as_sprites.add(chao);

cacto = Cacto();
todas_as_sprites.add(cacto);

grupo_obstaculos =  pg.sprite.Group();
grupo_obstaculos.add(cacto);

relogio = pg.time.Clock();
piscou = False;
with map_face_mesh.FaceMesh(min_detection_confidence = 0.5, min_tracking_confidence= 0.5) as face_mesh:

    while True:

        ret,frame = video.read();

        frame = cv.resize(frame, None, fx= 1.5, fy=1.5, interpolation=cv.INTER_CUBIC);

        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR);
        resultado = face_mesh.process(rgb_frame);
        if resultado.multi_face_landmarks:
            mesh_coords = achandoMarcacoes(frame, resultado, True);
            
            relacao = piscada(frame, mesh_coords, RIGHT_EYE, LEFT_EYE);
            cv.putText(frame, f"Piscada: {relacao}", (50,100), cv.FONT_HERSHEY_COMPLEX, 1.0, (255,0,0),2);
   
            #Se o olho direito piscar, cartão muda para vermelho
            if relacao > 4.5:
                cv.putText(frame, "Piscou", (50,400), cv.FONT_HERSHEY_COMPLEX, 1.3, (0,0,255),2);
                piscou = True;
             
        cv.imshow("Video", frame);
        key = cv.waitKey(1);
        if key ==ord('q') or key==ord('q'):
            break;
   
        relogio.tick(30);
        tela.fill(BRANCO);
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit();
                exit();
        if piscou:
            if dino.rect.y != dino.pos_y_inicial:
                pass;
            else:
                dino.pular();
                pontos += 1;
        
        if piscou and colidiu == True:
            reiniciar_jogo();
        pontuacao = exibe_mensagem(f"Pontos: {pontos}", 50, (0,0,0));
        tela.blit(pontuacao, (300, 0))
        colisoes = pg.sprite.spritecollide(dino, grupo_obstaculos, False, pg.sprite.collide_mask);
        todas_as_sprites.draw(tela);
        if colisoes and colidiu == False:
            som_colisao.play();
            colidiu = True;

        if colidiu == True:
            game_over = exibe_mensagem("GAME OVER", 40, (0,0,0));
            tela.blit(game_over, (largura/2, altura/2));
            restart = exibe_mensagem("Pisque para reiniciar", 20, (0,0,0));
            tela.blit(restart, (largura//2, (altura//2)+ 60));
        else:
            todas_as_sprites.update();
        
        pg.display.flip();
        piscou = False;
    cv.destroyAllWindows();
    cv.waitKey();
    video.release();