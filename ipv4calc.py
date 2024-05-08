import sys
#import json
import argparse
VERSION = '1.2'
#IPv4 address calculator
#Autor: Jared, contact hfyu.hzcn@gmail.com

STR_SBNMASK_LEN = 'subnet mask length'
STR_ADDR_BIN = 'binary address'
STR_SBMASK_DEC = 'decimal subnet mask'
STR_SBMASK_BIN = 'binary subnet mask'
STR_NETADDR_DEC = 'decimal network adddr'
STR_NETADDR_BIN = 'binary network adddr'
STR_FIRST_HOST_ADDR_DEC = 'decimal first assignable ip'
STR_FIRST_HOST_ADDR_BIN = 'binary first assignable ip'
STR_LAST_HOST_ADDR_DEC = 'decimal last assignable ip'
STR_LAST_HOST_ADDR_BIN = 'binary last assignable ip'
STR_BROADCAST_ADDR_DEC = 'decimal broadcast ip'
STR_BROADCAST_ADDR_BIN = 'binary broadcast ip'
STR_HOST_COUNT = 'total host count'
STR_HOST_COUNT_AVAIL = 'available host count'

#convert a binary string to a decimal number
def bin2dec(strBinary:str) -> int:
    return int(strBinary,2)

#convert a decimal number to a binary string
def dec2bin(strDecimal:str, length=8) -> str:
    str = bin(strDecimal)[2:]  #omit the leading '0b'
    return '0'*(length-len(str)) + str

class IPV4Calc():
    def __init__(self, ipv4address):
        # the parameter ipv4address can be a string or a list of strings
        if isinstance(ipv4address, str):
            listAddr = [ipv4address]
        elif isinstance(ipv4address, list):
            listAddr = ipv4address
        self.validAddress = True
        if not self.initAddrs( listAddr ):
            self.validAddress = False
            return
        
        self.doCalculation()
        
    
    def initAddrs(self, listAddr:list) -> bool:
        self.addrs = {}
        for addr in listAddr:
            addr = addr.replace(' ', '')
            str = addr.split('/')
            ip = str[0]
            len = int(str[1])
            if not self.validateAddrIpv4(ip,len):
                return False
            self.addrs[addr] = {STR_SBNMASK_LEN:int(len)}
            self.addrs[addr][STR_ADDR_BIN] = self.ipv4Dec2Bin(ip)
        return True

    def doCalculation(self) -> None:
        for addr, attrib in self.addrs.items():
            sbnLen = attrib[STR_SBNMASK_LEN]
            self.addrs[addr][STR_SBMASK_BIN] = self.getSubnetMaskBin(sbnLen)
            self.addrs[addr][STR_SBMASK_DEC] = self.ipv4Bin2Dec(self.addrs[addr][STR_SBMASK_BIN])
            self.addrs[addr][STR_NETADDR_BIN] = self.getSubnetAddrBin(self.addrs[addr][STR_ADDR_BIN],sbnLen)
            self.addrs[addr][STR_NETADDR_DEC] = self.ipv4Bin2Dec(self.addrs[addr][STR_NETADDR_BIN])
            self.addrs[addr][STR_FIRST_HOST_ADDR_BIN] = self.getFirstAssignableAddrBin(self.addrs[addr][STR_ADDR_BIN],sbnLen)
            self.addrs[addr][STR_FIRST_HOST_ADDR_DEC] = self.ipv4Bin2Dec(self.addrs[addr][STR_FIRST_HOST_ADDR_BIN])
            self.addrs[addr][STR_LAST_HOST_ADDR_BIN] = self.getLastAssignableAddrBin(self.addrs[addr][STR_ADDR_BIN],sbnLen)
            self.addrs[addr][STR_LAST_HOST_ADDR_DEC] = self.ipv4Bin2Dec(self.addrs[addr][STR_LAST_HOST_ADDR_BIN])
            self.addrs[addr][STR_BROADCAST_ADDR_BIN] = self.getBroadcastAddrBin(self.addrs[addr][STR_ADDR_BIN],sbnLen)
            self.addrs[addr][STR_BROADCAST_ADDR_DEC] = self.ipv4Bin2Dec(self.addrs[addr][STR_BROADCAST_ADDR_BIN])
            self.addrs[addr][STR_HOST_COUNT] = self.getHostCount(sbnLen)
            self.addrs[addr][STR_HOST_COUNT_AVAIL] = self.addrs[addr][STR_HOST_COUNT] - 2

    def validateAddrIpv4(self, strIP:str, intLen:int) -> bool:
        #print(strIP, intLen)
        if intLen <=0 or intLen >= 32:
            return False
        for addr in strIP.split('.'):
            num = int(addr)
            if num < 0 or num >= 256:
                return False

        return True
    
    def ipv4Bin2Dec(self, strBin:str) -> str:
        addrDec = []
        for num in strBin.split('.'):
            addrDec.append(str(bin2dec(num)))
        return '.'.join(addrDec)

    def ipv4Dec2Bin(self, strDec:str) -> str:
        addrBin = []
        for num in strDec.split('.'):
            addrBin.append(dec2bin(int(num)))
        return '.'.join(addrBin)

    # convert '11110000110000111010110001011110' to '11110000.11000011.10101100.01011110'
    def splitBinAddr(self, strBin:str) -> str:
        addrBin = [strBin[:8], strBin[8:16], strBin[16:24], strBin[24:]]
        return '.'.join(addrBin)

    def getSubnetMaskBin(self, intSubnetLen:int) -> str:
        bin = '1'*intSubnetLen + '0'*(32-intSubnetLen)
        return self.splitBinAddr(bin)

    def getSubnetAddrBin(self, addrBin:str, sbnLen:int) -> str:
        str = ''.join(addrBin.split('.'))
        addr = str[:sbnLen] + '0'*(32-sbnLen)
        return self.splitBinAddr(addr)
    
    def getFirstAssignableAddrBin(self, addrBin:str, sbnLen:int) -> str:
        str = ''.join(addrBin.split('.'))
        addr = str[:sbnLen] + '0'*(32-sbnLen-1) + '1'
        return self.splitBinAddr(addr)
    def getLastAssignableAddrBin(self, addrBin:str, sbnLen:int) -> str:
        str = ''.join(addrBin.split('.'))
        addr = str[:sbnLen] + '1'*(32-sbnLen-1) + '0'
        return self.splitBinAddr(addr)
    def getBroadcastAddrBin(self, addrBin:str, sbnLen:int) -> str:
        str = ''.join(addrBin.split('.'))
        addr = str[:sbnLen] + '1'*(32-sbnLen)
        return self.splitBinAddr(addr)
    
    def getHostCount(self, sbnLen:int) -> int:
        return bin2dec('1'*(32-sbnLen)) + 1

    def printResult(self, printBinary=True) -> None:
        if not self.validAddress:
            print('ERROR: invalid ip address')
            return
        for addr, attrib in self.addrs.items():
            if printBinary:
                print('{} {}/{}'.format(addr, attrib[STR_ADDR_BIN],attrib[STR_SBNMASK_LEN]))
                print('\tsubnet mask\t\t{} {}'.format(attrib[STR_SBMASK_DEC], attrib[STR_SBMASK_BIN]))
                print('\tnetwork addr\t\t{}/{} {}/{}'.format(attrib[STR_NETADDR_DEC], attrib[STR_SBNMASK_LEN], attrib[STR_NETADDR_BIN], attrib[STR_SBNMASK_LEN]))
                print('\tfirst usable addr\t{}/{} {}/{}'.format(attrib[STR_FIRST_HOST_ADDR_DEC], attrib[STR_SBNMASK_LEN], attrib[STR_FIRST_HOST_ADDR_BIN], attrib[STR_SBNMASK_LEN]))
                print('\tlast usable addr\t{}/{} {}/{}'.format(attrib[STR_LAST_HOST_ADDR_DEC], attrib[STR_SBNMASK_LEN], attrib[STR_LAST_HOST_ADDR_BIN], attrib[STR_SBNMASK_LEN]))
                print('\tbroadcast addr\t\t{}/{} {}/{}'.format(attrib[STR_BROADCAST_ADDR_DEC], attrib[STR_SBNMASK_LEN], attrib[STR_BROADCAST_ADDR_BIN], attrib[STR_SBNMASK_LEN]))
                print('\ttotal host count\t{}'.format(attrib[STR_HOST_COUNT]))
                print('\tusable host count\t{}'.format(attrib[STR_HOST_COUNT_AVAIL]))
            else:
                print(addr)
                print('\tsubnet mask\t\t{}'.format(attrib[STR_SBMASK_DEC]))
                print('\tnetwork addr\t\t{}/{}'.format(attrib[STR_NETADDR_DEC], attrib[STR_SBNMASK_LEN]))
                print('\tfirst usable addr\t{}/{}'.format(attrib[STR_FIRST_HOST_ADDR_DEC], attrib[STR_SBNMASK_LEN]))
                print('\tlast usable addr\t{}/{}'.format(attrib[STR_LAST_HOST_ADDR_DEC], attrib[STR_SBNMASK_LEN]))
                print('\tbroadcast addr\t\t{}/{}'.format(attrib[STR_BROADCAST_ADDR_DEC], attrib[STR_SBNMASK_LEN]))
                print('\ttotal host count\t{}'.format(attrib[STR_HOST_COUNT]))
                print('\tusable host count\t{}'.format(attrib[STR_HOST_COUNT_AVAIL]))

    

    def export2excel(self, fileName:str, sheetName:str, outputBinary = False) -> bool:
        colAddr = []
        colSbnMask = []
        colNetAddr = []
        colHostCount = []
        colHostCountUsable = []
        colFirstHost = []
        colLastHost = []
        colBroadcastAddr = []
        
        for addr, attrib in self.addrs.items():
            colAddr.append(addr)
            if outputBinary:
                colAddr.append('')
            colSbnMask.append(attrib[STR_SBMASK_DEC])
            if outputBinary:
                colSbnMask.append(attrib[STR_SBMASK_BIN])
            colNetAddr.append(attrib[STR_NETADDR_DEC] + '/' + str(attrib[STR_SBNMASK_LEN]))
            if outputBinary:
                colNetAddr.append(attrib[STR_NETADDR_BIN] + '/' + str(attrib[STR_SBNMASK_LEN]))
            colHostCount.append(attrib[STR_HOST_COUNT])
            if outputBinary:
                colHostCount.append('')
            colHostCountUsable.append(attrib[STR_HOST_COUNT_AVAIL])
            if outputBinary:
                colHostCountUsable.append('')
            colFirstHost.append(attrib[STR_FIRST_HOST_ADDR_DEC] + '/' + str(attrib[STR_SBNMASK_LEN]))
            if outputBinary:
                colFirstHost.append(attrib[STR_FIRST_HOST_ADDR_BIN] + '/' + str(attrib[STR_SBNMASK_LEN]))
            colLastHost.append(attrib[STR_LAST_HOST_ADDR_DEC] + '/' + str(attrib[STR_SBNMASK_LEN]))
            if outputBinary:
                colLastHost.append(attrib[STR_LAST_HOST_ADDR_BIN] + '/' + str(attrib[STR_SBNMASK_LEN]))
            colBroadcastAddr.append(attrib[STR_BROADCAST_ADDR_DEC] + '/' + str(attrib[STR_SBNMASK_LEN]))
            if outputBinary:
                colBroadcastAddr.append(attrib[STR_BROADCAST_ADDR_BIN] + '/' + str(attrib[STR_SBNMASK_LEN]))
        try:
            import pandas as pd
        except:
            print('This script requires module pandas for saving to an excel file, please install it by running: pip install pandas.')
            exit(-1)
        try:
            import openpyxl
        except:
            print('This script requires module openpyxl for saving to an excel file, please install it by running: pip install openpyxl.')
            exit(-1)
        try:
            import xlsxwriter
        except:
            print('This script requires module xlsxwriter for saving to an excel file, please install it by running: pip install xlsxwriter.')
            exit(-1)
        df = pd.DataFrame(data={'Address':colAddr, 'SubnetMask':colSbnMask, 'NetworkAddr':colNetAddr, 'HostCount':colHostCount, 'UsableHostCount':colHostCountUsable,
        'FirstUsableHostAddr':colFirstHost, 'LastUsableHostAddr':colLastHost, 'BroadcatAddr':colBroadcastAddr})
        #print(df)
        # try:
        #     writer = pd.ExcelWriter(fileName)
        #     df.to_excel(writer, index=False, sheet_name = sheetName)
            
        #     for column in df:
        #         columnWidth = max(df[column].astype(str).map(len).max(), len(column))
        #         colIndex = df.columns.get_loc(column)
        #         writer.sheets[sheetName].set_column(colIndex, colIndex, columnWidth)
        #     writer.close()
        #     return True
        # except:
        #     print('FAILED to write to file {}'.format(fileName))
        #     return False
        writer = pd.ExcelWriter(fileName)
        df.to_excel(writer, index=False, sheet_name = sheetName)
        
        for column in df:
            columnWidth = max(df[column].astype(str).map(len).max(), len(column))
            colIndex = df.columns.get_loc(column)
            writer.sheets[sheetName].set_column(colIndex, colIndex, columnWidth)
            
        writer.close()
        return True
        
def about() -> None:
    print('-'*20 + 'IPv4 address calculator ' + VERSION + '-'*20)
    print('any suggestion is welcome, contact hfyu.hzcn@gmail.com SVP.')
    print('-'*63)
def usage() -> None:
    print('Usage: {} IP_ADDRESS1/SubnetMaskLength,IP_ADDRESS2/SubnetMaskLength -output FILENAME'.format(sys.argv[0]))
    print('\t-ip')
    print('\t\tspecify ip addresses, seperated by commas, no space.')
    print('\t\tip address should contain a subnet mask length: xxx.xxx.xxx.xxx/xx')
    print('\t-output')
    print('\t\tOptional. If given, the results will be save to the file spacified.')
    print('\t\tif the extesion of the filename is not .xlsx, then .xlsx will be appended.')
    print('\tExample: {} -ip 172.28.208.200/25,196.200.32.150/26 -output save.xlsx'.format(sys.argv[0]))
    print(' ')
    print('For windows users, the command should be:')
    print('\tpython {} IP_ADDRESS1/SubnetMaskLength,IP_ADDRESS2/SubnetMaskLength -output FILENAME'.format(sys.argv[0]))
    print('MAKE SURE the directory where python locates is set in the system environment variable PATH')

def getArguments() -> dict:
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('-ip')
    parser.add_argument('-output')
    args = vars(parser.parse_args())
    if not args['output'] is None:
        if args['output'].split('.')[-1].lower() != 'xlsx':
            args['output'] = args['output'] + '.xlsx'
    return args
        

if __name__ == '__main__':
    about()
    if len(sys.argv) == 1:
        usage()
        exit(-1)
    #addr = ['192.168.0. 50 / 24', '172.28.208.200/25','196.200.32.150/26','192.168.50.112/27','184.20.65.20/29']
    args = getArguments()
    
    #addr = sys.argv[1:]
    if args['ip'] is None:
        usage()
        exit(-1)
    addr = args['ip'].split(',')
    ip = IPV4Calc(addr)
    #print(json.dumps(ip.addrs, indent=4))
    ip.printResult()
    if not args['output'] is None:
        # outputFileName = args['output']
        import os
        outputFileName = os.path.join(os.path.dirname(sys.argv[0]), args['output'])
        if ip.export2excel(outputFileName, 'decimal and binary', True):
            print('-'*20)
            print('The above information saved to file {}'.format(outputFileName))
    exit(0)
    
