# 🍄 Super Prady Bros 🍄

A fun Mario-style platformer game built with Python!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)

## 🎮 Play Online!

**🌐 Play now at: [pradygame1.streamlit.app](https://pradygame1.streamlit.app)**

## 🎯 How to Play

### Controls
| Key | Action |
|-----|--------|
| ← → or A/D | Move left/right |
| Space or ↑ or W | Jump |
| R | Restart game |

### Objective
- **Collect coins** 🪙 - Gather all the shiny coins for a high score
- **Avoid enemies** 👾 - Don't touch the purple creatures!
- **Reach the flag** 🚩 - Get to the green flag to win!
- **Don't fall** ⚠️ - Watch out for gaps in the ground!

## 🚀 Run Locally

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the game folder:**
   ```bash
   cd pradygame1
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the web version:**
   ```bash
   streamlit run app.py
   ```

5. **Or run the desktop version (requires pygame):**
   ```bash
   pip install pygame
   python game.py
   ```

## 🌐 Deploy to Streamlit Cloud

1. Push this code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and `app.py` as the main file
5. Click "Deploy"!

Your game will be live at `your-app-name.streamlit.app`

## 🎨 Game Features

- ✅ Smooth player movement and jumping physics
- ✅ Animated player character with a Mario-like appearance
- ✅ Multiple platforms at different heights
- ✅ Spinning, floating coins to collect
- ✅ Patrolling enemies with animations
- ✅ Beautiful gradient sky background with moving clouds
- ✅ Waving victory flag
- ✅ Score tracking
- ✅ Win and game over screens
- ✅ Mobile touch controls support
- ✅ Works in any modern web browser!

## 📁 Project Structure

```
pradygame1/
├── app.py            # Web version (Streamlit + HTML5 Canvas)
├── game.py           # Desktop version (Pygame)
├── requirements.txt  # Python dependencies
├── .streamlit/
│   └── config.toml   # Streamlit theme configuration
└── README.md         # This file!
```

## 🛠️ Technical Details

### Web Version (app.py)
- **Streamlit** - Hosts the game as a web application
- **HTML5 Canvas** - Renders the game graphics
- **JavaScript** - Handles game logic and animations

### Desktop Version (game.py)
- **Pygame** - Native game rendering
- **Object-Oriented Python** - Clean code structure

## 🎉 Have Fun!

Enjoy playing Super Prady Bros! Feel free to modify the code and make it your own.

Happy coding! 🚀

