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
        tech_string = ",".join(technologies) if technologies and isinstance(technologies, list) else ""
        
        analysis = Analysis(
            input_text=text,
            credibility_score=score,
            verdict=verdict,
            technologies=tech_string,
            reasoning=reasoning,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        print(f"Saved analysis with ID: {analysis.id}")
        return analysis.id
    except Exception as e:
        print(f"Error saving analysis: {e}")
        db.rollback()
        raise
    finally:
        db.close()
