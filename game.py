"""
🍄 Super Prady Bros - A Simple Mario-Style Platformer Game 🍄
Your first Python game! 

Controls:
- Arrow Keys or A/D to move left/right
- Space or Up Arrow to jump
- R to restart when game ends
- ESC to quit
"""

import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Try to initialize the mixer (for sound effects)
SOUND_AVAILABLE = False
try:
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except:
    print("Note: Sound is not available on this system. The game will run without sound.")

# Game Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 6

# Colors - A warm, vibrant palette
COLORS = {
    'sky_top': (135, 206, 235),      # Light sky blue
    'sky_bottom': (176, 224, 230),   # Powder blue
    'ground': (139, 90, 43),          # Saddle brown
    'grass': (34, 139, 34),           # Forest green
    'platform': (160, 82, 45),        # Sienna
    'platform_top': (50, 205, 50),    # Lime green
    'player': (220, 20, 60),          # Crimson red
    'player_face': (255, 218, 185),   # Peach
    'coin': (255, 215, 0),            # Gold
    'coin_shine': (255, 255, 200),    # Light yellow
    'enemy': (138, 43, 226),          # Blue violet
    'flag_pole': (139, 69, 19),       # Saddle brown
    'flag': (0, 255, 127),            # Spring green
    'cloud': (255, 255, 255),         # White
    'text': (255, 255, 255),          # White
    'text_shadow': (50, 50, 50),      # Dark gray
    'hill_back': (34, 120, 34),       # Dark green
    'hill_front': (50, 180, 50),      # Medium green
    'bush': (0, 100, 0),              # Dark green
}

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🍄 Super Prady Bros 🍄")
clock = pygame.time.Clock()

# Load fonts
FONT_AVAILABLE = False
title_font = None
score_font = None
info_font = None
try:
    title_font = pygame.font.Font(None, 72)
    score_font = pygame.font.Font(None, 48)
    info_font = pygame.font.Font(None, 36)
    FONT_AVAILABLE = True
except:
    try:
        title_font = pygame.font.SysFont('arial', 72)
        score_font = pygame.font.SysFont('arial', 48)
        info_font = pygame.font.SysFont('arial', 36)
        FONT_AVAILABLE = True
    except:
        print("Note: Font rendering is not available. Text will be displayed as shapes.")


class SoundEffects:
    """Simple sound effects using pygame's built-in synth"""
    def __init__(self):
        self.enabled = SOUND_AVAILABLE
        if not self.enabled:
            return
        try:
            # Create simple sound effects
            self.jump_sound = self._create_jump_sound()
            self.coin_sound = self._create_coin_sound()
            self.win_sound = self._create_win_sound()
            self.lose_sound = self._create_lose_sound()
        except:
            self.enabled = False
    
    def _create_jump_sound(self):
        """Create a simple jump sound"""
        sample_rate = 22050
        duration = 0.1
        samples = int(sample_rate * duration)
        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            freq = 400 + (800 * t)  # Rising frequency
            amplitude = int(4000 * (1 - t/duration))
            sample = int(amplitude * math.sin(2 * math.pi * freq * t))
            sound_array.append(max(-32767, min(32767, sample)))
        
        sound = pygame.mixer.Sound(buffer=bytes(0))
        try:
            import array
            arr = array.array('h', sound_array)
            sound = pygame.mixer.Sound(buffer=arr)
            sound.set_volume(0.3)
        except:
            pass
        return sound
    
    def _create_coin_sound(self):
        """Create a coin collection sound"""
        sample_rate = 22050
        duration = 0.15
        samples = int(sample_rate * duration)
        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            freq = 800 if t < 0.075 else 1000
            amplitude = int(3000 * (1 - t/duration))
            sample = int(amplitude * math.sin(2 * math.pi * freq * t))
            sound_array.append(max(-32767, min(32767, sample)))
        
        try:
            import array
            arr = array.array('h', sound_array)
            sound = pygame.mixer.Sound(buffer=arr)
            sound.set_volume(0.3)
            return sound
        except:
            return pygame.mixer.Sound(buffer=bytes(0))
    
    def _create_win_sound(self):
        """Create a victory sound"""
        sample_rate = 22050
        duration = 0.5
        samples = int(sample_rate * duration)
        sound_array = []
        notes = [523, 659, 784, 1047]  # C E G C
        for i in range(samples):
            t = i / sample_rate
            note_idx = min(int(t * 8), 3)
            freq = notes[note_idx]
            amplitude = int(3000 * (1 - t/duration))
            sample = int(amplitude * math.sin(2 * math.pi * freq * t))
            sound_array.append(max(-32767, min(32767, sample)))
        
        try:
            import array
            arr = array.array('h', sound_array)
            sound = pygame.mixer.Sound(buffer=arr)
            sound.set_volume(0.3)
            return sound
        except:
            return pygame.mixer.Sound(buffer=bytes(0))
    
    def _create_lose_sound(self):
        """Create a game over sound"""
        sample_rate = 22050
        duration = 0.4
        samples = int(sample_rate * duration)
        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            freq = 400 - (200 * t)  # Descending frequency
            amplitude = int(3000 * (1 - t/duration))
            sample = int(amplitude * math.sin(2 * math.pi * freq * t))
            sound_array.append(max(-32767, min(32767, sample)))
        
        try:
            import array
            arr = array.array('h', sound_array)
            sound = pygame.mixer.Sound(buffer=arr)
            sound.set_volume(0.3)
            return sound
        except:
            return pygame.mixer.Sound(buffer=bytes(0))
    
    def play_jump(self):
        if self.enabled:
            try:
                self.jump_sound.play()
            except:
                pass
    
    def play_coin(self):
        if self.enabled:
            try:
                self.coin_sound.play()
            except:
                pass
    
    def play_win(self):
        if self.enabled:
            try:
                self.win_sound.play()
            except:
                pass
    
    def play_lose(self):
        if self.enabled:
            try:
                self.lose_sound.play()
            except:
                pass


class Player:
    """The main player character - our hero!"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.animation_timer = 0
        self.is_jumping = False
    
    def update(self, platforms):
        """Update player physics and position"""
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Cap falling speed
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Update animation
        self.animation_timer += 1
        if self.animation_timer > 8:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
        
        # Move horizontally
        self.x += self.vel_x
        
        # Check horizontal collisions
        for platform in platforms:
            if self._collides_with(platform):
                if self.vel_x > 0:  # Moving right
                    self.x = platform.x - self.width
                elif self.vel_x < 0:  # Moving left
                    self.x = platform.x + platform.width
        
        # Move vertically
        self.y += self.vel_y
        
        # Check vertical collisions
        self.on_ground = False
        for platform in platforms:
            if self._collides_with(platform):
                if self.vel_y > 0:  # Falling
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                elif self.vel_y < 0:  # Jumping up
                    self.y = platform.y + platform.height
                    self.vel_y = 0
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
    
    def _collides_with(self, platform):
        """Check if player collides with a platform"""
        return (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y)
    
    def jump(self, sounds):
        """Make the player jump"""
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            self.is_jumping = True
            sounds.play_jump()
    
    def move_left(self):
        """Move player left"""
        self.vel_x = -PLAYER_SPEED
        self.facing_right = False
    
    def move_right(self):
        """Move player right"""
        self.vel_x = PLAYER_SPEED
        self.facing_right = True
    
    def stop(self):
        """Stop horizontal movement"""
        self.vel_x = 0
    
    def draw(self, surface):
        """Draw the player character"""
        x, y = int(self.x), int(self.y)
        
        # Body (red overalls)
        body_color = COLORS['player']
        pygame.draw.rect(surface, body_color, (x + 5, y + 20, 30, 30))
        
        # Head
        face_color = COLORS['player_face']
        pygame.draw.ellipse(surface, face_color, (x + 8, y, 24, 24))
        
        # Hat (red cap)
        pygame.draw.rect(surface, body_color, (x + 5, y, 30, 10))
        if self.facing_right:
            pygame.draw.rect(surface, body_color, (x + 25, y + 5, 12, 8))
        else:
            pygame.draw.rect(surface, body_color, (x - 2, y + 5, 12, 8))
        
        # Eyes
        eye_x = x + 22 if self.facing_right else x + 12
        pygame.draw.circle(surface, (0, 0, 0), (eye_x, y + 12), 3)
        pygame.draw.circle(surface, (255, 255, 255), (eye_x + 1, y + 11), 1)
        
        # Mustache
        pygame.draw.ellipse(surface, (101, 67, 33), (x + 10, y + 16, 20, 6))
        
        # Legs with simple animation
        leg_offset = 0
        if self.vel_x != 0 and self.on_ground:
            leg_offset = 3 if self.animation_frame % 2 == 0 else -3
        
        # Left leg
        pygame.draw.rect(surface, (0, 0, 139), (x + 8, y + 42, 10, 8))
        # Right leg  
        pygame.draw.rect(surface, (0, 0, 139), (x + 22, y + 42, 10, 8))
        
        # Shoes
        pygame.draw.ellipse(surface, (101, 67, 33), (x + 5, y + 45, 14, 8))
        pygame.draw.ellipse(surface, (101, 67, 33), (x + 21, y + 45, 14, 8))
    
    def get_rect(self):
        """Get player's collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Platform:
    """A platform that the player can stand on"""
    
    def __init__(self, x, y, width, height, is_ground=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_ground = is_ground
    
    def draw(self, surface):
        """Draw the platform with a nice brick/grass look"""
        if self.is_ground:
            # Ground with grass on top
            pygame.draw.rect(surface, COLORS['ground'], 
                           (self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, COLORS['grass'], 
                           (self.x, self.y, self.width, 10))
            
            # Draw grass blades
            for i in range(int(self.x), int(self.x + self.width), 8):
                pygame.draw.line(surface, COLORS['grass'], 
                               (i, self.y), (i - 2, self.y - 5), 2)
                pygame.draw.line(surface, COLORS['grass'], 
                               (i + 4, self.y), (i + 6, self.y - 4), 2)
        else:
            # Floating platform (brick style)
            pygame.draw.rect(surface, COLORS['platform'], 
                           (self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, COLORS['platform_top'], 
                           (self.x, self.y, self.width, 8))
            
            # Draw brick pattern
            brick_color = (180, 102, 65)
            for row in range(0, int(self.height), 15):
                offset = 0 if row % 30 == 0 else 15
                for col in range(int(-offset), int(self.width), 30):
                    pygame.draw.rect(surface, brick_color, 
                                   (self.x + col, self.y + row + 8, 28, 13), 1)


class Coin:
    """Collectible coins that give points"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.collected = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.float_offset = random.random() * math.pi * 2
    
    def update(self):
        """Animate the coin"""
        self.animation_timer += 1
        if self.animation_timer > 5:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 8
    
    def draw(self, surface):
        """Draw the spinning coin"""
        if self.collected:
            return
        
        # Floating animation
        float_y = self.y + math.sin(pygame.time.get_ticks() / 200 + self.float_offset) * 3
        
        # Coin width changes to simulate rotation
        width_factor = abs(math.sin(self.animation_frame * math.pi / 4))
        display_width = max(4, int(self.width * width_factor))
        
        x_offset = (self.width - display_width) // 2
        
        # Draw coin
        pygame.draw.ellipse(surface, COLORS['coin'], 
                          (self.x + x_offset, float_y, display_width, self.height))
        
        # Shine effect
        if display_width > 10:
            pygame.draw.ellipse(surface, COLORS['coin_shine'], 
                              (self.x + x_offset + 3, float_y + 3, 
                               display_width // 3, self.height // 3))
    
    def get_rect(self):
        """Get coin's collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Enemy:
    """A bad guy that the player must avoid"""
    
    def __init__(self, x, y, patrol_left, patrol_right):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 35
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.speed = 2
        self.direction = 1
        self.animation_frame = 0
        self.animation_timer = 0
    
    def update(self):
        """Move the enemy back and forth"""
        self.x += self.speed * self.direction
        
        # Reverse direction at patrol boundaries
        if self.x <= self.patrol_left:
            self.direction = 1
        elif self.x >= self.patrol_right:
            self.direction = -1
        
        # Animate
        self.animation_timer += 1
        if self.animation_timer > 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2
    
    def draw(self, surface):
        """Draw the enemy (a purple goomba-like creature)"""
        x, y = int(self.x), int(self.y)
        
        # Body
        pygame.draw.ellipse(surface, COLORS['enemy'], 
                          (x, y + 10, self.width, self.height - 10))
        
        # Head/top
        pygame.draw.ellipse(surface, COLORS['enemy'], 
                          (x + 5, y, self.width - 10, 20))
        
        # Angry eyebrows
        pygame.draw.polygon(surface, (0, 0, 0), [
            (x + 8, y + 12), (x + 18, y + 8), (x + 18, y + 14)
        ])
        pygame.draw.polygon(surface, (0, 0, 0), [
            (x + 32, y + 12), (x + 22, y + 8), (x + 22, y + 14)
        ])
        
        # Eyes
        pygame.draw.circle(surface, (255, 255, 255), (x + 13, y + 15), 5)
        pygame.draw.circle(surface, (255, 255, 255), (x + 27, y + 15), 5)
        pygame.draw.circle(surface, (0, 0, 0), (x + 14, y + 16), 2)
        pygame.draw.circle(surface, (0, 0, 0), (x + 28, y + 16), 2)
        
        # Feet with walking animation
        foot_offset = 3 if self.animation_frame == 0 else -3
        pygame.draw.ellipse(surface, (80, 30, 180), 
                          (x + 2, y + 30 + foot_offset, 15, 8))
        pygame.draw.ellipse(surface, (80, 30, 180), 
                          (x + 23, y + 30 - foot_offset, 15, 8))
    
    def get_rect(self):
        """Get enemy's collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Flag:
    """The goal flag that ends the level"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pole_height = 150
        self.flag_y = y + 20
        self.animation_timer = 0
    
    def update(self):
        """Animate the flag waving"""
        self.animation_timer += 1
    
    def draw(self, surface):
        """Draw the victory flag"""
        x, y = int(self.x), int(self.y)
        
        # Pole
        pygame.draw.rect(surface, COLORS['flag_pole'], 
                        (x, y, 8, self.pole_height))
        
        # Ball on top
        pygame.draw.circle(surface, COLORS['coin'], (x + 4, y), 8)
        
        # Flag with wave effect
        wave = math.sin(self.animation_timer / 10) * 5
        flag_points = [
            (x + 8, y + 10),
            (x + 60 + wave, y + 25),
            (x + 55 + wave * 0.5, y + 40),
            (x + 8, y + 50)
        ]
        pygame.draw.polygon(surface, COLORS['flag'], flag_points)
        
        # Star on flag
        star_x = x + 30 + wave * 0.5
        star_y = y + 30
        pygame.draw.polygon(surface, COLORS['coin'], [
            (star_x, star_y - 8),
            (star_x + 3, star_y - 2),
            (star_x + 9, star_y - 2),
            (star_x + 4, star_y + 2),
            (star_x + 6, star_y + 8),
            (star_x, star_y + 4),
            (star_x - 6, star_y + 8),
            (star_x - 4, star_y + 2),
            (star_x - 9, star_y - 2),
            (star_x - 3, star_y - 2),
        ])
    
    def get_rect(self):
        """Get flag's collision rectangle"""
        return pygame.Rect(self.x - 10, self.y, 30, self.pole_height)


class Cloud:
    """Decorative background clouds"""
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 0.2 + random.random() * 0.3
    
    def update(self):
        """Slowly move the cloud"""
        self.x -= self.speed
        if self.x < -100:
            self.x = SCREEN_WIDTH + 50
            self.y = random.randint(30, 150)
    
    def draw(self, surface):
        """Draw a fluffy cloud"""
        x, y = int(self.x), int(self.y)
        s = self.size
        
        # Multiple overlapping circles for fluffy effect
        pygame.draw.circle(surface, COLORS['cloud'], (x, y), s)
        pygame.draw.circle(surface, COLORS['cloud'], (x + s, y - s//3), int(s * 0.8))
        pygame.draw.circle(surface, COLORS['cloud'], (x + s * 2, y), int(s * 0.9))
        pygame.draw.circle(surface, COLORS['cloud'], (x + s, y + s//4), int(s * 0.7))


class Game:
    """Main game class that manages everything"""
    
    def __init__(self):
        self.sounds = SoundEffects()
        self.reset_game()
    
    def reset_game(self):
        """Reset/initialize the game state"""
        # Create player
        self.player = Player(50, 400)
        
        # Create platforms
        self.platforms = [
            # Ground
            Platform(0, 550, 400, 50, is_ground=True),
            Platform(500, 550, 200, 50, is_ground=True),
            Platform(800, 550, 200, 50, is_ground=True),
            
            # Floating platforms
            Platform(200, 450, 120, 30),
            Platform(400, 380, 100, 30),
            Platform(150, 300, 100, 30),
            Platform(350, 220, 120, 30),
            Platform(550, 300, 100, 30),
            Platform(700, 400, 120, 30),
            Platform(850, 280, 100, 30),
        ]
        
        # Create coins
        self.coins = [
            Coin(230, 410),
            Coin(280, 410),
            Coin(430, 340),
            Coin(180, 260),
            Coin(380, 180),
            Coin(420, 180),
            Coin(580, 260),
            Coin(730, 360),
            Coin(780, 360),
            Coin(880, 240),
        ]
        
        # Create enemies
        self.enemies = [
            Enemy(100, 515, 50, 350),
            Enemy(550, 515, 500, 680),
            Enemy(380, 185, 350, 450),
        ]
        
        # Create the goal flag
        self.flag = Flag(920, 400)
        
        # Create decorative clouds
        self.clouds = [
            Cloud(100, 80, 30),
            Cloud(300, 50, 25),
            Cloud(500, 100, 35),
            Cloud(700, 60, 28),
            Cloud(900, 90, 32),
        ]
        
        # Game state
        self.score = 0
        self.game_won = False
        self.game_over = False
        self.message_timer = 0
    
    def draw_background(self):
        """Draw the sky and background elements"""
        # Gradient sky
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(COLORS['sky_top'][0] * (1 - ratio) + COLORS['sky_bottom'][0] * ratio)
            g = int(COLORS['sky_top'][1] * (1 - ratio) + COLORS['sky_bottom'][1] * ratio)
            b = int(COLORS['sky_top'][2] * (1 - ratio) + COLORS['sky_bottom'][2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Background hills
        hill_points = [
            (0, 550), (100, 480), (200, 520), (350, 450), 
            (450, 500), (600, 420), (750, 480), (900, 440), 
            (1000, 500), (1000, 550)
        ]
        pygame.draw.polygon(screen, COLORS['hill_back'], hill_points)
        
        # Foreground hills
        hill_points2 = [
            (0, 550), (150, 500), (300, 530), (500, 480), 
            (700, 520), (850, 490), (1000, 530), (1000, 550)
        ]
        pygame.draw.polygon(screen, COLORS['hill_front'], hill_points2)
        
        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(screen)
    
    def draw_ui(self):
        """Draw score and game info"""
        if FONT_AVAILABLE:
            # Score with shadow
            score_text = f"Coins: {self.score}"
            shadow = score_font.render(score_text, True, COLORS['text_shadow'])
            text = score_font.render(score_text, True, COLORS['text'])
            screen.blit(shadow, (22, 22))
            screen.blit(text, (20, 20))
            
            # Instructions
            if self.score == 0 and not self.game_over and not self.game_won:
                hint = info_font.render("Arrow Keys/WASD to move, Space to jump!", 
                                       True, COLORS['text'])
                screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 70))
        else:
            # Draw coin count as coin icons
            for i in range(self.score):
                pygame.draw.circle(screen, COLORS['coin'], (30 + i * 25, 30), 10)
            # Draw total coins as empty circles
            for i in range(self.score, len(self.coins)):
                pygame.draw.circle(screen, COLORS['coin'], (30 + i * 25, 30), 10, 2)
    
    def draw_message(self, text, sub_text=""):
        """Draw a centered message on screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        if FONT_AVAILABLE:
            # Main message
            shadow = title_font.render(text, True, COLORS['text_shadow'])
            message = title_font.render(text, True, COLORS['text'])
            x = SCREEN_WIDTH // 2 - message.get_width() // 2
            y = SCREEN_HEIGHT // 2 - 50
            screen.blit(shadow, (x + 3, y + 3))
            screen.blit(message, (x, y))
            
            # Sub message
            if sub_text:
                sub = info_font.render(sub_text, True, COLORS['text'])
                screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, y + 70))
        else:
            # Draw visual indicators without text
            cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            if "WIN" in text:
                # Draw a big star for winning
                self._draw_star(cx, cy - 30, 60, COLORS['coin'])
                # Draw trophy shape
                pygame.draw.rect(screen, COLORS['coin'], (cx - 40, cy + 40, 80, 20))
                pygame.draw.rect(screen, COLORS['coin'], (cx - 20, cy + 60, 40, 30))
            else:
                # Draw X for game over
                pygame.draw.line(screen, (255, 0, 0), (cx - 50, cy - 50), (cx + 50, cy + 50), 10)
                pygame.draw.line(screen, (255, 0, 0), (cx + 50, cy - 50), (cx - 50, cy + 50), 10)
            
            # Draw "Press R" hint as keyboard key
            pygame.draw.rect(screen, COLORS['text'], (cx - 25, cy + 100, 50, 40), 3)
            pygame.draw.rect(screen, COLORS['text'], (cx - 15, cy + 110, 30, 20))
    
    def _draw_star(self, x, y, size, color):
        """Draw a star shape"""
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = size if i % 2 == 0 else size // 2
            px = x + r * math.cos(angle)
            py = y - r * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)
    
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        if self.game_over or self.game_won:
            if keys[pygame.K_r]:
                self.reset_game()
            return
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop()
        
        # Jumping
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.jump(self.sounds)
    
    def update(self):
        """Update all game objects"""
        if self.game_over or self.game_won:
            self.message_timer += 1
            return
        
        # Update player
        self.player.update(self.platforms)
        
        # Update coins
        for coin in self.coins:
            coin.update()
            if not coin.collected and self.player.get_rect().colliderect(coin.get_rect()):
                coin.collected = True
                self.score += 1
                self.sounds.play_coin()
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update()
            if self.player.get_rect().colliderect(enemy.get_rect()):
                self.game_over = True
                self.sounds.play_lose()
        
        # Update flag
        self.flag.update()
        if self.player.get_rect().colliderect(self.flag.get_rect()):
            self.game_won = True
            self.sounds.play_win()
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update()
        
        # Check if player fell off screen
        if self.player.y > SCREEN_HEIGHT:
            self.game_over = True
            self.sounds.play_lose()
    
    def draw(self):
        """Draw everything"""
        # Background
        self.draw_background()
        
        # Platforms
        for platform in self.platforms:
            platform.draw(screen)
        
        # Coins
        for coin in self.coins:
            coin.draw(screen)
        
        # Enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Flag
        self.flag.draw(screen)
        
        # Player
        self.player.draw(screen)
        
        # UI
        self.draw_ui()
        
        # Game over/win messages
        if self.game_won:
            self.draw_message(f"🎉 YOU WIN! 🎉", 
                            f"Collected {self.score}/{len(self.coins)} coins! Press R to play again")
        elif self.game_over:
            self.draw_message("💀 GAME OVER 💀", "Press R to try again")
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Handle continuous input
            self.handle_input()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            
            # Cap framerate
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


# Start the game!
if __name__ == "__main__":
    print("🍄 Welcome to Super Prady Bros! 🍄")
    print("=" * 40)
    print("Controls:")
    print("  ← → or A/D : Move left/right")
    print("  Space or ↑  : Jump")
    print("  R           : Restart")
    print("  ESC         : Quit")
    print("=" * 40)
    print("Goal: Collect coins and reach the flag!")
    print("Watch out for the purple enemies!")
    print()
    
    game = Game()
    game.run()

