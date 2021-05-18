import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import code, bold


from requests import get

from Helpers.helpers import config, save_config, get_time, prepare_message
url = 'http://127.0.0.1:22333/api/v1/status'


logger = logging.getLogger(__name__)

class Show_handler(StatesGroup):

    get_info = State()




async def get_info(message: types.Message, state: FSMContext):
    response = get(url)

    if response.status_code != 200:
        await message.answer("No active miners!")
        await state.finish()
        return None
    # response = {"miner":{"devices":[{"accepted_shares":17,"core_clock":1290,"core_utilization":100,"fan":54,"hashrate":"153.5 M","hashrate2":"0.000 ","hashrate2_raw":0,"hashrate_raw":153458118.14680353,"id":0,"info":"NVIDIA GeForce RTX 3070","invalid_shares":0,"mem_clock":7750,"mem_utilization":41,"pci_bus_id":4,"power":104,"rejected_shares":0,"temperature":54},{"accepted_shares":28,"core_clock":1260,"core_utilization":100,"fan":70,"hashrate":"187.6 M","hashrate2":"0.000 ","hashrate2_raw":0,"hashrate_raw":187581645.98665234,"id":1,"info":"NVIDIA GeForce RTX 3080","invalid_shares":0,"mem_clock":9251,"mem_utilization":34,"pci_bus_id":43,"power":170,"rejected_shares":0,"temperature":43}],"total_hashrate":"341.0 M","total_hashrate2":"0.000 ","total_hashrate2_raw":0,"total_hashrate_raw":341039764.1334559,"total_power_consume":274},"reboot_times":0,"start_time":1621367721,"stratum":{"accepted_shares":45,"algorithm":"ergo","difficulty":"5.000 G","dual_mine":False,"invalid_shares":0,"latency":121,"pool_hashrate_10m":"405.4 M","pool_hashrate_24h":"405.4 M","pool_hashrate_4h":"405.4 M","rejected_shares":0,"url":"ergo-eu1.nanopool.org:11111","use_ssl":False,"user":"9hsPLkvTKt7z61uYCxu5KuiPKU5atfV6AkFhypdhfkMKN4SonV6.ergo_3070_3080/slayer.han1997@gmail.com"},"version":"37.3"}

    answer = prepare_message(response.json())

    last_message_id = await message.answer(code(answer), parse_mode=types.ParseMode.MARKDOWN_V2)

    config.update({'last_message' : last_message_id['message_id']})
    
    save_config(config=config)

    await state.finish()

def register_handlers_show(dp: Dispatcher):
    dp.register_message_handler(get_info, commands="show", state="*")