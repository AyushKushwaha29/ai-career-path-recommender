from app import create_app
from datetime import datetime

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

   

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}
