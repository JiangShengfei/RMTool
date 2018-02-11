# -*- coding:utf-8 -*-

import os
import sys
import configparser
from linux import *
from network import *

curr_dir = sys.path[0]
os.chdir(curr_dir)

def linux(conf_file, msgOutput=False):

    conf = configparser.ConfigParser()
    conf.read(conf_file)
    remoteHost = conf.get('baseinfo', 'loginfile')
    hostOperate = conf.get('baseinfo', 'operate')
    if (msgOutput):
        filePrefix = conf.get('msgoutput', 'filepath')
    else:
        filePrefix = ''

    if ('cmd' == hostOperate):
        linux_cmd(remoteHost, conf.get('cmd', 'cmdfile'), filePrefix)
    elif ('upload' == hostOperate):
        localPath = conf.get('upload', 'local')
        remotePath = conf.get('upload', 'remote')
        linux_upload(remoteHost, localPath, remotePath)
    elif ('download' == hostOperate):
        localPath = conf.get('download', 'local')
        remotePath = conf.get('download', 'remote')
        linux_download(remoteHost, localPath, remotePath)
    else:
        print ("操作命令无法识别，请检查linux配置文件！！！")

def windows(conf_file, msgOutput=False):

    #conf = configparser.ConfigParser()
    #conf.read(conf)
    pass

def network(conf_file, msgOutput=False):
    conf = configparser.ConfigParser()
    conf.read(conf_file)

    if (msgOutput):
        filePrefix = conf.get('msgoutput', 'filepath')
    else:
        filePrefix = ''
    remoteHost = conf.get('baseinfo', 'loginfile')
    cmdfile = {}
    for key in conf.options('cmdfile'):
        cmdfile[key] = conf.get('cmdfile', key)

    netOperate = net(remoteHost, cmdfile, filePrefix)
    netOperate.exec_cmd()

def security(conf_file, msgOutput=False):
    pass




if __name__ == '__main__':

    mainconfig = 'config/mainconf.txt'

    conf = configparser.ConfigParser(allow_no_value=True)
    conf.read(mainconfig)

    system = conf.options('system')
    msgOutput = conf.get('msgoutput', 'msgtofile')
    if (msgOutput == 'on'):
        logType = True
    elif(msgOutput == 'off'):
        logType = False
    else:
        print ("配置文件错误，请再次检查msgfile配置。")
        sys.exit()

    print ("----------------------------------------")
    print ("请确认以下信息：")
    print ("选择的设备类型及配置文件如下：")
    count = 0
    for key in system:
        count += 1
        print ("%d、%s的配置文件为：%s" % (count, key, conf.get('configfile', key)))
    if logType:
        print ("远程操作返回信息处理方式为: 写入文件")
    else:
        print ("远程操作返回信息处理方式为: 输出至屏幕")

    input_str = ''
    while True:
        if (input_str == 'y'):
            break
        elif (input_str == 'n'):
            print ("程序已退出运行")
            sys.exit()
        input_str = input("请输入y或n,y为继续执行下一步，n退出程序: ")
        while input_str not in ('y', 'n'):
            input_str = input("请输入正确的字符y或n,回车：")

    print ("\n")
    
    for num in range(0,len(system)):
        if ('linux' == system[num]):
            print ('执行linux设备任务......\n')
            linux(conf.get('configfile', system[num]), logType)
        elif ('windows' == system[num]):
            print ('执行windows设备任务......\n')
        elif ('network' == system[num]):
            print ('执行网络设备任务......\n')
            network(conf.get('configfile', system[num]), logType)
        elif ('security' == system[num]):
            print ('执行安全设备任务......\n')
