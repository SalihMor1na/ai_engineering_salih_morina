def calculate_car_price(new_price, years_old, mileage):
    # 1000000 * (1 * 0,15)
    price_after_years = new_price * (years_old * 15/100)
    price_after_milage = 5000 * (mileage / 10000)
    total_price = int(new_price - (price_after_years - price_after_milage))
    
    return total_price





def user_input():
    new_price_1 = int(input("Ange ny pris: ").replace("kr", ""))
    years_old_2 = int(input("Ange år: ").replace("år", ""))
    mileage_3 = int(input("Ange ny km: ").replace("km", ""))
    
    car_price = calculate_car_price(new_price_1, years_old_2, mileage_3)
    print(car_price)

user_input()


