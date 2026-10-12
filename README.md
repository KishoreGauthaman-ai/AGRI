# AgriVision - Smart Farming Assistant

AgriVision is a Python-based desktop application for smart farming, featuring Weather monitoring, Plant Disease Detection, Crop Spacing Calculation, and an AI Chatbot.

**UI Theme:** Apple Glassmorphism — frosted translucent cards, light borders, gradient backgrounds with smooth rounded corners. Supports both Light and Dark glass modes via the top-bar toggle.

## 🧱 Architecture
- **Framework**: KivyMD (Material Design M3)
- **UI Theme**: Apple Glassmorphism (translucent cards, rounded glass surfaces, light/dark adaptive colors)
- **AI/ML**: PyTorch / ONNX Runtime (LeafGuard Disease Detection), OpenAI (AgroBot Chatbot)
- **API**: OpenWeatherMap (Weather data)

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9+
- pip (Python package manager)

### 2. Installation
1. Clone or extract the project folder.
2. Navigate to the project directory:
   ```bash
   cd AgriVision
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. API Key Configuration
Open the `.env` file and verify your API Keys:
- **OPENAI_API_KEY**: Required for AgroBot chat feature (add yours)
- **OPENWEATHER_API_KEY**: Add your OpenWeatherMap API key (Get one at openweathermap.org)

### 4. Running the App
Run the main entry point:
```bash
python agrivision_app.py
```

## 🧠 Models
The application uses an ONNX model (`model.onnx`) for the **LeafGuard** feature.
- The model file is located at the project root (`model.onnx`).
- The model expects a `plant_model.pth` (PyTorch format) or the converted `.onnx` version.
- If no model is found, the app will raise an initialization error; ensure `model.onnx` and `model.onnx.data` are present.
- The model classifies plant diseases across 15 classes (e.g., Tomato Early Blight, Potato Late Blight, Healthy leaves, etc.).
- To use real inference: keep `model.onnx` and `model.onnx.data` in the root directory.
- If the model is missing, you must provide your own trained `.pth` converted to ONNX, or place the provided files.

## 🛠 Features
1. **AgroSky**: Weather updates by city with live temperature, humidity, wind, and sea level.
2. **LeafGuard**: Detect plant diseases from uploaded leaf images using an ONNX model.
3. **CropSpace**: Calculate optimal spacing and plant counts based on field dimensions, crop type, soil, and pH.
4. **AgroBot**: Chat with an AI agriculture expert that analyzes weather, soil, spacing, and disease data.
5. **Cost Calculator**: Compute farm profit by entering crop, area, yield, price, and total cost.

## 🎨 Glass UI
- Light Glass Mode: bright translucent cards on a cool white-blue gradient background.
- Dark Glass Mode: deep translucent cards on a dark atmospheric gradient background.
- Toggle between modes using the theme icon in the AgroBot top app bar (`cog` → Settings).

## 🌐 Language Support
- **English** and **Tamil** (தமிழ்) languages supported.
- Open Settings (cog icon) in the AgroBot screen → choose **Language**.
- All UI text switches instantly, and AgroBot responds in the selected language.

## 📂 Project Structure
```
AGRI/
├── agrivision_app.py       # Main app entry
├── agrivision_app.kv        # Glass-themed UI layout
├── model.onnx              # ONNX inference model
├── model.onnx.data         # Model weights/data
├── plant_model.pth         # PyTorch model backup
├── api/
│   ├── weather_api.py      # OpenWeatherMap integration
│   └── chatbot_api.py      # OpenAI chatbot integration
├── .env                    # API keys
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## ⚠️ Notes
- The `.kv` layout is kept identical across both light and dark glass modes; only colors, card transparency, and borders change.
- The app runs in a single `MDScreen` with `MDBottomNavigation` for quick access to all modules.
