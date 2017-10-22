"""This model runs the app as the main function"""
#import app from the app model
from app import app

#execute app.run() when app is running as a script
if __name__ == "__main__":
    app.run()
    