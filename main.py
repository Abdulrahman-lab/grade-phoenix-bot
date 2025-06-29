#!/usr/bin/env python3
"""
🎓 Telegram University Bot - Main Entry Point
بوت إشعارات الدرجات الجامعية - نقطة البداية الرئيسية
"""
import asyncio
import logging
import os
import sys
import signal
from datetime import datetime
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.core import TelegramBot
from config import CONFIG

# Set up logging
logging.basicConfig(
    level=getattr(logging, CONFIG["LOG_LEVEL"]),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG["LOG_FILE"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("DEBUG: Main script starting - logging test")

class BotRunner:
    """Main bot runner (webhook only)"""
    
    def __init__(self):
        self.bot = TelegramBot()
        self.running = False
        self.start_time = None
        
    async def start(self):
        """Start the bot with all features"""
        try:
            logger.info("🚀 Starting Telegram University Bot...")
            self.start_time = datetime.now()
            self.running = True
            
            # Create necessary directories
            self.create_directories()
            
            # Start the bot
            await self.bot.start()
            
            logger.info("✅ Bot started successfully!")
            logger.info(f"📊 Admin ID: {CONFIG['ADMIN_ID']}")
            logger.info(f"🕒 Start time: {self.start_time}")
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot gracefully"""
        logger.info("🛑 Stopping bot...")
        self.running = False
        
        if self.bot:
            await self.bot.stop()
        
        logger.info("✅ Bot stopped successfully!")
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            CONFIG["DATA_DIR"],
            CONFIG.get("LOGS_DIR", "logs"),
            CONFIG.get("BACKUP_DIR", "backups")
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            logger.info(f"📁 Created directory: {directory}")

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ["TELEGRAM_TOKEN", "ADMIN_ID"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {missing_vars}")
        logger.info("💡 Please set the following environment variables:")
        for var in missing_vars:
            logger.info(f"   export {var}=your_value")
        return False
    
    return True

async def main():
    """Main function"""
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Create bot runner
    runner = BotRunner()
    
    # Set up signal handlers
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(runner.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await runner.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await runner.stop()

if __name__ == "__main__":
    print("🎓 Telegram University Bot v2.0.0")
    print("بوت إشعارات الدرجات الجامعية")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Failed to run bot: {e}")
        sys.exit(1) 