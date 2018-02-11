# -*- coding:utf-8 -*-

import sys
import paramiko

class baseSsh:
    login_status = True
    def __init__(self, ip, port, userName, password):
        self.ip = ip
        self.port = port
        self.userName = userName
        self.password = password



class linuxSsh(baseSsh):
    def __init__(self, ip, port, userName, password):
        baseSsh.__init__(self, ip, port, userName, password)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.ip, self.port, self.userName, self.password)
        except:
            self.login_status = False
            print ("远程linux主机%s认证出现异常，请确认登录配置信息及主机在线情况。" % self.ip)

    def shellCmd(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdin, stdout, stderr

    def __del__(self):
        if self.login_status:
            self.ssh.close()




class linuxSftp(baseSsh):
    def __init__(self, ip, port, userName, password):
        baseSsh.__init__(self, ip, port, userName, password)
        try:
            self.conn = paramiko.Transport((self.ip, int(self.port)))
            self.conn.connect(username = self.userName, password = self.password)
        except:
            self.login_status = False
            print ("远程主机%s认证出现异常，请确认登录配置信息及主机在线情况。")
        else:
            self.sftp = paramiko.SFTPClient.from_transport(self.conn)




class linuxScp(linuxSftp):
    def get(self, localfile, remotefile):
        self.sftp.get(remotefile, localfile)
    
    def put(self, localfile, remotefile):
        print (localfile)
        print (remotefile)
        self.sftp.put(localfile, remotefile)

    def __del__(self):
        if self.login_status:
            self.conn.close()



class netSsh(baseSsh):
    login_status = True
    def __init__(self, ip, port, userName, password):
        baseSsh.__init__(self, ip, port, userName, password)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(username=self.userName, password=self.password, hostname=self.ip, port=self.port)
        except:
            self.login_status = False
            print ("主机%sssh认证失败，请检查远程主机的登录信息及主机在线情况。" % self.ip)
        else:
            self.channel = self.ssh.invoke_shell()
            self.stdin = self.channel.makefile('wb')
            self.stdout = self.channel.makefile('r')

    def exec_su(self, cmd, passwd):
        self.stdin.write(cmd + '\n')
        self.stdin.write(passwd + '\n')
        self.stdin.flush()

    def exec_cmd(self, command):
        finish_cmd = 'cmd_end_off'
        for cmd in command:
            self.stdin.write(cmd + '\n')
        self.stdin.write(finish_cmd + '\n')
        self.stdin.flush()

        shout = ''
        for line in self.stdout:
            if ('cmd_end_off' in line):
                #判断如果结束符号在输出中，则终止循环，否则将结果添加到shout中
                break
            else:
                shout = shout + line

        return shout

    def __del__(self):
        if (self.login_status):
            self.channel.close()
