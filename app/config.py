import os

print("The configuration is working")
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev') #"raterosDelOxxoFT.Ramon"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/LISForo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    