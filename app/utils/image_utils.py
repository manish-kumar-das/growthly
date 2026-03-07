"""
Utility functions for image processing
"""

from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt

def get_circular_pixmap(image_path, size):
    """
    Creates a circular pixmap from an image path.
    Performs 'center-crop' to fit the circle.
    """
    src = QPixmap(image_path)
    if src.isNull():
        return None
    
    # Scale to fill (cover logic)
    transformed = src.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    
    # Center crop if AspectRatioByExpanding made it larger than size in one dimension
    x = (transformed.width() - size) // 2
    y = (transformed.height() - size) // 2
    cropped = transformed.copy(x, y, size, size)
    
    out = QPixmap(size, size)
    out.fill(Qt.transparent)
    
    painter = QPainter(out)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, cropped)
    painter.end()
    
    return out
