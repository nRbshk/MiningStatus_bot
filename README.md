# MiningStatus_bot
aiogram telegram bot for control miners

# Run:
- python -m pip install -r req.txt
- Rename example.ini to config.ini
- Write @BotFather and receive token for your bot. put this token into config.ini
- In config.ini setup your coins. Work only with NBMiner. 
- put nbminer.exe in bot root folder. Also need driver_install.bat and driver_uninstall.bat
- add nbminer.exe to exceptions for antivirus
- python main.py
- Open dialog with your bot and write /start
- /run and choose coin



# Features:
- can run and stop mining with bot. Use commands /run and /stop
- bot show total profit for all miners that running now. For calculation profit uses whattomine
- show your current balance at nanopool for all coins that specified in config.ini
- show one best coin with maximum profit for coins that specefied in config.ini
- can config miner with extra params. How you can do this you can look at nbminer params
- profit calculates from nanopool api. as it's not support power consumption it will does not give any impact on profit
