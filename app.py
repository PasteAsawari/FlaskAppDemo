#setting up Flask application
from flask import Flask,request
#from flask import request
# from sqlalchemy import Integer,String
# from sqlalchemy.orm import Mapped,mapped_column
#Importing SQLAlchemy class for db connection
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
#adding below code because interpreter throws error while creating db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

# with app.app_context():
#     db.create_all()

class Drink(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)
    description=db.Column(db.String(120),nullable=False)
    # id:Mapped[int] =mapped_column(Integer,primary_key=True)
    # name:Mapped[str] = mapped_column(String(80),unique=True,nullable=False)
    # description:Mapped[str] = mapped_column(String(120),nullable=False)

    def __repr__(self):
        # return f"{self.name} - {self.description}"
        return "{} - {}".format(self.name,self.description)


#creating a route/endpoints, whenver someone tries to access they are going to route it to this page
@app.route("/")
def index():
    return "Hello!!"

@app.route('/drinks')
def get_drinks():
    drinks= Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {"name": drink.name, "description":drink.description}
        output.append(drink_data)
    return {"drinks":output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {'name':drink.name, 'description':drink.description}

@app.route('/drinks',methods=['POST'])
def add_drink():
    if request.method =='POST':
        drink = Drink(name=request.json['name'], description=request.json['description'])
        db.session.add(drink)
        db.session.commit()
        return {'id':drink.id}
    
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    if request.method =='DELETE':
        drink = Drink.query.get(id)
        if drink is None:
            return {"error":"Not found"}
        db.session.delete(drink)
        db.session.commit()
        return {"Message":"data deleted"}


@app.route('/drinks/<id>', methods=['PUT'])
def update_drink(id):
    if request.method=='PUT':
        drink = Drink.query.get(id)
        if drink is None:
            return {"error":"Id Not found"}
        drink.name= request.json['name']
        drink.description = request.json['description']
        #db.session.add(drink)
        #db.session.commit()
        return {"message: data has been updated for {}".format(drink.id)}


