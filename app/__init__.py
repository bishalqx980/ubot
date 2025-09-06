import json
from time import time

from pyrogram import Client, __version__ as __pyroVersion__
from pyrogram.types import LinkPreviewOptions
from pyrogram.enums import ClientPlatform

from .utils.logger import setup_logging
from config import CONFIG

# constants
__version__ = json.load(open("version.json", "rb"))["__version__"] # major.minor.patch.commits
CLIENT_UPTIME = time()

# initializing config
logger = setup_logging() # need to execute after creating Required folderss
config = CONFIG()

ubot = Client(
    name="account",
    api_id=config.api_id,
    api_hash=config.api_hash,
    app_version=f"{__pyroVersion__} x64",
    device_model="Desktop",
    system_version="Windows 11 x64",
    session_string=config.session_string,
    workdir="sys",
    client_platform=ClientPlatform.DESKTOP,
    link_preview_options=LinkPreviewOptions(is_disabled=True)
)

logger.info(f"""
Developed by
 ______     __     ______     __  __     ______     __        
/\  == \   /\ \   /\  ___\   /\ \_\ \   /\  __ \   /\ \       
\ \  __<   \ \ \  \ \___  \  \ \  __ \  \ \  __ \  \ \ \____  
 \ \_____\  \ \_\  \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_____/ 
   
    Version: {__version__}
    Library: kurigram {__pyroVersion__}
    GitHub: https://github.com/bishalqx980
""")
