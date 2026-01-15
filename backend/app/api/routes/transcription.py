"""API routes for transcription endpoints"""
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.business.transcription_service import TranscriptionBusinessService
from app.services.word_export_service import WordExportService
from app.models.schemas import TranscriptionResponse, ActionItem, ExportRequest

router = APIRouter(prefix="/api", tags=["transcription"])


def get_transcription_service() -> TranscriptionBusinessService:
    """Dependency injection for transcription service"""
    return TranscriptionBusinessService()


def get_word_export_service() -> WordExportService:
    """Dependency injection for word export service"""
    return WordExportService()


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    transcription_service: TranscriptionBusinessService = Depends(get_transcription_service)
):
    """
    Upload and process an audio file (mp3/wav)
    
    Returns transcription, summary, participants, decisions, and action items
    """
    try:
        result = await transcription_service.process_audio_file(file)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/export")
async def export_to_word_post(
    request: ExportRequest,
    word_service: WordExportService = Depends(get_word_export_service)
):
    """
    Export transcription and analysis to Word document (POST method)
    
    Accepts JSON body with all transcription data
    """
    try:
        # Generate Word document
        doc_stream = word_service.create_document(
            transcription=request.transcription,
            summary=request.summary,
            participants=request.participants,
            decisions=request.decisions,
            action_items=request.action_items,
            filename=request.filename
        )
        
        return StreamingResponse(
            doc_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{request.filename}.docx"'}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")

