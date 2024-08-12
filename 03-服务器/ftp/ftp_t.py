
import os
from ftplib import FTP


class FtpApi(object):

    def init_ftp_api(self, ip, port, username, password, passive=1):
        """
        初始化ftp
        :param ip: 远端ip
        :param port: 远端端口:
        param username: 用户名
        :param password: 密码
        :param passive: 主动或者被动
        """
        self.ip = ip
        self.port = int(port)
        self.username = username
        self.password = password
        self.pasv = passive
        self.ftp = FTP()
        self.__ftp_init()

    def __ftp_init(self):
        self.ftp.encoding = 'gbk'
        self.ftp.set_debuglevel(0)  # 不开启调试模式
        self.ftp.set_pasv(self.pasv)  # ftp有主动 被动模式
        self.ftp.connect(self.ip, self.port)
        self.ftp.login(self.username, self.password)

    def isdir(self, path):
        """
        判断是否为文件夹
        :param path: 路劲
        :return:
        """
        try:
            self.ftp.cwd(path)
            return True
        except:
            return False

    def download_file(self, ftp_file_path, dst_file_path):
        """
        下载文件
        :param ftp_file_path: FTP文件，文件或者文件夹
        :param dst_file_path: 保存路径，文件夹
        :return:
        """
        file_list = self.ftp.nlst(ftp_file_path)
        if len(file_list) == 0:
            print('文件不存在或者文件夹为空')
            return False
        for file_name in file_list:
            ftp_file = os.path.join(ftp_file_path, file_name)
            write_file = os.path.join(dst_file_path, os.path.basename(ftp_file))
            buf_size = 1024
            # 接收服务器上文件并写入本地文件
            # with open(write_file, "wb") as f:
            f = open(write_file, 'wb')
            self.ftp.retrbinary('RETR %s' % ftp_file, f.write, buf_size)
            f.close()
        return True

    def upload_file(self, local_file_path, dst_file_path):
        """
        上传文件
        :param local_file_path: 本地文件，文件
        :param dst_file_path: 远端路径，文件夹
        :return:
        """
        if not os.path.isfile(local_file_path):
            return
        if not self.isdir(dst_file_path):
            return
        remote_file = os.path.join(dst_file_path, os.path.basename(local_file_path))
        buf_size = 1024
        f = open(local_file_path, 'rb')
        self.ftp.storbinary('STOR %s' % remote_file, f, buf_size)
        f.close()

    def close(self):
        """
        退出ftp
        """
        self.ftp.quit()


if __name__ == '__main__':
    a = FtpApi()
    a.init_ftp_api('192.168.222.10', 21, 'cdr', '*#@cdr@#*')
    print(a.ftp.nlst('/var/svc9000/cdr/cdr-csv'))
    a.download_file('/var/svc9000/cdr/cdr-csv/cdr.csv', '/home/frz/ftp')
    # a = FtpApi('192.168.222.108', 21, 'frz', 'qweasdzxc1')
    # print(a.ftp.nlst('/'))
    # a.download_file('/1.txt', '/home/frz/ftp/test')
    # a.upload_file('/home/frz/a.html', '/')
