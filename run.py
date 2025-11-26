<<<<<<< HEAD
from app import app
from datetime import datetime

app = create_app()

if __name__ == "__main__":
    app.run()
=======
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


    from datetime import datetime
>>>>>>> ae39b29 (Update files)

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}
