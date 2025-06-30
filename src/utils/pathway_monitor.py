import os
import time
import logging
import threading
from typing import Callable, Optional
from pathlib import Path
import watchdog.observers
from watchdog.events import FileSystemEventHandler

class PathwayFileHandler(FileSystemEventHandler):
    """File system event handler for Pathway monitoring."""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.logger = logging.getLogger(__name__)
        
        # Supported file extensions
        self.supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            file_path = event.src_path
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension in self.supported_extensions:
                self.logger.info(f"New file detected: {file_path}")
                
                # Wait a moment to ensure file is fully written
                time.sleep(1)
                
                # Call the callback function
                try:
                    self.callback(file_path)
                except Exception as e:
                    self.logger.error(f"Error processing file {file_path}: {str(e)}")
    
    def on_moved(self, event):
        """Handle file move events (treats as new file)."""
        if not event.is_directory:
            self.on_created(event)

class PathwayMonitor:
    """Monitors a folder for new legal documents using file system events."""
    
    def __init__(self, folder_path: str, callback: Callable[[str], None]):
        self.folder_path = folder_path
        self.callback = callback
        self.logger = logging.getLogger(__name__)
        
        # Create folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Setup file system watcher
        self.event_handler = PathwayFileHandler(callback)
        self.observer = watchdog.observers.Observer()
        self.observer.schedule(
            self.event_handler, 
            folder_path, 
            recursive=False
        )
        
        self.is_monitoring = False
    
    def start_monitoring(self):
        """Start monitoring the folder for changes."""
        try:
            self.observer.start()
            self.is_monitoring = True
            self.logger.info(f"Started monitoring folder: {self.folder_path}")
            
            # Keep the monitoring thread alive
            while self.is_monitoring:
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Error starting folder monitor: {str(e)}")
        finally:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring the folder."""
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        
        self.is_monitoring = False
        self.logger.info("Stopped folder monitoring")
    
    def scan_existing_files(self):
        """Scan for existing files in the folder and process them."""
        try:
            supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
            
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                
                if os.path.isfile(file_path):
                    file_extension = Path(file_path).suffix.lower()
                    
                    if file_extension in supported_extensions:
                        self.logger.info(f"Processing existing file: {file_path}")
                        try:
                            self.callback(file_path)
                        except Exception as e:
                            self.logger.error(f"Error processing existing file {file_path}: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error scanning existing files: {str(e)}")

class SimplePathwayMonitor:
    """
    Simplified Pathway-like monitoring implementation.
    This provides basic folder monitoring functionality similar to Pathway.
    """
    
    def __init__(self, folder_path: str, callback: Callable[[str], None]):
        self.folder_path = folder_path
        self.callback = callback
        self.logger = logging.getLogger(__name__)
        
        # Create folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Track processed files to avoid reprocessing
        self.processed_files = set()
        self.is_monitoring = False
        
        # Supported file extensions
        self.supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    
    def start_polling_monitor(self, interval: int = 5):
        """Start polling-based monitoring (fallback if watchdog fails)."""
        self.is_monitoring = True
        self.logger.info(f"Started polling monitor for: {self.folder_path}")
        
        while self.is_monitoring:
            try:
                self.check_for_new_files()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in polling monitor: {str(e)}")
                time.sleep(interval)
    
    def check_for_new_files(self):
        """Check for new files in the monitored folder."""
        try:
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                
                if os.path.isfile(file_path) and file_path not in self.processed_files:
                    file_extension = Path(file_path).suffix.lower()
                    
                    if file_extension in self.supported_extensions:
                        self.logger.info(f"New file detected: {file_path}")
                        
                        # Mark as processed first to avoid duplicates
                        self.processed_files.add(file_path)
                        
                        # Process the file
                        try:
                            self.callback(file_path)
                        except Exception as e:
                            self.logger.error(f"Error processing file {file_path}: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error checking for new files: {str(e)}")
    
    def stop_monitoring(self):
        """Stop the monitoring process."""
        self.is_monitoring = False
        self.logger.info("Stopped file monitoring")

def create_pathway_monitor(folder_path: str, callback: Callable[[str], None]) -> PathwayMonitor:
    """
    Factory function to create a Pathway monitor.
    Falls back to simple polling if watchdog is not available.
    """
    try:
        # Try to create watchdog-based monitor
        return PathwayMonitor(folder_path, callback)
    except ImportError:
        # Fallback to simple polling monitor
        logging.warning("Watchdog not available, using simple polling monitor")
        return SimplePathwayMonitor(folder_path, callback)
