import os
import time
import threading
import pygame

OPEN_EYED_CAT = [" /\\_/\\ ",
                 "( o.o )",
                 ">     <"]
CLOSED_EYED_CAT = [" /\\_/\\ ",
                   "( -.- )",
                   ">     <"]
SLEEPING_CAT = [" /\\_/\\ ",
                "( -.- )  zzz...",
                ">     <"]

work_timer_done_event = threading.Event()
break_timer_done_event = threading.Event()

task = ""

last_music_index = 0

def create_speech_bubble(cat, task):
    if len(task) > 10:
        task = task[:10] + '...'
    padding_left = (len(cat[2]) - len(task) - 4) // 2
    padding_right = len(cat[2]) - len(task) - 4 - padding_left
    cat[2] = ">" + " " * padding_left + "[" + task + "]" + " " * padding_right + "<"
    return cat

def start_timer(duration, break_duration):
    global work_timer_done_event
    global break_timer_done_event

    while True:
        pygame.mixer.music.load('ding.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1.0)
        time.sleep(duration)
        work_timer_done_event.set()
        pygame.mixer.music.load('ding.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1.0)
        time.sleep(1)
        pygame.mixer.music.stop()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(SLEEPING_CAT))
        time.sleep(1)
        pygame.mixer.music.load('ding.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1.0)
        time.sleep(break_duration)
        break_timer_done_event.set()
        pygame.mixer.music.stop()
        pygame.mixer.music.rewind()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(OPEN_EYED_CAT))
        time.sleep(1)
        work_timer_done_event.clear()
        break_timer_done_event.clear()

def set_task():
    global task
    task = input("What is your focus task? ")
    print("You are now working on: ", task)
    return task

def play_music(directory):
    global last_music_index
    global music_files

    while True:
        if not pygame.mixer.music.get_busy() and not work_timer_done_event.is_set():
            pygame.mixer.music.load(os.path.join(directory, music_files[last_music_index]))
            pygame.mixer.music.play()
            last_music_index = (last_music_index + 1) % len(music_files)

        elif work_timer_done_event.is_set():
            pygame.mixer.music.stop()

        time.sleep(1)

def animate_cat():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if work_timer_done_event.is_set() and not break_timer_done_event.is_set():
            print("\n".join(SLEEPING_CAT))
            time.sleep(5)
        else:
            print("\n".join(create_speech_bubble(OPEN_EYED_CAT.copy(), task)))
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n".join(create_speech_bubble(CLOSED_EYED_CAT.copy(), task)))
            time.sleep(1)

if __name__ == "__main__":
    work_time = input("Set your focus time (in minutes): ")
    work_time = int(work_time)
    break_time = input("Set your break time (in minutes): ")
    break_time = int(break_time)
    set_task()

    pygame.mixer.init()
    music_files = [f for f in os.listdir('lofimusic') if f.endswith('.mp3')]
    music_files.sort()

    pygame.mixer.music.load('ding.mp3')
    pygame.mixer.music.set_volume(1.0)
    while True:
        timer_thread = threading.Thread(target=start_timer, args=(work_time * 60, break_time * 60,))
        timer_thread.start()

        music_thread = threading.Thread(target=play_music, args=('lofimusic',))
        music_thread.start()

        animate_cat_thread = threading.Thread(target=animate_cat)
        animate_cat_thread.start()

        timer_thread.join()
        music_thread.join()
        animate_cat_thread.join()
