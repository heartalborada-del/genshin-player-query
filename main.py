import ma
import utlis.options
import utlis.query

CN_Cookie = ""
Oversea_Cookie = ""
httpProxy = ""

if __name__ == '__main__':
    utlis.options.readOptions()
    ma.run()
