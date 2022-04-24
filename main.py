import ma
import utils.options
import utils.query
import utils.character_ids

CN_Cookie = ""
Oversea_Cookie = ""
httpProxy = ""

if __name__ == '__main__':
    utils.options.readOptions()
    utils.character_ids.checkNewIDsList()
    ma.run()
