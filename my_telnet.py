# -*- coding:utf-8 -*-

import time
import telnetlib

class baseTelnet:
    login_status = True
    def __init__(self, ip, port, userName, password, tn=telnetlib.Telnet()):
        self.tn = tn
        self.ip = ip
        self.port = port
        self.userName = userName
        self.password = password
        
class netTelnet(baseTelnet):
    def __init__(self, ip, port, userName, password):
        baseTelnet.__init__(self, ip, port, userName, password)
        try:
            self.tn.open(self.ip, self.port)
        except:
            self.login_status = False
            print ("主机%sTelnet认证失败，请检查远程主机的登录信息及主机在线情况。" % self.ip)
        else:
            try:
                userName = (self.userName + '\n').encode('utf-8')
                password = (self.password + '\n').encode('utf-8')
                self.tn.read_until('Username:'.encode('utf-8'))
                self.tn.write(userName)
                self.tn.read_until('Password:'.encode('utf-8'))
                self.tn.write(password)
                time.sleep(1)
            except:
                print ("登录主机%s时发生错误!!!" % self.ip)

    def exec_su(self, cmd, passwd):
        cmd = (cmd + '\n').encode('utf-8')
        passwd = (passwd + '\n').encode('utf-8')
        self.tn.write(cmd)
        self.tn.read_until(''.encode('utf-8'))
        self.tn.write(passwd)
        self.tn.read_until(''.encode('utf-8'))
            
    def exec_cmd(self, command):
        msg = ""
        command = (command + '\r').encode('utf-8')
        self.tn.write('\r'.encode('utf-8'))
        self.tn.write(command)
        self.tn.write('\r'.encode('utf-8'))
        result = []
        while self.tn.read_some():
            time.sleep(1)
            log = self.tn.read_very_eager()
            result.append(log)
            msg = msg + log.decode('utf-8')
            if (len(result) > 2):
                del result[0]
                if (result[0] == result[1]):
                    break
                else:
                    self.tn.write(' '.encode('utf-8'))
            else:
                self.tn.write(' '.encode('utf-8'))
        return msg

    def __del__(self):
        if self.login_status:
            self.tn.close()


#在python3+中在telnetlib中必须对字符串加上编码，否则报错
