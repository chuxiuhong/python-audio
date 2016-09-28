# coding=utf-8
import re
import requests

p = re.compile(r'class="fl ei"/><div class="et">')
text = requests.get('http://library.applinzi.com').text
# print text
print p.findall(text)
'''
for i in range(1140310503,1140310730):
    url = 'http://'+i.__str__()+'.applinzi.com'
    text = requests.get(url).text
    if len(p.findall(text)) == 0:
        print i,'found!!!!!!!!!'
'''
