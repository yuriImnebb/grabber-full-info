import time
import subprocess

def pressionar_tecla_especial(tecla: str) -> bool:
    try:
     
        codigo_vbs = f"CreateObject(\"WScript.Shell\").SendKeys(\"{{{tecla.upper()}}}\")"
        subprocess.Popen(f"mshta vbscript:Execute(\"{codigo_vbs}:close\")", shell=True)
        return True
    except:
        return False

def simular_digitacao(texto: str) -> bool:
    try:
       
        codigo_vbs = f"CreateObject(\"WScript.Shell\").SendKeys(\"{texto}\")"
        subprocess.Popen(f"mshta vbscript:Execute(\"{codigo_vbs}:close\")", shell=True)
        return True
    except:
        return False

def fechar_jogo_force() -> bool:
    """Aperta F8, aguarda abrir o console, digita /quit e confirma"""
    try:
        pressionar_tecla_especial("F8")
        time.sleep(0.2)
        simular_digitacao("/quit")
        pressionar_tecla_especial("ENTER")
        return True
    except:
        return False
