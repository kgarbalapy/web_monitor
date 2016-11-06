import logging

from django.shortcuts import render

import kronos
import requests

from web_monitor.settings import LOGGING, CRON_FORMAT

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def get_sites_list():
    with open('sites_list.txt') as file:
        for line in file:
            try:
                url, pattern = line.split(' ', 1)
            except ValueError:
                url, pattern = line, ''
                logger.info('no pattern for {url}'.format(url=url))
            yield url, pattern.rstrip()


def get_web_data(request):
    result, total_time = get_requests_result()
    return render(
        request, 'index.html', {
            'result': result, 'total_time': total_time})


def get_requests_result():
    result = list()
    total_time = float()
    for url, pattern in get_sites_list():
        try:
            request = requests.get(url)
            request.matched = False if request.content.find(str.encode(pattern)) == -1 else True
            request.response_time = request.elapsed.total_seconds()
            total_time += request.response_time
        except requests.ConnectionError:
            request = requests
            request.url = url
            request.status_code = ''
            request.reason = 'Website Not Found'
            request.matched = None
            request.response_time = 0
        finally:
            request.pattern = pattern
            result.append(request)
            logger.info(
                'url: {0}, pattern: {1}, matched: {2}, status_code: {3}, response_time[sec]: {4}' .format(
                    request.url,
                    request.pattern,
                    request.matched,
                    request.status_code,
                    request.response_time))
    logger.info('total time {0}'.format(total_time))
    return result, total_time


@kronos.register(CRON_FORMAT)
def run_cron():
    get_requests_result()
