"""Tests for model layer (Pydantic schemas)"""
import pytest
from pydantic import ValidationError

from app.models.schemas import ActionItem, TranscriptionResponse, ExportRequest


class TestActionItem:
    """Tests for ActionItem schema"""
    
    def test_valid_action_item(self):
        """Test creating a valid action item"""
        item = ActionItem(
            task="Complete task",
            assignee="John Doe",
            deadline="2024-01-15"
        )
        assert item.task == "Complete task"
        assert item.assignee == "John Doe"
        assert item.deadline == "2024-01-15"
    
    def test_action_item_without_deadline(self):
        """Test action item without deadline"""
        item = ActionItem(
            task="Complete task",
            assignee="John Doe"
        )
        assert item.deadline is None
    
    def test_action_item_missing_required_fields(self):
        """Test that missing required fields raise ValidationError"""
        with pytest.raises(ValidationError):
            ActionItem(task="Task only")
        
        with pytest.raises(ValidationError):
            ActionItem(assignee="Assignee only")


class TestTranscriptionResponse:
    """Tests for TranscriptionResponse schema"""
    
    def test_valid_transcription_response(self):
        """Test creating a valid transcription response"""
        response = TranscriptionResponse(
            transcription="Test transcription",
            summary="Test summary",
            participants=["Alice", "Bob"],
            decisions=["Decision 1"],
            action_items=[
                ActionItem(task="Task 1", assignee="Alice")
            ]
        )
        assert response.transcription == "Test transcription"
        assert len(response.participants) == 2
        assert len(response.action_items) == 1
    
    def test_transcription_response_empty_lists(self):
        """Test transcription response with empty lists"""
        response = TranscriptionResponse(
            transcription="Test",
            summary="Summary",
            participants=[],
            decisions=[],
            action_items=[]
        )
        assert response.participants == []
        assert response.decisions == []
        assert response.action_items == []
    
    def test_transcription_response_missing_fields(self):
        """Test that missing required fields raise ValidationError"""
        with pytest.raises(ValidationError):
            TranscriptionResponse(
                transcription="Test"
                # Missing other required fields
            )


class TestExportRequest:
    """Tests for ExportRequest schema"""
    
    def test_valid_export_request(self):
        """Test creating a valid export request"""
        request = ExportRequest(
            transcription="Test transcription",
            summary="Test summary",
            participants=["Alice"],
            decisions=["Decision 1"],
            action_items=[ActionItem(task="Task", assignee="Alice")],
            filename="test_meeting"
        )
        assert request.filename == "test_meeting"
    
    def test_export_request_default_filename(self):
        """Test export request with default filename"""
        request = ExportRequest(
            transcription="Test",
            summary="Summary",
            participants=[],
            decisions=[],
            action_items=[]
        )
        assert request.filename == "meeting_transcription"

