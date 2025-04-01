"""
This script uploads a QF GUI project to the BP3D system using parameters 
provided in a JSON file. 

Args:
    gui_dir (str): QF GUI project directory.

"""

import bp3d
import json
import sys
from datetime import datetime


gui_dir = sys.argv[1]

date = datetime.today().strftime('%Y-%m-%d')

# Load parameters from JSON file
with open(gui_dir + 'bp3d_parameters.json', 'r') as json_file:
    loaded_parameters = json.load(json_file)

# Assign loaded parameters - parameters can be a list of values
site = loaded_parameters["site"]
c = bp3d.Client(user=loaded_parameters["user"], password=loaded_parameters["password"])
wind_speed = loaded_parameters["wind_speed"]
wind_direction = loaded_parameters["wind_direction"]

ensemble_name = f'{site} {date} updated ignition'

path = gui_dir

#upload fuels
qf_ensemble = c.import_qfgui_project(name = ensemble_name, path = path)

#add ignition
pattern = f'{path}/ignition_pattern.json'
ign  = qf_ensemble.add_ignition(dat = f'{path}/ignite.dat', pattern = pattern)

#add environmental conditions
qf_ensemble.add_runs(
                ignition=ign,
                wind_speed=wind_speed,
                wind_direction=wind_direction,
                replace=True)

#run ensemble
qf_ensemble.execute()