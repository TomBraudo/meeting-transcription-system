"""Simple script to test the API with an actual MP3 file"""
import requests
import json
import sys
from pathlib import Path


def test_transcribe_api(audio_file_path: str, api_url: str = "http://localhost:8000"):
    """
    Test the transcription API with an actual audio file
    
    Args:
        audio_file_path: Path to the MP3/WAV file
        api_url: Base URL of the API
    """
    # Check if file exists
    file_path = Path(audio_file_path)
    if not file_path.exists():
        print(f"Error: File not found: {audio_file_path}")
        return None
    
    print(f"Testing transcription API with file: {audio_file_path}")
    print(f"File size: {file_path.stat().st_size / 1024:.2f} KB")
    print("-" * 80)
    
    # Prepare the file for upload
    url = f"{api_url}/api/transcribe"
    
    try:
        with open(file_path, 'rb') as audio_file:
            files = {'file': (file_path.name, audio_file, 'audio/mpeg')}
            
            print("Uploading file and processing...")
            print("This may take a while depending on file size...")
            
            response = requests.post(url, files=files, timeout=300)  # 5 minute timeout
            
            print(f"\nResponse Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                print("\n" + "=" * 80)
                print("TRANSCRIPTION RESULT")
                print("=" * 80)
                print(f"\nSummary:\n{result.get('summary', 'N/A')}")
                print(f"\nParticipants: {', '.join(result.get('participants', []))}")
                print(f"\nDecisions ({len(result.get('decisions', []))}):")
                for i, decision in enumerate(result.get('decisions', []), 1):
                    print(f"  {i}. {decision}")
                print(f"\nAction Items ({len(result.get('action_items', []))}):")
                for i, item in enumerate(result.get('action_items', []), 1):
                    print(f"  {i}. {item.get('task', 'N/A')}")
                    print(f"     Assignee: {item.get('assignee', 'Unassigned')}")
                    if item.get('deadline'):
                        print(f"     Deadline: {item.get('deadline')}")
                
                print("\n" + "-" * 80)
                print("Full Transcription (first 500 chars):")
                print("-" * 80)
                transcription = result.get('transcription', '')
                print(transcription[:500] + ("..." if len(transcription) > 500 else ""))
                print(f"\nFull transcription length: {len(transcription)} characters")
                print("=" * 80)
                
                # Save result to JSON file
                output_file = f"{file_path.stem}_result.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\nFull result saved to: {output_file}")
                
                return result
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None
                
    except requests.exceptions.Timeout:
        print("Error: Request timed out. The file might be too large.")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {api_url}")
        print("Make sure the backend server is running!")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def test_export_api(result: dict, api_url: str = "http://localhost:8000"):
    """
    Test the export API to generate a Word document
    
    Args:
        result: The transcription result from test_transcribe_api
        api_url: Base URL of the API
    """
    if not result:
        print("No result to export")
        return
    
    print("\n" + "=" * 80)
    print("Testing Word Export...")
    print("=" * 80)
    
    url = f"{api_url}/api/export"
    
    try:
        response = requests.post(url, json=result, timeout=60)
        
        if response.status_code == 200:
            output_file = "meeting_transcription.docx"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Word document saved to: {output_file}")
            print(f"File size: {len(response.content) / 1024:.2f} KB")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <path_to_audio_file>")
        print("Example: python test_api.py test_meeting.mp3")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    result = test_transcribe_api(audio_file)
    
    if result:
        # Ask if user wants to export
        export = input("\nExport to Word document? (y/n): ").lower().strip()
        if export == 'y':
            test_export_api(result)
    
    print("\nDone! Check the logs directory for detailed AI service logs.")

