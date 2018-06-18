from .phoneprov_app import app

if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['ENV'] = 'development'

    app.run(host='0.0.0.0', port=8080)
