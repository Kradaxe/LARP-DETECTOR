from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.resume_extractor import ResumeExtractor
from app.services.resume_analysis_service import ResumeAnalysisService
from app.schemas.response_schema import ResumeAnalysisResponse

router = APIRouter()


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze a resume file (PDF or DOCX) for technical credibility.
    
    This endpoint:
    1. Extracts text from the uploaded resume
    2. Splits text into individual technical claims
    3. Analyzes each claim using the existing analysis pipeline
    4. Returns overall credibility score and per-claim analysis
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in ['pdf', 'docx']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}. Only PDF and DOCX are supported."
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Extract text from file
        text = ResumeExtractor.extract_text(file_content, file_extension)
        
        if not text or len(text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from the resume. Please ensure the file contains readable text."
            )
        
        # Analyze the resume
        result = await ResumeAnalysisService.analyze_resume(text)
        
        return ResumeAnalysisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during resume analysis: {str(e)}"
        )
