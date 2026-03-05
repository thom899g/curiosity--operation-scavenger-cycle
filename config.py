"""
Configuration manager for DEX Scanner System
Centralizes all configuration with environment variable fallbacks
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import logging

load_dotenv()

@dataclass
class DEXConfig:
    """DEX Scanner Configuration"""
    # DEX and Trading Pair Configuration
    DEX_NAME: str = "pancakeswap"
    CHAIN_ID: int = 56  # BSC Mainnet
    RPC_URL: str = os.getenv("RPC_URL", "https://bsc-dataseed.binance.org/")
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "0xE6Df0BB08e5A97b40B21950a0A51b5c4cDc0E4f8")  # BONK/USDT pair
    
    # Scanner Configuration
    POLL_INTERVAL_SECONDS: int = 3
    MAX_RETRIES: int = 5
    RETRY_DELAY: float = 1.0
    
    # Firebase Configuration
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
    
    # Arbitrage Detection Parameters
    MIN_PROFIT_THRESHOLD_BPS: int = 10  # 0.1%
    MAX_SLIPPAGE_BPS: int = 50  # 0.5%
    SIMULATION_CAPITAL_USD: float = 1000.0
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self) -> bool:
        """Validate critical configuration parameters"""
        if not self.RPC_URL:
            logging.error("RPC_URL is required")
            return False
        
        if not self.FIREBASE_PROJECT_ID or not self.FIREBASE_CREDENTIALS_PATH:
            logging.warning("Firebase configuration incomplete - some features disabled")
        
        return True
    
    @classmethod
    def from_env(cls) -> 'DEXConfig':
        """Create configuration from environment variables"""
        return cls()

# Global configuration instance
config = DEXConfig.from_env()