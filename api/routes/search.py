from fastapi import APIRouter, Depends, HTTPException
import time

from api.deps import get_engine
from api.schemas.search import SearchRequest, SearchResponse, SearchResult


router = APIRouter(prefix="/api/v1", tags=["search"])


@router.get("/search", response_model=SearchResponse)
def search(
    params: SearchRequest = Depends(),
    engine = Depends(get_engine)
):
    start = time.time()

    if not params.q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = engine.search(params.q, params.k)

    response_results = [
        SearchResult(doc_id=d, title=t, score=s)
        for d, t, s in results
    ]

    return SearchResponse(
        query=params.q,
        k=params.k,
        took_ms=round((time.time() - start) * 1000, 2),
        results=response_results
    )
