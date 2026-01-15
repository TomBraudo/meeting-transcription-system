"""Word document export service"""
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from typing import List, Optional
from datetime import datetime
import io

from app.models.schemas import ActionItem


class WordExportService:
    """Service for generating Word documents"""
    
    def create_document(
        self,
        transcription: str,
        summary: str,
        participants: List[str],
        decisions: List[str],
        action_items: List[ActionItem],
        filename: Optional[str] = "meeting_transcription"
    ) -> io.BytesIO:
        """
        Create a Word document with meeting transcription and analysis
        
        Args:
            transcription: Full transcription text
            summary: Meeting summary
            participants: List of participants
            decisions: List of decisions
            action_items: List of action items
            filename: Base filename (without extension)
        
        Returns:
            BytesIO object containing the Word document
        """
        doc = Document()
        
        # Title
        title = doc.add_heading('Meeting Transcription & Summary', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Metadata
        meta_para = doc.add_paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        meta_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        meta_para.runs[0].font.size = Pt(10)
        doc.add_paragraph()  # Spacing
        
        # Summary Section
        doc.add_heading('Summary', level=1)
        doc.add_paragraph(summary)
        doc.add_paragraph()  # Spacing
        
        # Participants Section
        doc.add_heading('Participants', level=1)
        if participants:
            for participant in participants:
                doc.add_paragraph(participant, style='List Bullet')
        else:
            doc.add_paragraph('No participants identified.')
        doc.add_paragraph()  # Spacing
        
        # Decisions Section
        doc.add_heading('Decisions', level=1)
        if decisions:
            for decision in decisions:
                doc.add_paragraph(decision, style='List Bullet')
        else:
            doc.add_paragraph('No decisions recorded.')
        doc.add_paragraph()  # Spacing
        
        # Action Items Section
        doc.add_heading('Action Items', level=1)
        if action_items:
            for item in action_items:
                task_para = doc.add_paragraph(f'Task: {item.task}', style='List Bullet')
                doc.add_paragraph(f'  Assignee: {item.assignee}', style='List Bullet 2')
                if item.deadline:
                    doc.add_paragraph(f'  Deadline: {item.deadline}', style='List Bullet 2')
        else:
            doc.add_paragraph('No action items identified.')
        doc.add_paragraph()  # Spacing
        
        # Full Transcription Section
        doc.add_heading('Full Transcription', level=1)
        doc.add_paragraph(transcription)
        
        # Save to BytesIO
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        return file_stream

