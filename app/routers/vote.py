from fastapi import APIRouter, Depends, HTTPException, status
from .. import schema, database, models, oauth
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schema.Vote,
            db: Session = Depends(database.get_db),
            current_user: int = Depends(oauth.get_current_user)):
    # cari data post yg ingin divote
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    # CEK JIKA DATA POST YG INGIN DI VOTE TIDAK ADA
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post dengan id {vote.post_id} tidak ada')
    # cari id post & id user dalam tabel vote yg = id vote yg dikunjungi untuk diberi vote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    # ambil semua data dari query diatas
    data = vote_query.first()
    # jika vote pd post bernilai 1 artinya user ingin add vote (like/subscribe)
    if vote.dir == 1:
        # dan jika user telah vote postnya
        if data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user dengan id {current_user.id} telah vote post ini ({vote.post_id})")
        # user blm vote  dan ingin vote post nya
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"pesan":"post berhsl di vote"}
    # jika user ingin menghapus/ vote (dir) = 0
    else:
        # jika post yg ingin divote tidak ada
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote doesnt exist")
        # hapus vote nya (unlike/unsubscribe)
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"pesan":"vote berhsl dihapus"}