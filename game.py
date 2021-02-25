import pygame, sys, random
import agent as ag
import main as m


class Game:

    def __init__(self, type):

        self.gameType = int(type)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.roundIsDone = False
        # screen settings
        self.screen_width = 1280
        self.screen_height = 820

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption("Pong " + str(self.gameType))

        alpha = 0.5
        gamma = 0.9
        epsilon = 0.01


        # game objects
        self.ball = pygame.Rect(self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_width - 10, self.screen_height / 2 - 70, 10, 140)
        self.opponent = pygame.Rect(10, self.screen_height / 2 - 70, 10, 140)

        # permanent RL agent
        self.agent = ag.Qlearning(alpha, gamma, epsilon, 820, 140)
        # agent's side :
        self.AgentControl = self.opponent
        if self.gameType == 3:
            # sedondary agent for RL vs RL
            self.agent2 = ag.Qlearning(alpha, gamma, epsilon, 820, 140)
            self.OtherAgentControl = self.player


        self.bg_color = pygame.Color("grey12")
        self.light_grey = (200, 200, 200)

        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = 7 * random.choice((1, -1))

        if self.gameType == 1:
            self.player_speed = 0
            self.opponent_speed = 0
        if self.gameType == 2:
            self.player_speed = 0
            self.opponent_speed = 7
        if self.gameType == 3:
            self.player_speed = 0
            self.opponent_speed = 0

        # text variables
        self.player_score = 0
        self.opponent_score = 0

        self.game_font = pygame.font.Font("freesansbold.ttf", 32)

    def ball_animation(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.ball_speed_y *= -1
        if self.ball.left <= 0 or self.ball.right >= self.screen_width:
            if self.ball.left <= 0:
                self.player_score += 1
            if self.ball.right >= self.screen_width:
                self.opponent_score += 1
            self.ball_restart()
            self.roundIsDone = True

        # Collison
        if self.ball.colliderect(self.player) or self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1

    def player_animation(self):
        self.player.y += self.player_speed
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

    def opponent_ai(self):
        if self.opponent.top < self.ball.y:
            self.opponent.top += self.opponent_speed

        if self.opponent.bottom > self.ball.y:
            self.opponent.top -= self.opponent_speed

        if self.opponent.top <= 0:
            self.opponent.top = 0

        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom -= self.screen_height

    def ball_restart(self):
        self.ball.center = (self.screen_width / 2, self.screen_height / 2)
        self.ball_speed_y *= random.choice((1, -1))
        self.ball_speed_y *= random.choice((1, -1))

    def play(self, episodes):
        # game loop
        episode = 0
        while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        m.plot_agent_reward(self.agent.rewards)
                        pygame.quit()
                        sys.exit()

                    if self.gameType == 1:
                        # keys event down and up
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_DOWN:
                                self.player_speed += 6
                            if event.key == pygame.K_UP:
                                self.player_speed -= 6

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_DOWN:
                                self.player_speed -= 6
                            if event.key == pygame.K_UP:
                                self.player_speed += 6

                if self.gameType in (1, 3):
                    self.AgentControl = self.opponent
                if self.gameType == 2:
                    self.AgentControl = self.player
                    self.opponent_ai()
                if self.gameType == 3:
                    self.OtherAgentControl = self.player
                    if self.OtherAgentControl.x - self.ball.x <= 50:
                        self.AgentRLControl(self.OtherAgentControl, self.agent2, self.ball)

                if (self.gameType in (1, 3) and self.ball.x - self.AgentControl.x <= 50) or \
                        (self.gameType == 2 and self.AgentControl.x - self.ball.x <= 50):
                    self.AgentRLControl(self.AgentControl, self.agent, self.ball)

                # inject animation and logic
                self.ball_animation()
                self.player_animation()

                # visuals
                self.screen.fill(self.bg_color)
                pygame.draw.rect(self.screen, self.light_grey, self.player)
                pygame.draw.rect(self.screen, self.light_grey, self.opponent)
                pygame.draw.ellipse(self.screen, self.light_grey, self.ball)
                pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width / 2, 0),
                                   (self.screen_width / 2, self.screen_height))
                player_txt = self.game_font.render(f"{self.player_score}", False, self.light_grey)
                self.screen.blit(player_txt, (600, 470))
                opponent_txt = self.game_font.render(f"{self.opponent_score}", False, self.light_grey)
                self.screen.blit(opponent_txt, (660, 470))
                # updating the window
                pygame.display.flip()
                self.clock.tick(60)

    def getAgent(self):
        return self.agent

    def getBall(self):
        return self.ball

    def AgentRLControl(self,agentControl,agent,ball):
        s = agent.get_state_from_pos(agentControl.centery, 140, self.screen_height)
        agentControl.y = agent.update(s, agentControl, ball)