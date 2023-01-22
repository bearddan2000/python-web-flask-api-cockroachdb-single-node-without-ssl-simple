from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "cockroachdb://root@db:26257/animal"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class DogModel(db.Model):
    __tablename__ = 'dog'

    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String())
    color = db.Column(db.String())

    def __init__(self, breed, color):
        self.breed = breed
        self.color = color


@app.route('/dog', methods=['POST', 'GET'])
def handle_beverage():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_dog = DogModel(breed=data['breed'], color=data['color'])

            db.session.add(new_dog)
            db.session.commit()

            return {"message": f"Animal {new_dog.breed} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        dogs = DogModel.query.all()
        results = [
            {
                "breed": dog.breed,
                "color": dog.color
            } for dog in dogs]

        return {"count": len(results), "dog": results, "message": "success"}


@app.route('/dog/<dog_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_dog(dog_id):
    dog = DogModel.query.get_or_404(dog_id)

    if request.method == 'GET':
        response = {
            "breed": dog.breed,
            "color": dog.color
        }
        return {"message": "success", "animal": response}

    elif request.method == 'PUT':
        data = request.get_json()
        dog.breed = data['breed']
        dog.color = data['color']

        db.session.add(dog)
        db.session.commit()

        return {"message": f"Animal {dog.breed} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(dog)
        db.session.commit()

        return {"message": f"Animal {dog.breed} successfully deleted."}

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)
