from bloqit_api.data.json_db import load_bloqs, load_lockers, load_rents

print("Bloqs:")
print(load_bloqs(), "\n")

print("Lockers:")
print(load_lockers(), "\n")

print("Rents:")
print(load_rents(), "\n")