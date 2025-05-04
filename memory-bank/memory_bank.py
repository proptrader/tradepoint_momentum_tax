import json
import os
from typing import Any, Dict, Optional
from datetime import datetime

class MemoryBank:
    def __init__(self, storage_path: str = "memory-bank/data"):
        """
        Initialize the memory bank.
        
        Args:
            storage_path (str): Path where data will be stored
        """
        self.storage_path = storage_path
        self._ensure_storage_directory()
        
    def _ensure_storage_directory(self) -> None:
        """Ensure the storage directory exists."""
        os.makedirs(self.storage_path, exist_ok=True)
        
    def store(self, key: str, data: Any) -> None:
        """
        Store data in the memory bank.
        
        Args:
            key (str): Unique identifier for the data
            data (Any): Data to store (must be JSON serializable)
        """
        file_path = os.path.join(self.storage_path, f"{key}.json")
        with open(file_path, 'w') as f:
            json.dump({
                'data': data,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
            
    def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve data from the memory bank.
        
        Args:
            key (str): Unique identifier for the data
            
        Returns:
            Optional[Any]: The stored data if found, None otherwise
        """
        file_path = os.path.join(self.storage_path, f"{key}.json")
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r') as f:
            stored_data = json.load(f)
            return stored_data['data']
            
    def delete(self, key: str) -> bool:
        """
        Delete data from the memory bank.
        
        Args:
            key (str): Unique identifier for the data
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        file_path = os.path.join(self.storage_path, f"{key}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
        
    def list_keys(self) -> list[str]:
        """
        List all keys in the memory bank.
        
        Returns:
            list[str]: List of all stored keys
        """
        files = os.listdir(self.storage_path)
        return [f.replace('.json', '') for f in files if f.endswith('.json')]
        
    def clear(self) -> None:
        """Clear all data from the memory bank."""
        for key in self.list_keys():
            self.delete(key) 