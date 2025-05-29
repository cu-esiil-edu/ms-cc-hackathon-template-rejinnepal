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

def suggest_reduction_plan(total_emissions, emissions_breakdown):

    reduction = 0

    sorted_sources = sorted(emissions_breakdown.items(), key=lambda x: x[1], reverse=True)

    for source, amount in sorted_sources:
        if amount < total_emissions * 0.05:
            continue

        if source == "flight":
            print(f"Your Flight travel is a major contributor ({amount} kg).")
            print("Here's a suggestion for you: Fly less often, opt for trains/buses, or offset flights.\n")
            reduction += amount * 0.4

        elif source == "vehicle":
            print(f"Your driving contributes significantly ({amount} kg).")
            print("Here's a suggestion for you: Carpool, walk/bike more, or consider an electric vehicle.\n")
            reduction += amount * 0.3

        elif source == "electricity":
            print(f"Your electricity use is high ({amount} kg).")
            print("Here's a suggestion for you: Switch to LEDs, unplug devices, or try renewable providers.\n")
            reduction += amount * 0.25

        elif source == "clothing":
            print(f"Your clothing purchases emit ({amount} kg).")
            print("Here's a suggestion for you: Buy fewer or second-hand clothes, and avoid fast fashion.\n")
            reduction += amount * 0.3

        elif source == "electronics":
            print(f"Your electronics spending leads to ({amount} kg) CO₂.")
            print("Here's a suggestion for you: Upgrade less often and repair instead of replacing.\n")
            reduction += amount * 0.3

        elif source == "food":
            print(f"Your diet contributes ({amount} kg).")
            print("Here's a suggestion for you: Reduce red meat, try plant-based meals more often.\n")
            reduction += amount * 0.2

    new_total = total_emissions - reduction

    print(f"Your potential reduction could be: {reduction} kg CO₂")
    print(f"Your new estimated footprint: {new_total} kg CO₂")
    print(f"That is about a {100 * reduction / total_emissions}% decrease in emissions!\n")

    return new_total

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

    total_emissions = 0
    flight_emissions = 0
    vehicle_emissions = 0
    electricity_emissions = 0
    clothing_emissions = 0
    electronics_emissions = 0
    food_emissions = 0

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
        
        vehicle_emissions = get_vehicle_emissions_api(make)
        flight_emissions = get_flight_emissions_api(departure_airport, arrival_airport, passengers_count)
        electricity_emissions = get_electricity_emissions_api(country, state, consumption_kwh)
        clothing_emissions = get_clothing_emissions(clothing_cost)
        electronics_emissions = get_electronics_emissions(electronics_cost)
        food_emissions = get_food_emissions(diet_type)

        total_emissions = vehicle_emissions + flight_emissions + electricity_emissions + clothing_emissions + electronics_emissions + food_emissions

        print("_______________________________________________________________________")
        print("The total estimated CO₂ emmissions for all categories is :", total_emissions, "kg")
        print("_______________________________________________________________________")

    elif choice == "1":
        departure_airport = input("Enter the departure airport ICAO code (Example: JFK):: ")
        arrival_airport = input("Enter the arrival airport ICAO code (Example: SEA):: ")
        passengers_count = 1
        print("_______________________________________________________________________")
        flight_emissions = get_flight_emissions_api(departure_airport, arrival_airport, passengers_count)
        total_emissions = flight_emissions

    elif choice == "2":
        make = input("Enter the vehicle make (Example: Toyota):: ").capitalize()
        print("_______________________________________________________________________")
        vehicle_emissions = get_vehicle_emissions_api(make)
        total_emissions = vehicle_emissions

    elif choice == "3":
        country = input("Enter country code (Example: US):: ").upper()
        state = input("Enter state code (Example: CA):: ").upper()
        consumption_kwh = float(input("Enter monthly electricity consumption (in kWh):: "))
        print("_______________________________________________________________________")
        electricity_emissions = get_electricity_emissions_api(country, state, consumption_kwh)
        total_emissions = electricity_emissions

    elif choice == "4":
        clothing_cost = float(input("Enter the monthly clothing expenditure (in USD):: "))
        print("_______________________________________________________________________")
        clothing_emissions = get_clothing_emissions(clothing_cost)
        total_emissions = clothing_emissions

    elif choice == "5":
        electronics_cost = float(input("Enter monthly electronics expenditure in USD:: "))
        print("_______________________________________________________________________")
        electricity_emissions = get_electronics_emissions(electronics_cost)
        total_emissions = electricity_emissions

    elif choice == "6":
        diet_type = input("Enter your diet type (omnivore/vegetarian/vegan), default omnivore:: ") or "omnivore"
        print("_______________________________________________________________________")
        food_emissions = get_food_emissions(diet_type)
        total_emissions = food_emissions

    else:
        print("Invalid choice.")

    print("_______________________________________________________________________")
    print("_______________________________________________________________________")
    print("Reduced Emissions Plan Details")
    print("_______________________________________________________________________")
    print("_______________________________________________________________________")

    emissions_breakdown = {
        "vehicle": vehicle_emissions,
        "flight": flight_emissions,
        "electricity": electricity_emissions,
        "clothing": clothing_emissions,
        "electronics": electronics_emissions,
        "food": food_emissions
    }

    total_emissions = sum(emissions_breakdown.values())


    suggest_reduction_plan(total_emissions, emissions_breakdown)

if __name__ == "__main__":
    main()

