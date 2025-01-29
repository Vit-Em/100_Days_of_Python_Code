import random

states_of_america = ["Delaware", "Pennsylvania", "New Jersey", "Georgia", "Connecticut", "Massachusetts", "Maryland", "South Carolina", "New Hampshire", "Virginia", "New York", "North Carolina", "Rhode Island", "Vermont", "Kentucky", "Tennessee", "Ohio", "Louisiana", "Indiana", "Mississippi", "Illinois", "Alabama", "Maine", "Missouri", "Arkansas", "Michigan", "Florida", "Texas", "Iowa", "Wisconsin", "California", "Minnesota", "Oregon", "Kansas", "West Virginia", "Nevada", "Nebraska", "Colorado", "North Dakota", "South Dakota", "Montana", "Washington", "Idaho", "Wyoming", "Utah", "Oklahoma", "New Mexico", "Arizona", "Alaska", "Hawaii"]

def state_mixer():
    return f"{random.choice(states_of_america)}-{random.choice(states_of_america)}istan"

def state_population_generator():
    return f"{random.choice(states_of_america)} has a population of {random.randint(1, 1000000)} squirrels"

def state_fact_generator():
    facts = [
        "is known for its underground cheese mines",
        "has a law that requires all citizens to wear sombreros on Tuesdays",
        "has a yearly festival where people race on giant hamster wheels",
        "has declared pizza as its official state vegetable",
        "has a town where it's illegal to frown"
    ]
    return f"{random.choice(states_of_america)} {random.choice(facts)}"

print(f"The first state is: {states_of_america[0]}")
states_of_america.append("Angelaland")
print(f"We added a new state: {states_of_america[-1]}")

print("\nFun with states:")
print(f"New mixed state: {state_mixer()}")
print(state_population_generator())
print(state_fact_generator())
