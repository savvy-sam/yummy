"""This model runs the app as the main function"""
#import app from the app model
import os
from app import app

#execute app.run() when app is running as a script
if __name__ == "__main__":
#Get port from the environment otherwise use port 5000 
    app.run('', port=int(os.environ.get('PORT', 5000)))
    