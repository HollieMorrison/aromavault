from typing import Dict, List

try:
    import storage
except Exception as e:  # pragma: no cover
    storage = None  # if storage import fails we simply skip

SAMPLES: List[Dict] = [
    {"name": "Rose Dusk", "brand": "Floral", "price": 55, "notes": ["rose", "musk"], "stock": 3},
    {
        "name": "Amber Trail",
        "brand": "Nocturne",
        "price": 72,
        "notes": ["amber", "vanilla", "tonka"],
        "stock": 2,
    },
    {
        "name": "Ocean Mist",
        "brand": "Aqua",
        "price": 49,
        "notes": ["marine", "citrus", "salt"],
        "stock": 5,
    },
    {
        "name": "Vetiver Line",
        "brand": "Terra",
        "price": 67,
        "notes": ["vetiver", "grapefruit", "pepper"],
        "stock": 4,
    },
    {
        "name": "Jasmine Night",
        "brand": "Floral",
        "price": 58,
        "notes": ["jasmine", "white musk"],
        "stock": 3,
    },
    {
        "name": "Patchouli Drift",
        "brand": "Terra",
        "price": 61,
        "notes": ["patchouli", "woods"],
        "stock": 2,
    },
]


def install(app):
    """Seed once per dyno, on the first incoming request, if DB is empty."""
    if storage is None:
        return
    app.config.setdefault("SEEDED_ONCE", False)

    def maybe_seed():
        if app.config.get("SEEDED_ONCE", False):
            return
        try:
            if len(storage.list_perfumes()) == 0:
                for p in SAMPLES:
                    storage.add_perfume(p)
                app.logger.info(f"[seed] Silent seeded {len(SAMPLES)} perfumes")
        except Exception as e:  # pragma: no cover
            app.logger.warning(f"[seed] Silent seed skipped: {e}")
        finally:
            app.config["SEEDED_ONCE"] = True

    @app.before_request
    def _ensure_seeded_once():
        maybe_seed()
