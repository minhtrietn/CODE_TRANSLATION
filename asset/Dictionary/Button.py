from pygame import gfxdraw
import pygame


class AAfilledRoundedRect:
    def __init__(self, surface, rect=(0, 0, 0, 0), color: tuple or list = (0, 0, 0), radius: float = 1):
        rect = pygame.rect.Rect(rect)
        color = pygame.color.Color(color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0

        if radius > 1.0:
            raise ValueError("Max radius is 1.0")

        rectangle = pygame.surface.Surface(rect.size, pygame.constants.SRCALPHA).convert_alpha()
        circle = pygame.surface.Surface([min(rect.size) * 3] * 2, pygame.constants.SRCALPHA).convert_alpha()
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect())
        circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.constants.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.constants.BLEND_RGBA_MIN)

        surface.blit(rectangle, pos)


class Button_TEXT:
    def border(self, color: tuple or list = (0, 0, 0), border_thickness: float = 0, border_check: bool = True):
        self.color_border = color
        self.border_thickness = border_thickness
        self.border_check = border_check

    def __init__(self, text, font, width, height, pos, color, scaled, radius=0.5):
        self.check_disable = False
        self.text = text
        self.color_border = (255, 255, 255)
        self.border_check = False
        self.border_thickness = 10
        self.color = color
        self.font = font
        self.font2 = pygame.font.Font(self.font[0], self.font[1])
        self.radius = radius
        self.clicked = False
        self.scaled = scaled
        self.dynamic_scaled = scaled
        self.width = width
        self.height = height
        self.original_x_pos = pos[0]
        self.original_y_pos = pos[1]
        self.original_x_pos_border = pos[0] - self.border_thickness
        self.original_y_pos_border = pos[1] - self.border_thickness
        self.rect = pygame.Rect(pos, (width, height))
        self.rect_border = pygame.Rect((pos[0] - self.border_thickness, pos[1] - self.border_thickness),
                                       (width + self.border_thickness, height + self.border_thickness)
                                       )
        self.state = "normal"
        self.text_surf = self.font2.render(self.text, True, self.font[2] if len(self.font) > 2 else (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def update_state(self, new_state):
        if self.state != new_state:
            self.state = "update"

    def draw(self, surface):
        if not self.check_disable:
            if self.state == "update":
                if self.border_check:
                    self.rect_border.size = (self.width - self.dynamic_scaled + self.border_thickness,
                                             self.height - self.dynamic_scaled + self.border_thickness)
                    self.rect_border.x = self.original_x_pos_border + (
                            self.original_x_pos_border - self.original_x_pos) / 2 + self.dynamic_scaled / 2 + self.border_thickness
                    self.rect_border.y = self.original_y_pos_border + (
                            self.original_y_pos_border - self.original_y_pos) / 2 + self.dynamic_scaled / 2 + self.border_thickness
                    AAfilledRoundedRect(surface,
                                        self.rect_border,
                                        self.color_border,
                                        self.radius
                                        )

                self.rect.size = (self.width - self.dynamic_scaled, self.height - self.dynamic_scaled)
                self.rect.x = self.original_x_pos + self.dynamic_scaled / 2
                self.rect.y = self.original_y_pos + self.dynamic_scaled / 2
                AAfilledRoundedRect(surface,
                                    self.rect,
                                    self.color,
                                    self.radius
                                    )

                self.font2 = pygame.font.Font(self.font[0], self.font[1] - self.dynamic_scaled // 4)
                self.text_surf = self.font2.render(self.text, True, self.font[2] if len(self.font) > 2 else (255, 255, 255))
                self.text_rect = self.text_surf.get_rect(center=self.rect.center)
                self.state = "normal"
            else:
                if self.border_check:
                    AAfilledRoundedRect(surface,
                                        self.rect_border,
                                        self.color_border,
                                        self.radius
                                        )
                AAfilledRoundedRect(surface,
                                    self.rect,
                                    self.color, self.radius
                                    )
                self.state = "update"

            surface.blit(self.text_surf, self.text_rect)
            return self.check_click()
        else:
            if self.state == "update":
                if self.border_check:
                    self.rect_border.size = (self.width - self.dynamic_scaled + self.border_thickness,
                                             self.height - self.dynamic_scaled + self.border_thickness)
                    self.rect_border.x = self.original_x_pos_border + (
                            self.original_x_pos_border - self.original_x_pos) / 2 + self.dynamic_scaled / 2 + self.border_thickness
                    self.rect_border.y = self.original_y_pos_border + (
                            self.original_y_pos_border - self.original_y_pos) / 2 + self.dynamic_scaled / 2 + self.border_thickness
                    AAfilledRoundedRect(surface,
                                        self.rect_border,
                                        self.color_border,
                                        self.radius
                                        )

                self.rect.size = (self.width - self.dynamic_scaled, self.height - self.dynamic_scaled)
                self.rect.x = self.original_x_pos + self.dynamic_scaled / 2
                self.rect.y = self.original_y_pos + self.dynamic_scaled / 2
                AAfilledRoundedRect(surface,
                                    self.rect,
                                    self.color,
                                    self.radius
                                    )

                self.font2 = pygame.font.Font(self.font[0], self.font[1] - self.dynamic_scaled // 4)
                self.text_surf = self.font2.render(self.text, True,
                                                   self.font[2] if len(self.font) > 2 else (255, 255, 255))
                self.text_rect = self.text_surf.get_rect(center=self.rect.center)
                self.state = "normal"
            else:
                if self.border_check:
                    AAfilledRoundedRect(surface,
                                        self.rect_border,
                                        self.color_border,
                                        self.radius
                                        )
                AAfilledRoundedRect(surface,
                                    self.rect,
                                    self.color, self.radius
                                    )
                self.state = "update"

            surface.blit(self.text_surf, self.text_rect)

    def check_click(self):
        if not self.check_disable:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    if self.dynamic_scaled != self.scaled:
                        self.dynamic_scaled = self.scaled
                        self.update_state("update")
                    self.clicked = True
                else:
                    if self.clicked:
                        self.clicked = False
                        return True
                    if self.dynamic_scaled != 0:
                        self.dynamic_scaled = 0
                        self.update_state("update")
            elif self.dynamic_scaled != self.scaled:
                self.dynamic_scaled = self.scaled
                self.update_state("update")
        else:
            return False

    def disable(self):
        self.check_disable = True

    def enable(self):
        self.check_disable = False


class Button_IMG:
    def __init__(self, x: float = 0, y: float = 0, image=None, scale: float = 0, scale_change: float = 0):
        self.check_disable = False
        self.x = x
        self.y = y
        self.image = image
        self.clicked = False
        self.scale = scale
        self.scaled = scale
        self.scale_change = scale_change
        self.width = image.get_width()
        self.height = image.get_height()
        self.imaged = pygame.transform.smoothscale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.imaged.get_rect()
        self.rect.center = (x, y)
        self.state = "normal"

    def draw(self, surface):
        if not self.check_disable:
            if self.state == "update":
                self.imaged = pygame.transform.smoothscale(self.image,
                                                           (int(self.width * self.scaled),
                                                            int(self.height * self.scaled)))
                self.state = "normal"
            surface.blit(self.imaged, (self.rect.x + (self.width * self.scale - int(self.width * self.scaled)) / 2,
                                       self.rect.y + (self.height * self.scale - int(self.height * self.scaled)) / 2))
            return self.check_click()
        else:
            surface.blit(self.imaged, (self.rect.x + (self.width * self.scale - int(self.width * self.scaled)) / 2,
                                       self.rect.y + (self.height * self.scale - int(self.height * self.scaled)) / 2))
            return self.check_click()

    def update_state(self, new_state):
        if self.state != new_state:
            self.state = "update"

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if not self.check_disable:
            if self.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    if self.scaled != self.scale:
                        self.scaled = self.scale
                        self.update_state("update")
                    self.clicked = True
                else:
                    if self.clicked:
                        self.clicked = False
                        return True
                    if self.scaled != self.scale + self.scale_change:
                        self.scaled = self.scale + self.scale_change
                        self.update_state("update")
            elif self.scaled != self.scale:
                self.scaled = self.scale
                self.update_state("update")
        else:
            return False

    def disable(self):
        self.check_disable = True

    def enable(self):
        self.check_disable = False


class Animation_Toggle:
    def __init__(self, pos: tuple or list = (0, 0), width: float = 0, height: float = 0, scale: float = 0, comparison: bool = False):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = 400
        if comparison:
            self.x_circle = self.x + (self.width - self.scale - (self.height - self.scale) / 2)
            self.color_change = 255
        else:
            self.x_circle = self.x + (self.height - self.scale) / 2
            self.color_change = 0
        self.y_circle = self.y + (self.height - self.scale) / 2
        self.color_circle = (0, 0, 0)
        self.bool_check = True
        self.bool_stop = True
        self.bool_active = False
        self.started = False
        self.clicked = False

    def draw(self, screen, dt):
        if not self.started:
            self.started = True

        background = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        AAfilledRoundedRect(screen,
                            (self.x, self.y, self.width, self.height),
                            (self.color_change, self.color_change,
                             self.color_change)
                            )
        gfxdraw.aacircle(screen,
                         round(self.x_circle + self.scale / 2),
                         round(self.y_circle + self.scale / 2),
                         round(self.scale / 2), self.color_circle
                         )
        gfxdraw.filled_circle(screen,
                              round(self.x_circle + self.scale / 2),
                              round(self.y_circle + self.scale / 2),
                              round(self.scale / 2), self.color_circle
                              )

        mouse_pos = pygame.mouse.get_pos()

        if background.collidepoint(mouse_pos) or self.bool_active:
            if pygame.mouse.get_pressed()[0] or self.bool_active:
                self.clicked = True
            else:
                if self.clicked:
                    self.clicked = False
                    self.bool_stop = False
                    self.bool_active = False
                    if self.x_circle <= self.x + (self.height - self.scale) / 2:
                        self.bool_check = False
                    elif self.x_circle >= self.x + (self.width - self.scale - (self.height - self.scale) / 2):
                        self.bool_check = True

        movement = self.speed * dt
        if not self.bool_check and not self.bool_stop:
            self.x_circle += movement
            self.color_change += int(255 / ((self.x + (self.width - self.scale - (self.height - self.scale) / 2) - self.x + (self.height - self.scale) / 2) / movement) * 1.4 + movement)
            if self.x_circle >= self.x + (self.width - self.scale - (self.height - self.scale) / 2) or self.color_change >= 255:
                self.color_change = 255
                self.x_circle = self.x + (self.width - self.scale - (self.height - self.scale) / 2)
                self.bool_stop = True
                return True
        elif self.bool_check and not self.bool_stop:
            self.x_circle -= movement
            self.color_change -= int(255 / ((self.x + (self.width - self.scale - (self.height - self.scale) / 2) - self.x + (self.height - self.scale) / 2) / movement) * 1.4 + movement)
            if self.x_circle <= self.x + (self.height - self.scale) / 2 or self.color_change <= 0:
                self.color_change = 0
                self.x_circle = self.x + (self.height - self.scale) / 2
                self.bool_stop = True
                return True

    def set_speed(self, speed):
        self.speed = speed

    def set_circle_color(self, color: tuple or list = (0, 0, 0)):
        self.color_circle = color

    def active(self):
        self.bool_active = True

    def check(self):
        return self.bool_check
