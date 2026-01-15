"""API routes for transcription endpoints"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List

from app.business.transcription_service import TranscriptionBusinessService
from app.services.word_export_service import WordExportService
from app.models.schemas import TranscriptionResponse, ActionItem, ExportRequest

router = APIRouter(prefix="/api", tags=["transcription"])

transcription_service = TranscriptionBusinessService()
word_export_service = WordExportService()


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
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


@router.get("/export")
async def export_to_word(
    transcription: str = Query(...),
    summary: str = Query(...),
    participants: str = Query(...),  # Comma-separated string
    decisions: str = Query(...),  # Comma-separated string
    action_items: str = Query(...),  # JSON string
    filename: str = Query("meeting_transcription", description="Output filename")
):
    """
    Export transcription and analysis to Word document
    
    Query parameters:
    - transcription: Full transcription text
    - summary: Meeting summary
    - participants: Comma-separated list of participants
    - decisions: Comma-separated list of decisions
    - action_items: JSON string array of action items
    - filename: Output filename (without extension)
    """
    try:
        import json
        
        # Parse participants and decisions
        participants_list = [p.strip() for p in participants.split(",") if p.strip()]
        decisions_list = [d.strip() for d in decisions.split(",") if d.strip()]
        
        # Parse action items JSON
        try:
            action_items_data = json.loads(action_items)
            action_items_list = [
                ActionItem(**item) if isinstance(item, dict) else ActionItem(
                    task=item.get("task", str(item)),
                    assignee=item.get("assignee", "Unassigned"),
                    deadline=item.get("deadline")
                )
                for item in action_items_data
            ]
        except (json.JSONDecodeError, TypeError):
            action_items_list = []
        
        # Generate Word document
        doc_stream = word_export_service.create_document(
            transcription=transcription,
            summary=summary,
            participants=participants_list,
            decisions=decisions_list,
            action_items=action_items_list,
            filename=filename
        )
        
        return StreamingResponse(
            doc_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{filename}.docx"'}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


@router.post("/export")
async def export_to_word_post(request: ExportRequest):
    """
    Export transcription and analysis to Word document (POST method)
    
    Accepts JSON body with all transcription data
    """
    try:
        # Generate Word document
        doc_stream = word_export_service.create_document(
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

