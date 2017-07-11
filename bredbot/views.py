# -*- coding: utf8 -*-

import json
import os, random, sys
import telepot
import logging
#from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import blogbootstrap.settings as settings
from .utils import help_text, make_text, get_picture, show_smile, tell_anecdote, tell_anecdote2

if not settings.DEBUG:
  import urllib3

  proxyname = "http://proxy.server:3128"
  telepot.api._pools = {
      'default': urllib3.ProxyManager(proxy_url=proxyname, num_pools=3, maxsize=10, retries=False, timeout=30),
  }
  telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxyname, num_pools=1, maxsize=1, retries=False, timeout=30))

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
#print('GET ME!',TelegramBot.getMe())
#TelegramBot.deleteWebhook()
#TelegramBot.setWebhook('https://cpuloader.pythonanywhere.com/bredbot/bot/{token}/'.format(token=settings.TELEGRAM_BOT_TOKEN))

logger = logging.getLogger('telegram.bot')

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            #sys.stderr.write('Invalid token')
            print('Invalid request body')
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': help_text,
            'help': help_text,
            'smile' : show_smile,
            'anec' : tell_anecdote2,
            u'анек' : tell_anecdote
        }

        raw = request.body.decode('utf-8')
        #print(raw)
        #logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            print('Invalid request body')
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
            except AttributeError:
                print('Attribute Error')
                pass
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
                print('TelegramError', err)
                pass
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)