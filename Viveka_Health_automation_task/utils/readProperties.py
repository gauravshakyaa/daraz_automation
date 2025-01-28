import configparser

config = configparser.ConfigParser()
config.read("Configurations\config.ini")

class ReadConfig:
    @staticmethod
    def getURL():
        url = config.get("Basic Info", "baseURL")
        return url
    
    @staticmethod
    def getBrowser():
        browser = config.get("Basic Info", "browser")
        return browser
    
    @staticmethod
    def getProductName():
        productName = config.get("Basic Info", "productName")
        return productName
    