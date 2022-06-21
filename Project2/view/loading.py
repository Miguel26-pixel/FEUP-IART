import pygame, sys, threading


def doWork(WORK):
	# Do some math WORK amount times
	global loading_finished, loading_progress

	for i in range(WORK):
		math_equation = 523687 / 789456 * 89456
		loading_progress = i 

	loading_finished = True

def loading_screen(screen, screen_width, screen_height, CLOCK):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        FONT = pygame.font.SysFont("Bangers", 100)
        finished = FONT.render("Done! Let's START!", True, "white")
        finished_rect = finished.get_rect(center=(screen_width//2,screen_height//2))
        
        ship = pygame.image.load("./view/black.jpg")
        ship = pygame.transform.scale(ship,(screen_width,screen_height))
        ship_top = screen.get_height() - ship.get_height()
        ship_left = screen.get_width()/2 - ship.get_width()/2

        screen.blit(ship, (ship_top,ship_left))

        WORK = 1000

        LOADING_BG = pygame.image.load("./view/Loading Bar Background.png")
        LOADING_BG_RECT = LOADING_BG.get_rect(center=(screen_width//2, screen_height//2))


        loading_bar = pygame.image.load("./view/Loading Bar.png")
        loading_bar_rect = loading_bar.get_rect(midleft=(400, 300))
        loading_finished = False
        loading_progress = 0
        loading_bar_width = 8

        # Thread
        threading.Thread(target=doWork(WORK)).start()

        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill("#0d0e2e")

            if not loading_finished:
                loading_bar_width = loading_progress / WORK * 720

                loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 150))
                loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))

                screen.blit(LOADING_BG, LOADING_BG_RECT)
                screen.blit(loading_bar, loading_bar_rect)
            else:
                screen.blit(finished, finished_rect)


            pygame.display.update()
            CLOCK.tick(60)





