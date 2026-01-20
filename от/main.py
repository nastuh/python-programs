import tkinter as tk
from tkinter import ttk, messagebox
import random
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
import requests
import os
from tkinter import colorchooser
import json

class SafetyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Инспектор охраны труда - Республика Беларусь")
        self.root.geometry("1600x900")
        
        # Настройки темы
        self.theme = "light"
        self.colors = self.get_theme_colors()
        
        # Статистика игры
        self.game_stats = {
            "rooms_checked": 0,
            "violations_found": 0,
            "total_violations": 24,  # 6 комнат × 4 нарушения = 24
            "hints_used": 0,
            "attempts": 0,
            "score": 0
        }
        
        # Создаем базу всех возможных нарушений
        self.all_violations = self.create_all_violations()
        
        # Создаем комнаты завода с 4 нарушениями в каждой
        self.rooms = self.create_factory_rooms()
        
        # Переменные игры
        self.current_room = None
        self.found_violations = []
        self.selected_violations = []
        self.hints_available = 3
        self.in_room_view = False
        
        # Загружаем изображения
        self.room_images = {}
        self.load_room_images()
        
        # Создаем интерфейс
        self.setup_main_interface()
        
        # Применяем тему
        self.apply_theme()
        
    def get_theme_colors(self):
        """Возвращает цвета для текущей темы"""
        themes = {
            "light": {
                "bg": "#f5f5f5",
                "fg": "#333333",
                "primary": "#2c3e50",
                "secondary": "#34495e",
                "accent": "#3498db",
                "success": "#27ae60",
                "warning": "#f39c12",
                "danger": "#e74c3c",
                "card_bg": "#ffffff",
                "border": "#dddddd",
                "text_muted": "#666666"
            },
            "dark": {
                "bg": "#1a1a1a",
                "fg": "#ffffff",
                "primary": "#3498db",
                "secondary": "#2c3e50",
                "accent": "#9b59b6",
                "success": "#2ecc71",
                "warning": "#f1c40f",
                "danger": "#e74c3c",
                "card_bg": "#2d3436",
                "border": "#444444",
                "text_muted": "#b2bec3"
            },
            "blue": {
                "bg": "#e3f2fd",
                "fg": "#0d47a1",
                "primary": "#1565c0",
                "secondary": "#1976d2",
                "accent": "#2196f3",
                "success": "#4caf50",
                "warning": "#ff9800",
                "danger": "#f44336",
                "card_bg": "#ffffff",
                "border": "#bbdefb",
                "text_muted": "#5c6bc0"
            }
        }
        return themes.get(self.theme, themes["light"])
    
    def create_all_violations(self):
        """Создаем базу всех возможных нарушений"""
        violations = [
            # Правильные нарушения (16 штук - больше, чтобы у каждой комнаты было уникальные)
            {
                "id": "ppe_missing",
                "name": "Отсутствие средств индивидуальной защиты",
                "description": "Работник без каски, защитных очков или спецобуви",
                "regulation": "ТКП 45-1.03-44-2016 п. 5.12",
                "penalty": 5,
                "is_correct": True,
                "image_key": "worker_no_helmet"
            },
            {
                "id": "blocked_exit",
                "name": "Загромождение эвакуационного выхода",
                "description": "Выход заблокирован оборудованием или материалами",
                "regulation": "СТБ 11.13.03-2009 п. 6.2",
                "penalty": 10,
                "is_correct": True,
                "image_key": "blocked_exit"
            },
            {
                "id": "no_grounding",
                "name": "Отсутствие защитного заземления",
                "description": "Электрооборудование не имеет заземления",
                "regulation": "ТКП 181-2009 п. 3.14",
                "penalty": 8,
                "is_correct": True,
                "image_key": "no_grounding"
            },
            {
                "id": "high_storage",
                "name": "Неправильное складирование материалов",
                "description": "Материалы сложены выше допустимой высоты 2 метра",
                "regulation": "ТКП 45-1.03-40-2016 п. 4.15",
                "penalty": 3,
                "is_correct": True,
                "image_key": "high_storage"
            },
            {
                "id": "no_first_aid",
                "name": "Отсутствие аптечки первой помощи",
                "description": "В помещении нет укомплектованной аптечки",
                "regulation": "Постановление Минздрава №113",
                "penalty": 5,
                "is_correct": True,
                "image_key": "no_first_aid"
            },
            {
                "id": "bad_ventilation",
                "name": "Неисправная вентиляционная система",
                "description": "Вентиляция не работает или работает неэффективно",
                "regulation": "ТКП 45-2.02-38-2008 п. 8.3",
                "penalty": 4,
                "is_correct": True,
                "image_key": "bad_ventilation"
            },
            {
                "id": "no_safety_signs",
                "name": "Отсутствие знаков безопасности",
                "description": "Нет обязательных предупреждающих знаков",
                "regulation": "СТБ 1392-2003 п. 5.2",
                "penalty": 2,
                "is_correct": True,
                "image_key": "no_safety_signs"
            },
            {
                "id": "no_machine_guard",
                "name": "Отсутствие ограждения станка",
                "description": "Опасные части оборудования не ограждены",
                "regulation": "ТКП 45-1.03-161-2009 п. 7.3",
                "penalty": 7,
                "is_correct": True,
                "image_key": "no_machine_guard"
            },
            {
                "id": "bad_emergency_light",
                "name": "Неисправное аварийное освещение",
                "description": "Лампы аварийного освещения не горят",
                "regulation": "ТКП 45-2.04-153-2009 п. 5.7",
                "penalty": 4,
                "is_correct": True,
                "image_key": "bad_emergency_light"
            },
            {
                "id": "no_fire_extinguisher",
                "name": "Отсутствие огнетушителя",
                "description": "В помещении нет огнетушителя в доступном месте",
                "regulation": "ТКП 45-2.02-82-2009 п. 9.5",
                "penalty": 5,
                "is_correct": True,
                "image_key": "no_fire_extinguisher"
            },
            {
                "id": "chemicals_open",
                "name": "Неправильное хранение химикатов",
                "description": "Химические вещества хранятся без маркировки",
                "regulation": "ТКП 45-1.03-40-2016 п. 6.8",
                "penalty": 6,
                "is_correct": True,
                "image_key": "chemicals_open"
            },
            {
                "id": "cables_on_floor",
                "name": "Кабели на полу без защиты",
                "description": "Электрические кабели лежат на полу, создавая опасность",
                "regulation": "ТКП 181-2009 п. 4.10",
                "penalty": 4,
                "is_correct": True,
                "image_key": "cables_on_floor"
            },
            {
                "id": "no_safety_glasses",
                "name": "Отсутствие защитных очков",
                "description": "Работник не использует защитные очки при работе",
                "regulation": "ТКП 45-1.03-44-2016 п. 5.14",
                "penalty": 4,
                "is_correct": True,
                "image_key": "no_safety_glasses"
            },
            {
                "id": "spilled_oil",
                "name": "Пролитое масло на полу",
                "description": "На полу есть масляные пятна, создающие опасность поскользнуться",
                "regulation": "ТКП 45-1.03-40-2016 п. 4.8",
                "penalty": 3,
                "is_correct": True,
                "image_key": "spilled_oil"
            },
            {
                "id": "incorrect_fire_exit",
                "name": "Неправильная маркировка пожарного выхода",
                "description": "Знаки пожарного выхода отсутствуют или не соответствуют нормам",
                "regulation": "СТБ 1392-2003 п. 6.3",
                "penalty": 5,
                "is_correct": True,
                "image_key": "incorrect_fire_exit"
            },
            {
                "id": "no_emergency_plan",
                "name": "Отсутствие плана эвакуации",
                "description": "В помещении нет плана эвакуации при пожаре",
                "regulation": "СТБ 11.13.03-2009 п. 7.5",
                "penalty": 6,
                "is_correct": True,
                "image_key": "no_emergency_plan"
            },
            
            # Неправильные нарушения (10 штук)
            {
                "id": "wrong_clock",
                "name": "Неправильно идущие часы",
                "description": "Часы на стене показывают неверное время",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "wrong_clock"
            },
            {
                "id": "messy_desk",
                "name": "Неубранный рабочий стол",
                "description": "На столе разбросаны бумаги и инструменты",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "messy_desk"
            },
            {
                "id": "dirty_windows",
                "name": "Грязные окна",
                "description": "Окна не мыты, на стеклах пыль и разводы",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "dirty_windows"
            },
            {
                "id": "no_curtains",
                "name": "Отсутствие штор",
                "description": "На окнах нет штор или жалюзи",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "no_curtains"
            },
            {
                "id": "wrong_poster",
                "name": "Устаревший информационный стенд",
                "description": "На стенде висит информация прошлого года",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "wrong_poster"
            },
            {
                "id": "broken_pencil",
                "name": "Сломанный карандаш",
                "description": "На столе лежит карандаш без грифеля",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "broken_pencil"
            },
            {
                "id": "uneven_poster",
                "name": "Криво висящий плакат",
                "description": "Плакат по технике безопасности висит неровно",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "uneven_poster"
            },
            {
                "id": "empty_flower",
                "name": "Засохшее растение",
                "description": "Растение в горшке не полито и засохло",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "empty_flower"
            },
            {
                "id": "wrong_chair",
                "name": "Неподходящий стул",
                "description": "Стул не соответствует цвету стола",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "wrong_chair"
            },
            {
                "id": "open_door",
                "name": "Приоткрытая дверь",
                "description": "Дверь в помещение не закрыта до конца",
                "regulation": "Не является нарушением ОТ",
                "penalty": 0,
                "is_correct": False,
                "image_key": "open_door"
            }
        ]
        
        # Перемешиваем нарушения
        random.shuffle(violations)
        return violations
    
    def create_factory_rooms(self):
        """Создаем комнаты завода с 4 правильными нарушениями в каждой"""
        rooms = [
            {
                "name": "ЦЕХ МЕХАНИЧЕСКОЙ ОБРАБОТКИ",
                "id": "workshop",
                "description": "Производственный цех с металлообрабатывающими станками. Рабочие выполняют фрезерные и токарные работы. В цеху установлены 5 токарных станков, 3 фрезерных станка и 2 сверлильных станка.",
                "detailed_description": "В цеху механической обработки металла рабочий работает на токарном станке. Он обрабатывает стальную деталь. Рядом со станком находятся стружка и охлаждающая жидкость. На стене висит инструкция по эксплуатации станка.",
                "correct_violations": ["ppe_missing", "no_machine_guard", "no_grounding", "cables_on_floor"],
                "worker_action": "токарная обработка металлической детали",
                "hazards": "Вращающиеся части станка, металлическая стружка, шум 85 дБ",
                "color": "#FF6B6B",
                "position": (50, 50),
                "size": (380, 250),
                "image_key": "workshop_room"
            },
            {
                "name": "СКЛАД МАТЕРИАЛОВ",
                "id": "warehouse",
                "description": "Складское помещение для хранения металлических заготовок и готовой продукции. Высота потолков 6 метров. Площадь склада 400 м².",
                "detailed_description": "На складе материалов хранятся металлические заготовки и готовая продукция. Складщик использует погрузчик для перемещения паллет. Стеллажи металлические, высотой 5 метров.",
                "correct_violations": ["high_storage", "no_safety_signs", "blocked_exit", "no_fire_extinguisher"],
                "worker_action": "перемещение паллет с помощью погрузчика",
                "hazards": "Падение груза, опрокидывание погрузчика, завал стеллажей",
                "color": "#4ECDC4",
                "position": (460, 50),
                "size": (380, 250),
                "image_key": "warehouse_room"
            },
            {
                "name": "ЭЛЕКТРОЩИТОВАЯ",
                "id": "electrical_room",
                "description": "Помещение с распределительными щитами и электрооборудованием. Температура поддерживается на уровне 18°C. Влажность не более 60%.",
                "detailed_description": "В электрощитовой расположены распределительные щиты. Электрик проверяет показания счетчиков и состояние автоматических выключателей.",
                "correct_violations": ["no_grounding", "no_first_aid", "cables_on_floor", "no_safety_signs"],
                "worker_action": "проверка показаний счетчиков и оборудования",
                "hazards": "Поражение электрическим током, короткое замыкание",
                "color": "#45B7D1",
                "position": (870, 50),
                "size": (380, 250),
                "image_key": "electrical_room"
            },
            {
                "name": "СТОЛОВАЯ",
                "id": "canteen",
                "description": "Помещение для приема пищи работниками. Имеется микроволновая печь, холодильник, кулер с водой, 8 столов на 32 посадочных места.",
                "detailed_description": "В столовой работница разогревает обед в микроволновой печи. На столах расставлены салфетки и приборы. В углу помещения стоит холодильник.",
                "correct_violations": ["no_first_aid", "bad_ventilation", "no_fire_extinguisher", "spilled_oil"],
                "worker_action": "разогрев обеда в микроволновой печи",
                "hazards": "Пожар от электроприборов, пищевое отравление",
                "color": "#FFE66D",
                "position": (50, 330),
                "size": (380, 250),
                "image_key": "canteen_room"
            },
            {
                "name": "СВАРОЧНЫЙ ПОСТ",
                "id": "welding",
                "description": "Участок для сварочных работ. Имеется сварочный аппарат, баллоны с газом, вытяжная система. Площадь поста 20 м².",
                "detailed_description": "Сварщик выполняет сварку металлических конструкций. Используется аппарат для дуговой сварки. Рядом стоят баллоны с газом.",
                "correct_violations": ["ppe_missing", "no_fire_extinguisher", "chemicals_open", "no_safety_glasses"],
                "worker_action": "дуговая сварка металлических конструкций",
                "hazards": "Ультрафиолетовое излучение, искры, отравление газами",
                "color": "#95E1D3",
                "position": (460, 330),
                "size": (380, 250),
                "image_key": "welding_room"
            },
            {
                "name": "КОРИДОР И ЭВАКУАЦИОННЫЕ ПУТИ",
                "id": "corridor",
                "description": "Основные проходы между цехами и эвакуационные пути. Ширина проходов 2.5 метра. Длина коридора 40 метров.",
                "detailed_description": "В главном коридоре завода работник переносит коробки с документами. Вдоль стены стоят ящики с оборудованием.",
                "correct_violations": ["blocked_exit", "bad_emergency_light", "incorrect_fire_exit", "no_emergency_plan"],
                "worker_action": "перенос коробок с документами",
                "hazards": "Затрудненная эвакуация, падение в темноте",
                "color": "#F38181",
                "position": (870, 330),
                "size": (380, 250),
                "image_key": "corridor_room"
            }
        ]
        return rooms
    
    def load_room_images(self):
        """Загружаем изображения для комнат - ВСТАВЬТЕ СВОИ КАРТИНКИ ЗДЕСЬ!"""
        try:
            # Для каждой комнаты загружаем изображение
            image_paths = {
                "workshop": "workshop_image.jpg",      # Изображение для цеха
                "warehouse": "warehouse_image.jpg",    # Изображение для склада
                "electrical_room": "electrical_image.jpg",  # Изображение для электрощитовой
                "canteen": "canteen_image.jpg",        # Изображение для столовой
                "welding": "welding_image.jpg",        # Изображение для сварочного поста
                "corridor": "corridor_image.jpg"       # Изображение для коридора
            }
            
            for room_id, image_path in image_paths.items():
                try:
                    # Пробуем загрузить ваше изображение
                    if os.path.exists(image_path):
                        img = Image.open(image_path)
                        img = img.resize((800, 500), Image.Resampling.LANCZOS)
                    else:
                        # Если файл не найден, создаем временное изображение
                        img = self.create_temp_room_image(room_id)
                except:
                    # Если ошибка, создаем временное изображение
                    img = self.create_temp_room_image(room_id)
                
                photo = ImageTk.PhotoImage(img)
                self.room_images[room_id] = photo
                
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем временные изображения для всех комнат
            for room in self.rooms:
                img = self.create_temp_room_image(room["id"])
                photo = ImageTk.PhotoImage(img)
                self.room_images[room["id"]] = photo
    
    def create_temp_room_image(self, room_id):
        """Создаем временное изображение для комнаты (используется если нет ваших картинок)"""
        img = Image.new('RGB', (800, 500), '#3a506b')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        
        # Находим название комнаты
        room_name = ""
        for room in self.rooms:
            if room["id"] == room_id:
                room_name = room["name"]
                break
        
        draw.rectangle([0, 0, 800, 50], fill="#333333")
        draw.text((400, 25), room_name, fill='white', font=font, anchor='mm')
        draw.text((400, 200), "ВАШЕ ИЗОБРАЖЕНИЕ", fill='white', font=font, anchor='mm')
        draw.text((400, 250), "Разместите файл в папке с программой:", fill='white', font=ImageFont.load_default(), anchor='mm')
        
        if room_id == "workshop":
            draw.text((400, 300), "workshop_image.jpg", fill='yellow', font=ImageFont.load_default(), anchor='mm')
        elif room_id == "warehouse":
            draw.text((400, 300), "warehouse_image.jpg", fill='yellow', font=ImageFont.load_default(), anchor='mm')
        elif room_id == "electrical_room":
            draw.text((400, 300), "electrical_image.jpg", fill='yellow', font=ImageFont.load_default(), anchor='mm')
        elif room_id == "canteen":
            draw.text((400, 300), "canteen_image.jpg", fill='yellow', font=ImageFont.load_default(), anchor='mm')
        elif room_id == "welding":
            draw.text((400, 300), "welding_image.jpg", fill='yellow', font=ImageFont.load_default(), anchor='mm')
        elif room_id == "corridor":
            draw.text((400, 300), "corridor_image.jpg", fill='yellow', font=ImageFont.load_default(), anchor='mm')
        
        return img



    def setup_main_interface(self):
        """Настраиваем основной интерфейс"""
        # Создаем стилизованную верхнюю панель
        self.setup_top_panel()
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая часть - карта завода
        left_frame = tk.Frame(main_container, bg=self.colors["bg"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Правая часть - паспорт и управление
        right_frame = tk.Frame(main_container, bg=self.colors["bg"], width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_frame.pack_propagate(False)
        
        # Настраиваем карту
        self.setup_factory_map(left_frame)
        
        # Настраиваем паспорт объекта
        self.setup_passport_panel(right_frame)
        
        # Настраиваем панель управления
        self.setup_control_panel(right_frame)
        
        # Обновляем статистику
        self.update_stats_display()
    
    def setup_top_panel(self):
        """Настраиваем верхнюю панель"""
        top_panel = tk.Frame(self.root, bg=self.colors["primary"], height=70)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        # Логотип и название
        logo_frame = tk.Frame(top_panel, bg=self.colors["primary"])
        logo_frame.pack(side=tk.LEFT, padx=20)
        
        logo_label = tk.Label(logo_frame, 
                             text="🏭", 
                             font=("Arial", 24),
                             bg=self.colors["primary"], 
                             fg="white")
        logo_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(logo_frame,
                              text="ИНСПЕКТОР ОХРАНЫ ТРУДА",
                              font=("Arial", 18, "bold"),
                              bg=self.colors["primary"],
                              fg="white")
        title_label.pack(side=tk.LEFT, padx=10)
        
        subtitle_label = tk.Label(logo_frame,
                                 text="Республика Беларусь",
                                 font=("Arial", 12),
                                 bg=self.colors["primary"],
                                 fg="white")
        subtitle_label.pack(side=tk.LEFT)
        
        # Панель управления темой и статистикой
        control_frame = tk.Frame(top_panel, bg=self.colors["primary"])
        control_frame.pack(side=tk.RIGHT, padx=20)
        
        # Выбор темы
        theme_label = tk.Label(control_frame,
                              text="Тема:",
                              font=("Arial", 10),
                              bg=self.colors["primary"],
                              fg="white")
        theme_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.theme_var = tk.StringVar(value="light")
        theme_menu = ttk.Combobox(control_frame,
                                 textvariable=self.theme_var,
                                 values=["light", "dark", "blue"],
                                 state="readonly",
                                 width=10)
        theme_menu.pack(side=tk.LEFT, padx=(0, 15))
        theme_menu.bind("<<ComboboxSelected>>", self.change_theme)
        
        # Статистика
        stats_frame = tk.Frame(control_frame, bg=self.colors["primary"])
        stats_frame.pack(side=tk.LEFT)
        
        self.hints_label = tk.Label(stats_frame,
                                   text=f"💡 Подсказки: {self.hints_available}",
                                   font=("Arial", 10, "bold"),
                                   bg=self.colors["primary"],
                                   fg="white")
        self.hints_label.pack()
        
        self.score_label = tk.Label(stats_frame,
                                   text="🏆 Счет: 0",
                                   font=("Arial", 10),
                                   bg=self.colors["primary"],
                                   fg="white")
        self.score_label.pack()
    
    def setup_factory_map(self, parent):
        """Настраиваем карту завода"""
        # Заголовок карты
        map_header = tk.Frame(parent, bg=self.colors["card_bg"], 
                             relief=tk.RAISED, bd=1)
        map_header.pack(fill=tk.X, pady=(0, 10))
        
        map_title = tk.Label(map_header,
                            text="🗺️ КАРТА ПРОИЗВОДСТВЕННОГО ОБЪЕКТА",
                            font=("Arial", 14, "bold"),
                            bg=self.colors["card_bg"],
                            fg=self.colors["primary"],
                            pady=10)
        map_title.pack()
        
        # Контейнер для карты с прокруткой
        map_container = tk.Frame(parent, bg=self.colors["card_bg"],
                                relief=tk.SUNKEN, bd=2)
        map_container.pack(fill=tk.BOTH, expand=True)
        
        # Холст для карты
        self.canvas = tk.Canvas(map_container,
                               bg=self.colors["card_bg"],
                               highlightthickness=0)
        
        # Полосы прокрутки
        v_scrollbar = ttk.Scrollbar(map_container, orient=tk.VERTICAL, 
                                   command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(map_container, orient=tk.HORIZONTAL,
                                   command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set,
                             xscrollcommand=h_scrollbar.set)
        
        # Размещение элементов
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Рисуем карту
        self.draw_factory_map()
        
        # Инструкция
        instruction = tk.Label(parent,
                              text="🔍 Кликните на комнату для детального осмотра и поиска нарушений",
                              font=("Arial", 11),
                              bg=self.colors["bg"],
                              fg=self.colors["text_muted"],
                              pady=10)
        instruction.pack()
    
    def draw_factory_map(self):
        """Рисуем карту завода с комнатами"""
        # Очищаем холст
        self.canvas.delete("all")
        
        # Устанавливаем область прокрутки
        self.canvas.config(scrollregion=(0, 0, 1300, 700))
        
        # Фон
        self.canvas.create_rectangle(0, 0, 1300, 700,
                                    fill=self.colors["card_bg"],
                                    outline="")
        
        # Контур здания
        self.canvas.create_rectangle(50, 50, 1250, 650,
                                    width=3,
                                    outline=self.colors["primary"],
                                    fill=self.colors["bg"])
        
        # Заголовок
        self.canvas.create_text(650, 30,
                               text="ОАО 'Минский машиностроительный завод' - План 1 этажа",
                               font=("Arial", 14, "bold"),
                               fill=self.colors["primary"])
        
        # Рисуем комнаты
        self.room_buttons = {}
        
        for room in self.rooms:
            x, y = room["position"]
            width, height = room["size"]
            
            # Определяем статус комнаты
            found_count = len([v for v in room["correct_violations"]
                             if (room["id"], v) in self.found_violations])
            total_count = len(room["correct_violations"])
            
            # Цвет комнаты в зависимости от статуса проверки
            if found_count == total_count:
                room_color = self.colors["success"]
            elif found_count > 0:
                room_color = self.colors["warning"]
            else:
                room_color = room["color"]
            
            # Прямоугольник комнаты
            rect_id = self.canvas.create_rectangle(x, y, x+width, y+height,
                                                  fill=room_color,
                                                  width=2,
                                                  outline=self.colors["primary"],
                                                  tags=("room", room["id"]))
            
            # Название комнаты
            self.canvas.create_text(x+width//2, y+30,
                                   text=room["name"],
                                   font=("Arial", 11, "bold"),
                                   fill='white',
                                   width=width-40)
            
            # Действие работника
            self.canvas.create_text(x+width//2, y+height-40,
                                   text=f"👷 {room['worker_action']}",
                                   font=("Arial", 9),
                                   fill='white',
                                   width=width-40)
            
            # Прогресс проверки
            progress_text = f"Найдено: {found_count}/{total_count}"
            self.canvas.create_text(x+width//2, y+height-20,
                                   text=progress_text,
                                   font=("Arial", 9, "bold"),
                                   fill='white')
            
            # Делаем комнату кликабельной
            self.canvas.tag_bind(rect_id, '<Button-1>',
                                lambda e, r=room: self.show_room_detail(r))
            self.canvas.tag_bind(rect_id, '<Enter>',
                                lambda e, rid=rect_id: self.highlight_room(rid, True))
            self.canvas.tag_bind(rect_id, '<Leave>',
                                lambda e, rid=rect_id: self.highlight_room(rid, False))
        
        # Легенда
        self.draw_legend()
    
    def draw_legend(self):
        """Рисуем легенду на карте"""
        legend_x, legend_y = 50, 660
        
        # Фон легенды
        self.canvas.create_rectangle(legend_x, legend_y,
                                    legend_x+400, legend_y+80,
                                    fill=self.colors["card_bg"],
                                    outline=self.colors["border"],
                                    width=1)
        
        # Заголовок легенды
        self.canvas.create_text(legend_x+200, legend_y+15,
                               text="📋 Легенда:",
                               font=("Arial", 11, "bold"),
                               fill=self.colors["primary"])
        
        # Элементы легенды
        items = [
            (self.colors["success"], "✓ Проверено полностью"),
            (self.colors["warning"], "⚠ Частично проверено"),
            ("#FF6B6B", "Не проверено")
        ]
        
        for i, (color, text) in enumerate(items):
            y_pos = legend_y + 35 + i*20
            
            # Квадратик цвета
            self.canvas.create_rectangle(legend_x+10, y_pos-7,
                                        legend_x+25, y_pos+7,
                                        fill=color,
                                        outline=self.colors["border"])
            
            # Текст
            self.canvas.create_text(legend_x+40, y_pos,
                                   text=text,
                                   font=("Arial", 9),
                                   fill=self.colors["fg"],
                                   anchor='w')
    
    def highlight_room(self, rect_id, highlight):
        """Подсвечиваем комнату при наведении"""
        if highlight:
            self.canvas.itemconfig(rect_id, width=4)
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.itemconfig(rect_id, width=2)
            self.canvas.config(cursor="")
    
    def setup_passport_panel(self, parent):
        """Настраиваем панель паспорта объекта"""
        # Контейнер паспорта
        passport_frame = tk.Frame(parent, bg=self.colors["card_bg"],
                                 relief=tk.RAISED, bd=2)
        passport_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Заголовок
        passport_header = tk.Frame(passport_frame, bg=self.colors["primary"])
        passport_header.pack(fill=tk.X)
        
        passport_title = tk.Label(passport_header,
                                 text="📄 ПАСПОРТ ОБЪЕКТА",
                                 font=("Arial", 14, "bold"),
                                 bg=self.colors["primary"],
                                 fg="white",
                                 pady=10)
        passport_title.pack()
        
        # Содержимое паспорта
        content_frame = tk.Frame(passport_frame, bg=self.colors["card_bg"],
                                padx=15, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Информация об объекте - выравнивание с использованием grid
        info_frame = tk.Frame(content_frame, bg=self.colors["card_bg"])
        info_frame.pack(fill=tk.X)
        
        info_items = [
            ("🏢 Организация:", "ОАО 'Минский машиностроительный завод'"),
            ("📍 Адрес:", "г. Минск, ул. Заводская, 15"),
            ("👨‍💼 Руководитель:", "Ген. директор Раевская А.А."),
            ("🛡️ Ответственный по ОТ:", "Гл. инженер Филановичи Д. и Я."),
            ("📅 Год постройки:", "1978 (ремонт 2019)"),
            ("📐 Общая площадь:", "12 500 м²"),
            ("👥 Численность:", "245 сотрудников"),
            ("🔄 Режим работы:", "2 смены, 5/2")
        ]
        
        # Используем grid для точного выравнивания
        for i, (title, value) in enumerate(info_items):
            title_label = tk.Label(info_frame,
                                  text=title,
                                  font=("Arial", 10, "bold"),
                                  bg=self.colors["card_bg"],
                                  fg=self.colors["primary"],
                                  width=25,
                                  anchor='w')
            title_label.grid(row=i, column=0, sticky='w', padx=(0, 10), pady=2)
            
            value_label = tk.Label(info_frame,
                                  text=value,
                                  font=("Arial", 10),
                                  bg=self.colors["card_bg"],
                                  fg=self.colors["fg"],
                                  anchor='w')
            value_label.grid(row=i, column=1, sticky='w', pady=2)
        
        # Настраиваем равномерное распределение колонок
        info_frame.columnconfigure(0, weight=0)
        info_frame.columnconfigure(1, weight=1)
        
        # Разделитель
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Статистика проверки
        stats_frame = tk.Frame(content_frame, bg=self.colors["bg"],
                              relief=tk.GROOVE, bd=1, padx=10, pady=10)
        stats_frame.pack(fill=tk.X)
        
        stats_title = tk.Label(stats_frame,
                              text="📊 СТАТИСТИКА ПРОВЕРКИ",
                              font=("Arial", 12, "bold"),
                              bg=self.colors["bg"],
                              fg=self.colors["primary"])
        stats_title.pack()
        
        self.stats_display = tk.Label(stats_frame,
                                     font=("Arial", 10),
                                     bg=self.colors["bg"],
                                     fg=self.colors["fg"],
                                     justify=tk.LEFT)
        self.stats_display.pack(pady=5)
        
        # Прогресс-бар
        self.progress_bar = ttk.Progressbar(stats_frame,
                                          length=300,
                                          mode='determinate')
        self.progress_bar.pack(pady=10)
    
    def setup_control_panel(self, parent):
        """Настраиваем панель управления"""
        control_frame = tk.Frame(parent, bg=self.colors["card_bg"],
                                relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.BOTH)
        
        # Заголовок
        control_header = tk.Frame(control_frame, bg=self.colors["secondary"])
        control_header.pack(fill=tk.X)
        
        control_title = tk.Label(control_header,
                                text="⚙️ УПРАВЛЕНИЕ ПРОВЕРКОЙ",
                                font=("Arial", 14, "bold"),
                                bg=self.colors["secondary"],
                                fg="white",
                                pady=10)
        control_title.pack()
        
        # Кнопки управления
        button_frame = tk.Frame(control_frame, bg=self.colors["card_bg"],
                               padx=20, pady=20)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка помощи
        help_btn = tk.Button(button_frame,
                            text="📋 ИНСТРУКЦИЯ",
                            command=self.show_help,
                            font=("Arial", 11, "bold"),
                            bg=self.colors["accent"],
                            fg="white",
                            relief=tk.RAISED,
                            padx=30,
                            pady=10,
                            cursor="hand2")
        help_btn.pack(fill=tk.X, pady=5)
        
        # Кнопка новой игры
        new_game_btn = tk.Button(button_frame,
                                text="🔄 НОВАЯ ПРОВЕРКА",
                                command=self.reset_game,
                                font=("Arial", 11),
                                bg=self.colors["warning"],
                                fg="white",
                                relief=tk.RAISED,
                                padx=30,
                                pady=8,
                                cursor="hand2")
        new_game_btn.pack(fill=tk.X, pady=5)
        
        # Кнопка завершения
        finish_btn = tk.Button(button_frame,
                              text="🏁 ЗАВЕРШИТЬ ПРОВЕРКУ",
                              command=self.finish_game,
                              font=("Arial", 11, "bold"),
                              bg=self.colors["success"],
                              fg="white",
                              relief=tk.RAISED,
                              padx=30,
                              pady=10,
                              cursor="hand2")
        finish_btn.pack(fill=tk.X, pady=5)
        
        # Разделитель
        ttk.Separator(button_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Нормативные документы
        docs_label = tk.Label(button_frame,
                             text="📚 Нормативные документы РБ:",
                             font=("Arial", 11, "bold"),
                             bg=self.colors["card_bg"],
                             fg=self.colors["primary"])
        docs_label.pack(anchor='w', pady=(0, 5))
        
        docs_list = [
            "• ТКП 45-1.03-44-2016 (СИЗ)",
            "• ТКП 181-2009 (Электробезопасность)",
            "• СТБ 11.13.03-2009 (Пожарная безопасность)",
            "• ТКП 45-1.03-40-2016 (Хранение материалов)",
            "• Постановление Минздрава №113"
        ]
        
        for doc in docs_list:
            doc_label = tk.Label(button_frame,
                                text=doc,
                                font=("Arial", 9),
                                bg=self.colors["card_bg"],
                                fg=self.colors["fg"],
                                justify=tk.LEFT,
                                anchor='w')
            doc_label.pack(anchor='w', padx=10)
    
    def show_room_detail(self, room):
        """Показываем детальный вид комнаты"""
        self.current_room = room
        
        # Скрываем основной интерфейс
        for widget in self.root.pack_slaves():
            widget.pack_forget()
        
        # Создаем интерфейс детального просмотра
        self.create_room_detail_interface(room)
    
    def create_room_detail_interface(self, room):
        """Создаем интерфейс детального просмотра комнаты"""
        # Основной фрейм
        self.room_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.room_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель
        top_panel = tk.Frame(self.room_frame, bg=self.colors["primary"], height=80)
        top_panel.pack(fill=tk.X)
        top_panel.pack_propagate(False)
        
        # Кнопка возврата
        back_btn = tk.Button(top_panel,
                            text="← ВЕРНУТЬСЯ К КАРТЕ",
                            command=self.return_to_map,
                            font=("Arial", 12, "bold"),
                            bg=self.colors["accent"],
                            fg="white",
                            relief=tk.RAISED,
                            padx=20,
                            pady=5,
                            cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Название комнаты
        room_title = tk.Label(top_panel,
                             text=f"🔍 {room['name']}",
                             font=("Arial", 16, "bold"),
                             bg=self.colors["primary"],
                             fg="white")
        room_title.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Кнопка подсказки
        if self.hints_available > 0:
            hint_btn = tk.Button(top_panel,
                                text=f"💡 ПОДСКАЗКА ({self.hints_available})",
                                command=self.use_hint,
                                font=("Arial", 11),
                                bg=self.colors["warning"],
                                fg="white",
                                relief=tk.RAISED,
                                padx=15,
                                pady=5,
                                cursor="hand2")
            hint_btn.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Основное содержимое
        content_frame = tk.Frame(self.room_frame, bg=self.colors["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая часть - изображение и описание
        left_frame = tk.Frame(content_frame, bg=self.colors["bg"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Изображение комнаты
        image_frame = tk.Frame(left_frame, bg=self.colors["card_bg"],
                              relief=tk.RAISED, bd=2)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        if room["id"] in self.room_images:
            image_label = tk.Label(image_frame,
                                  image=self.room_images[room["id"]],
                                  bg=self.colors["card_bg"])
            image_label.pack(padx=10, pady=10)
        
        # Описание комнаты
        desc_frame = tk.Frame(left_frame, bg=self.colors["card_bg"],
                             relief=tk.RAISED, bd=2)
        desc_frame.pack(fill=tk.BOTH)
        
        desc_title = tk.Label(desc_frame,
                             text="📋 ОПИСАНИЕ РАБОЧЕГО ПРОЦЕССА:",
                             font=("Arial", 12, "bold"),
                             bg=self.colors["card_bg"],
                             fg=self.colors["primary"],
                             pady=10)
        desc_title.pack()
        
        desc_text = tk.Label(desc_frame,
                            text=room["detailed_description"],
                            font=("Arial", 11),
                            bg=self.colors["card_bg"],
                            fg=self.colors["fg"],
                            wraplength=600,
                            justify=tk.LEFT,
                            padx=20,
                            pady=10)
        desc_text.pack()
        
        # Правая часть - выбор нарушений
        right_frame = tk.Frame(content_frame, bg=self.colors["bg"], width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_frame.pack_propagate(False)
        
        # Создаем основной контейнер с прокруткой
        main_container = tk.Frame(right_frame, bg=self.colors["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Контейнер для выбора нарушений с прокруткой
        violations_container = tk.Frame(main_container, bg=self.colors["card_bg"])
        violations_container.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        violations_title = tk.Label(violations_container,
                                   text="🔎 ВЫБЕРИТЕ НАЙДЕННЫЕ НАРУШЕНИЯ:",
                                   font=("Arial", 14, "bold"),
                                   bg=self.colors["primary"],
                                   fg="white",
                                   pady=15)
        violations_title.pack(fill=tk.X)
        
        # Информация о необходимом количестве
        info_label = tk.Label(violations_container,
                             text=f"В этой комнате нужно найти {len(room['correct_violations'])} нарушения",
                             font=("Arial", 11),
                             bg=self.colors["card_bg"],
                             fg=self.colors["primary"],
                             pady=10)
        info_label.pack()
        
        # Фрейм для списка нарушений
        violations_list_frame = tk.Frame(violations_container, bg=self.colors["card_bg"])
        violations_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Полоса прокрутки
        scrollbar = tk.Scrollbar(violations_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas для плавной прокрутки
        violations_canvas = tk.Canvas(violations_list_frame,
                                     bg=self.colors["card_bg"],
                                     yscrollcommand=scrollbar.set,
                                     highlightthickness=0)
        violations_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=violations_canvas.yview)
        
        # Внутренний фрейм для нарушений
        inner_frame = tk.Frame(violations_canvas, bg=self.colors["card_bg"])
        violations_canvas.create_window((0, 0), window=inner_frame, anchor='nw', width=440)
        
        # Создаем кнопки нарушений
        self.create_violation_buttons(room, inner_frame)
        
        # Обновляем размер прокрутки
        inner_frame.update_idletasks()
        violations_canvas.config(scrollregion=violations_canvas.bbox("all"))
        
        # Фрейм для кнопки проверки (внизу)
        check_frame = tk.Frame(violations_container, bg=self.colors["card_bg"],
                              pady=20)
        check_frame.pack(fill=tk.X, padx=20, side=tk.BOTTOM)
        
        check_btn = tk.Button(check_frame,
                             text="✅ ПРОВЕРИТЬ ВЫБОР",
                             command=lambda: self.check_violations(room),
                             font=("Arial", 12, "bold"),
                             bg="#27ae60",  # Зеленый цвет
                             fg="white",
                             relief=tk.RAISED,
                             padx=40,
                             pady=12,
                             cursor="hand2")
        check_btn.pack(fill=tk.X)
    
    def create_violation_buttons(self, room, parent_frame):
        """Создаем кнопки для выбора нарушений"""
        # Очищаем предыдущие кнопки
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Выбираем 8 случайных нарушений для этой комнаты (4 правильных + 4 неправильных)
        correct_violations = [v for v in self.all_violations
                             if v["id"] in room["correct_violations"]]
        
        # Добавляем неправильные нарушения
        wrong_violations = [v for v in self.all_violations
                           if v["id"] not in room["correct_violations"]
                           and not v["is_correct"]]
        wrong_violations = random.sample(wrong_violations, 4)  # Теперь 4 неправильных
        
        # Смешиваем нарушения
        all_violations = correct_violations + wrong_violations
        random.shuffle(all_violations)
        
        # Создаем переменные для хранения выбора
        self.violation_vars = {}
        
        for violation in all_violations:
            # Создаем фрейм для каждого нарушения
            violation_frame = tk.Frame(parent_frame,
                                      bg=self.colors["card_bg"],
                                      relief=tk.GROOVE,
                                      bd=1)
            violation_frame.pack(fill=tk.X, pady=5)
            
            # Переменная для чекбокса
            var = tk.BooleanVar(value=False)
            self.violation_vars[violation["id"]] = var
            
            # Чекбокс
            cb = tk.Checkbutton(violation_frame,
                               text="",
                               variable=var,
                               bg=self.colors["card_bg"],
                               activebackground=self.colors["card_bg"],
                               cursor="hand2")
            cb.pack(side=tk.LEFT, padx=10)
            
            # Информация о нарушении
            info_frame = tk.Frame(violation_frame, bg=self.colors["card_bg"])
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Название нарушения
            name_label = tk.Label(info_frame,
                                 text=violation["name"],
                                 font=("Arial", 10, "bold"),
                                 bg=self.colors["card_bg"],
                                 fg=self.colors["primary"],
                                 anchor='w',
                                 cursor="hand2")
            name_label.pack(fill=tk.X)
            name_label.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
            
            # Описание
            desc_label = tk.Label(info_frame,
                                 text=violation["description"],
                                 font=("Arial", 9),
                                 bg=self.colors["card_bg"],
                                 fg=self.colors["fg"],
                                 anchor='w',
                                 cursor="hand2")
            desc_label.pack(fill=tk.X)
            desc_label.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
            
            # Нормативный документ
            reg_label = tk.Label(info_frame,
                                text=violation["regulation"],
                                font=("Arial", 8),
                                bg=self.colors["card_bg"],
                                fg=self.colors["text_muted"],
                                anchor='w',
                                cursor="hand2")
            reg_label.pack(fill=tk.X)
            reg_label.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
            
            # Делаем весь фрейм кликабельным
            violation_frame.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
            violation_frame.config(cursor="hand2")
    
    def check_violations(self, room):
        """Проверяем выбранные нарушения"""
        # Собираем выбранные нарушения
        selected_ids = [vid for vid, var in self.violation_vars.items() if var.get()]
        
        if not selected_ids:
            messagebox.showwarning("Внимание", "Выберите хотя бы одно нарушение!")
            return
        
        # Проверяем правильность выбора
        correct_selected = 0
        wrong_selected = 0
        newly_found = []
        
        for violation_id in selected_ids:
            violation = next((v for v in self.all_violations if v["id"] == violation_id), None)
            if not violation:
                continue
            
            violation_key = (room["id"], violation_id)
            
            if violation["is_correct"] and violation_id in room["correct_violations"]:
                if violation_key not in self.found_violations:
                    self.found_violations.append(violation_key)
                    newly_found.append(violation["name"])
                    correct_selected += 1
                    self.game_stats["score"] += violation["penalty"]
            else:
                wrong_selected += 1
        
        # Увеличиваем счетчик попыток
        self.game_stats["attempts"] += 1
        
        # Формируем сообщение с результатом
        result_text = f"📊 РЕЗУЛЬТАТ ПРОВЕРКИ:\n\n"
        result_text += f"✅ Правильно выбрано: {correct_selected}\n"
        result_text += f"❌ Неправильно выбрано: {wrong_selected}\n"
        
        total_in_room = len(room["correct_violations"])
        found_in_room = len([v for v in room["correct_violations"] 
                           if (room["id"], v) in self.found_violations])
        
        result_text += f"🎯 Найдено в комнате: {found_in_room}/{total_in_room}\n\n"
        
        if newly_found:
            result_text += "✨ НОВЫЕ НАЙДЕННЫЕ НАРУШЕНИЯ:\n"
            for violation in newly_found:
                result_text += f"• {violation}\n"
        
        if found_in_room == total_in_room:
            result_text += f"\n🎉 ВСЕ НАРУШЕНИЯ В КОМНАТЕ НАЙДЕНЫ!\n"
            self.game_stats["rooms_checked"] += 1
        
        # Показываем результат
        messagebox.showinfo("Результат проверки", result_text)
        
        # Обновляем статистику
        self.update_stats_display()
        
        # Если все нарушения найдены, предлагаем вернуться к карте
        if found_in_room == total_in_room:
            if messagebox.askyesno("Проверка завершена", 
                                  "Хотите вернуться к карте завода?"):
                self.return_to_map()
    
    def use_hint(self):
        """Используем подсказку"""
        if self.hints_available <= 0:
            messagebox.showinfo("Нет подсказок", "У вас закончились подсказки!")
            return
        
        if not self.current_room:
            messagebox.showwarning("Ошибка", "Сначала выберите комнату!")
            return
        
        # Уменьшаем количество подсказок
        self.hints_available -= 1
        self.hints_label.config(text=f"💡 Подсказки: {self.hints_available}")
        
        # Показываем подсказку - одно из правильных нарушений
        remaining_violations = [v for v in self.current_room["correct_violations"]
                              if (self.current_room["id"], v) not in self.found_violations]
        
        if remaining_violations:
            # Выбираем случайное нарушение для подсказки
            hint_violation_id = random.choice(remaining_violations)
            hint_violation = next(v for v in self.all_violations 
                                 if v["id"] == hint_violation_id)
            
            # Показываем подсказку
            hint_text = f"💡 ПОДСКАЗКА:\n\n"
            hint_text += f"Одно из нарушений в этой комнате:\n"
            hint_text += f"• {hint_violation['name']}\n"
            hint_text += f"• {hint_violation['description']}\n\n"
            hint_text += f"Норма: {hint_violation['regulation']}"
            
            messagebox.showinfo("Подсказка", hint_text)
        else:
            messagebox.showinfo("Подсказка", "Все нарушения в этой комнате уже найдены!")
    
    def return_to_map(self):
        """Возвращаемся к карте завода"""
        # Удаляем интерфейс просмотра комнаты
        if hasattr(self, 'room_frame'):
            self.room_frame.destroy()
        
        # Восстанавливаем основной интерфейс
        self.setup_main_interface()
        
        # Обновляем статистику
        self.update_stats_display()
    
    def update_stats_display(self):
        """Обновляем отображение статистики"""
        # Обновляем общую статистику
        total_found = len(self.found_violations)
        progress = (total_found / self.game_stats["total_violations"] * 100) if self.game_stats["total_violations"] > 0 else 0
        
        stats_text = f"\n".join([
            f"🔍 Проверено комнат: {self.game_stats['rooms_checked']}/{len(self.rooms)}",
            f"⚠️ Всего нарушений: {self.game_stats['total_violations']}",
            f"✅ Найдено нарушений: {total_found}",
            f"📈 Прогресс: {progress:.1f}%",
            f"🎯 Эффективность: {(total_found / max(self.game_stats['attempts'], 1) * 100):.1f}%"
        ])
        
        if hasattr(self, 'stats_display'):
            self.stats_display.config(text=stats_text)
            self.progress_bar['value'] = progress
        
        # Обновляем верхнюю панель
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"🏆 Счет: {self.game_stats['score']}")
        
        if hasattr(self, 'hints_label'):
            self.hints_label.config(text=f"💡 Подсказки: {self.hints_available}")
    
    def change_theme(self, event=None):
        """Меняем тему оформления"""
        self.theme = self.theme_var.get()
        self.colors = self.get_theme_colors()
        self.apply_theme()
    
    def apply_theme(self):
        """Применяем выбранную тему ко всем виджетам"""
        try:
            # Обновляем цвета корневого окна
            self.root.config(bg=self.colors["bg"])
            
            # Рекурсивно обновляем все виджеты
            self.update_widget_colors(self.root)
            
            # Перерисовываем карту
            if hasattr(self, 'canvas'):
                self.draw_factory_map()
        except Exception as e:
            print(f"Ошибка применения темы: {e}")
    
    def update_widget_colors(self, widget):
        """Рекурсивно обновляем цвета виджетов"""
        try:
            # Получаем тип виджета
            widget_type = str(widget.winfo_class())
            
            # Обновляем цвета в зависимости от типа виджета
            if widget_type in ("Frame", "Labelframe", "TFrame"):
                widget.config(bg=self.colors["bg"])
            elif widget_type == "Label":
                if 'primary' in str(widget.cget("text")).lower() or '🛡️' in str(widget.cget("text")):
                    widget.config(bg=self.colors["primary"], fg="white")
                elif 'success' in str(widget.cget("bg")):
                    widget.config(bg=self.colors["success"])
                elif 'warning' in str(widget.cget("bg")):
                    widget.config(bg=self.colors["warning"])
                elif 'danger' in str(widget.cget("bg")):
                    widget.config(bg=self.colors["danger"])
                else:
                    widget.config(bg=self.colors["card_bg"], fg=self.colors["fg"])
            elif widget_type == "Button":
                # Сохраняем оригинальный цвет кнопки
                text = widget.cget("text")
                if "ПОДСКАЗКА" in text:
                    widget.config(bg=self.colors["warning"], fg="white")
                elif "ВЕРНУТЬСЯ" in text:
                    widget.config(bg=self.colors["accent"], fg="white")
                elif "ПРОВЕРИТЬ" in text:
                    widget.config(bg=self.colors["success"], fg="white")
                elif "НОВАЯ" in text:
                    widget.config(bg=self.colors["warning"], fg="white")
                elif "ЗАВЕРШИТЬ" in text:
                    widget.config(bg=self.colors["success"], fg="white")
                else:
                    widget.config(bg=self.colors["accent"], fg="white")
            elif widget_type == "Canvas":
                widget.config(bg=self.colors["card_bg"])
            elif widget_type == "Checkbutton":
                widget.config(bg=self.colors["card_bg"], 
                            activebackground=self.colors["card_bg"],
                            fg=self.colors["fg"])
            
            # Рекурсивно обновляем дочерние виджеты
            for child in widget.winfo_children():
                self.update_widget_colors(child)
                
        except Exception as e:
            # Пропускаем ошибки для специфичных виджетов
            pass
    
    def show_help(self):
        """Показываем справку по игре"""
        help_text = """🎮 ИНСТРУКЦИЯ ПО ИГРЕ "ИНСПЕКТОР ОХРАНЫ ТРУДА"

🎯 ЦЕЛЬ ИГРЫ:
Найти ВСЕ нарушения правил охраны труда на территории завода
в соответствии с законодательством Республики Беларусь.

🔍 КАК ИГРАТЬ:
1. Изучите карту завода в основном окне
2. Кликните на любую комнату для детального осмотра
3. Изучите изображение и описание комнаты
4. В правой панели выберите РЕАЛЬНЫЕ нарушения (4 на комнату)
5. Нажмите "ПРОВЕРИТЬ ВЫБОР" для проверки
6. Используйте подсказки 💡 если нужно
7. Вернитесь к карте и проверьте другие комнаты

🎮 ОСОБЕННОСТИ ИГРЫ:
• 3 темы оформления (светлая, темная, синяя)
• 6 комнат с уникальными нарушениями
• 4 реальных нарушения в каждой комнате (всего 24)
• 3 подсказки на всю игру
• Система подсчета очков и эффективности

📋 ПРАВИЛА:
• В каждой комнате нужно найти ВСЕ 4 реальных нарушения
• За неправильный выбор очки не снимаются
• Используйте подсказки экономно
• Чем меньше попыток - тем выше эффективность

🛡️ НАРУШЕНИЯ ОХРАНЫ ТРУДА:
Основаны на реальных нормативных документах РБ:
• ТКП 45-1.03-44-2016 (СИЗ)
• ТКП 181-2009 (Электробезопасность)
• СТБ 11.13.03-2009 (Пожарная безопасность)
• И другие нормативные акты

🏆 ОЦЕНКА РЕЗУЛЬТАТА:
• Найдено 100% нарушений - Отлично!
• Найдено 80-99% - Хорошо
• Найдено 60-79% - Удовлетворительно
• Менее 60% - Требуется обучение

УДАЧИ В ПРОВЕРКЕ! 🏭🛡️"""

        messagebox.showinfo("Инструкция по игре", help_text)
    
    def reset_game(self):
        """Начинаем новую игру"""
        if messagebox.askyesno("Новая игра", "Начать новую проверку?\nТекущий прогресс будет сброшен."):
            # Сбрасываем статистику
            self.found_violations = []
            self.selected_violations = []
            self.hints_available = 3
            self.game_stats = {
                "rooms_checked": 0,
                "violations_found": 0,
                "total_violations": 24,  # 6 комнат × 4 нарушения
                "hints_used": 0,
                "attempts": 0,
                "score": 0
            }
            
            # Перемешиваем нарушения
            random.shuffle(self.all_violations)
            
            # Возвращаемся к карте если нужно
            if hasattr(self, 'room_frame'):
                self.return_to_map()
            else:
                # Обновляем интерфейс
                self.update_stats_display()
                if hasattr(self, 'canvas'):
                    self.draw_factory_map()
            
            messagebox.showinfo("Новая игра", "Новая проверка начата! Удачи!")
    
    def finish_game(self):
        """Завершаем игру и показываем результаты"""
        total_found = len(self.found_violations)
        total_needed = self.game_stats["total_violations"]
        percentage = (total_found / total_needed * 100) if total_needed > 0 else 0
        
        efficiency = (total_found / max(self.game_stats["attempts"], 1) * 100)
        
        result_text = f"🏁 ПРОВЕРКА ЗАВЕРШЕНА! 🏁\n\n"
        result_text += f"📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:\n"
        result_text += f"✅ Найдено нарушений: {total_found}/{total_needed}\n"
        result_text += f"🔍 Проверено комнат: {self.game_stats['rooms_checked']}/{len(self.rooms)}\n"
        result_text += f"🎯 Всего попыток: {self.game_stats['attempts']}\n"
        result_text += f"💡 Использовано подсказок: {3 - self.hints_available}\n"
        result_text += f"🏆 Итоговый счет: {self.game_stats['score']}\n"
        result_text += f"📈 Эффективность: {efficiency:.1f}%\n\n"
        
        # Оценка результата
        if percentage >= 90:
            result_text += "🎖️ ОТЛИЧНО! Вы - профессиональный инспектор!\n"
            result_text += "Рекомендуем Вас на должность главного инспектора по ОТ."
        elif percentage >= 70:
            result_text += "👍 ХОРОШО! Вы грамотный специалист.\n"
            result_text += "Рекомендуется пройти курсы повышения квалификации."
        elif percentage >= 50:
            result_text += "⚠️ УДОВЛЕТВОРИТЕЛЬНО. Требуется дополнительное обучение.\n"
            result_text += "Рекомендуем изучить нормативные документы РБ."
        else:
            result_text += "❌ НЕУДОВЛЕТВОРИТЕЛЬНО. Требуется переподготовка.\n"
            result_text += "Обязательно пройдите обучение по охране труда."
        
        result_text += "\n\n🎓 РЕКОМЕНДАЦИИ:\n"
        result_text += "• Пройти обучение в УО 'РИИТ'\n"
        result_text += "• Изучить СТБ 11.13.03-2009\n"
        result_text += "• Пройти аттестацию по электробезопасности"
        
        messagebox.showinfo("Игра завершена!", result_text)
        
        # Предлагаем начать новую игру
        if messagebox.askyesno("Новая игра", "Хотите начать новую проверку?"):
            self.reset_game()

def main():
    root = tk.Tk()
    
    # Настраиваем иконку и заголовок
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    # Создаем стили для ttk виджетов
    style = ttk.Style()
    style.theme_use('clam')
    
    # Настраиваем прогресс-бар
    style.configure("TProgressbar",
                   thickness=20,
                   troughcolor='#e0e0e0',
                   background='#4CAF50',
                   bordercolor='#cccccc',
                   lightcolor='#4CAF50',
                   darkcolor='#388E3C')
    
    style.configure("TCombobox",
                   fieldbackground='white',
                   background='white',
                   arrowcolor='#333333')
    
    # Запускаем игру
    app = SafetyGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()