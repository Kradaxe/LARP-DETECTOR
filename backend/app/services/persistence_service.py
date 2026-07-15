from app.db.database import SessionLocal
from app.models.analysis import Analysis


def save_analysis(
    text,
    score,
    verdict,
    technologies,
    reasoning
):

    db = SessionLocal()
    try:
        analysis = Analysis(
            input_text=text,
            credibility_score=score,
            verdict=verdict,
            technologies=",".join(technologies),
            reasoning=reasoning,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis.id
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
