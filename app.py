from flask import Flask, request, jsonify
from calculator import Calculator, Car, ElectricCar

app = Flask(__name__)

calculator = Calculator()


@app.route("/add_car/", methods=["POST"])
def add_car():
    data = request.get_json()

    if not data or "type" not in data:
        return jsonify({"error": "JSON must contain 'type': 'car' or 'electric'"}), 400

    # обычный автомобиль
    if data["type"] == "car":
        try:
            car = Car(
                name=data["name"],
                price=data["price"],
                fuel_economy=data["fuel_economy"],
                service_cost=data["service_cost"],
                insurance_cost=data["insurance_cost"]
            )
        except KeyError as e:
            return jsonify({"error": f"Missing field: {e}"}), 400

    # электромобиль
    elif data["type"] == "electric":
        try:
            car = ElectricCar(
                name=data["name"],
                price=data["price"],
                insurance_cost=data["insurance_cost"],
                power_consumption=data["power_consumption"]
            )
        except KeyError as e:
            return jsonify({"error": f"Missing field: {e}"}), 400

    else:
        return jsonify({"error": "Invalid type"}), 400

    calculator.add_car(car)
    return jsonify({"status": "added", "car": car.name})


@app.route("/cars/", methods=["GET"])
def list_cars():
    cars = [car.name for car in calculator.cars.keys()]
    return jsonify({"cars": cars})


@app.route("/car/<name>/cost/", methods=["GET"])
def get_cost(name):
    try:
        mileage = int(request.args.get("mileage", calculator.mileage))
        years = int(request.args.get("years", calculator.years))
    except ValueError:
        return jsonify({"error": "mileage and years must be integers"}), 400

    # ищем машину
    target_car = None
    for car in calculator.cars.keys():
        if car.name.lower() == name.lower():
            target_car = car
            break

    if not target_car:
        return jsonify({"error": "Car not found"}), 404

    # считаем стоимость
    calc = Calculator(mileage=mileage, years=years)
    calc.add_car(target_car)
    cost = calc.cars[target_car]

    return jsonify({
        "car": target_car.name,
        "mileage_per_year": mileage,
        "years": years,
        "yearly_cost": cost,
        "total_cost": cost * years
    })


if __name__ == "__main__":
    app.run(debug=True)