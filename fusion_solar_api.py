#retrieve current power production
from fusion_solar_py.client import FusionSolarClient

client = FusionSolarClient(user, 
                           pw,
                           huawei_subdomain="region02eu5")

# get the stats
stats = client.get_power_status()

# print all stats
print(f"Current power: {stats.current_power_kw} kW")
print(f"Total energy today: {stats.energy_today_kwh} kWh")
print(f"Total energy: {stats.energy_kwh} kWh")

client.log_out()

#%%
#retreive power production throughout the day
from fusion_solar_py.client import FusionSolarClient

client = FusionSolarClient(user, 
                           pw,
                            huawei_subdomain="region02eu5")
# get the plant ids
plant_ids = client.get_plant_ids()

plant_a_data = client.get_plant_stats(plant_ids[0])
plant_b_data = client.get_plant_stats(plant_ids[1])

plant_a_power=plant_a_data['productPower']
plant_b_power=plant_b_data['productPower']

client.log_out()