import pygame
import random
import copy
import time

game_grid = []
click_grid = []
score = 0
selector = 1
select1 = None
select2 = None
check = False
missed = 0
end = False

def main():
    global game_grid, click_grid, selector, select1, select2, check, score, end
    pygame.init()
    pygame.font.init()

    res = (1280, 720)

    screen = pygame.display.set_mode((res))
    pygame.display.set_caption('Matching Game')

    watpng = pygame.image.load("wat.png")
    shufflepng = pygame.image.load("shuffle.png")

    runmenu = True
    rungame = False

    rows = 0
    columns = 0

    

    red = (255,0,0)
    pink = (255,200,200)
    darkGreen = (0,128,0)
    green = (0, 255, 0)
    darkBlue = (0,0,15)
    yellow = (255, 255, 0)
    purple = (128, 0, 128)
    orange = (255, 165, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)

    class Text():
        def draw(self, win, text, textsize,textcolor, x, y):
            self.text = text
            self.textsize = textsize
            self.textcolor = textcolor
            self.x = x
            self.y = y
            font = pygame.font.SysFont("Tahoma", self.textsize)
            text = font.render (self.text, 1, self.textcolor)
            win.blit(text, (self.x, self.y))

    class Button():
        def __init__(self, color, x, y, width, height, text, textcolor, textsize):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.textcolor = textcolor
            self.textsize = textsize

        def draw(self, win):
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 2)

            if self.text != None:
                font = pygame.font.SysFont("Tahoma", self.textsize)
                text = font.render (self.text, 1, self.textcolor)
                win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    class Card():
        def __init__(self, color, shape, shape_color):
            self.color = color
            self.shape = shape
            self.shape_color = shape_color

        def draw(self, win,x , y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
            if self.shape == "quad": 
                self.shape_width = int(self.width/2)
                self.shape_height = int(self.width/2)
                self.shape_x = self.x + int(self.shape_width/2)
                self.shape_y = self.y + int(self.height/2 - int(self.shape_height/2))
                pygame.draw.rect(win, self.shape_color, (self.shape_x, self.shape_y, self.shape_width, self.shape_height))
            elif self.shape == "circle":
                self.shape_x = self.x + int(self.width/2)
                self.shape_y = self.y + int(self.height/2)
                pygame.draw.circle(win, self.shape_color, (self.shape_x, self.shape_y), int(self.width/4))
            elif self.shape == "triangle":
                pygame.draw.polygon(win , self.shape_color , [(self.x + int(self.width/2), (self.y + int(self.height/2)) - int(self.height/4))  , (self.x + int(self.width/4), self.y + int(self.height/2) + int(self.width/4)) , (self.x + self.width - int(self.width/4), self.y + int(self.height/2) + int(self.width/4))])
        
    scoretext = Text()

    B4x3 = Button(yellow, res[0]/2 - 75, res[1]/2, 150, 50, "4X3", yellow, 20)
    B4x4 = Button(yellow, res[0]/2 - 75, res[1]/2 +60, 150, 50, "4X4", yellow, 20)
    B5x4 = Button(yellow, res[0]/2 - 75, res[1]/2 + 120, 150, 50, "5x4", yellow, 20)
    B6x5 = Button(yellow, res[0]/2 - 75, res[1]/2 + 180, 150, 50, "6x5", yellow, 20)
    B6x6 = Button(yellow, res[0]/2 - 75, res[1]/2 + 240, 150, 50, "6x6", yellow, 20)
    Bexitmenu = Button(yellow, res[0]/2 - 75, res[1]/2 + 300, 150, 50, "Exit", yellow, 20)
    Bexitgame = Button(yellow, 10, res[1] - 60, 150, 50, "Exit", yellow, 20)
    Bexitend = Button(yellow, 10, res[1] - 60, 150, 50, "Exit", yellow, 20)
    
    c1 = Card(darkBlue, "quad", red)
    c2 = Card(darkBlue, "quad", pink)
    c3 = Card(darkBlue, "quad", darkGreen)
    c4 = Card(darkBlue, "quad", yellow)
    c5 = Card(darkBlue, "quad", purple)
    c6 = Card(darkBlue, "quad", orange)
    c7 = Card(darkBlue, "circle", red)
    c8 = Card(darkBlue, "circle", pink)
    c9 = Card(darkBlue, "circle", darkGreen)
    c10 = Card(darkBlue, "circle", yellow)
    c11 = Card(darkBlue, "circle", purple)
    c12 = Card(darkBlue, "circle", orange)
    c13 = Card(darkBlue, "triangle", red)
    c14 = Card(darkBlue, "triangle", pink)
    c15 = Card(darkBlue, "triangle", darkGreen)
    c16 = Card(darkBlue, "triangle", yellow)
    c17 = Card(darkBlue, "triangle", purple)
    c18 = Card(darkBlue, "triangle", orange)

    def game_gen():
        global game_grid, click_grid
        game_grid = []
        click_grid = []
        game_cards = []
        cards = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18]
        random.shuffle(cards)
        for x in range(int(rows*columns/2)):
            game_cards.append(cards.pop())            
            game_cards.append(copy.deepcopy(game_cards[-1]))
        random.shuffle(game_cards)
        for x in range(rows):
            aux_list = []
            click_grid.append([])
            for y in range(columns):
                aux_list.append(game_cards.pop())
                click_grid[x].append(0)
            game_grid.append(aux_list)

    def match_check():
        global select1, select2, check, score, end
        if game_grid[select1[0]][select1[1]] != None and game_grid[select2[0]][select2[1]] != None:
            if select1 != select2:
                if game_grid[select1[0]][select1[1]].shape == game_grid[select2[0]][select2[1]].shape:
                    if game_grid[select1[0]][select1[1]].shape_color == game_grid[select2[0]][select2[1]].shape_color:
                        game_grid[select1[0]][select1[1]] = None
                        game_grid[select2[0]][select2[1]] = None
                        score += 100
                        check = False
                    else:
                        mismatched()
                else:
                    mismatched()
            else:
                mismatched()
        else:
            mismatched()
        if score < 0:
            score = 0
        end = True
        for x in range(rows):
            for y in range(columns):
                if click_grid[x][y] == 0:
                    end = False

        pygame.display.flip()
        time.sleep(0.5)

    def mismatched():
        global click_grid, select1, select2, score, missed, check
        click_grid[select1[0]][select1[1]] = 0
        click_grid[select2[0]][select2[1]] = 0
        score -= missed * 20
        missed += 1
        check = False

    while runmenu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runmenu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    runmenu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if B4x3.x < pos[0] < (B4x3.x + B4x3.width):
                    if B4x3.y < pos[1] < (B4x3.y + B4x3.height):
                        rows = 3
                        columns = 4
                        game_gen()
                        rungame = True
                        
                if B4x4.x < pos[0] < (B4x4.x + B4x4.width):
                    if B4x4.y < pos[1] < (B4x4.y + B4x4.height):
                        rows = 4
                        columns = 4
                        game_gen()
                        rungame = True
                        
                if B5x4.x < pos[0] < (B5x4.x + B5x4.width):
                    if B5x4.y < pos[1] < (B5x4.y + B5x4.height):
                        rows = 4
                        columns = 5
                        game_gen()
                        rungame = True
                        
                if B6x5.x < pos[0] < (B6x5.x + B6x5.width):
                    if B6x5.y < pos[1] < (B6x5.y + B6x5.height):
                        rows = 5
                        columns = 6
                        game_gen()
                        rungame = True

                if B6x6.x < pos[0] < (B6x6.x + B6x6.width):
                    if B6x6.y < pos[1] < (B6x6.y + B6x6.height):
                        rows = 6
                        columns = 6
                        game_gen()
                        rungame = True

                if Bexitmenu.x < pos[0] < (Bexitmenu.x + Bexitmenu.width):
                    if Bexitmenu.y < pos[1] < (Bexitmenu.y + Bexitmenu.height):
                        runmenu = False
                
        screen.fill(darkBlue)
        mbuttons = (B4x3, B4x4, B5x4, B6x5, B6x6, Bexitmenu)
        for button in mbuttons:
            button.draw(screen)
        
        screen.blit(shufflepng, (240, 0))

        pygame.display.flip()
        
        while rungame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rungame = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rungame = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if Bexitgame.x < pos[0] < (Bexitgame.x + Bexitgame.width):
                        if Bexitgame.y < pos[1] < (Bexitgame.y + Bexitgame.height):
                            score = 0
                            rungame = False
                    for i in range(rows):
                        for j in range(columns):
                            if game_grid[i][j] == None:
                                continue
                            else:
                                if game_grid[i][j].x < pos[0] < game_grid[i][j].x + game_grid[i][j].width:
                                    if game_grid[i][j].y < pos[1] < game_grid[i][j].y + game_grid[i][j].height:
                                        click_grid[i][j] = 1
                                        if selector == 1:
                                            select1 = (i, j)
                                            selector = 2
                                        elif selector == 2:
                                            select2 = (i, j)
                                            selector = 1
                                            check = True
                                        else:
                                            continue
                                            


            screen.fill(darkBlue)
            Bexitgame.draw(screen)
            scoretext.draw(screen, "Score: {}".format(score), 20, white, 10, 10)

            for x in range(rows):
                for y in range(columns):
                    if game_grid[x][y] == None:
                        continue
                    else:
                        game_grid[x][y].draw(screen, 340 + int(600/columns) * y + 10 * y, int(120/(rows+1)) + int(600/rows) * x + int(120/(rows+1)) * x, int(600/columns), int(600/rows))
                    if click_grid[x][y] == 0:
                        pygame.draw.rect(screen, green, (game_grid[x][y].x, game_grid[x][y].y, game_grid[x][y].width, game_grid[x][y].height), 0)
            
            if check:
                match_check()


            pygame.display.flip()

            while end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = False
                        rungame = False
                        score = 0
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            end = False
                            rungame = False
                            score = 0
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if Bexitend.x < pos[0] < (Bexitgame.x + Bexitgame.width):
                            if Bexitgame.y < pos[1] < (Bexitgame.y + Bexitgame.height):
                                end = False
                                rungame = False
                                score = 0
                
                screen.fill(darkBlue)
                screen.blit(watpng, (340, 50))
                scoretext.draw(screen, "Score: {}".format(score), 48, white, 340, 500)
                Bexitend.draw(screen)
                pygame.display.flip()

main()
