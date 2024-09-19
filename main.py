import pygame
import random
import math
import numpy as np

pygame.init()

def play_tone(frequency, duration, sample_rate=44100):
    pygame.mixer.init(frequency=sample_rate)
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Generate sine wave
    tone = np.sin(frequency * t * 2 * np.pi)
    # Ensure that highest value is in 16-bit range
    audio = (tone * (2**15 - 1)).astype(np.int16)
    # Convert to bytes
    audio = audio.tobytes()
    # Create sound object
    sound = pygame.mixer.Sound(buffer=audio)
    # Play sound
    sound.play()
    # pygame.time.delay(int(duration * 1000))  # Wait for the sound to finish

def freq(x):
    return x*25

class GameInfo:
    BLACK = 30, 3, 66
    WHITE = 225, 247, 245
    GREEN = 15, 255, 80
    RED = 227, 11, 92
    GREY = 169, 169, 169
    NAVY = 30, 3, 66
    BLUE = 14, 70, 163
    TEAL = 154, 200, 205

    GRADIENTS = [NAVY,BLUE,TEAL]

    BACKGROUND_COLOR = WHITE
    SIDE_PAD = 100
    TOP_PAD = 150

    FONT  =pygame.font.Font('freesansbold.ttf',20);
    LARGE_FONT = pygame.font.Font('freesansbold.ttf',25)




    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Sorting Visualizer")

        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        self.start_x = self.SIDE_PAD // 2


def draw(draw_info,algo_name,ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                          draw_info.GREEN)
    draw_info.window.blit(title, ((draw_info.width - title.get_width()) // 2, 5))

    controls =  draw_info.FONT.render("R -RESET | SPACE - Sorting | A-Ascending | D-Descending ",1,draw_info.BLACK)
    draw_info.window.blit(controls,((draw_info.width-controls.get_width())//2,45))

    sorting = draw_info.FONT.render("I - INSERTION SORT | B - BUBBLE SORT | S - SELECTION SORT",1,draw_info.GREY)
    draw_info.window.blit(sorting,((draw_info.width-sorting.get_width())//2,75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={},clear_bg=False):

    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2,draw_info.TOP_PAD,draw_info.width-draw_info.SIDE_PAD,draw_info.height-draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR,clear_rect)


    for i,val in enumerate(lst):
        x = draw_info.start_x + i*draw_info.block_width
        y = draw_info.height - (val-draw_info.min_val)*draw_info.block_height
        color  = draw_info.GRADIENTS[i%3]

        if i in color_positions:
            color =color_positions[i]

        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height))
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info,ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range (len(lst)-i-1):
            val1 , val2 = lst[j] , lst[j+1]

            if (val1>val2 and ascending) or (val1<val2 and not ascending):
                lst[j],lst[j+1] =lst[j+1],lst[j]
                play_tone(lst[j] * 200, 0.05)
                play_tone(lst[j+1] * 200, 0.05)
                draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED},True)
                yield True


def insertion_sort(draw_info,ascending =True):
    lst = draw_info.lst

    for i in range(1,len(lst)):
        cur = lst[i]
        while True:
            ascending_sort = i>0 and lst[i-1] >cur  and ascending
            descending_sort= i>0 and lst[i-1]<cur and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i]=lst[i-1]
            i-=1
            lst[i] =cur
            play_tone(freq(lst[i]), 0.1)
            play_tone(freq(lst[i+1]) , 0.1)
            draw_list(draw_info,{i:draw_info.GREEN,i+1:draw_info.RED},True)
            yield True


    return lst

def selection_sort(draw_info,ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        mini = i
        for j in range(i+1,len(lst)):
            if (ascending and lst[mini]>lst[j]) or (not ascending and lst[mini]<lst[j]):
                prev =mini
                mini = j
                play_tone(lst[prev]+200,0.1)
                play_tone(lst[mini]+200,0.1)
                draw_list(draw_info, {prev:draw_info.RED,mini:draw_info.GREEN},True)
                yield True

        lst[i],lst[mini] =lst[mini],lst[i]
        play_tone(lst[i] + 200, 0.1)
        play_tone(lst[mini] + 200, 0.1)
        draw_list(draw_info,{i:draw_info.GREEN,mini:draw_info.RED},True)
        yield True

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n=100
    min_val =1;max_val=100
    lst =generate_starting_list(n,min_val,max_val)
    draw_info = GameInfo(800,600,lst)
    sorting = False
    ascending = True

    sorting_algorithm = selection_sort
    sorting_algo_name = "Selection Sort"
    sorting_algorithm_generator = None


    while run:
        # clock.tick(60)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting =False

        else:
            draw(draw_info,sorting_algo_name,ascending)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst =generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
                # sorting =False
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending =False
            elif event.key == pygame.K_i:
                sorting_algorithm =insertion_sort
                sorting_algo_name ="Insertion Sort"
                sorting_algorithm_generator = None
            elif event.key == pygame.K_b:
                sorting_algorithm =bubble_sort
                sorting_algo_name ="Bubble Sort"
                sorting_algorithm_generator =None
            elif event.key == pygame.K_s:
                sorting_algorithm =selection_sort
                sorting_algo_name ="Selection Sort"
                sorting_algorithm_generator =None

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()


'''
color pallete

https://colorhunt.co/palette/1e03420e46a39ac8cde1f7f5

'''