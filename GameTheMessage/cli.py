#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--config', '-c', help='配置文件路径。', default=r"config\GameTheMessage-config.ini")
def start(config: str):
    """主持一个对战"""
    from GameTheMessage.lobby.server import create_lobby
    create_lobby(config)


@cli.command()
@click.argument('host', default='127.0.0.1')
@click.argument('port', default='4444')
@click.option('--config', '-c', help='配置文件路径。', default=r"config\GameTheMessage-config.ini")
def join(host, port, config):
    """加入一个对战"""
    from GameTheMessage.lobby.client import join_lobby
    cf = configparser.ConfigParser(allow_no_value=True)
    cf.read(config)
    cf.set('HOST', 'SOCKET_HOST', host)
    cf.set('HOST', 'SOCK_PORT', port)
    join_lobby(cf)


@cli.command()
def setting():
    """编辑配置文件"""
    pass


if __name__ == "__main__":
    cli()
