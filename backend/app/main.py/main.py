from typing import List

from db.database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Query
from models.models import Base, Bid, Organization, Review, Tender
from schemas import (BidCreate, BidResponse, ReviewResponse, TenderCreate,
                     TenderResponse)
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/api/ping")
def ping():
    return "ok"


@app.post("/api/tenders/new", response_model=TenderResponse)
def create_tender(tender: TenderCreate, db: Session = Depends(get_db)):
    db_tender = Tender(
        name=tender.name,
        description=tender.description,
        service_type=tender.service_type,
        status=tender.status,
        organization_id=tender.organization_id,
        creator_username=tender.creator_username
    )
    db.add(db_tender)
    db.commit()
    db.refresh(db_tender)
    return db_tender


@app.get("/api/tenders", response_model=List[TenderResponse])
def get_tenders(db: Session = Depends(get_db)):
    tenders = db.query(Tender).all()
    return tenders


@app.get("/api/tenders/my", response_model=List[TenderResponse])
def get_my_tenders(username: str, db: Session = Depends(get_db)):
    tenders = db.query(Tender).filter(Tender.creator_username == username).all()
    return tenders


@app.patch("/api/tenders/{tender_id}/edit", response_model=TenderResponse)
def edit_tender(tender_id: int, updated_data: TenderCreate, db: Session = Depends(get_db)):
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    
    tender.name = updated_data.name
    tender.description = updated_data.description
    db.commit()
    db.refresh(tender)
    return tender


@app.post("/api/bids/new", response_model=BidResponse)
def create_bid(bid: BidCreate, db: Session = Depends(get_db)):
    db_bid = Bid(
        name=bid.name,
        description=bid.description,
        status=bid.status,
        tender_id=bid.tender_id,
        organization_id=bid.organization_id,
        creator_username=bid.creator_username
    )
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid


@app.get("/api/bids/my", response_model=List[BidResponse])
def get_my_bids(username: str, db: Session = Depends(get_db)):
    bids = db.query(Bid).filter(Bid.creator_username == username).all()
    return bids


@app.get("/api/bids/{tender_id}/list", response_model=List[BidResponse])
def get_tender_bids(tender_id: int, db: Session = Depends(get_db)):
    bids = db.query(Bid).filter(Bid.tender_id == tender_id).all()
    return bids


@app.patch("/api/bids/{bid_id}/edit", response_model=BidResponse)
def edit_bid(bid_id: int, updated_data: BidCreate, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    
    bid.name = updated_data.name
    bid.description = updated_data.description
    db.commit()
    db.refresh(bid)
    return bid


@app.put("/api/bids/{bid_id}/rollback/{version}", response_model=BidResponse)
def rollback_bid(bid_id: int, version: int, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id, Bid.version == version).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Version not found")
    
    bid.version += 1
    db.commit()
    db.refresh(bid)
    return bid


@app.get("/api/bids/{tender_id}/reviews", response_model=List[ReviewResponse])
def get_reviews(
    tender_id: int,
    authorUsername: str = Query(...),
    organizationId: int = Query(...),
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(Organization.id == organizationId).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    user_reviews = db.query(Review).join(Bid).filter(Bid.tender_id == tender_id, Bid.creator_username == authorUsername).all()
    return user_reviews


@app.post("/api/reviews/new", response_model=ReviewResponse)
def leave_review(bid_id: int, reviewer_id: int, comment: str, rating: int, db: Session = Depends(get_db)):
    review = Review(bid_id=bid_id, reviewer_id=reviewer_id, comment=comment, rating=rating)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
