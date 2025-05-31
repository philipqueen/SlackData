from sqlmodel import Field, Relationship, SQLModel

class BaseBrands(SQLModel):
    """
    Base class for brands/manufacturers.
    """
    name: str = Field(index=True)
    country: str | None = None
    year_founded: int | None = None
    active: bool = True
    slackline_focused: bool = True
    website: str | None = None
    socials: str | None = None
    description: str | None = None
    notes: str | None = None

class Brand(BaseBrands, table=True):
    id: int | None = Field(default=None, primary_key=True)
    webbing: list["Webbing"] = Relationship(back_populates="brand")

class BrandCreate(BaseBrands):
    """
    Model for creating a new brand entry.
    """
    
    class Config:
        exclude = ["id"]
        validate_assignment = True

class BrandUpdate(BaseBrands):
    """
    Model for updating an existing brand entry.
    """
    
    class Config:
        exclude = ["id"]
        validate_assignment = True
        extra = "forbid"