from links import create_app


if __name__ == '__main__':
    app = create_app()
    # from links import init_database
    # init_database(app)
    app.run(debug=True)