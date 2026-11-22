import pygame
from pytmx.util_pygame import load_pygame
import pytmx
pygame.init()
screen = pygame.display.set_mode((480,320),pygame.SCALED | pygame.FULLSCREEN)
runing = True
hero = pygame.image.load('assets/geroy.png').convert_alpha()
tmx_data = load_pygame("assets/map.tmx")
click = pygame.time.Clock()
hero_x = 256
hero_y = 480
speed = 2
again = pygame.Rect(170,160,140,30)
quit = pygame.Rect(170,200,140,30)
xz_text = ""
rules = [
    "You are stranded on an island.",
    "Goal: build a raft and sail away!",
    "",
    "WASD - move",
    "E - collect wood or stone",
    "C - craft a tool (1 wood + 2 stone)",
    "F - build a raft at the sign",
    "    (tool + 2 wood + 3 stone)",
    "Space - get on the raft",
    "Esc - quit the game",
]
back = pygame.Rect(170,270,140,30)

timer = 0
menu_button = ["Play" ,"How to play" ,"Exit" ]
overlay = pygame.Surface((480,320) , pygame.SRCALPHA )
overlay.fill((0,0,0,120))
walk1 = pygame.image.load('assets/geroy_walk1.png').convert_alpha()
walk2 = pygame.image.load('assets/geroy_walk2.png').convert_alpha()
walk_run = [hero,walk1,hero,walk2]
plot = pygame.image.load('assets/New Piskel-12.png').convert_alpha()
plot_x = 18 *32
plot_y = 17 * 32
seet_on_plot = False

buttons = [
    pygame.Rect(170,120,140,30),
    pygame.Rect(170,160,140,30),
    pygame.Rect(170,200,140,30),
]


anim_timer = 0
def id_solid(px, py):
    cx = int(px // 32)
    cy = int(py // 32)
    if cx < 0 or cy < 0 or cx >= 30 or cy >= 20:
        return True
    for index in range(len(tmx_data.layers)):
        pro = tmx_data.get_tile_properties(cx, cy, index)
        if pro is not None and pro.get("solid"):
            return True
    return False

zone = pygame.Rect(plot_x, plot_y - 32, 64, 96)
font = pygame.font.SysFont('arial', 16)
wood = 0
stone = 0
tools = False
plot_yes = False
def try_colect():
    hx = int((hero_x +16) // 32)
    hy = int((hero_y +28) // 32)
    for dx,dy in[(1,0) , (0,1) ,(0,-1) ,(-1,0)]:
        cx = hx + dx
        cy = hy + dy
        for a in range(len(tmx_data.layers)):
            pro = tmx_data.get_tile_properties(cx, cy, a)
            if pro is not None and pro.get("resource"):
                tmx_data.layers[a].data[cy][cx] = 0
                return pro.get("resource")
    return None
def table():
    hx = int((hero_x +16) // 32)
    hy = int((hero_y +28) // 32)
    for dx,dy in[(1,0) , (0,1) ,(0,-1) ,(-1,0)]:
        cx = hx + dx
        cy = hy + dy
        for a in range(len(tmx_data.layers)):
            pro = tmx_data.get_tile_properties(cx, cy, a)
            if pro is not None and pro.get("table"):
                return True
state = "menu"
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if state == "play" and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            r = try_colect()
            if r == "wood":
                wood += 1
            if r == "stone":
                stone += 1
        if  state == "play" and event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            if not tools and wood >= 1 and stone >= 2:
                wood -= 1
                stone -= 2
                tools = True
        if  state == "play" and event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if not table():
                continue
            else:
                if not plot_yes:
                    if not tools:
                        xz_text = "no tools"
                        timer = 120
                    elif wood < 2:
                        xz_text = "no wood"
                        timer = 120
                    elif stone < 3:
                        xz_text = "no stone"
                        timer = 120
                    else:
                        plot_yes = True
                        stone -= 3
                        wood -= 2
                        xz_text = "build plot"

        if state == "play" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if plot_yes:
                if not seet_on_plot and zone.collidepoint(hero_x + 16, hero_y + 28):
                    seet_on_plot = True
                    hero_x = plot_x + 16
                    hero_y = plot_y + 8
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            runing = False
        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if buttons[0].collidepoint(event.pos):
                state = "play"
            if buttons[1].collidepoint(event.pos):
                state = "how_to"
            if buttons[2].collidepoint(event.pos):
                runing = False
        if state == "how_to" and event.type == pygame.MOUSEBUTTONDOWN:
            if back.collidepoint(event.pos):
                state = "menu"
        if state =="win" and event.type == pygame.MOUSEBUTTONDOWN:
            if again.collidepoint(event.pos):
                tmx_data = load_pygame("assets/map.tmx")
                hero_x = 256
                hero_y = 480
                wood = 0
                stone = 0
                tools = False
                plot_yes = False
                seet_on_plot = False
                plot_x = 18 * 32
                plot_y = 17 * 32
                xz_text = ""
                timer = 0
                anim_timer = 0
                state = "play"
            if quit.collidepoint(event.pos):
                runing = False
    if state == "play":
        keys = pygame.key.get_pressed()
        if timer > 0:
            timer -= 1
        if not seet_on_plot:
            new_x = hero_x
            new_y = hero_y
            if keys[pygame.K_w]:
                new_y -= speed
            if keys[pygame.K_s]:
                new_y += speed
            if keys[pygame.K_a]:
                new_x -= speed
            if keys[pygame.K_d]:
                new_x += speed
            if not id_solid(new_x + 16 ,new_y + 28):
                hero_x = new_x
                hero_y = new_y

        if seet_on_plot:
            plot_y += 1
            hero_y = plot_y + 8
            if plot_y > 640:
                state = "win"

        mowing = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]
        if mowing:
            anim_timer += 1
            current = walk_run[(anim_timer // 8)  % 4]
        else:
            anim_timer = 0
            current = hero


        cam_x = hero_x + 16 -240
        cam_y = hero_y + 16 -160
        cam_x = max(0,min(cam_x,480))
        cam_y = max(0,min(cam_y,320))
        screen.fill((54, 191, 196))
        for i in tmx_data.visible_layers:
            if isinstance(i,pytmx.TiledTileLayer):
                for x,y,j in i.tiles():
                    screen.blit(j, (x*32-cam_x,y*32-cam_y))

        if tools:
            f = "Yes"
        else:
            f = "No"
        if plot_yes:
            screen.blit(plot,(plot_x-cam_x,plot_y-cam_y))
        screen.blit(current, (hero_x - cam_x, hero_y - cam_y))
        text = font.render(f"Wood: {wood}; Stone: {stone}; Tools {f}", True, (255,255,255))
        screen.blit(text, (8, 8))


        if timer > 0:
            msg = font.render(xz_text, True, (255,255,255))
            screen.blit(msg, (8,20))
    elif state == "menu":
        for i in tmx_data.visible_layers:
            if isinstance(i,pytmx.TiledTileLayer):
                for x,y,j in i.tiles():
                    screen.blit(j, (x*32 - 240, y*32 - 160))
        screen.blit(overlay, (0, 0))
        title= font.render("Survival on island", True, (255,255,255))
        screen.blit(title, (170, 70))
        mouse = pygame.mouse.get_pos()
        if buttons[0].collidepoint(mouse):
            color = [255,220,0]
        else:
            color = [255,255,255]
        pygame.draw.rect(screen,(40,80,110),buttons[0])
        label = font.render("Play" ,True,color)
        screen.blit(label, (buttons[0].x+10, buttons[0].y+6))

        if buttons[1].collidepoint(mouse):
            color = [255,220,0]
        else:
            color = [255,255,255]
        pygame.draw.rect(screen,(40,80,110),buttons[1])
        label = font.render("How to play" ,True,color)
        screen.blit(label, (buttons[1].x+10, buttons[1].y+6))

        if buttons[2].collidepoint(mouse):
            color = [255,220,0]
        else:
            color = [255,255,255]
        pygame.draw.rect(screen,(40,80,110),buttons[2])
        label = font.render("exit" ,True,color)
        screen.blit(label, (buttons[2].x+10, buttons[2].y+6))

    elif state == "how_to":
        screen.fill((20,40,60))
        y = 30
        for i in rules:
            t = font.render(i,True,(255,255,255))
            screen.blit(t,(30,y))
            y += 22



        pygame.draw.rect(screen,(40,80,110),back)
        label = font.render("Back" ,True,(255,255,255))
        screen.blit(label,(back.x+ 10, back.y+6))
    elif state == "win":
        screen.fill((20,40,60))

        title = font.render("You win!" ,True,(255,255,255))
        screen.blit(title,(150,90))

        pygame.draw.rect(screen,(40,80,110),again)
        label = font.render("Play again" ,True,(255,255,255))
        screen.blit(label,(again.x+ 10, again.y+6))

        pygame.draw.rect(screen,(40,80,110),quit)

        label = font.render("Exit",True,(255,255,255))
        screen.blit(label,(quit.x+ 10, quit.y+6))




    click.tick(60)
    pygame.display.flip()

pygame.quit()