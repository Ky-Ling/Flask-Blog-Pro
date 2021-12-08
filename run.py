'''
Date: 2021-11-25 13:33:24
LastEditors: GC
LastEditTime: 2021-12-05 16:57:53
FilePath: \Flask-Blog-Project2\run.py
'''
from flaskblog import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


# Give some validation feedback to the user so that if they input incorrect information and then they know exactly what it is
#    that they did wrong and what they need to fix


# cd D: \Programming\Python Work\.vscode\Projects\Flask Projects\Flask-Blog-Project2