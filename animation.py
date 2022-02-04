import pygame


class AnimationSequence(object):
    def __init__(self, source_surface, x, y, frame_width, frame_height, num_frames):
        self.src = source_surface
        self.src_x = x
        self.src_y = y
        self.w = frame_width
        self.h = frame_height
        self.num_frames = num_frames

    def draw(self, dest_surface, dest_x, dest_y, frame_num, center=True):
        """draws the given frame at the destination"""
        if center:
            offset_x = -self.w/2
            offset_y = -self.h/2
        else:
            offset_x = 0
            offset_y = 0
        dest_surface.blit(self.src, (dest_x+offset_x, dest_y+offset_y),
                          (self.src_x + frame_num*self.w, self.src_y, self.w, self.h))

def test_animations():
    sprite_sheet = pygame.image.load("./images/sprite_sheet.gif")
    # Load the animations. The numbers denote where the animation frames start,
    # and the total length of frames.
    walk_left_anim = AnimationSequence(sprite_sheet, 8, 453, 24, 28, 8)
    walk_right_anim = AnimationSequence(sprite_sheet, 198, 453, 23, 28, 8)
    walk_up_anim = AnimationSequence(sprite_sheet, 9, 486, 23, 28, 8)
    walk_down_anim = AnimationSequence(sprite_sheet, 200, 486, 22, 28, 8)
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    running = True
    frame_num = 0
    curr_anim = walk_left_anim
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    print ("walk left")
                    curr_anim = walk_left_anim
                if event.key == pygame.K_RIGHT:
                    print ("walk right")
                    curr_anim = walk_right_anim
                if event.key == pygame.K_UP:
                    print ("walk up")
                    curr_anim = walk_up_anim
                if event.key == pygame.K_DOWN:
                    print ("walk down")
                    curr_anim = walk_down_anim
        screen.fill((0,0,0))
        curr_anim.draw(screen, 320, 240, frame_num)
        frame_num += 1
        if frame_num >=8:
            frame_num = 0
        pygame.display.flip()
        pygame.time.delay(100)
    pygame.quit()

if __name__ == "__main__":
    test_animations()

