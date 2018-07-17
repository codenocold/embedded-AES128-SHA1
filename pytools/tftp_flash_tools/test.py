import sys
import tftpy
import ctypes
from socket import *
from cmd import Cmd


FOREGROUND_RED   = 0x0c     # red.
FOREGROUND_GREEN = 0x0a     # green.
FOREGROUND_BLUE  = 0x09     # blue.

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_color(color, handle=std_out_handle):
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)


def reset_color():
    set_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


class MyCmd(Cmd):
    def __init__(self):
        super(MyCmd, self).__init__()
        self.prompt = ">>> "

    def emptyline(self):
        print('\r', end='')

    def do_flash(self, args):
        strs = args.split()
        if len(strs) == 2 and strs[0].isdigit() and strs[1].isdigit():
            ip_start = int(strs[0])
            ip_end = int(strs[1])
            if ip_end > ip_start and ip_start in range(0,255) and ip_end in range(0,255):
                total_cnt = ip_end - ip_start
                error_cnt = 0
                for index in range(ip_start, ip_end):
                    ip = "192.168.1." + str(index)
                    try:
                        client = tftpy.TftpClient(ip, 69)
                        client.upload('Ethernet_app.bin', 'Ethernet_app.bin')
                        sys.stdout.write("  OK\n")
                    except Exception:
                        set_color(FOREGROUND_RED)
                        sys.stdout.write("    FAIL\n")
                        sys.stdout.flush()
                        reset_color()
                        error_cnt += 1
                print("Flash %d Module, %d Success, %d Failed"% (total_cnt, total_cnt-error_cnt, error_cnt))
            else:
                print("IP index illegal")
        else:
            print("Syntax error")

    def help_flash(self):
        print("flash [start ip index] [end ip index]\n"
              "\tstart ip index 0~255\n"
              "\tend ip index 0~255\n"
              "Update the firmware witch ip index form start ip index to end ip index\n"
              "e.g.: flash 10 12\n"
              "\tupdata 192.168.1.10 and 192.168.1.11")

    def do_test(self, args):
        strs = args.split()
        if len(strs) == 2 and strs[0].isdigit() and strs[1].isdigit():
            ip_start = int(strs[0])
            ip_end = int(strs[1])
            if ip_end > ip_start and ip_start in range(0, 255) and ip_end in range(0, 255):
                total_cnt = ip_end - ip_start
                error_cnt = 0
                for index in range(ip_start, ip_end):
                    addr = ("192.168.1." + str(index), 8088)
                    tcp_client = socket(AF_INET, SOCK_STREAM)
                    tcp_client.settimeout(2)
                    try:
                        tcp_client.connect(addr)
                        tcp_client.send(b"\x00\x00\x00\x00\x00")
                        data = tcp_client.recv(1024)
                        if data[0] == 0xBB and data[1] == 0xCC and data[2] == 0x02 and data[3] == 0xCC and data[
                            4] == 0xBB:
                            print("%s Test OK"% (addr[0]))
                        else:
                            set_color(FOREGROUND_RED)
                            print("%s Test Fail" % (addr[0]))
                            reset_color()
                            error_cnt += 1
                    except:
                        set_color(FOREGROUND_RED)
                        print("%s Test Fail" % (addr[0]))
                        reset_color()
                        error_cnt += 1
                    tcp_client.close()
                print("Test %d Module, %d Success, %d Failed" % (total_cnt, total_cnt - error_cnt, error_cnt))
            else:
                print("IP index illegal")
        else:
            print("Syntax error")

    def help_test(self):
        print("test [start ip index] [end ip index]\n"
              "\tstart ip index 0~255\n"
              "\tend ip index 0~255\n"
              "Test the Modules witch ip index form start ip index to end ip index\n"
              "e.g.: test 10 12\n"
              "\ttest 192.168.1.10 and 192.168.1.11")

    def do_quit(self, args):
        exit(0)

    def help_quit(self):
        print("quit\n"
              "Quit this application")


def main():
    reset_color()
    myca = MyCmd()
    myca.cmdloop(intro="CSHT Flash Tool")


if __name__ == "__main__":
    main()
