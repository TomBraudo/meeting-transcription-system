import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * API service for communicating with the backend
 */
class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Transcribe audio file and get meeting analysis
   * @param {File} audioFile - Audio file (mp3/wav)
   * @param {string|null} language - Language code ('en', 'he', or null for auto-detect)
   * @param {Function} onUploadProgress - Progress callback
   * @returns {Promise} Transcription response
   */
  async transcribeAudio(audioFile, language = null, onUploadProgress) {
    const formData = new FormData();
    formData.append('file', audioFile);

    // Build URL with optional language parameter
    const url = language 
      ? `/api/transcribe?language=${language}`
      : '/api/transcribe';

    try {
      const response = await this.client.post(
        url,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress,
        }
      );
      return response.data;
    } catch (error) {
      console.error('Transcription error:', error);
      throw this._handleError(error);
    }
  }

  /**
   * Export transcription results to Word document
   * @param {Object} data - Transcription data
   * @returns {Promise<Blob>} Word document blob
   */
  async exportToWord(data) {
    try {
      const response = await this.client.post('/api/export', data, {
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      console.error('Export error:', error);
      throw this._handleError(error);
    }
  }

  /**
   * Health check endpoint
   * @returns {Promise} Health status
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw this._handleError(error);
    }
  }

  /**
   * Handle API errors
   * @private
   */
  _handleError(error) {
    if (error.response) {
      // Server responded with error
      return new Error(
        error.response.data?.detail || 
        error.response.data?.message || 
        'Server error occurred'
      );
    } else if (error.request) {
      // Request made but no response
      return new Error('No response from server. Please check if the backend is running.');
    } else {
      // Something else happened
      return new Error(error.message || 'An unexpected error occurred');
    }
  }
}

const apiService = new ApiService();
export default apiService;
