# -*- coding:utf-8 -*-

import time
import readtext
import my_ssh
import my_telnet
#import myTools

SUCC_NUM = 0
FAIL_NUM = 0

class net_init:
    def __init__(self, hostInfo, msgOutput):
        self.featureCmd = 'enable'
        self.descriptions = hostInfo[0]
        self.dev_type = hostInfo[1]
        self.serv_type = hostInfo[2]
        self.ip = hostInfo[3]
        self.port = int(hostInfo[4])
        self.userName = hostInfo[5]
        self.password = hostInfo[6]
        if (len(hostInfo) == 8):
            self.supassword = hostInfo[7]
        else:
            self.supassword = ''
        self.msgOutput = msgOutput

class net_cisco(net_init):
    def __init__(self, hostInfo, msgOutput):
        net_init.__init__(self, hostInfo, msgOutput)
        self.featureCmd = 'enable'

    def ssh(self, command):
        global SUCC_NUM
        global FAIL_NUM
        command = readtext.readcommands(command)
        self.st = my_ssh.netSsh(self.ip, self.port, self.userName, self.password)
        if self.st.login_status:
            SUCC_NUM += 1
            print ("正在处理主机：%s" % self.ip)
            if (self.supassword != ''):
                self.st.exec_su(self.featureCmd, self.supassword)
                if (self.msgOutput != ''):
                    #输出至日志文件
                    fileName = self.msgOutput + self.descriptions + '_' + self.ip + '_' + time.strftime("%m%d%H%M%S") + '.txt'
                    msg2file = readtext.std2file(fileName)
                    message = self.st.exec_cmd(command)
                    if msg2file.open_status:
                        msg2file.msg_write(message)
                    print ("执行结果写至文件：%s" % fileName)
                else:
                    message = self.st.exec_cmd(command)
                    print (message)

            else:
                if (self.msgOutput != ''):
                    #输出至日志文件
                    fileName = self.msgOutput + self.descriptions + '_' + self.ip + '_' + time.strftime("%m%d%H%M%S") + '.txt'
                    msg2file = readtext.std2file(fileName)
                    message = self.st.exec_cmd(command)
                    if msg2file.open_status:
                        msg2file.msg_write(message)
                    print ("执行结果写至文件：%s" % fileName)
                else:
                    message = self.st.exec_cmd(command)
                    print (message)
        else:
            FAIL_NUM += 1

    def telnet(self, command):
        global SUCC_NUM
        global FAIL_NUM
        command = readtext.readcommands(command)
        self.tn = my_telnet.netTelnet(self.ip, self.port, self.userName, self.password)
        if self.tn.login_status:
            SUCC_NUM += 1
            print ("正在处理主机：%s" % self.ip)
            if (self.supassword != ''):
                self.tn.exec_su(self.featureCmd, self.supassword) #输入enable密码
                if (self.msgOutput != ''):
                    #输出至日志文件
                    fileName = self.msgOutput + self.descriptions + '_' + self.ip + '_' + time.strftime("%m%d%H%M%S") + '.txt'
                    msg2file = readtext.std2file(fileName)
                    for cmd in command:
                        message = self.tn.exec_cmd(cmd)
                        if msg2file.open_status:
                            msg2file.msg_write(message)
                    print ("执行结果写至文件：%s" % fileName)
                else:
                    for cmd in command:
                        message = self.tn.exec_cmd(cmd)
                        print (message)

            else:
                if (self.msgOutput != ''):
                    #输出至日志文件
                    fileName = self.msgOutput + self.descriptions + '_' + self.ip + '_' + time.strftime("%m%d%H%M%S") + '.txt'
                    msg2file = readtext.std2file(fileName)
                    for cmd in command:
                        message = self.tn.exec_cmd(cmd)
                        if msg2file.open_status:
                            msg2file.msg_write(message)
                    print ("执行结果写至文件：%s" % fileName)
                else:
                    for cmd in command:
                        message = self.tn.exec_cmd(cmd)
                        print (message)
        else:
            FAIL_NUM += 1

    def __str__(self):
        return ("思科产品!!!")

class net_zte(net_cisco):
    def __str__(self):
        return ("中兴产品!!!")

class net_ruijie(net_cisco):
    def __str__(self):
        return ("锐捷产品!!!")

class net_huawei(net_cisco):
    def __init__(self, hostInfo, msgOutput):
        net_cisco.__init__(self, hostInfo, msgOutput)
        self.featureCmd = 'super'

    def __str__(self):
        return ("华为产品!!!")

class net_h3c(net_huawei):
    def __str__(self):
        return ("H3C产品!!!")

class net:
    def __init__(self, remote_dev, cmdfile, msgOutput=False):
            
        self.remoteHost = readtext.readremoteinfo(remote_dev)
        self.cmdfile = cmdfile
        self.msgOutput = msgOutput

    def exec_cmd(self):
        global SUCC_NUM
        global FAIL_NUM
        for host in self.remoteHost:
            if (host[2] == 'ssh'): #根据远程主机的服务类型采用不不同的协议登录
                if (host[1] == 'cisco'):
                    cisco_st = net_cisco(host, self.msgOutput)
                    cisco_st.ssh(self.cmdfile[host[1]])
                elif (host[1] == 'huawei'):
                    huawei_st = net_huawei(host, self.msgOutput)
                    huawei_st.ssh(self.cmdfile[host[1]])
                else:
                    print ("本程序不支持的设备类型：%s !!!" % host[1])
                    
            elif (host[2] == 'telnet'):
                if (host[1] == 'cisco'):
                    cisco_tn = net_cisco(host, self.msgOutput)
                    cisco_tn.telnet(self.cmdfile[host[1]])
                elif (host[1] == 'huawei'):
                    huawei_tn = net_huawei(host, self.msgOutput)
                    huawei_tn.telnet(self.cmdfile[host[1]])
                else:
                    print ("本程序不支持的设备类型：%s !!!" % host[1])

            else:
                print ("本程序不支持的服务类型：%s !!!" % host[2])

        print ("-----------------------------------------------\n")
        print ("所有网络设备命令执行完成：")
        print ("操作执行主机总数为：%d台;" % len(self.remoteHost))
        print ("本次任务执行中成功主机%s台，失败主机%s台;" % (SUCC_NUM, FAIL_NUM))
