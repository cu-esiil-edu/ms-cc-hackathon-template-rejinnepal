import requests

API_KEY = 'ibpSMFMSAnGeoJPEb6vbnA'
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def get_flight_emissions_api(departure_airport, arrival_airport, passengers_count):
    url = 'https://www.carboninterface.com/api/v1/estimates'
    payload = {
        "type": "flight",
        "passengers": passengers_count,
        "legs": [
            {
                "departure_airport": departure_airport,
                "destination_airport": arrival_airport
            }
        ]
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        data = response.json()
        emissions_kg = data['data']['attributes']['carbon_kg']
        print(f"The Estimated CO₂ for flight from {departure_airport} to {arrival_airport}: {emissions_kg} kg per {passengers_count} passenger(s)")
        return emissions_kg
    else:
        print("Error:", response.status_code, response.text)
        return 0

def get_vehicle_emissions_api(make):
    response = requests.get('https://www.carboninterface.com/api/v1/vehicle_makes', headers=HEADERS)
    makes = response.json()

    make_id = next((m['data']['id'] for m in makes if m['data']['attributes']['name'] == make), None)
    if not make_id:
        print("The Vehicle Make you provided is not found.")
        return

    models_url = f'https://www.carboninterface.com/api/v1/vehicle_makes/{make_id}/vehicle_models'
    models_resp = requests.get(models_url, headers=HEADERS)
    models = models_resp.json()

    print("The available models of {make} are:")
    for i, model in enumerate(models):
        print(f"{i + 1}. {model['data']['attributes']['name']}")
    choice = int(input("Please choose a model by number:: ")) - 1

    if 0 <= choice < len(models):
        vehicle_id = models[choice]['data']['id']
        distance = float(input("Please enter distance driven (in miles):: "))
        print("_______________________________________________________________________")
        payload = {
            "type": "vehicle",
            "distance_unit": "mi",
            "distance_value": distance,
            "vehicle_model_id": vehicle_id
        }
        resp = requests.post('https://www.carboninterface.com/api/v1/estimates', headers=HEADERS, json=payload)
        if resp.status_code == 201:
            carbon_kg = resp.json()['data']['attributes']['carbon_kg']
            print(f"The estimated CO₂ emissions for driving: {carbon_kg} kg")
            return carbon_kg
        else:
            print("Error:", resp.status_code, resp.text)
            return 0
    else:
        print("Invalid choice.")

def get_electricity_emissions_api(country, state, consumption_kwh):
    payload = {
        "type": "electricity",
        "electricity_unit": "kwh",
        "electricity_value": consumption_kwh,
        "country": country,
        "state": state
    }
    response = requests.post('https://www.carboninterface.com/api/v1/estimates', headers=HEADERS, json=payload)

    if response.status_code == 201:
        carbon_kg = response.json()['data']['attributes']['carbon_kg']
        print(f"The estimated CO₂ emissions: {carbon_kg} kg")
        return carbon_kg
    else:
        print("Error:", response.status_code, response.text)
        return 0

def get_clothing_emissions(spending_usd):
    emissions_kg = (spending_usd / 100) * 20 # Approx. 20 kg CO₂ per $100 spent
    print(f"The estimated CO₂ emmissions for clothing: {emissions_kg:.2f} kg")
    return emissions_kg


def get_electronics_emissions(spending_usd):
    emissions_kg = (spending_usd / 100) * 75 # Approx. 75 kg CO₂ per $100 spent (average)
    print(f"The estimated CO₂ emmissions for electronics: {emissions_kg:.2f} kg")
    return emissions_kg

def get_food_emissions(diet_type):
    factors = {
        "meat": 3300,
        "vegetarian": 1700,
        "vegan": 1500
    }
    emissions_kg = factors.get(diet_type.lower(), 3300)
    print(f"The estimated CO₂ emmissions for food diet: {emissions_kg:.2f} kg")
    return emissions_kg

def main():
    print("Welcome to 4Earths' Carbon Footprint Calculator")
    print("0. Estimate all emmissions")
    print("1. Estimate flight emissions")
    print("2. Estimate vehicle emissions")
    print("3. Estimate electricity emissions")
    print("4. Estimate clothing emissions")
    print("5. Estimate electronics emissions")
    print("6. Estimate food emissions")
    choice = input("Please choose an option (0/1/2/...):: ")

    if choice == "0":
        departure_airport = input("Enter the departure airport ICAO code (Example: JFK):: ")
        arrival_airport = input("Enter the arrival airport ICAO code (Example: SEA):: ")
        passengers_count = 1
        make = input("Enter the vehicle make (Example: Toyota):: ").capitalize()
        country = input("Enter country code (Example: US):: ").upper()
        state = input("Enter state code (Example: CA):: ").upper()
        consumption_kwh = float(input("Enter monthly electricity consumption (in kWh):: "))
        clothing_cost = float(input("Enter the monthly clothing expenditure (in USD):: "))
        electronics_cost = float(input("Enter monthly electronics expenditure in USD:: "))
        diet_type = input("Enter your diet type (omnivore/vegetarian/vegan), default omnivore:: ") or "omnivore"
        print("_______________________________________________________________________")
        total_emmissions = + get_vehicle_emissions_api(make) + get_flight_emissions_api(departure_airport, arrival_airport, passengers_count) + get_electricity_emissions_api(country, state, consumption_kwh) + get_clothing_emissions(clothing_cost) + get_electronics_emissions(electronics_cost) + get_food_emissions(diet_type)
        print("_______________________________________________________________________")
        print("The total estimated CO₂ emmissions for all categories is :", total_emmissions, "kg")
        print("_______________________________________________________________________")

    elif choice == "1":
        departure_airport = input("Enter the departure airport ICAO code (Example: JFK):: ")
        arrival_airport = input("Enter the arrival airport ICAO code (Example: SEA):: ")
        passengers_count = 1
        print("_______________________________________________________________________")
        get_flight_emissions_api(departure_airport, arrival_airport, passengers_count)

    elif choice == "2":
        make = input("Enter the vehicle make (Example: Toyota):: ").capitalize()
        print("_______________________________________________________________________")
        get_vehicle_emissions_api(make)
    elif choice == "3":
        country = input("Enter country code (Example: US):: ").upper()
        state = input("Enter state code (Example: CA):: ").upper()
        consumption_kwh = float(input("Enter monthly electricity consumption (in kWh):: "))
        print("_______________________________________________________________________")
        get_electricity_emissions_api(country, state, consumption_kwh)

    elif choice == "4":
        clothing_cost = float(input("Enter the monthly clothing expenditure (in USD):: "))
        print("_______________________________________________________________________")
        get_clothing_emissions(clothing_cost)

    elif choice == "5":
        electronics_cost = float(input("Enter monthly electronics expenditure in USD:: "))
        print("_______________________________________________________________________")
        get_electronics_emissions(electronics_cost)

    elif choice == "6":
        diet_type = input("Enter your diet type (omnivore/vegetarian/vegan), default omnivore:: ") or "omnivore"
        print("_______________________________________________________________________")
        get_food_emissions(diet_type)

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()

