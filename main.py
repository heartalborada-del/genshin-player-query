import json
import os

from prettytable import PrettyTable

import ma
import utlis.options
import utlis.stats
import utlis.query

CN_Cookie = ""
Oversea_Cookie = ""
httpProxy = ""

if __name__ == '__main__':
    #os.system("mode con cols=120 lines=500")
    utlis.options.readOptions()
    ma.run()
