from kivymd.app import MDApp
from kivy.lang import Builder
from api.weather_api import WeatherAPI
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
import threading
from api.chatbot_api import ChatbotAPI
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
import re
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime
from plyer import filechooser
from PIL import Image
import os
import onnxruntime as ort
import numpy as np
import traceback
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

TRANSLATIONS = {
    "English": {
        "nav_weather": "AgroSky",
        "nav_spacing": "CropSpace",
        "nav_disease": "LeafGuard",
        "nav_chat": "AgroBot",
        "nav_cost": "Cost",
        "weather_title": "AGROSKY",
        "city_hint": "Enter City Name",
        "get_weather": "Get Weather",
        "loading": "Loading...",
        "select_city": "Select a City",
        "humidity_label": "Humidity --%",
        "wind_label": "Wind Speed --km/h",
        "feels_like": "Feels Like",
        "sea_level": "Sea Level",
        "disease_title": "LeafGuard – AI Disease Detection",
        "upload_leaf": "Upload Leaf Image",
        "analyze_disease": "Analyze Disease",
        "result_placeholder": "Prediction result will appear here.",
        "smart_analysis": "Smart Farm AI Analysis",
        "run_analysis": "Run Smart Farm Analysis",
        "spacing_title": "Crop Planning Suite",
        "field_details": "Field Details",
        "field_length": "Field Length (meters)",
        "field_width": "Field Width (meters)",
        "select_crop": "Select Crop",
        "soil_env": "Soil & Environment",
        "select_soil": "Select Soil Type",
        "select_moisture": "Select Moisture Level",
        "ph_hint": "Soil pH Level",
        "chat_title": "AgroBot",
        "ask_hint": "Ask AgroBot...",
        "profit_title": "Farm Profit Calculator",
        "crop_name": "Crop Name (Example: Tomato)",
        "area_acres": "Area (Acres)",
        "yield_acre": "Yield per Acre (Tons)",
        "market_price": "Market Price per Kg (₹)",
        "prod_cost": "Total Production Cost (₹)",
        "calc_profit": "Calculate Profit",
        "enter_city": "Please enter a city name",
        "error": "Error",
        "upload_first": "Please upload an image first.",
        "valid_numbers": "Please enter valid numbers.",
        "crop_lbl": "Crop",
        "production": "Production",
        "revenue": "Revenue",
        "cost": "Cost",
        "profit": "Profit",
        "margin": "Margin",
        "plant": "Plant",
        "disease": "Disease",
        "confidence": "Confidence",
        "settings_title": "Settings & About",
        "theme_settings": "Theme Settings",
        "theme_btn": "Toggle Theme (Current:",
        "language": "Language",
        "language_btn": "Select Language",
        "close": "CLOSE",
        "app_overview": "App Overview",
        "model_section": "AI / ML Model",
        "api_section": "APIs",
        "features_section": "Features",
        "app_overview_txt": "AgriVision is a Python-based smart farming desktop app using KivyMD M3 with an Apple Glass UI theme (translucent cards, rounded surfaces, light/dark modes). Navigation uses MDBottomNavigation for quick module access.",
        "model_txt": "LeafGuard uses an ONNX model (model.onnx) located at the project root. It classifies 15 plant disease classes (Tomato, Potato, Pepper, etc.). Real inference requires the .onnx file.",
        "api_txt": "AgroSky uses OpenWeatherMap for weather data. AgroBot uses Groq/OpenAI for agricultural expert chat responses. Both require API keys in the .env file.",
        "features_txt": "AgroSky: weather by city. LeafGuard: disease detection from leaf images. CropSpace: spacing and density calculations. AgroBot: AI chat with farm analysis. Cost: profit calculator.",
        "language_prompt": "You MUST respond entirely in English.",
    },
    "Tamil": {
        "nav_weather": "வானிலை",
        "nav_spacing": "பயிர் இடைவெளி",
        "nav_disease": "இலை பாதுகாப்பு",
        "nav_chat": "AgroBot",
        "nav_cost": "செலவு",
        "weather_title": "வானிலை",
        "city_hint": "நகரத்தின் பெயரை உள்ளிடவும்",
        "get_weather": "வானிலை பெறு",
        "loading": "ஏற்றுகிறது...",
        "select_city": "நகரத்தை தேர்ந்தெடுக்கவும்",
        "humidity_label": "ஈரப்பதம் --%",
        "wind_label": "காற்று வேகம் --km/h",
        "feels_like": "உணர்வு",
        "sea_level": "கடல் மட்டம்",
        "disease_title": "இலை பாதுகாப்பு – AI நோய் கண்டறிதல்",
        "upload_leaf": "இலை படத்தை பதிவேற்றவும்",
        "analyze_disease": "நோயை பகுப்பாய்வு செய்",
        "result_placeholder": "முன்னறிவிப்பு முடிவு இங்கே தோன்றும்.",
        "smart_analysis": "ஸ்மார்ட் பண்ணை AI பகுப்பாய்வு",
        "run_analysis": "ஸ்மார்ட் பண்ணை பகுப்பாய்வை இயக்கவும்",
        "spacing_title": "பயிர் திட்டமிடல்",
        "field_details": "வயல் விவரங்கள்",
        "field_length": "வயல் நீளம் (மீட்டர்)",
        "field_width": "வயல் அகலம் (மீட்டர்)",
        "select_crop": "பயிர் தேர்ந்தெடுக்கவும்",
        "soil_env": "மண் & சூழல்",
        "select_soil": "மண் வகை தேர்ந்தெடுக்கவும்",
        "select_moisture": "ஈரப்பத அளவை தேர்ந்தெடுக்கவும்",
        "ph_hint": "மண் pH அளவு",
        "chat_title": "AgroBot",
        "ask_hint": "AgroBot-ஐ கேளுங்கள்...",
        "profit_title": "பண்ணை லாப கணக்கீடு",
        "crop_name": "பயிர் பெயர் (எடுத்துக்காட்டு: தக்காளி)",
        "area_acres": "பரப்பளவு (ஏக்கர்)",
        "yield_acre": "ஒரு ஏக்கர் விளைச்சல் (டன்)",
        "market_price": "ஒரு கிலோ சந்தை விலை (₹)",
        "prod_cost": "மொத்த உற்பத்தி செலவு (₹)",
        "calc_profit": "லாபத்தை கணக்கிடு",
        "enter_city": "தயவுசெய்து நகரத்தின் பெயரை உள்ளிடவும்",
        "error": "பிழை",
        "upload_first": "முதலில் ஒரு படத்தை பதிவேற்றவும்.",
        "valid_numbers": "சரியான எண்களை உள்ளிடவும்.",
        "crop_lbl": "பயிர்",
        "production": "உற்பத்தி",
        "revenue": "வருவாய்",
        "cost": "செலவு",
        "profit": "லாபம்",
        "margin": "விளிம்பு",
        "plant": "செடி",
        "disease": "நோய்",
        "confidence": "நம்பிக்கை",
        "settings_title": "அமைப்புகள் & பற்றி",
        "theme_settings": "தீம் அமைப்புகள்",
        "theme_btn": "தீம் மாற்று (தற்போது:",
        "language": "மொழி",
        "language_btn": "மொழியை தேர்ந்தெடுக்கவும்",
        "close": "மூடு",
        "app_overview": "பயன்பாடு கண்ணோட்டம்",
        "model_section": "AI / ML மாதிரி",
        "api_section": "APIகள்",
        "features_section": "அம்சங்கள்",
        "app_overview_txt": "AgriVision என்பது Python அடிப்படையிலான ஸ்மார்ட் விவசாய டெஸ்க்டாப் பயன்பாடு. KivyMD M3 உடன் ஆப்பிள் கிளாஸ் UI தீம் (translucent cards, rounded surfaces, light/dark modes). MDBottomNavigation மூலம் விரைவான அணுகல்.",
        "model_txt": "LeafGuard ONNX மாதிரியை (model.onnx) பயன்படுத்துகிறது. இது 15 வகையான தாவர நோய்களை (தக்காளி, உருளைக்கிழங்கு, மிளகு போன்றவை) அடையாளம் காட்டுகிறது.",
        "api_txt": "AgroSky வானிலைக்கு OpenWeatherMap-ஐ பயன்படுத்துகிறது. AgroBot விவசாய ஆலோசனைகளுக்கு Groq/OpenAI-ஐ பயன்படுத்துகிறது. API விசைகள் .env கோப்பில் இருக்க வேண்டும்.",
        "features_txt": "AgroSky: நகரம் வாரியாக வானிலை. LeafGuard: இலை படங்களில் இருந்து நோய் கண்டறிதல். CropSpace: இடைவெளி மற்றும் அடர்த்தி கணக்கீடு. AgroBot: விவசாய பகுப்பாய்வுடன் AI அரட்டை. Cost: லாப கணக்கீடு.",
        "language_prompt": "You MUST respond entirely in Tamil. Use proper Tamil script (தமிழ்).",
    },
}

class AgriApp(MDApp):

    #SECTION 1
    weather_icon = StringProperty("weather-cloudy")
    temperature = StringProperty("--°C")
    humidity = StringProperty("Humidity --%")
    wind = StringProperty("Wind Speed --km/h")
    condition = StringProperty("Select a City")
    feels_like = StringProperty("Feels Like")
    sea_level = StringProperty("Sea Level")
    coord=""
    plant_1 = ""
    diseases_1 = ""
    language = StringProperty("English")

    def tr(self, key):
        return TRANSLATIONS.get(self.language, TRANSLATIONS["English"]).get(key, key)

    def set_language(self, lang):
        self.language = lang
        self.update_language()

    def update_language(self):
        lang_prompt = self.tr("language_prompt")
        base_prompt = (
            "You are AgroBot, a smart agricultural assistant integrated into a farm management system.\n\n"
            "CRITICAL: NEVER HALLUCINATE. Only analyze the exact data provided. Do not invent weather, diseases, crops, soil types, or measurements that were not explicitly given.\n\n"
            "You receive contextual farm data when available such as weather, soil, crop type, and measurements of the land.\n"
            "Only analyze the data that is provided.\n\n"
            "Behavior Rules:\n"
            "- If weather data is provided → analyze weather impact only using those numbers.\n"
            "- If soil data is provided → analyze soil suitability using that exact soil type and pH.\n"
            "- If land measurements data is provided → analyze planting efficiency such as spacing and fertilizers based ONLY on the given length, width, crop, soil, moisture, and pH.\n"
            "- If full farm data is provided → give complete farm analysis, but stick strictly to the provided values.\n"
            "- NEVER guess a plant name, disease name, or crop type. If a leaf image result is provided, repeat the exact plant and disease names from the result without altering them.\n"
            "- If a user asks for data from history, retrieve only the exact historical entries given in the conversation.\n\n"
            "Respond clearly and concisely. Use structured headings only when full analysis is requested. For simple questions, respond briefly. Avoid unnecessary over-analysis.\n\n"
            + lang_prompt
        )
        if hasattr(self, "chatbot"):
            self.chatbot.set_system_prompt(base_prompt)

        if not self.root:
            return
        ids = self.root.ids
        ids.nav_weather.text = self.tr("nav_weather")
        ids.nav_spacing.text = self.tr("nav_spacing")
        ids.nav_disease.text = self.tr("nav_disease")
        ids.nav_chat.text = self.tr("nav_chat")
        ids.nav_cost.text = self.tr("nav_cost")
        ids.weather_title.text = self.tr("weather_title")
        ids.city_field.hint_text = self.tr("city_hint")
        ids.search_btn.text = self.tr("get_weather")
        if self.condition in (TRANSLATIONS["English"]["select_city"], TRANSLATIONS["Tamil"]["select_city"]):
            self.condition = self.tr("select_city")
        ids.spacing_title.text = self.tr("spacing_title")
        ids.field_details.text = self.tr("field_details")
        ids.field_length.hint_text = self.tr("field_length")
        ids.field_width.hint_text = self.tr("field_width")
        ids.crop_dropdown.text = self.tr("select_crop")
        ids.soil_env.text = self.tr("soil_env")
        ids.soil_dropdown.text = self.tr("select_soil")
        ids.moisture_dropdown.text = self.tr("select_moisture")
        ids.ph_input.hint_text = self.tr("ph_hint")
        ids.smart_analysis.text = self.tr("smart_analysis")
        ids.run_analysis.text = self.tr("run_analysis")
        ids.disease_title.text = self.tr("disease_title")
        ids.upload_leaf.text = self.tr("upload_leaf")
        ids.analyze_disease.text = self.tr("analyze_disease")
        if ids.result_label.text in (TRANSLATIONS["English"]["result_placeholder"], TRANSLATIONS["Tamil"]["result_placeholder"]):
            ids.result_label.text = self.tr("result_placeholder")
        ids.smart_analysis_leaf.text = self.tr("smart_analysis")
        ids.run_analysis_leaf.text = self.tr("run_analysis")
        ids.chat_title.title = self.tr("chat_title")
        ids.user_input.hint_text = self.tr("ask_hint")
        ids.profit_title.text = self.tr("profit_title")
        ids.profit_crop.hint_text = self.tr("crop_name")
        ids.profit_area.hint_text = self.tr("area_acres")
        ids.profit_yield.hint_text = self.tr("yield_acre")
        ids.profit_price.hint_text = self.tr("market_price")
        ids.profit_cost.hint_text = self.tr("prod_cost")
        ids.calc_profit.text = self.tr("calc_profit")
    

    

    def build(self):
        self.chat_history = []
        self.chatbot = ChatbotAPI(
            "You are AgroBot, a smart agricultural assistant integrated into a farm management system.\n\n"
            "CRITICAL: NEVER HALLUCINATE. Only analyze the exact data provided. Do not invent weather, diseases, crops, soil types, or measurements that were not explicitly given.\n\n"
            "You receive contextual farm data when available such as weather, soil, crop type, and measurements of the land.\n"
            "Only analyze the data that is provided.\n\n"
            "Behavior Rules:\n"
            "- If weather data is provided → analyze weather impact only using those numbers.\n"
            "- If soil data is provided → analyze soil suitability using that exact soil type and pH.\n"
            "- If land measurements data is provided → analyze planting efficiency such as spacing and fertilizers based ONLY on the given length, width, crop, soil, moisture, and pH.\n"
            "- If full farm data is provided → give complete farm analysis, but stick strictly to the provided values.\n"
            "- NEVER guess a plant name, disease name, or crop type. If a leaf image result is provided, repeat the exact plant and disease names from the result without altering them.\n"
            "- If a user asks for data from history, retrieve only the exact historical entries given in the conversation.\n\n"
            "Respond clearly and concisely. Use structured headings only when full analysis is requested. For simple questions, respond briefly. Avoid unnecessary over-analysis."
            )

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.dark_mode = True
        self.set_glass_colors()
        self.model = None

        # Register Tamil font (Variable covers Latin + Tamil) for SDL2 rendering
        from kivy.core.text import LabelBase
        LabelBase.register(
            name='NotoTamil',
            fn_regular='fonts/NotoSansTamil-Variable.ttf',
            fn_bold='fonts/NotoSansTamil-Variable.ttf',
            fn_italic='fonts/NotoSansTamil-Variable.ttf',
            fn_bolditalic='fonts/NotoSansTamil-Variable.ttf',
        )
        # KivyMD font_styles override font_name -> point every style at the Tamil font
        # (skip "Icon": it must keep the Material Icons font for MDIcon rendering)
        for style in self.theme_cls.font_styles:
            if style == "Icon":
                continue
            self.theme_cls.font_styles[style][0] = 'NotoTamil'
        return Builder.load_file("agrivision_app.kv")
    
    #SECTION GLASS THEME
    def set_glass_colors(self):
        if self.dark_mode:
            # Apple Glass Dark — improved deep premium glass
            self.theme_bg_color = (0.05, 0.06, 0.1, 0.92)
            self.theme_nav_color = (0.03, 0.04, 0.08, 0.95)
            self.theme_card_color = (0.18, 0.2, 0.26, 0.55)
            self.theme_btn_color = (0.35, 0.45, 0.75, 0.95)
            self.theme_line_color = (0.9, 0.92, 1, 0.18)
            self.theme_text_color = (0.96, 0.97, 1, 1)
            self.theme_sub_color = (0.8, 0.84, 0.92, 1)
            self.theme_title_color = (0.98, 0.98, 1, 1)
            self.theme_icon_color = (0.85, 0.88, 1, 1)
            self.theme_hint_color = (0.75, 0.78, 0.85, 1)
            self.theme_field_fill = (0.12, 0.14, 0.2, 0.5)
        else:
            # Apple Glass Light
            self.theme_bg_color = (0.92, 0.95, 0.98, 0.85)
            self.theme_nav_color = (0.88, 0.92, 0.96, 0.95)
            self.theme_card_color = (1, 1, 1, 0.45)
            self.theme_btn_color = (0.35, 0.5, 0.75, 0.95)
            self.theme_line_color = (0, 0, 0, 0.12)
            self.theme_text_color = (0.1, 0.1, 0.15, 1)
            self.theme_sub_color = (0.35, 0.38, 0.45, 0.9)
            self.theme_title_color = (0.1, 0.12, 0.2, 1)
            self.theme_icon_color = (0.2, 0.3, 0.6, 1)
            self.theme_hint_color = (0.5, 0.52, 0.58, 0.9)
            self.theme_field_fill = (1, 1, 1, 0.3)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.theme_cls.theme_style = "Dark" if self.dark_mode else "Light"
        self.set_glass_colors()
        # Refresh labels/cards by notifying theme change
        self.theme_cls.primary_palette = "BlueGray"

    def open_settings(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.menu import MDDropdownMenu
        from kivymd.uix.list import OneLineListItem
        from kivy.uix.scrollview import ScrollView
        from kivy.metrics import dp

        scroll = ScrollView(size_hint_y=None, height=dp(560))
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(20),
            adaptive_height=True,
            size_hint_y=None,
            md_bg_color=self.theme_bg_color,
        )
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)

        # Theme Toggle Card
        theme_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            radius=[20],
            elevation=6,
            adaptive_height=True,
            md_bg_color=self.theme_card_color,
            line_color=self.theme_line_color,
        )
        theme_card.add_widget(MDLabel(
            text="[b]" + self.tr("theme_settings") + "[/b]",
            markup=True,
            font_name="NotoTamil",
            theme_text_color="Custom",
            text_color=self.theme_title_color,
            adaptive_height=True,
        ))
        theme_btn = MDFlatButton(
            text=self.tr("theme_btn") + ("Dark" if self.dark_mode else "Light") + ")",
            on_release=lambda *args: self._toggle_from_settings(theme_btn)
        )
        theme_card.add_widget(theme_btn)
        content.add_widget(theme_card)

        # Language Card
        lang_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            radius=[20],
            elevation=6,
            adaptive_height=True,
            md_bg_color=self.theme_card_color,
            line_color=self.theme_line_color,
        )
        lang_card.add_widget(MDLabel(
            text="[b]" + self.tr("language") + "[/b]",
            markup=True,
            font_name="NotoTamil",
            theme_text_color="Custom",
            text_color=self.theme_title_color,
            adaptive_height=True,
        ))
        lang_btn = MDFlatButton(
            text=self.language,
            on_release=lambda *args: self._open_language_menu(lang_btn)
        )
        lang_card.add_widget(lang_btn)
        content.add_widget(lang_card)

        # About Cards
        about_sections = [
            (self.tr("app_overview"), self.tr("app_overview_txt")),
            (self.tr("model_section"), self.tr("model_txt")),
            (self.tr("api_section"), self.tr("api_txt")),
            (self.tr("features_section"), self.tr("features_txt")),
        ]
        for title, desc in about_sections:
            card = MDCard(
                orientation="vertical",
                padding=dp(15),
                spacing=dp(10),
                radius=[25],
                elevation=8,
                adaptive_height=True,
                size_hint_y=None,
                md_bg_color=self.theme_card_color,
                line_color=self.theme_line_color,
            )
            card.add_widget(MDLabel(
                text=f"[b]{title}[/b]",
                markup=True,
                font_name="NotoTamil",
                theme_text_color="Custom",
                text_color=self.theme_title_color,
                size_hint_y=None,
                height=dp(30),
            ))
            desc_label = MDLabel(
                text=desc,
                font_name="NotoTamil",
                theme_text_color="Custom",
                text_color=self.theme_text_color,
                adaptive_height=True,
                size_hint_y=None,
            )
            desc_label.bind(
                width=lambda instance, value: setattr(instance, "text_size", (value, None))
            )
            desc_label.bind(
                texture_size=lambda instance, value: setattr(instance, "height", value[1])
            )
            card.add_widget(desc_label)
            content.add_widget(card)

        dialog = MDDialog(
            title=self.tr("settings_title"),
            type="custom",
            content_cls=scroll,
            buttons=[MDFlatButton(text=self.tr("close"), on_release=lambda x: dialog.dismiss())],
            size_hint=(0.92, 0.85),
        )
        dialog.open()

    def _open_language_menu(self, button):
        menu_items = [
            {
                "text": "English",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="English": self._select_language(button, x),
            },
            {
                "text": "Tamil",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Tamil": self._select_language(button, x),
            },
        ]
        self._lang_menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=4,
        )
        self._lang_menu.open()

    def _select_language(self, button, lang):
        self._lang_menu.dismiss()
        self.set_language(lang)
        button.text = lang

    def _toggle_from_settings(self, button):
        self.toggle_theme()
        button.text = self.tr("theme_btn") + ("Dark" if self.dark_mode else "Light") + ")"

    #SECTION 2
    def get_weather(self):
        city = self.root.ids.city_field.text
        if not city:
            self.show_error("Please enter a city name")
            return

        self.root.ids.search_btn.text = self.tr("loading")
        Clock.schedule_once(lambda dt: self._fetch_weather(city), .15)
        

    def bot_processing(self):
        weather_data = {
            "city": self.root.ids.city_field.text,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "condition": self.condition,
            "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
            "prompt": "Read them properply",
            "coordniates": (self.coord),
            "data": getattr(self,"data","")
            }

        
        self.chat_history.append({
            "role": "user",
            "content": str(weather_data) # limit stored length
        })
        response = self.chatbot.get_response(str(weather_data), self.chat_history)
        self.chat_history.append({
            "role": "assistant",
            "content": str(response[:1000])  # limit stored length
        })
        


    #SECTION 3
    def _fetch_weather(self, city):
        data = WeatherAPI.get_weather(city)
        self.root.ids.search_btn.text = self.tr("get_weather")


        if "error" in data:
            self.show_error(data["error"])
        else:
            self.temperature = f"{data['temp']}°C"
            self.humidity = f"{self.tr('humidity_label').split('--')[0]}{data['humidity']}%"
            self.wind = f"{self.tr('wind_label').split('--')[0]}{data['wind_speed']} km/h"
            self.condition = data['condition']
            self.weather_icon = data['icon']
            self.sea_level = f"{self.tr('sea_level')} {data['sea_level']}"
            self.feels_like = f"{self.tr('feels_like')} {data['feels_like']}"
            self.coord = f"The Coordinates are {data['coord']}"
            self.data = f"The whole datas are {data['data']}"
            self.bot_processing()


    #SECTION 4
    def show_error(self, message):
        dialog = MDDialog(
            title=self.tr("error"),
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

#-------------------------------------------------------------------------------------------------------------------------------------------------
    #ChatBot Screen 


    # ------------------------
    # SEND MESSAGE To the chatbot API
    # ------------------------

    #SECTION 5
    def send_message(self):
        user_input = self.root.ids.user_input.text
        if not user_input.strip():
            return

        self.add_message_bubble(user_input, is_user=True)
        self.root.ids.user_input.text = ""
        self.root.ids.chat_scroll.scroll_y = 0

        # 🔹 Add loading bubble
        self.loading_widget = self.add_message_bubble(
            "AgroBot is typing...",
            is_user=False,
            loading=True
        )

        threading.Thread(
            target=self.get_bot_response,
            args=(user_input,),
            daemon=True
        ).start()

    # ------------------------
    # GET BOT RESPONSE
    # ------------------------

    #SECTION 6
    def get_bot_response(self, user_input):
        response = self.chatbot.get_response(user_input, self.chat_history)

        def update_ui(dt):
            # Remove loading bubble safely
            if hasattr(self, "loading_widget") and self.loading_widget:
                if self.loading_widget.parent:
                    self.loading_widget.parent.remove_widget(self.loading_widget)

            # Add fresh response bubble
            self.add_message_bubble(response, is_user=False)
            print(response)
        Clock.schedule_once(update_ui)

        # self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({
            "role": "user",
            "content": user_input[:1000]  # limit stored length
        })
        self.chat_history.append({
            "role": "assistant",
            "content": response[:1000]  # limit stored length
        })

    # ------------------------
    # ADD MESSAGE BUBBLE
    # ------------------------
    #SECTION 7
    def add_message_bubble(self, text, is_user, loading=False):


        bubble_layout = MDBoxLayout(
            size_hint_y=None,
            adaptive_height=True,
            padding=(dp(10), dp(8)),
            spacing=dp(10)
        )

        card = MDCard(
            size_hint_x=0.9,
            size_hint_y=None,
            adaptive_height=True,
            padding=dp(15),
            radius=[20,20,5,20] if not is_user else [20,20,20,5],
            md_bg_color=(0.12,0.12,0.12,1) if not is_user else (0.1,0.6,0.3,1),
            elevation=3
        )


        formatted_text = self.format_markdown_for_kivy(text)

        label = MDLabel(
            text=formatted_text,
            markup=True,
            size_hint_y=None,
            halign="left",
            theme_text_color="Custom",
            text_color=(1,1,1,1),
            font_name="NotoTamil",
        )

        label.bind(
            width=lambda instance, value: setattr(instance, "text_size", (value, None))
        )

        label.bind(
            texture_size=lambda instance, value: setattr(instance, "height", value[1])
        )



        card.add_widget(label)

        if is_user:
            bubble_layout.add_widget(MDBoxLayout())  # spacer
            bubble_layout.add_widget(card)
        else:
            bubble_layout.add_widget(card)
            bubble_layout.add_widget(MDBoxLayout())  # spacer

        self.root.ids.chat_list.add_widget(bubble_layout)

        self.root.ids.chat_scroll.scroll_y = 0

        if loading:
            return bubble_layout   # Return loading widget reference


    #SECTION 8
    def format_markdown_for_kivy(self, text):

        # Convert headers
        text = re.sub(
            r"^### (.*)",
            r"\n[b][size=20]\1[/size][/b]\n",
            text,
            flags=re.MULTILINE
        )

        # Convert bold
        text = re.sub(r"\*\*(.*?)\*\*", r"[b]\1[/b]", text)

        # Convert horizontal rules
        text = re.sub(
            r"---",
            "\n[color=#555555]────────────────────────[/color]\n",
            text
        )

        # Convert markdown table rows into bullet style
        lines = text.split("\n")
        new_lines = []

        for line in lines:
            if "|" in line and not line.strip().startswith("---"):
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) > 1:
                    formatted = "\n• " + "  |  ".join(parts)
                    new_lines.append(formatted)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        text = "\n".join(new_lines)

        return text

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
    
    #SECTION 9
    def on_start(self):
        # -------- CROP DATA --------
        self.crop_spacing = {
            "Wheat": (0.20, 0.10),
            "Rice": (0.25, 0.15),
            "Maize": (0.60, 0.25),
            "Tomato": (0.75, 0.45),
            "Potato": (0.60, 0.30),
        }

        crop_items = [
            {
                "text": crop,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=crop: self.set_crop(x),
            }
            for crop in self.crop_spacing.keys()
        ]

        self.crop_menu = MDDropdownMenu(
            caller=self.root.ids.crop_dropdown,
            items=crop_items,
            width_mult=4,
        )

        # -------- SOIL TYPES --------
        self.soil_types = [
            "Sandy",
            "Clay",
            "Loamy",
            "Silty",
            "Peaty"
        ]

        soil_items = [
            {
                "text": soil,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=soil: self.set_soil(x),
            }
            for soil in self.soil_types
        ]

        self.soil_menu = MDDropdownMenu(
            caller=self.root.ids.soil_dropdown,
            items=soil_items,
            width_mult=4,
        )

        # -------- MOISTURE LEVELS --------
        self.moisture_levels = [
            "Low",
            "Moderate",
            "High"
        ]

        moisture_items = [
            {
                "text": level,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=level: self.set_moisture(x),
            }
            for level in self.moisture_levels
        ]

        self.moisture_menu = MDDropdownMenu(
            caller=self.root.ids.moisture_dropdown,
            items=moisture_items,
            width_mult=4,
        )



    #SECTION 10
    def set_crop(self, crop_name):
        self.root.ids.crop_dropdown.text = crop_name
        self.crop_menu.dismiss()


    def set_soil(self, soil_type):
        self.root.ids.soil_dropdown.text = soil_type
        self.soil_menu.dismiss()


    def set_moisture(self, moisture_level):
        self.root.ids.moisture_dropdown.text = moisture_level
        self.moisture_menu.dismiss()

    
    #SECTION 11
    def generate_farm_prompt(self):
        """
        Collect form inputs and convert into simple text prompt
        """

        crop = self.root.ids.crop_dropdown.text
        length = self.root.ids.field_length.text
        width = self.root.ids.field_width.text
        soil = self.root.ids.soil_dropdown.text
        moisture = self.root.ids.moisture_dropdown.text
        ph = self.root.ids.ph_input.text


        prompt = f"""
            Analyze this farm setup:

            Crop: {crop}
            Field Size: {length}m x {width}m
            Soil Type: {soil}
            Moisture Level: {moisture}
            Soil pH: {ph}


            Give recommendations on:
            - Plant density suitability
            - Soil improvement suggestions
            - Fertilizer advice
            - Yield outlook
        """

        return prompt
    

    def generate_farm_prompt_leaf(self):
        """
        Collect form inputs and convert into simple text prompt
        """

        plant = self.plant_1
        leaf_color = "green"
        diseases_affected = self.diseases_1
        humidity = self.humidity
        temperature = self.temperature


        prompt = f"""
            Analyze this plant leaf condition EXACTLY as given. DO NOT HALLUCINATE or invent new diseases, plants, or conditions.

            Plant Type: {self.plant_1 or plant}
            Leaf Color: {leaf_color}
            Disease Affected: {self.diseases_1 or diseases_affected}
            Humidity Level: {humidity}%
            Temperature: {temperature}°C

            Use ONLY the above values. Give analysis strictly on:
            - Disease identification based ONLY on the given disease name
            - Causes of the condition (match the exact disease)
            - Severity level (Low/Medium/High) based ONLY on the given confidence
            - Treatment recommendations (general best practice)
            - Prevention methods

            If the disease is "Healthy" or "Unknown", say the leaf appears healthy and do not invent diseases.
        """

        return prompt
    
    
    
    #SECTION 12
    def run_bot_processing(self):
        prompt = self.generate_farm_prompt()
        
        response = self.chatbot.get_response(prompt, self.chat_history)

        # Format for label display
        formatted_text = response.replace("\n", "\n\n")

        self.root.ids.bot_output.markup = True
        format_text = self.format_markdown_for_kivy(formatted_text)
        self.root.ids.bot_output.text = format_text
        
        self.chat_history.append({
            "role": "user",
            "content": prompt[:1000]  # limit stored length
        })
        self.chat_history.append({
            "role": "assistant",
            "content": response[:1000]  # limit stored length
        })

    def run_bot_processing_leaf(self):
        prompt = self.generate_farm_prompt_leaf()
        
        response = self.chatbot.get_response(prompt, self.chat_history)

        # Format for label display
        formatted_text = response.replace("\n", "\n\n")

        self.root.ids.bot_output.markup = True
        format_text = self.format_markdown_for_kivy(formatted_text)
        self.root.ids.bot_output_leaf.text = format_text
        
        self.chat_history.append({
            "role": "user",
            "content": prompt[:1000]  # limit stored length
        })
        self.chat_history.append({
            "role": "assistant",
            "content": response[:1000]  # limit stored length
        })
  #=========================================================================================

    # -------------------------------
    # Initialize Model
    # -------------------------------
    

    # -------------------------------
    # Open File Chooser (PLYER)
    # -------------------------------
    def open_file_chooser(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        if selection:
            self.selected_image = selection[0]
            self.root.ids.leaf_preview.source = self.selected_image

    # -------------------------------
    # Analyze Image
    # -------------------------------
    
    def init_onnx(self):
        # Class Names (same as before)
        # -------------------------------
        self.class_names = [
            "Pepper__bell___Bacterial_spot",
            "Pepper__bell___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato_Bacterial_spot",
            "Tomato_Early_blight",
            "Tomato_Late_blight",
            "Tomato_Leaf_Mold",
            "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite",
            "Tomato__Target_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus",
            "Tomato__Tomato_mosaic_virus",
            "Tomato_health"
        ]

        # -------------------------------
        # Load ONNX Model
        # -------------------------------
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "model.onnx")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX model not found at: {model_path}")

        # -------------------------------
        # Create ONNX Session
        # -------------------------------
        self.session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"]  # safe default
        )

        # -------------------------------
        # Get Input Name
        # -------------------------------
        self.input_name = self.session.get_inputs()[0].name

        print("✅ ONNX model loaded successfully")


    def preprocess_image(self, image_path):

        # Load image
        image = Image.open(image_path).convert("RGB")

        # Resize to model input size
        image = image.resize((224, 224))

        # Convert to numpy
        img = np.array(image).astype("float32") / 255.0

        # Normalize (VERY IMPORTANT — must match training)
        mean = np.array([0.485, 0.456, 0.406], dtype="float32")
        std = np.array([0.229, 0.224, 0.225], dtype="float32")

        img = (img - mean) / std

        # Change HWC → CHW
        img = np.transpose(img, (2, 0, 1))

        # Add batch dimension
        img = np.expand_dims(img, axis=0)

        return img


    def analyze_leaf(self):

        if not hasattr(self, "session"):
            self.init_onnx()

        if not hasattr(self, "selected_image") or not self.selected_image:
            self.root.ids.result_label.text = self.tr("upload_first")
            return

        threading.Thread(target=self._analyze_leaf_worker, daemon=True).start()


    def _analyze_leaf_worker(self):

    

        try:
            # -------------------------------
            # Safety Checks
            # -------------------------------
            if not hasattr(self, "session"):
                raise RuntimeError("ONNX session not initialized")

            if not self.selected_image:
                raise ValueError("No image selected")

            # -------------------------------
            # Preprocess
            # -------------------------------
            input_image = self.preprocess_image(self.selected_image)

            # Ensure correct dtype
            input_image = input_image.astype(np.float32)

            # -------------------------------
            # ONNX Inference
            # -------------------------------
            outputs = self.session.run(
                None,
                {self.input_name: input_image}
            )

            logits = outputs[0]

            # -------------------------------
            # Stable Softmax (IMPORTANT FIX)
            # -------------------------------
            logits = logits - np.max(logits, axis=1, keepdims=True)
            exp = np.exp(logits)
            probabilities = exp / np.sum(exp, axis=1, keepdims=True)

            predicted = int(np.argmax(probabilities, axis=1)[0])
            confidence = float(probabilities[0][predicted])

            # -------------------------------
            # Label Mapping
            # -------------------------------
            raw_label = self.class_names[predicted]
            confidence_percent = round(confidence * 100, 2)

            # -------------------------------
            # Label Cleaning
            # -------------------------------
            cleaned = (
                raw_label
                .replace("___", " - ")
                .replace("__", " - ")
                .replace("_", " ")
            )

            if " - " in cleaned:
                plant, disease = cleaned.split(" - ", 1)
            else:
                parts = cleaned.split(" ", 1)
                plant = parts[0] if parts else cleaned
                disease = parts[1] if len(parts) > 1 else "Healthy / Unknown"

            # Store exact values for prompt
            self.plant_1 = plant
            self.diseases_1 = disease

            # -------------------------------
            # UI Result
            # -------------------------------
            result_text = (
                f"[b][color=#1bb56b]{self.tr('plant')}:[/color][/b] {plant}\n"
                f"[b][color=#1bb56b]{self.tr('disease')}:[/color][/b] {disease}\n"
                f"[b][color=#1bb56b]{self.tr('confidence')}:[/color][/b] {confidence_percent}%"
            )

            Clock.schedule_once(lambda dt: self.update_result(result_text))

            # -------------------------------
            # Chatbot Integration
            # -------------------------------
            dummy = f"Plant: {plant}\nDisease: {disease}\nConfidence: {confidence_percent}%"

            self.chat_history.append({
                "role": "user",
                "content": dummy
            })

            response = self.chatbot.get_response(dummy, self.chat_history)

            self.chat_history.append({
                "role": "assistant",
                "content": str(response[:1000])
            })

            print("Chatbot Response:\n", response)

        except Exception as e:
            # -------------------------------
            # Proper Error Handling (FIXED)
            # -------------------------------
            traceback.print_exc()

            error_msg = f"Error analyzing image:\n{str(e)}"

            Clock.schedule_once(
                lambda dt: self.update_result(error_msg)
            )


    def update_result(self, text):
        self.root.ids.result_label.markup = True
        self.root.ids.result_label.text = text


    def calculate_profit(self):

        try:
            crop = self.root.ids.profit_crop.text
            area = float(self.root.ids.profit_area.text)
            yield_per_acre = float(self.root.ids.profit_yield.text)
            price = float(self.root.ids.profit_price.text)
            cost = float(self.root.ids.profit_cost.text)

            # tons → kg
            production = yield_per_acre * area * 1000

            revenue = production * price
            profit = revenue - cost

            margin = (profit / revenue) * 100 if revenue != 0 else 0

            result = (
                f"[b]{self.tr('crop_lbl')}:[/b] {crop}\n"
                f"[b]{self.tr('production')}:[/b] {round(production,2)} kg\n"
                f"[b]{self.tr('revenue')}:[/b] ₹{round(revenue,2)}\n"
                f"[b]{self.tr('cost')}:[/b] ₹{round(cost,2)}\n"
                f"[b]{self.tr('profit')}:[/b] ₹{round(profit,2)}\n"
                f"[b]{self.tr('margin')}:[/b] {round(margin,2)}%"
            )

            self.root.ids.profit_result.text = result

        except ValueError:
            self.root.ids.profit_result.text = self.tr("valid_numbers")

        except Exception as e:
            self.root.ids.profit_result.text = f"Error: {str(e)}"



if __name__ == "__main__":
    try:
        AgriApp().run()
    except Exception as e:
        import traceback
        traceback.print_exc()