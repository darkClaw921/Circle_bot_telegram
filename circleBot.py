from loguru import logger
from art import text2art
from dotenv import load_dotenv
from aiogram.types import InputFile
import moviepy.editor as mpy

from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

logger.add('log.log', level='INFO')

load_dotenv()
tgToken = os.environ.get('TG_TOKEN')

bot = Bot(token=str(tgToken)) 
dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@logger.catch
def test_movie(path):
    clip = mpy.VideoFileClip(f'{path}')
    (w, h) = clip.size
    #720 не работает
    w = 640
    os.system(f'ffmpeg -i {path} -filter:v "crop={w}:{w}:{0}:{h/4}" 0{path}')
    #когда нибуди добавить статистику

    #a = os.system(f'du -h 0{path}')
    #logger.debug(a)

@dp.message_handler(content_types=['video'])
@logger.catch
async def handle_docs_photo(message):
    name = message.from_user.id
    #firstName = message.first_name
    #logger.info(f'{firstName} ')
    await message.video.download(f'{name}.mp4')
    test_movie(f'{name}.mp4')
    await bot.send_video_note(name, video_note= InputFile(f'0{name}.mp4'),duration=2)#open(f'0{name}.mp4', 'rb'))#f'{name}.mp4')#f'{name}.png')
    os.system(f'rm 0{name}.mp4')

@dp.message_handler(content_types=ContentType.ANY)
@logger.catch
async def echo_message(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    
    message = msg.text.lower()
    user_id = msg.from_user.id

    await bot.send_message(msg.from_user.id, 'Пришлите ваше видео')
    #await state.set_state('firstMsg')



if __name__ == '__main__':
    art = text2art('circle bot', 'rand')
    print(art)
    #main()
    executor.start_polling(dp)
