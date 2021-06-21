import configparser
import os

def config():
    config = configparser.ConfigParser()
    # config.read('config.ini')
    config.read('/Users/weichenho/Desktop/config.ini')
    # print(os.getcwd())
    return config

if __name__ == '__main__':
    config()
