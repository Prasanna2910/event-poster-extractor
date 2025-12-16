"""
API Client for communicating with Flask backend
"""

import requests
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """Client for Flask backend API"""
    
    def __init__(self, base_url="https://event-poster-extractor.onrender.com/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_connection(self):
        """Test if backend is running"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def extract_data(self, image_base64):
        """
        Extract data from poster image
        
        Args:
            image_base64 (str): Base64 encoded image
            
        Returns:
            dict: Response with extracted data
        """
        try:
            response = self.session.post(
                f"{self.base_url}/extract",
                json={"image": f"data:image/png;base64,{image_base64}"},
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'success': False,
                    'error': response.json().get('error', 'Unknown error')
                }
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout - backend is taking too long'
            }
        except Exception as e:
            logger.error(f"Error in extract_data: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_email(self, template_type, event_data):
        """
        Generate email from template
        
        Args:
            template_type (str): Template ID
            event_data (dict): Event data for template
            
        Returns:
            dict: Response with generated email
        """
        try:
            response = self.session.post(
                f"{self.base_url}/generate-email",
                json={
                    "template_type": template_type,
                    "event_data": event_data
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'success': False,
                    'error': response.json().get('error', 'Unknown error')
                }
        except Exception as e:
            logger.error(f"Error in generate_email: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_email(self, to_email, subject, body):
        """
        Send email
        
        Args:
            to_email (str): Recipient email
            subject (str): Email subject
            body (str): Email body
            
        Returns:
            dict: Response with send status
        """
        try:
            response = self.session.post(
                f"{self.base_url}/send-email",
                json={
                    "to": to_email,
                    "subject": subject,
                    "body": body
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'success': False,
                    'error': response.json().get('error', 'Unknown error')
                }
        except Exception as e:
            logger.error(f"Error in send_email: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_templates(self):
        """
        Get all available email templates
        
        Returns:
            dict: List of templates
        """
        try:
            response = self.session.get(f"{self.base_url}/templates", timeout=5)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'templates': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to fetch templates'
                }
        except Exception as e:
            logger.error(f"Error in get_templates: {e}")
            return {
                'success': False,
                'error': str(e)
            }