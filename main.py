import ma
import utlis.options
import utlis.query
import utlis.character_ids

CN_Cookie = ""
Oversea_Cookie = ""
httpProxy = ""

if __name__ == '__main__':
    utlis.options.readOptions()
    utlis.character_ids.checkNewIDsList()
    ma.run()
