class Config:
    SECRET_KEY="root123"
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://kam_use:kam_pass@localhost/kam'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO = True  # Enable SQL echo for debugging