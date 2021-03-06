#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>GitHub Notifications</bitbar.title>
# <bitbar.version>v2.0.0</bitbar.version>
# <bitbar.author>Keith Cirkel, John Flesch</bitbar.author>
# <bitbar.author.github>flesch</bitbar.author.github>
# <bitbar.desc>GitHub (and GitHub:Enterprise) notifications in your menu bar!</bitbar.desc>
# <bitbar.image>https://cloud.githubusercontent.com/assets/13259/12300782/9f1f5ba8-b9e2-11e5-8e67-e59966aace9a.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>

import json
import urllib2
from os.path import (join, dirname, abspath)
import re

print 'GH'
# GitHub.com
github_api_key = str()
path_to_token = join(dirname(dirname( abspath(__file__))), 'github_token.txt')

with open(path_to_token, 'r') as f:
    github_api_key = f.read().strip()

active = '#4078C0'
inactive = '#7d7d7d'

def get_notifications( api_key, api_url = 'https://api.github.com' ):
    if len( api_key ) == 40:
        try:
            request = urllib2.Request( api_url + '/notifications', headers = { 'Authorization': 'token ' + api_key } )
            response = urllib2.urlopen( request )
            notifications = json.load( response )
            return map(format_notification, notifications)
        except Exception as e:
            return []
    else:
        return []

def format_notification( notification ):
    title = notification['subject']['title']
    repo = notification['repository']['full_name']
    url = re.sub( 'api\.|api/v3/|repos/', '', notification['subject']['url'] )
    url = re.sub( '(pull|commit)s', ur'\1', url )
    return ( '%s: %s | length=90 refresh=true href=%s' % ( repo, title, url ) ).encode( 'utf-8' )

def plural( word, n ):
    return str(n) + ' ' + (word + 's' if n > 1 else word)

is_github_defined = len( github_api_key ) == 40

github_notifications = get_notifications( github_api_key ) if is_github_defined else []
has_notifications = len( github_notifications )

color = active if has_notifications else inactive

print ( u'\u25CF | color=' + color ).encode( 'utf-8' )
print '---'


if is_github_defined:
    if len( github_notifications ):
        print ( u'GitHub \u2014 %s | color=%s href=https://github.com/notifications' % ( plural( 'notification', len( github_notifications ) ), active ) ).encode( 'utf-8' )
        print '\n'.join( github_notifications )
    else:
        print ( u'GitHub \u2014 No new notifications | color=%s' % inactive ).encode( 'utf-8' )
