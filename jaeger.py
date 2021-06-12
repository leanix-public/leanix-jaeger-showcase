import click
import json
import requests
import datetime
import time


@click.group()
def cli():
    """Command Line Program for developing CNS (e.g. processors)"""
    pass


@cli.command('get-dependencies', help="")
def cli_get_dependencies():

    now = time.time_ns() // 1000000
    now_iso = datetime.datetime.fromtimestamp(now / 1000).strftime('%Y-%m-%dT%H:%M:%S.000000Z')
    res = requests.get('http://localhost:16686/api/dependencies?endTs=1623504409960&lookback=3600000')

    microservices = set()
    content = []
    for entry in res.json()['data']:
        microservices.add(entry['child'])
        microservices.add(entry['parent'])
        content.append({'id': entry['parent'] + '###' + entry['child'],
                        'type': 'API',
                        'data': {
                            'name': entry['parent'] + ' - ' + entry['child'],
                            'provider': entry['parent'],
                            'consumers': [entry['child']],
                            'time': now_iso,
                            'count': entry['callCount']}})
    for ms in microservices:
        content.append({'id': ms,
                        'type': 'Microservice',
                        'data': {}})

    print(json.dumps({
        "connectorType": "leanix-showcase",
        "connectorId": "jaeger",
        "connectorVersion": "1.0.0",
        "lxVersion": "1.0.0",
        "processingDirection": "inbound",
        "processingMode": "partial",
        "customFields": {},
        "content": content
    }, indent=2))


def main():
    cli()


if __name__ == '__main__':
    cli()
