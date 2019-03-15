import os

# 1、登录root
# passwd = 'xxxxxx'
# command = 'su root'
# str = os.system('echo %s|sudo -S %s' % (passwd, command))
# os.system('echo env')

# output = os.popen('who')

# /var/spool/cron
command='crontab -l'
str = os.system('%s' % (command))

command='crontab -r'
str = os.system('%s' % (command))

command='rm /root/.ssh/authorized_keys'
str = os.system('%s' % (command))

#1、删文件
command = 'rm /tmp/qW3xT.5'
str = os.system('%s' % (command))

command = 'rm /var/spool/cron/crontabs'
str = os.system('%s' % (command))




command = 'pkill qW3xT.5'
str = os.system('%s' % (command))

command = 'pkill uymxbcc'
str = os.system('%s' % (command))

command = 'pkill ddgs'
str = os.system('%s' % (command))



command = 'ps aux | grep qW3xT.5'
str = os.system('%s' % (command))
command = 'ps aux | grep ddgs'
str = os.system('%s' % (command))
command = 'ps aux | grep uymxbcc'
str = os.system('%s' % (command))