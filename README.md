# ipv4-calculator-py
a python script for calculating ipv4 addresses
The script accepts arguments of ipv4 addresses with subnet mask length, produces the following info:
  subnet mask
  network address
  the first assignable ip address
  the last assignable ip address
  total host count
  total usable host count
  broadcast ip address
usage: python ipv4calc.py -ip ip1/len1,ip2/len2,ip3/len3 -output FILENAME
e.g.: python ipv4calc.py -ip 172.28.208.200/25,196.200.32.150/26,184.20.65.20/29 -output save.xlsx

required modules: pandas, argparse

