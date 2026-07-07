import os

import uvicorn


if __name__ == "__main__":
    port = int(os.getenv("DAMAGE_API_PORT", "8001"))
    uvicorn.run(
        "combat_engine.Api.Damage.Controller:app",
        host="127.0.0.1",
        port=port,
        reload=True,
    )
