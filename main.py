import calculator

if __name__ == '__main__':
    calc = calculator.Calculator(years=3)
    calc.add_car(
        calculator.Car(name="Toyota Corolla", price=120000, fuel_economy=7, service_cost=1200, insurance_cost=2500),
    )
    calc.add_car(
        calculator.ElectricCar(name="Tesla Model 3", price=200000, insurance_cost=5500, power_consumption=150),
    )
    calc.add_car(
        calculator.Car(name="Range Rover", price=650000, fuel_economy=3, service_cost=3000, insurance_cost=7000),
    )

    calc.print_cars()
