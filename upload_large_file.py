
from replit.object_storage import Client
import os

# Initialize Object Storage client
storage_client = Client()

def upload_large_file(file_path, storage_name=None):
    """
    Upload a large file to Replit Object Storage
    
    Args:
        file_path: Path to the local file
        storage_name: Name to store the file as (optional, uses original name if not provided)
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return False
            
        # Use original filename if storage_name not provided
        if storage_name is None:
            storage_name = os.path.basename(file_path)
        
        # Get file size for progress indication
        file_size = os.path.getsize(file_path)
        print(f"Uploading '{file_path}' ({file_size / (1024*1024):.1f} MB) to Object Storage as '{storage_name}'...")
        
        # Upload the file
        with open(file_path, 'rb') as f:
            storage_client.upload_from_file(storage_name, f)
        
        print(f"✅ File '{storage_name}' uploaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading file: {str(e)}")
        return False

def list_uploaded_files():
    """List all files in Object Storage"""
    try:
        files = storage_client.list()
        if files:
            print("\n📁 Files in Object Storage:")
            for file in files:
                print(f"  • {file}")
        else:
            print("No files in storage yet.")
    except Exception as e:
        print(f"Error listing files: {str(e)}")

if __name__ == "__main__":
    # Example usage - replace with your actual file path
    # upload_large_file("automgen_software.exe", "eng2_automgen_software.exe")
    
    print("Large File Upload Script")
    print("========================")
    
    # List current files
    list_uploaded_files()
    
    # Interactive upload
    file_path = input("\nEnter the path to your file: ").strip()
    storage_name = input("Enter storage name (press Enter to use original name): ").strip()
    
    if not storage_name:
        storage_name = None
    
    if upload_large_file(file_path, storage_name):
        print("\n📁 Updated file list:")
        list_uploaded_files()
