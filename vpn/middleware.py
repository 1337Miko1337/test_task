import re

from django.shortcuts import redirect
from .urls import *
from bs4 import BeautifulSoup


class ProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/addsite/'):  # Ви повинні встановити шлях до вашого проксі вигляду
            main_url = re.findall('addsite/(https?://[\w.-]+)', request.path, re.DOTALL)
            soup = BeautifulSoup(response.content, 'html.parser')
            for tag in soup.find_all('a', href=True):
                if re.findall('(^//)', tag['href']):
                    tag['href'] = f'/addsite/https:/{tag["href"][1:]}'
                elif main_url != [] and main_url[0]+'/' in tag['href']:
                    tag['href'] = f'http://127.0.0.1:8000/addsite/{tag["href"]}'
            for tag in soup.find_all(src=True):
                if re.findall('(^//[\w.-]+)', tag['src'], re.DOTALL):
                    tag['src'] = f'https:/{tag["src"][1:]}'
                elif re.findall('(^/)', tag['src'], re.DOTALL):
                    tag['src'] = f'{main_url[0]}{tag["src"]}'
                elif re.findall('(https?://[\w.-]+)', tag['src']) == []:
                    tag['src'] = f'{main_url[0]}/{tag["src"][1:]}'
            response.content = soup.prettify(formatter='html')

        return response
