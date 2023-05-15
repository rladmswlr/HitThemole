import pygame
import random
from pygame import *

class Game:
    def __init__(self):
        self.SCREEN_WIDTH = 800 #화면 폭
        self.SCREEN_HEIGHT = 600 #화면 높이
        self.MOLE_WIDTH = 100 #두더지 폭
        self.MOLE_HEIGHT = 100 #두더지 높이
        self.FONT_SIZE = 31 #폰트 크기
        self.FONT_TOP_MARGIN = 26 #폰트 위 마진
        self.LEVEL_SCORE_GAP = 100 #스코어에  따른 레벨 상승 변수
        self.GAME_TITLE = "Hit The Mole League"

        #스코어, 미스횟수, 레벨, 라이프
        self.score = 0
        self.miss = 0
        self.level = 1
        self.life = 3

        #스크린 초기화
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("bg.png")

        #폰트 설정
        self.font_obj = pygame.font.Font('GROBOLD.ttf', self.FONT_SIZE)
        self.font_obj_main = pygame.font.Font('GROBOLD.ttf', 50)

        #버튼 설정
        self.play = pygame.image.load("play.png")
        self.playover = pygame.image.load("playover.png")
        self.exit = pygame.image.load("exit.png")
        self.exitover = pygame.image.load("exitover.png")
        
        #게임 오버 설정
        self.gameover = pygame.image.load("gameover.png")
        self.gameover = transform.scale(self.gameover, (400,400))
        
        #망치 설정
        self.hammer = pygame.image.load("hammerhit.png")
        self.hammer = transform.scale(self.hammer, (100,100))
        
        #두더지 설정 (스프라이트 시트로 초기화)
        sprite_sheet = pygame.image.load("mole.png")
        self.mole = []
        self.mole.append(sprite_sheet.subsurface(0, 0, 140, 120))
        self.mole.append(sprite_sheet.subsurface(180, 0, 140, 120))
        self.mole.append(sprite_sheet.subsurface(345, 0, 140, 120))
        self.mole.append(sprite_sheet.subsurface(549, 0, 140, 120))
        self.mole.append(sprite_sheet.subsurface(729, 0, 140, 120))
        self.mole.append(sprite_sheet.subsurface(884, 0, 140, 120))

        #구멍 설정
        self.hole_positions = []
        self.hole_positions.append((180, 85))
        self.hole_positions.append((350, 85))
        self.hole_positions.append((535, 85))
        self.hole_positions.append((180, 235))
        self.hole_positions.append((350, 235))
        self.hole_positions.append((535, 235))
        self.hole_positions.append((180, 400))
        self.hole_positions.append((350, 400))
        self.hole_positions.append((535, 400))

        #사운드 설정
        self.soundEffect = SoundEffect()


    #레벨에 따른 두더지가 생성되고 사라지는 때까지의 딜레이 함수
    def player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the mole pop up and down the holes
    # It's in inverse ratio to the player's current level
    def interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    #두더지 피격 함수
    def mole_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.MOLE_HEIGHT):
            return True
        else:
            return False

    button_down = False
    #게임 시작 버튼
    def button(self, x,y,w,h,picture,pictureOver):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        buttonDown = False
        
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            self.screen.blit(pictureOver,(x,y))
            if click[0] == 1 and not buttonDown:
                buttonDown = True
                return True

            elif click[0] == 0:
                buttonDown = False
                return False
        else:
           self.screen.blit(picture,(x,y))
        
    #게임 레벨, 스코어, 미스횟수 업데이트 함수
    def update(self):
        #스코어
        current_score_string = "SCORE : " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255,255,255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = 100
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)

        #미스횟수
        current_misses_string = "MISSES : " + str(self.miss)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = 700
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)

        #레벨
        current_level_string = "LEVEL : " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = 300
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)

        #라이프
        current_life_string = "LIFE : " + str(self.life)
        life_text = self.font_obj.render(current_life_string, True, (255, 255, 255))
        life_text_pos = level_text.get_rect()
        life_text_pos.centerx = 500
        life_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(life_text, life_text_pos)

    #시작메뉴
    def menu(self):
        intro = True
        while intro:
            
            self.screen.blit(self.background, (0,0))
            
            current_main_string = "HTML"
            main_text = self.font_obj_main.render(current_main_string, True, (255, 255, 255))
            main_text_pos = main_text.get_rect()
            main_text_pos.centerx = 410
            main_text_pos.centery = 30
            self.screen.blit(main_text, main_text_pos)

            current_main2_string = "Hit The Mole League"
            main2_text = self.font_obj_main.render(current_main2_string, True, (255, 255, 255))
            main2_text_pos = main2_text.get_rect()
            main2_text_pos.centerx = 410
            main2_text_pos.centery = 70
            self.screen.blit(main2_text, main2_text_pos)
            
            if self.button(315,400,196,100, self.play, self.playover):
                intro = False
                
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    intro = False
            pygame.display.update()
            
    #게임오버
    def gameisdone(self):
        gameover = True
        while gameover:

            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.gameover, (200,50))

            #스코어
            current_score_string = "SCORE : " + str(self.score)
            score_text = self.font_obj.render(current_score_string, True, (255,255,255))
            score_text_pos = score_text.get_rect()
            score_text_pos.centerx = 320
            score_text_pos.centery = 450
            self.screen.blit(score_text, score_text_pos)

            #레벨
            current_level_string = "LEVEL : " + str(self.level)
            level_text = self.font_obj.render(current_level_string, True, (255,255,255))
            level_text_pos = level_text.get_rect()
            level_text_pos.centerx = 510
            level_text_pos.centery = 450
            self.screen.blit(level_text, level_text_pos)
            
            if self.button(315,480,196,100, self.exit, self.exitover):
                gameover = False
                
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    gameover = False
            pygame.display.update()
            
    #메인함수
    def start(self):
        looptime = 0
        num = -1
        loop = True
        is_down = False #두더지가 맞았는가 (true, false)
        interval = 0.1
        initial_interval = 1
        frame_num = 0 #두더지가 나오는 구멍 변수
        left = 0 #두더지 클릭시 두더지 위치 조절

        clock = pygame.time.Clock()

        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0,0,0))
            self.mole[i] = self.mole[i].convert_alpha()
            
        pygame.display.update()

        #무한 반복 부분
        while loop:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

                #두더지 클릭 조건문
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.mole_hit(mouse.get_pos(), self.hole_positions[frame_num]) and num > 0 and left == 0:
                        for i in range(150):
                            self.screen.blit(self.hammer, (self.hole_positions[frame_num][0]+55, self.hole_positions[frame_num][1]-70))
                            pygame.display.update()
                        num = 3
                        left = 14
                        is_down = False
                        interval = 0
                        self.score += 10
                        self.soundEffect.playHurt()
                        self.level = self.player_level()
                        self.update()
                        
                    else:
                        self.miss += 1
                        if self.miss % 5 == 0 and self.miss > 0 and self.life == 3:
                            self.life -= 1

                        elif self.miss % 5 == 0 and self.miss > 0 and self.life == 2:
                            self.life -= 1

                        elif self.miss % 5 == 0 and self.miss > 0 and self.life == 1:
                            self.life -= 1
                        self.update()

            
            if self.life == 0:
                loop = False
            
            if num > 5:
                self.screen.blit(self.background, (0,0))
                self.update()
                num = -1
                left = 0

            if num == -1:
                self.screen.blit(self.background, (0,0))              
                self.update()
                num = 0
                is_down = False
                interval = 0.5
                #두더지가 나올 구멍 0~8까지 랜덤 숫자
                frame_num = random.randint(0,8) 

            #인터벌을 통한 두더지 속도조절
            sec = clock.tick(60)/1000.0
            looptime += sec
            if looptime > interval:
                self.screen.blit(self.background,(0,0))
                self.screen.blit(self.mole[num], (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                self.update()
                
                if is_down is False:
                    num += 1

                else:
                    num -= 1
                    
                if num == 4:
                    interval = 0.3
                    
                elif num == 3:
                    num -= 1
                    is_down = True
                    self.soundEffect.playPop()
                    interval = self.interval_by_level(initial_interval)      
                    
                else:
                    interval = 0.1
                looptime = 0
            pygame.display.flip()

class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("Tetris.mp3")
        self.popSound = pygame.mixer.Sound("pop.wav")
        self.levelSound = pygame.mixer.Sound("point.wav")
        self.hurtSound = pygame.mixer.Sound("hurt.wav")
        pygame.mixer.music.play(-1)
        
    def playPop(self):
        self.popSound.play()
        
    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

pygame.init()

mygame = Game()
mygame.menu()
mygame.start()
mygame.gameisdone()
pygame.quit()

