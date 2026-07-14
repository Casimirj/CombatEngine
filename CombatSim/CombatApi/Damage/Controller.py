from pathlib import Path
from typing import cast

from fastapi import Body, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, PlainTextResponse

from CombatSim.CombatApi.Environment import Config

from CombatSim.CombatApi.Damage.Models.calculate_hit import CalculateHitInput
from CombatSim.CombatApi.Damage.Models.calculate_hit import CalculateHitOutput
from CombatSim.CombatApi.Damage.Services.CalculateHitService import calculate_hit_damage

from CombatSim.CombatApi.Damage.Models.get_combat_calcs import GetCombatCalcsInput
from CombatSim.CombatApi.Damage.Models.get_combat_calcs import GetCombatCalcsOutput
from CombatSim.CombatApi.Damage.Services.GetCombatCalcsService import get_combat_calcs

from CombatSim.CombatApi.Damage.Models.test import TestInput, TestOutput
from CombatSim.CombatApi.Damage.Services.TestService import run_test


CSS_PATH = Path(__file__).with_name("DamageController.css")
OPENAPI_URL = "/openapi.json"


app = FastAPI(
    title="Damage Controller",
    description="Small API for damage tooling and local testing.",
    version="1.0.0",
    openapi_url=OPENAPI_URL,
    docs_url=None,
    redoc_url=None,
)


@app.get("/test", response_class=PlainTextResponse)
def test() -> str:
    return "hello world"


@app.post("/calculate_hit", response_model=CalculateHitOutput)
def calculate_hit(
    payload: CalculateHitInput = Body(
        ...,
        openapi_examples={
            "custom_scythe_maiden": {
                "summary": "Custom Scythe Maiden",
                "value": {
                    "Loadout": "Custom",
                    "Weapon": "Scythe of Vitur",
                    "Monster": {
                        "Name": "Maiden",
                        "ReduceDefense": True,
                        "Defense": 80,
                    },
                    "Scale": 3,
                    "Gear": {
                        "Pieces": ["Salve (e)"],
                        "Prayer": "Piety",
                        "Boosts": ["Super combat"]
                    },
                    "PlayerLevels": {
                        "attack_level": 99,
                        "strength_level": 99
                    },
                },
            },
            "named_loadout": {
                "summary": "Named Loadout",
                "value": {
                    "Loadout": "OathTorvaRancour",
                    "Weapon": "Scythe of Vitur",
                    "Monster": {
                        "Name": "Maiden",
                        "ReduceDefense": True,
                        "Defense": 80,
                    },
                    "Scale": 3,
                },
            },
        },
    ),
) -> CalculateHitOutput:
    try:
        damage, monster_defense = calculate_hit_damage(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CalculateHitOutput(damage=damage, monster_defense=monster_defense)


@app.post("/get_combat_calcs", response_model=GetCombatCalcsOutput)
def combat_calcs(
    payload: GetCombatCalcsInput = Body(
        ...,
        openapi_examples={
            "custom_scythe_maiden": {
                "summary": "Custom Scythe Maiden",
                "value": {
                    "Loadout": "Custom",
                    "Weapon": "Scythe of Vitur",
                    "Monster": {
                        "Name": "Maiden",
                        "ReduceDefense": True,
                        "Defense": 80,
                    },
                    "Scale": 3,
                    "Gear": {
                        "Pieces": ["Salve (e)"],
                        "Prayer": "Piety",
                        "Boosts": ["Super combat"]
                    },
                    "PlayerLevels": {
                        "attack_level": 99,
                        "strength_level": 99
                    },
                },
            },
            "named_loadout": {
                "summary": "Named Loadout",
                "value": {
                    "Loadout": "OathTorvaRancour",
                    "Weapon": "Scythe of Vitur",
                    "Monster": {
                        "Name": "Maiden",
                        "ReduceDefense": True,
                        "Defense": 80,
                    },
                    "Scale": 3,
                },
            },
        },
    ),
) -> GetCombatCalcsOutput:
    try:
        return get_combat_calcs(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/run_test", response_model=TestOutput)
def run_combat_test(
    payload: TestInput = Body(
        ...,
        openapi_examples={
            "default": {
                "summary": "Scythe Bloat",
                "value": {
                    "Loadout": "OathTorvaRancour",
                    "Weapon": "Scythe of Vitur",
                    "Monster": {
                        "Name": "Bloat",
                        "ReduceDefense": False,
                    },
                    "Scale": 5,
                },
            },
        },
    ),
) -> TestOutput:
    try:
        return run_test(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


if not Config.is_prod:

    @app.get("/docs", include_in_schema=False)
    def docs() -> HTMLResponse:
        openapi_url = cast(str, app.openapi_url)
        html = get_swagger_ui_html(
            openapi_url=openapi_url,
            title=f"{app.title} - Swagger UI",
            swagger_ui_parameters={"tryItOutEnabled": True, "displayRequestDuration": True},
        )
        dark_css = CSS_PATH.read_text(encoding="utf-8")
        js = """
        <script>
        const obs = new MutationObserver(() => {
            const dur = document.querySelector('.response-duration');
            const wrapper = document.querySelector('.responses-wrapper');
            if (!dur || !wrapper) return;
            if (wrapper.previousElementSibling === dur) return;
            dur.remove();
            wrapper.parentElement.insertBefore(dur, wrapper);
        });
        obs.observe(document.body, { childList: true, subtree: true });
        </script>
        """
        style_tag = f"<style>{dark_css}</style>"
        body = html.body or b""
        content = body.decode("utf-8").replace("</head>", f"{style_tag}{js}</head>")
        return HTMLResponse(content=content)
