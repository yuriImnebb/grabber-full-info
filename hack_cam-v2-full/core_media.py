import cv2
import os

def capturar_foto_webcam() -> bytes:
    """
    Inicializa o barramento de vídeo padrão (Index 0), aguarda a regulagem
    de brilho do sensor e extrai o frame em formato JPEG bruto.
    """

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camera.isOpened():
        return b""
        
    try:
        
        for _ in range(5):
            camera.read()
            
        ret, frame = camera.read()
        if not ret:
            return b""
        
        sucesso, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if sucesso:
            return buffer.tobytes()
    finally:
        
        camera.release()
        
    return b""
