import pygame
import random
import json
import os
pygame.init()



#Global Variables
Cgame=True
walkRight=[]
slideRight=[]
jumpRight=[]
background=""
win=""
screenX=1000
screenY=450
bird=[]
EnemyY=0
EnemyX=980
walkRight=[]
relx=0
tdelay=50
Run=True
cDrawX=""
cDrawY=""
score=0
fcount=0
monster=[]
mcount=0
pause=False
high_score=0
snd="speaker_on.png"
mstatus=True
#/Global Variables

# runSound=pygame.mixer.Sound("run.wav")

def getHighScore():
    global high_score
    try:
        with open(os.path.join(os.path.dirname(__file__),'score.json'), 'r') as openfile:
            json_score=json.load(openfile)
        high_score=json_score["high-score"]
    except:
        score={"high-score":0}
        with open(os.path.join(os.path.dirname(__file__),"score.json"), "w") as outfile:
            json.dump(score,outfile)

def saveScore(score):
    with open(os.path.join(os.path.dirname(__file__),'score.json'), 'r') as openfile:
        json_score=json.load(openfile)
    if json_score["high-score"]<score:
        score={"high-score":score}
        with open(os.path.join(os.path.dirname(__file__),"score.json"), "w") as outfile:
            json.dump(score,outfile)


def reset():
    global walkRight,slideRight,jumpRight,background,win,screenX,screenY,bird,EnemyX,EnemyY,walkRight,relx,tdelay,Run,cDrawX,cDrawX,score,fcount,monster,mcount,pause
    walkRight=[]
    slideRight=[]
    jumpRight=[]
    background=""
    win=""
    screenX=1000
    screenY=450
    bird=[]
    EnemyY=0
    EnemyX=980
    walkRight=[]
    relx=0
    tdelay=50
    Run=True
    cDrawX=""
    cDrawY=""
    score=0
    fcount=0
    monster=[]
    mcount=0
    pause=False


def main():
    music=pygame.mixer.music.load(os.path.join(os.path.dirname(__file__),'Assets','music','music.mp3'))
    if mstatus:
        pygame.mixer.music.play(-1)
    
    def texInit(resx,resy):
        global walkRight
        global slideRight
        global jumpRight
        global background
        global win
        global bird
        global monster
        win = pygame.display.set_mode((resx,resy))
        pygame.display.set_caption("Mad Run")
        for number in range(0,10):
            number=str(number)
            sprite=pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Character','Run__00'+number+'.png'))
            sprite=pygame.transform.scale(sprite,(130,130))
            walkRight.append(sprite)
            #Loading Character textures
        for number in range(0,9):
            number=str(number)
            sprite=pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','bluebat','skeleton-fly_0'+number+'.png'))
            sprite=pygame.transform.scale(sprite,(60,60))
            #sprite=pygame.transform.flip(sprite, False, True)
            bird.append(sprite)
        for number in range(0,9):
            number=str(number)
            sprite=pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Monster','skeleton-walking_'+number+'.png'))
            sprite=pygame.transform.scale(sprite,(60,60))
            #sprite=pygame.transform.flip(sprite, False, True)
            monster.append(sprite)

        for number in range(0,10):
            number=str(number)
            sprite=pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Character','Slide__00'+number+'.png'))
            sprite=pygame.transform.scale(sprite,(100,100))
            slideRight.append(sprite)


        for number in range(0,10):
            number=str(number)
            sprite=pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Character','Jump__00'+number+'.png'))
            sprite=pygame.transform.scale(sprite,(130,130))
            jumpRight.append(sprite)

        background = pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background','back.jpg')).convert()
        #bird = pygame.image.load('./Background/bird.png')

    def redrawGameWindow(motion):
        global high_score
        proto.draw(win,motion)
        text=font.render("Score: "+str(score),1,(255,255,255))
        highscore=font.render("High-Score: "+str(high_score),1,(255,255,255))
        win.blit(text,(800,10))
        win.blit(highscore,(600,10))
        pygame.display.update()

    def back(): #Moving background
        global relx
        rel=relx % background.get_rect().width
        win.blit(background, (rel-background.get_rect().width,0))
        if rel < screenX:
            win.blit(background,(rel,0))
        relx-=8
            



    class ene():
        def __init__(self):
            self.hitbox=[0,0,0,0]
        def drawEnemy(self,win,x,y):
            global bird,fcount,mcount,monster
            if y>=250:
                if mcount + 1 >= 27:
                        mcount = 0
                win.blit(monster[mcount//3], (x,y))
                mcount=mcount+3
                self.hitbox=(x,y,60,45)
            else:
                if fcount + 1 >= 27:
                        fcount = 0
                win.blit(bird[fcount//3], (x,y))
                fcount=fcount+3
                self.hitbox=(x,y,60,45)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        def spawnEnemy(self):
            global EnemyX,EnemyY,cDrawX,cDrawY
            if EnemyY==0 or EnemyX<=proto.x+30:
                if EnemyX<=proto.x+30:
                    cDrawX=EnemyX
                    cDrawY=EnemyY            
                EnemyX=980
                EnemyY=random.randrange(40,300,10)
                enemy.drawEnemy(win,EnemyX,EnemyY)
            EnemyX=EnemyX-20
            enemy.drawEnemy(win,EnemyX,EnemyY)
            if cDrawX and cDrawY:
                enemy.drawEnemy(win,cDrawX,cDrawY)
                if cDrawX<=0:
                    cDrawX=""
                    cDrawY=""
                else:
                    cDrawX=cDrawX-20

    enemy=ene()




    class player():
        def __init__(self,x,y,walkCount,slideCount,jumpCount):
            self.x=x
            self.y=y
            self.walkCount=walkCount
            self.slideCount=slideCount
            self.jumpCount=jumpCount
            self.hitbox=(self.x+20,self.y,90,120)
        def draw(self,win,motion):
            if motion=="run":
                
                if self.walkCount + 1 >= 27:
                    self.walkCount = 0
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.hitbox=(self.x+20,self.y,90,120)
                self.walkCount=self.walkCount+3
            if motion=="slide":     
                if self.slideCount + 1 >= 27:
                    self.slideCount = 0
                win.blit(slideRight[self.slideCount//3], (self.x,self.y+50))
                self.hitbox=(self.x+20,self.y+50,80,100)
                self.slideCount=self.slideCount+3
            if motion=="jump":    
                if self.jumpCount + 1 >= 27:
                    self.jumpCount = 0
                win.blit(jumpRight[self.jumpCount//3], (self.x,self.y-100))
                self.hitbox=(self.x+20,self.y-100,70,110)
                self.jumpCount=self.jumpCount+3
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    texInit(screenX,screenY)
    proto=player((screenX/2)-210,screenY-250,0,0,0)


    global Run,score,tdelay,high_score,Cgame
    while Cgame:
        getHighScore()
        back()
        motion="run"
        score+=1
        if score>high_score:
            high_score=score
        fail=False
        font=pygame.font.SysFont('comicsans',25,True)
        pygame.time.delay(tdelay)
        if proto.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and proto.hitbox[1] + proto.hitbox[3] > enemy.hitbox[1]:
            if proto.hitbox[0] + proto.hitbox[2] > enemy.hitbox[0] and proto.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                fail=True
        if tdelay>20:
                tdelay=tdelay-1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Cgame = False 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:  
            motion="slide"
        elif keys[pygame.K_UP] or keys[pygame.K_SPACE]:  
            motion="jump"
        enemy.spawnEnemy()
        redrawGameWindow(motion)
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.music.pause()
            reset()
            menu()
        if fail:
            pygame.mixer.music.pause()
            failSound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__),'Assets',"music","fail.wav"))
            if mstatus:
                pygame.mixer.Sound.play(failSound)
            saveScore(score)
            font = pygame.font.Font('freesansbold.ttf', 32)
            instfont = pygame.font.Font('freesansbold.ttf', 20) 
            text=font.render("GAME OVER",1,(255,255,255))
            inst=instfont.render("Press Q to quit to main menu  or Return to restart",1,(0,0,0))
            textRect = text.get_rect()  
            instRect = inst.get_rect()
            instRect.center=(screenX//2,screenY//2+30)
            textRect.center = (screenX // 2, screenY // 2) 
            win.blit(text, textRect)
            win.blit(inst, instRect)  
            pygame.display.update()
            while Cgame:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Cgame=False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    pygame.mixer.Sound.stop(failSound)
                    break
                if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                    reset()
                    pygame.mixer.Sound.stop(failSound)
                    menu()

            reset()
            main()



def button(x,y,game,action,win):
    global snd,mstatus,Cgame
    select= pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background','selector.png')).convert_alpha()
    select=pygame.transform.scale(select,(60,60))
    w=game.get_rect().width
    h=game.get_rect().height
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        win.blit(select,(x-50,y+15))
        if click[0] == 1:
            if action=="ngame":
                pygame.mixer.music.pause()
                score={"high-score":0}
                with open(os.path.join(os.path.dirname(__file__),"score.json"), "w") as outfile:
                    json.dump(score,outfile)
                main()
            elif action=="cont":
                pygame.mixer.music.pause()
                main()
            elif action=="quit":
                Cgame=False
            elif action=="spk":
                if mstatus:
                    mstatus=False
                    snd="speaker_off.png"
                    menu()
                else:
                    mstatus=True
                    snd="speaker_on.png"
                    menu()

def menu():
    global Cgame
    music=pygame.mixer.music.load(os.path.join(os.path.dirname(__file__),'Assets','music','menumc.mp3'))
    if mstatus:
        pygame.mixer.music.play(-1)
    while Cgame:
        win = pygame.display.set_mode((screenX,screenY))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Cgame = False 
        logo = pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background','logo.png')).convert_alpha()
        if mstatus:
            spk = pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background',snd)).convert_alpha()
        else:
            spk = pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background',snd)).convert_alpha()
        spk=pygame.transform.scale(spk,(60,60))
        menuBg = pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background','menu.jpg')).convert()
        win.blit(menuBg, (0,0))
        cgame =pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background','start.png')).convert_alpha()
        cgx=(screenX/2)+50
        cgy=(screenY/3)-50
        ngame = pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets','Background','reset.png')).convert_alpha()
        ngx=(screenX/2)+50
        ngy=cgy+80
        qgame = pygame.image.load(os.path.join(os.path.dirname(__file__),'Assets',    'Background','quit.png')).convert_alpha()
        qgx=(screenX/2)+50
        qgy=ngy+80
        win.blit(logo,(100,screenY/2-50))
        win.blit(cgame,(cgx,cgy))
        win.blit(ngame,(ngx,ngy))
        win.blit(qgame,(qgx,qgy))
        win.blit(spk,(30,30))
        button(ngx,ngy,ngame,"ngame",win)
        button(30,30,spk,"spk",win)
        button(cgx,cgy,cgame,"cont",win)
        button(qgx,qgy,qgame,"quit",win)
        #print(select)
        pygame.display.flip()
        #main() 


menu()
if not Cgame:
    pygame.quit()


