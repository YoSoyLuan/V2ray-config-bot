
from pyrogram import (Client, filters,idle,errors)
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton)
import os
import json
import time
from random import choice
from config import *


# CLIENT BOT
bot = Client("V2ray-config",Api_id,Api_hash,bot_token=TOKEN)
bot.start()
BOTD = bot.get_me()
print("Iniciando Bot Config :","@"+BOTD.username) 


# Memory Data
Step = dict()
USERS = dict()
PRO = dict() 
SLP = dict()


# Defs Script
def RandomLineFile(path):
    with open(path,"r",encoding="utf-8") as f:
        return choice(f.read().splitlines())

def users(method="get",id=""):
    if method == "get":
        with open("users.json","r",encoding="utf-8") as f:
            return json.load(f)
    elif method == "add":
        data = users()
        with open("users.json","w",encoding="utf-8") as f:
            data["users"].append(int(id))
            json.dump(data,f,ensure_ascii=False)
            return True

def userpro(id=""):
    data = users()
    with open("users.json","w",encoding="utf-8") as f:
        data["pro"].append(int(id))
        json.dump(data,f,ensure_ascii=False)
        return True


# Telegram methods
async def check_join(user_id):
    global channels
    ls = []
    for i in channels:
        try:
            await bot.get_chat_member(i, user_id)
            continue
        except errors.exceptions.bad_request_400.UserNotParticipant:
            ls.append([InlineKeyboardButton("📢 Únete al canal {}".format(len(ls)+1),url="https://t.me/{}".format(i.replace("@", '')))])
            continue
        except errors.exceptions.bad_request_400.ChatAdminRequired:
            await bot.send_message(admins[0],"**⛔️ El bot no es admin del {} canal**".format(i))
            continue
        except errors.exceptions.bad_request_400.UsernameNotOccupied:
            await bot.send_message(admins[0],"**⛔️ No está registrado en el {} canal**".format(i))
            continue
        except Exception as e:
            print(i,user_id)
            print(e)
        finally:continue
    return ls


# Keyborad Panel
panelKEY = ReplyKeyboardMarkup(
        [
            ["📊 Status Bot","🗂 Recursos"],
            ["👥 Enviar a todos","👥 Reenviar a todos"],
            ["◀️back"],
        ],
        resize_keyboard=True
    )

backP = ReplyKeyboardMarkup(
        [
            ["◀️"],
        ],
        resize_keyboard=True
    )

home = ReplyKeyboardMarkup(
        [
            ["📡 Config Free","📡 Config Premium"],
            ["⬆️ Actualizar a Pro"],
            ["👤 Cuenta","📣 Owners"],
        ],
        resize_keyboard=True
    )

back = ReplyKeyboardMarkup(
        [
            ["◀️back"],
        ],
        resize_keyboard=True
    )

configKEY = ReplyKeyboardMarkup(
        [
            ["📡 NORMAL","📡 BASE64"],
            ["📡 CLASH","📡 CLASH.Meta"],
            ["◀️back"]
        ],
        resize_keyboard=True
    )

configsKEY = ReplyKeyboardMarkup(
        [
            ["🔗 VMESS","🔗 VLESS"],
            ["🔗 REALITY","🔗 TROJAN"],
            ["🔗 ShadowSocks"],
            ["◀️back"]
        ],
        resize_keyboard=True
    )

def memmber(link):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🤖 Abrir Bot 🤖",
                    url=link
                ),
            ],
        ]
    )


# Load Data form File
USERS = users()
PRO = USERS["pro"]


# Def Main Bot message
@bot.on_message(filters.private & filters.text)
async def Main(client, message):
    global Step,USERS,PRO,SLP
    from_id = message.from_user.id
    text = message.text
    message_id = message.id
    telegram_date = message.date
    if from_id not in Step:
        Step[from_id] = ""
    ck = await check_join(from_id)
    if ck != []:
        await bot.send_message(from_id,"**❤️ Únase primero a nuestro canal del patrocinador..\n\n✅ Luego reinicia el bot : /start**",reply_markup=InlineKeyboardMarkup(ck))
        return False
    if text.startswith("/start "):
        id = text.split(" ")[1]
        if id.isdigit():
            id = int(id)
            if id != from_id and from_id not in USERS["users"]:
                await bot.send_message(from_id,"**🤖 Bienvenido a V2ray Config Bot🤖\n\n🔰 Elige la opción que quieras :**",reply_markup=home,reply_to_message_id=message_id)
                USERS["users"].append(from_id)
                users("add",from_id)
                try:
                    await bot.send_message(id,"**🎉 Usuario [{0}](tg://user?id{0}) Me uní al bot con tu enlace.**".format(id))
                    PRO.append(id)
                    userpro(id)
                except:pass
                return False
            else:
                await bot.send_message(from_id,"**🤖 Bienvenido a V2ray Config Bot🤖\n\n🔰 Elige la opción que quieras :**",reply_markup=home,reply_to_message_id=message_id)
                USERS["users"].append(from_id)
                users("add",from_id)
                return False
        else:
            await bot.send_message(from_id,"**🤖 Bienvenido a V2ray Config Bot🤖\n\n🔰 Elige la opción que quieras :**",reply_markup=home,reply_to_message_id=message_id)
            USERS["users"].append(from_id)
            users("add",from_id)
            return False
    if from_id not in USERS["users"]:
        USERS["users"].append(from_id)
        users("add",from_id)
    if text in ['/start','◀️back']:
        Step[from_id] = "None"
        await bot.send_message(from_id,"**🤖 Bienvenido a V2ray Config Bot🤖\n\n🔰 Elige la opción que quieras :**",reply_markup=home,reply_to_message_id=message_id)
        return False
    elif text == "📡 Config Free":
        if from_id not in PRO:
            if from_id in SLP:
                if SLP[from_id] > int(time.time()):
                    await bot.send_message(from_id,"**⚠️ Actualice su cuenta haciendo clic en (⬆️ Actualizar a Pro) o espere {} segundos.**".format(SLP[from_id]-int(time.time())),reply_markup=back,reply_to_message_id=message_id)
                    return False
        Step[from_id] = "freeconfig2|"+"NORMAL"
        await bot.send_message(from_id,"**📡 Seleccione su tipo de configuración :**",reply_markup=configsKEY,reply_to_message_id=message_id)
        return False
    elif text == "📡 Config Premium":
        if from_id not in PRO:
            await bot.send_message(from_id,"**⚠️ Para utilizar esta sección, debes actualizar tu cuenta mediante (⬆️ Actualizar a Pro)**",reply_markup=back,reply_to_message_id=message_id)
            return False
        Step[from_id] = "fileconfig"
        await bot.send_message(from_id,"**📡 Select Your Config Subscription :**",reply_markup=configKEY,reply_to_message_id=message_id)    
        return False
    elif text == "⬆️ Actualizar a Pro":
        Step[from_id] = "upgrade"
        link = memmber("https://t.me/{}?start={}".format(BOTD.username,from_id))
        msg = await bot.send_message(from_id,"**⚡️ Bot de V2ray Gratis\n💯 Los mejores servicios de V2ray\n🚀 Máxima velocidad y sin interrupciones\n👤 Sin límite de número de usuarios.\n📱 Se puede conectar en Android, iOS, Windows, MacOS y Linux\n🧪 Cuenta completamente gratuita\n\nPara iniciar el Bot👇🏻**",reply_markup=link)    
        await msg.reply_text("**⭐️ Envíe el mensaje anterior a sus amigos para actualizar su cuenta.**",True,reply_markup=back)
        return False
    elif text == "👤 Cuenta":
        Step[from_id] = "account"
        if from_id in PRO:tp = "Pro"
        else:tp = "Free"
        await bot.send_message(from_id,"**🆔 User ID :** `{}`\n**👤 Tipo de cuenta :** `{}`\n**📅 Fecha :** `{}`\n\n**🤖 @{}**".format(from_id,tp,telegram_date,BOTD.username),reply_markup=back,reply_to_message_id=message_id)
        return False
    elif text == "📣 Owners":
        Step[from_id] = "spons"
        Tex = "💜 Canal :\n\n"
        for i in channels:
            Tex += "🏆 {}\n".format(i)
        await bot.send_message(from_id,"**{}\n\n\n**🤖 @{}**".format(Tex,BOTD.username),reply_markup=back,reply_to_message_id=message_id)
        return False
    elif Step[from_id] == "fileconfig":
        Step[from_id] = "fileconfig2|"+text.replace("🔗 ","")
        await bot.send_message(from_id,"**📡 Seleccione su tipo de configuración :**",reply_markup=configsKEY,reply_to_message_id=message_id)
        return False
    elif "freeconfig2|" in Step[from_id] and text in ["🔗 VMESS","🔗 VLESS","🔗 REALITY","🔗 TROJAN","🔗 ShadowSocks"]:
        SLP[from_id] = int(time.time()) + int(timefree)
        cnf = Step[from_id].split("|")[1].replace("📡 ", "").replace(".", "")
        typ = text.replace("🔗 ", "")
        if os.path.isfile("configs/"+typ+"/"+cnf+".txt"):
            con = RandomLineFile("configs/"+typ+"/"+cnf+".txt")
            await bot.send_message(from_id,"**📡 Config : (**`{}`**)\n🖥 Tipo : **`{}`\n📅**Fecha :** `{}`\n**⚠️ Las configuraciones están probadas y el bot solo es un editor... Cualquier error reportar a: \n\n@LuAnMontes12\n@xASUNA\n\n🤖 @{}**".format(con,typ,telegram_date,BOTD.username),reply_markup=back,reply_to_message_id=message_id)
        else:
            await bot.send_message(from_id,"**❌ Actualmente las configuraciones de V2ray no están disponibles para proporcionar, inténtelo nuevamente más tarde**",reply_markup=back,reply_to_message_id=message_id)
        Step[from_id] = "None"
        return False
    elif "fileconfig2|" in Step[from_id] and text in ["🔗 VMESS","🔗 VLESS","🔗 REALITY","🔗 TROJAN","🔗 ShadowSocks"]:
        cnf = Step[from_id].split("|")[1].replace("📡 ", "").replace(".", "")
        typ = text.replace("🔗 ", "")
        if os.path.isfile("configs/"+typ+"/"+cnf+".txt"):
            await bot.send_document(from_id,"configs/"+typ+"/"+cnf+".txt",caption="**📡 Subscripción :** `{}`\n**🖥 Tipo : **`{}`\n📅**Fecha :** `{}`\n**⚠️ Las configuraciones están probadas y el bot solo es un editor... Cualquier error reportar a: \n\n@LuAnMontes12\n@xASUNA\n\n🤖 @{}**".format(cnf,typ,telegram_date,BOTD.username),reply_markup=back,reply_to_message_id=message_id)
        else:
            await bot.send_message(from_id,"**❌ Actualmente las configuraciones de V2ray no están disponibles para proporcionar, inténtelo nuevamente más tarde**",reply_markup=back,reply_to_message_id=message_id)
        Step[from_id] = "None"
        return False
    elif text in ["/panel","Panel","panel","/Panel","◀️"] and from_id in admins:
        Step[from_id] = "panel"
        await bot.send_message(from_id,"**🌹 Bienvenido al panel de administración del Bot Config V2ray\n\n🔰 Elige la opción que quieras :**",reply_markup=panelKEY,reply_to_message_id=message_id)
        return False
    elif text == "📊 Status Bot" and from_id in admins:
        Step[from_id] = "StatusBot"
        msg = await bot.send_message(from_id,"**♻️ Espere por favor ...**",reply_markup=backP,reply_to_message_id=message_id)
        chn = ""
        for i in channels:
            try:mmb = await bot.get_chat_members_count(i)
            except:mmb = "Error"
            chn += "📢 {} : 👥 {}\n".format(i,mmb)
        await msg.delete()
        await bot.send_message(from_id,"**👤 Número de usuarios : {}\n⭐️ Número de usuarios Pro : {}\n💜 Canales conectados : {}\n\n{}**".format(len(USERS["users"]),len(PRO),len(channels),chn),reply_markup=backP,reply_to_message_id=message_id)
        return False
    elif text == "🗂 Recursos" and from_id in admins:
        Step[from_id] = "github"
        await bot.send_message(from_id,"**GitHub link : github.com/luan-03/V2ray-config-bot\n\n😉 No olvides darle me gusta❤️!**",reply_markup=backP,reply_to_message_id=message_id,disable_web_page_preview=True)
        return False
    elif text == "👥 Enviar a todos" and from_id in admins:
        Step[from_id] = "SendALL"
        await bot.send_message(from_id,"**✅ Envía tu mensaje :**",reply_markup=backP,reply_to_message_id=message_id)
        return False
    elif text == "👥 Reenviar a todos" and from_id in admins:
        Step[from_id] = "ForwardALL"
        await bot.send_message(from_id,"**✅ Reenvie su mensaje :**",reply_markup=backP,reply_to_message_id=message_id)
        return False
    elif Step[from_id] == "SendALL":
        Step[from_id] = "None"
        await bot.send_message(from_id,"**⚙️ Comience a enviar, ¡espere hasta el final!**",reply_markup=backP,reply_to_message_id=message_id)
        ok,bad = 0 , 0
        for i in users()["users"]:
            try:await message.copy(i);ok+=1;print("Send to ",i)
            except:bad+=1
        await bot.send_message(from_id,"**✅ {} ¡Mensajes enviados!\n❌ {} ¡Los mensajes fallaron!**".format(ok,bad),reply_markup=backP,reply_to_message_id=message_id)
        return False
    elif Step[from_id] == "ForwardALL":
        Step[from_id] = "None"
        await bot.send_message(from_id,"**⚙️ Comience a Reenviar, ¡espere hasta el final!**",reply_markup=backP,reply_to_message_id=message_id)
        ok,bad = 0 , 0
        for i in users()["users"]:
            try:await message.copy(i);ok+=1;print("Forward to ",i)
            except:bad+=1
        await bot.send_message(from_id,"**✅ {} ¡Mensajes enviados!\n❌ {} ¡Los mensajes fallaron!**".format(ok,bad),reply_markup=backP,reply_to_message_id=message_id)
        return False

            


idle()
bot.stop()
