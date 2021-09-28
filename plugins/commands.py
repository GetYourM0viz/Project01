#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @REQUEST_M0viz


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from script import script


@Client.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    try:
        await message.reply_text(
            text=script.START_MSG.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("HELP", callback_data="help_data"),
                        InlineKeyboardButton("ABOUT", callback_data="about_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "🖤JOIN SUPPORT GROUP🖤", url="https://t.me/R_Mvz")
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        )
    except:
        pass

@Client.on_message(filters.command(["help"]) & filters.private)
async def help(client, message):
    try:
        await message.reply_text(
            text=script.HELP_MSG,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("BACK", callback_data="start_data"),
                        InlineKeyboardButton("ABOUT", callback_data="about_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "💕DONATE US 💕", url="https://t.me/Harshsoni_08")
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        )
    except:
        pass

@Client.on_message(filters.command(["about"]) & filters.private)
async def about(client, message):
    try:
        await message.reply_text(
            text=script.ABOUT_MSG,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("BACK", callback_data="help_data"),
                        InlineKeyboardButton("START", callback_data="start_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "SHARE OUR GROUP 🖤🤙", url="http://t.me/share/url?url=Hey%20There%E2%9D%A4%EF%B8%8F%2C%0A%20%0A%20I%20Found%20A%20Really%20Awesome%20Group%20%20For%20Searching%20Movies%20Hope%20You%20will%20Join%20This%20Group%20Too😁😁👍%E2%9D%A4%EF%B8%8F%E2%9D%A4%EF%B8%8F%E2%9D%A4%EF%B8%8F%0A%20%0A%20Group%20Sharing%20Username%20Link%20%3A-%20%40REQUEST_M0viz")
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        )
    except:
        pass
