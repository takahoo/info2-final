import pyxel

monsterlist = []
firelist = []

class Monster:
    def __init__(self):
        self.x = pyxel.rndi(1, 99)
        self.y = -10
        self.speed = 1
        self.alive = True
        self.random_number = pyxel.rndi(0, 1)
        self.type = self.random_number

    def update(self):
        self.y += 1 * self.speed
        if self.y > 400:
            self.alive = False

    def draw(self):
        if self.alive:
            if self.type == 0:
                pyxel.blt(self.x, self.y, 0, 2, 1, 9, 9, 0)
            elif self.type == 1:
                pyxel.blt(self.x, self.y, 0, 17, 2, 9, 9, 0)

class Packman:
    def __init__(self):
        self.x = 100
        self.y = 180
        self.w = 40
        self.h = 5
        self.type = 0
        self.firecatch = False

    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
            
        if self.x > 100: #if it goes outside of the screen
            self.x = 0
        elif self.x < 0:
            self.x = 100

    def draw(self):
        if self.type == 0:
            pyxel.blt(self.x, self.y, 0, 8, 24, 14, 14, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 24, 25, -14, 14, 0)

class Fire:
    def __init__(self):
        self.x = pyxel.rndi(1, 99)
        self.y = -10
        self.speed = 1
        self.alive = True

    def update(self):
        self.y += 1 * self.speed
        if self.y > 400:
            self.alive = False

    def draw(self):
        if self.alive:
            pyxel.blt(self.x, self.y, 0, 34, 2, 11, 10, 0)

class App:
    def __init__(self):
        pyxel.init(100, 200)
        pyxel.load("monster.pyxres")
        self.packman = Packman()
        self.score = 0
        self.start_button_region = (30, 80, 70, 100)  # Adjust the region for your "START" text
        self.gameover = False
        self.gameend = False
        self.state = "START"
        pyxel.play(0, 0, loop=True)
        pyxel.mouse(True)  # Enable mouse input
        pyxel.run(self.update, self.draw)
        pyxel.mouse(True)

    def update(self):
        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and (
            self.start_button_region[0] < mouse_x < self.start_button_region[2]
            and self.start_button_region[1] < mouse_y < self.start_button_region[3]
        ):
            self.state = "GAME"

        if self.state == "GAME" and not self.gameend and not self.gameover:
            if self.score < 0:
                self.gameover = True

            if self.score >= 10:
                self.gameend = True

            monstercatch = False

            if pyxel.frame_count % 25 == 0:
                monsterlist.append(Monster())

            if pyxel.frame_count % 35 == 0:
                firelist.append(Fire())

            for elm in monsterlist:
                elm.update()

            monstercatch == False

            for elm in firelist:
                elm.update()

            self.packman.update()

            for monster in monsterlist:
                if (
                    monster.y >= self.packman.y
                    and self.packman.x < monster.x + 4 < self.packman.x + 10
                    and monster.alive
                ):
                    monster.alive = False
                    self.score += 1

            for fire in firelist:
                if (
                    fire.y >= self.packman.y
                    and self.packman.x < fire.x + 4 < self.packman.x + 10
                    and fire.alive
                ):
                    fire.alive = False
                    self.score -= 1

    def draw(self):
        pyxel.cls(0)
        if self.state == "START":
            self.draw_start()
        elif self.state == "GAME":
            self.draw_game()

    def draw_start(self):
        pyxel.text(30, 80, "START", pyxel.frame_count % 16)

    def draw_game(self):
        if self.gameover:
            pyxel.text(10, 60, "GAME OVER!", pyxel.frame_count % 16)

        if self.gameend:
            pyxel.text(10, 60, "COMPLETED!", pyxel.frame_count % 16)

        pyxel.text(1, 2, "score:" + str(self.score), pyxel.frame_count % 16)

        for elm in monsterlist:
            elm.draw()

        for elm in firelist:
            elm.draw()

        self.packman.draw()

App()
