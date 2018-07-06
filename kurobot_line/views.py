from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Create your views here.

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def index(request):
	if request.method == 'POST':
		signature = request.META['HTTP_X_LINE_SIGNATURE']
		body = request.body.decode('utf-8')
		try:
			events = parser.parse(body, signature)
		except InvalidSignatureError:
			print('InvalidSignatureError')
			return HttpResponseForbidden()
		except LineBotApiError:
			print('LineBotApiError')
			return HttpResponseBadRequest()
		for event in events:
			if isinstance(event, MessageEvent):
				if isinstance(event.message, TextMessage):
					translation = ''
					for word in event.message.text.split():
						query = parse.urlencode({"client": "gtx", "sl":"auto", "tl":"en", "dt": "t", "q": word})
						tword = json.loads(requests.get("https://translate.googleapis.com/translate_a/single?" + query).text)[0][0][0]
						translation += tword + ' '
					try:
						line_bot_api.reply_message(
							event.reply_token,
							TextSendMessage(text=translation[:-1])
							)
					except LineBotApiError as e:
						print(e.status_code)
						print(e.error.message)
						print(e.error.details)
		return HttpResponse()
	else:
		print('HttpResponseBadRequest')
		return HttpResponseBadRequest()