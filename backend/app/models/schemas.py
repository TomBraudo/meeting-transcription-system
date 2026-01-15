"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel
from typing import List, Optional


class ActionItem(BaseModel):
    """Action item schema"""
    task: str
    assignee: str
    deadline: Optional[str] = None


class TranscriptionResponse(BaseModel):
    """Response schema for transcription endpoint"""
    transcription: str
    summary: str
    participants: List[str]
    decisions: List[str]
    action_items: List[ActionItem]


class ExportRequest(BaseModel):
    """Request schema for export endpoint"""
    transcription: str
    summary: str
    participants: List[str]
    decisions: List[str]
    action_items: List[ActionItem]
    filename: Optional[str] = "meeting_transcription"

