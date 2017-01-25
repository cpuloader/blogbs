# -*- coding: utf8 -*-

import json
import os, random
import telepot
#from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#from django.conf import settings

import blogbootstrap.settings as settings
from .utils import help_text, make_text, get_picture, show_smile

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
            'smile' : show_smile,
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
                    ans_words = cmd.split()
                else:
                    func = None
                    ans_words = []
            except AttributeError: pass
            try:
                if func:
                    TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
                else:
                    if chat_id:
                        TelegramBot.sendMessage(chat_id, make_text(ans_words=ans_words))
                        '''
                        filepath = get_picture()
                        file = open(filepath, 'rb')
                        TelegramBot.sendPhoto(chat_id, file)
                        file.close()
                        try:
                            os.remove(filepath)
                            print('file deleted successfully')
                        except EnvironmentError:
                            print('file error!')
                            pass
                        '''
            except telepot.exception.TelegramError as err:
                print(err)
                pass
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)