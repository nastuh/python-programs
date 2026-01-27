import asyncio
import logging
import pickle
import os
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import random
from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter, TelegramAPIError

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "your_token"  # Замените на ваш токен

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Папка для сохранения данных
SAVE_DIR = Path("game_data")
SAVE_DIR.mkdir(exist_ok=True)

# ========== ОСНОВНЫЕ ПЕРЕЧИСЛЕНИЯ ==========

class Biome(Enum):
    FOREST = "🌲 Лес"
    MOUNTAINS = "⛰️ Горы"
    PLAINS = "🌾 Равнины"
    RIVER = "🌊 Река"
    VILLAGE = "🏘️ Деревня"
    BEACH = "🏖️ Пляж"
    CAVE = "🕳️ Пещера"

class Resource(Enum):
    WOOD = "🪵 Дерево"
    STONE = "🪨 Камень"
    IRON = "⚙️ Железо"
    GOLD = "💰 Золото"
    FOOD = "🍎 Еда"
    WATER = "💧 Вода"
    HERBS = "🌿 Травы"

class BuildingType(Enum):
    HOUSE = "🏠 Дом"
    WORKSHOP = "⚒️ Мастерская"
    FARM = "🌽 Ферма"
    STORAGE = "📦 Склад"
    DEFENSE = "🛡️ Укрепления"

class MonsterType(Enum):
    GOBLIN = "👺 Гоблин"
    WOLF = "🐺 Волк"
    ORC = "👹 Орк"
    DRAGON = "🐲 Дракон"
    SLIME = "🫧 Слизень"
    SKELETON = "💀 Скелет"

class WeaponType(Enum):
    FIST = "👊 Кулаки"
    SWORD = "⚔️ Меч"
    AXE = "🪓 Топор"
    BOW = "🏹 Лук"
    STAFF = "🪄 Посох"
    DAGGER = "🗡️ Кинжал"

class QuestType(Enum):
    KILL = "⚔️ Убить монстров"
    GATHER = "📦 Собрать ресурсы"
    DELIVER = "📨 Доставить предмет"
    EXPLORE = "🗺️ Исследовать"
    CRAFT = "🔨 Скрафтить"

class ItemRarity(Enum):
    COMMON = "Обычный"
    UNCOMMON = "Необычный"
    RARE = "Редкий"
    EPIC = "Эпический"
    LEGENDARY = "Легендарный"

class Season(Enum):
    SPRING = "🌱 Весна"
    SUMMER = "☀️ Лето"
    AUTUMN = "🍂 Осень"
    WINTER = "❄️ Зима"

# ========== ОСНОВНЫЕ МОДЕЛИ ДАННЫХ ==========

@dataclass
class Position:
    x: int
    y: int
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def distance_to(self, other: 'Position') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def to_dict(self):
        return {"x": self.x, "y": self.y}
    
    @classmethod
    def from_dict(cls, data):
        return cls(x=data["x"], y=data["y"])

@dataclass
class Building:
    type: BuildingType
    position: Position
    level: int = 1
    health: int = 100
    
    def to_dict(self):
        return {
            "type": self.type.name,
            "position": self.position.to_dict(),
            "level": self.level,
            "health": self.health
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            type=BuildingType[data["type"]],
            position=Position.from_dict(data["position"]),
            level=data["level"],
            health=data["health"]
        )

@dataclass
class Weapon:
    type: WeaponType
    damage: Tuple[int, int]
    speed: float
    rarity: ItemRarity
    level_requirement: int = 1
    gold_cost: int = 0
    
    def calculate_damage(self, player_level: int) -> int:
        base_damage = random.randint(self.damage[0], self.damage[1])
        multiplier = 1 + (player_level - self.level_requirement) * 0.1
        return int(base_damage * multiplier)
    
    def to_dict(self):
        return {
            "type": self.type.name,
            "damage": self.damage,
            "speed": self.speed,
            "rarity": self.rarity.name,
            "level_requirement": self.level_requirement,
            "gold_cost": self.gold_cost
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            type=WeaponType[data["type"]],
            damage=tuple(data["damage"]),
            speed=data["speed"],
            rarity=ItemRarity[data["rarity"]],
            level_requirement=data["level_requirement"],
            gold_cost=data["gold_cost"]
        )

@dataclass
class Monster:
    type: MonsterType
    health: int
    damage: Tuple[int, int]
    gold_reward: int
    exp_reward: int
    level: int
    drop_items: List[Tuple[str, float]] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "type": self.type.name,
            "health": self.health,
            "damage": self.damage,
            "gold_reward": self.gold_reward,
            "exp_reward": self.exp_reward,
            "level": self.level,
            "drop_items": self.drop_items
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            type=MonsterType[data["type"]],
            health=data["health"],
            damage=tuple(data["damage"]),
            gold_reward=data["gold_reward"],
            exp_reward=data["exp_reward"],
            level=data["level"],
            drop_items=[tuple(item) for item in data.get("drop_items", [])]
        )

@dataclass
class Quest:
    quest_id: str
    quest_type: QuestType
    title: str
    description: str
    requirements: Dict[str, int]
    rewards: Dict[str, int]
    level_requirement: int
    time_limit: Optional[int] = None
    
    def to_dict(self):
        return {
            "quest_id": self.quest_id,
            "quest_type": self.quest_type.name,
            "title": self.title,
            "description": self.description,
            "requirements": self.requirements,
            "rewards": self.rewards,
            "level_requirement": self.level_requirement,
            "time_limit": self.time_limit
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            quest_id=data["quest_id"],
            quest_type=QuestType[data["quest_type"]],
            title=data["title"],
            description=data["description"],
            requirements=data["requirements"],
            rewards=data["rewards"],
            level_requirement=data["level_requirement"],
            time_limit=data.get("time_limit")
        )

@dataclass
class Clan:
    clan_id: str
    name: str
    leader_id: int
    members: List[int] = field(default_factory=list)
    level: int = 1
    experience: int = 0
    treasury: Dict[Resource, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            "clan_id": self.clan_id,
            "name": self.name,
            "leader_id": self.leader_id,
            "members": self.members,
            "level": self.level,
            "experience": self.experience,
            "treasury": {k.name: v for k, v in self.treasury.items()},
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        clan = cls(
            clan_id=data["clan_id"],
            name=data["name"],
            leader_id=data["leader_id"],
            members=data["members"],
            level=data["level"],
            experience=data["experience"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
        clan.treasury = {Resource[k]: v for k, v in data.get("treasury", {}).items()}
        return clan

@dataclass
class TradeOffer:
    offer_id: str
    seller_id: int
    item_type: str
    item_amount: int
    price_gold: int
    price_resources: Dict[Resource, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    expires_in: int = 24
    
    def to_dict(self):
        return {
            "offer_id": self.offer_id,
            "seller_id": self.seller_id,
            "item_type": self.item_type,
            "item_amount": self.item_amount,
            "price_gold": self.price_gold,
            "price_resources": {k.name: v for k, v in self.price_resources.items()},
            "created_at": self.created_at.isoformat(),
            "expires_in": self.expires_in
        }
    
    @classmethod
    def from_dict(cls, data):
        offer = cls(
            offer_id=data["offer_id"],
            seller_id=data["seller_id"],
            item_type=data["item_type"],
            item_amount=data["item_amount"],
            price_gold=data["price_gold"],
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_in=data["expires_in"]
        )
        offer.price_resources = {Resource[k]: v for k, v in data.get("price_resources", {}).items()}
        return offer

@dataclass
class CraftRecipe:
    recipe_id: str
    result_item: str
    result_amount: int
    ingredients: Dict[str, int]
    required_level: int = 1
    required_building: Optional[BuildingType] = None
    
    def to_dict(self):
        return {
            "recipe_id": self.recipe_id,
            "result_item": self.result_item,
            "result_amount": self.result_amount,
            "ingredients": self.ingredients,
            "required_level": self.required_level,
            "required_building": self.required_building.name if self.required_building else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            recipe_id=data["recipe_id"],
            result_item=data["result_item"],
            result_amount=data["result_amount"],
            ingredients=data["ingredients"],
            required_level=data["required_level"],
            required_building=BuildingType[data["required_building"]] if data.get("required_building") else None
        )

@dataclass
class ChatMessage:
    player_id: int
    username: str
    message: str
    timestamp: datetime
    
    def to_dict(self):
        return {
            "player_id": self.player_id,
            "username": self.username,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            player_id=data["player_id"],
            username=data["username"],
            message=data["message"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )

# ========== ИГРОК ==========

@dataclass
class Player:
    user_id: int
    username: str
    position: Position
    health: int = 100
    max_health: int = 100
    energy: int = 100
    max_energy: int = 100
    level: int = 1
    experience: int = 0
    gold: int = 30
    resources: Dict[Resource, int] = field(default_factory=lambda: {
        Resource.WOOD: 20,
        Resource.STONE: 15,
        Resource.FOOD: 30,
        Resource.WATER: 20,
        Resource.IRON: 5,
        Resource.GOLD: 10,
        Resource.HERBS: 10
    })
    buildings: List[Building] = field(default_factory=list)
    equipment: Dict[str, Any] = field(default_factory=lambda: {
        "weapon": Weapon(WeaponType.FIST, (5, 10), 1.0, ItemRarity.COMMON),
        "armor": None,
        "accessory": None
    })
    active_quests: List[Quest] = field(default_factory=list)
    completed_quests: List[str] = field(default_factory=list)
    kills: Dict[MonsterType, int] = field(default_factory=dict)
    clan_id: Optional[str] = None
    inventory: Dict[str, int] = field(default_factory=lambda: {
        "health_potion": 3,
        "energy_potion": 2
    })
    last_action_time: datetime = field(default_factory=datetime.now)
    chat_muted: bool = False
    
    def add_experience(self, amount: int):
        self.experience += amount
        if self.experience >= self.level * 100:
            self.level += 1
            self.experience = 0
            self.max_health += 20
            self.max_energy += 10
            self.health = self.max_health
            self.energy = self.max_energy
            return True
        return False
    
    def get_total_damage(self) -> Tuple[int, int]:
        weapon = self.equipment.get("weapon")
        if weapon and isinstance(weapon, Weapon):
            base_min, base_max = weapon.damage
            level_bonus = self.level * 0.5
            return (int(base_min + level_bonus), int(base_max + level_bonus))
        return (5, 10)
    
    def calculate_gathering_bonus(self) -> float:
        weapon = self.equipment.get("weapon")
        base_bonus = 1.0
        
        if weapon:
            weapon_bonuses = {
                WeaponType.FIST: 1.0,
                WeaponType.SWORD: 1.2,
                WeaponType.AXE: 1.5,
                WeaponType.BOW: 1.1,
                WeaponType.STAFF: 1.3,
                WeaponType.DAGGER: 1.0
            }
            base_bonus = weapon_bonuses.get(weapon.type, 1.0)
        
        level_bonus = 1 + (self.level - 1) * 0.05
        return base_bonus * level_bonus
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "position": self.position.to_dict(),
            "health": self.health,
            "max_health": self.max_health,
            "energy": self.energy,
            "max_energy": self.max_energy,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "resources": {k.name: v for k, v in self.resources.items()},
            "buildings": [b.to_dict() for b in self.buildings],
            "equipment": {
                "weapon": self.equipment["weapon"].to_dict() if self.equipment.get("weapon") else None,
                "armor": None,
                "accessory": None
            },
            "active_quests": [q.to_dict() for q in self.active_quests],
            "completed_quests": self.completed_quests,
            "kills": {k.name: v for k, v in self.kills.items()},
            "clan_id": self.clan_id,
            "inventory": self.inventory,
            "last_action_time": self.last_action_time.isoformat(),
            "chat_muted": self.chat_muted
        }
    
    @classmethod
    def from_dict(cls, data):
        player = cls(
            user_id=data["user_id"],
            username=data["username"],
            position=Position.from_dict(data["position"]),
            health=data["health"],
            max_health=data["max_health"],
            energy=data["energy"],
            max_energy=data["max_energy"],
            level=data["level"],
            experience=data["experience"],
            gold=data["gold"],
            completed_quests=data["completed_quests"],
            clan_id=data.get("clan_id"),
            inventory=data["inventory"],
            last_action_time=datetime.fromisoformat(data["last_action_time"]),
            chat_muted=data.get("chat_muted", False)
        )
        
        player.resources = {Resource[k]: v for k, v in data["resources"].items()}
        player.buildings = [Building.from_dict(b) for b in data["buildings"]]
        player.active_quests = [Quest.from_dict(q) for q in data["active_quests"]]
        player.kills = {MonsterType[k]: v for k, v in data.get("kills", {}).items()}
        
        equipment_data = data.get("equipment", {})
        if equipment_data.get("weapon"):
            player.equipment["weapon"] = Weapon.from_dict(equipment_data["weapon"])
        
        return player

# ========== БАЗОВЫЙ ИГРОВОЙ МИР ==========

class GameWorld:
    def __init__(self, size: int = 50):
        self.size = size
        self.players: Dict[int, Player] = {}
        self.buildings: List[Building] = []
        self.chat_messages: List[ChatMessage] = []
        self.world_map: Dict[Tuple[int, int], Biome] = {}
        self.generate_world()
    
    def generate_world(self):
        for x in range(-self.size, self.size + 1):
            for y in range(-self.size, self.size + 1):
                value = random.random()
                distance = (x**2 + y**2)**0.5
                
                if distance < 5:
                    self.world_map[(x, y)] = Biome.VILLAGE
                elif value < 0.3:
                    self.world_map[(x, y)] = Biome.FOREST
                elif value < 0.5:
                    self.world_map[(x, y)] = Biome.PLAINS
                elif value < 0.65:
                    self.world_map[(x, y)] = Biome.MOUNTAINS
                elif value < 0.75:
                    self.world_map[(x, y)] = Biome.RIVER
                elif value < 0.85:
                    self.world_map[(x, y)] = Biome.BEACH
                else:
                    self.world_map[(x, y)] = Biome.CAVE
    
    def get_biome(self, position: Position) -> Biome:
        return self.world_map.get((position.x, position.y), Biome.PLAINS)
    
    def get_resources_in_biome(self, biome: Biome) -> List[Resource]:
        resources = {
            Biome.FOREST: [Resource.WOOD, Resource.HERBS, Resource.FOOD],
            Biome.MOUNTAINS: [Resource.STONE, Resource.IRON, Resource.GOLD],
            Biome.PLAINS: [Resource.FOOD, Resource.HERBS],
            Biome.RIVER: [Resource.WATER, Resource.FOOD],
            Biome.VILLAGE: [Resource.FOOD, Resource.WATER],
            Biome.BEACH: [Resource.WOOD, Resource.WATER],
            Biome.CAVE: [Resource.STONE, Resource.IRON, Resource.GOLD]
        }
        return resources.get(biome, [Resource.FOOD])
    
    def get_players_in_area(self, position: Position, radius: int = 5) -> List[Player]:
        return [p for p in self.players.values() 
                if p.position.distance_to(position) <= radius]
    
    def save_to_file(self, filename: str = "game_world.json"):
        """Сохраняет состояние мира в файл"""
        try:
            data = {
                "size": self.size,
                "players": {str(k): v.to_dict() for k, v in self.players.items()},
                "buildings": [b.to_dict() for b in self.buildings],
                "chat_messages": [msg.to_dict() for msg in self.chat_messages],
                "world_map": {f"{x},{y}": biome.name for (x, y), biome in self.world_map.items()}
            }
            
            save_path = SAVE_DIR / filename
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Мир сохранен в {save_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении мира: {e}")
            return False
    
    def load_from_file(self, filename: str = "game_world.json"):
        """Загружает состояние мира из файла"""
        try:
            save_path = SAVE_DIR / filename
            if not save_path.exists():
                logger.info("Файл сохранения не найден, создаем новый мир")
                return False
            
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.size = data["size"]
            
            # Загружаем игроков
            self.players = {}
            for user_id_str, player_data in data["players"].items():
                player = Player.from_dict(player_data)
                self.players[player.user_id] = player
            
            # Загружаем постройки
            self.buildings = [Building.from_dict(b) for b in data["buildings"]]
            
            # Загружаем сообщения чата
            self.chat_messages = [ChatMessage.from_dict(msg) for msg in data["chat_messages"]]
            
            # Загружаем карту
            self.world_map = {}
            for coord_str, biome_name in data["world_map"].items():
                x_str, y_str = coord_str.split(",")
                self.world_map[(int(x_str), int(y_str))] = Biome[biome_name]
            
            logger.info(f"Мир загружен из {save_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при загрузке мира: {e}")
            return False

# ========== РАСШИРЕННЫЙ ИГРОВОЙ МИР ==========

class EnhancedGameWorld(GameWorld):
    def __init__(self, size: int = 50):
        super().__init__(size)
        self.monsters: Dict[Tuple[int, int], Monster] = {}
        self.quests: Dict[str, Quest] = {}
        self.clans: Dict[str, Clan] = {}
        self.trade_offers: Dict[str, TradeOffer] = {}
        self.craft_recipes: Dict[str, CraftRecipe] = {}
        self.current_season: Season = Season.SPRING
        self.season_start: datetime = datetime.now()
        self.combat_states: Dict[int, Dict] = {}  # Состояния боев
        self.initialize_monsters()
        self.initialize_quests()
        self.initialize_crafting()
        self.load_from_file("enhanced_world.json")
    
    def save_to_file(self, filename: str = "enhanced_world.json"):
        """Сохраняет состояние расширенного мира"""
        try:
            data = {
                "size": self.size,
                "players": {str(k): v.to_dict() for k, v in self.players.items()},
                "buildings": [b.to_dict() for b in self.buildings],
                "chat_messages": [msg.to_dict() for msg in self.chat_messages],
                "world_map": {f"{x},{y}": biome.name for (x, y), biome in self.world_map.items()},
                "monsters": {f"{x},{y}": monster.to_dict() for (x, y), monster in self.monsters.items()},
                "quests": {k: v.to_dict() for k, v in self.quests.items()},
                "clans": {k: v.to_dict() for k, v in self.clans.items()},
                "trade_offers": {k: v.to_dict() for k, v in self.trade_offers.items()},
                "craft_recipes": {k: v.to_dict() for k, v in self.craft_recipes.items()},
                "current_season": self.current_season.name,
                "season_start": self.season_start.isoformat(),
                "combat_states": self.combat_states  # Временные данные, не сохраняем
            }
            
            save_path = SAVE_DIR / filename
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Расширенный мир сохранен в {save_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении расширенного мира: {e}")
            return False
    
    def load_from_file(self, filename: str = "enhanced_world.json"):
        """Загружает состояние расширенного мира"""
        try:
            save_path = SAVE_DIR / filename
            if not save_path.exists():
                logger.info("Файл сохранения не найден, создаем новый расширенный мир")
                self.initialize_monsters()
                self.initialize_quests()
                self.initialize_crafting()
                return False
            
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Загружаем базовые данные
            super().load_from_file("game_world.json")
            
            # Загружаем монстров
            self.monsters = {}
            for coord_str, monster_data in data.get("monsters", {}).items():
                x_str, y_str = coord_str.split(",")
                self.monsters[(int(x_str), int(y_str))] = Monster.from_dict(monster_data)
            
            # Загружаем квесты
            self.quests = {k: Quest.from_dict(v) for k, v in data.get("quests", {}).items()}
            
            # Загружаем кланы
            self.clans = {k: Clan.from_dict(v) for k, v in data.get("clans", {}).items()}
            
            # Загружаем торговые предложения
            self.trade_offers = {k: TradeOffer.from_dict(v) for k, v in data.get("trade_offers", {}).items()}
            
            # Загружаем рецепты крафта
            self.craft_recipes = {k: CraftRecipe.from_dict(v) for k, v in data.get("craft_recipes", {}).items()}
            
            # Загружаем сезон
            self.current_season = Season[data.get("current_season", "SPRING")]
            self.season_start = datetime.fromisoformat(data.get("season_start", datetime.now().isoformat()))
            
            logger.info(f"Расширенный мир загружен из {save_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при загрузке расширенного мира: {e}")
            self.initialize_monsters()
            self.initialize_quests()
            self.initialize_crafting()
            return False
    
    def initialize_monsters(self):
        monster_definitions = [
            (MonsterType.GOBLIN, (20, 30), (5, 10), 15, 20, 1),
            (MonsterType.WOLF, (30, 40), (8, 15), 20, 30, 2),
            (MonsterType.SLIME, (15, 25), (3, 8), 10, 15, 1),
            (MonsterType.SKELETON, (40, 60), (10, 20), 30, 40, 3),
            (MonsterType.ORC, (60, 80), (15, 25), 50, 60, 4),
            (MonsterType.DRAGON, (150, 200), (30, 50), 200, 300, 10),
        ]
        
        for _ in range(100):
            monster_def = random.choice(monster_definitions)
            x = random.randint(-self.size, self.size)
            y = random.randint(-self.size, self.size)
            
            self.monsters[(x, y)] = Monster(
                type=monster_def[0],
                health=random.randint(monster_def[1][0], monster_def[1][1]),
                damage=monster_def[2],
                gold_reward=monster_def[3],
                exp_reward=monster_def[4],
                level=monster_def[5]
            )
    
    def initialize_quests(self):
        self.quests = {
            "first_kill": Quest(
                quest_id="first_kill",
                quest_type=QuestType.KILL,
                title="Первая кровь",
                description="Убейте 5 гоблинов",
                requirements={"goblin_kills": 5},
                rewards={"gold": 100, "experience": 50},
                level_requirement=1
            ),
            "lumberjack": Quest(
                quest_id="lumberjack",
                quest_type=QuestType.GATHER,
                title="Дровосек",
                description="Соберите 50 дерева",
                requirements={"wood_gathered": 50},
                rewards={"gold": 80, "wood": 20},
                level_requirement=2
            ),
            "dragon_slayer": Quest(
                quest_id="dragon_slayer",
                quest_type=QuestType.KILL,
                title="Убийца драконов",
                description="Убейте 1 дракона",
                requirements={"dragon_kills": 1},
                rewards={"gold": 500, "experience": 300, "dragon_scale": 1},
                level_requirement=8
            ),
            "blacksmith": Quest(
                quest_id="blacksmith",
                quest_type=QuestType.CRAFT,
                title="Кузнец",
                description="Скрафтите меч",
                requirements={"craft_sword": 1},
                rewards={"gold": 150, "iron_sword": 1},
                level_requirement=3
            ),
        }
    
    def initialize_crafting(self):
        self.craft_recipes = {
            "wooden_sword": CraftRecipe(
                recipe_id="wooden_sword",
                result_item="wooden_sword",
                result_amount=1,
                ingredients={"wood": 20, "stone": 5},
                required_level=2,
                required_building=BuildingType.WORKSHOP
            ),
            "iron_sword": CraftRecipe(
                recipe_id="iron_sword",
                result_item="iron_sword",
                result_amount=1,
                ingredients={"iron": 15, "wood": 10, "stone": 5},
                required_level=5,
                required_building=BuildingType.WORKSHOP
            ),
            "health_potion": CraftRecipe(
                recipe_id="health_potion",
                result_item="health_potion",
                result_amount=3,
                ingredients={"herbs": 5, "water": 2},
                required_level=3
            ),
            "stone_axe": CraftRecipe(
                recipe_id="stone_axe",
                result_item="stone_axe",
                result_amount=1,
                ingredients={"stone": 10, "wood": 5},
                required_level=2
            ),
            "gold_ring": CraftRecipe(
                recipe_id="gold_ring",
                result_item="gold_ring",
                result_amount=1,
                ingredients={"gold": 5, "stone": 2},
                required_level=4,
                required_building=BuildingType.WORKSHOP
            ),
        }
    
    def get_monsters_in_area(self, position: Position, radius: int = 3) -> List[Tuple[Position, Monster]]:
        nearby = []
        for (x, y), monster in self.monsters.items():
            monster_pos = Position(x, y)
            if monster_pos.distance_to(position) <= radius:
                nearby.append((monster_pos, monster))
        return nearby
    
    def get_seasonal_bonus(self) -> Dict[str, float]:
        bonuses = {
            Season.SPRING: {"gathering": 1.2, "healing": 1.1, "experience": 1.05},
            Season.SUMMER: {"gathering": 1.1, "damage": 1.1, "energy_regen": 1.2},
            Season.AUTUMN: {"gathering": 1.3, "gold": 1.25, "crafting": 1.1},
            Season.WINTER: {"combat": 1.15, "defense": 1.2, "mining": 0.9},
        }
        return bonuses.get(self.current_season, {})
    
    def update_season(self):
        now = datetime.now()
        if now - self.season_start > timedelta(hours=24):
            seasons = list(Season)
            current_index = seasons.index(self.current_season)
            self.current_season = seasons[(current_index + 1) % len(seasons)]
            self.season_start = now
            
            for player in self.players.values():
                try:
                    asyncio.create_task(self.send_season_notification(player.user_id))
                except:
                    pass
    
    async def send_season_notification(self, user_id: int):
        try:
            season_bonus = self.get_seasonal_bonus()
            bonus_text = "\n".join([f"• {k}: x{v}" for k, v in season_bonus.items()])
            
            await safe_send_message(
                user_id,
                f"🎭 СМЕНА СЕЗОНА!\n"
                f"Новый сезон: {self.current_season.value}\n\n"
                f"🌡️ Активные бонусы:\n{bonus_text}\n\n"
                f"Используйте бонусы по максимуму!"
            )
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления о сезоне: {e}")

# Инициализация расширенного мира
world = EnhancedGameWorld()

# ========== УТИЛИТЫ ДЛЯ БЕЗОПАСНОЙ ОТПРАВКИ ==========

async def safe_send_message(chat_id: int, text: str, reply_markup=None, parse_mode=None):
    """Безопасная отправка сообщения с обработкой исключений"""
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        return True
    except TelegramBadRequest as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return False
    except TelegramRetryAfter as e:
        logger.warning(f"Превышен лимит, повтор через {e.retry_after} сек.")
        await asyncio.sleep(e.retry_after)
        return await safe_send_message(chat_id, text, reply_markup, parse_mode)
    except TelegramAPIError as e:
        logger.error(f"API ошибка Telegram: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при отправке сообщения: {e}")
        return False

async def safe_edit_message(chat_id: int, message_id: int, text: str, reply_markup=None, parse_mode=None):
    """Безопасное редактирование сообщения"""
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        return True
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            # Сообщение не изменилось, это нормально
            return True
        logger.error(f"Ошибка редактирования сообщения: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при редактировании сообщения: {e}")
        return False

# ========== КЛАВИАТУРЫ ==========

def get_main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🗺️ Карта", callback_data="map"),
        InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory"),
        InlineKeyboardButton(text="🏠 Постройки", callback_data="buildings"),
    )
    keyboard.row(
        InlineKeyboardButton(text="⚔️ Бой", callback_data="combat_menu"),
        InlineKeyboardButton(text="🛒 Торговля", callback_data="shop"),
    )
    keyboard.row(
        InlineKeyboardButton(text="📜 Квесты", callback_data="quests_menu"),
        InlineKeyboardButton(text="👑 Кланы", callback_data="clan_menu"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🔨 Крафт", callback_data="craft_menu"),
        InlineKeyboardButton(text="💬 Чат", callback_data="chat_menu"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🚶‍♂️ Движение", callback_data="move_menu"),
        InlineKeyboardButton(text="⚒️ Добывать", callback_data="gather"),
        InlineKeyboardButton(text="ℹ️ Статус", callback_data="status"),
    )
    return keyboard.as_markup()

def get_chat_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💬 Глобальный чат", callback_data="global_chat"),
        InlineKeyboardButton(text="📨 Локальный чат", callback_data="local_chat"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🔇 Выкл. чат", callback_data="mute_chat"),
        InlineKeyboardButton(text="🔊 Вкл. чат", callback_data="unmute_chat"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

def get_movement_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="⬆️ Север", callback_data="move_north"),
        InlineKeyboardButton(text="⬇️ Юг", callback_data="move_south"),
    )
    keyboard.row(
        InlineKeyboardButton(text="⬅️ Запад", callback_data="move_west"),
        InlineKeyboardButton(text="➡️ Восток", callback_data="move_east"),
    )
    keyboard.row(
        InlineKeyboardButton(text="📍 Телепорт", callback_data="teleport"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

def get_combat_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="⚔️ Атаковать", callback_data="combat_attack"),
        InlineKeyboardButton(text="🛡️ Защита", callback_data="combat_defend"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🧪 Исп. зелье", callback_data="combat_potion"),
        InlineKeyboardButton(text="🏃 Сбежать", callback_data="combat_flee"),
    )
    return keyboard.as_markup()

def get_shop_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🛒 Купить", callback_data="shop_buy"),
        InlineKeyboardButton(text="💰 Продать", callback_data="shop_sell"),
    )
    keyboard.row(
        InlineKeyboardButton(text="⚔️ Оружие", callback_data="shop_weapons"),
        InlineKeyboardButton(text="🧪 Зелья", callback_data="shop_potions"),
    )
    keyboard.row(
        InlineKeyboardButton(text="📊 Торг. площадка", callback_data="marketplace"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

def get_quests_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="📜 Активные", callback_data="quests_active"),
        InlineKeyboardButton(text="🎯 Доступные", callback_data="quests_available"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🏆 Завершенные", callback_data="quests_completed"),
        InlineKeyboardButton(text="🎁 Награды", callback_data="quests_rewards"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

def get_clan_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="👑 Создать клан", callback_data="clan_create"),
        InlineKeyboardButton(text="🔍 Найти клан", callback_data="clan_search"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🏰 Мой клан", callback_data="clan_my"),
        InlineKeyboardButton(text="👥 Участники", callback_data="clan_members"),
    )
    keyboard.row(
        InlineKeyboardButton(text="💰 Казна", callback_data="clan_treasury"),
        InlineKeyboardButton(text="⚔️ Война", callback_data="clan_war"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

def get_craft_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="⚔️ Оружие", callback_data="craft_weapons"),
        InlineKeyboardButton(text="🧪 Зелья", callback_data="craft_potions"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🛠️ Инструменты", callback_data="craft_tools"),
        InlineKeyboardButton(text="💎 Украшения", callback_data="craft_jewelry"),
    )
    keyboard.row(
        InlineKeyboardButton(text="📜 Рецепты", callback_data="craft_recipes"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

def get_weapons_keyboard():
    keyboard = InlineKeyboardBuilder()
    weapons = [
        (WeaponType.SWORD, "sword", 100),
        (WeaponType.AXE, "axe", 120),
        (WeaponType.BOW, "bow", 150),
        (WeaponType.STAFF, "staff", 200),
        (WeaponType.DAGGER, "dagger", 80),
    ]
    
    for weapon_type, callback_suffix, gold_cost in weapons:
        keyboard.row(
            InlineKeyboardButton(
                text=f"{weapon_type.value} - {gold_cost}💰",
                callback_data=f"buy_{callback_suffix}"
            )
        )
    
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="shop_weapons"),
    )
    return keyboard.as_markup()

def get_resource_keyboard():
    keyboard = InlineKeyboardBuilder()
    for resource in Resource:
        keyboard.add(InlineKeyboardButton(
            text=f"{resource.value}", 
            callback_data=f"gather_{resource.name}"
        ))
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

def get_build_keyboard():
    keyboard = InlineKeyboardBuilder()
    for building in BuildingType:
        keyboard.add(InlineKeyboardButton(
            text=f"{building.value}", 
            callback_data=f"build_{building.name}"
        ))
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
    )
    return keyboard.as_markup()

# ========== КОМАНДЫ ==========

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        
        if user_id not in world.players:
            start_pos = Position(
                x=random.randint(-10, 10),
                y=random.randint(-10, 10)
            )
            world.players[user_id] = Player(user_id, username, start_pos)
            
            player = world.players[user_id]
            player.equipment["weapon"] = Weapon(
                type=WeaponType.SWORD,
                damage=(8, 15),
                speed=1.2,
                rarity=ItemRarity.UNCOMMON
            )
            
            await safe_send_message(
                user_id,
                f"🎮 Добро пожаловать в мир приключений, {username}!\n\n"
                f"📍 Стартовая позиция: {start_pos}\n"
                f"🌍 Локация: {world.get_biome(start_pos).value}\n"
                f"💰 Стартовый капитал: 30 золота\n"
                f"⚔️ Стартовое оружие: {WeaponType.SWORD.value}\n\n"
                f"🔥 Новые возможности:\n"
                f"• Система боев с монстрами\n"
                f"• Торговля между игроками\n"
                f"• Квесты и задания\n"
                f"• Клановая система\n"
                f"• Сезонные события\n"
                f"• Система крафта\n"
                f"• Глобальный и локальный чат\n",
                reply_markup=get_main_keyboard()
            )
        else:
            player = world.players[user_id]
            player.username = username  # Обновляем имя на случай изменения
            
            await safe_send_message(
                user_id,
                f"С возвращением, {username}!\n"
                f"📍 Позиция: {player.position}\n"
                f"🌍 Локация: {world.get_biome(player.position).value}\n"
                f"❤️ Здоровье: {player.health}/{player.max_health}\n"
                f"⚡ Энергия: {player.energy}/{player.max_energy}\n"
                f"⭐ Уровень: {player.level}\n"
                f"💰 Золото: {player.gold}",
                reply_markup=get_main_keyboard()
            )
        
        # Автосохранение
        world.save_to_file()
        
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")
        await safe_send_message(
            message.from_user.id,
            "❌ Произошла ошибка при запуске игры. Попробуйте еще раз."
        )

@dp.message(Command("chat"))
async def cmd_chat(message: types.Message):
    try:
        user_id = message.from_user.id
        
        if user_id not in world.players:
            await safe_send_message(user_id, "❌ Сначала начните игру командой /start")
            return
        
        player = world.players[user_id]
        
        if player.chat_muted:
            await safe_send_message(user_id, "🔇 Чат отключен. Включите его в настройках чата.")
            return
        
        if len(message.text.split()) > 1:
            msg_text = ' '.join(message.text.split()[1:])
            
            if len(msg_text) > 500:
                await safe_send_message(user_id, "❌ Сообщение слишком длинное (макс. 500 символов)")
                return
            
            # Добавляем сообщение в чат
            world.chat_messages.append(ChatMessage(
                player_id=user_id,
                username=player.username,
                message=msg_text,
                timestamp=datetime.now()
            ))
            
            # Ограничиваем историю чата
            if len(world.chat_messages) > 200:
                world.chat_messages = world.chat_messages[-200:]
            
            # Отправляем сообщение всем игрокам (глобальный чат)
            for other_player in world.players.values():
                if other_player.user_id != user_id and not other_player.chat_muted:
                    try:
                        await safe_send_message(
                            other_player.user_id,
                            f"💬 {player.username}: {msg_text}"
                        )
                    except:
                        pass
            
            await safe_send_message(user_id, "✅ Сообщение отправлено в глобальный чат!")
            
            # Автосохранение
            world.save_to_file()
            
        else:
            await show_chat(user_id)
            
    except Exception as e:
        logger.error(f"Ошибка в команде /chat: {e}")
        await safe_send_message(message.from_user.id, "❌ Ошибка отправки сообщения")

@dp.message(Command("save"))
async def cmd_save(message: types.Message):
    try:
        if world.save_to_file():
            await safe_send_message(message.from_user.id, "✅ Игра сохранена!")
        else:
            await safe_send_message(message.from_user.id, "❌ Ошибка при сохранении игры")
    except Exception as e:
        logger.error(f"Ошибка в команде /save: {e}")
        await safe_send_message(message.from_user.id, "❌ Ошибка при сохранении")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
🎮 *Команды бота:*

*/start* - Начать игру или продолжить
*/chat [сообщение]* - Отправить сообщение в глобальный чат
*/save* - Сохранить игру
*/help* - Показать это сообщение
*/profile* - Показать профиль
*/players* - Показать игроков онлайн
*/top* - Топ игроков

⚔️ *Игровые возможности:*
• Исследование мира с разными биомами
• Бои с монстрами
• Добыча ресурсов
• Строительство зданий
• Торговля с другими игроками
• Выполнение квестов
• Создание и участие в кланах
• Крафт предметов
• Сезонные события
• Глобальный и локальный чат

📱 *Управление:* Используйте кнопки под сообщениями для навигации
    """
    await safe_send_message(message.from_user.id, help_text, parse_mode="Markdown")

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    try:
        user_id = message.from_user.id
        
        if user_id not in world.players:
            await safe_send_message(user_id, "❌ Сначала начните игру командой /start")
            return
        
        player = world.players[user_id]
        weapon = player.equipment.get("weapon")
        weapon_name = weapon.type.value if weapon else "👊 Кулаки"
        min_dmg, max_dmg = player.get_total_damage()
        
        profile_text = (
            f"👤 *Профиль игрока:* {player.username}\n"
            f"⭐ Уровень: {player.level}\n"
            f"📊 Опыт: {player.experience}/{player.level * 100}\n"
            f"❤️ Здоровье: {player.health}/{player.max_health}\n"
            f"⚡ Энергия: {player.energy}/{player.max_energy}\n"
            f"💰 Золото: {player.gold}\n"
            f"📍 Позиция: {player.position}\n"
            f"🌍 Биом: {world.get_biome(player.position).value}\n"
            f"⚔️ Оружие: {weapon_name}\n"
            f"💢 Урон: {min_dmg}-{max_dmg}\n"
            f"🏠 Построек: {len(player.buildings)}\n"
            f"🎯 Активных квестов: {len(player.active_quests)}\n"
            f"👑 Клан: {'Нет' if not player.clan_id else world.clans[player.clan_id].name if player.clan_id in world.clans else 'Неизвестно'}\n"
        )
        
        await safe_send_message(user_id, profile_text, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Ошибка в команде /profile: {e}")
        await safe_send_message(message.from_user.id, "❌ Ошибка загрузки профиля")

@dp.message(Command("players"))
async def cmd_players(message: types.Message):
    try:
        if not world.players:
            await safe_send_message(message.from_user.id, "👥 Сейчас нет игроков онлайн")
            return
        
        players_text = "👥 *Игроки онлайн:*\n\n"
        for player in world.players.values():
            online_status = "🟢" if (datetime.now() - player.last_action_time).seconds < 300 else "⚫"
            players_text += f"{online_status} {player.username} (Ур. {player.level})\n"
        
        players_text += f"\nВсего игроков: {len(world.players)}"
        
        await safe_send_message(message.from_user.id, players_text, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Ошибка в команде /players: {e}")
        await safe_send_message(message.from_user.id, "❌ Ошибка загрузки списка игроков")

@dp.message(Command("top"))
async def cmd_top(message: types.Message):
    try:
        if not world.players:
            await safe_send_message(message.from_user.id, "🏆 Пока нет игроков в топе")
            return
        
        # Сортируем игроков по уровню и золоту
        sorted_players = sorted(
            world.players.values(),
            key=lambda p: (p.level, p.gold),
            reverse=True
        )
        
        top_text = "🏆 *Топ игроков:*\n\n"
        for i, player in enumerate(sorted_players[:10], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            top_text += f"{medal} {player.username} - Ур. {player.level} | 💰 {player.gold}\n"
        
        await safe_send_message(message.from_user.id, top_text, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Ошибка в команде /top: {e}")
        await safe_send_message(message.from_user.id, "❌ Ошибка загрузки топа")

# ========== CALLBACK ОБРАБОТЧИКИ ==========

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    try:
        data = callback.data
        
        # Обработка главного меню
        if data == "main_menu":
            await main_menu(callback)
        elif data == "map":
            await show_map(callback)
        elif data == "status":
            await show_status(callback)
        elif data == "inventory":
            await show_inventory(callback)
        elif data == "buildings":
            await show_buildings(callback)
        elif data == "move_menu":
            await move_menu(callback)
        elif data == "gather":
            await gather_menu(callback)
        
        # Боевая система
        elif data == "combat_menu":
            await combat_menu(callback)
        elif data.startswith("attack_"):
            await start_combat(callback)
        elif data.startswith("combat_"):
            await combat_action(callback)
        
        # Чат
        elif data == "chat_menu":
            await chat_menu(callback)
        elif data == "global_chat":
            await global_chat(callback)
        elif data == "local_chat":
            await local_chat(callback)
        elif data == "mute_chat":
            await mute_chat(callback)
        elif data == "unmute_chat":
            await unmute_chat(callback)
        
        # Торговля
        elif data == "shop":
            await shop_menu(callback)
        elif data == "shop_weapons":
            await shop_weapons(callback)
        elif data.startswith("buy_"):
            await buy_item(callback)
        elif data == "marketplace":
            await marketplace(callback)
        
        # Квесты
        elif data == "quests_menu":
            await quests_menu(callback)
        elif data == "quests_available":
            await quests_available(callback)
        elif data.startswith("accept_quest_"):
            await accept_quest(callback)
        
        # Кланы
        elif data == "clan_menu":
            await clan_menu(callback)
        elif data == "clan_create":
            await clan_create(callback)
        
        # Крафт
        elif data == "craft_menu":
            await craft_menu(callback)
        elif data == "craft_weapons":
            await craft_weapons(callback)
        elif data.startswith("craft_"):
            await execute_craft(callback)
        
        # Движение
        elif data.startswith("move_"):
            await move_player(callback)
        elif data == "teleport":
            await teleport_menu(callback)
        
        # Добыча
        elif data.startswith("gather_"):
            await gather_resource(callback)
        
        # Строительство
        elif data.startswith("build_"):
            await build_structure(callback)
        
        else:
            await callback.answer("⚠️ Функция в разработке")
            
    except Exception as e:
        logger.error(f"Ошибка в обработчике callback: {e}")
        try:
            await callback.answer("❌ Произошла ошибка")
        except:
            pass

async def main_menu(callback: types.CallbackQuery):
    player = world.players.get(callback.from_user.id)
    if player:
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            f"🎮 *Главное меню*\n"
            f"📍 Позиция: {player.position}\n"
            f"🌍 Локация: {world.get_biome(player.position).value}\n"
            f"🎭 Сезон: {world.current_season.value}",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    await callback.answer()

async def show_map(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        map_size = 5
        map_text = "🗺️ *Карта местности:*\n\n"
        
        for y in range(player.position.y + map_size, player.position.y - map_size - 1, -1):
            line = ""
            for x in range(player.position.x - map_size, player.position.x + map_size + 1):
                if x == player.position.x and y == player.position.y:
                    line += "👤"
                elif (x, y) in world.monsters:
                    line += "👹"
                elif any(b.position.x == x and b.position.y == y for b in player.buildings):
                    line += "🏠"
                elif (x, y) in world.world_map:
                    biome = world.world_map[(x, y)]
                    icons = {
                        Biome.FOREST: "🌲",
                        Biome.MOUNTAINS: "⛰️",
                        Biome.PLAINS: "🟩",
                        Biome.RIVER: "🌊",
                        Biome.VILLAGE: "🏘️",
                        Biome.BEACH: "🏖️",
                        Biome.CAVE: "🕳️"
                    }
                    line += icons.get(biome, "·")
                else:
                    line += "·"
            map_text += line + "\n"
        
        map_text += f"\n📍 *Ваша позиция:* {player.position}"
        map_text += f"\n👤 - Вы, 👹 - Монстр, 🏠 - Ваша постройка"
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            map_text,
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка показа карты: {e}")
        await callback.answer("❌ Ошибка загрузки карты")

async def show_status(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        weapon = player.equipment.get("weapon")
        weapon_name = weapon.type.value if weapon else "👊 Кулаки"
        min_dmg, max_dmg = player.get_total_damage()
        gathering_bonus = player.calculate_gathering_bonus()
        
        status_text = (
            f"👤 *Статус игрока:* {player.username}\n"
            f"⭐ Уровень: {player.level}\n"
            f"📊 Опыт: {player.experience}/{player.level * 100}\n"
            f"❤️ Здоровье: {player.health}/{player.max_health}\n"
            f"⚡ Энергия: {player.energy}/{player.max_energy}\n"
            f"💰 Золото: {player.gold}\n"
            f"📍 Позиция: {player.position}\n"
            f"🌍 Биом: {world.get_biome(player.position).value}\n"
            f"🎭 Сезон: {world.current_season.value}\n"
            f"⚔️ Оружие: {weapon_name}\n"
            f"💢 Урон: {min_dmg}-{max_dmg}\n"
            f"🎯 Бонус добычи: x{gathering_bonus:.1f}\n"
            f"🏠 Построек: {len(player.buildings)}\n"
            f"🎯 Активных квестов: {len(player.active_quests)}\n"
            f"🏆 Завершено квестов: {len(player.completed_quests)}\n"
        )
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            status_text,
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка показа статуса: {e}")
        await callback.answer("❌ Ошибка загрузки статуса")

async def show_inventory(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        inventory_text = "🎒 *Ваш инвентарь:*\n\n"
        
        # Ресурсы
        inventory_text += "📦 *Ресурсы:*\n"
        has_resources = False
        for resource, amount in player.resources.items():
            if amount > 0:
                inventory_text += f"{resource.value}: {amount}\n"
                has_resources = True
        
        if not has_resources:
            inventory_text += "Пусто\n"
        
        # Предметы
        inventory_text += "\n🎁 *Предметы:*\n"
        has_items = False
        for item, amount in player.inventory.items():
            if amount > 0:
                item_name = {
                    "health_potion": "🧪 Зелье здоровья",
                    "energy_potion": "⚡ Зелье энергии"
                }.get(item, item)
                inventory_text += f"{item_name}: {amount}\n"
                has_items = True
        
        if not has_items:
            inventory_text += "Пусто\n"
        
        # Оружие
        weapon = player.equipment.get("weapon")
        if weapon:
            inventory_text += f"\n⚔️ *Оружие:* {weapon.type.value}\n"
            inventory_text += f"💢 Урон: {weapon.damage[0]}-{weapon.damage[1]}\n"
            inventory_text += f"⭐ Редкость: {weapon.rarity.value}"
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            inventory_text,
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка показа инвентаря: {e}")
        await callback.answer("❌ Ошибка загрузки инвентаря")

async def chat_menu(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        chat_text = (
            f"💬 *Меню чата*\n\n"
            f"Статус: {'🔇 Отключен' if player.chat_muted else '🔊 Включен'}\n"
            f"Сообщений в истории: {len(world.chat_messages)}\n\n"
            f"*Глобальный чат:* Виден всем игрокам\n"
            f"*Локальный чат:* Виден игрокам в радиусе 20 клеток\n\n"
            f"Для отправки сообщения используйте команду:\n"
            f"`/chat [ваше сообщение]`"
        )
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            chat_text,
            reply_markup=get_chat_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка меню чата: {e}")
        await callback.answer("❌ Ошибка загрузки меню чата")

async def global_chat(callback: types.CallbackQuery):
    try:
        chat_text = "💬 *Глобальный чат (последние 10 сообщений):*\n\n"
        
        if not world.chat_messages:
            chat_text += "Пока нет сообщений. Будьте первым!"
        else:
            for msg in world.chat_messages[-10:]:
                time_str = msg.timestamp.strftime("%H:%M")
                chat_text += f"[{time_str}] *{msg.username}:* {msg.message}\n"
        
        chat_text += "\nДля отправки сообщения используйте команду:\n`/chat [ваше сообщение]`"
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            chat_text,
            reply_markup=get_chat_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка глобального чата: {e}")
        await callback.answer("❌ Ошибка загрузки чата")

async def local_chat(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        # Получаем игроков в радиусе 20 клеток
        nearby_players = world.get_players_in_area(player.position, 20)
        nearby_player_ids = {p.user_id for p in nearby_players}
        
        # Фильтруем сообщения от этих игроков
        local_messages = [
            msg for msg in world.chat_messages[-20:]
            if msg.player_id in nearby_player_ids
        ]
        
        chat_text = f"📨 *Локальный чат (радиус 20 клеток):*\n\n"
        
        if not local_messages:
            chat_text += "Пока нет сообщений в вашей области.\n"
            chat_text += f"Игроков рядом: {len(nearby_players)}"
        else:
            for msg in local_messages[-10:]:
                time_str = msg.timestamp.strftime("%H:%M")
                distance = "???"
                if msg.player_id in world.players:
                    sender_pos = world.players[msg.player_id].position
                    distance = f"{sender_pos.distance_to(player.position):.1f}"
                chat_text += f"[{time_str}] *{msg.username}* ({distance}кл): {msg.message}\n"
        
        chat_text += "\nДля отправки сообщения используйте команду:\n`/chat [ваше сообщение]`"
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            chat_text,
            reply_markup=get_chat_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка локального чата: {e}")
        await callback.answer("❌ Ошибка загрузки локального чата")

async def mute_chat(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        player.chat_muted = True
        world.save_to_file()
        
        await callback.answer("🔇 Чат отключен")
        await chat_menu(callback)
        
    except Exception as e:
        logger.error(f"Ошибка отключения чата: {e}")
        await callback.answer("❌ Ошибка отключения чата")

async def unmute_chat(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        player.chat_muted = False
        world.save_to_file()
        
        await callback.answer("🔊 Чат включен")
        await chat_menu(callback)
        
    except Exception as e:
        logger.error(f"Ошибка включения чата: {e}")
        await callback.answer("❌ Ошибка включения чата")

async def show_chat(user_id: int):
    try:
        chat_text = "💬 *Глобальный чат (последние 10 сообщений):*\n\n"
        
        if not world.chat_messages:
            chat_text += "Пока нет сообщений. Будьте первым!"
        else:
            for msg in world.chat_messages[-10:]:
                time_str = msg.timestamp.strftime("%H:%M")
                chat_text += f"[{time_str}] *{msg.username}:* {msg.message}\n"
        
        chat_text += "\nДля отправки сообщения используйте команду:\n`/chat [ваше сообщение]`"
        
        await safe_send_message(user_id, chat_text, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Ошибка показа чата: {e}")

# ========== БОЕВАЯ СИСТЕМА ==========

async def combat_menu(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        nearby_monsters = world.get_monsters_in_area(player.position, 3)
        
        if not nearby_monsters:
            text = "⚔️ *Вокруг нет монстров*\nПередвигайтесь по карте, чтобы найти их"
            keyboard = InlineKeyboardBuilder()
            keyboard.row(
                InlineKeyboardButton(text="🗺️ Карта", callback_data="map"),
                InlineKeyboardButton(text="🚶‍♂️ Движение", callback_data="move_menu"),
            )
            keyboard.row(
                InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
            )
        else:
            text = "⚔️ *Монстры поблизости:*\n\n"
            for i, (pos, monster) in enumerate(nearby_monsters[:5], 1):
                distance = pos.distance_to(player.position)
                text += f"{i}. {monster.type.value} (Ур. {monster.level})\n"
                text += f"   ❤️ {monster.health} | 📍 {distance:.1f} клеток\n"
            
            keyboard = InlineKeyboardBuilder()
            for i in range(min(3, len(nearby_monsters))):
                monster_type = nearby_monsters[i][1].type.name
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"⚔️ Атаковать {nearby_monsters[i][1].type.value}",
                        callback_data=f"attack_{monster_type}"
                    )
                )
            keyboard.row(
                InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"),
            )
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            text,
            reply_markup=keyboard.as_markup(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка меню боя: {e}")
        await callback.answer("❌ Ошибка загрузки меню боя")

async def start_combat(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        monster_type_name = callback.data.split("_")[1]
        monster_type = MonsterType[monster_type_name]
        
        nearby_monsters = world.get_monsters_in_area(player.position, 3)
        target_monster = None
        monster_pos = None
        
        for pos, monster in nearby_monsters:
            if monster.type == monster_type:
                target_monster = monster
                monster_pos = pos
                break
        
        if not target_monster:
            await callback.answer("❌ Монстр убежал!")
            return
        
        # Сохраняем состояние боя
        player_data = {
            "monster": target_monster,
            "monster_pos": monster_pos,
            "player_health": player.health,
            "monster_health": target_monster.health,
            "round": 1
        }
        
        world.combat_states[callback.from_user.id] = player_data
        
        min_dmg, max_dmg = player.get_total_damage()
        weapon_name = player.equipment["weapon"].type.value if player.equipment.get("weapon") else "Кулаки"
        
        text = (
            f"⚔️ *НАЧАЛО БОЯ!*\n\n"
            f"👤 {player.username} vs {target_monster.type.value}\n\n"
            f"*Ваши характеристики:*\n"
            f"❤️ Здоровье: {player.health}/{player.max_health}\n"
            f"⚔️ Оружие: {weapon_name}\n"
            f"💢 Урон: {min_dmg}-{max_dmg}\n\n"
            f"*Характеристики монстра:*\n"
            f"❤️ Здоровье: {target_monster.health}\n"
            f"💢 Урон: {target_monster.damage[0]}-{target_monster.damage[1]}\n"
            f"⭐ Уровень: {target_monster.level}\n"
            f"💰 Награда: {target_monster.gold_reward} золота\n\n"
            f"*Выберите действие:*"
        )
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            text,
            reply_markup=get_combat_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка начала боя: {e}")
        await callback.answer("❌ Ошибка начала боя")

async def combat_action(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        action = callback.data.split("_")[1]
        combat_state = world.combat_states.get(callback.from_user.id)
        
        if not combat_state:
            await callback.answer("❌ Бой не найден")
            return
        
        monster = combat_state["monster"]
        monster_pos = combat_state["monster_pos"]
        
        result_text = ""
        
        if action == "attack":
            # Игрок атакует
            min_dmg, max_dmg = player.get_total_damage()
            player_damage = random.randint(min_dmg, max_dmg)
            combat_state["monster_health"] -= player_damage
            
            result_text += f"🎯 *Вы нанесли {player_damage} урона!*\n"
            
            # Проверяем смерть монстра
            if combat_state["monster_health"] <= 0:
                # Награда за победу
                gold_earned = monster.gold_reward * 2
                exp_earned = monster.exp_reward
                
                player.gold += gold_earned
                player.experience += exp_earned
                
                # Записываем убийство
                player.kills[monster.type] = player.kills.get(monster.type, 0) + 1
                
                # Удаляем монстра с карты
                if monster_pos in world.monsters:
                    del world.monsters[monster_pos]
                
                level_up = player.add_experience(exp_earned)
                
                result_text += (
                    f"\n🎉 *ПОБЕДА!*\n"
                    f"💰 Получено: {gold_earned} золота\n"
                    f"⭐ Опыт: {exp_earned}\n"
                )
                
                if level_up:
                    result_text += f"🏆 *Уровень повышен!* Теперь у вас {player.level} уровень!\n"
                
                # Обновляем здоровье игрока
                player.health = combat_state["player_health"]
                player.last_action_time = datetime.now()
                
                del world.combat_states[callback.from_user.id]
                
                keyboard = InlineKeyboardBuilder()
                keyboard.row(
                    InlineKeyboardButton(text="⚔️ Еще бой", callback_data="combat_menu"),
                    InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory"),
                )
                keyboard.row(
                    InlineKeyboardButton(text="🔙 В меню", callback_data="main_menu"),
                )
                
                await safe_edit_message(
                    callback.message.chat.id,
                    callback.message.message_id,
                    result_text,
                    reply_markup=keyboard.as_markup(),
                    parse_mode="Markdown"
                )
                
                world.save_to_file()
                await callback.answer()
                return
            
            # Монстр контратакует
            monster_damage = random.randint(monster.damage[0], monster.damage[1])
            combat_state["player_health"] -= monster_damage
            
            result_text += f"👹 *Монстр нанес {monster_damage} урона!*\n"
            
            # Проверяем смерть игрока
            if combat_state["player_health"] <= 0:
                player.health = player.max_health // 2
                player.gold = max(0, player.gold // 2)
                
                result_text += (
                    f"\n💀 *ВЫ УМЕРЛИ!*\n"
                    f"💰 Потеряно: {player.gold} золота\n"
                    f"❤️ Воскрешение с {player.health} здоровья\n"
                )
                
                del world.combat_states[callback.from_user.id]
                
                keyboard = InlineKeyboardBuilder()
                keyboard.row(
                    InlineKeyboardButton(text="🏥 Лечиться", callback_data="heal"),
                    InlineKeyboardButton(text="🔙 В меню", callback_data="main_menu"),
                )
                
                await safe_edit_message(
                    callback.message.chat.id,
                    callback.message.message_id,
                    result_text,
                    reply_markup=keyboard.as_markup(),
                    parse_mode="Markdown"
                )
                
                world.save_to_file()
                await callback.answer()
                return
        
        elif action == "defend":
            # Защита уменьшает урон
            monster_damage = random.randint(monster.damage[0], monster.damage[1]) // 2
            combat_state["player_health"] -= monster_damage
            
            result_text += f"🛡️ *Вы защитились!* Получено {monster_damage} урона\n"
        
        elif action == "potion":
            # Использование зелья
            if player.inventory.get("health_potion", 0) > 0:
                heal_amount = 30
                combat_state["player_health"] = min(
                    player.max_health,
                    combat_state["player_health"] + heal_amount
                )
                player.inventory["health_potion"] -= 1
                
                result_text += f"🧪 *Использовано зелье здоровья!* +{heal_amount}❤️\n"
            else:
                result_text += "❌ *У вас нет зелий здоровья!*\n"
        
        elif action == "flee":
            # Попытка сбежать
            flee_chance = 0.7
            if random.random() < flee_chance:
                player.health = combat_state["player_health"]
                player.last_action_time = datetime.now()
                result_text = "🏃 *Вы успешно сбежали!*"
                
                del world.combat_states[callback.from_user.id]
                
                await safe_edit_message(
                    callback.message.chat.id,
                    callback.message.message_id,
                    result_text,
                    reply_markup=get_main_keyboard(),
                    parse_mode="Markdown"
                )
                
                world.save_to_file()
                await callback.answer()
                return
            else:
                # Неудачная попытка побега
                monster_damage = random.randint(monster.damage[0], monster.damage[1])
                combat_state["player_health"] -= monster_damage
                result_text += f"❌ *Не удалось сбежать!* Получено {monster_damage} урона\n"
        
        # Обновляем состояние боя
        combat_state["round"] += 1
        world.combat_states[callback.from_user.id] = combat_state
        player.last_action_time = datetime.now()
        
        # Показываем текущее состояние
        result_text += (
            f"\n📊 *Состояние после раунда {combat_state['round']-1}:*\n"
            f"❤️ Ваше здоровье: {combat_state['player_health']}/{player.max_health}\n"
            f"❤️ Здоровье монстра: {combat_state['monster_health']}\n"
        )
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            result_text,
            reply_markup=get_combat_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка действия в бою: {e}")
        await callback.answer("❌ Ошибка в бою")

# ========== ДОБЫЧА РЕСУРСОВ ==========

async def gather_menu(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        biome = world.get_biome(player.position)
        available_resources = world.get_resources_in_biome(biome)
        
        text = f"⚒️ *Добыча ресурсов в {biome.value}:*\n\n"
        text += "*Доступные ресурсы:*\n"
        for resource in available_resources:
            text += f"{resource.value}\n"
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            text,
            reply_markup=get_resource_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка меню добычи: {e}")
        await callback.answer("❌ Ошибка загрузки меню добычи")

async def gather_resource(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        if player.energy < 15:
            await callback.answer("❌ Недостаточно энергии!")
            return
        
        resource_name = callback.data.split("_")[1]
        try:
            resource = Resource[resource_name]
        except:
            await callback.answer("❌ Ресурс не найден")
            return
        
        biome = world.get_biome(player.position)
        available_resources = world.get_resources_in_biome(biome)
        
        if resource not in available_resources:
            await callback.answer("❌ Этот ресурс недоступен в этой локации")
            return
        
        # Расчет бонусов
        gathering_bonus = player.calculate_gathering_bonus()
        seasonal_bonus = world.get_seasonal_bonus().get("gathering", 1.0)
        total_bonus = gathering_bonus * seasonal_bonus
        
        # Базовая добыча
        base_amount = random.randint(5, 15)
        amount = int(base_amount * total_bonus)
        
        # Особый бонус для золота
        if resource == Resource.GOLD:
            amount *= 2
            if player.equipment["weapon"].type in [WeaponType.AXE, WeaponType.SWORD]:
                amount = int(amount * 1.5)
        
        player.resources[resource] = player.resources.get(resource, 0) + amount
        player.energy -= 15
        player.last_action_time = datetime.now()
        
        # Даем золото с шансом при любой добыче
        gold_chance = 0.3
        gold_msg = ""
        if random.random() < gold_chance:
            extra_gold = random.randint(5, 20)
            player.gold += extra_gold
            gold_msg = f"\n💰 *Бонусное золото:* +{extra_gold}"
        
        # Добавляем опыт
        exp_gained = amount * 2
        level_up_msg = ""
        if player.add_experience(exp_gained):
            level_up_msg = "\n🎉 *Поздравляем! Вы достигли нового уровня!*"
        
        # Сезонное сообщение
        season_msg = ""
        if seasonal_bonus != 1.0:
            season_msg = f"\n🎭 *Сезонный бонус:* x{seasonal_bonus}"
        
        result_text = (
            f"✅ *Вы добыли {amount} единиц {resource.value}!*\n"
            f"⚡ Энергия: {player.energy}/{player.max_energy}\n"
            f"🎯 Бонус добычи: x{total_bonus:.1f}{season_msg}"
            f"{gold_msg}{level_up_msg}"
        )
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            result_text,
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
        # Автосохранение
        world.save_to_file()
        
    except Exception as e:
        logger.error(f"Ошибка добычи ресурсов: {e}")
        await callback.answer("❌ Ошибка добычи ресурсов")

# ========== ДВИЖЕНИЕ ==========

async def move_menu(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            f"*Выберите направление движения:*\n"
            f"📍 Текущая позиция: {player.position}",
            reply_markup=get_movement_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка меню движения: {e}")
        await callback.answer("❌ Ошибка загрузки меню движения")

async def move_player(callback: types.CallbackQuery):
    try:
        player = world.players.get(callback.from_user.id)
        if not player:
            await callback.answer("❌ Игрок не найден")
            return
        
        if player.energy < 10:
            await callback.answer("❌ Недостаточно энергии!")
            return
        
        direction = callback.data.split("_")[1]
        new_pos = Position(player.position.x, player.position.y)
        
        if direction == "north":
            new_pos.y += 1
        elif direction == "south":
            new_pos.y -= 1
        elif direction == "east":
            new_pos.x += 1
        elif direction == "west":
            new_pos.x -= 1
        
        # Проверка границ мира
        if abs(new_pos.x) > world.size or abs(new_pos.y) > world.size:
            await callback.answer("❌ Вы достигли края мира!")
            return
        
        player.position = new_pos
        player.energy -= 10
        player.health = min(player.max_health, player.health + 1)
        player.last_action_time = datetime.now()
        
        # Проверка на уровень
        level_up_msg = ""
        if player.add_experience(5):
            level_up_msg = "\n🎉 *Поздравляем! Вы достигли нового уровня!*"
        
        biome = world.get_biome(new_pos)
        result_text = (
            f"*Вы переместились {direction}!*\n"
            f"📍 Новая позиция: {new_pos}\n"
            f"🌍 Локация: {biome.value}\n"
            f"⚡ Энергия: {player.energy}/{player.max_energy}"
            f"{level_up_msg}"
        )
        
        await safe_edit_message(
            callback.message.chat.id,
            callback.message.message_id,
            result_text,
            reply_markup=get_movement_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        
        # Автосохранение
        world.save_to_file()
        
    except Exception as e:
        logger.error(f"Ошибка движения: {e}")
        await callback.answer("❌ Ошибка движения")

# Добавьте остальные обработчики по аналогии...

# ========== СИСТЕМНЫЕ ФУНКЦИИ ==========

async def auto_regen():
    """Автоматическое восстановление здоровья и энергии"""
    while True:
        try:
            await asyncio.sleep(60)
            
            for player in world.players.values():
                # Восстановление в зависимости от построек
                has_house = any(b.type == BuildingType.HOUSE for b in player.buildings)
                
                if has_house:
                    regen_amount = 10
                    player.health = min(player.max_health, player.health + regen_amount)
                    player.energy = min(player.max_energy, player.energy + 15)
                else:
                    regen_amount = 5
                    player.energy = min(player.max_energy, player.energy + regen_amount)
                
                # Производство на ферме
                has_farm = any(b.type == BuildingType.FARM for b in player.buildings)
                if has_farm:
                    player.resources[Resource.FOOD] = player.resources.get(Resource.FOOD, 0) + 10
                    if random.random() < 0.1:
                        player.gold += random.randint(5, 15)
                
                # Автосохранение каждые 5 минут
                if (datetime.now() - player.last_action_time).seconds > 300:
                    world.save_to_file()
            
        except Exception as e:
            logger.error(f"Ошибка в auto_regen: {e}")

async def seasonal_updater():
    """Обновление сезонов и событий"""
    while True:
        try:
            await asyncio.sleep(3600)
            world.update_season()
            
            # Случайные мировые события
            if random.random() < 0.3:
                events = [
                    "🐉 Появился древний дракон в горах!",
                    "💎 Обнаружена золотая жила в пещерах!",
                    "👥 Организуется турнир между кланами!",
                    "🎁 Таинственный торговец в деревне!",
                    "👹 Орды монстров атакуют окраины!",
                ]
                
                event = random.choice(events)
                for player in world.players.values():
                    if not player.chat_muted:
                        await safe_send_message(
                            player.user_id,
                            f"📢 *МИРОВОЕ СОБЫТИЕ:* {event}\n"
                            f"Спешите принять участие!",
                            parse_mode="Markdown"
                        )
            
            # Автосохранение
            world.save_to_file()
            
        except Exception as e:
            logger.error(f"Ошибка в seasonal_updater: {e}")

# ========== ЗАПУСК БОТА ==========

async def main():
    try:
        # Загружаем сохраненную игру
        if os.path.exists(SAVE_DIR / "enhanced_world.json"):
            logger.info("Загружаем сохраненную игру...")
            world.load_from_file("enhanced_world.json")
        
        # Запускаем системные задачи
        asyncio.create_task(auto_regen())
        asyncio.create_task(seasonal_updater())
        
        # Запускаем бота
        logger.info("Бот запущен!")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
