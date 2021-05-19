from asyncio import run
from Services.bot import start


if __name__ == '__main__':
    print('running bot')
    run(start())