from main.__init__ import create_app, init_db

app = create_app()

'''
@TODO: uncomment init_db() on first run or when refreshing database
!! NOTE: will drop entire db and recreate
'''
# init_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0')