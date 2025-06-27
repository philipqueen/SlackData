import json
from pathlib import Path

from sqlmodel import select

from slack_data.database import SessionDep
from slack_data.models.brands import Brand, BrandCreate
from slack_data.models.rollers import SliderType, Roller, RollerCreate
from slack_data.utilities.currencies import get_currency
from slack_data.utilities.materials import MetalMaterial, RollerMaterial


ROLLER_FILE = Path(__file__).parent.parent.parent / "rollers.json"

def load_rollers_json() -> list[dict]:
    """
    Load the rollers data from the `rollers.json` file.
    """
    if not ROLLER_FILE.exists():
        raise FileNotFoundError(f"rollers file not found: {ROLLER_FILE}")

    with open(ROLLER_FILE, "r", encoding="utf-8") as file:
        roller_data = json.load(file)

    return roller_data

def clean_roller_data(rollers: dict) -> dict:
    """
    Clean the roller data by removing any keys with None values.
    """
    cleaned_rollers = rollers
    for key, value in rollers.items():
        if key in {"width", "weight"} and value == "":
            cleaned_rollers[key] = 0
        elif key not in {"name", "brand", "materialType"} and value == "":
            cleaned_rollers[key] = None
        elif key == "isa_approved":
            cleaned_rollers[key] = bool(value) if isinstance(value, str) else value
            if value is None:
                cleaned_rollers[key] = False
        else:
            cleaned_rollers[key] = str(value) if value is not None else None
    return cleaned_rollers

def add_rollers_to_db(rollers: list[dict], session: SessionDep) -> None:
    """
    Add the loaded roller and brand data to the database session.
    """


    for roller in rollers:
        brand_id = get_brand(session, roller)

        if (currency := roller.get("currency")) is not None:
            currency = get_currency(currency)

        roller_create = RollerCreate(
            name=str(roller.get("name")),
            brand_id=brand_id,
            material=get_metal_material(str(roller.get("materialType", ""))),
            roller_material=get_roller_material(str(roller.get("roller_material", ""))),
            width=roller.get("width", None),
            weight=float(roller.get("weight", 0)),
            breaking_strength=roller.get("mbs"),
            slider_type=get_slider_type(str(roller.get("slider_type", ""))),
            isa_certified=roller.get("isa_approved", False),
            price=roller.get("price"),
            currency=currency,
        )
        db_roller = Roller.model_validate(roller_create)
        db_roller.brand = session.get(Brand, brand_id)
        print(f"Adding roller: {db_roller.name} by {db_roller.brand.name}")
        session.add(db_roller)

    session.commit()
    session.refresh(db_roller)

def get_brand(session: SessionDep, roller: dict) -> int:
    brand_name = roller.get("manufacturer") or roller.get("brand")

    if not brand_name:
        raise ValueError("Brand name is missing from roller data.")
    
    brand_name = str(brand_name).strip()

    statement = select(Brand.id).where(Brand.name == brand_name)
    result = session.exec(statement).first()

    if result is None:
        brand_create = BrandCreate(name=brand_name)
        db_brand = Brand.model_validate(brand_create)
        print(f"Adding brand: {db_brand.name}")
        session.add(db_brand)
        session.commit()
        session.refresh(db_brand)
        brand_id = db_brand.id
    else:
        brand_id = result

    if brand_id is None:
        raise ValueError(f"Brand ID for '{brand_name}' could not be determined.")
        
    return brand_id

def get_slider_type(slider_type: str) -> SliderType:
    """
    Convert the material string to a Material enum.
    """
    slider_type = slider_type.lower()
    if "moving plates" in slider_type:
        return SliderType.MovingPlates
    elif "carabiner" in slider_type:
        return SliderType.Carabiner
    elif "locking carabiner" in slider_type:
        return SliderType.LockingCarabiner
    else:
        return SliderType.Other
    
def get_metal_material(material: str) -> MetalMaterial:
    """
    Convert the material string to a MetalMaterial enum.
    """
    material = material.lower()
    if "aluminum" in material:
        return MetalMaterial.ALUMINUM
    elif "stainless steel" in material:
        return MetalMaterial.STAINLESS_STEEL
    elif "steel" in material:
        return MetalMaterial.STEEL
    elif "titanium" in material:
        return MetalMaterial.TITANIUM
    else:
        return MetalMaterial.OTHER
    
def get_roller_material(roller_material: str) -> RollerMaterial:
    """
    Convert the roller material string to a RollerMaterial enum.
    """
    roller_material = roller_material.lower()
    if "aluminum" in roller_material:
        return RollerMaterial.ALUMINUM
    elif "stainless steel" in roller_material:
        return RollerMaterial.STAINLESS_STEEL
    elif "steel" in roller_material:
        return RollerMaterial.STEEL
    elif "plastic" in roller_material or "nylon" in roller_material:
        return RollerMaterial.PLASTIC
    else:
        return RollerMaterial.OTHER


def load_rollers(session: SessionDep) -> None:
    """
    Load the roller data from the JSON file and add it to the database.
    """
    rollers = load_rollers_json()
    cleaned_rollers = [clean_roller_data(roller) for roller in rollers]

    add_rollers_to_db(cleaned_rollers, session)
    print(f"Added {len(cleaned_rollers)} rollers to the database.")

if __name__ == "__main__":
    rollers = load_rollers_json()
    print(f"Loaded {len(rollers)} rollers from {ROLLER_FILE}")
    print(rollers[:1])
