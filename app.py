import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///result.db"

db = SQLAlchemy(app)


# Создание таблицы User
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    email = db.Column(db.String(30))
    role = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    # orders = relationship("Order", back_populates="user_orders")
    # offers = relationship("Offer", back_populates="user_offers")


# Создание таблицы Order
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(15))
    end_date = db.Column(db.String(15))
    address = db.Column(db.String(50))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # Внешний ключ тб User
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # Внешний ключ тб User
    # user_orders = relationship("User", back_populates="orders")
    # offer_orders = relationship("Offer", back_populates="orders_offer")


# Создание таблицы Offer
class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))  # Внешний ключ тб Order
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # Внешний ключ тб User
    # orders_offers = relationship("Order", back_populates="offer_orders")
    # user_offers = relationship("User", back_populates="offers")


def load_from_json(json_file):
    """
    Получение данных из json файла
    """
    with open(json_file, "r", encoding="utf-8") as file:
        result = json.load(file)
        return result


with app.app_context():
    db.drop_all()
    db.create_all()

    # Добавляем данные в таблицу User
    users_json = load_from_json("users.json")
    for user in users_json:
        db.session.add(User(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"],
            role=user["role"],
            phone=user["phone"]
        )
        )

    # Добавляем данные в таблицу Order
    orders_json = load_from_json("orders.json")
    for order in orders_json:
        db.session.add(Order(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=order["start_date"],
            end_date=order["end_date"],
            address=order["address"],
            price=order["price"],
            # customer_id=User,
            # executor_id=User
            customer_id=order["customer_id"],
            executor_id=order["executor_id"]
        )
        )

    # Добавляем данные в таблицу Offers
    offers_json = load_from_json("offers.json")
    for offer in offers_json:
        db.session.add(Offer(
            id=offer["id"],
            # order_id=Order,
            # executor_id=Order
            order_id=offer["order_id"],
            executor_id=offer["executor_id"]
        )
        )
    db.session.commit()
    db.session.close()


# Представление выводит данные всех пользователей из таблицы User
@app.route("/users")
def get_users():
    user_list = User.query.all()
    result = []

    for usr in user_list:
        result.append(
            {
                "id": usr.id,
                "first_name": usr.first_name,
                "last_name": usr.last_name,
                "age": usr.age,
                "email": usr.email,
                "role": usr.role,
                "phone": usr.phone
            }
        )
    return json.dumps(result)


# Представление выводит данные пользователя с id=uid из таблицы User
@app.route("/users/<int:uid>")
def get_user_by_pk(uid):
    usr = User.query.get(uid)
    return json.dumps(
        {
            "id": usr.id,
            "first_name": usr.first_name,
            "last_name": usr.last_name,
            "age": usr.age,
            "email": usr.email,
            "role": usr.role,
            "phone": usr.phone
        }
    )


# Представление выводит все данные из таблицы Order
@app.route("/orders")
def get_orders():
    order_list = Order.query.all()
    result = []

    for ordr in order_list:
        result.append(
            {
                "id": ordr.id,
                "name": ordr.name,
                "description": ordr.description,
                "start_date": ordr.start_date,
                "end_date": ordr.end_date,
                "address": ordr.address,
                "price": ordr.price,
                "customer_id": ordr.customer_id,
                "executor_id": ordr.executor_id
            }
        )
    return json.dumps(result, ensure_ascii=False).encode('utf8')


# Представление выводит данные из таблицы Order, где id=oid
@app.route("/orders/<int:oid>")
def get_order(oid):
    ordr = Order.query.get(oid)
    result = {
        "id": ordr.id,
        "name": ordr.name,
        "description": ordr.description,
        "start_date": ordr.start_date,
        "end_date": ordr.end_date,
        "address": ordr.address,
        "price": ordr.price,
        "customer_id": ordr.customer_id,
        "executor_id": ordr.executor_id
    }
    return json.dumps(result, ensure_ascii=False).encode('utf8')


# Представление выводит все данные из таблицы Offer
@app.route("/offers")
def get_offers():
    offers_list = Offer.query.all()
    result = []

    for offr in offers_list:
        result.append(
            {
                "id": offr.id,
                "order_id": offr.order_id,
                "executor_id": offr.executor_id
            }
        )
    return json.dumps(result)


# Представление выводит данные из таблицы Offer, где id=oid
@app.route("/offers/<int:oid>")
def get_offer_by_pk(oid):
    offr = Offer.query.get(oid)
    return json.dumps(
        {
            "id": offr.id,
            "order_id": offr.order_id,
            "executor_id": offr.executor_id
        }
    )


"""
Представления добавления, обновления и удаления для таблицы User
"""


# Представление с добавлением пользователя в таблицу Users
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = User(
        id=User.query.count() + 1,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        age=data.get("age"),
        email=data.get("email"),
        role=data.get("role"),
        phone=data.get("phone")
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "age": new_user.age,
            "email": new_user.email,
            "role": new_user.role,
            "phone": new_user.phone
        }
    )


# Представление с обновлением пользователя
@app.route("/users/<uid>", methods=["PUT"])
def put_user(uid):
    data = request.json
    usr = User.query.get(uid)
    usr.first_name = data.get("first_name")
    usr.last_name = data.get("last_name")
    usr.age = data.get("age")
    usr.email = data.get("email")
    usr.role = data.get("role")
    usr.phone = data.get("phone")
    db.session.add(usr)
    db.session.commit()
    return jsonify(
        {
            "id": usr.id,
            "first_name": usr.first_name,
            "last_name": usr.last_name,
            "age": usr.age,
            "email": usr.email,
            "role": usr.role,
            "phone": usr.phone
        })


# Представление с удалением пользователя по введенному uid из таблицы User
@app.route("/users/<uid>", methods=["DELETE"])
def delete_user(uid):
    usr = User.query.get(uid)
    db.session.delete(usr)
    db.session.commit()
    return "Пользователь удален"


"""
Представления добавления, обновления и удаления для таблицы Order
"""


# Представление с добавлением в таблицу Order
@app.route("/orders", methods=["POST"])
def add_order():
    order_data = request.json
    new_order = Order(
        id=Order.query.count(),
        name=order_data.get("name"),
        description=order_data.get("description"),
        start_date=order_data.get("start_date"),
        end_date=order_data.get("end_date"),
        address=order_data.get("address"),
        price=order_data.get("price"),
        customer_id=order_data.get("customer_id"),
        executor_id=order_data.get("executor_id")
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(
        {
            "id": new_order.id,
            "name": new_order.name,
            "description": new_order.description,
            "start_date": new_order.start_date,
            "end_date": new_order.end_date,
            "address": new_order.address,
            "price": new_order.price,
            "customer_id": new_order.customer_id,
            "executor_id": new_order.executor_id
        }
    )


# Представление с обновлением данных таблицы Order
@app.route("/orders/<oid>", methods=["PUT"])
def put_order(oid):
    order_data = request.json
    ordr = Order.query.get(oid)
    ordr.name = order_data.get("name")
    ordr.description = order_data.get("description")
    ordr.start_date = order_data.get("start_date")
    ordr.end_date = order_data.get("end_date")
    ordr.address = order_data.get("address")
    ordr.price = order_data.get("price")
    ordr.customer_id = order_data.get("customer_id")
    ordr.executor_id = order_data.get("executor_id")
    db.session.add(ordr)
    db.session.commit()
    return jsonify(
        {
            "id": ordr.id,
            "name": ordr.name,
            "description": ordr.description,
            "start_date": ordr.start_date,
            "end_date": ordr.end_date,
            "address": ordr.address,
            "price": ordr.price,
            "customer_id": ordr.customer_id,
            "executor_id": ordr.executor_id
        })


# Представление с удалением данных по введенному oid из таблицы Order
@app.route("/orders/<oid>", methods=["DELETE"])
def delete_order(oid):
    ordr = Order.query.get(oid)
    db.session.delete(ordr)
    db.session.commit()
    return "Данные удалены"


"""
Представления добавления, обновления и удаления для таблицы Offer
"""


# Представление с добавлением в таблицу Offer
@app.route("/offers", methods=["POST"])
def add_offer():
    offer_data = request.json
    new_offer = Offer(
        id=Offer.query.count(),
        order_id=offer_data.get("order_id"),
        executor_id=offer_data.get("executor_id")
    )
    db.session.add(new_offer)
    db.session.commit()
    return jsonify(
        {
            "id": new_offer.id,
            "order_id": new_offer.order_id,
            "executor_id": new_offer.executor_id
        }
    )


# Представление с обновлением данных таблицы Offer
@app.route("/offers/<oid>", methods=["PUT"])
def put_offer(oid):
    offer_data = request.json
    offr = Offer.query.get(oid)
    offr.order_id = offer_data.get("order_id")
    offr.executor_id = offer_data.get("executor_id")
    db.session.add(offr)
    db.session.commit()
    return jsonify(
        {
            "id": offr.id,
            "order_id": offr.order_id,
            "executor_id": offr.executor_id
        })


# Представление с удалением данных по введенному oid из таблицы Offer
@app.route("/offers/<oid>", methods=["DELETE"])
def delete_offer(oid):
    offr = Offer.query.get(oid)
    db.session.delete(offr)
    db.session.commit()
    return "Данные удалены"


if __name__ == '__main__':
    app.run(debug=True)
