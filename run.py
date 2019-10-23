from App import App

app = App()


def run():
    app.run(app.config['HOST'], app.config['PORT'])


if __name__ == '__main__':
    run()