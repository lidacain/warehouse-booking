import httpx
from config.settings import get_settings


ACCOUNTING_TIMEOUT = httpx.Timeout(connect=3.0, read=10.0, write=5.0, pool=5.0)


class AccountingClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    async def lookup_vins(self, vins: list[str]) -> set[str]:
        async with httpx.AsyncClient(base_url=self._base_url, timeout=ACCOUNTING_TIMEOUT) as client:
            response = await client.post("/api/v1/vehicles/lookup", json={"vins": vins})
            response.raise_for_status()
            return set(response.json()["found"])


def get_accounting_client() -> AccountingClient:
    return AccountingClient(get_settings().ACCOUNTING_URL)
