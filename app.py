"""
🍄 Super Prady Bros - Web Version 🍄
A Mario-style platformer game that runs in your browser via Streamlit!
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="🍄 Super Prady Bros",
    page_icon="🍄",
    layout="wide"
)

# Hide Streamlit's default menu and footer for a cleaner game experience
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    .game-title {
        text-align: center;
        font-family: 'Press Start 2P', cursive, monospace;
        color: #ffd700;
        text-shadow: 3px 3px 0px #c73659, 6px 6px 0px #1a1a2e;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .game-subtitle {
        text-align: center;
        color: #87ceeb;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .controls-box {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px auto;
        max-width: 600px;
        text-align: center;
        color: white;
    }
    .controls-box kbd {
        background: #333;
        padding: 5px 10px;
        border-radius: 5px;
        margin: 0 5px;
        border: 1px solid #555;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="game-title">🍄 Super Prady Bros 🍄</h1>', unsafe_allow_html=True)
st.markdown('<p class="game-subtitle">A Mario-Style Platformer Game</p>', unsafe_allow_html=True)

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
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 0 4px #ffd700;
        }
        #gameCanvas {
            display: block;
            background: #87CEEB;
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
            background: rgba(0,0,0,0.7);
            color: white;
            font-size: 24px;
            text-align: center;
            display: none;
        }
        #overlay h1 {
            font-size: 48px;
            margin-bottom: 20px;
            text-shadow: 3px 3px 0 #c73659;
        }
        #overlay p {
            margin: 10px 0;
        }
        #overlay .restart-hint {
            margin-top: 30px;
            font-size: 18px;
            color: #ffd700;
            animation: pulse 1.5s infinite;
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
            <p class="restart-hint">Press R to choose character & play again</p>
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

        // Colors
        const COLORS = {
            skyTop: '#87CEEB',
            skyBottom: '#B0E0E6',
            ground: '#8B5A2B',
            grass: '#228B22',
            platform: '#A0522D',
            platformTop: '#32CD32',
            player: '#DC143C',
            playerFace: '#FFDAB9',
            coin: '#FFD700',
            coinShine: '#FFFFC8',
            enemy: '#CC0000',
            flagPole: '#8B4513',
            flag: '#00FF7F',
            cloud: '#FFFFFF',
            text: '#FFFFFF',
            textShadow: '#323232'
        };

        // Game state
        let gameState = 'title'; // 'title', 'character', 'playing', 'won', 'lost'
        let score = 0;
        let animationFrame = 0;
        let playerName = '';
        let nameInputActive = false;
        let selectedCharacter = 0;
        
        // Available characters - each with unique features
        const characters = [
            { 
                name: 'Mario', 
                color: '#DC143C', 
                hatColor: '#DC143C',
                shirtColor: '#DC143C',
                pantsColor: '#00008B',
                description: 'The classic hero!',
                gender: 'male',
                skinTone: '#FFDAB9',
                eyeColor: '#4169E1',
                hairColor: '#5D4037',
                hasHat: true,
                hasMustache: true,
                hairStyle: 'none'
            },
            { 
                name: 'Luigi', 
                color: '#228B22', 
                hatColor: '#228B22',
                shirtColor: '#228B22',
                pantsColor: '#00008B',
                description: 'Tall & brave!',
                gender: 'male',
                skinTone: '#FFDAB9',
                eyeColor: '#228B22',
                hairColor: '#5D4037',
                hasHat: true,
                hasMustache: true,
                hairStyle: 'none'
            },
            { 
                name: 'Peach', 
                color: '#FFB6C1', 
                hatColor: '#FFD700',
                shirtColor: '#FFB6C1',
                pantsColor: '#FF69B4',
                description: 'Royal & graceful!',
                gender: 'female',
                skinTone: '#FFE4C4',
                eyeColor: '#4169E1',
                hairColor: '#FFD700',
                hasHat: false,
                hasMustache: false,
                hairStyle: 'long',
                hasCrown: true
            },
            { 
                name: 'Prady', 
                color: '#FFD700', 
                hatColor: '#FFD700',
                shirtColor: '#FF8C00',
                pantsColor: '#8B4513',
                description: 'The golden champion!',
                gender: 'male',
                skinTone: '#D2691E',
                eyeColor: '#8B4513',
                hairColor: '#1a1a1a',
                hasHat: true,
                hasMustache: false,
                hairStyle: 'short'
            },
            { 
                name: 'Rosa', 
                color: '#00CED1', 
                hatColor: '#00CED1',
                shirtColor: '#40E0D0',
                pantsColor: '#008B8B',
                description: 'Swift & clever!',
                gender: 'female',
                skinTone: '#8B5A2B',
                eyeColor: '#00CED1',
                hairColor: '#1a1a1a',
                hasHat: false,
                hasMustache: false,
                hairStyle: 'curly'
            },
            { 
                name: 'Shadow', 
                color: '#4B0082', 
                hatColor: '#4B0082',
                shirtColor: '#2F0052',
                pantsColor: '#1a1a2e',
                description: 'Dark & mysterious!',
                gender: 'male',
                skinTone: '#C9A86C',
                eyeColor: '#9400D3',
                hairColor: '#1a1a1a',
                hasHat: true,
                hasMustache: false,
                hairStyle: 'spiky'
            },
            { 
                name: 'Daisy', 
                color: '#FFA500', 
                hatColor: '#FFA500',
                shirtColor: '#FFD700',
                pantsColor: '#FF8C00',
                description: 'Sporty & fun!',
                gender: 'female',
                skinTone: '#FFDAB9',
                eyeColor: '#228B22',
                hairColor: '#8B4513',
                hasHat: false,
                hasMustache: false,
                hairStyle: 'ponytail',
                hasCrown: true
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

        // Platforms - Extended scrollable level
        const platforms = [
            // Section 1: Starting area
            { x: 0, y: 450, width: 400, height: 50, isGround: true },
            { x: 180, y: 370, width: 100, height: 25, isGround: false },
            { x: 350, y: 310, width: 90, height: 25, isGround: false },
            
            // Section 2: First gap
            { x: 500, y: 450, width: 200, height: 50, isGround: true },
            { x: 550, y: 350, width: 100, height: 25, isGround: false },
            { x: 450, y: 250, width: 90, height: 25, isGround: false },
            
            // Section 3: Platforming challenge
            { x: 800, y: 450, width: 150, height: 50, isGround: true },
            { x: 750, y: 350, width: 80, height: 25, isGround: false },
            { x: 880, y: 280, width: 100, height: 25, isGround: false },
            { x: 1000, y: 350, width: 80, height: 25, isGround: false },
            
            // Section 4: Mid level
            { x: 1050, y: 450, width: 250, height: 50, isGround: true },
            { x: 1100, y: 350, width: 100, height: 25, isGround: false },
            { x: 1250, y: 280, width: 90, height: 25, isGround: false },
            
            // Section 5: Tricky jumps
            { x: 1400, y: 450, width: 120, height: 50, isGround: true },
            { x: 1380, y: 350, width: 80, height: 25, isGround: false },
            { x: 1500, y: 380, width: 70, height: 25, isGround: false },
            { x: 1600, y: 320, width: 80, height: 25, isGround: false },
            
            // Section 6: More platforms
            { x: 1700, y: 450, width: 200, height: 50, isGround: true },
            { x: 1750, y: 350, width: 100, height: 25, isGround: false },
            { x: 1650, y: 250, width: 90, height: 25, isGround: false },
            { x: 1850, y: 280, width: 100, height: 25, isGround: false },
            
            // Section 7: Near the end
            { x: 2000, y: 450, width: 150, height: 50, isGround: true },
            { x: 2050, y: 350, width: 80, height: 25, isGround: false },
            { x: 2180, y: 400, width: 100, height: 25, isGround: false },
            
            // Section 8: Final stretch
            { x: 2300, y: 450, width: 200, height: 50, isGround: true },
            { x: 2350, y: 350, width: 100, height: 25, isGround: false },
            { x: 2500, y: 300, width: 90, height: 25, isGround: false },
            
            // Final platform with flag
            { x: 2650, y: 450, width: 350, height: 50, isGround: true },
        ];

        // Coins - Spread across the extended level
        let coins = [];
        function initCoins() {
            coins = [
                // Section 1
                { x: 200, y: 330, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 250, y: 330, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 375, y: 270, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Section 2
                { x: 580, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 475, y: 210, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Section 3
                { x: 780, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 910, y: 240, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Section 4
                { x: 1130, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 1280, y: 240, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Section 5
                { x: 1410, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 1530, y: 340, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 1630, y: 280, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Section 6
                { x: 1780, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 1680, y: 210, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 1880, y: 240, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Section 7
                { x: 2080, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 2210, y: 360, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Section 8
                { x: 2380, y: 310, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                { x: 2530, y: 260, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
                // Final area
                { x: 2750, y: 410, collected: false, frame: 0, offset: Math.random() * Math.PI * 2 },
            ];
        }

        // Enemies - Red demons and green Koopa turtles
        let enemies = [];
        let turtles = [];
        
        function initEnemies() {
            // Red demon monsters
            enemies = [
                // Section 1
                { x: 100, y: 412, width: 38, height: 38, patrolLeft: 50, patrolRight: 350, direction: 1, animFrame: 0 },
                // Section 2
                { x: 550, y: 412, width: 38, height: 38, patrolLeft: 500, patrolRight: 680, direction: 1, animFrame: 0 },
                // Section 3
                { x: 850, y: 412, width: 38, height: 38, patrolLeft: 800, patrolRight: 930, direction: 1, animFrame: 0 },
                // Section 4
                { x: 1100, y: 412, width: 38, height: 38, patrolLeft: 1050, patrolRight: 1280, direction: 1, animFrame: 0 },
                // Section 5
                { x: 1420, y: 412, width: 38, height: 38, patrolLeft: 1400, patrolRight: 1500, direction: 1, animFrame: 0 },
                // Section 6
                { x: 1750, y: 412, width: 38, height: 38, patrolLeft: 1700, patrolRight: 1880, direction: 1, animFrame: 0 },
                // Section 7
                { x: 2050, y: 412, width: 38, height: 38, patrolLeft: 2000, patrolRight: 2130, direction: 1, animFrame: 0 },
                // Final area
                { x: 2700, y: 412, width: 38, height: 38, patrolLeft: 2650, patrolRight: 2850, direction: 1, animFrame: 0 },
            ];
            
            // Green Koopa turtles
            turtles = [
                // Section 1
                { x: 280, y: 410, width: 40, height: 40, patrolLeft: 50, patrolRight: 350, direction: -1, animFrame: 0, inShell: false },
                // Section 2
                { x: 620, y: 410, width: 40, height: 40, patrolLeft: 500, patrolRight: 680, direction: -1, animFrame: 0, inShell: false },
                // Section 3
                { x: 910, y: 240, width: 40, height: 40, patrolLeft: 880, patrolRight: 960, direction: -1, animFrame: 0, inShell: false },
                // Section 4
                { x: 1200, y: 410, width: 40, height: 40, patrolLeft: 1050, patrolRight: 1280, direction: -1, animFrame: 0, inShell: false },
                // Section 5
                { x: 1630, y: 282, width: 40, height: 40, patrolLeft: 1600, patrolRight: 1680, direction: 1, animFrame: 0, inShell: false },
                // Section 6
                { x: 1880, y: 240, width: 40, height: 40, patrolLeft: 1850, patrolRight: 1930, direction: -1, animFrame: 0, inShell: false },
                // Section 7
                { x: 2210, y: 360, width: 40, height: 40, patrolLeft: 2180, patrolRight: 2260, direction: 1, animFrame: 0, inShell: false },
                // Section 8
                { x: 2400, y: 410, width: 40, height: 40, patrolLeft: 2300, patrolRight: 2480, direction: -1, animFrame: 0, inShell: false },
                // Final area
                { x: 2800, y: 410, width: 40, height: 40, patrolLeft: 2650, patrolRight: 2950, direction: -1, animFrame: 0, inShell: false },
            ];
        }

        // Flag - At the end of the extended level
        const flag = {
            x: 2920,
            y: 300,
            poleHeight: 150,
            animTimer: 0
        };

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
            gameState = 'title';  // Start at title screen
            cameraX = 0;
            playerName = '';
            nameInputActive = false;
            initCoins();
            initEnemies();
            overlay.style.display = 'none';
        }

        // Draw gradient sky
        function drawSky() {
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, COLORS.skyTop);
            gradient.addColorStop(1, COLORS.skyBottom);
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // Draw hills
        function drawHills() {
            // Back hills
            ctx.fillStyle = '#228B22';
            ctx.beginPath();
            ctx.moveTo(0, 450);
            ctx.lineTo(100, 380);
            ctx.lineTo(200, 420);
            ctx.lineTo(350, 350);
            ctx.lineTo(450, 400);
            ctx.lineTo(600, 320);
            ctx.lineTo(750, 380);
            ctx.lineTo(900, 340);
            ctx.lineTo(900, 450);
            ctx.closePath();
            ctx.fill();

            // Front hills
            ctx.fillStyle = '#32B432';
            ctx.beginPath();
            ctx.moveTo(0, 450);
            ctx.lineTo(150, 400);
            ctx.lineTo(300, 430);
            ctx.lineTo(500, 380);
            ctx.lineTo(700, 420);
            ctx.lineTo(850, 390);
            ctx.lineTo(900, 430);
            ctx.lineTo(900, 450);
            ctx.closePath();
            ctx.fill();
        }

        // Draw clouds
        function drawClouds() {
            ctx.fillStyle = COLORS.cloud;
            clouds.forEach(cloud => {
                const { x, y, size } = cloud;
                ctx.beginPath();
                ctx.arc(x, y, size, 0, Math.PI * 2);
                ctx.arc(x + size, y - size/3, size * 0.8, 0, Math.PI * 2);
                ctx.arc(x + size * 2, y, size * 0.9, 0, Math.PI * 2);
                ctx.arc(x + size, y + size/4, size * 0.7, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        // Draw platform
        function drawPlatform(p) {
            if (p.isGround) {
                ctx.fillStyle = COLORS.ground;
                ctx.fillRect(p.x, p.y, p.width, p.height);
                ctx.fillStyle = COLORS.grass;
                ctx.fillRect(p.x, p.y, p.width, 8);
                
                // Grass blades
                for (let i = p.x; i < p.x + p.width; i += 8) {
                    ctx.strokeStyle = COLORS.grass;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(i, p.y);
                    ctx.lineTo(i - 2, p.y - 5);
                    ctx.stroke();
                }
            } else {
                ctx.fillStyle = COLORS.platform;
                ctx.fillRect(p.x, p.y, p.width, p.height);
                ctx.fillStyle = COLORS.platformTop;
                ctx.fillRect(p.x, p.y, p.width, 6);
                
                // Brick pattern
                ctx.strokeStyle = '#B4663D';
                for (let row = 6; row < p.height; row += 12) {
                    const offset = (row % 24 === 6) ? 0 : 15;
                    for (let col = -offset; col < p.width; col += 30) {
                        ctx.strokeRect(p.x + col, p.y + row, 28, 10);
                    }
                }
            }
        }

        // Draw player with enhanced graphics and unique character features
        function drawPlayer() {
            const { x, y, width, height, facingRight } = player;
            const char = characters[selectedCharacter];
            const isFemale = char.gender === 'female';
            const skinTone = char.skinTone || '#FFDAB9';
            const skinDark = shadeColor(skinTone, -20);
            const hairColor = char.hairColor || '#5D4037';
            const eyeColor = char.eyeColor || '#4169E1';
            
            // Draw player name above character
            if (playerName) {
                ctx.save();
                ctx.font = 'bold 14px Arial';
                ctx.textAlign = 'center';
                const nameWidth = ctx.measureText(playerName).width + 16;
                
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.beginPath();
                ctx.roundRect(x + width/2 - nameWidth/2 + 2, y - 32, nameWidth, 20, 5);
                ctx.fill();
                
                const nameBg = ctx.createLinearGradient(0, y - 34, 0, y - 14);
                nameBg.addColorStop(0, 'rgba(0,0,0,0.8)');
                nameBg.addColorStop(1, 'rgba(30,30,30,0.9)');
                ctx.fillStyle = nameBg;
                ctx.beginPath();
                ctx.roundRect(x + width/2 - nameWidth/2, y - 34, nameWidth, 20, 5);
                ctx.fill();
                ctx.strokeStyle = char.color;
                ctx.lineWidth = 2;
                ctx.stroke();
                
                ctx.shadowColor = char.color;
                ctx.shadowBlur = 8;
                ctx.fillStyle = '#FFD700';
                ctx.fillText(playerName, x + width/2, y - 19);
                ctx.shadowBlur = 0;
                ctx.restore();
            }
            
            // Shadow on ground
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height + 2, 16, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Hair behind head for long styles
            if (char.hairStyle === 'long') {
                ctx.fillStyle = hairColor;
                ctx.beginPath();
                ctx.ellipse(x + width/2, y + 15, 16, 20, 0, 0, Math.PI * 2);
                ctx.fill();
                const hairSide = facingRight ? x - 2 : x + width + 2;
                ctx.beginPath();
                ctx.moveTo(hairSide, y + 10);
                ctx.quadraticCurveTo(hairSide + (facingRight ? -5 : 5), y + 35, hairSide + (facingRight ? 3 : -3), y + 45);
                ctx.quadraticCurveTo(hairSide + (facingRight ? 6 : -6), y + 35, hairSide + (facingRight ? 4 : -4), y + 15);
                ctx.fill();
            } else if (char.hairStyle === 'curly') {
                ctx.fillStyle = hairColor;
                for (let i = 0; i < 8; i++) {
                    const angle = (i / 8) * Math.PI * 2;
                    const hx = x + width/2 + Math.cos(angle) * 14;
                    const hy = y + 8 + Math.sin(angle) * 12;
                    ctx.beginPath();
                    ctx.arc(hx, hy, 6, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
            
            // Body
            const bodyGrad = ctx.createLinearGradient(x + 4, y + 18, x + 32, y + 45);
            bodyGrad.addColorStop(0, char.shirtColor);
            bodyGrad.addColorStop(0.5, shadeColor(char.shirtColor, -15));
            bodyGrad.addColorStop(1, shadeColor(char.shirtColor, -30));
            ctx.fillStyle = bodyGrad;
            
            if (isFemale) {
                ctx.beginPath();
                ctx.moveTo(x + 8, y + 18);
                ctx.lineTo(x + 28, y + 18);
                ctx.lineTo(x + 32, y + 42);
                ctx.lineTo(x + 4, y + 42);
                ctx.closePath();
                ctx.fill();
                ctx.beginPath();
                for (let i = 0; i < 5; i++) {
                    ctx.arc(x + 6 + i * 6, y + 42, 4, 0, Math.PI);
                }
                ctx.fill();
            } else {
                ctx.beginPath();
                ctx.roundRect(x + 5, y + 18, 26, 25, 4);
                ctx.fill();
                ctx.fillStyle = char.pantsColor;
                ctx.fillRect(x + 8, y + 18, 4, 10);
                ctx.fillRect(x + 24, y + 18, 4, 10);
                ctx.fillStyle = shadeColor(char.pantsColor, -20);
                ctx.fillRect(x + 5, y + 38, 26, 4);
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.roundRect(x + 14, y + 38, 8, 4, 1);
                ctx.fill();
            }
            
            ctx.fillStyle = 'rgba(255,255,255,0.2)';
            ctx.beginPath();
            ctx.roundRect(x + 6, y + 19, 8, 12, 2);
            ctx.fill();
            
            // Head
            const headGrad = ctx.createRadialGradient(x + width/2 - 3, y + 8, 0, x + width/2, y + 11, 13);
            headGrad.addColorStop(0, shadeColor(skinTone, 10));
            headGrad.addColorStop(0.7, skinTone);
            headGrad.addColorStop(1, skinDark);
            ctx.fillStyle = headGrad;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + 11, 12, 12, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Blush
            if (isFemale) {
                ctx.fillStyle = 'rgba(255,150,150,0.4)';
                ctx.beginPath();
                ctx.ellipse(x + 8, y + 14, 4, 3, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.ellipse(x + 28, y + 14, 4, 3, 0, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Ear
            const earX = facingRight ? x + 5 : x + 31;
            ctx.fillStyle = skinTone;
            ctx.beginPath();
            ctx.ellipse(earX, y + 12, 3, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Hat or Hair
            if (char.hasHat) {
                const hatGrad = ctx.createLinearGradient(x + 4, y, x + 32, y + 12);
                hatGrad.addColorStop(0, shadeColor(char.hatColor, 20));
                hatGrad.addColorStop(0.5, char.hatColor);
                hatGrad.addColorStop(1, shadeColor(char.hatColor, -25));
                ctx.fillStyle = hatGrad;
                ctx.beginPath();
                ctx.roundRect(x + 4, y - 2, 28, 12, 3);
                ctx.fill();
                if (facingRight) {
                    ctx.beginPath();
                    ctx.roundRect(x + 22, y + 4, 14, 8, 2);
                    ctx.fill();
                } else {
                    ctx.beginPath();
                    ctx.roundRect(x, y + 4, 14, 8, 2);
                    ctx.fill();
                }
                ctx.fillStyle = '#FFF';
                ctx.beginPath();
                ctx.arc(x + width/2, y + 4, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = char.hatColor;
                ctx.font = 'bold 7px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(char.name[0], x + width/2, y + 7);
                ctx.textAlign = 'left';
            } else if (char.hairStyle === 'short') {
                ctx.fillStyle = hairColor;
                ctx.beginPath();
                ctx.ellipse(x + width/2, y + 2, 10, 8, 0, 0, Math.PI * 2);
                ctx.fill();
            } else if (char.hairStyle === 'spiky') {
                ctx.fillStyle = hairColor;
                for (let i = 0; i < 5; i++) {
                    ctx.beginPath();
                    ctx.moveTo(x + 8 + i * 5, y + 5);
                    ctx.lineTo(x + 10 + i * 5, y - 6);
                    ctx.lineTo(x + 12 + i * 5, y + 5);
                    ctx.fill();
                }
            } else if (char.hairStyle === 'ponytail') {
                ctx.fillStyle = hairColor;
                ctx.beginPath();
                ctx.ellipse(x + width/2, y + 2, 12, 8, 0, 0, Math.PI * 2);
                ctx.fill();
                const tailX = facingRight ? x + 30 : x + 6;
                ctx.beginPath();
                ctx.moveTo(tailX, y);
                ctx.quadraticCurveTo(tailX + (facingRight ? 10 : -10), y + 5, tailX + (facingRight ? 8 : -8), y + 25);
                ctx.quadraticCurveTo(tailX + (facingRight ? 5 : -5), y + 20, tailX + (facingRight ? 2 : -2), y + 5);
                ctx.fill();
            }
            
            // Crown
            if (char.hasCrown) {
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.moveTo(x + 8, y - 5);
                ctx.lineTo(x + 10, y - 15);
                ctx.lineTo(x + 14, y - 8);
                ctx.lineTo(x + 18, y - 18);
                ctx.lineTo(x + 22, y - 8);
                ctx.lineTo(x + 26, y - 15);
                ctx.lineTo(x + 28, y - 5);
                ctx.closePath();
                ctx.fill();
                ctx.fillStyle = '#FF1493';
                ctx.beginPath();
                ctx.arc(x + 18, y - 12, 3, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Eyes
            const eyeX = facingRight ? x + 21 : x + 13;
            const eyeSize = isFemale ? 5 : 4;
            ctx.fillStyle = '#FFF';
            ctx.beginPath();
            ctx.ellipse(eyeX, y + 10, eyeSize, eyeSize + 1, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = eyeColor;
            ctx.beginPath();
            ctx.arc(eyeX + (facingRight ? 1 : -1), y + 10, 2.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(eyeX + (facingRight ? 1 : -1), y + 10, 1.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#FFF';
            ctx.beginPath();
            ctx.arc(eyeX + (facingRight ? 2 : 0), y + 9, 0.8, 0, Math.PI * 2);
            ctx.fill();
            
            // Eyelashes
            if (isFemale) {
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(eyeX - 3, y + 6);
                ctx.lineTo(eyeX - 4, y + 4);
                ctx.moveTo(eyeX, y + 5);
                ctx.lineTo(eyeX, y + 3);
                ctx.stroke();
            }
            
            // Eyebrow
            ctx.strokeStyle = hairColor;
            ctx.lineWidth = isFemale ? 1.5 : 2;
            ctx.beginPath();
            ctx.moveTo(eyeX - 4, y + 4);
            ctx.quadraticCurveTo(eyeX, y + 2, eyeX + 4, y + 4);
            ctx.stroke();
            ctx.lineWidth = 1;
            
            // Nose
            ctx.fillStyle = skinDark;
            ctx.beginPath();
            ctx.ellipse(x + width/2 + (facingRight ? 3 : -3), y + 13, isFemale ? 2 : 3, 2, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Smile! 😊
            ctx.strokeStyle = '#C0392B';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(x + width/2, y + 14, 5, 0.2, Math.PI - 0.2);
            ctx.stroke();
            ctx.lineWidth = 1;
            
            // Mustache or Lipstick
            if (char.hasMustache) {
                const mustacheGrad = ctx.createLinearGradient(x + 9, y + 15, x + 27, y + 20);
                mustacheGrad.addColorStop(0, hairColor);
                mustacheGrad.addColorStop(1, shadeColor(hairColor, -30));
                ctx.fillStyle = mustacheGrad;
                ctx.beginPath();
                ctx.moveTo(x + width/2, y + 16);
                ctx.quadraticCurveTo(x + 8, y + 17, x + 6, y + 21);
                ctx.quadraticCurveTo(x + 10, y + 19, x + width/2, y + 18);
                ctx.quadraticCurveTo(x + 26, y + 19, x + 30, y + 21);
                ctx.quadraticCurveTo(x + 28, y + 17, x + width/2, y + 16);
                ctx.fill();
            }
            if (isFemale) {
                ctx.fillStyle = '#E74C3C';
                ctx.beginPath();
                ctx.ellipse(x + width/2, y + 18, 4, 2, 0, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Legs
            const legGrad = ctx.createLinearGradient(x + 7, y + 42, x + 16, y + 48);
            legGrad.addColorStop(0, isFemale ? skinTone : char.pantsColor);
            legGrad.addColorStop(1, isFemale ? skinDark : shadeColor(char.pantsColor, -30));
            ctx.fillStyle = legGrad;
            ctx.beginPath();
            ctx.roundRect(x + 7, y + 44, 10, 8, 2);
            ctx.fill();
            ctx.beginPath();
            ctx.roundRect(x + 19, y + 44, 10, 8, 2);
            ctx.fill();
            
            // Shoes
            const shoeColor = isFemale ? char.color : '#8B4513';
            const shoeGrad = ctx.createRadialGradient(x + 10, y + 50, 0, x + 12, y + 52, 10);
            shoeGrad.addColorStop(0, shadeColor(shoeColor, 20));
            shoeGrad.addColorStop(0.6, shoeColor);
            shoeGrad.addColorStop(1, shadeColor(shoeColor, -30));
            ctx.fillStyle = shoeGrad;
            ctx.beginPath();
            ctx.ellipse(x + 11, y + 52, 8, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(x + 25, y + 52, 8, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = 'rgba(255,255,255,0.3)';
            ctx.beginPath();
            ctx.ellipse(x + 9, y + 50, 3, 2, -0.3, 0, Math.PI * 2);
            ctx.fill();
            
            if (isFemale) {
                ctx.fillStyle = shadeColor(shoeColor, -30);
                ctx.fillRect(x + 8, y + 52, 3, 5);
                ctx.fillRect(x + 22, y + 52, 3, 5);
            }
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

        // Draw coin
        function drawCoin(coin) {
            if (coin.collected) return;
            
            const floatY = coin.y + Math.sin(Date.now() / 200 + coin.offset) * 3;
            const widthFactor = Math.abs(Math.sin(coin.frame * Math.PI / 4));
            const displayWidth = Math.max(4, 22 * widthFactor);
            const xOffset = (22 - displayWidth) / 2;
            
            ctx.fillStyle = COLORS.coin;
            ctx.beginPath();
            ctx.ellipse(coin.x + 11, floatY + 11, displayWidth/2, 11, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Shine
            if (displayWidth > 10) {
                ctx.fillStyle = COLORS.coinShine;
                ctx.beginPath();
                ctx.ellipse(coin.x + 8, floatY + 6, displayWidth/6, 4, 0, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        // Draw enemy - Scary red demon monster
        function drawEnemy(enemy) {
            const { x, y, width, height, animFrame } = enemy;
            const bounce = Math.sin(Date.now() / 150) * 2;
            
            // Shadow
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height + 2, width/2.5, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Body - Dark red with gradient effect
            const bodyGrad = ctx.createRadialGradient(x + width/2, y + height/2, 0, x + width/2, y + height/2, width/2);
            bodyGrad.addColorStop(0, '#FF2020');
            bodyGrad.addColorStop(0.7, '#AA0000');
            bodyGrad.addColorStop(1, '#660000');
            ctx.fillStyle = bodyGrad;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height/2 + 3 + bounce, width/2 + 2, height/2, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Spiky head/horns
            ctx.fillStyle = '#880000';
            // Left horn
            ctx.beginPath();
            ctx.moveTo(x + 5, y + 10);
            ctx.lineTo(x - 3, y - 8);
            ctx.lineTo(x + 12, y + 5);
            ctx.closePath();
            ctx.fill();
            // Right horn
            ctx.beginPath();
            ctx.moveTo(x + width - 5, y + 10);
            ctx.lineTo(x + width + 3, y - 8);
            ctx.lineTo(x + width - 12, y + 5);
            ctx.closePath();
            ctx.fill();
            
            // Glowing angry eyes
            ctx.fillStyle = '#FFFF00';
            ctx.shadowColor = '#FF0000';
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.ellipse(x + 10, y + 15 + bounce, 6, 5, -0.3, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(x + width - 10, y + 15 + bounce, 6, 5, 0.3, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            // Evil red pupils
            ctx.fillStyle = '#FF0000';
            ctx.beginPath();
            ctx.arc(x + 11, y + 16 + bounce, 3, 0, Math.PI * 2);
            ctx.arc(x + width - 9, y + 16 + bounce, 3, 0, Math.PI * 2);
            ctx.fill();
            
            // Black slits in pupils
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.ellipse(x + 11, y + 16 + bounce, 1, 3, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(x + width - 9, y + 16 + bounce, 1, 3, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Angry eyebrows
            ctx.strokeStyle = '#440000';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(x + 3, y + 8 + bounce);
            ctx.lineTo(x + 15, y + 12 + bounce);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x + width - 3, y + 8 + bounce);
            ctx.lineTo(x + width - 15, y + 12 + bounce);
            ctx.stroke();
            ctx.lineWidth = 1;
            
            // Scary mouth with fangs
            ctx.fillStyle = '#220000';
            ctx.beginPath();
            ctx.moveTo(x + 8, y + 26 + bounce);
            ctx.quadraticCurveTo(x + width/2, y + 35 + bounce, x + width - 8, y + 26 + bounce);
            ctx.quadraticCurveTo(x + width/2, y + 30 + bounce, x + 8, y + 26 + bounce);
            ctx.fill();
            
            // Fangs
            ctx.fillStyle = '#FFFFFF';
            ctx.beginPath();
            ctx.moveTo(x + 11, y + 26 + bounce);
            ctx.lineTo(x + 14, y + 33 + bounce);
            ctx.lineTo(x + 17, y + 26 + bounce);
            ctx.fill();
            ctx.beginPath();
            ctx.moveTo(x + width - 11, y + 26 + bounce);
            ctx.lineTo(x + width - 14, y + 33 + bounce);
            ctx.lineTo(x + width - 17, y + 26 + bounce);
            ctx.fill();
            
            // Clawed feet
            const footOffset = animFrame === 0 ? 2 : -2;
            ctx.fillStyle = '#660000';
            // Left foot with claws
            ctx.beginPath();
            ctx.ellipse(x + 8, y + height - 3 + footOffset, 8, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#440000';
            for (let i = 0; i < 3; i++) {
                ctx.beginPath();
                ctx.moveTo(x + 3 + i * 5, y + height + footOffset);
                ctx.lineTo(x + 5 + i * 5, y + height + 5 + footOffset);
                ctx.lineTo(x + 7 + i * 5, y + height + footOffset);
                ctx.fill();
            }
            // Right foot with claws
            ctx.fillStyle = '#660000';
            ctx.beginPath();
            ctx.ellipse(x + width - 8, y + height - 3 - footOffset, 8, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#440000';
            for (let i = 0; i < 3; i++) {
                ctx.beginPath();
                ctx.moveTo(x + width - 13 + i * 5, y + height - footOffset);
                ctx.lineTo(x + width - 11 + i * 5, y + height + 5 - footOffset);
                ctx.lineTo(x + width - 9 + i * 5, y + height - footOffset);
                ctx.fill();
            }
        }

        // Draw Koopa turtle enemy
        function drawTurtle(turtle) {
            const { x, y, width, height, direction, animFrame, inShell } = turtle;
            const bounce = Math.sin(Date.now() / 200) * 2;
            
            if (inShell) {
                // Draw shell only (when hiding)
                const shellGrad = ctx.createRadialGradient(x + width/2, y + height/2, 0, x + width/2, y + height/2, width/2);
                shellGrad.addColorStop(0, '#32CD32');
                shellGrad.addColorStop(0.7, '#228B22');
                shellGrad.addColorStop(1, '#006400');
                ctx.fillStyle = shellGrad;
                ctx.beginPath();
                ctx.ellipse(x + width/2, y + height/2 + 5, width/2, height/2.5, 0, 0, Math.PI * 2);
                ctx.fill();
                
                // Shell pattern
                ctx.strokeStyle = '#004400';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(x + width/2, y + 5);
                ctx.lineTo(x + width/2, y + height - 5);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x + 8, y + height/2);
                ctx.lineTo(x + width - 8, y + height/2);
                ctx.stroke();
                return;
            }
            
            // Shadow
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height + 2, width/2.5, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Shell (back)
            const shellGrad = ctx.createRadialGradient(x + width/2, y + height/2 + 5, 0, x + width/2, y + height/2, width/2);
            shellGrad.addColorStop(0, '#32CD32');
            shellGrad.addColorStop(0.6, '#228B22');
            shellGrad.addColorStop(1, '#006400');
            ctx.fillStyle = shellGrad;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height/2 + 5 + bounce/2, width/2 + 2, height/2, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Shell pattern
            ctx.strokeStyle = '#004400';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + height/2 + 5 + bounce/2, width/3, height/3, 0, 0, Math.PI * 2);
            ctx.stroke();
            
            // Head
            const headX = direction > 0 ? x + width - 5 : x - 5;
            ctx.fillStyle = '#FFDB58';
            ctx.beginPath();
            ctx.ellipse(headX, y + 12 + bounce, 12, 10, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Snout/beak
            ctx.fillStyle = '#F0C040';
            const beakX = direction > 0 ? headX + 8 : headX - 8;
            ctx.beginPath();
            ctx.ellipse(beakX, y + 15 + bounce, 6, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Eyes
            const eyeX = direction > 0 ? headX + 2 : headX - 2;
            ctx.fillStyle = '#FFF';
            ctx.beginPath();
            ctx.arc(eyeX, y + 10 + bounce, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(eyeX + (direction > 0 ? 1 : -1), y + 10 + bounce, 2.5, 0, Math.PI * 2);
            ctx.fill();
            
            // Eyebrow (angry look)
            ctx.strokeStyle = '#8B4513';
            ctx.lineWidth = 2;
            ctx.beginPath();
            if (direction > 0) {
                ctx.moveTo(eyeX - 4, y + 5 + bounce);
                ctx.lineTo(eyeX + 4, y + 7 + bounce);
            } else {
                ctx.moveTo(eyeX + 4, y + 5 + bounce);
                ctx.lineTo(eyeX - 4, y + 7 + bounce);
            }
            ctx.stroke();
            
            // Feet
            const footOffset = Math.floor(Date.now() / 150) % 2 === 0 ? 3 : -3;
            ctx.fillStyle = '#FF8C00';
            // Front foot
            ctx.beginPath();
            ctx.ellipse(direction > 0 ? x + width - 8 : x + 8, y + height - 3 + footOffset, 7, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            // Back foot
            ctx.beginPath();
            ctx.ellipse(direction > 0 ? x + 12 : x + width - 12, y + height - 3 - footOffset, 7, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Tail
            ctx.fillStyle = '#FFDB58';
            ctx.beginPath();
            const tailX = direction > 0 ? x + 5 : x + width - 5;
            ctx.moveTo(tailX, y + height/2 + bounce);
            ctx.lineTo(tailX + (direction > 0 ? -12 : 12), y + height/2 + 8 + bounce);
            ctx.lineTo(tailX + (direction > 0 ? -8 : 8), y + height/2 - 3 + bounce);
            ctx.closePath();
            ctx.fill();
        }
        
        // Draw flag
        function drawFlag() {
            const { x, y, poleHeight, animTimer } = flag;
            
            // Pole
            ctx.fillStyle = COLORS.flagPole;
            ctx.fillRect(x, y, 7, poleHeight);
            
            // Ball on top
            ctx.fillStyle = COLORS.coin;
            ctx.beginPath();
            ctx.arc(x + 3, y, 7, 0, Math.PI * 2);
            ctx.fill();
            
            // Flag with wave
            const wave = Math.sin(animTimer / 10) * 4;
            ctx.fillStyle = COLORS.flag;
            ctx.beginPath();
            ctx.moveTo(x + 7, y + 8);
            ctx.lineTo(x + 55 + wave, y + 20);
            ctx.lineTo(x + 50 + wave * 0.5, y + 35);
            ctx.lineTo(x + 7, y + 45);
            ctx.closePath();
            ctx.fill();
            
            // Star on flag
            const starX = x + 27 + wave * 0.5;
            const starY = y + 26;
            ctx.fillStyle = COLORS.coin;
            drawStar(starX, starY, 8, 4, 5);
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

        // Draw UI
        function drawUI() {
            // Coin counter background
            ctx.fillStyle = 'rgba(0,0,0,0.5)';
            ctx.roundRect(15, 12, 130, 35, 8);
            ctx.fill();
            
            // Coin icon
            ctx.fillStyle = COLORS.coin;
            ctx.beginPath();
            ctx.arc(35, 30, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#B8860B';
            ctx.font = 'bold 14px Arial';
            ctx.fillText('$', 31, 35);
            
            // Score text
            ctx.fillStyle = COLORS.text;
            ctx.font = 'bold 20px Arial';
            ctx.fillText(`× ${score}`, 55, 37);
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
            const flagRect = { x: flag.x - 10, y: flag.y, width: 30, height: flag.poleHeight };
            if (checkCollision(player, flagRect)) {
                gameWon();
            }
        }

        // Game over
        function gameOver() {
            gameState = 'lost';
            overlayTitle.textContent = '💀 GAME OVER 💀';
            overlayScore.textContent = `${playerName} collected ${score}/${coins.length} coins`;
            overlay.style.display = 'flex';
        }

        // Game won
        function gameWon() {
            gameState = 'won';
            overlayTitle.textContent = '🎉 YOU WIN! 🎉';
            overlayScore.textContent = `${playerName} collected ${score}/${coins.length} coins!`;
            overlay.style.display = 'flex';
        }

        // Update game
        function update() {
            if (gameState !== 'playing') return;
            
            animationFrame++;
            flag.animTimer++;
            
            updatePlayer();
            updateCoins();
            updateEnemies();
            checkFlag();
            
            // Move clouds (gentle drift)
            clouds.forEach(cloud => {
                cloud.x -= 0.15;
                if (cloud.x < -60) cloud.x = canvas.width + 30;
            });
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
            
            drawSky();
            
            // Save context and apply camera transform
            ctx.save();
            ctx.translate(-cameraX, 0);
            
            // Draw background elements (parallax - slower)
            ctx.save();
            ctx.translate(cameraX * 0.5, 0); // Parallax effect
            drawHills();
            ctx.restore();
            
            // Draw clouds with parallax
            ctx.save();
            ctx.translate(cameraX * 0.7, 0);
            drawClouds();
            ctx.restore();
            
            // Draw game objects
            platforms.forEach(drawPlatform);
            coins.forEach(drawCoin);
            enemies.forEach(drawEnemy);
            turtles.forEach(drawTurtle);
            drawFlag();
            drawPlayer();
            
            ctx.restore();
            
            // UI is drawn without camera offset
            drawUI();
            
            // Draw progress bar at top
            drawProgressBar();
        }
        
        // Draw title screen
        function drawTitleScreen() {
            // Animated background
            const time = Date.now() / 1000;
            
            // Gradient sky
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#1a1a2e');
            gradient.addColorStop(0.5, '#16213e');
            gradient.addColorStop(1, '#0f3460');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Animated stars
            ctx.fillStyle = '#FFF';
            for (let i = 0; i < 50; i++) {
                const x = (i * 73 + time * 20) % canvas.width;
                const y = (i * 37) % (canvas.height / 2);
                const twinkle = Math.sin(time * 3 + i) * 0.5 + 0.5;
                ctx.globalAlpha = twinkle;
                ctx.beginPath();
                ctx.arc(x, y, 1.5, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.globalAlpha = 1;
            
            // Title with glow effect
            ctx.shadowColor = '#FFD700';
            ctx.shadowBlur = 30;
            ctx.fillStyle = '#FFD700';
            ctx.font = 'bold 56px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('🍄 SUPER PRADY BROS 🍄', canvas.width / 2, 120);
            ctx.shadowBlur = 0;
            
            // Subtitle
            ctx.fillStyle = '#87CEEB';
            ctx.font = '24px Arial';
            ctx.fillText('A Mario-Style Adventure', canvas.width / 2, 160);
            
            // Draw a preview character
            const previewX = canvas.width / 2 - 20;
            const previewY = 200 + Math.sin(time * 2) * 10;
            drawPlayerAt(previewX, previewY, true);
            
            // Name input box
            ctx.fillStyle = 'rgba(255,255,255,0.1)';
            ctx.strokeStyle = nameInputActive ? '#FFD700' : '#87CEEB';
            ctx.lineWidth = 3;
            const boxX = canvas.width / 2 - 150;
            const boxY = 300;
            ctx.beginPath();
            ctx.roundRect(boxX, boxY, 300, 50, 10);
            ctx.fill();
            ctx.stroke();
            
            // Label
            ctx.fillStyle = '#FFF';
            ctx.font = '18px Arial';
            ctx.fillText('Enter Your Name:', canvas.width / 2, boxY - 15);
            
            // Name text or placeholder
            ctx.font = 'bold 24px Arial';
            if (playerName) {
                ctx.fillStyle = '#FFD700';
                ctx.fillText(playerName, canvas.width / 2, boxY + 33);
            } else {
                ctx.fillStyle = 'rgba(255,255,255,0.4)';
                ctx.fillText('Click here to type...', canvas.width / 2, boxY + 33);
            }
            
            // Cursor blink
            if (nameInputActive && Math.floor(time * 2) % 2 === 0) {
                const textWidth = ctx.measureText(playerName).width;
                ctx.fillStyle = '#FFD700';
                ctx.fillRect(canvas.width / 2 + textWidth / 2 + 5, boxY + 12, 2, 26);
            }
            
            // Start button
            const canStart = playerName.length >= 1;
            const btnY = 400;
            const btnHover = Math.sin(time * 4) * 3;
            const btnText = canStart ? '▶ CHOOSE CHARACTER' : 'Enter name first';
            const btnWidth = Math.max(280, ctx.measureText(btnText).width + 60);
            
            if (canStart) {
                ctx.fillStyle = '#00FF7F';
                ctx.shadowColor = '#00FF7F';
                ctx.shadowBlur = 20;
            } else {
                ctx.fillStyle = '#555';
                ctx.shadowBlur = 0;
            }
            
            ctx.beginPath();
            ctx.roundRect(canvas.width / 2 - btnWidth / 2, btnY + btnHover, btnWidth, 50, 10);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = canStart ? '#000' : '#888';
            ctx.font = 'bold 22px Arial';
            ctx.fillText(btnText, canvas.width / 2, btnY + 33 + btnHover);
            
            // Instructions
            ctx.fillStyle = 'rgba(255,255,255,0.6)';
            ctx.font = '16px Arial';
            ctx.fillText('Press ENTER or click START to begin', canvas.width / 2, 480);
            
            ctx.textAlign = 'left';
        }
        
        // Draw character selection screen - Carousel style
        function drawCharacterSelect() {
            const time = Date.now() / 1000;
            
            // Gradient background
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#1a1a2e');
            gradient.addColorStop(0.5, '#16213e');
            gradient.addColorStop(1, '#0f3460');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Title
            ctx.fillStyle = '#FFD700';
            ctx.font = 'bold 42px Arial';
            ctx.textAlign = 'center';
            ctx.shadowColor = '#FFD700';
            ctx.shadowBlur = 20;
            ctx.fillText('CHOOSE YOUR HERO', canvas.width / 2, 55);
            ctx.shadowBlur = 0;
            
            // Player name display
            ctx.fillStyle = '#87CEEB';
            ctx.font = '20px Arial';
            ctx.fillText(`Playing as: ${playerName}`, canvas.width / 2, 85);
            
            // Carousel - show 3 characters at a time with selected in center
            const cardWidth = 160;
            const cardHeight = 220;
            const cardY = 120;
            const centerX = canvas.width / 2;
            const cardSpacing = 180;
            
            // Draw navigation arrows
            ctx.fillStyle = '#FFD700';
            ctx.font = 'bold 48px Arial';
            ctx.fillText('◀', 40, cardY + cardHeight / 2 + 15);
            ctx.fillText('▶', canvas.width - 60, cardY + cardHeight / 2 + 15);
            
            // Draw characters in carousel (show 5: 2 left, center, 2 right)
            for (let offset = -2; offset <= 2; offset++) {
                let charIndex = (selectedCharacter + offset + characters.length) % characters.length;
                const char = characters[charIndex];
                const isSelected = offset === 0;
                
                // Calculate position with perspective
                const cardX = centerX + offset * cardSpacing - cardWidth / 2;
                const scale = isSelected ? 1.0 : 0.75;
                const opacity = isSelected ? 1.0 : 0.6;
                const yOffset = isSelected ? 0 : 20;
                const hover = isSelected ? Math.sin(time * 4) * 5 : 0;
                
                // Skip if too far off screen
                if (cardX < -cardWidth || cardX > canvas.width + cardWidth) continue;
                
                ctx.save();
                ctx.globalAlpha = opacity;
                
                // Scale from center of card
                const scaledWidth = cardWidth * scale;
                const scaledHeight = cardHeight * scale;
                const scaledX = cardX + (cardWidth - scaledWidth) / 2;
                const scaledY = cardY + yOffset + (cardHeight - scaledHeight) / 2 + hover;
                
                // Card background
                if (isSelected) {
                    ctx.fillStyle = 'rgba(255, 215, 0, 0.3)';
                    ctx.strokeStyle = '#FFD700';
                    ctx.lineWidth = 4;
                    ctx.shadowColor = '#FFD700';
                    ctx.shadowBlur = 25;
                } else {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
                    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
                    ctx.lineWidth = 2;
                    ctx.shadowBlur = 0;
                }
                
                ctx.beginPath();
                ctx.roundRect(scaledX, scaledY, scaledWidth, scaledHeight, 15 * scale);
                ctx.fill();
                ctx.stroke();
                ctx.shadowBlur = 0;
                
                // Character preview (adjust position for scale)
                const charPreviewX = scaledX + scaledWidth / 2 - 18 * scale;
                const charPreviewY = scaledY + 30 * scale;
                
                ctx.save();
                ctx.translate(scaledX + scaledWidth / 2, scaledY + scaledHeight / 2 - 30);
                ctx.scale(scale, scale);
                ctx.translate(-18, -30);
                drawCharacterPreview(0, 0, char);
                ctx.restore();
                
                // Character name
                ctx.fillStyle = isSelected ? '#FFD700' : '#FFF';
                ctx.font = `bold ${Math.floor(18 * scale)}px Arial`;
                ctx.fillText(char.name, scaledX + scaledWidth / 2, scaledY + scaledHeight - 50 * scale);
                
                // Description
                ctx.fillStyle = 'rgba(255,255,255,0.7)';
                ctx.font = `${Math.floor(12 * scale)}px Arial`;
                ctx.fillText(char.description, scaledX + scaledWidth / 2, scaledY + scaledHeight - 28 * scale);
                
                // Selection indicator for center character
                if (isSelected) {
                    ctx.fillStyle = '#FFD700';
                    ctx.font = '24px Arial';
                    ctx.fillText('▼', scaledX + scaledWidth / 2, scaledY - 5);
                }
                
                ctx.restore();
            }
            
            // Character counter
            ctx.fillStyle = '#FFF';
            ctx.font = '16px Arial';
            ctx.fillText(`${selectedCharacter + 1} / ${characters.length}`, canvas.width / 2, 365);
            
            // Navigation hints
            ctx.fillStyle = 'rgba(255,255,255,0.6)';
            ctx.font = '18px Arial';
            ctx.fillText('← → to select  |  ENTER or SPACE to start', canvas.width / 2, 395);
            
            // Start button
            const btnY = 420;
            ctx.fillStyle = '#00FF7F';
            ctx.shadowColor = '#00FF7F';
            ctx.shadowBlur = 15;
            ctx.beginPath();
            ctx.roundRect(canvas.width / 2 - 120, btnY, 240, 50, 10);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = '#000';
            ctx.font = 'bold 22px Arial';
            ctx.fillText(`▶ PLAY AS ${characters[selectedCharacter].name.toUpperCase()}`, canvas.width / 2, btnY + 33);
            
            ctx.textAlign = 'left';
        }
        
        // Draw character preview for selection screen (enhanced with unique features)
        function drawCharacterPreview(x, y, char) {
            const floatY = y + Math.sin(Date.now() / 300) * 4;
            const isFemale = char.gender === 'female';
            const skinTone = char.skinTone || '#FFDAB9';
            const skinDark = shadeColor(skinTone, -20);
            const hairColor = char.hairColor || '#5D4037';
            const eyeColor = char.eyeColor || '#4169E1';
            
            // Shadow
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.beginPath();
            ctx.ellipse(x + 18, y + 58, 14, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Hair behind head (for long/curly styles)
            if (char.hairStyle === 'long') {
                ctx.fillStyle = hairColor;
                ctx.beginPath();
                ctx.ellipse(x + 18, floatY + 15, 16, 20, 0, 0, Math.PI * 2);
                ctx.fill();
                // Flowing hair
                ctx.beginPath();
                ctx.moveTo(x + 2, floatY + 10);
                ctx.quadraticCurveTo(x - 2, floatY + 35, x + 5, floatY + 45);
                ctx.quadraticCurveTo(x + 8, floatY + 35, x + 6, floatY + 15);
                ctx.fill();
                ctx.beginPath();
                ctx.moveTo(x + 34, floatY + 10);
                ctx.quadraticCurveTo(x + 38, floatY + 35, x + 31, floatY + 45);
                ctx.quadraticCurveTo(x + 28, floatY + 35, x + 30, floatY + 15);
                ctx.fill();
            } else if (char.hairStyle === 'curly') {
                ctx.fillStyle = hairColor;
                for (let i = 0; i < 8; i++) {
                    const angle = (i / 8) * Math.PI * 2;
                    const hx = x + 18 + Math.cos(angle) * 14;
                    const hy = floatY + 8 + Math.sin(angle) * 12;
                    ctx.beginPath();
                    ctx.arc(hx, hy, 6, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
            
            // Body with gradient
            const bodyGrad = ctx.createLinearGradient(x + 4, floatY + 18, x + 32, floatY + 45);
            bodyGrad.addColorStop(0, char.shirtColor);
            bodyGrad.addColorStop(0.5, shadeColor(char.shirtColor, -15));
            bodyGrad.addColorStop(1, shadeColor(char.shirtColor, -30));
            ctx.fillStyle = bodyGrad;
            
            if (isFemale) {
                // Dress/feminine body shape
                ctx.beginPath();
                ctx.moveTo(x + 8, floatY + 18);
                ctx.lineTo(x + 28, floatY + 18);
                ctx.lineTo(x + 32, floatY + 42);
                ctx.lineTo(x + 4, floatY + 42);
                ctx.closePath();
                ctx.fill();
                // Dress ruffle
                ctx.beginPath();
                for (let i = 0; i < 5; i++) {
                    ctx.arc(x + 6 + i * 6, floatY + 42, 4, 0, Math.PI);
                }
                ctx.fill();
            } else {
                ctx.beginPath();
                ctx.roundRect(x + 5, floatY + 18, 26, 25, 4);
                ctx.fill();
                // Overalls straps
                ctx.fillStyle = char.pantsColor;
                ctx.fillRect(x + 8, floatY + 18, 4, 10);
                ctx.fillRect(x + 24, floatY + 18, 4, 10);
            }
            
            // Body highlight
            ctx.fillStyle = 'rgba(255,255,255,0.2)';
            ctx.beginPath();
            ctx.roundRect(x + 6, floatY + 19, 8, 12, 2);
            ctx.fill();
            
            // Belt (only for non-dress)
            if (!isFemale) {
                ctx.fillStyle = shadeColor(char.pantsColor, -20);
                ctx.fillRect(x + 5, floatY + 38, 26, 4);
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.roundRect(x + 14, floatY + 38, 8, 4, 1);
                ctx.fill();
            }
            
            // Head with gradient (using character skin tone)
            const headGrad = ctx.createRadialGradient(x + 15, floatY + 8, 0, x + 18, floatY + 11, 13);
            headGrad.addColorStop(0, shadeColor(skinTone, 10));
            headGrad.addColorStop(0.7, skinTone);
            headGrad.addColorStop(1, skinDark);
            ctx.fillStyle = headGrad;
            ctx.beginPath();
            ctx.ellipse(x + 18, floatY + 11, 12, 12, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Blush for female characters
            if (isFemale) {
                ctx.fillStyle = 'rgba(255,150,150,0.4)';
                ctx.beginPath();
                ctx.ellipse(x + 8, floatY + 14, 4, 3, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.ellipse(x + 28, floatY + 14, 4, 3, 0, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Ear
            ctx.fillStyle = skinTone;
            ctx.beginPath();
            ctx.ellipse(x + 31, floatY + 12, 3, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Hat or Hair on top
            if (char.hasHat) {
                const hatGrad = ctx.createLinearGradient(x + 4, floatY, x + 32, floatY + 12);
                hatGrad.addColorStop(0, shadeColor(char.hatColor, 20));
                hatGrad.addColorStop(0.5, char.hatColor);
                hatGrad.addColorStop(1, shadeColor(char.hatColor, -25));
                ctx.fillStyle = hatGrad;
                ctx.beginPath();
                ctx.roundRect(x + 4, floatY - 2, 28, 12, 3);
                ctx.fill();
                ctx.beginPath();
                ctx.roundRect(x + 22, floatY + 4, 14, 8, 2);
                ctx.fill();
                
                // Hat emblem
                ctx.fillStyle = '#FFF';
                ctx.beginPath();
                ctx.arc(x + 18, floatY + 4, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = char.hatColor;
                ctx.font = 'bold 7px Arial';
                ctx.fillText(char.name[0], x + 15, floatY + 7);
            } else if (char.hairStyle === 'short') {
                // Short spiky hair
                ctx.fillStyle = hairColor;
                ctx.beginPath();
                ctx.ellipse(x + 18, floatY + 2, 10, 8, 0, 0, Math.PI * 2);
                ctx.fill();
            } else if (char.hairStyle === 'spiky') {
                ctx.fillStyle = hairColor;
                for (let i = 0; i < 5; i++) {
                    ctx.beginPath();
                    ctx.moveTo(x + 8 + i * 5, floatY + 5);
                    ctx.lineTo(x + 10 + i * 5, floatY - 8 - Math.random() * 4);
                    ctx.lineTo(x + 12 + i * 5, floatY + 5);
                    ctx.fill();
                }
            } else if (char.hairStyle === 'ponytail') {
                ctx.fillStyle = hairColor;
                ctx.beginPath();
                ctx.ellipse(x + 18, floatY + 2, 12, 8, 0, 0, Math.PI * 2);
                ctx.fill();
                // Ponytail
                ctx.beginPath();
                ctx.moveTo(x + 30, floatY);
                ctx.quadraticCurveTo(x + 40, floatY + 5, x + 38, floatY + 25);
                ctx.quadraticCurveTo(x + 35, floatY + 20, x + 32, floatY + 5);
                ctx.fill();
                // Hair tie
                ctx.fillStyle = char.color;
                ctx.beginPath();
                ctx.ellipse(x + 32, floatY + 3, 3, 2, 0.3, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Crown for princess characters
            if (char.hasCrown) {
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.moveTo(x + 8, floatY - 5);
                ctx.lineTo(x + 10, floatY - 15);
                ctx.lineTo(x + 14, floatY - 8);
                ctx.lineTo(x + 18, floatY - 18);
                ctx.lineTo(x + 22, floatY - 8);
                ctx.lineTo(x + 26, floatY - 15);
                ctx.lineTo(x + 28, floatY - 5);
                ctx.closePath();
                ctx.fill();
                // Gems
                ctx.fillStyle = '#FF1493';
                ctx.beginPath();
                ctx.arc(x + 18, floatY - 12, 3, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#00CED1';
                ctx.beginPath();
                ctx.arc(x + 11, floatY - 10, 2, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(x + 25, floatY - 10, 2, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Eyes (larger for female characters)
            const eyeSize = isFemale ? 5 : 4;
            const eyeHeight = isFemale ? 6 : 5;
            ctx.fillStyle = '#FFF';
            ctx.beginPath();
            ctx.ellipse(x + 13, floatY + 10, eyeSize - 1, eyeHeight, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(x + 23, floatY + 10, eyeSize - 1, eyeHeight, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Iris
            ctx.fillStyle = eyeColor;
            ctx.beginPath();
            ctx.arc(x + 14, floatY + 10, 2.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(x + 24, floatY + 10, 2.5, 0, Math.PI * 2);
            ctx.fill();
            
            // Pupil
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(x + 14, floatY + 10, 1.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(x + 24, floatY + 10, 1.2, 0, Math.PI * 2);
            ctx.fill();
            
            // Eye shine
            ctx.fillStyle = '#FFF';
            ctx.beginPath();
            ctx.arc(x + 15, floatY + 9, 1, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(x + 25, floatY + 9, 1, 0, Math.PI * 2);
            ctx.fill();
            
            // Eyelashes for female
            if (isFemale) {
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(x + 9, floatY + 6);
                ctx.lineTo(x + 8, floatY + 4);
                ctx.moveTo(x + 11, floatY + 5);
                ctx.lineTo(x + 10, floatY + 3);
                ctx.moveTo(x + 27, floatY + 6);
                ctx.lineTo(x + 28, floatY + 4);
                ctx.moveTo(x + 25, floatY + 5);
                ctx.lineTo(x + 26, floatY + 3);
                ctx.stroke();
            }
            
            // Eyebrows
            ctx.strokeStyle = hairColor;
            ctx.lineWidth = isFemale ? 1.5 : 2;
            ctx.beginPath();
            ctx.moveTo(x + 10, floatY + 5);
            ctx.quadraticCurveTo(x + 13, floatY + 3, x + 16, floatY + 5);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x + 20, floatY + 5);
            ctx.quadraticCurveTo(x + 23, floatY + 3, x + 26, floatY + 5);
            ctx.stroke();
            ctx.lineWidth = 1;
            
            // Nose
            ctx.fillStyle = skinDark;
            ctx.beginPath();
            ctx.ellipse(x + 18, floatY + 13, isFemale ? 2 : 3, 2, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Smile! 😊
            ctx.strokeStyle = '#C0392B';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(x + 18, floatY + 14, 6, 0.2, Math.PI - 0.2);
            ctx.stroke();
            ctx.lineWidth = 1;
            
            // Mustache (only for male characters with mustache)
            if (char.hasMustache) {
                const mustacheGrad = ctx.createLinearGradient(x + 9, floatY + 15, x + 27, floatY + 20);
                mustacheGrad.addColorStop(0, hairColor);
                mustacheGrad.addColorStop(0.5, shadeColor(hairColor, -15));
                mustacheGrad.addColorStop(1, shadeColor(hairColor, -30));
                ctx.fillStyle = mustacheGrad;
                ctx.beginPath();
                ctx.moveTo(x + 18, floatY + 16);
                ctx.quadraticCurveTo(x + 8, floatY + 17, x + 6, floatY + 21);
                ctx.quadraticCurveTo(x + 10, floatY + 19, x + 18, floatY + 18);
                ctx.quadraticCurveTo(x + 26, floatY + 19, x + 30, floatY + 21);
                ctx.quadraticCurveTo(x + 28, floatY + 17, x + 18, floatY + 16);
                ctx.fill();
            }
            
            // Lipstick for female
            if (isFemale) {
                ctx.fillStyle = '#E74C3C';
                ctx.beginPath();
                ctx.ellipse(x + 18, floatY + 18, 4, 2, 0, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Legs
            const legGrad = ctx.createLinearGradient(x + 7, floatY + 42, x + 16, floatY + 48);
            legGrad.addColorStop(0, char.pantsColor);
            legGrad.addColorStop(1, shadeColor(char.pantsColor, -30));
            ctx.fillStyle = legGrad;
            
            if (isFemale) {
                // Leggings/tights
                ctx.fillStyle = skinTone;
            }
            ctx.beginPath();
            ctx.roundRect(x + 7, floatY + 44, 10, 8, 2);
            ctx.fill();
            ctx.beginPath();
            ctx.roundRect(x + 19, floatY + 44, 10, 8, 2);
            ctx.fill();
            
            // Shoes
            const shoeColor = isFemale ? char.color : '#8B4513';
            const shoeGrad = ctx.createRadialGradient(x + 10, floatY + 50, 0, x + 12, floatY + 52, 10);
            shoeGrad.addColorStop(0, shadeColor(shoeColor, 20));
            shoeGrad.addColorStop(0.6, shoeColor);
            shoeGrad.addColorStop(1, shadeColor(shoeColor, -30));
            ctx.fillStyle = shoeGrad;
            ctx.beginPath();
            ctx.ellipse(x + 11, floatY + 52, 8, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(x + 25, floatY + 52, 8, 5, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Shoe shine
            ctx.fillStyle = 'rgba(255,255,255,0.3)';
            ctx.beginPath();
            ctx.ellipse(x + 9, floatY + 50, 3, 2, -0.3, 0, Math.PI * 2);
            ctx.fill();
            
            // High heels for female
            if (isFemale) {
                ctx.fillStyle = shadeColor(shoeColor, -30);
                ctx.fillRect(x + 8, floatY + 52, 3, 5);
                ctx.fillRect(x + 22, floatY + 52, 3, 5);
            }
        }
        
        // Draw player at specific position (for title screen preview - enhanced)
        function drawPlayerAt(x, y, facingRight) {
            // Use the first character (Mario style) for title preview
            drawCharacterPreview(x, y, characters[0]);
        }

        // Draw level progress bar
        function drawProgressBar() {
            const progress = player.x / WORLD_WIDTH;
            const barWidth = 200;
            const barHeight = 8;
            const barX = canvas.width - barWidth - 20;
            const barY = 20;
            
            // Background
            ctx.fillStyle = 'rgba(0,0,0,0.5)';
            ctx.roundRect(barX - 5, barY - 5, barWidth + 10, barHeight + 10, 5);
            ctx.fill();
            
            // Progress track
            ctx.fillStyle = '#444';
            ctx.fillRect(barX, barY, barWidth, barHeight);
            
            // Progress fill
            const gradient = ctx.createLinearGradient(barX, 0, barX + barWidth, 0);
            gradient.addColorStop(0, '#00FF7F');
            gradient.addColorStop(1, '#FFD700');
            ctx.fillStyle = gradient;
            ctx.fillRect(barX, barY, barWidth * progress, barHeight);
            
            // Flag icon at end
            ctx.fillStyle = '#00FF7F';
            ctx.font = '14px Arial';
            ctx.fillText('🚩', barX + barWidth + 5, barY + 10);
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
            
            if ((e.key === 'r' || e.key === 'R') && (gameState === 'won' || gameState === 'lost')) {
                // Go back to character select (keep the name)
                gameState = 'character';
                overlay.style.display = 'none';
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
            player.x = 50;
            player.y = 350;
            player.velX = 0;
            player.velY = 0;
            player.onGround = false;
            player.facingRight = true;
            score = 0;
            gameState = 'playing';
            cameraX = 0;
            initCoins();
            initEnemies();
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
    <strong>🎮 Controls:</strong><br>
    <kbd>← →</kbd> or <kbd>A D</kbd> Move &nbsp;|&nbsp; 
    <kbd>Space</kbd> or <kbd>↑</kbd> Jump &nbsp;|&nbsp;
    <kbd>R</kbd> Restart
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🪙 **Collect** all the coins!")
with col2:
    st.markdown("👾 **Avoid** the purple enemies!")
with col3:
    st.markdown("🚩 **Reach** the flag to win!")


