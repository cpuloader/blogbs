# -*- coding: utf8 -*-

import json
import random
import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#from django.conf import settings

import blogbootstrap.settings as settings
from .utils import help_text, make_text

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

#def _display_help():
#    return render_to_string('help.md')

#def _display_planetpy_feed():
#    return render_to_string('feed.md', {'items': parse_planetpy_rss()})


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': help_text,
            'help': help_text,
        }

        raw = request.body.decode('utf-8')
        #logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            try:
                chat_id = payload['message']['chat']['id']
                cmd = payload['message'].get('text')
            except KeyError:
                chat_id = None
                cmd = None
            try:
                if cmd:
                    func = commands.get(cmd.split()[0].lower())
                    ans_word = random.choice(cmd.split()).lower()
                    if not ans_word.isalpha():
                        ans_word = None
                else:
                    func = None
            except AttributeError: pass
            if func:
                try:
                    TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
                except telepot.exception.BotWasBlockedError: pass
            else:
                if chat_id:
                    try:
                        TelegramBot.sendMessage(chat_id, make_text(ans_word=ans_word))
                    except telepot.exception.BotWasBlockedError: pass
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)