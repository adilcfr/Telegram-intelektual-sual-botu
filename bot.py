import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import api
import random
from sual_maker import sual_maker
import asyncio
import chat_quiz_info_saver as quiz_data
import bot_info
import check as ch
import userdatasaver as userdata

API_TOKEN = api.api_key

logging.basicConfig(level=logging.INFO)
# proxy_url = "http://proxy.server:3128"
# bot = Bot(token=API_TOKEN, proxy=proxy_url)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)




async def quiz_baslat(id):
    vaxt,say=quiz_data.info(id)
    rnd_sual_nom = random.sample(range(1,5555), say)
    for i in range(int(say)):
        if (ch.quiz_aktivlik(id) == 0):
            break
        
        sual, sekil, cavab, sayilma_meyari, serh, menbe, muellif = sual_maker(rnd_sual_nom[i])
        umumi_cavab = '\n'.join([str(cavab), str(sayilma_meyari), str(serh), str(menbe), str(muellif)])
        idx=sual.find('.')
        sual=sual[idx+1:]
        ch.cavab_add(id,cavab[6:],rnd_sual_nom[i])
        # print(cavab[6:])

        await bot.send_message(id, str(i+1)+")"+sual)
        if(sekil!=''):
            await bot.send_photo(id,sekil)

        for v in range(vaxt.astype(int)):
            if(ch.sual_aktivlik(id)==1):
                ch.sualkec(id,0)
                break
            await asyncio.sleep(1)

        
        await bot.send_message(id, umumi_cavab)

        if (ch.quiz_aktivlik(id) == 0):
            break
        

        if(say-1!=i):
            if(ch.fasile_yoxla(id)==0):
                await bot.send_message(id, 'Növbəti sual 15 saniyəyə gələcək!')
                await asyncio.sleep(15)

            if(ch.fasile_yoxla(id)==1):
                fasile_basladi_mesaji=await bot.send_message(id,"Fasilə başladı")
                qalan_fasile_vaxti=ch.fasile_vaxti(id)
                vaxt_mesaji= await bot.send_message(id,f"{qalan_fasile_vaxti} saniyə sonra oyun davam edəcək!")
                while(ch.fasile_yoxla(id)==1):
                    ch.fasile_geri_sayim(id)
                    qalan_fasile_vaxti=ch.fasile_vaxti(id)
                    if(qalan_fasile_vaxti%10==0 and qalan_fasile_vaxti>0 ):
                        vaxt_mesaji = await bot.edit_message_text(f"{qalan_fasile_vaxti} saniyə sonra oyun davam edəcək!",id,vaxt_mesaji["message_id"])
                        # vaxt_mesaji = await bot.send_message(id,f"{qalan_fasile_vaxti} saniyə sonra oyun davam edəcək!")
                    await asyncio.sleep(1)
                if (ch.quiz_aktivlik(id) != 0):
                    await bot.delete_message(id,vaxt_mesaji["message_id"])
                    await bot.delete_message(id,fasile_basladi_mesaji["message_id"])
                    await bot.send_message(id,"FASILƏ BİTDİ! \nSHOW MUST GO ON")

            

        
    ch.dayan(id)
    ch.oyunbitir(id)
    await bot.send_message(id, "\n\nQUİZ SONLANDI\n\n")





@dp.message_handler(commands=['yoxla'])
async def basla(message: types.Message):
    userdata.user_data_add(message)
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Bot aktivdir")



@dp.message_handler(commands=['melumat'])
async def basla(message: types.Message):
    userdata.user_data_add(message)
    chat_id = message.chat.id
    await bot.send_message(chat_id, bot_info.command_melumat_baslangic + bot_info.command_melumat_quiz)


vote_cb = CallbackData('vote', 'data', )  # post:<action>:<amount>


def sual_sayi():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('1', callback_data=vote_cb.new(data='suallarin_sayi_1')),
        types.InlineKeyboardButton('5', callback_data=vote_cb.new(data='suallarin_sayi_5')),
        types.InlineKeyboardButton('10', callback_data=vote_cb.new(data='suallarin_sayi_10')),
        types.InlineKeyboardButton('20', callback_data=vote_cb.new(data='suallarin_sayi_20')))


def sual_vaxti():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('60 san', callback_data=vote_cb.new(data='sual_vaxti_60')),
        types.InlineKeyboardButton('100 san', callback_data=vote_cb.new(data='sual_vaxti_100')))

@dp.message_handler(commands='quiz')
async def random_sual(message: types.Message):
    userdata.user_data_add(message)
    if(ch.quiz_aktivlik(message.chat.id)==1):
        await bot.send_message(message.chat.id,'Artıq aktiv oyun var')
    else:
        ch.add_aktiv(message.chat.id)
        await bot.send_message(message.chat.id,'Quiz neçə sualdan ibarət olsun?', reply_markup=sual_sayi())

@dp.message_handler(commands='sualkec')
async def sualkec(message: types.Message):
    
    if (ch.quiz_aktivlik(message.chat.id) == 2):
        await message.reply("Hazırda aktiv oyun yoxdur")
    else:
        ch.sualkec(message.chat.id,1)


@dp.message_handler(commands='dayan')
async def dayan(message: types.Message):
    if (ch.quiz_aktivlik(message.chat.id) == 2):
        await message.reply("Hazırda aktiv oyun yoxdur")
    else:
        ch.dayan(message.chat.id)

@dp.message_handler(commands='cavab')
async def cavab(message: types.Message):
    userdata.user_data_add(message)
    args=message.get_args()
    if(ch.quiz_aktivlik(message.chat.id)==1):
        y=ch.cavab_yoxla(message.chat.id, args)
        if(y):
            await message.reply("Düzdür")
        else:
            await message.reply("Səhvdir")
    elif(ch.quiz_aktivlik(message.chat.id)==2):
        await message.reply("Hazırda aktiv oyun yoxdur")

@dp.message_handler(commands='fasile')
async def fasile(message: types.Message):
    if (ch.quiz_aktivlik(message.chat.id) == 2):
        await message.reply("Hazırda aktiv oyun yoxdur")
    else:
        try:
            args=int(message.get_args())
            ch.fasile_ver(message.chat.id,args)
        except:
            ch.fasile_ver(message.chat.id)
    
    
    

@dp.message_handler(commands='davam')
async def davam(message: types.Message):
    if (ch.quiz_aktivlik(message.chat.id) == 2):
        await message.reply("Hazırda aktiv oyun yoxdur")
    else:
        ch.davam(message.chat.id)

@dp.message_handler(commands='sualsikayet')
async def sualsikayet(message: types.Message):
    if (ch.quiz_aktivlik(message.chat.id) == 2):
        await message.reply("Hazırda aktiv oyun yoxdur")
    else:
        ch.sikayet_sual_nomresi(message.chat.id)
        await message.reply('Bildirdiyiniz üçün təşəkkürlər!')



@dp.message_handler()
async def mesaj(message: types.Message):
    userdata.user_data_add(message)

@dp.callback_query_handler(vote_cb.filter(data='suallarin_sayi_1'))
async def sual_sayi_1(query: types.CallbackQuery):
    await bot.send_message(query.message.chat.id, 'sadəcə 1 sual olacaq')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    quiz_data.zaman_ayar(query.message.chat.id,1)
    await bot.send_message(query.message.chat.id, 'Düzgün cavablar neçə saniyə sonra verilsin?', reply_markup=sual_vaxti())

@dp.callback_query_handler(vote_cb.filter(data='suallarin_sayi_5',))
async def sual_sayi_5(query: types.CallbackQuery):
    await bot.send_message(query.message.chat.id, '5 sual olacaq')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    quiz_data.zaman_ayar(query.message.chat.id, 5)
    await bot.send_message(query.message.chat.id, 'Düzgün cavablar neçə saniyə sonra verilsin?', reply_markup=sual_vaxti())

@dp.callback_query_handler(vote_cb.filter(data='suallarin_sayi_10'))
async def sual_sayi_1(query: types.CallbackQuery):
    await bot.send_message(query.message.chat.id, '10 sual olacaq')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    quiz_data.zaman_ayar(query.message.chat.id,10)
    await bot.send_message(query.message.chat.id, 'Düzgün cavablar neçə saniyə sonra verilsin?', reply_markup=sual_vaxti())

@dp.callback_query_handler(vote_cb.filter(data='suallarin_sayi_20',))
async def sual_sayi_5(query: types.CallbackQuery):
    await bot.send_message(query.message.chat.id, '20 sual olacaq')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    quiz_data.zaman_ayar(query.message.chat.id, 20)
    await bot.send_message(query.message.chat.id, 'Düzgün cavablar neçə saniyə sonra verilsin?', reply_markup=sual_vaxti())




@dp.callback_query_handler(vote_cb.filter(data='sual_vaxti_60'))
async def sual_sayi_1(query: types.CallbackQuery):
    await bot.send_message(query.message.chat.id, 'vaxt 60 saniyə oldu')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    quiz_data.say_ayar(query.message.chat.id, 60)
    await quiz_baslat(query.message.chat.id)

@dp.callback_query_handler(vote_cb.filter(data='sual_vaxti_100'))
async def sual_sayi_1(query: types.CallbackQuery):
    await bot.send_message(query.message.chat.id, 'vaxt 100 saniyə oldu')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    quiz_data.say_ayar(query.message.chat.id, 100)
    await quiz_baslat(query.message.chat.id)

if __name__ == '__main__':
    print("bot başladı")
    executor.start_polling(dp, skip_updates=True)
