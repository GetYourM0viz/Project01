#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import re
import pyrogram

from pyrogram import (
    filters,
    Client
)

from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Message,
    CallbackQuery
)

from bot import Bot
from script import script
from database.mdb import searchquery
from plugins.channel import deleteallfilters
from config import AUTH_USERS

BUTTONS = {}
 
@Client.on_message(filters.group & filters.text)
async def filter(client: Bot, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if 2 < len(message.text) < 50:    
        btn = []

        group_id = message.chat.id
        name = message.text

        filenames, links = await searchquery(group_id, name)
        if filenames and links:
            for filename, link in zip(filenames, links):
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",url=f"{link}")]
                )
        else:
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🦾RESULTS 1/1",callback_data="pages")]
            )
            await message.reply_text(
                f"<b>CHECK YOUR QUERY:- {message.text}    TEAM :- @R_Mvz </b>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="⚡NEXT PAGE⚡👉",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🦾RESULTS 1/{data['total']}",callback_data="pages")]
        )

        await message.reply_text(
                f"<b>💕👇CHECK FOR YOUR REQUEST👇💕{message.text}</b>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )    


@Client.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    clicked = query.from_user.id
    typed = query.message.reply_to_message.from_user.id

    if (clicked == typed) or (clicked in AUTH_USERS):

        if query.data.startswith("next"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("👈⚡GO BACK⚡", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🦾RESULTS {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("👈⚡GO BACK⚡", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("⚡NEXT PAGE⚡👉", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🦾RESULTS {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⚡NEXT PAGE⚡👉", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🦾RESULTS {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("👈⚡GO BACK⚡", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("⚡NEXT PAGE⚡👉", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🦾RESULTS {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data == "pages":
            await query.answer()


        elif query.data == "start_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("HELP", callback_data="help_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("⭕️🔥JOIN OUR MAIN GROUP🔥⭕️", url="https://t.me/REQUEST_M0viz")]
            ])

            await query.message.edit_text(
                script.START_MSG.format(query.from_user.mention),
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "help_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="start_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("💕DONATE US💕", url="https://t.me/harshsoni_08")]
            ])

            await query.message.edit_text(
                script.HELP_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "about_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("START", callback_data="start_data")],
                [InlineKeyboardButton("SHARE OUR GROUP💕💕🤙", url="http://t.me/share/url?url=Hey%20There%E2%9D%A4%EF%B8%8F%2C%0A%20%0A%20I%20Found%20A%20Really%20Awesome%20Group%20%20For%20Searching%20Movies%20Hope%20You%20will%20Join%20This%20Group%20Too😁😁👍%E2%9D%A4%EF%B8%8F%E2%9D%A4%EF%B8%8F%E2%9D%A4%EF%B8%8F%0A%20%0A%20Group%20Sharing%20Username%20Link%20%3A-%20%40REQUEST_M0viz")]
            ])

            await query.message.edit_text(
                script.ABOUT_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "delallconfirm":
            await query.message.delete()
            await deleteallfilters(client, query.message)
        
        elif query.data == "delallcancel":
            await query.message.reply_to_message.delete()
            await query.message.delete()

    else:
        await query.answer("Thats not for you!!",show_alert=True)


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]  
