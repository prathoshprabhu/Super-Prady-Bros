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
        <canvas id="gameCanvas" width="900" height="500"></canvas>
        <div id="overlay">
            <h1 id="overlayTitle">🎉 YOU WIN! 🎉</h1>
            <p id="overlayScore">Coins: 0/10</p>
            <p class="restart-hint">Press SPACE or R to play again</p>
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

        // Game constants (tuned for comfortable gameplay)
        const GRAVITY = 0.4;
        const JUMP_STRENGTH = -11;
        const PLAYER_SPEED = 3.5;
        
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
        let gameState = 'playing'; // 'playing', 'won', 'lost'
        let score = 0;
        let animationFrame = 0;

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

        // Enemies - More scary red monsters across the level
        let enemies = [];
        function initEnemies() {
            enemies = [
                // Section 1
                { x: 100, y: 412, width: 38, height: 38, patrolLeft: 50, patrolRight: 350, direction: 1, animFrame: 0 },
                { x: 280, y: 412, width: 38, height: 38, patrolLeft: 50, patrolRight: 350, direction: -1, animFrame: 0 },
                // Section 2
                { x: 550, y: 412, width: 38, height: 38, patrolLeft: 500, patrolRight: 680, direction: 1, animFrame: 0 },
                // Section 3
                { x: 850, y: 412, width: 38, height: 38, patrolLeft: 800, patrolRight: 930, direction: 1, animFrame: 0 },
                { x: 910, y: 242, width: 38, height: 38, patrolLeft: 880, patrolRight: 960, direction: -1, animFrame: 0 },
                // Section 4
                { x: 1100, y: 412, width: 38, height: 38, patrolLeft: 1050, patrolRight: 1280, direction: 1, animFrame: 0 },
                { x: 1200, y: 412, width: 38, height: 38, patrolLeft: 1050, patrolRight: 1280, direction: -1, animFrame: 0 },
                // Section 5
                { x: 1420, y: 412, width: 38, height: 38, patrolLeft: 1400, patrolRight: 1500, direction: 1, animFrame: 0 },
                // Section 6
                { x: 1750, y: 412, width: 38, height: 38, patrolLeft: 1700, patrolRight: 1880, direction: 1, animFrame: 0 },
                { x: 1780, y: 312, width: 38, height: 38, patrolLeft: 1750, patrolRight: 1830, direction: -1, animFrame: 0 },
                // Section 7
                { x: 2050, y: 412, width: 38, height: 38, patrolLeft: 2000, patrolRight: 2130, direction: 1, animFrame: 0 },
                // Section 8
                { x: 2350, y: 412, width: 38, height: 38, patrolLeft: 2300, patrolRight: 2480, direction: 1, animFrame: 0 },
                { x: 2450, y: 412, width: 38, height: 38, patrolLeft: 2300, patrolRight: 2480, direction: -1, animFrame: 0 },
                // Final area - guardians
                { x: 2700, y: 412, width: 38, height: 38, patrolLeft: 2650, patrolRight: 2850, direction: 1, animFrame: 0 },
                { x: 2800, y: 412, width: 38, height: 38, patrolLeft: 2650, patrolRight: 2950, direction: -1, animFrame: 0 },
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

        // Initialize game
        function initGame() {
            player.x = 50;
            player.y = 350;
            player.velX = 0;
            player.velY = 0;
            player.onGround = false;
            player.facingRight = true;
            score = 0;
            gameState = 'playing';
            cameraX = 0;  // Reset camera
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

        // Draw player
        function drawPlayer() {
            const { x, y, width, height, facingRight } = player;
            
            // Body (red overalls)
            ctx.fillStyle = COLORS.player;
            ctx.fillRect(x + 4, y + 18, 28, 27);
            
            // Head
            ctx.fillStyle = COLORS.playerFace;
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + 11, 11, 11, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Hat
            ctx.fillStyle = COLORS.player;
            ctx.fillRect(x + 4, y, 28, 9);
            if (facingRight) {
                ctx.fillRect(x + 24, y + 4, 10, 7);
            } else {
                ctx.fillRect(x + 2, y + 4, 10, 7);
            }
            
            // Eye
            const eyeX = facingRight ? x + 20 : x + 12;
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(eyeX, y + 11, 2.5, 0, Math.PI * 2);
            ctx.fill();
            
            // Mustache
            ctx.fillStyle = '#654321';
            ctx.beginPath();
            ctx.ellipse(x + width/2, y + 17, 9, 3, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Legs
            ctx.fillStyle = '#00008B';
            ctx.fillRect(x + 7, y + 38, 9, 7);
            ctx.fillRect(x + 20, y + 38, 9, 7);
            
            // Shoes
            ctx.fillStyle = '#654321';
            ctx.beginPath();
            ctx.ellipse(x + 11, y + 43, 6, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(x + 25, y + 43, 6, 4, 0, 0, Math.PI * 2);
            ctx.fill();
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
            overlayScore.textContent = `Coins: ${score}/${coins.length}`;
            overlay.style.display = 'flex';
        }

        // Game won
        function gameWon() {
            gameState = 'won';
            overlayTitle.textContent = '🎉 YOU WIN! 🎉';
            overlayScore.textContent = `Coins: ${score}/${coins.length}`;
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
            drawFlag();
            drawPlayer();
            
            ctx.restore();
            
            // UI is drawn without camera offset
            drawUI();
            
            // Draw progress bar at top
            drawProgressBar();
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
            if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = true;
            if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = true;
            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W' || e.key === ' ') keys.jump = true;
            
            if ((e.key === 'r' || e.key === 'R' || e.key === ' ') && gameState !== 'playing') {
                initGame();
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

        // Click to focus (for keyboard input)
        canvas.addEventListener('click', () => {
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

