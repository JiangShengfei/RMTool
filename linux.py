# -*- coding:utf-8 -*-

import time
import my_ssh
import readtext

def linux_cmd(hosts, cmdfile, msgOutput):
    remote = readtext.readremoteinfo(hosts)
    command = readtext.readcommands(cmdfile)
    succ_num = 0
    fail_num = 0

    for host in remote:
        if (len(host) < 5):
            fail_num += 1
            print ("主机：%s登录失败，登录信息不完善，请完善配置。" % host[1])
            continue
        conn = my_ssh.linuxSsh(host[1], host[2], host[3], host[4])
        if not conn.login_status:
            fail_num += 1
            continue
        succ_num += 1
        if (msgOutput == ''):
            print ("正在处理主机：%s\n" % host[1])
            for cmd in command:
                stdin, stdout, stderr = conn.shellCmd(cmd)
                print ("命令%s的执行结果为:" % cmd)
                for line in stdout.readlines():
                    print (line.rstrip('\n'))
                print ("\n")

        else:
            #输出至配置文件
            fileName = msgOutput + host[0] + '_' + host[1] + '_' + time.strftime("%m%d%H%M%S") + '.txt'
            print ("正在处理主机：%s" % host[1])
            msg2file = readtext.std2file(fileName)
            for cmd in command:
                stdin, stdout, stderr = conn.shellCmd(cmd)
                for line in stdout.readlines():
                    if msg2file.open_status:
                        msg2file.msg_write("%s\n" % cmd)
                        msg2file.msg_write(line.rstrip('\n'))
                msg2file.msg_write('\n')
            print ("执行结果写至文件：%s" % fileName)

    print ("----------------------------------------------\n")
    print ("所有linux远程主机命令执行完成:")
    print ("操作执行主机总数为：%d台；" % len(remote))
    print ("本次任务执行中成功主机%d台，失败主机%d台；" % (succ_num, fail_num))
    print ("每台远程主机执行命令为：%d条。\n\n" % len(command))



def linux_upload(hosts, localpath, remotepath):
    remote = readtext.readremoteinfo(hosts)
    print ("上传文件的主机个数为：%d台" % len(remote))
    print ("本地文件为：%s" % localpath)
    print ("远程主机文件为：%s" % remotepath)
    print ("-----------------------------------------")
    for host in remote:
        if (len(host) < 5):
            print ("主机：%s登录失败，登录信息不完善，请完善配置。")
            continue
        print ("正在连接至主机%s,并上传文件...")
        sftp = my_ssh.linuxScp(host[1], host[2], host[3], host[4])
        sftp.put(localpath, remotepath)
        print ("发送完成，退出主机: %s" % host[1])

    print ("已完成所有文件上传操作。")




def linux_download(hosts, localpath, remotepath):
    remote = readtext.readremoteinfo(hosts)
    print ("下载文件的主机个数为：%d台" % len(remote))
    print ("本地文件为：%s" % localpath)
    print ("远程主机文件为：%s" % remotepath)
    print ("-----------------------------------------")
    for	host in	remote:
        if (len(host) < 5):
            print ("主机：%s登录失败，登录信息不完善，请完善配置。")
            continue
        print ("正在连接至主机%s,并下载文件...")
        sftp = my_ssh.linuxScp(host[1], host[2], host[3], host[4])
        sftp.get(localpath, remotepath)
        print ("下载完成，退出主机: %s" % host[1])

    print ("已完成所有文件下载操作。")
