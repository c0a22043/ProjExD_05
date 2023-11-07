import pygame 
import sys
import random 
import numpy as np
import datetime


OCTO_CAT_VELOCITY = 4
OCTO_CAT_JUMP = 20


BGM_FILES = ["ex05/fig/BGM.mp3",
             "ex05/fig/baadakkuman.mp3",
             "ex05/fig/kessen.mp3",
             "ex05/fig/ajito.mp3",
             "ex05/fig/maou-kessen.mp3"
             ]
CURRENT_BGM_INDEX = 0  # 現在のBGMのインデックス

# 別のBGMファイルが再生中かどうかを示すフラグ
is_bgm_playing = False

BGM_FILES = ["ex05/fig/BGM.mp3",
             "ex05/fig/baadakkuman.mp3",
             "ex05/fig/kessen.mp3",
             "ex05/fig/ajito.mp3",
             "ex05/fig/maou-kessen.mp3"
             ]
CURRENT_BGM_INDEX = 0  # 現在のBGMのインデックス

# 別のBGMファイルが再生中かどうかを示すフラグ
is_bgm_playing = False

pygame.init()      
screen = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption("Jump the Rope") 
heart_image = pygame.image.load("ex05/images/heart.png")
clock = pygame.time.Clock()


def COLORS():
    x = random.randint(0,255)
    y =random.randint(0,255)
    z =random.randint(0,255)
    COLORS = [x,y,z]
    return COLORS


class Octo_Cat:
    def __init__(self,x,y):
        #position(プレーヤーのポジション)
        self.x = x
        self.y = y
        #image before scaling(サイズを変える前の画像)
        self.rough_image = pygame.image.load("ex05/images/greenoctocat.png").convert()
        #properly scaled image(サイズを変えた後の画像)
        self.image = pygame.transform.scale(self.rough_image, (20,20))
        #image to show when the player is jumping(ジャンプしてる時の画像)
        self.immune_image = pygame.transform.scale(self.rough_image, (30,30))
        #about movements(動きに関するもの)
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        #if jumping or not(ジャンプしているか否か)
        self.immunity = False
        #the player cannot jump more than a specified amount of time
        #(プレーヤーは一定以上の時間はジャンプし続けられない)
        self.immunity_count = 0
        #life(ライフ)
        self.life = 4
        #if the player is inflicted with damage, it cannot be inflicted again for a certain amount of time
        #(ダメージを受けた後一定時間はダメージを受けない)
        self.life_lost_time = 0
        self.right_shift_pressed = False
        #基本のキーボード状態をFalseとする
        self.shift_pressed = False
        #変数のためローカルに新しく速度を作成。デフォルトは4
        self.OCTO_CAT_VELOCITY = 4
        self.is_paused = False

    #movements(動きに関して)
    def update(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move_right = True
            if event.key == pygame.K_LEFT:
                self.move_left = True
            if event.key == pygame.K_UP:
                self.move_up = True
            if event.key == pygame.K_DOWN:
                self.move_down = True
            if event.key == pygame.K_SPACE:
                self.immunity = True
            if event.key == pygame.K_RSHIFT:  # 右シフトキーが押されたとき
                self.right_shift_pressed = True

            #左シフトダウンの時の処理
            if event.key == pygame.K_LSHIFT:
                self.shift_pressed = True
                self.update_velocity()

            if event.key == pygame.K_p:
                self.is_paused = not self.is_paused

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            if event.key == pygame.K_LEFT:
                self.move_left = False
            if event.key == pygame.K_UP:
                self.move_up = False
            if event.key == pygame.K_DOWN:
                self.move_down = False
            if event.key == pygame.K_RSHIFT:  # 右シフトキーが離されたとき
                self.right_shift_pressed = False

            if event.key == pygame.K_RSHIFT:  # 右シフトキーが離されたとき
                self.right_shift_pressed = False
            #左シフトアップの時の処理
            if event.key == pygame.K_LSHIFT:
                self.shift_pressed = False
                self.update_velocity()

#defiens ropes and dots(線とドットの親クラス)

    #シフトが押された際の速度を分岐させる関数
    def update_velocity(self):
        if self.shift_pressed == True:
            self.OCTO_CAT_VELOCITY = 8
        if self.shift_pressed == False :
            self.OCTO_CAT_VELOCITY = 4
#defiens ropes and dots

class Rope:
    def __init__(self,x=0,y=0,velocity=0,tilt=0,color=0):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.tilt = tilt
        #self.color = color
    def update(self):
        return
    def judge(self,octo_cat):
        return

#vertical ropes(垂直の線)
class Straight_Rope(Rope):
    
    def update(self):
        if(self.x > 635):
            self.direction = "LEFT"
        elif(self.x < 5):
            self.direction = "RIGHT"
        if(self.direction == "RIGHT"):
            self.x += self.velocity
        elif(self.direction == "LEFT"):
            self.x -= self.velocity
        # pygame.draw.line(screen, COLORS[3], [self.x, 0], [self.x, 480], 5)

        pygame.draw.line(screen, COLORS(), [self.x, 0], [self.x, 480], 5)


    #checks if the player and the rope collided
    #(プレーヤーとぶつかったか判定)
    def judge(self,octo_cat):
        if(self.x > (octo_cat.x) and self.x < (octo_cat.x + 20)):
            return True
        else:
            return False

#horizontal ropes(水平の線)
class Straight_Rope_Horizontal(Rope):
    def update(self):
        if(self.y > 475):
            self.direction = "DOWN"
        elif(self.y < 5):
            self.direction = "UP"
        if(self.direction == "DOWN"):
            self.y -= self.velocity
        elif(self.direction == "UP"):
            self.y += self.velocity

        pygame.draw.line(screen, COLORS(),[0, self.y], [640, self.y], 5)

    #checks if the player and the rope collided
    #(プレーヤーとぶつかったか判定)
    def judge(self,octo_cat):
        if(self.y > (octo_cat.y) and self.y < (octo_cat.y + 20)):
            return True
        else:
            return False

#dots(ドット)
class Shooting_Star(Rope):
    def update(self):
        self.x += self.tilt
        self.y += self.velocity

        pygame.draw.circle(screen, COLORS(), [self.x, self.y], 6)

    #checks if the player and the dot collided
    #(プレーヤーとぶつかったか判定)
    def judge(self,octo_cat):
        if((self.y > (octo_cat.y) and self.y < (octo_cat.y + 20)) and (self.x > (octo_cat.x) and self.x < (octo_cat.x + 20))):
            return True
        else:
            return False
pygame.mixer.music.stop()

#起動時画面表示の処理

pygame.mixer.music.stop()

def open():
    endFlag = False
    #フォントとテキストの設定
    font1 = pygame.font.SysFont(None, 80)
    text1 = font1.render("Jump the Rope", False, (255,255,255))
    font2 = pygame.font.SysFont(None, 40)
    text2 = font1.render("Press Any Key to Start", False, (255,255,255))

    # 開始BGMを再生
    pygame.mixer.music.load('ex05/fig/jokyoku.mp3')  # 開始BGMのファイル名に置き換える
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # -1を渡すと無限ループ再生

    while endFlag == False:
        screen.fill((0,0,0))
         #上で設定したテキストを表示
        screen.blit(text1,(30,50))
        screen.blit(text2,(20,150))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                endFlag = True
            elif event.type == pygame.KEYDOWN:

                pygame.mixer.music.stop()


                pygame.mixer.music.stop()

            #もしも何かしらのキーが押されたら、メイン関数を呼び出す

                endFlag = True
                main()


def play_game_over_music():
    pygame.mixer.music.stop()  # すべてのBGMを停止
    game_over_sound = pygame.mixer.Sound('ex05/fig/dead.wav')
    game_over_sound.set_volume(0.2)
    game_over_sound.play()


def main():
    global is_bgm_playing, CURRENT_BGM_INDEX
    endFlag = False
    octo_cat = Octo_Cat(400,400)
    time_elapsed = 0
    force_quit = False
    pygame.mixer.init()
    # ゲーム開始時に最初のBGMを再生
    pygame.mixer.music.load(BGM_FILES[CURRENT_BGM_INDEX])
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    is_bgm_playing = True

    pygame.mixer.init()
    # ゲーム開始時に最初のBGMを再生
    pygame.mixer.music.load(BGM_FILES[CURRENT_BGM_INDEX])
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    is_bgm_playing = True

    q = 0

    ropes = []
    time_2 = 0

    while endFlag == False:
        clock.tick(60)
        if octo_cat.is_paused == False:
            time_elapsed += 1
        font2=pygame.font.SysFont(None, 80)
        text3 = font2.render("Pause now", False, (255,255,255))
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                endFlag = True
                force_quit = True
            octo_cat.update(event)



        # キーボード入力を処理
        keys = pygame.key.get_pressed()

        if keys[pygame.K_TAB]:
            if not is_bgm_playing:
                pygame.mixer.music.stop()  # 現在のBGMを停止
                CURRENT_BGM_INDEX = (CURRENT_BGM_INDEX + 1) % len(BGM_FILES)  # 次のBGMに切り替え
                pygame.mixer.music.load(BGM_FILES[CURRENT_BGM_INDEX])  # 新しいBGMを読み込み
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)  # -1を渡すと無限ループ再生
                is_bgm_playing = True
        else:
            is_bgm_playing = False
       
        if octo_cat.is_paused:
            screen.blit(text3,(20,150))
            pygame.display.update()
            continue


        # キーボード入力を処理
        keys = pygame.key.get_pressed()

        if keys[pygame.K_TAB]:
            if not is_bgm_playing:
                pygame.mixer.music.stop()  # 現在のBGMを停止
                CURRENT_BGM_INDEX = (CURRENT_BGM_INDEX + 1) % len(BGM_FILES)  # 次のBGMに切り替え
                pygame.mixer.music.load(BGM_FILES[CURRENT_BGM_INDEX])  # 新しいBGMを読み込み
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)  # -1を渡すと無限ループ再生
                is_bgm_playing = True
        else:
            is_bgm_playing = False
       
        #move the player

        # timeの計算と表示
        if time_elapsed % 60 == 0:  # timeを増やす頻度を調整
            time_2 += 1

            if time_2 >= 10:  # timeが10以上になった場合の処理
                time_2 *= 1  

        font = pygame.font.SysFont(None, 36)
        text = font.render(f"time: {time_2}", True, (255, 255, 0)) #timeの表示
        screen.blit(text, (10, 10)) #timeの表示位置

        #move the player(プレーヤーを動かす)

        if octo_cat.move_right == True:
            if octo_cat.x < 620:
                octo_cat.x += octo_cat.OCTO_CAT_VELOCITY
        if octo_cat.move_left == True:
            if octo_cat.x > 00:
                octo_cat.x -= octo_cat.OCTO_CAT_VELOCITY
        if octo_cat.move_up == True:
            if octo_cat.y > 00:
                octo_cat.y -= octo_cat.OCTO_CAT_VELOCITY
        if octo_cat.move_down == True:
            if octo_cat.y < 460:
                octo_cat.y += octo_cat.OCTO_CAT_VELOCITY

        #make the instances of ropes and dots
        #(線とドットのインスタンスを作る)
        if (time_elapsed == 20):
            straight_rope = Straight_Rope(0,0,3)
            ropes.append(straight_rope)
        if (time_elapsed == 300):
            straight_rope_horizontal = Straight_Rope_Horizontal(0,0,3)
            ropes.append(straight_rope_horizontal)
        if (time_elapsed == 600):
            straight_rope = Straight_Rope(0,0,3)
            ropes.append(straight_rope)
        if (time_elapsed == 860):
            straight_rope_horizontal = Straight_Rope_Horizontal(0,0,3)
            ropes.append(straight_rope_horizontal)
        #ランダムなタイミングで、ランダムな種類のドットを発生させる
        if(random.randrange(200) < 6):
            shooting_star1 = Shooting_Star(random.randrange(640),0,random.randrange(5) + 5,random.randrange(10) - 5)
            ropes.append(shooting_star1)
            shooting_star2 = Shooting_Star(random.randrange(640),0,random.randrange(5) + 5,random.randrange(10) - 5)
            ropes.append(shooting_star2)
            shooting_star3 = Shooting_Star(10,random.randrange(480),random.randrange(5) + 5,random.randrange(10) - 5)
            ropes.append(shooting_star3)
            shooting_star4 = Shooting_Star(10,random.randrange(480),random.randrange(5) + 5,random.randrange(10) - 5)
            ropes.append(shooting_star4)

        #move all the ropes and dots(線とドットを動かす)
        
        #move all the ropes and dots
        for rope in ropes:
            rope.update()
            #画面から出てしまったドットは削除
            if (rope.x < 0 or rope.x > 640) or (rope.y < 0 or rope.y > 480):
                ropes.remove(rope)
            #一定時間経つごとに、線の動きを早める
            if(time_elapsed % 1000 == 0) and time_elapsed != 0:
                rope.velocity += 1

        #if the player is jumping, do not check if it collided with ropes or dots
        #プレーヤーがジャンプ中であれば、当たり判定を行わない
        if(octo_cat.immunity == True):
            octo_cat.immunity_count += 1
            if (octo_cat.immunity_count < OCTO_CAT_JUMP ):
                screen.blit(octo_cat.immune_image,(octo_cat.x,octo_cat.y))
            else:
                octo_cat.immunity = False
                octo_cat.immunity_count = 0
                screen.blit(octo_cat.image,(octo_cat.x,octo_cat.y))
                
        else:
            screen.blit(octo_cat.image,(octo_cat.x,octo_cat.y))
            for rope in ropes:
                #敵とぶつかった場合でも、前回ダメージを受けてから一定時間が経っていなければダメージを受けない
                if(rope.judge(octo_cat) == True) and (octo_cat.life_lost_time + 30 < time_elapsed):
                    octo_cat.life_lost_time = time_elapsed
                    octo_cat.life -= 1
                    if octo_cat.life == 0:
                        endFlag = True


            if not octo_cat.right_shift_pressed:  # 右シフトが押されていない場合にのみ判定
                for rope in ropes:
                    if(rope.judge(octo_cat) == True) and (octo_cat.life_lost_time + 30 < time_elapsed):
                        octo_cat.life_lost_time = time_elapsed
                        octo_cat.life -= 1
                        if octo_cat.life == 0:
                            endFlag = True
            else:
                # 右シフトが押されている場合、ライフを増やす
                octo_cat.life += 1
                if octo_cat.life > 4:  # ライフが上限を超えないようにする
                    octo_cat.life = 4

             
        # ゲームオーバー音楽を再生
        #プレーヤーのライフの数だけハートを表示する
        if not octo_cat.right_shift_pressed:  # 右シフトが押されていない場合にのみ判定
            for rope in ropes:
                #敵とぶつかった場合でも、前回ダメージを受けてから一定時間が経っていなければダメージを受けない
                if(rope.judge(octo_cat) == True) and (octo_cat.life_lost_time + 30 < time_elapsed):
                    octo_cat.life_lost_time = time_elapsed
                    octo_cat.life -= 1
                    if octo_cat.life == 0:
                        endFlag = True
            
        if octo_cat.right_shift_pressed:
            # 右シフトが押されている場合、ライフを増やす
            octo_cat.life += 1
            if octo_cat.life > 4:  # ライフが上限を超えないようにする
                octo_cat.life = 4


        if octo_cat.life == 0:
            endFlag = True
            play_game_over_music() 
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()  # ゲームオーバー時にBGMを停止

 # ゲームオーバー音楽を再生



        for i in range(octo_cat.life - 1):
            screen.blit(heart_image,(i * 30,50))
        pygame.display.update()

   
   

    quit(time_elapsed,force_quit) 
    quit(score, force_quit)


#when quitting the game
#ゲームをやめる時
def quit(score,force_quit):
    #ユーザが画面を閉じた際は、終了画面を表示せずにゲームを終了させる
    if force_quit == False:
        endFlag = False
        yourScore = "your score: " + str(score)
        #フォントとテキストの設定
        font1 = pygame.font.SysFont(None, 40)
        text1 = font1.render(yourScore, False, (255,255,255))
        font2 = pygame.font.SysFont(None, 40)
        text2 = font1.render("Press Any Key to Re-Start", False, (255,255,255))

        while endFlag == False:
            screen.fill((0,0,0))
            screen.blit(text1,(20,50))
            screen.blit(text2,(20,150))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    endFlag = True
                elif event.type == pygame.KEYDOWN:
                    #何かしらキーが押されたらゲームを再開
                    endFlag = True
                    main()
    #retrieve the highest score
    #今までのハイスコアの取得
    data = np.loadtxt("score/score.tsv",dtype="str",delimiter=",")
    highest_score = data[1]
    print("The highest score so far: " + highest_score)
    if(score > int(highest_score)):
        save_data = np.array([str(datetime.datetime.today()),str(score)])
        np.savetxt('score/score.tsv',save_data,delimiter=',', fmt="%s")
    pygame.quit()

if __name__ == "__main__":
    open()