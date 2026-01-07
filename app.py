"""
⚡ Super Prady Bros - The Grid Runner ⚡
A Tron-inspired platformer game that runs in your browser via Streamlit!
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="⚡ Super Prady Bros",
    page_icon="⚡",
    layout="wide"
)

# Hide Streamlit's default menu and footer for a cleaner game experience
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #0a0a0a 50%, #1a1a2e 100%);
    }
    .game-title {
        text-align: center;
        font-family: 'Orbitron', 'Press Start 2P', monospace;
        color: #00FFFF;
        text-shadow: 0 0 20px #00FFFF, 0 0 40px #00FFFF, 0 0 60px #0088FF;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: 8px;
    }
    .game-subtitle {
        text-align: center;
        color: #FF6600;
        font-size: 1rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px #FF6600;
        letter-spacing: 4px;
    }
    .controls-box {
        background: rgba(0, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 2px;
        padding: 15px;
        margin: 10px auto;
        max-width: 600px;
        text-align: center;
        color: #00FFFF;
    }
    .controls-box kbd {
        background: #000;
        padding: 5px 10px;
        border-radius: 2px;
        margin: 0 5px;
        border: 1px solid #00FFFF;
        color: #00FFFF;
        text-shadow: 0 0 5px #00FFFF;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="game-title">⚡ SUPER PRADY BROS ⚡</h1>', unsafe_allow_html=True)
st.markdown('<p class="game-subtitle">ENTER THE GRID</p>', unsafe_allow_html=True)

# The game HTML/JavaScript
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            background: transparent;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        #gameContainer {
            position: relative;
            border-radius: 0;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.3), 0 0 0 2px #00FFFF;
        }
        #gameCanvas {
            display: block;
            background: #000000;
        }
        #overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0,0,0,0.9);
            color: #00FFFF;
            font-size: 24px;
            text-align: center;
            display: none;
            font-family: 'Courier New', monospace;
        }
        #overlay h1 {
            font-size: 42px;
            margin-bottom: 20px;
            text-shadow: 0 0 20px #00FFFF, 0 0 40px #00FFFF;
            letter-spacing: 4px;
        }
        #overlay p {
            margin: 10px 0;
            color: #FF6600;
        }
        #overlay .restart-hint {
            margin-top: 30px;
            font-size: 16px;
            color: #00FFFF;
            animation: pulse 1.5s infinite;
            letter-spacing: 2px;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .mobile-controls {
            display: none;
            position: absolute;
            bottom: 10px;
            left: 0;
            right: 0;
            padding: 10px;
        }
        .mobile-btn {
            background: rgba(255,255,255,0.3);
            border: 2px solid rgba(255,255,255,0.5);
            color: white;
            font-size: 24px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            cursor: pointer;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
        }
        .mobile-btn:active {
            background: rgba(255,255,255,0.5);
        }
        @media (max-width: 800px) {
            .mobile-controls {
                display: flex;
                justify-content: space-between;
            }
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <canvas id="gameCanvas" width="900" height="500" tabindex="1"></canvas>
        <div id="overlay">
            <h1 id="overlayTitle">🎉 YOU WIN! 🎉</h1>
            <p id="overlayScore">Coins: 0/10</p>
            <p class="restart-hint">[ PRESS R TO SELECT PROGRAM AND REBOOT ]</p>
        </div>
        <div class="mobile-controls">
            <div style="display: flex; gap: 10px;">
                <button class="mobile-btn" id="btnLeft">◀</button>
                <button class="mobile-btn" id="btnRight">▶</button>
            </div>
            <button class="mobile-btn" id="btnJump">▲</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const overlay = document.getElementById('overlay');
        const overlayTitle = document.getElementById('overlayTitle');
        const overlayScore = document.getElementById('overlayScore');

        // Game constants (tuned for comfortable gameplay - 60% speed)
        const GRAVITY = 0.35;
        const JUMP_STRENGTH = -10;
        const PLAYER_SPEED = 2.1;
        
        // World size (scrollable level)
        const WORLD_WIDTH = 3000;
        let cameraX = 0;

        // Colors - TRON aesthetic (Level 1)
        const COLORS_L1 = {
            skyTop: '#000000',
            skyBottom: '#0a0a1a',
            ground: '#0a0a0a',
            grass: '#00FFFF',
            platform: '#111111',
            platformTop: '#00FFFF',
            neonCyan: '#00FFFF',
            neonOrange: '#FF6600',
            neonRed: '#FF0044',
            gridLine: 'rgba(0, 255, 255, 0.15)'
        };
        
        // Colors - NYC Dimension (Level 2)
        const COLORS_L2 = {
            skyTop: '#1a1a2e',
            skyBottom: '#2d132c',
            ground: '#1a1a1a',
            grass: '#FFD700',
            platform: '#2a2a2a',
            platformTop: '#FFD700',
            neonCyan: '#FFD700',
            neonOrange: '#FF4500',
            neonRed: '#FF1744',
            gridLine: 'rgba(255, 215, 0, 0.1)'
        };
        
        // Colors - Space Dimension (Level 3)
        const COLORS_L3 = {
            skyTop: '#000011',
            skyBottom: '#000033',
            ground: '#000000',
            grass: '#00FFAA',
            platform: '#111122',
            platformTop: '#00FFAA',
            neonCyan: '#00FFFF',
            neonOrange: '#FF6600',
            neonRed: '#FF0066',
            gridLine: 'rgba(0, 255, 170, 0.1)'
        };
        
        // Current colors (changes based on level)
        let COLORS = {
            skyTop: '#000000',
            skyBottom: '#0a0a1a',
            ground: '#0a0a0a',
            grass: '#00FFFF',
            platform: '#111111',
            platformTop: '#00FFFF',
            player: '#00FFFF',
            playerFace: '#000000',
            coin: '#FF6600',
            coinShine: '#FFAA44',
            enemy: '#FF0044',
            flagPole: '#333333',
            flag: '#00FFFF',
            cloud: 'rgba(0, 255, 255, 0.1)',
            text: '#00FFFF',
            textShadow: '#004444',
            gridLine: 'rgba(0, 255, 255, 0.15)',
            neonCyan: '#00FFFF',
            neonOrange: '#FF6600',
            neonRed: '#FF0044',
            neonWhite: '#FFFFFF',
            neonPurple: '#AA00FF'
        };
        
        // Update colors based on level
        function updateLevelColors() {
            let src = COLORS_L1;
            if (currentLevel === 2) src = COLORS_L2;
            else if (currentLevel === 3) src = COLORS_L3;
            
            COLORS.skyTop = src.skyTop;
            COLORS.skyBottom = src.skyBottom;
            COLORS.ground = src.ground;
            COLORS.grass = src.grass;
            COLORS.platform = src.platform;
            COLORS.platformTop = src.platformTop;
            COLORS.gridLine = src.gridLine;
        }

        // Game state
        let gameState = 'title'; // 'title', 'character', 'playing', 'won', 'lost', 'transition'
        let score = 0;
        let animationFrame = 0;
        let playerName = '';
        let nameInputActive = false;
        let selectedCharacter = 0;
        let currentLevel = 1;
        let totalScore = 0; // Accumulated score across levels
        
        // Identity Disc weapon
        let disc = {
            active: false,
            x: 0,
            y: 0,
            velX: 0,
            velY: 0,
            returning: false,
            rotation: 0
        };
        const DISC_SPEED = 12;
        const DISC_SIZE = 15;
        
        // Player health (Level 2 only)
        const MAX_HEALTH = 50;
        let playerHealth = MAX_HEALTH;
        let invincibilityTimer = 0;
        
        // Enemy discs (Level 2 - enemies shoot at player)
        let enemyDiscs = [];
        const ENEMY_DISC_SPEED = 5;
        const ENEMY_DISC_SIZE = 10;
        
        // Level 3 - Space Shooter variables
        let missiles = []; // Player missiles
        let spaceDrones = []; // Enemy drones
        let stars = []; // Background stars
        const MISSILE_SPEED = 10;
        const JET_SPEED = 3;
        let jetY = 250; // Jet vertical position
        let jetVelY = 0; // Jet vertical velocity
        const JET_WIDTH = 60;
        const JET_HEIGHT = 30;
        
        // Available characters - TRON inspired programs
        const characters = [
            { 
                name: 'ARES', 
                circuitColor: '#FF0044',
                secondaryColor: '#AA0022',
                description: 'Elite Grid Warrior',
                helmetStyle: 'visor',
                circuitPattern: 'angular'
            },
            { 
                name: 'SIREN', 
                circuitColor: '#FF6600',
                secondaryColor: '#FF3300',
                description: 'Rogue Program',
                helmetStyle: 'sleek',
                circuitPattern: 'flowing'
            },
            { 
                name: 'QUORRA', 
                circuitColor: '#FFFFFF',
                secondaryColor: '#88CCFF',
                description: 'The Last ISO',
                helmetStyle: 'open',
                circuitPattern: 'organic'
            },
            { 
                name: 'RINZLER', 
                circuitColor: '#00FFFF',
                secondaryColor: '#0088FF',
                description: 'Repurposed Warrior',
                helmetStyle: 'full',
                circuitPattern: 'aggressive'
            },
            { 
                name: 'GEM', 
                circuitColor: '#AA00FF',
                secondaryColor: '#FF00AA',
                description: 'Siren Program',
                helmetStyle: 'elegant',
                circuitPattern: 'symmetric'
            },
            { 
                name: 'CASTOR', 
                circuitColor: '#FFFFFF',
                secondaryColor: '#AAAAAA',
                description: 'End of Line Club',
                helmetStyle: 'stylish',
                circuitPattern: 'flashy'
            },
            { 
                name: 'FLYNN', 
                circuitColor: '#00FFFF',
                secondaryColor: '#00AAFF',
                description: 'The Creator',
                helmetStyle: 'classic',
                circuitPattern: 'legacy'
            },
            { 
                name: 'YORI', 
                circuitColor: '#00FFFF',
                secondaryColor: '#00FF88',
                description: 'System Monitor',
                helmetStyle: 'feminine',
                circuitPattern: 'elegant'
            }
        ];

        // Input state
        const keys = {
            left: false,
            right: false,
            jump: false
        };

        // Player
        const player = {
            x: 50,
            y: 350,
            width: 36,
            height: 45,
            velX: 0,
            velY: 0,
            onGround: false,
            facingRight: true,
            animFrame: 0,
            animTimer: 0
        };

        // Platforms - Dynamic based on level
        let platforms = [];
        
        // Level 1 platforms (The Grid)
        const platforms_L1 = [
            { x: 0, y: 450, width: 400, height: 50, isGround: true },
            { x: 180, y: 370, width: 100, height: 25, isGround: false },
            { x: 350, y: 310, width: 90, height: 25, isGround: false },
            { x: 500, y: 450, width: 200, height: 50, isGround: true },
            { x: 550, y: 350, width: 100, height: 25, isGround: false },
            { x: 450, y: 250, width: 90, height: 25, isGround: false },
            { x: 800, y: 450, width: 150, height: 50, isGround: true },
            { x: 750, y: 350, width: 80, height: 25, isGround: false },
            { x: 880, y: 280, width: 100, height: 25, isGround: false },
            { x: 1000, y: 350, width: 80, height: 25, isGround: false },
            { x: 1050, y: 450, width: 250, height: 50, isGround: true },
            { x: 1100, y: 350, width: 100, height: 25, isGround: false },
            { x: 1250, y: 280, width: 90, height: 25, isGround: false },
            { x: 1400, y: 450, width: 120, height: 50, isGround: true },
            { x: 1380, y: 350, width: 80, height: 25, isGround: false },
            { x: 1500, y: 380, width: 70, height: 25, isGround: false },
            { x: 1600, y: 320, width: 80, height: 25, isGround: false },
            { x: 1700, y: 450, width: 200, height: 50, isGround: true },
            { x: 1750, y: 350, width: 100, height: 25, isGround: false },
            { x: 1650, y: 250, width: 90, height: 25, isGround: false },
            { x: 1850, y: 280, width: 100, height: 25, isGround: false },
            { x: 2000, y: 450, width: 150, height: 50, isGround: true },
            { x: 2050, y: 350, width: 80, height: 25, isGround: false },
            { x: 2180, y: 400, width: 100, height: 25, isGround: false },
            { x: 2300, y: 450, width: 200, height: 50, isGround: true },
            { x: 2350, y: 350, width: 100, height: 25, isGround: false },
            { x: 2500, y: 300, width: 90, height: 25, isGround: false },
            { x: 2650, y: 450, width: 350, height: 50, isGround: true },
        ];
        
        // Level 2 platforms (NYC Streets) - Rooftops and fire escapes
        const platforms_L2 = [
            // Starting rooftop
            { x: 0, y: 450, width: 300, height: 50, isGround: true },
            { x: 150, y: 380, width: 60, height: 15, isGround: false },
            // Gap with fire escape
            { x: 380, y: 420, width: 50, height: 15, isGround: false },
            { x: 450, y: 380, width: 50, height: 15, isGround: false },
            { x: 520, y: 340, width: 50, height: 15, isGround: false },
            // Building 2
            { x: 600, y: 450, width: 200, height: 50, isGround: true },
            { x: 650, y: 370, width: 80, height: 20, isGround: false },
            { x: 750, y: 300, width: 80, height: 20, isGround: false },
            // Crane section
            { x: 900, y: 380, width: 40, height: 15, isGround: false },
            { x: 970, y: 350, width: 40, height: 15, isGround: false },
            { x: 1040, y: 320, width: 40, height: 15, isGround: false },
            // Building 3
            { x: 1120, y: 450, width: 180, height: 50, isGround: true },
            { x: 1150, y: 380, width: 60, height: 15, isGround: false },
            { x: 1220, y: 320, width: 60, height: 15, isGround: false },
            // Water tower section
            { x: 1350, y: 400, width: 60, height: 15, isGround: false },
            { x: 1430, y: 360, width: 60, height: 15, isGround: false },
            { x: 1510, y: 320, width: 60, height: 15, isGround: false },
            // Building 4
            { x: 1600, y: 450, width: 200, height: 50, isGround: true },
            { x: 1680, y: 370, width: 80, height: 20, isGround: false },
            // Billboard section
            { x: 1850, y: 380, width: 100, height: 20, isGround: false },
            { x: 1980, y: 340, width: 80, height: 15, isGround: false },
            // Building 5 - Times Square
            { x: 2100, y: 450, width: 250, height: 50, isGround: true },
            { x: 2150, y: 380, width: 60, height: 15, isGround: false },
            { x: 2250, y: 320, width: 60, height: 15, isGround: false },
            // Final stretch
            { x: 2400, y: 400, width: 50, height: 15, isGround: false },
            { x: 2480, y: 360, width: 50, height: 15, isGround: false },
            { x: 2560, y: 320, width: 50, height: 15, isGround: false },
            // Final rooftop
            { x: 2650, y: 450, width: 350, height: 50, isGround: true },
        ];
        
        function loadLevelPlatforms() {
            platforms = currentLevel === 1 ? [...platforms_L1] : [...platforms_L2];
        }

        // Coins - Dynamic based on level
        let coins = [];
        
        function initCoins() {
            if (currentLevel === 1) {
                coins = [
                    { x: 200, y: 330, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 250, y: 330, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 375, y: 270, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 580, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 475, y: 210, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 780, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 910, y: 240, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1130, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1280, y: 240, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1410, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1530, y: 340, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1630, y: 280, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1780, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1680, y: 210, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1880, y: 240, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2080, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2210, y: 360, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2380, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2530, y: 260, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2750, y: 410, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                ];
            } else {
                // Level 2 coins - NYC rooftops
                coins = [
                    { x: 100, y: 410, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 170, y: 340, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 400, y: 380, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 540, y: 300, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 680, y: 330, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 780, y: 260, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 920, y: 340, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1060, y: 280, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1180, y: 340, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1240, y: 280, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1380, y: 360, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1530, y: 280, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1700, y: 330, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 1880, y: 340, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2000, y: 300, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2180, y: 340, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2280, y: 280, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2500, y: 320, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2580, y: 280, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                    { x: 2750, y: 410, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                ];
            }
        }

        // Enemies - Dynamic based on level
        let enemies = [];
        let turtles = [];
        let nycEnemies = []; // NYC specific harder enemies
        
        function initEnemies() {
            if (currentLevel === 1) {
                // Level 1: Standard enemies
                enemies = [
                    { x: 200, y: 412, width: 38, height: 38, patrolLeft: 150, patrolRight: 350, direction: 1, animFrame: 0, health: 1 },
                    { x: 550, y: 412, width: 38, height: 38, patrolLeft: 500, patrolRight: 680, direction: 1, animFrame: 0, health: 1 },
                    { x: 850, y: 412, width: 38, height: 38, patrolLeft: 800, patrolRight: 930, direction: 1, animFrame: 0, health: 1 },
                    { x: 1100, y: 412, width: 38, height: 38, patrolLeft: 1050, patrolRight: 1280, direction: 1, animFrame: 0, health: 1 },
                    { x: 1420, y: 412, width: 38, height: 38, patrolLeft: 1400, patrolRight: 1500, direction: 1, animFrame: 0, health: 1 },
                    { x: 1750, y: 412, width: 38, height: 38, patrolLeft: 1700, patrolRight: 1880, direction: 1, animFrame: 0, health: 1 },
                    { x: 2050, y: 412, width: 38, height: 38, patrolLeft: 2000, patrolRight: 2130, direction: 1, animFrame: 0, health: 1 },
                    { x: 2700, y: 412, width: 38, height: 38, patrolLeft: 2650, patrolRight: 2850, direction: 1, animFrame: 0, health: 1 },
                ];
                turtles = [
                    { x: 280, y: 410, width: 40, height: 40, patrolLeft: 150, patrolRight: 350, direction: -1, animFrame: 0, inShell: false, health: 1 },
                    { x: 620, y: 410, width: 40, height: 40, patrolLeft: 500, patrolRight: 680, direction: -1, animFrame: 0, inShell: false, health: 1 },
                    { x: 910, y: 240, width: 40, height: 40, patrolLeft: 880, patrolRight: 960, direction: -1, animFrame: 0, inShell: false, health: 1 },
                    { x: 1200, y: 410, width: 40, height: 40, patrolLeft: 1050, patrolRight: 1280, direction: -1, animFrame: 0, inShell: false, health: 1 },
                    { x: 1630, y: 282, width: 40, height: 40, patrolLeft: 1600, patrolRight: 1680, direction: 1, animFrame: 0, inShell: false, health: 1 },
                    { x: 1880, y: 240, width: 40, height: 40, patrolLeft: 1850, patrolRight: 1930, direction: -1, animFrame: 0, inShell: false, health: 1 },
                    { x: 2210, y: 360, width: 40, height: 40, patrolLeft: 2180, patrolRight: 2260, direction: 1, animFrame: 0, inShell: false, health: 1 },
                    { x: 2400, y: 410, width: 40, height: 40, patrolLeft: 2300, patrolRight: 2480, direction: -1, animFrame: 0, inShell: false, health: 1 },
                    { x: 2800, y: 410, width: 40, height: 40, patrolLeft: 2650, patrolRight: 2950, direction: -1, animFrame: 0, inShell: false, health: 1 },
                ];
                nycEnemies = [];
            } else {
                // Level 2: Harder NYC enemies - thugs, drones, jumpers
                enemies = []; // No basic enemies in L2
                turtles = []; // No turtles in L2
                nycEnemies = [
                    // Thug type - aggressive, requires 2 hits, shoots discs
                    { x: 200, y: 412, width: 42, height: 45, patrolLeft: 150, patrolRight: 280, direction: 1, type: 'thug', speed: 0.9, health: 2, shootTimer: 0, shootCooldown: 120 },
                    { x: 650, y: 412, width: 42, height: 45, patrolLeft: 600, patrolRight: 780, direction: -1, type: 'thug', speed: 0.8, health: 2, shootTimer: 0, shootCooldown: 100 },
                    // Drone type - flies, shoots discs
                    { x: 400, y: 320, width: 35, height: 35, patrolLeft: 350, patrolRight: 550, direction: 1, type: 'drone', speed: 0.7, health: 1, floatOffset: 0, shootTimer: 0, shootCooldown: 90 },
                    { x: 1000, y: 280, width: 35, height: 35, patrolLeft: 900, patrolRight: 1100, direction: -1, type: 'drone', speed: 0.8, health: 1, floatOffset: Math.PI, shootTimer: 0, shootCooldown: 110 },
                    { x: 1900, y: 300, width: 35, height: 35, patrolLeft: 1830, patrolRight: 2020, direction: 1, type: 'drone', speed: 0.7, health: 1, floatOffset: Math.PI/2, shootTimer: 0, shootCooldown: 100 },
                    // Jumper type - jumps at player
                    { x: 1200, y: 412, width: 40, height: 40, patrolLeft: 1120, patrolRight: 1280, direction: 1, type: 'jumper', speed: 0.8, health: 1, velY: 0, onGround: true, jumpCooldown: 0 },
                    { x: 1700, y: 412, width: 40, height: 40, patrolLeft: 1600, patrolRight: 1780, direction: -1, type: 'jumper', speed: 0.7, health: 1, velY: 0, onGround: true, jumpCooldown: 0 },
                    { x: 2200, y: 412, width: 40, height: 40, patrolLeft: 2100, patrolRight: 2330, direction: 1, type: 'jumper', speed: 0.8, health: 1, velY: 0, onGround: true, jumpCooldown: 0 },
                    // Boss - slow but shoots frequently
                    { x: 2750, y: 405, width: 50, height: 55, patrolLeft: 2680, patrolRight: 2920, direction: 1, type: 'boss', speed: 0.5, health: 4, shootTimer: 0, shootCooldown: 60 },
                ];
            }
            
            // Level 3 - Space Drones
            if (currentLevel === 3) {
                initSpaceDrones();
                initStars();
            }
        }
        
        // Initialize space drones for Level 3
        function initSpaceDrones() {
            spaceDrones = [];
            // Wave 1 - Basic drones
            for (let i = 0; i < 5; i++) {
                spaceDrones.push({
                    x: 900 + i * 200,
                    y: 100 + Math.random() * 300,
                    width: 40,
                    height: 25,
                    type: 'basic',
                    speed: 1.5,
                    health: 1,
                    shootTimer: Math.random() * 60,
                    shootCooldown: 90,
                    waveOffset: Math.random() * Math.PI * 2
                });
            }
            // Wave 2 - Fast drones
            for (let i = 0; i < 4; i++) {
                spaceDrones.push({
                    x: 1800 + i * 250,
                    y: 80 + Math.random() * 340,
                    width: 35,
                    height: 20,
                    type: 'fast',
                    speed: 2.5,
                    health: 1,
                    shootTimer: Math.random() * 40,
                    shootCooldown: 60,
                    waveOffset: Math.random() * Math.PI * 2
                });
            }
            // Wave 3 - Heavy drones
            for (let i = 0; i < 3; i++) {
                spaceDrones.push({
                    x: 2500 + i * 300,
                    y: 120 + Math.random() * 260,
                    width: 55,
                    height: 35,
                    type: 'heavy',
                    speed: 1.0,
                    health: 3,
                    shootTimer: Math.random() * 30,
                    shootCooldown: 50,
                    waveOffset: Math.random() * Math.PI * 2
                });
            }
            // Boss drone at the end
            spaceDrones.push({
                x: 3200,
                y: 200,
                width: 80,
                height: 50,
                type: 'boss',
                speed: 0.8,
                health: 8,
                shootTimer: 0,
                shootCooldown: 30,
                waveOffset: 0
            });
        }
        
        // Initialize stars for space background
        function initStars() {
            stars = [];
            for (let i = 0; i < 100; i++) {
                stars.push({
                    x: Math.random() * 4000,
                    y: Math.random() * canvas.height,
                    size: Math.random() * 2 + 1,
                    speed: Math.random() * 2 + 0.5,
                    brightness: Math.random()
                });
            }
        }

        // Portal - At the end of each level
        let portal = {
            x: 2920,
            y: 300,
            poleHeight: 150,
            animTimer: 0
        };
        
        // Transition effect
        let transitionAlpha = 0;
        let transitionDirection = 0; // 0 = none, 1 = fading out, -1 = fading in

        // Clouds
        const clouds = [
            { x: 100, y: 60, size: 25 },
            { x: 300, y: 40, size: 20 },
            { x: 500, y: 80, size: 30 },
            { x: 700, y: 50, size: 22 },
            { x: 850, y: 70, size: 28 },
        ];

        // Initialize game (called once at start)
        function initGame() {
            player.x = 50;
            player.y = 350;
            player.velX = 0;
            player.velY = 0;
            player.onGround = false;
            player.facingRight = true;
            score = 0;
            totalScore = 0;
            currentLevel = 1;
            gameState = 'title';
            cameraX = 0;
            playerName = '';
            nameInputActive = false;
            disc.active = false;
            transitionAlpha = 0;
            transitionDirection = 0;
            loadLevel(1);
            overlay.style.display = 'none';
        }
        
        // Load a specific level
        function loadLevel(levelNum) {
            currentLevel = levelNum;
            cameraX = 0;
            disc.active = false;
            invincibilityTimer = 0;
            enemyDiscs = [];
            missiles = [];
            droneProjectiles = [];
            
            // Reset health for Level 2 and 3
            if (levelNum >= 2) {
                playerHealth = MAX_HEALTH;
            }
            
            if (levelNum === 3) {
                // Space shooter mode
                jetY = canvas.height / 2 - JET_HEIGHT / 2;
                jetVelY = 0;
                player.width = JET_WIDTH;
                player.height = JET_HEIGHT;
            } else {
                // Platformer mode
                player.x = 50;
                player.y = 350;
                player.velX = 0;
                player.velY = 0;
                player.onGround = false;
                player.width = 36;
                player.height = 48;
            }
            
            updateLevelColors();
            if (levelNum !== 3) {
                loadLevelPlatforms();
            }
            initCoins();
            initEnemies();
        }
        
        // Transition to next level
        function goToNextLevel() {
            totalScore += score;
            score = 0;
            
            if (currentLevel === 1) {
                // Go to Level 2 (NYC)
                gameState = 'transition';
                transitionDirection = 1;
            } else if (currentLevel === 2) {
                // Go to Level 3 (Space)
                gameState = 'transition';
                transitionDirection = 1;
            } else {
                // Won the game after Level 3!
                gameWon();
            }
        }
        
        // Handle transition animation
        function updateTransition() {
            if (transitionDirection === 1) {
                transitionAlpha += 0.02;
                if (transitionAlpha >= 1) {
                    loadLevel(currentLevel + 1);
                    transitionDirection = -1; // Start fade in
                }
            } else if (transitionDirection === -1) {
                transitionAlpha -= 0.02;
                if (transitionAlpha <= 0) {
                    transitionAlpha = 0;
                    transitionDirection = 0;
                    gameState = 'playing';
                }
            }
        }
        
        // Draw transition effect
        function drawTransition() {
            if (transitionAlpha > 0) {
                ctx.fillStyle = `rgba(0, 0, 0, ${transitionAlpha})`;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                if (transitionDirection === 1 && transitionAlpha > 0.5) {
                    let titleText = 'ENTERING NYC DIMENSION';
                    let titleColor = 'rgba(255, 215, 0, ';
                    let subText = '[ USE IDENTITY DISC ]';
                    
                    if (currentLevel === 2) {
                        titleText = 'ENTERING SPACE DIMENSION';
                        titleColor = 'rgba(0, 255, 170, ';
                        subText = '[ PILOT YOUR JET - FIRE MISSILES ]';
                    }
                    
                    ctx.fillStyle = titleColor + `${(transitionAlpha - 0.5) * 2})`;
                    ctx.font = 'bold 32px "Courier New", monospace';
                    ctx.textAlign = 'center';
                    ctx.fillText(titleText, canvas.width / 2, canvas.height / 2);
                    ctx.font = '16px "Courier New", monospace';
                    ctx.fillText('[ CHECKPOINT SAVED ]', canvas.width / 2, canvas.height / 2 + 35);
                    ctx.font = '14px "Courier New", monospace';
                    ctx.fillStyle = `rgba(255, 255, 255, ${(transitionAlpha - 0.5) * 1.5})`;
                    ctx.fillText(subText, canvas.width / 2, canvas.height / 2 + 60);
                    ctx.textAlign = 'left';
                }
            }
        }

        // Draw TRON grid background
        function drawSky() {
            // Dark gradient background
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#000000');
            gradient.addColorStop(0.5, '#050510');
            gradient.addColorStop(1, '#0a0a1a');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw perspective grid floor
            ctx.strokeStyle = COLORS.gridLine;
            ctx.lineWidth = 1;
            
            // Horizontal lines (perspective)
            for (let y = 300; y < canvas.height; y += 20) {
                const intensity = (y - 300) / 200;
                ctx.strokeStyle = `rgba(0, 255, 255, ${0.05 + intensity * 0.15})`;
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }
            
            // Vertical grid lines
            const gridSpacing = 80;
            for (let x = -gridSpacing; x < canvas.width + gridSpacing; x += gridSpacing) {
                ctx.strokeStyle = 'rgba(0, 255, 255, 0.1)';
                ctx.beginPath();
                ctx.moveTo(x, 300);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }
        }

        // Draw distant city/structures (TRON style)
        function drawHills() {
            // Distant buildings/structures silhouette
            ctx.fillStyle = '#0a0a15';
            ctx.beginPath();
            ctx.moveTo(0, 350);
            // Create angular building shapes
            for (let x = 0; x < canvas.width; x += 60) {
                const height = 280 + Math.sin(x * 0.05) * 40 + Math.random() * 20;
                ctx.lineTo(x, height);
                ctx.lineTo(x + 30, height - 20);
                ctx.lineTo(x + 60, height + 10);
            }
            ctx.lineTo(canvas.width, 350);
            ctx.lineTo(canvas.width, canvas.height);
            ctx.lineTo(0, canvas.height);
            ctx.closePath();
            ctx.fill();
            
            // Glowing edges on buildings
            ctx.strokeStyle = 'rgba(0, 255, 255, 0.3)';
            ctx.lineWidth = 1;
            ctx.stroke();
        }

        // Draw data streams (instead of clouds)
        function drawClouds() {
            ctx.strokeStyle = COLORS.cloud;
            ctx.lineWidth = 2;
            clouds.forEach(cloud => {
                const { x, y, size } = cloud;
                // Draw data stream / light ribbon
                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.lineTo(x + size * 2, y);
                ctx.lineTo(x + size * 2.5, y + 3);
                ctx.lineTo(x + size * 0.5, y + 3);
                ctx.closePath();
                ctx.strokeStyle = `rgba(0, 255, 255, ${0.2 + Math.sin(Date.now() / 500 + x) * 0.1})`;
                ctx.stroke();
            });
        }

        // Draw platform - TRON style
        function drawPlatform(p) {
            if (currentLevel === 1) {
                // Level 1: TRON Grid style
                ctx.fillStyle = '#0a0a0a';
                ctx.fillRect(p.x, p.y, p.width, p.height);
                
                ctx.shadowColor = COLORS.grass;
                ctx.shadowBlur = 10;
                ctx.fillStyle = COLORS.grass;
                ctx.fillRect(p.x, p.y, p.width, 3);
                ctx.shadowBlur = 0;
                
                ctx.strokeStyle = `${COLORS.grass}50`;
                ctx.lineWidth = 1;
                
                for (let y = p.y + 8; y < p.y + p.height - 4; y += 8) {
                    ctx.beginPath();
                    ctx.moveTo(p.x + 4, y);
                    ctx.lineTo(p.x + p.width - 4, y);
                    ctx.stroke();
                }
                
                ctx.strokeStyle = `${COLORS.grass}80`;
                ctx.beginPath();
                ctx.moveTo(p.x + 2, p.y + 3);
                ctx.lineTo(p.x + 2, p.y + p.height);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(p.x + p.width - 2, p.y + 3);
                ctx.lineTo(p.x + p.width - 2, p.y + p.height);
                ctx.stroke();
                
                ctx.fillStyle = COLORS.grass;
                ctx.fillRect(p.x, p.y + p.height - 2, 6, 2);
                ctx.fillRect(p.x + p.width - 6, p.y + p.height - 2, 6, 2);
            } else {
                // Level 2: NYC Rooftop/Fire escape style
                // Building/rooftop base
                ctx.fillStyle = '#1a1a1a';
                ctx.fillRect(p.x, p.y, p.width, p.height);
                
                // Darker top edge (rooftop ledge)
                ctx.fillStyle = '#2a2a2a';
                ctx.fillRect(p.x, p.y, p.width, 4);
                
                // Yellow safety stripe on edge (fire escape/rooftop style)
                ctx.shadowColor = '#FFD700';
                ctx.shadowBlur = 5;
                ctx.fillStyle = '#FFD700';
                ctx.fillRect(p.x, p.y, p.width, 2);
                ctx.shadowBlur = 0;
                
                // Brick/metal texture
                ctx.strokeStyle = 'rgba(255, 215, 0, 0.15)';
                ctx.lineWidth = 1;
                for (let brickY = p.y + 8; brickY < p.y + p.height - 4; brickY += 10) {
                    for (let brickX = p.x + 3; brickX < p.x + p.width - 6; brickX += 20) {
                        ctx.strokeRect(brickX, brickY, 16, 8);
                    }
                }
                
                // Graffiti accent (random position)
                if (p.width > 80) {
                    ctx.fillStyle = 'rgba(255, 69, 0, 0.4)';
                    ctx.fillRect(p.x + 20, p.y + 15, 30, 3);
                }
                
                // Metal bolts at corners
                ctx.fillStyle = '#444';
                ctx.fillRect(p.x + 4, p.y + 6, 4, 4);
                ctx.fillRect(p.x + p.width - 8, p.y + 6, 4, 4);
            }
        }

        // Draw player - TRON 8-bit style with circuit patterns
        function drawPlayer() {
            const { x, y, width, height, facingRight } = player;
            const char = characters[selectedCharacter];
            const circuitColor = char.circuitColor || '#00FFFF';
            const secondaryColor = char.secondaryColor || '#0088FF';
            
            // Flash when invincible (Level 2)
            if (currentLevel === 2 && invincibilityTimer > 0) {
                if (Math.floor(invincibilityTimer / 5) % 2 === 0) {
                    return; // Skip drawing every other 5 frames for flashing effect
                }
            }
            
            // Draw player name above character
            if (playerName) {
                ctx.save();
                ctx.font = 'bold 12px "Courier New", monospace';
                ctx.textAlign = 'center';
                const nameWidth = ctx.measureText(playerName).width + 20;
                
                // Dark background with circuit border
                ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
                ctx.fillRect(x + width/2 - nameWidth/2, y - 28, nameWidth, 18);
                
                // Glowing border
                ctx.shadowColor = circuitColor;
                ctx.shadowBlur = 8;
                ctx.strokeStyle = circuitColor;
                ctx.lineWidth = 1;
                ctx.strokeRect(x + width/2 - nameWidth/2, y - 28, nameWidth, 18);
                ctx.shadowBlur = 0;
                
                // Name text with glow
                ctx.shadowColor = circuitColor;
                ctx.shadowBlur = 6;
                ctx.fillStyle = circuitColor;
                ctx.fillText(playerName.toUpperCase(), x + width/2, y - 14);
                ctx.shadowBlur = 0;
                ctx.restore();
            }
            
            // Glow effect on ground
            ctx.shadowColor = circuitColor;
            ctx.shadowBlur = 15;
            ctx.fillStyle = `rgba(${hexToRgb(circuitColor)}, 0.3)`;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height + 2, 14, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            // === 8-BIT TRON BODY ===
            const px = 3; // pixel size for 8-bit look
            
            // Body base (dark suit)
            ctx.fillStyle = '#0a0a0a';
            
            // Torso (blocky 8-bit)
            ctx.fillRect(x + 6, y + 14, 24, 28);
            
            // Head (blocky)
            ctx.fillRect(x + 8, y, 20, 16);
            
            // Legs
            ctx.fillRect(x + 8, y + 42, 8, 12);
            ctx.fillRect(x + 20, y + 42, 8, 12);
            
            // === CIRCUIT LINES (glowing) ===
            ctx.shadowColor = circuitColor;
            ctx.shadowBlur = 8;
            ctx.strokeStyle = circuitColor;
            ctx.fillStyle = circuitColor;
            ctx.lineWidth = 2;
            
            // Helmet visor
            if (char.helmetStyle === 'full' || char.helmetStyle === 'visor') {
                // T-shaped visor
                ctx.fillRect(x + 10, y + 6, 16, 3);
                ctx.fillRect(x + 16, y + 6, 4, 8);
            } else if (char.helmetStyle === 'sleek' || char.helmetStyle === 'elegant') {
                // Curved visor line
                ctx.beginPath();
                ctx.moveTo(x + 10, y + 8);
                ctx.lineTo(x + 26, y + 8);
                ctx.stroke();
                // Eye dots
                ctx.fillRect(x + 12, y + 6, 3, 3);
                ctx.fillRect(x + 21, y + 6, 3, 3);
            } else {
                // Open face with eye line
                ctx.fillRect(x + 10, y + 5, 16, 2);
            }
            
            // Torso circuits based on pattern
            if (char.circuitPattern === 'angular' || char.circuitPattern === 'aggressive') {
                // Angular circuit pattern
                ctx.beginPath();
                ctx.moveTo(x + 18, y + 16);
                ctx.lineTo(x + 18, y + 24);
                ctx.lineTo(x + 10, y + 30);
                ctx.lineTo(x + 10, y + 38);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 18, y + 24);
                ctx.lineTo(x + 26, y + 30);
                ctx.lineTo(x + 26, y + 38);
                ctx.stroke();
            } else if (char.circuitPattern === 'flowing' || char.circuitPattern === 'organic') {
                // Flowing pattern
                ctx.beginPath();
                ctx.moveTo(x + 18, y + 16);
                ctx.lineTo(x + 18, y + 38);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 10, y + 22);
                ctx.lineTo(x + 26, y + 22);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 10, y + 32);
                ctx.lineTo(x + 26, y + 32);
                ctx.stroke();
            } else if (char.circuitPattern === 'symmetric' || char.circuitPattern === 'elegant') {
                // Symmetric V pattern
                ctx.beginPath();
                ctx.moveTo(x + 8, y + 18);
                ctx.lineTo(x + 18, y + 30);
                ctx.lineTo(x + 28, y + 18);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 18, y + 30);
                ctx.lineTo(x + 18, y + 40);
                ctx.stroke();
            } else {
                // Default/legacy pattern
                ctx.beginPath();
                ctx.moveTo(x + 18, y + 16);
                ctx.lineTo(x + 18, y + 40);
                ctx.stroke();
                ctx.fillRect(x + 8, y + 26, 20, 2);
            }
            
            // Shoulder accents
            ctx.fillRect(x + 4, y + 16, 4, 2);
            ctx.fillRect(x + 28, y + 16, 4, 2);
            
            // Arm circuits
            ctx.fillRect(x + 4, y + 20, 2, 16);
            ctx.fillRect(x + 30, y + 20, 2, 16);
            
            // Leg circuits
            ctx.fillRect(x + 10, y + 44, 2, 8);
            ctx.fillRect(x + 24, y + 44, 2, 8);
            
            // Boot tops
            ctx.fillRect(x + 8, y + 50, 8, 2);
            ctx.fillRect(x + 20, y + 50, 8, 2);
            
            // Identity disc on back (secondary color)
            ctx.strokeStyle = secondaryColor;
            ctx.shadowColor = secondaryColor;
            ctx.beginPath();
            if (facingRight) {
                ctx.arc(x + 6, y + 26, 5, 0, Math.PI * 2);
            } else {
                ctx.arc(x + 30, y + 26, 5, 0, Math.PI * 2);
            }
            ctx.stroke();
            
            ctx.shadowBlur = 0;
        }
        
        // Helper to convert hex to rgb
        function hexToRgb(hex) {
            const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? 
                `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : 
                '0, 255, 255';
        }
        
        // Helper function to shade colors
        function shadeColor(color, percent) {
            if (!color) return '#888888';
            const num = parseInt(color.replace('#', ''), 16);
            const amt = Math.round(2.55 * percent);
            const R = Math.max(0, Math.min(255, (num >> 16) + amt));
            const G = Math.max(0, Math.min(255, (num >> 8 & 0x00FF) + amt));
            const B = Math.max(0, Math.min(255, (num & 0x0000FF) + amt));
            return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
        }
        
        // Draw triangular identity disc
        function drawDisc() {
            if (!disc.active) return;
            
            const char = characters[selectedCharacter];
            const discColor = char.circuitColor || '#00FFFF';
            
            ctx.save();
            ctx.translate(disc.x, disc.y);
            ctx.rotate(disc.rotation);
            
            // Glow
            ctx.shadowColor = discColor;
            ctx.shadowBlur = 15;
            
            // Triangular disc shape
            ctx.fillStyle = discColor;
            ctx.beginPath();
            ctx.moveTo(0, -DISC_SIZE);
            ctx.lineTo(DISC_SIZE * 0.866, DISC_SIZE * 0.5);
            ctx.lineTo(-DISC_SIZE * 0.866, DISC_SIZE * 0.5);
            ctx.closePath();
            ctx.fill();
            
            // Inner triangle (darker)
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.moveTo(0, -DISC_SIZE * 0.5);
            ctx.lineTo(DISC_SIZE * 0.433, DISC_SIZE * 0.25);
            ctx.lineTo(-DISC_SIZE * 0.433, DISC_SIZE * 0.25);
            ctx.closePath();
            ctx.fill();
            
            // Center energy core
            ctx.fillStyle = discColor;
            ctx.beginPath();
            ctx.arc(0, 0, 3, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.shadowBlur = 0;
            ctx.restore();
        }
        
        // Throw disc
        function throwDisc() {
            if (disc.active) return; // Can only throw one at a time
            
            disc.active = true;
            disc.x = player.x + player.width / 2;
            disc.y = player.y + player.height / 2;
            disc.velX = player.facingRight ? DISC_SPEED : -DISC_SPEED;
            disc.velY = 0;
            disc.returning = false;
            disc.rotation = 0;
        }
        
        // Update disc
        function updateDisc() {
            if (!disc.active) return;
            
            disc.rotation += 0.3;
            
            if (!disc.returning) {
                disc.x += disc.velX;
                
                // Check if disc should return (max distance or hit wall)
                const distFromPlayer = Math.abs(disc.x - (player.x + player.width / 2));
                if (distFromPlayer > 300 || disc.x < cameraX - 50 || disc.x > cameraX + canvas.width + 50) {
                    disc.returning = true;
                }
            } else {
                // Return to player
                const targetX = player.x + player.width / 2;
                const targetY = player.y + player.height / 2;
                const dx = targetX - disc.x;
                const dy = targetY - disc.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < 20) {
                    disc.active = false;
                } else {
                    disc.x += (dx / dist) * DISC_SPEED * 1.2;
                    disc.y += (dy / dist) * DISC_SPEED * 1.2;
                }
            }
            
            // Check collision with enemies
            checkDiscEnemyCollision();
        }
        
        // Check disc collision with enemies
        function checkDiscEnemyCollision() {
            const discRect = { x: disc.x - DISC_SIZE, y: disc.y - DISC_SIZE, width: DISC_SIZE * 2, height: DISC_SIZE * 2 };
            
            // Check Level 1 enemies
            for (let i = enemies.length - 1; i >= 0; i--) {
                if (checkCollision(discRect, enemies[i])) {
                    enemies[i].health--;
                    if (enemies[i].health <= 0) {
                        enemies.splice(i, 1);
                        score += 10;
                    }
                    disc.returning = true;
                }
            }
            
            // Check turtles
            for (let i = turtles.length - 1; i >= 0; i--) {
                if (checkCollision(discRect, turtles[i])) {
                    turtles[i].health--;
                    if (turtles[i].health <= 0) {
                        turtles.splice(i, 1);
                        score += 15;
                    }
                    disc.returning = true;
                }
            }
            
            // Check NYC enemies (Level 2)
            for (let i = nycEnemies.length - 1; i >= 0; i--) {
                if (checkCollision(discRect, nycEnemies[i])) {
                    nycEnemies[i].health--;
                    if (nycEnemies[i].health <= 0) {
                        const bonus = nycEnemies[i].type === 'boss' ? 100 : 25;
                        score += bonus;
                        nycEnemies.splice(i, 1);
                    }
                    disc.returning = true;
                }
            }
        }
        
        // Draw NYC enemy types - Digital Tron style (black body with red circuit outlines)
        function drawNYCEnemy(enemy) {
            const { x, y, width, height, type, direction, health } = enemy;
            const pulse = 0.7 + Math.sin(Date.now() / 200) * 0.3;
            
            // Ground glow
            ctx.shadowColor = '#FF0044';
            ctx.shadowBlur = 8 * pulse;
            ctx.fillStyle = 'rgba(255, 0, 68, 0.3)';
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height + 2, width/2.5, 3, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            if (type === 'thug' || type === 'boss') {
                // Digital Thug/Boss - 8-bit style, black with red circuit outlines
                const scale = type === 'boss' ? 1.2 : 1;
                
                // Solid black body
                ctx.fillStyle = '#000000';
                ctx.fillRect(x + 6, y + 14, width - 12, height - 18);
                ctx.fillRect(x + 12, y + 2, width - 24, 14);
                ctx.fillRect(x + 10, y + height - 10, 8, 10);
                ctx.fillRect(x + width - 18, y + height - 10, 8, 10);
                
                // Red circuit outlines
                ctx.strokeStyle = '#FF0044';
                ctx.shadowColor = '#FF0044';
                ctx.shadowBlur = 6 * pulse;
                ctx.lineWidth = 2;
                
                // Head outline
                ctx.strokeRect(x + 12, y + 2, width - 24, 14);
                // Body outline
                ctx.strokeRect(x + 6, y + 14, width - 12, height - 18);
                // Leg outlines
                ctx.strokeRect(x + 10, y + height - 10, 8, 10);
                ctx.strokeRect(x + width - 18, y + height - 10, 8, 10);
                
                // Eyes - glowing red pixels
                ctx.fillStyle = '#FF0044';
                ctx.fillRect(x + 16, y + 6, 4, 4);
                ctx.fillRect(x + width - 20, y + 6, 4, 4);
                
                // Circuit pattern on body
                ctx.beginPath();
                ctx.moveTo(x + width/2, y + 16);
                ctx.lineTo(x + width/2, y + height - 12);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 10, y + 24);
                ctx.lineTo(x + width - 10, y + 24);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 10, y + 34);
                ctx.lineTo(x + width - 10, y + 34);
                ctx.stroke();
                
                // Health indicator for boss
                if (type === 'boss' && health > 1) {
                    for (let i = 0; i < health; i++) {
                        ctx.fillRect(x + 8 + i * 12, y - 8, 10, 5);
                    }
                }
                ctx.shadowBlur = 0;
                
            } else if (type === 'drone') {
                // Digital Drone - 8-bit flying disc
                const floatY = y + Math.sin(Date.now() / 120 + enemy.floatOffset) * 6;
                
                // Black body
                ctx.fillStyle = '#000000';
                ctx.beginPath();
                ctx.ellipse(x + width/2, floatY + height/2, width/2 - 2, height/3, 0, 0, Math.PI * 2);
                ctx.fill();
                
                // Red outline
                ctx.strokeStyle = '#FF0044';
                ctx.shadowColor = '#FF0044';
                ctx.shadowBlur = 8 * pulse;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.ellipse(x + width/2, floatY + height/2, width/2 - 2, height/3, 0, 0, Math.PI * 2);
                ctx.stroke();
                
                // Center scanner eye
                ctx.fillStyle = '#FF0044';
                ctx.beginPath();
                ctx.arc(x + width/2, floatY + height/2, 5, 0, Math.PI * 2);
                ctx.fill();
                
                // Side circuit lines
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(x + 4, floatY + height/2);
                ctx.lineTo(x + width/2 - 8, floatY + height/2);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + width/2 + 8, floatY + height/2);
                ctx.lineTo(x + width - 4, floatY + height/2);
                ctx.stroke();
                
                ctx.shadowBlur = 0;
                
            } else if (type === 'jumper') {
                // Digital Jumper - compact 8-bit style
                const squash = enemy.onGround ? 1 : 0.85;
                
                // Black body
                ctx.fillStyle = '#000000';
                ctx.fillRect(x + 6, y + 8 * squash, width - 12, (height - 12) * squash);
                ctx.fillRect(x + 10, y + height - 8, 6, 8);
                ctx.fillRect(x + width - 16, y + height - 8, 6, 8);
                
                // Red outlines
                ctx.strokeStyle = '#FF0044';
                ctx.shadowColor = '#FF0044';
                ctx.shadowBlur = 6 * pulse;
                ctx.lineWidth = 2;
                ctx.strokeRect(x + 6, y + 8 * squash, width - 12, (height - 12) * squash);
                ctx.strokeRect(x + 10, y + height - 8, 6, 8);
                ctx.strokeRect(x + width - 16, y + height - 8, 6, 8);
                
                // Eyes
                ctx.fillStyle = '#FF0044';
                ctx.fillRect(x + 12, y + 14 * squash, 5, 5);
                ctx.fillRect(x + width - 17, y + 14 * squash, 5, 5);
                
                // Circuit lines
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(x + width/2, y + 10 * squash);
                ctx.lineTo(x + width/2, y + (height - 14) * squash);
                ctx.stroke();
                
                ctx.shadowBlur = 0;
            }
        }
        
        // Draw enemy disc (red triangular)
        function drawEnemyDisc(eDisc) {
            ctx.save();
            ctx.translate(eDisc.x, eDisc.y);
            ctx.rotate(eDisc.rotation);
            
            ctx.shadowColor = '#FF0044';
            ctx.shadowBlur = 10;
            
            // Red triangular disc
            ctx.fillStyle = '#FF0044';
            ctx.beginPath();
            ctx.moveTo(0, -ENEMY_DISC_SIZE);
            ctx.lineTo(ENEMY_DISC_SIZE * 0.866, ENEMY_DISC_SIZE * 0.5);
            ctx.lineTo(-ENEMY_DISC_SIZE * 0.866, ENEMY_DISC_SIZE * 0.5);
            ctx.closePath();
            ctx.fill();
            
            // Black center
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(0, 0, 3, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.shadowBlur = 0;
            ctx.restore();
        }
        
        // ========== LEVEL 3 - SPACE SHOOTER FUNCTIONS ==========
        
        // Draw player jet (based on character colors)
        function drawJet() {
            const char = characters[selectedCharacter];
            const mainColor = char.circuitColor || '#00FFFF';
            const secondColor = char.secondaryColor || '#0088FF';
            const jetX = 80; // Fixed X position on screen
            const y = jetY;
            
            // Jet trail/exhaust
            ctx.shadowColor = '#FF6600';
            ctx.shadowBlur = 15;
            ctx.fillStyle = '#FF6600';
            const exhaustFlicker = Math.random() * 10;
            ctx.beginPath();
            ctx.moveTo(jetX - 10, y + JET_HEIGHT/2);
            ctx.lineTo(jetX - 30 - exhaustFlicker, y + JET_HEIGHT/2 - 5);
            ctx.lineTo(jetX - 25 - exhaustFlicker/2, y + JET_HEIGHT/2);
            ctx.lineTo(jetX - 30 - exhaustFlicker, y + JET_HEIGHT/2 + 5);
            ctx.closePath();
            ctx.fill();
            ctx.shadowBlur = 0;
            
            // Main body (fuselage)
            ctx.fillStyle = '#000000';
            ctx.beginPath();
            ctx.moveTo(jetX + JET_WIDTH, y + JET_HEIGHT/2);
            ctx.lineTo(jetX + 10, y);
            ctx.lineTo(jetX - 5, y + 5);
            ctx.lineTo(jetX - 5, y + JET_HEIGHT - 5);
            ctx.lineTo(jetX + 10, y + JET_HEIGHT);
            ctx.closePath();
            ctx.fill();
            
            // Circuit outline
            ctx.strokeStyle = mainColor;
            ctx.shadowColor = mainColor;
            ctx.shadowBlur = 8;
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Wings
            ctx.fillStyle = '#000000';
            // Top wing
            ctx.beginPath();
            ctx.moveTo(jetX + 15, y + 5);
            ctx.lineTo(jetX + 30, y - 12);
            ctx.lineTo(jetX + 40, y - 10);
            ctx.lineTo(jetX + 35, y + 5);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            
            // Bottom wing
            ctx.beginPath();
            ctx.moveTo(jetX + 15, y + JET_HEIGHT - 5);
            ctx.lineTo(jetX + 30, y + JET_HEIGHT + 12);
            ctx.lineTo(jetX + 40, y + JET_HEIGHT + 10);
            ctx.lineTo(jetX + 35, y + JET_HEIGHT - 5);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            
            // Cockpit
            ctx.fillStyle = secondColor;
            ctx.beginPath();
            ctx.ellipse(jetX + 35, y + JET_HEIGHT/2, 10, 6, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Circuit lines on body
            ctx.strokeStyle = mainColor;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(jetX, y + JET_HEIGHT/2);
            ctx.lineTo(jetX + 50, y + JET_HEIGHT/2);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(jetX + 20, y + 8);
            ctx.lineTo(jetX + 20, y + JET_HEIGHT - 8);
            ctx.stroke();
            
            ctx.shadowBlur = 0;
            
            // Draw player name above jet
            if (playerName) {
                ctx.font = 'bold 10px "Courier New", monospace';
                ctx.textAlign = 'center';
                ctx.fillStyle = mainColor;
                ctx.shadowColor = mainColor;
                ctx.shadowBlur = 5;
                ctx.fillText(playerName.toUpperCase(), jetX + JET_WIDTH/2, y - 15);
                ctx.shadowBlur = 0;
                ctx.textAlign = 'left';
            }
        }
        
        // Draw missile (player weapon in Level 3)
        function drawMissile(m) {
            const char = characters[selectedCharacter];
            const missileColor = char.circuitColor || '#00FFFF';
            
            ctx.save();
            ctx.translate(m.x, m.y);
            
            ctx.shadowColor = missileColor;
            ctx.shadowBlur = 10;
            
            // Missile body
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.moveTo(20, 0);
            ctx.lineTo(0, -5);
            ctx.lineTo(-5, -4);
            ctx.lineTo(-5, 4);
            ctx.lineTo(0, 5);
            ctx.closePath();
            ctx.fill();
            
            // Circuit outline
            ctx.strokeStyle = missileColor;
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Exhaust
            ctx.fillStyle = '#FF6600';
            ctx.beginPath();
            ctx.moveTo(-5, -2);
            ctx.lineTo(-12 - Math.random() * 5, 0);
            ctx.lineTo(-5, 2);
            ctx.closePath();
            ctx.fill();
            
            ctx.shadowBlur = 0;
            ctx.restore();
        }
        
        // Draw space drone enemy
        function drawSpaceDrone(drone) {
            const { x, y, width, height, type, health } = drone;
            const pulse = 0.7 + Math.sin(Date.now() / 200) * 0.3;
            
            ctx.save();
            
            // Drone body - black with red circuits
            ctx.fillStyle = '#000000';
            
            if (type === 'basic') {
                // Basic drone - simple design
                ctx.beginPath();
                ctx.ellipse(x + width/2, y + height/2, width/2, height/2, 0, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.strokeStyle = '#FF0044';
                ctx.shadowColor = '#FF0044';
                ctx.shadowBlur = 6 * pulse;
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Eye
                ctx.fillStyle = '#FF0044';
                ctx.beginPath();
                ctx.arc(x + width/2 + 5, y + height/2, 4, 0, Math.PI * 2);
                ctx.fill();
                
            } else if (type === 'fast') {
                // Fast drone - sleek triangle
                ctx.beginPath();
                ctx.moveTo(x + width, y + height/2);
                ctx.lineTo(x, y);
                ctx.lineTo(x + 10, y + height/2);
                ctx.lineTo(x, y + height);
                ctx.closePath();
                ctx.fill();
                
                ctx.strokeStyle = '#FF6600';
                ctx.shadowColor = '#FF6600';
                ctx.shadowBlur = 8 * pulse;
                ctx.lineWidth = 2;
                ctx.stroke();
                
            } else if (type === 'heavy') {
                // Heavy drone - chunky
                ctx.fillRect(x, y, width, height);
                
                ctx.strokeStyle = '#FF0044';
                ctx.shadowColor = '#FF0044';
                ctx.shadowBlur = 6 * pulse;
                ctx.lineWidth = 2;
                ctx.strokeRect(x, y, width, height);
                
                // Cannon
                ctx.fillRect(x + width - 5, y + height/2 - 3, 15, 6);
                ctx.strokeRect(x + width - 5, y + height/2 - 3, 15, 6);
                
                // Health bar for heavy
                if (health > 1) {
                    ctx.fillStyle = '#FF0044';
                    for (let i = 0; i < health; i++) {
                        ctx.fillRect(x + 5 + i * 15, y - 8, 12, 4);
                    }
                }
                
            } else if (type === 'boss') {
                // Boss drone - large and menacing
                ctx.beginPath();
                ctx.moveTo(x + width, y + height/2);
                ctx.lineTo(x + width - 20, y);
                ctx.lineTo(x, y + 10);
                ctx.lineTo(x, y + height - 10);
                ctx.lineTo(x + width - 20, y + height);
                ctx.closePath();
                ctx.fill();
                
                ctx.strokeStyle = '#FF0066';
                ctx.shadowColor = '#FF0066';
                ctx.shadowBlur = 12 * pulse;
                ctx.lineWidth = 3;
                ctx.stroke();
                
                // Multiple guns
                ctx.fillStyle = '#FF0066';
                ctx.fillRect(x + width - 10, y + 10, 20, 8);
                ctx.fillRect(x + width - 10, y + height - 18, 20, 8);
                ctx.fillRect(x + width - 5, y + height/2 - 4, 15, 8);
                
                // Health bar
                ctx.fillStyle = '#FF0066';
                for (let i = 0; i < health; i++) {
                    ctx.fillRect(x + 5 + i * 10, y - 12, 8, 6);
                }
            }
            
            ctx.shadowBlur = 0;
            ctx.restore();
        }
        
        // Draw drone projectile
        function drawDroneProjectile(proj) {
            ctx.save();
            ctx.shadowColor = '#FF0044';
            ctx.shadowBlur = 8;
            ctx.fillStyle = '#FF0044';
            ctx.beginPath();
            ctx.arc(proj.x, proj.y, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.restore();
        }
        
        // Draw space background
        function drawSpaceBackground() {
            // Deep space gradient
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#000011');
            gradient.addColorStop(0.5, '#000022');
            gradient.addColorStop(1, '#001133');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw stars (parallax scrolling)
            stars.forEach(star => {
                const screenX = (star.x - cameraX * 0.3) % canvas.width;
                const twinkle = 0.5 + Math.sin(Date.now() / 200 + star.brightness * 10) * 0.5;
                ctx.fillStyle = `rgba(255, 255, 255, ${twinkle})`;
                ctx.fillRect(screenX, star.y, star.size, star.size);
            });
            
            // Nebula effect
            ctx.fillStyle = 'rgba(0, 100, 150, 0.05)';
            ctx.beginPath();
            ctx.arc(300, 200, 150, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(100, 0, 150, 0.05)';
            ctx.beginPath();
            ctx.arc(600, 350, 120, 0, Math.PI * 2);
            ctx.fill();
        }
        
        // Draw Level 3 finish portal
        function drawSpacePortal() {
            const portalX = 3500 - cameraX;
            const portalY = canvas.height / 2;
            const pulse = 0.6 + Math.sin(Date.now() / 150) * 0.4;
            
            // Only draw if visible
            if (portalX > -100 && portalX < canvas.width + 100) {
                ctx.save();
                
                // Outer glow
                ctx.shadowColor = '#00FFAA';
                ctx.shadowBlur = 30 * pulse;
                ctx.strokeStyle = '#00FFAA';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.ellipse(portalX, portalY, 40, 80, 0, 0, Math.PI * 2);
                ctx.stroke();
                
                // Inner portal
                ctx.fillStyle = `rgba(0, 255, 170, ${0.3 * pulse})`;
                ctx.fill();
                
                // Core
                ctx.fillStyle = '#00FFAA';
                ctx.beginPath();
                ctx.arc(portalX, portalY, 10, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.shadowBlur = 0;
                ctx.restore();
            }
        }
        
        // Update player jet
        function updateJet() {
            // Vertical movement
            if (keys.jump || keys.left) { // Up
                jetVelY = -JET_SPEED;
            } else if (keys.right) { // Down (use right key for down in space mode)
                jetVelY = JET_SPEED;
            } else {
                jetVelY *= 0.9; // Decelerate
            }
            
            jetY += jetVelY;
            
            // Keep in bounds
            if (jetY < 20) jetY = 20;
            if (jetY > canvas.height - JET_HEIGHT - 20) jetY = canvas.height - JET_HEIGHT - 20;
            
            // Auto-scroll camera
            cameraX += 1.5;
            
            // Check if reached end
            if (cameraX > 3400) {
                gameWon();
            }
            
            // Update player position for collision detection
            player.x = 80 + cameraX;
            player.y = jetY;
            player.width = JET_WIDTH;
            player.height = JET_HEIGHT;
        }
        
        // Update missiles
        function updateMissiles() {
            for (let i = missiles.length - 1; i >= 0; i--) {
                const m = missiles[i];
                m.x += MISSILE_SPEED;
                
                // Remove if off screen
                if (m.x > cameraX + canvas.width + 50) {
                    missiles.splice(i, 1);
                    continue;
                }
                
                // Check collision with drones
                for (let j = spaceDrones.length - 1; j >= 0; j--) {
                    const drone = spaceDrones[j];
                    if (m.x > drone.x && m.x < drone.x + drone.width &&
                        m.y > drone.y && m.y < drone.y + drone.height) {
                        drone.health--;
                        missiles.splice(i, 1);
                        if (drone.health <= 0) {
                            const bonus = drone.type === 'boss' ? 200 : (drone.type === 'heavy' ? 50 : 20);
                            score += bonus;
                            spaceDrones.splice(j, 1);
                        }
                        break;
                    }
                }
            }
        }
        
        // Update space drones
        let droneProjectiles = [];
        
        function updateSpaceDrones() {
            const jetCenterY = jetY + JET_HEIGHT / 2;
            
            spaceDrones.forEach(drone => {
                // Wave motion
                const waveY = Math.sin(Date.now() / 500 + drone.waveOffset) * 20;
                
                // Move towards player (scroll with camera but also move left)
                drone.x -= drone.speed * 0.5;
                
                // Shoot at player
                drone.shootTimer++;
                if (drone.shootTimer >= drone.shootCooldown && drone.x < cameraX + canvas.width) {
                    droneProjectiles.push({
                        x: drone.x,
                        y: drone.y + drone.height / 2,
                        velX: -6,
                        velY: (jetCenterY - (drone.y + drone.height/2)) * 0.02
                    });
                    drone.shootTimer = 0;
                }
                
                // Collision with player jet
                const jetRect = { x: 80 + cameraX, y: jetY, width: JET_WIDTH, height: JET_HEIGHT };
                const droneRect = { x: drone.x, y: drone.y, width: drone.width, height: drone.height };
                if (checkCollision(jetRect, droneRect) && invincibilityTimer <= 0) {
                    playerHealth -= 10;
                    invincibilityTimer = 60;
                    if (playerHealth <= 0) gameOver();
                }
            });
            
            // Update projectiles
            for (let i = droneProjectiles.length - 1; i >= 0; i--) {
                const proj = droneProjectiles[i];
                proj.x += proj.velX;
                proj.y += proj.velY;
                
                // Remove if off screen
                if (proj.x < cameraX - 50) {
                    droneProjectiles.splice(i, 1);
                    continue;
                }
                
                // Check collision with player
                if (proj.x > 80 + cameraX - 10 && proj.x < 80 + cameraX + JET_WIDTH + 10 &&
                    proj.y > jetY - 10 && proj.y < jetY + JET_HEIGHT + 10 &&
                    invincibilityTimer <= 0) {
                    playerHealth -= 5;
                    invincibilityTimer = 30;
                    droneProjectiles.splice(i, 1);
                    if (playerHealth <= 0) gameOver();
                }
            }
        }
        
        // Shoot missile
        function shootMissile() {
            missiles.push({
                x: 80 + cameraX + JET_WIDTH,
                y: jetY + JET_HEIGHT / 2
            });
        }
        
        // Update NYC enemies (harder AI with disc shooting)
        function updateNYCEnemies() {
            const playerCenterX = player.x + player.width / 2;
            const playerCenterY = player.y + player.height / 2;
            
            nycEnemies.forEach(enemy => {
                const distToPlayer = Math.abs(enemy.x + enemy.width/2 - playerCenterX);
                const enemyCenterX = enemy.x + enemy.width / 2;
                const enemyCenterY = enemy.y + enemy.height / 2;
                
                if (enemy.type === 'thug' || enemy.type === 'boss') {
                    // Patrol at constant speed
                    enemy.x += enemy.speed * enemy.direction;
                    
                    if (enemy.x <= enemy.patrolLeft) enemy.direction = 1;
                    if (enemy.x + enemy.width >= enemy.patrolRight) enemy.direction = -1;
                    
                    // Shoot disc at player when in range
                    if (enemy.shootTimer !== undefined) {
                        enemy.shootTimer++;
                        if (enemy.shootTimer >= enemy.shootCooldown && distToPlayer < 350) {
                            shootEnemyDisc(enemyCenterX, enemyCenterY, playerCenterX, playerCenterY);
                            enemy.shootTimer = 0;
                        }
                    }
                    
                } else if (enemy.type === 'drone') {
                    // Float and move
                    enemy.x += enemy.speed * enemy.direction;
                    
                    if (enemy.x <= enemy.patrolLeft) enemy.direction = 1;
                    if (enemy.x + enemy.width >= enemy.patrolRight) enemy.direction = -1;
                    
                    // Shoot disc at player
                    if (enemy.shootTimer !== undefined) {
                        enemy.shootTimer++;
                        const floatY = enemy.y + Math.sin(Date.now() / 120 + enemy.floatOffset) * 6;
                        if (enemy.shootTimer >= enemy.shootCooldown && distToPlayer < 300) {
                            shootEnemyDisc(enemyCenterX, floatY + enemy.height/2, playerCenterX, playerCenterY);
                            enemy.shootTimer = 0;
                        }
                    }
                    
                } else if (enemy.type === 'jumper') {
                    // Move and jump at player
                    enemy.x += enemy.speed * enemy.direction;
                    
                    if (enemy.x <= enemy.patrolLeft) enemy.direction = 1;
                    if (enemy.x + enemy.width >= enemy.patrolRight) enemy.direction = -1;
                    
                    // Jump when player is close
                    enemy.jumpCooldown--;
                    if (distToPlayer < 120 && enemy.onGround && enemy.jumpCooldown <= 0) {
                        enemy.velY = -10;
                        enemy.onGround = false;
                        enemy.jumpCooldown = 100;
                    }
                    
                    // Apply gravity
                    if (!enemy.onGround) {
                        enemy.velY += 0.5;
                        enemy.y += enemy.velY;
                        
                        platforms.forEach(p => {
                            if (enemy.y + enemy.height >= p.y && 
                                enemy.y + enemy.height <= p.y + 20 &&
                                enemy.x + enemy.width > p.x && 
                                enemy.x < p.x + p.width) {
                                enemy.y = p.y - enemy.height;
                                enemy.velY = 0;
                                enemy.onGround = true;
                            }
                        });
                    }
                }
                
                // Check collision with player (damage instead of instant death in L2)
                if (checkCollision(player, enemy) && invincibilityTimer <= 0) {
                    playerHealth -= 5;
                    invincibilityTimer = 60; // 1 second invincibility
                    if (playerHealth <= 0) {
                        gameOver();
                    }
                }
            });
        }
        
        // Shoot an enemy disc towards the player
        function shootEnemyDisc(fromX, fromY, toX, toY) {
            const dx = toX - fromX;
            const dy = toY - fromY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist > 0) {
                enemyDiscs.push({
                    x: fromX,
                    y: fromY,
                    velX: (dx / dist) * ENEMY_DISC_SPEED,
                    velY: (dy / dist) * ENEMY_DISC_SPEED,
                    rotation: 0
                });
            }
        }
        
        // Update enemy discs
        function updateEnemyDiscs() {
            for (let i = enemyDiscs.length - 1; i >= 0; i--) {
                const eDisc = enemyDiscs[i];
                eDisc.x += eDisc.velX;
                eDisc.y += eDisc.velY;
                eDisc.rotation += 0.2;
                
                // Remove if off screen
                if (eDisc.x < cameraX - 50 || eDisc.x > cameraX + canvas.width + 50 ||
                    eDisc.y < -50 || eDisc.y > canvas.height + 50) {
                    enemyDiscs.splice(i, 1);
                    continue;
                }
                
                // Check collision with player
                const discRect = { x: eDisc.x - ENEMY_DISC_SIZE, y: eDisc.y - ENEMY_DISC_SIZE, 
                                   width: ENEMY_DISC_SIZE * 2, height: ENEMY_DISC_SIZE * 2 };
                if (checkCollision(player, discRect) && invincibilityTimer <= 0) {
                    playerHealth -= 3;
                    invincibilityTimer = 45; // Brief invincibility
                    enemyDiscs.splice(i, 1);
                    if (playerHealth <= 0) {
                        gameOver();
                    }
                }
            }
        }
        
        // Draw health bar (Level 2 and 3)
        function drawHealthBar() {
            if (currentLevel < 2) return;
            
            const barWidth = 150;
            const barHeight = 12;
            const barX = canvas.width - barWidth - 20;
            const barY = 50;
            
            // Background
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(barX - 5, barY - 5, barWidth + 10, barHeight + 10);
            
            // Border
            ctx.strokeStyle = '#FF0044';
            ctx.lineWidth = 1;
            ctx.strokeRect(barX - 5, barY - 5, barWidth + 10, barHeight + 10);
            
            // Health bar fill
            const healthPercent = playerHealth / MAX_HEALTH;
            const healthWidth = barWidth * healthPercent;
            
            // Color based on health
            let healthColor = '#00FF00';
            if (healthPercent < 0.3) healthColor = '#FF0044';
            else if (healthPercent < 0.6) healthColor = '#FFAA00';
            
            ctx.shadowColor = healthColor;
            ctx.shadowBlur = 8;
            ctx.fillStyle = healthColor;
            ctx.fillRect(barX, barY, healthWidth, barHeight);
            ctx.shadowBlur = 0;
            
            // Health text
            ctx.fillStyle = '#FFFFFF';
            ctx.font = '10px "Courier New", monospace';
            ctx.fillText(`HP: ${playerHealth}/${MAX_HEALTH}`, barX + 5, barY + 9);
        }
        
        // Draw NYC background
        function drawNYCSky() {
            // Night sky gradient
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#0a0a1a');
            gradient.addColorStop(0.4, '#1a1a2e');
            gradient.addColorStop(1, '#2d132c');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Stars
            ctx.fillStyle = '#FFF';
            for (let i = 0; i < 30; i++) {
                const starX = (i * 73 + Date.now() / 100) % canvas.width;
                const starY = (i * 37) % 150;
                const twinkle = Math.sin(Date.now() / 300 + i) * 0.5 + 0.5;
                ctx.globalAlpha = twinkle * 0.6;
                ctx.fillRect(starX, starY, 2, 2);
            }
            ctx.globalAlpha = 1;
        }
        
        // Draw NYC buildings background
        function drawNYCBuildings() {
            // Far buildings silhouette
            ctx.fillStyle = '#0f0f1a';
            for (let x = 0; x < canvas.width; x += 80) {
                const height = 150 + Math.sin(x * 0.02) * 80;
                ctx.fillRect(x, canvas.height - height - 50, 70, height);
                
                // Windows
                ctx.fillStyle = 'rgba(255, 215, 0, 0.3)';
                for (let wy = canvas.height - height - 40; wy < canvas.height - 60; wy += 20) {
                    for (let wx = x + 5; wx < x + 65; wx += 15) {
                        if (Math.random() > 0.3) {
                            ctx.fillRect(wx, wy, 8, 12);
                        }
                    }
                }
                ctx.fillStyle = '#0f0f1a';
            }
            
            // Near buildings
            ctx.fillStyle = '#1a1a2a';
            for (let x = 0; x < canvas.width; x += 120) {
                const height = 80 + Math.sin(x * 0.03 + 1) * 50;
                ctx.fillRect(x - 20, canvas.height - height - 50, 100, height);
            }
            
            // Billboard glow
            ctx.shadowColor = '#FFD700';
            ctx.shadowBlur = 20;
            ctx.fillStyle = '#FFD700';
            ctx.fillRect(400, 200, 100, 40);
            ctx.shadowBlur = 0;
            ctx.fillStyle = '#000';
            ctx.font = 'bold 16px Arial';
            ctx.fillText('NYC', 425, 225);
        }

        // Draw energy bit (TRON style coin)
        function drawCoin(coin) {
            if (coin.collected) return;
            
            const floatY = coin.y + Math.sin(Date.now() / 200 + coin.offset) * 3;
            const pulse = 0.8 + Math.sin(Date.now() / 150 + coin.offset) * 0.2;
            
            // Outer glow
            ctx.shadowColor = COLORS.neonOrange;
            ctx.shadowBlur = 15 * pulse;
            
            // Diamond/bit shape (8-bit style)
            ctx.fillStyle = COLORS.neonOrange;
            ctx.beginPath();
            ctx.moveTo(coin.x + 11, floatY);
            ctx.lineTo(coin.x + 22, floatY + 11);
            ctx.lineTo(coin.x + 11, floatY + 22);
            ctx.lineTo(coin.x, floatY + 11);
            ctx.closePath();
            ctx.fill();
            
            // Inner diamond
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.moveTo(coin.x + 11, floatY + 4);
            ctx.lineTo(coin.x + 18, floatY + 11);
            ctx.lineTo(coin.x + 11, floatY + 18);
            ctx.lineTo(coin.x + 4, floatY + 11);
            ctx.closePath();
            ctx.fill();
            
            // Center dot
            ctx.fillStyle = COLORS.neonOrange;
            ctx.fillRect(coin.x + 9, floatY + 9, 4, 4);
            
            ctx.shadowBlur = 0;
        }

        // Draw enemy - TRON corrupted program / virus
        function drawEnemy(enemy) {
            const { x, y, width, height, animFrame } = enemy;
            const glitch = Math.sin(Date.now() / 100) * 2;
            const pulse = 0.7 + Math.sin(Date.now() / 150) * 0.3;
            
            // Ground glow
            ctx.shadowColor = COLORS.neonRed;
            ctx.shadowBlur = 12;
            ctx.fillStyle = `rgba(255, 0, 68, 0.4)`;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height + 2, width/2, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Body base (dark)
            ctx.shadowBlur = 0;
            ctx.fillStyle = '#0a0a0a';
            ctx.fillRect(x + 4, y + 4, width - 8, height - 8);
            
            // Corrupted circuit lines (red, glitchy)
            ctx.shadowColor = COLORS.neonRed;
            ctx.shadowBlur = 10 * pulse;
            ctx.strokeStyle = COLORS.neonRed;
            ctx.fillStyle = COLORS.neonRed;
            ctx.lineWidth = 2;
            
            // Glitchy head pattern
            ctx.fillRect(x + 8 + glitch, y + 6, 22, 3);
            ctx.fillRect(x + 14, y + 6, 3, 10);
            
            // Body circuits (corrupted/broken pattern)
            ctx.beginPath();
            ctx.moveTo(x + 6, y + 16);
            ctx.lineTo(x + 18 + glitch * 0.5, y + 20);
            ctx.lineTo(x + 6 + glitch, y + 30);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + width - 6, y + 16);
            ctx.lineTo(x + width - 18 - glitch * 0.5, y + 20);
            ctx.lineTo(x + width - 6 - glitch, y + 30);
            ctx.stroke();
            
            // Center corruption symbol
            ctx.fillRect(x + 16, y + 18, 6, 6);
            
            // Glitchy legs
            ctx.fillRect(x + 8, y + height - 12, 3, 10);
            ctx.fillRect(x + width - 11, y + height - 12 + (animFrame === 0 ? 2 : 0), 3, 10);
            
            // Error/corruption marks
            ctx.fillRect(x + 4, y + height - 4, 8, 2);
            ctx.fillRect(x + width - 12, y + height - 4, 8, 2);
            
            // Static/noise effect (random pixels)
            ctx.fillStyle = 'rgba(255, 0, 68, 0.5)';
            for (let i = 0; i < 5; i++) {
                const nx = x + 6 + Math.random() * (width - 12);
                const ny = y + 6 + Math.random() * (height - 12);
                ctx.fillRect(nx, ny, 2, 2);
            }
            
            ctx.shadowBlur = 0;
        }

        // Draw TRON tank/sentinel (replaces turtle)
        function drawTurtle(turtle) {
            const { x, y, width, height, direction, animFrame, inShell } = turtle;
            const hover = Math.sin(Date.now() / 200) * 2;
            const pulse = 0.7 + Math.sin(Date.now() / 180) * 0.3;
            
            // Ground glow
            ctx.shadowColor = COLORS.neonPurple;
            ctx.shadowBlur = 12;
            ctx.fillStyle = `rgba(170, 0, 255, 0.4)`;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height + 2, width/2, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            if (inShell) {
                // Compact mode - just a spinning disc
                ctx.fillStyle = '#0a0a0a';
                ctx.beginPath();
                ctx.ellipse(x + width/2, y + height/2, width/2, height/3, 0, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.shadowColor = COLORS.neonPurple;
                ctx.shadowBlur = 10;
                ctx.strokeStyle = COLORS.neonPurple;
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.shadowBlur = 0;
                return;
            }
            
            // Main body (tank/recognizer shape)
            ctx.fillStyle = '#0a0a0a';
            
            // Upper hull
            ctx.beginPath();
            ctx.moveTo(x + 5, y + 15 + hover);
            ctx.lineTo(x + width - 5, y + 15 + hover);
            ctx.lineTo(x + width - 2, y + 25 + hover);
            ctx.lineTo(x + 2, y + 25 + hover);
            ctx.closePath();
            ctx.fill();
            
            // Lower hull
            ctx.fillRect(x + 4, y + 25 + hover, width - 8, 12);
            
            // Treads/legs
            ctx.fillRect(x, y + height - 8, 10, 8);
            ctx.fillRect(x + width - 10, y + height - 8 + (animFrame === 0 ? 2 : 0), 10, 8);
            
            // Circuit lines
            ctx.shadowColor = COLORS.neonPurple;
            ctx.shadowBlur = 8 * pulse;
            ctx.strokeStyle = COLORS.neonPurple;
            ctx.fillStyle = COLORS.neonPurple;
            ctx.lineWidth = 2;
            
            // Scanner/visor
            const scannerWidth = 20 + Math.sin(Date.now() / 100) * 4;
            ctx.fillRect(x + (width - scannerWidth) / 2, y + 8 + hover, scannerWidth, 4);
            
            // Hull accent lines
            ctx.beginPath();
            ctx.moveTo(x + 8, y + 18 + hover);
            ctx.lineTo(x + width - 8, y + 18 + hover);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(x + 6, y + 28 + hover);
            ctx.lineTo(x + width - 6, y + 28 + hover);
            ctx.stroke();
            
            // Direction indicator
            const indX = direction > 0 ? x + width - 8 : x + 8;
            ctx.fillRect(indX - 2, y + 20 + hover, 4, 8);
            
            // Tread accents
            ctx.fillRect(x + 2, y + height - 6, 6, 2);
            ctx.fillRect(x + width - 8, y + height - 6, 6, 2);
            
            // Energy core
            ctx.beginPath();
            ctx.arc(x + width / 2, y + 22 + hover, 4, 0, Math.PI * 2);
            ctx.stroke();
            
            ctx.shadowBlur = 0;
        }
        
        // Draw exit portal (TRON style)
        function drawFlag() {
            const { x, y, poleHeight, animTimer } = portal;
            const pulse = 0.6 + Math.sin(animTimer / 8) * 0.4;
            const rotation = animTimer * 0.02;
            
            // Portal glow on ground
            ctx.shadowColor = COLORS.neonCyan;
            ctx.shadowBlur = 30 * pulse;
            ctx.fillStyle = `rgba(0, 255, 255, ${0.3 * pulse})`;
            ctx.beginPath();
            ctx.ellipse(x + 25, y + poleHeight, 40, 10, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Portal frame (angular)
            ctx.fillStyle = '#0a0a0a';
            ctx.beginPath();
            ctx.moveTo(x, y + poleHeight);
            ctx.lineTo(x + 10, y);
            ctx.lineTo(x + 40, y);
            ctx.lineTo(x + 50, y + poleHeight);
            ctx.closePath();
            ctx.fill();
            
            // Portal circuits
            ctx.shadowColor = COLORS.neonCyan;
            ctx.shadowBlur = 15 * pulse;
            ctx.strokeStyle = COLORS.neonCyan;
            ctx.lineWidth = 3;
            
            // Outer frame
            ctx.beginPath();
            ctx.moveTo(x + 2, y + poleHeight - 5);
            ctx.lineTo(x + 12, y + 5);
            ctx.lineTo(x + 38, y + 5);
            ctx.lineTo(x + 48, y + poleHeight - 5);
            ctx.stroke();
            
            // Inner portal energy
            ctx.fillStyle = `rgba(0, 255, 255, ${0.2 + pulse * 0.3})`;
            ctx.beginPath();
            ctx.moveTo(x + 15, y + poleHeight - 20);
            ctx.lineTo(x + 18, y + 25);
            ctx.lineTo(x + 32, y + 25);
            ctx.lineTo(x + 35, y + poleHeight - 20);
            ctx.closePath();
            ctx.fill();
            
            // Scanning lines
            for (let i = 0; i < 4; i++) {
                const lineY = y + 40 + i * 25;
                if (lineY < y + poleHeight - 10) {
                    const scanPulse = Math.sin(animTimer / 5 + i) * 0.5 + 0.5;
                    ctx.strokeStyle = `rgba(0, 255, 255, ${scanPulse})`;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(x + 16, lineY);
                    ctx.lineTo(x + 34, lineY);
                    ctx.stroke();
                }
            }
            
            // EXIT text
            ctx.fillStyle = COLORS.neonCyan;
            ctx.font = 'bold 10px "Courier New", monospace';
            ctx.textAlign = 'center';
            ctx.fillText('EXIT', x + 25, y + 18);
            ctx.textAlign = 'left';
            
            // Top accent
            ctx.fillRect(x + 20, y + 2, 10, 3);
            
            ctx.shadowBlur = 0;
        }

        // Draw star shape
        function drawStar(cx, cy, outerR, innerR, points) {
            ctx.beginPath();
            for (let i = 0; i < points * 2; i++) {
                const r = i % 2 === 0 ? outerR : innerR;
                const angle = (i * Math.PI / points) - Math.PI / 2;
                const x = cx + r * Math.cos(angle);
                const y = cy + r * Math.sin(angle);
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fill();
        }

        // Draw UI - TRON style
        function drawUI() {
            // Energy bit counter background
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(15, 12, 120, 30);
            
            // Border
            ctx.strokeStyle = COLORS.neonOrange;
            ctx.lineWidth = 1;
            ctx.strokeRect(15, 12, 120, 30);
            
            // Energy icon (diamond)
            ctx.shadowColor = COLORS.neonOrange;
            ctx.shadowBlur = 8;
            ctx.fillStyle = COLORS.neonOrange;
            ctx.beginPath();
            ctx.moveTo(30, 18);
            ctx.lineTo(40, 27);
            ctx.lineTo(30, 36);
            ctx.lineTo(20, 27);
            ctx.closePath();
            ctx.fill();
            ctx.shadowBlur = 0;
            
            // Inner diamond
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.moveTo(30, 22);
            ctx.lineTo(36, 27);
            ctx.lineTo(30, 32);
            ctx.lineTo(24, 27);
            ctx.closePath();
            ctx.fill();
            
            // Score text
            ctx.fillStyle = COLORS.neonOrange;
            ctx.font = 'bold 16px "Courier New", monospace';
            ctx.fillText(`${score + totalScore} / ${coins.length}`, 50, 32);
            
            // Level indicator
            const levelText = currentLevel === 1 ? 'THE GRID' : (currentLevel === 2 ? 'NYC' : 'SPACE');
            const levelColor = currentLevel === 1 ? '#00FFFF' : (currentLevel === 2 ? '#FFD700' : '#00FFAA');
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(canvas.width - 120, 12, 105, 30);
            ctx.strokeStyle = levelColor;
            ctx.strokeRect(canvas.width - 120, 12, 105, 30);
            ctx.fillStyle = levelColor;
            ctx.shadowColor = levelColor;
            ctx.shadowBlur = 8;
            ctx.font = 'bold 14px "Courier New", monospace';
            ctx.fillText(`LVL ${currentLevel}: ${levelText}`, canvas.width - 115, 32);
            ctx.shadowBlur = 0;
            
            // Weapon indicator (Level 2: Disc, Level 3: Missile)
            if (currentLevel >= 2) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                ctx.fillRect(15, 48, 95, 22);
                const weaponColor = characters[selectedCharacter].circuitColor;
                ctx.fillStyle = currentLevel === 2 && disc.active ? '#555' : weaponColor;
                ctx.font = '12px "Courier New", monospace';
                ctx.fillText(currentLevel === 2 ? '[X] DISC' : '[X] MISSILE', 22, 63);
            }
        }

        // Collision detection
        function checkCollision(rect1, rect2) {
            return rect1.x < rect2.x + rect2.width &&
                   rect1.x + rect1.width > rect2.x &&
                   rect1.y < rect2.y + rect2.height &&
                   rect1.y + rect1.height > rect2.y;
        }

        // Update player
        function updatePlayer() {
            // Apply input
            if (keys.left) {
                player.velX = -PLAYER_SPEED;
                player.facingRight = false;
            } else if (keys.right) {
                player.velX = PLAYER_SPEED;
                player.facingRight = true;
            } else {
                player.velX = 0;
            }
            
            if (keys.jump && player.onGround) {
                player.velY = JUMP_STRENGTH;
                player.onGround = false;
            }
            
            // Apply gravity
            player.velY += GRAVITY;
            if (player.velY > 12) player.velY = 12;
            
            // Move horizontally
            player.x += player.velX;
            
            // Check horizontal collisions
            platforms.forEach(p => {
                if (checkCollision(player, p)) {
                    if (player.velX > 0) {
                        player.x = p.x - player.width;
                    } else if (player.velX < 0) {
                        player.x = p.x + p.width;
                    }
                }
            });
            
            // Move vertically
            player.y += player.velY;
            
            // Check vertical collisions
            player.onGround = false;
            platforms.forEach(p => {
                if (checkCollision(player, p)) {
                    if (player.velY > 0) {
                        player.y = p.y - player.height;
                        player.velY = 0;
                        player.onGround = true;
                    } else if (player.velY < 0) {
                        player.y = p.y + p.height;
                        player.velY = 0;
                    }
                }
            });
            
            // World boundaries (extended level)
            if (player.x < 0) player.x = 0;
            if (player.x > WORLD_WIDTH - player.width) {
                player.x = WORLD_WIDTH - player.width;
            }
            
            // Update camera to follow player
            const targetCameraX = player.x - canvas.width / 3;
            cameraX += (targetCameraX - cameraX) * 0.1; // Smooth camera follow
            
            // Clamp camera to world bounds
            if (cameraX < 0) cameraX = 0;
            if (cameraX > WORLD_WIDTH - canvas.width) cameraX = WORLD_WIDTH - canvas.width;
            
            // Fell off screen
            if (player.y > canvas.height) {
                gameOver();
            }
        }

        // Update coins
        function updateCoins() {
            coins.forEach(coin => {
                if (!coin.collected) {
                    coin.frame = (coin.frame + 0.15) % 8;
                    
                    const coinRect = { x: coin.x, y: coin.y, width: 22, height: 22 };
                    if (checkCollision(player, coinRect)) {
                        coin.collected = true;
                        score++;
                    }
                }
            });
        }

        // Update enemies
        function updateEnemies() {
            enemies.forEach(enemy => {
                enemy.x += 0.8 * enemy.direction;  // Slower enemy movement
                
                if (enemy.x <= enemy.patrolLeft) enemy.direction = 1;
                if (enemy.x >= enemy.patrolRight) enemy.direction = -1;
                
                enemy.animFrame = Math.floor(Date.now() / 200) % 2;
                
                if (checkCollision(player, enemy)) {
                    gameOver();
                }
            });
            
            // Update turtles
            turtles.forEach(turtle => {
                if (!turtle.inShell) {
                    turtle.x += 0.6 * turtle.direction;  // Turtles move slower
                    
                    if (turtle.x <= turtle.patrolLeft) turtle.direction = 1;
                    if (turtle.x >= turtle.patrolRight) turtle.direction = -1;
                }
                
                turtle.animFrame = Math.floor(Date.now() / 200) % 2;
                
                if (checkCollision(player, turtle)) {
                    gameOver();
                }
            });
        }

        // Check flag
        function checkFlag() {
            const portalRect = { x: portal.x - 10, y: portal.y, width: 60, height: portal.poleHeight };
            if (checkCollision(player, portalRect)) {
                goToNextLevel();
            }
        }

        // Game over
        function gameOver() {
            gameState = 'lost';
            const levelName = currentLevel === 1 ? 'THE GRID' : 'NYC';
            overlayTitle.textContent = '⚠ DEREZZED ⚠';
            overlayScore.innerHTML = `${playerName.toUpperCase()} was derezzed in ${levelName}<br>
                <span style="color: #888; font-size: 14px;">Checkpoint: Level ${currentLevel} | Total: ${score + totalScore} bits</span><br>
                <span style="color: #00FFFF; font-size: 12px;">Press R to restart from checkpoint</span>`;
            overlay.style.display = 'flex';
        }

        // Game won - both levels complete!
        function gameWon() {
            const finalScore = score + totalScore;
            gameState = 'won';
            overlayTitle.textContent = '⚡ MISSION COMPLETE ⚡';
            overlayScore.innerHTML = `${playerName.toUpperCase()} escaped both dimensions!<br>
                <span style="color: #FFD700; font-size: 18px;">TOTAL SCORE: ${finalScore} energy bits</span><br>
                <span style="color: #00FFFF; font-size: 12px;">Press R to play again</span>`;
            overlay.style.display = 'flex';
        }

        // Update game
        function update() {
            if (gameState !== 'playing') return;
            
            animationFrame++;
            portal.animTimer++;
            
            // Update invincibility timer
            if (invincibilityTimer > 0) {
                invincibilityTimer--;
            }
            
            // Level 3 - Space shooter mode
            if (currentLevel === 3) {
                updateJet();
                updateMissiles();
                updateSpaceDrones();
                return; // Skip platformer updates
            }
            
            updatePlayer();
            updateCoins();
            updateEnemies();
            
            // Update player disc (Level 2 only)
            if (currentLevel === 2) {
                updateDisc();
            }
            
            // Update NYC enemies for Level 2
            if (currentLevel === 2) {
                updateNYCEnemies();
                updateEnemyDiscs();
            }
            
            checkFlag();
            
            // Move clouds (gentle drift) - Level 1 only
            if (currentLevel === 1) {
                clouds.forEach(cloud => {
                    cloud.x -= 0.15;
                    if (cloud.x < -60) cloud.x = canvas.width + 30;
                });
            }
        }

        // Draw game with camera offset
        function draw() {
            // Show title screen
            if (gameState === 'title') {
                drawTitleScreen();
                return;
            }
            
            // Show character selection
            if (gameState === 'character') {
                drawCharacterSelect();
                return;
            }
            
            // Handle transition
            if (gameState === 'transition') {
                updateTransition();
                drawSky();
                drawTransition();
                return;
            }
            
            // Level 3 - Space Shooter drawing
            if (currentLevel === 3) {
                drawSpaceBackground();
                
                // Draw space elements (with camera offset for scrolling)
                ctx.save();
                ctx.translate(-cameraX, 0);
                
                // Draw missiles
                missiles.forEach(drawMissile);
                
                // Draw drones
                spaceDrones.forEach(drawSpaceDrone);
                
                // Draw drone projectiles
                droneProjectiles.forEach(drawDroneProjectile);
                
                // Draw portal at end
                drawSpacePortal();
                
                ctx.restore();
                
                // Draw jet (fixed position on screen)
                // Flash when invincible
                if (invincibilityTimer <= 0 || Math.floor(invincibilityTimer / 5) % 2 === 1) {
                    drawJet();
                }
                
                // UI
                drawUI();
                drawHealthBar();
                
                // Draw progress bar
                drawProgressBar();
                drawTransition();
                return;
            }
            
            // Draw level-specific background
            if (currentLevel === 1) {
                drawSky();
            } else {
                drawNYCSky();
                drawNYCBuildings();
            }
            
            // Save context and apply camera transform
            ctx.save();
            ctx.translate(-cameraX, 0);
            
            // Draw background elements (parallax - slower)
            if (currentLevel === 1) {
                ctx.save();
                ctx.translate(cameraX * 0.5, 0);
                drawHills();
                ctx.restore();
            }
            
            // Draw clouds with parallax (Level 1 only)
            if (currentLevel === 1) {
                ctx.save();
                ctx.translate(cameraX * 0.7, 0);
                drawClouds();
                ctx.restore();
            }
            
            // Draw game objects
            platforms.forEach(drawPlatform);
            coins.forEach(drawCoin);
            
            // Level 1 enemies
            enemies.forEach(drawEnemy);
            turtles.forEach(drawTurtle);
            
            // Level 2 enemies
            nycEnemies.forEach(drawNYCEnemy);
            
            // Enemy discs (Level 2)
            enemyDiscs.forEach(drawEnemyDisc);
            
            drawFlag();
            drawPlayer();
            
            // Player disc (Level 2 only)
            if (currentLevel === 2) {
                drawDisc();
            }
            
            ctx.restore();
            
            // UI is drawn without camera offset
            drawUI();
            
            // Health bar (Level 2)
            drawHealthBar();
            
            // Draw progress bar at top
            drawProgressBar();
            
            // Draw transition overlay if active
            drawTransition();
        }
        
        // Draw title screen - TRON style
        function drawTitleScreen() {
            const time = Date.now() / 1000;
            
            // Dark gradient background
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#000000');
            gradient.addColorStop(0.5, '#050510');
            gradient.addColorStop(1, '#0a0a1a');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Grid floor
            ctx.strokeStyle = 'rgba(255, 0, 68, 0.1)';
            ctx.lineWidth = 1;
            for (let y = 350; y < canvas.height; y += 15) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }
            for (let x = 0; x < canvas.width; x += 60) {
                ctx.beginPath();
                ctx.moveTo(x, 350);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }
            
            // Animated data streams
            ctx.strokeStyle = 'rgba(255, 0, 68, 0.3)';
            ctx.lineWidth = 2;
            for (let i = 0; i < 8; i++) {
                const streamX = (i * 120 + time * 50) % (canvas.width + 100) - 50;
                const streamY = 50 + i * 20;
                ctx.beginPath();
                ctx.moveTo(streamX, streamY);
                ctx.lineTo(streamX + 40 + Math.sin(time + i) * 10, streamY);
                ctx.stroke();
            }
            
            // Title with neon glow - RED only
            ctx.shadowColor = '#FF0044';
            ctx.shadowBlur = 30;
            ctx.fillStyle = '#FF0044';
            ctx.font = 'bold 44px "Courier New", monospace';
            ctx.textAlign = 'center';
            ctx.fillText('SUPER PRADY BROS', canvas.width / 2, 100);
            ctx.shadowBlur = 0;
            
            // Subtitle
            ctx.shadowColor = COLORS.neonOrange;
            ctx.shadowBlur = 15;
            ctx.fillStyle = COLORS.neonOrange;
            ctx.font = '20px "Courier New", monospace';
            ctx.fillText('[ ENTER THE GRID ]', canvas.width / 2, 140);
            ctx.shadowBlur = 0;
            
            // Draw preview program
            const previewX = canvas.width / 2 - 18;
            const previewY = 180 + Math.sin(time * 2) * 5;
            drawCharacterPreview(previewX, previewY, characters[0]);
            
            // Name input box (angular TRON style)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            const boxX = canvas.width / 2 - 150;
            const boxY = 290;
            ctx.fillRect(boxX, boxY, 300, 45);
            
            // Glowing border
            ctx.shadowColor = nameInputActive ? COLORS.neonOrange : '#FF0044';
            ctx.shadowBlur = nameInputActive ? 15 : 8;
            ctx.strokeStyle = nameInputActive ? COLORS.neonOrange : '#FF0044';
            ctx.lineWidth = 2;
            ctx.strokeRect(boxX, boxY, 300, 45);
            ctx.shadowBlur = 0;
            
            // Label
            ctx.fillStyle = '#FF0044';
            ctx.font = '14px "Courier New", monospace';
            ctx.fillText('ENTER PROGRAM ID:', canvas.width / 2, boxY - 10);
            
            // Name text or placeholder
            ctx.font = 'bold 20px "Courier New", monospace';
            if (playerName) {
                ctx.shadowColor = '#FF0044';
                ctx.shadowBlur = 10;
                ctx.fillStyle = '#FF0044';
                ctx.fillText(playerName.toUpperCase(), canvas.width / 2, boxY + 28);
                ctx.shadowBlur = 0;
            } else {
                ctx.fillStyle = 'rgba(255, 0, 68, 0.3)';
                ctx.fillText('_', canvas.width / 2, boxY + 28);
            }
            
            // Cursor blink
            if (nameInputActive && Math.floor(time * 3) % 2 === 0) {
                const textWidth = ctx.measureText(playerName.toUpperCase()).width;
                ctx.fillStyle = COLORS.neonOrange;
                ctx.fillRect(canvas.width / 2 + textWidth / 2 + 5, boxY + 10, 3, 25);
            }
            
            // Start button
            const canStart = playerName.length >= 1;
            const btnY = 380;
            const pulse = 0.8 + Math.sin(time * 4) * 0.2;
            const btnText = canStart ? '[ SELECT PROGRAM ]' : '[ ENTER ID FIRST ]';
            
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(canvas.width / 2 - 130, btnY, 260, 45);
            
            if (canStart) {
                ctx.shadowColor = '#FF0044';
                ctx.shadowBlur = 15 * pulse;
                ctx.strokeStyle = '#FF0044';
            } else {
                ctx.strokeStyle = 'rgba(255, 0, 68, 0.3)';
            }
            ctx.lineWidth = 2;
            ctx.strokeRect(canvas.width / 2 - 130, btnY, 260, 45);
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = canStart ? '#FF0044' : 'rgba(255, 0, 68, 0.4)';
            ctx.font = 'bold 18px "Courier New", monospace';
            ctx.fillText(btnText, canvas.width / 2, btnY + 28);
            
            // Instructions
            ctx.fillStyle = 'rgba(255, 0, 68, 0.5)';
            ctx.font = '12px "Courier New", monospace';
            ctx.fillText('PRESS ENTER TO CONTINUE', canvas.width / 2, 470);
            
            ctx.textAlign = 'left';
        }
        
        // Draw character selection screen - TRON style carousel
        function drawCharacterSelect() {
            const time = Date.now() / 1000;
            
            // Dark background with grid
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#000000');
            gradient.addColorStop(1, '#0a0a15');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Grid lines
            ctx.strokeStyle = 'rgba(0, 255, 255, 0.08)';
            ctx.lineWidth = 1;
            for (let x = 0; x < canvas.width; x += 40) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }
            for (let y = 0; y < canvas.height; y += 40) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }
            
            // Title
            ctx.shadowColor = COLORS.neonCyan;
            ctx.shadowBlur = 25;
            ctx.fillStyle = COLORS.neonCyan;
            ctx.font = 'bold 36px "Courier New", monospace';
            ctx.textAlign = 'center';
            ctx.fillText('[ SELECT PROGRAM ]', canvas.width / 2, 50);
            ctx.shadowBlur = 0;
            
            // Player ID display
            ctx.fillStyle = COLORS.neonOrange;
            ctx.font = '16px "Courier New", monospace';
            ctx.fillText(`ID: ${playerName.toUpperCase()}`, canvas.width / 2, 75);
            
            // Carousel settings
            const cardWidth = 140;
            const cardHeight = 200;
            const cardY = 100;
            const centerX = canvas.width / 2;
            const cardSpacing = 160;
            
            // Navigation arrows
            ctx.shadowColor = COLORS.neonCyan;
            ctx.shadowBlur = 10;
            ctx.fillStyle = COLORS.neonCyan;
            ctx.font = 'bold 40px "Courier New", monospace';
            ctx.fillText('<', 50, cardY + cardHeight / 2 + 15);
            ctx.fillText('>', canvas.width - 50, cardY + cardHeight / 2 + 15);
            ctx.shadowBlur = 0;
            
            // Draw character cards
            for (let offset = -2; offset <= 2; offset++) {
                let charIndex = (selectedCharacter + offset + characters.length) % characters.length;
                const char = characters[charIndex];
                const isSelected = offset === 0;
                
                const cardX = centerX + offset * cardSpacing - cardWidth / 2;
                const scale = isSelected ? 1.0 : 0.7;
                const opacity = isSelected ? 1.0 : 0.5;
                const yOffset = isSelected ? 0 : 25;
                const pulse = isSelected ? (0.8 + Math.sin(time * 4) * 0.2) : 1;
                
                if (cardX < -cardWidth || cardX > canvas.width + cardWidth) continue;
                
                ctx.save();
                ctx.globalAlpha = opacity;
                
                const scaledWidth = cardWidth * scale;
                const scaledHeight = cardHeight * scale;
                const scaledX = cardX + (cardWidth - scaledWidth) / 2;
                const scaledY = cardY + yOffset + (cardHeight - scaledHeight) / 2;
                
                // Card background (angular TRON style)
                ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
                ctx.fillRect(scaledX, scaledY, scaledWidth, scaledHeight);
                
                // Card border with glow
                if (isSelected) {
                    ctx.shadowColor = char.circuitColor;
                    ctx.shadowBlur = 20 * pulse;
                    ctx.strokeStyle = char.circuitColor;
                    ctx.lineWidth = 3;
                } else {
                    ctx.strokeStyle = 'rgba(0, 255, 255, 0.3)';
                    ctx.lineWidth = 1;
                }
                ctx.strokeRect(scaledX, scaledY, scaledWidth, scaledHeight);
                ctx.shadowBlur = 0;
                
                // Corner accents
                if (isSelected) {
                    ctx.fillStyle = char.circuitColor;
                    ctx.fillRect(scaledX, scaledY, 15, 3);
                    ctx.fillRect(scaledX, scaledY, 3, 15);
                    ctx.fillRect(scaledX + scaledWidth - 15, scaledY, 15, 3);
                    ctx.fillRect(scaledX + scaledWidth - 3, scaledY, 3, 15);
                    ctx.fillRect(scaledX, scaledY + scaledHeight - 3, 15, 3);
                    ctx.fillRect(scaledX, scaledY + scaledHeight - 15, 3, 15);
                    ctx.fillRect(scaledX + scaledWidth - 15, scaledY + scaledHeight - 3, 15, 3);
                    ctx.fillRect(scaledX + scaledWidth - 3, scaledY + scaledHeight - 15, 3, 15);
                }
                
                // Character preview
                ctx.save();
                ctx.translate(scaledX + scaledWidth / 2, scaledY + scaledHeight / 2 - 20);
                ctx.scale(scale * 1.2, scale * 1.2);
                ctx.translate(-18, -30);
                drawCharacterPreview(0, 0, char);
                ctx.restore();
                
                // Character name
                ctx.shadowColor = char.circuitColor;
                ctx.shadowBlur = isSelected ? 10 : 0;
                ctx.fillStyle = isSelected ? char.circuitColor : 'rgba(255, 255, 255, 0.7)';
                ctx.font = `bold ${Math.floor(14 * scale)}px "Courier New", monospace`;
                ctx.fillText(char.name, scaledX + scaledWidth / 2, scaledY + scaledHeight - 35 * scale);
                
                // Description
                ctx.shadowBlur = 0;
                ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
                ctx.font = `${Math.floor(10 * scale)}px "Courier New", monospace`;
                ctx.fillText(char.description, scaledX + scaledWidth / 2, scaledY + scaledHeight - 18 * scale);
                
                ctx.restore();
            }
            
            // Program counter
            ctx.fillStyle = 'rgba(0, 255, 255, 0.7)';
            ctx.font = '14px "Courier New", monospace';
            ctx.fillText(`[ ${selectedCharacter + 1} / ${characters.length} ]`, canvas.width / 2, 340);
            
            // Navigation hints
            ctx.fillStyle = 'rgba(0, 255, 255, 0.5)';
            ctx.font = '12px "Courier New", monospace';
            ctx.fillText('< > SELECT  |  ENTER INITIALIZE', canvas.width / 2, 365);
            
            // Initialize button
            const btnY = 395;
            ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
            ctx.fillRect(canvas.width / 2 - 120, btnY, 240, 45);
            
            const selectedChar = characters[selectedCharacter];
            ctx.shadowColor = selectedChar.circuitColor;
            ctx.shadowBlur = 15;
            ctx.strokeStyle = selectedChar.circuitColor;
            ctx.lineWidth = 2;
            ctx.strokeRect(canvas.width / 2 - 120, btnY, 240, 45);
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = selectedChar.circuitColor;
            ctx.font = 'bold 16px "Courier New", monospace';
            ctx.fillText(`[ INITIALIZE ${selectedChar.name} ]`, canvas.width / 2, btnY + 28);
            
            // Back hint
            ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.font = '11px "Courier New", monospace';
            ctx.fillText('ESC: RETURN', canvas.width / 2, 475);
            
            ctx.textAlign = 'left';
        }
        
        // Draw character preview - TRON 8-bit style
        function drawCharacterPreview(x, y, char) {
            const floatY = y + Math.sin(Date.now() / 300) * 3;
            const circuitColor = char.circuitColor || '#00FFFF';
            const secondaryColor = char.secondaryColor || '#0088FF';
            const pulse = 0.7 + Math.sin(Date.now() / 200) * 0.3;
            
            // Ground glow
            ctx.shadowColor = circuitColor;
            ctx.shadowBlur = 12 * pulse;
            ctx.fillStyle = `rgba(${hexToRgb(circuitColor)}, 0.3)`;
            ctx.beginPath();
            ctx.ellipse(x + 18, y + 58, 12, 3, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            // === 8-BIT TRON BODY ===
            
            // Body base (dark suit)
            ctx.fillStyle = '#0a0a0a';
            
            // Torso
            ctx.fillRect(x + 6, floatY + 14, 24, 28);
            
            // Head
            ctx.fillRect(x + 8, floatY, 20, 16);
            
            // Legs
            ctx.fillRect(x + 8, floatY + 42, 8, 12);
            ctx.fillRect(x + 20, floatY + 42, 8, 12);
            
            // === CIRCUIT LINES ===
            ctx.shadowColor = circuitColor;
            ctx.shadowBlur = 8 * pulse;
            ctx.strokeStyle = circuitColor;
            ctx.fillStyle = circuitColor;
            ctx.lineWidth = 2;
            
            // Helmet/visor based on style
            if (char.helmetStyle === 'full' || char.helmetStyle === 'visor') {
                ctx.fillRect(x + 10, floatY + 6, 16, 3);
                ctx.fillRect(x + 16, floatY + 6, 4, 8);
            } else if (char.helmetStyle === 'sleek' || char.helmetStyle === 'elegant' || char.helmetStyle === 'feminine') {
                ctx.beginPath();
                ctx.moveTo(x + 10, floatY + 8);
                ctx.lineTo(x + 26, floatY + 8);
                ctx.stroke();
                ctx.fillRect(x + 12, floatY + 6, 3, 3);
                ctx.fillRect(x + 21, floatY + 6, 3, 3);
            } else if (char.helmetStyle === 'stylish') {
                ctx.fillRect(x + 8, floatY + 4, 20, 2);
                ctx.fillRect(x + 10, floatY + 8, 16, 2);
            } else {
                ctx.fillRect(x + 10, floatY + 5, 16, 2);
            }
            
            // Torso circuit pattern
            if (char.circuitPattern === 'angular' || char.circuitPattern === 'aggressive') {
                ctx.beginPath();
                ctx.moveTo(x + 18, floatY + 16);
                ctx.lineTo(x + 18, floatY + 24);
                ctx.lineTo(x + 10, floatY + 30);
                ctx.lineTo(x + 10, floatY + 38);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 18, floatY + 24);
                ctx.lineTo(x + 26, floatY + 30);
                ctx.lineTo(x + 26, floatY + 38);
                ctx.stroke();
            } else if (char.circuitPattern === 'flowing' || char.circuitPattern === 'organic') {
                ctx.beginPath();
                ctx.moveTo(x + 18, floatY + 16);
                ctx.lineTo(x + 18, floatY + 38);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 10, floatY + 22);
                ctx.lineTo(x + 26, floatY + 22);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 10, floatY + 32);
                ctx.lineTo(x + 26, floatY + 32);
                ctx.stroke();
            } else if (char.circuitPattern === 'symmetric' || char.circuitPattern === 'elegant') {
                ctx.beginPath();
                ctx.moveTo(x + 8, floatY + 18);
                ctx.lineTo(x + 18, floatY + 30);
                ctx.lineTo(x + 28, floatY + 18);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 18, floatY + 30);
                ctx.lineTo(x + 18, floatY + 40);
                ctx.stroke();
            } else if (char.circuitPattern === 'flashy') {
                ctx.fillRect(x + 8, floatY + 18, 20, 2);
                ctx.fillRect(x + 8, floatY + 26, 20, 2);
                ctx.fillRect(x + 8, floatY + 34, 20, 2);
                ctx.fillRect(x + 16, floatY + 16, 4, 24);
            } else {
                ctx.beginPath();
                ctx.moveTo(x + 18, floatY + 16);
                ctx.lineTo(x + 18, floatY + 40);
                ctx.stroke();
                ctx.fillRect(x + 8, floatY + 26, 20, 2);
            }
            
            // Shoulder accents
            ctx.fillRect(x + 4, floatY + 16, 4, 2);
            ctx.fillRect(x + 28, floatY + 16, 4, 2);
            
            // Arm circuits
            ctx.fillRect(x + 4, floatY + 20, 2, 16);
            ctx.fillRect(x + 30, floatY + 20, 2, 16);
            
            // Leg circuits
            ctx.fillRect(x + 10, floatY + 44, 2, 8);
            ctx.fillRect(x + 24, floatY + 44, 2, 8);
            
            // Boot tops
            ctx.fillRect(x + 8, floatY + 50, 8, 2);
            ctx.fillRect(x + 20, floatY + 50, 8, 2);
            
            // Identity disc (secondary color)
            ctx.strokeStyle = secondaryColor;
            ctx.shadowColor = secondaryColor;
            ctx.beginPath();
            ctx.arc(x + 30, floatY + 26, 5, 0, Math.PI * 2);
            ctx.stroke();
            
            ctx.shadowBlur = 0;
        }
        
        // Draw player at specific position (for title screen preview)
        function drawPlayerAt(x, y, facingRight) {
            drawCharacterPreview(x, y, characters[0]);
        }

        // Draw level progress bar - TRON style
        function drawProgressBar() {
            // Level 3 uses camera position for progress
            const worldWidth = currentLevel === 3 ? 3500 : WORLD_WIDTH;
            const progress = currentLevel === 3 ? cameraX / worldWidth : player.x / worldWidth;
            const barWidth = 200;
            const barHeight = 6;
            const barX = canvas.width - barWidth - 20;
            const barY = 20;
            
            // Background
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(barX - 3, barY - 3, barWidth + 6, barHeight + 6);
            
            // Border
            ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
            ctx.lineWidth = 1;
            ctx.strokeRect(barX - 3, barY - 3, barWidth + 6, barHeight + 6);
            
            // Progress track
            ctx.fillStyle = '#111';
            ctx.fillRect(barX, barY, barWidth, barHeight);
            
            // Progress fill with glow
            ctx.shadowColor = COLORS.neonCyan;
            ctx.shadowBlur = 10;
            ctx.fillStyle = COLORS.neonCyan;
            ctx.fillRect(barX, barY, barWidth * progress, barHeight);
            ctx.shadowBlur = 0;
            
            // Exit portal indicator
            ctx.fillStyle = COLORS.neonCyan;
            ctx.font = '10px "Courier New", monospace';
            ctx.fillText('EXIT', barX + barWidth + 8, barY + 6);
            
            // Sector markers
            ctx.fillStyle = 'rgba(0, 255, 255, 0.3)';
            for (let i = 1; i < 4; i++) {
                ctx.fillRect(barX + (barWidth / 4) * i, barY, 1, barHeight);
            }
        }

        // Game loop
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        // Keyboard input
        document.addEventListener('keydown', (e) => {
            // Title screen input
            if (gameState === 'title') {
                if (nameInputActive) {
                    if (e.key === 'Backspace') {
                        playerName = playerName.slice(0, -1);
                        e.preventDefault();
                    } else if (e.key === 'Enter' && playerName.length >= 1) {
                        goToCharacterSelect();
                    } else if (e.key.length === 1 && playerName.length < 12) {
                        // Only allow letters, numbers, and some symbols
                        if (/^[a-zA-Z0-9_\- ]$/.test(e.key)) {
                            playerName += e.key;
                        }
                    }
                    e.preventDefault();
                    return;
                }
                
                if (e.key === 'Enter' && playerName.length >= 1) {
                    goToCharacterSelect();
                }
                return;
            }
            
            // Character selection input
            if (gameState === 'character') {
                if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
                    selectedCharacter = (selectedCharacter - 1 + characters.length) % characters.length;
                }
                if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
                    selectedCharacter = (selectedCharacter + 1) % characters.length;
                }
                if (e.key === 'Enter' || e.key === ' ') {
                    startGame();
                }
                if (e.key === 'Escape' || e.key === 'Backspace') {
                    gameState = 'title';
                }
                e.preventDefault();
                return;
            }
            
            if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = true;
            if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = true;
            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W' || e.key === ' ') keys.jump = true;
            
            // Throw disc (Level 2) or shoot missile (Level 3)
            if ((e.key === 'x' || e.key === 'X' || e.key === 'k' || e.key === 'K') && gameState === 'playing') {
                if (currentLevel === 2) {
                    throwDisc();
                } else if (currentLevel === 3) {
                    shootMissile();
                }
            }
            
            if ((e.key === 'r' || e.key === 'R') && (gameState === 'won' || gameState === 'lost')) {
                if (gameState === 'lost') {
                    // Restart from checkpoint (current level)
                    resetGame();
                } else {
                    // Won - go back to beginning for a new game
                    restartFromBeginning();
                }
            }
            
            // Prevent scrolling
            if (['ArrowUp', 'ArrowDown', ' '].includes(e.key)) {
                e.preventDefault();
            }
        });

        document.addEventListener('keyup', (e) => {
            if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = false;
            if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = false;
            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W' || e.key === ' ') keys.jump = false;
        });
        
        // Go to character selection from title
        function goToCharacterSelect() {
            gameState = 'character';
            nameInputActive = false;
        }
        
        // Start game from character selection
        function startGame() {
            gameState = 'playing';
            nameInputActive = false;
            resetGame();
        }
        
        // Reset game (keep the player name)
        function resetGame() {
            // Restart at current checkpoint level
            score = 0;
            disc.active = false;
            gameState = 'playing';
            cameraX = 0;
            
            // Reset health for Level 2 and 3
            if (currentLevel >= 2) {
                playerHealth = MAX_HEALTH;
            }
            invincibilityTimer = 0;
            enemyDiscs = [];
            missiles = [];
            droneProjectiles = [];
            
            if (currentLevel === 3) {
                // Space shooter mode reset
                jetY = canvas.height / 2 - JET_HEIGHT / 2;
                jetVelY = 0;
                player.width = JET_WIDTH;
                player.height = JET_HEIGHT;
                initSpaceDrones();
                initStars();
            } else {
                // Platformer mode reset
                player.x = 50;
                player.y = 350;
                player.velX = 0;
                player.velY = 0;
                player.onGround = false;
                player.facingRight = true;
                player.width = 36;
                player.height = 48;
                loadLevelPlatforms();
            }
            
            // Keep totalScore from previous levels
            initCoins();
            initEnemies();
            overlay.style.display = 'none';
        }
        
        // Restart from beginning (after winning or returning to character select)
        function restartFromBeginning() {
            currentLevel = 1;
            totalScore = 0;
            updateLevelColors();
            loadLevel(1);
            gameState = 'character';
            overlay.style.display = 'none';
        }

        // Mobile controls
        const btnLeft = document.getElementById('btnLeft');
        const btnRight = document.getElementById('btnRight');
        const btnJump = document.getElementById('btnJump');

        btnLeft.addEventListener('touchstart', (e) => { e.preventDefault(); keys.left = true; });
        btnLeft.addEventListener('touchend', (e) => { e.preventDefault(); keys.left = false; });
        btnRight.addEventListener('touchstart', (e) => { e.preventDefault(); keys.right = true; });
        btnRight.addEventListener('touchend', (e) => { e.preventDefault(); keys.right = false; });
        btnJump.addEventListener('touchstart', (e) => { e.preventDefault(); keys.jump = true; });
        btnJump.addEventListener('touchend', (e) => { e.preventDefault(); keys.jump = false; });

        // Click handler for title screen and focus
        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const clickY = e.clientY - rect.top;
            
            if (gameState === 'title') {
                // Check if clicked on name input box
                const boxX = canvas.width / 2 - 150;
                const boxY = 300;
                if (clickX >= boxX && clickX <= boxX + 300 && clickY >= boxY && clickY <= boxY + 50) {
                    nameInputActive = true;
                } else {
                    nameInputActive = false;
                }
                
                // Check if clicked on start button
                const btnY = 400;
                const btnWidth = 280;
                if (playerName.length >= 1 && clickX >= canvas.width / 2 - btnWidth / 2 && clickX <= canvas.width / 2 + btnWidth / 2 && clickY >= btnY && clickY <= btnY + 50) {
                    goToCharacterSelect();
                }
            }
            
            if (gameState === 'character') {
                // Check if clicked on left arrow
                if (clickX >= 20 && clickX <= 80 && clickY >= 180 && clickY <= 280) {
                    selectedCharacter = (selectedCharacter - 1 + characters.length) % characters.length;
                }
                
                // Check if clicked on right arrow
                if (clickX >= canvas.width - 80 && clickX <= canvas.width - 20 && clickY >= 180 && clickY <= 280) {
                    selectedCharacter = (selectedCharacter + 1) % characters.length;
                }
                
                // Check if clicked on left character card
                const centerX = canvas.width / 2;
                if (clickX >= centerX - 270 && clickX <= centerX - 90 && clickY >= 140 && clickY <= 340) {
                    selectedCharacter = (selectedCharacter - 1 + characters.length) % characters.length;
                }
                
                // Check if clicked on right character card
                if (clickX >= centerX + 90 && clickX <= centerX + 270 && clickY >= 140 && clickY <= 340) {
                    selectedCharacter = (selectedCharacter + 1) % characters.length;
                }
                
                // Check if clicked on play button
                const btnY = 420;
                if (clickX >= canvas.width / 2 - 120 && clickX <= canvas.width / 2 + 120 && clickY >= btnY && clickY <= btnY + 50) {
                    startGame();
                }
            }
            
            // Throw disc (Level 2) or shoot missile (Level 3) on click
            if (gameState === 'playing') {
                if (currentLevel === 2) {
                    throwDisc();
                } else if (currentLevel === 3) {
                    shootMissile();
                }
            }
            
            canvas.focus();
        });

        // Start game
        initGame();
        gameLoop();
    </script>
</body>
</html>
"""

# Embed the game
st.components.v1.html(game_html, height=560, scrolling=False)

# Controls section
st.markdown("""
<div class="controls-box">
    <strong>⚡ CONTROLS:</strong><br>
    <kbd>← →</kbd> or <kbd>A D</kbd> MOVE &nbsp;|&nbsp; 
    <kbd>SPACE</kbd> or <kbd>↑</kbd> JUMP &nbsp;|&nbsp;
    <kbd>X</kbd> or <kbd>CLICK</kbd> THROW DISC &nbsp;|&nbsp;
    <kbd>R</kbd> REBOOT
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("⚡ **Collect** energy bits!")
with col2:
    st.markdown("🔺 **Throw** your identity disc!")
with col3:
    st.markdown("🚀 **3 Levels**: Grid → NYC → Space!")
with col4:
    st.markdown("🚪 **Reach** the portal!")



