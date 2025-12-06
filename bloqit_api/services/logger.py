from datetime import datetime
import os
import json

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

#attaches log entry for rents, lockers and bloqs
def log_change(entity: str, entity_id: str, old: dict, new: dict, action: str):
    
    log_file = os.path.join(LOG_DIR, f"{entity}.log")

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "entity_id": entity_id,
        "action": action,
        "old": old,
        "new": new
    }
    
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")