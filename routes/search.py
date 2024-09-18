from fastapi import APIRouter,HTTPException,status,Request
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from models import SearchResponse,Search,SearchResults

router = APIRouter()

es=Elasticsearch("http://localhost:9200/")
client=MongoClient("mongodb://localhost:27017")
db=client['news_database']
users_collection=db['users']

@router.post("/search",response_model=SearchResponse)
async def search_document(search_request: Search,user_id:int):


    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Check for User_id in headers")

    user_data=users_collection.find_one({"user_id":user_id})

    if user_data:
        if user_data['request_count']>=5:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Too Many Request")
        else:
            users_collection.update_one({"user_id":user_id},{"$inc": {"request_count": 1}})
    else:
        users_collection.insert_one({"user_id":user_id,"request_count":1})

    body = {
        "query": {
            "more_like_this": {
                "fields": ["title", "content"],
                "like": search_request.text,
                "min_term_freq": 1,
                "min_doc_freq": 1
            }
        }
    }

    try:
        response = es.search(index="documents",body=body)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error with ElasticSearch")

    hits=response["hits"]["hits"]
    results=[]
    seen_ids=set()

    for hit in hits:
        score=hit["_score"]
        article_id=hit["_id"]
        if article_id not in seen_ids and score>=search_request.threshold:
            results.append(SearchResults(id=hit["_id"],content=hit["_source"]["content"],score=score))
        if len(results)==search_request.top_k:
            break
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No result found")

    return SearchResponse(
        query=search_request.text,
        results=results,
        top_k=search_request.top_k,
        threshold=search_request.threshold
    )
