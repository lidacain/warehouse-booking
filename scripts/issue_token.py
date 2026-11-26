import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import jwt
from config.settings import get_settings


USERS = {
    "astana-motors": {"sub": "u-am-1", "org_id": 1, "org_type": "company"},
    "distributor-a": {"sub": "u-da-1", "org_id": 2, "org_type": "distributor"},
    "distributor-b": {"sub": "u-db-1", "org_id": 3, "org_type": "distributor"},
}


def main() -> None:
    key = sys.argv[1]
    payload = {
        **USERS[key],
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7),
    }
    print(jwt.encode(payload, get_settings().JWT_SECRET, algorithm="HS256"))


if __name__ == "__main__":
    main()
