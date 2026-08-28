from fastapi import FastAPI

from app.database import Base, engine

from app.models.party import Party
from app.models.spatial_unit import SpatialUnit
from app.models.rrr import RRR
from app.models.baunit import BAUnit
from app.models.document import Document
from app.models.rrr_document import RRRDocument
from app.models.mutation import Mutation
from app.models.mutation_history import MutationHistory

from app.routes.parties import router as party_router
from app.routes.spatial_units import router as spatial_unit_router
from app.routes.rrr import router as rrr_router
from app.routes.baunits import router as baunit_router
from app.routes.documents import router as document_router
from app.routes.rrr_documents import router as rrr_document_router
from app.routes.mutations import router as mutation_router
from app.routes.legal_summary import router as legal_summary_router



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(party_router)
app.include_router(spatial_unit_router)
app.include_router(rrr_router)
app.include_router(baunit_router)
app.include_router(document_router)
app.include_router(rrr_document_router)
app.include_router(mutation_router)
app.include_router(legal_summary_router)


@app.get("/")
def root():
    return {
        "message": "Group 4 Legal Ledger API is running"
    }