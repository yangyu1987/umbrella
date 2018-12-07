from django import setup
import os

# 加载配置

os.environ.setdefault('DJAGNO_SETTINGS_MODULE','server.settings')
setup()