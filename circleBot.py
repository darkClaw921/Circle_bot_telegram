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

logger.add('log.log', level='DEBUG')

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
    #w = 640
    if w > h:
        if w > 640:
            w = 640
        os.system(f'ffmpeg -i {path} -filter:v "crop={h}:{h}:{w/4}:{0}" 0{path}')
        logger.debug(f'левый угол {w/4} {0}')
        logger.debug(f'{w} {h}')
    else:  
        if w > 640:
            w=640
        os.system(f'ffmpeg -i {path} -filter:v "crop={w}:{w}:{0}:{h/4}" 0{path}')
        logger.debug(f'левый угол {0} {h/4}')
        logger.debug(f'{w} {h}')
                
    
    #os.system(f'ffmpeg -i {path} -filter:v "crop={w}:{w}:{0}:{h/4}" 0{path}')
    #os.system(f'ffmpeg -i {path} -filter:v "crop={w}:{w}:{0}:{h/4}" -c:v mp4 -vtag XVID -q:v 4 -c:a libmp3lame -q:a 4 0{path}')
#-c:v mpeg4 -vtag XVID -q:v 4 -c:a libmp3lame -q:a 4
#    -c:v libx264 -preset slow -crf 0
    #когда нибуди добавить статистику

    #a = os.system(f'du -h 0{path}')
    #logger.debug(a)

@dp.message_handler(content_types=['video'])
@logger.catch
async def handle_docs_photo(message):
    name = message.from_user.id
    #try:
    #firstName = message.first_name
    #logger.info(f'{firstName} ')
    file_id = message.video.file_id # Get file id
    file1 = await bot.get_file(file_id) # Get file path
    await bot.download_file(file1.file_path, f"{name}.mp4") # Download video and save output in file "video.mp4"
    #await message.video.download(f'{name}.mp4')
    test_movie(f'{name}.mp4')
    files = '/home/igor/python/igor2/venvcircle_bot/Circle_bot_telegram'
    await bot.send_video_note(name, video_note= InputFile(f'{files}/0{name}.mp4'))#,duration=2)#open(f'0{name}.mp4', 'rb'))#f'{name}.mp4')#f'{name}.png')
    #except Exception as e:
    logger.info('скачиваем файл {e}')

    os.system(f'rm {name}.mp4')
    os.system(f'rm 0{name}.mp4')

@dp.message_handler(content_types=ContentType.ANY)
@logger.catch
async def echo_message(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    
    try:
        message = msg.text.lower()
        user_id = msg.from_user.id
    except Exception as e:
        logger.info(f'любой формат {e}')

    await bot.send_message(msg.from_user.id, 'Пришлите ваше видео')
    #await state.set_state('firstMsg')



if __name__ == '__main__':
    art = text2art('circle bot', 'rand')
    print(art)
    #main()
    executor.start_polling(dp)
