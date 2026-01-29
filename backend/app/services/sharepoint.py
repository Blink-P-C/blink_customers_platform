import httpx
from typing import Optional, BinaryIO
from msal import ConfidentialClientApplication
from app.config import settings


class SharePointService:
    def __init__(self):
        self.tenant_id = settings.MICROSOFT_TENANT_ID
        self.client_id = settings.MICROSOFT_CLIENT_ID
        self.client_secret = settings.MICROSOFT_CLIENT_SECRET
        self.site_id = settings.SHAREPOINT_SITE_ID
        self.drive_id = settings.SHAREPOINT_DRIVE_ID
        self.graph_url = "https://graph.microsoft.com/v1.0"
        self._access_token = None

    def _get_access_token(self) -> str:
        """Get access token using client credentials flow"""
        if self._access_token:
            return self._access_token
        
        app = ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret,
        )
        
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        
        if "access_token" in result:
            self._access_token = result["access_token"]
            return self._access_token
        else:
            raise Exception(f"Failed to get access token: {result.get('error_description')}")

    async def upload_file(
        self, 
        file_content: bytes, 
        file_name: str, 
        folder_path: str = "/"
    ) -> dict:
        """Upload a file to SharePoint"""
        token = self._get_access_token()
        
        # Clean folder path
        if not folder_path.startswith("/"):
            folder_path = f"/{folder_path}"
        if folder_path.endswith("/"):
            folder_path = folder_path[:-1]
        
        # Upload URL for files < 4MB (use resumable upload for larger files)
        url = f"{self.graph_url}/drives/{self.drive_id}/root:{folder_path}/{file_name}:/content"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers, content=file_content)
            response.raise_for_status()
            return response.json()

    async def get_file_info(self, file_id: str) -> dict:
        """Get file metadata from SharePoint"""
        token = self._get_access_token()
        
        url = f"{self.graph_url}/drives/{self.drive_id}/items/{file_id}"
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_download_url(self, file_id: str) -> str:
        """Get a temporary download URL for a file"""
        token = self._get_access_token()
        
        url = f"{self.graph_url}/drives/{self.drive_id}/items/{file_id}"
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            file_info = response.json()
            return file_info.get("@microsoft.graph.downloadUrl")

    async def delete_file(self, file_id: str) -> None:
        """Delete a file from SharePoint"""
        token = self._get_access_token()
        
        url = f"{self.graph_url}/drives/{self.drive_id}/items/{file_id}"
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            response.raise_for_status()

    async def create_folder(self, folder_name: str, parent_path: str = "/") -> dict:
        """Create a folder in SharePoint"""
        token = self._get_access_token()
        
        url = f"{self.graph_url}/drives/{self.drive_id}/root:{parent_path}:/children"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()


# Singleton instance
sharepoint_service = SharePointService()
