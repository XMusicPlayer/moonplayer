﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

import moonplayer
import re
from moonplayer_utils import parse_flvcd_page

hosts = ('www.acfun.tv',)

def parse(url, options):
    origin_url = url
    url = 'http://www.flvcd.com/parse.php?go=1&kw=' + origin_url
    if options & moonplayer.OPT_QL_SUPER:
        url += '&format=super'
    elif options & moonplayer.OPT_QL_HIGH:
        url += '&format=high'
    moonplayer.get_url(url, parse_cb, (options, origin_url))
    
def parse_cb(page, data):
    (options, url) = data
    result = parse_flvcd_page(page, None)
    if len(result) == 0:
        moonplayer.warn("Cannot parse acfun's video!")
    elif options & moonplayer.OPT_DOWNLOAD and len(result) > 2:
        moonplayer.download(result, result[0])
    else:
        moonplayer.get_url(url, parse_danmaku_cb, (options, result))
        
cid_re = re.compile(r'''data-vid=['"](\d+)['"]''')
name_re = re.compile(r'''data-title=['"](.+?)['"]''')
def parse_danmaku_cb(page, data):
    (options, result) = data
    match = name_re.search(page)
    if match:
        result[0] = match.group(1) + ".flv"
        
    match = cid_re.search(page)
    if match:
        danmaku = 'http://danmu.aixifan.com/V2/' + match.group(1)
        if options & moonplayer.OPT_DOWNLOAD:
            moonplayer.download_with_danmaku(result, danmaku)
        else:
            moonplayer.play(result, danmaku)
    else:
        moonplayer.warn('无法获取弹幕！')
        if options & moonplayer.OPT_DOWNLOAD:
            moonplayer.download(result)
        else:
            moonplayer.play(result)
