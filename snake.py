import math,pygame,random,neat,sys,os,neat,pickle
from pygame.math import Vector2


class SNAKE:
    def __init__(self,cell_size,cell_number,screen):
        self.body=[Vector2(3,10),Vector2(2,10),Vector2(1,10)]
        self.direction=Vector2(1,0)
        self.new_block=False
        self.cell_size=cell_size
        self.cell_number=cell_number
        self.screen=screen


    
    def draw_snake(self):
        for block in self.body:
            block_rect=pygame.Rect(block.x*self.cell_size,block.y*self.cell_size,self.cell_size,self.cell_size) #(x,y,w,h)
            pygame.draw.rect(self.screen,(15,56,15),block_rect)


    def move_snake(self):
        if self.new_block==True:
            body_copy=self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]
            self.new_block=False
        else:
            body_copy=self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]

    def add_block(self):
        #print("SCOOooooooooooooooRE!!!!!!!!!!!!!!")
        self.new_block=True
    
    def reset(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(1,0)

class FRUIT:
    def __init__(self,cell_size,cell_number,screen):
        #creates the fruit position
        self.cell_size=cell_size
        self.cell_number=cell_number
        self.screen=screen
        self.randomize()
        

    def draw_fruit(self):
        fruit_rect=pygame.Rect(self.pos.x*self.cell_size,self.pos.y*self.cell_size,self.cell_size,self.cell_size) #(x,y,w,h)
        pygame.draw.ellipse(self.screen,(15,56,15),fruit_rect) #(surface,color,rect)

    def randomize(self):
            x = random.randint(0, self.cell_number - 1)
            y = random.randint(0, self.cell_number - 1)
            self.pos = Vector2(x, y)




class GAME:
    def __init__(self,genome="boy",train=True):
        self.highscore=0
        self.score_before_death=0
        self.cell_size=40
        self.cell_number=20
        self.screen=self.screen=pygame.display.set_mode((self.cell_number*self.cell_size,self.cell_number*self.cell_size)) 
        self.snake=SNAKE(self.cell_size,self.cell_number,self.screen)
        self.fruit=FRUIT(self.cell_size,self.cell_number,self.screen)
        while self.fruit.pos in self.snake.body:
            self.fruit.randomize()
        self.died=False
        self.genome=genome
        self.train=True


    def update(self):
        self.snake.move_snake() 
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass() 
        self.snake.draw_snake()
        self.draw_score()
        self.fruit.draw_fruit()
    
    def check_collision(self):
        if self.fruit.pos==self.snake.body[0]:
            self.fruit.randomize()
            while self.fruit.pos in self.snake.body:
                self.fruit.randomize()
                    

            self.snake.add_block()

    def check_fail(self):
        head=self.snake.body[0]
        if not 0<=head.x<=self.cell_number-1:
            self.score_before_death=len(self.snake.body)-3
            if len(self.snake.body)-3>self.highscore:
                self.highscore=len(self.snake.body)-3
            self.game_over()

        if not 0<=head.y<=self.cell_number-1:
            self.score_before_death=len(self.snake.body)-3
            if len(self.snake.body)-3>self.highscore:
                self.highscore=len(self.snake.body)-3
            self.game_over()

        for block in self.snake.body[1:]:
            if head==block:
                self.score_before_death=len(self.snake.body)-3
                if len(self.snake.body)-3>self.highscore:
                    self.highscore=len(self.snake.body)-3
                self.game_over()




    def draw_grass(self):
        grass_color=(150,172,15)
        for row in range(self.cell_number):
            if row%2==0:
                for column in range(self.cell_number):
                    if column%2==0:
                        grass_rect=pygame.Rect(column*self.cell_size,row*self.cell_size,self.cell_size,self.cell_size)
                        pygame.draw.rect(self.screen,grass_color,grass_rect)
            else:
                for column in range(self.cell_number):
                    if column%2!=0:
                        grass_rect=pygame.Rect(column*self.cell_size,row*self.cell_size,self.cell_size,self.cell_size)
                        pygame.draw.rect(self.screen,grass_color,grass_rect)

    def draw_score(self):
        game_font=pygame.font.Font("Font/Early GameBoy.ttf",50)
        score=len(self.snake.body)-3
        score_text=str(score)
        score_surface=game_font.render(score_text,False,(48,98,58)) #(text,anti-aliasing,color)
        if score<=99:
            x_pos=int(0+50)
            y_pos=int(0+50)
        else:
            x_pos=int(0+75)
            y_pos=int(0+75)
        score_rect=score_surface.get_rect(center=(x_pos,y_pos))
        self.screen.blit(score_surface,score_rect) #(surface,rect)
    
    def get_highscore(self):
        return self.highscore
    
    def game_over(self):
        if self.genome!="boy" or self.train==False:
            self.genome.fitness+=(len(self.snake.body)-3)*1000
        self.died=True
        self.snake.reset()

        


    def play_game(self):
        #creates the game window
        pygame.init()

        clock=pygame.time.Clock()
        


        self.screen_UPDATE=pygame.USEREVENT
        pygame.time.set_timer(self.screen_UPDATE,150) #(user event, time in ms)

        main_game=GAME()

        b=False
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #handles closing the window
                    print("HIGHSCORE= "+str(main_game.get_highscore()))
                    b=True

                
                if event.type==self.screen_UPDATE: #moves the snake
                    main_game.update()
                
                if event.type==pygame.KEYDOWN: #handles user controls
                    if (event.key==pygame.K_UP or event.key==pygame.K_w) and main_game.snake.direction.y!=1:
                        main_game.snake.direction=Vector2(0,-1)
                    if event.key==pygame.K_DOWN or event.key==pygame.K_s and main_game.snake.direction.y!=-1:
                        main_game.snake.direction=Vector2(0,1)
                    if event.key==pygame.K_LEFT or event.key==pygame.K_a and main_game.snake.direction.x!=1:
                        main_game.snake.direction=Vector2(-1,0)
                    if event.key==pygame.K_RIGHT or event.key==pygame.K_d and main_game.snake.direction.x!=-1:
                        main_game.snake.direction=Vector2(1,0)
                print(self.score_before_death)
            if b==True:
                break
            self.screen.fill((155,188,15)) #creates the color (R,G,B)
            main_game.draw_elements()
            pygame.display.update()
            clock.tick(60)
            
    
    def train_ai(self,genome,config):
        network=neat.nn.FeedForwardNetwork.create(genome,config)

        #creates the game window
        pygame.init()

        clock=pygame.time.Clock()
        


        self.screen_UPDATE=pygame.USEREVENT
        pygame.time.set_timer(self.screen_UPDATE,150) #(user event, time in ms)

        c=0
        b=False
        score=0
        total_moves=0
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #handles closing the window
                    b=True
                    break

                if event.type==self.screen_UPDATE: #moves the snake
                    self.update()

                if self.snake.body[0].y==0 or (self.snake.body[0]+Vector2(0,-1)) in self.snake.body:
                    north=-1
                elif (self.snake.body[0]+Vector2(0,-1))==self.fruit.pos:
                    north=1
                else:
                    north=0

                if self.snake.body[0].y==self.cell_number-1 or (self.snake.body[0]+Vector2(0,1)) in self.snake.body:
                    south=-1
                elif (self.snake.body[0]+Vector2(0,1))==self.fruit.pos:
                    south=1
                else:
                    south=0

                if self.snake.body[0].x==0 or (self.snake.body[0]+Vector2(-1,0)) in self.snake.body:
                    west=-1
                elif (self.snake.body[0]+Vector2(-1,0))==self.fruit.pos:
                    west=1
                else:
                    west=0

                if self.snake.body[0].x==self.cell_number-1 or (self.snake.body[0]+Vector2(1,0)) in self.snake.body:
                    east=-1
                elif (self.snake.body[0]+Vector2(1,0))==self.fruit.pos:
                    east=1
                else:
                    east=0

                
                x_distance=self.fruit.pos.x-self.snake.body[0].x
                self.genome.fitness+=(20-abs(x_distance))/20
                x_distance=math.copysign(1,x_distance)

                y_distance=self.fruit.pos.y-self.snake.body[0].y
                self.genome.fitness+=(20-abs(y_distance))/20
                y_distance=math.copysign(1,y_distance)

                output=network.activate([x_distance,y_distance,self.snake.direction.x,self.snake.direction.y,north,south,east,west]) #([snake's x distance from the fruit, snake's y distance from the fruit, direction x location, direction y location,object north,object south,object east,object west])


                decision=output.index(max(output))
                if decision==0 and self.snake.direction.y!=-1:
                        self.snake.direction=Vector2(0,1)
                if decision==1 and self.snake.direction.y!=1:
                        self.snake.direction=Vector2(0,-1)
                if decision==2 and self.snake.direction.x!=1:
                        self.snake.direction=Vector2(-1,0)
                if decision==3 and self.snake.direction.x!=-1:
                        self.snake.direction=Vector2(1,0)

                total_moves+=1
                if len(self.snake.body)-3>score:
                    c=0
                    score=len(self.snake.body)-3
                else:
                    c+=1
            if b:
                self.genome.fitness=-1000
                break     
                
                    


            self.screen.fill((155,188,15)) #creates the color (R,G,B)
            self.draw_elements()
            pygame.display.update()
            clock.tick(60)
            if self.died or c>85:
                if c>=85:
                    self.genome.fitness=-1000
                break
            
    def test_genome(self,genome,config):
        network=neat.nn.FeedForwardNetwork.create(genome,config)

        #creates the game window
        pygame.init()

        clock=pygame.time.Clock()
        


        self.screen_UPDATE=pygame.USEREVENT
        pygame.time.set_timer(self.screen_UPDATE,150) #(user event, time in ms)

        b=False
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #handles closing the window
                    sys.exit()

                if event.type==self.screen_UPDATE: #moves the snake
                    self.update()
                
                if self.snake.body[0].y==0 or (self.snake.body[0]+Vector2(0,-1)) in self.snake.body:
                    north=-1
                elif (self.snake.body[0]+Vector2(0,-1))==self.fruit.pos:
                    north=1
                else:
                    north=0

                if self.snake.body[0].y==self.cell_number-1 or (self.snake.body[0]+Vector2(0,1)) in self.snake.body:
                    south=-1
                elif (self.snake.body[0]+Vector2(0,1))==self.fruit.pos:
                    south=1
                else:
                    south=0

                if self.snake.body[0].x==0 or (self.snake.body[0]+Vector2(-1,0)) in self.snake.body:
                    west=-1
                elif (self.snake.body[0]+Vector2(-1,0))==self.fruit.pos:
                    west=1
                else:
                    west=0

                if self.snake.body[0].x==self.cell_number-1 or (self.snake.body[0]+Vector2(1,0)) in self.snake.body:
                    east=-1
                elif (self.snake.body[0]+Vector2(1,0))==self.fruit.pos:
                    east=1
                else:
                    east=0

                
                x_distance=self.fruit.pos.x-self.snake.body[0].x
                x_distance=math.copysign(1,x_distance)

                y_distance=self.fruit.pos.y-self.snake.body[0].y
                y_distance=math.copysign(1,y_distance)

                output=network.activate([x_distance,y_distance,self.snake.direction.x,self.snake.direction.y,north,south,east,west]) #([snake's x distance from the fruit, snake's y distance from the fruit, direction x location, direction y location,object north,object south,object east,object west])


                decision=output.index(max(output))
                if decision==0 and self.snake.direction.y!=-1:
                        self.snake.direction=Vector2(0,1)
                if decision==1 and self.snake.direction.y!=1:
                        self.snake.direction=Vector2(0,-1)
                if decision==2 and self.snake.direction.x!=1:
                        self.snake.direction=Vector2(-1,0)
                if decision==3 and self.snake.direction.x!=-1:
                        self.snake.direction=Vector2(1,0)

                if self.died:
                    self.fruit.randomize()
                    self.died=False

                
                    


            self.screen.fill((155,188,15)) #creates the color (R,G,B)
            self.draw_elements()
            pygame.display.update()
            clock.tick(60)


    def calculate_fitness(self,genome):
        self.genome.fitness+=self.score_before_death














