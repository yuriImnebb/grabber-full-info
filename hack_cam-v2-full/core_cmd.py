import subprocess
import requests
import os
import platform

def executar_comando_prompt(comando: str) -> str:
    """Executa comandos nativos no Prompt de Comando do Windows a partir da raiz."""
    try:
        resultado = subprocess.check_output(
            f"C:\\Windows\\System32\\cmd.exe /c {comando}", 
            shell=True, 
            stderr=subprocess.STDOUT, 
            stdin=subprocess.DEVNULL
        )
        return resultado.decode('cp850', errors='replace')
    except subprocess.CalledProcessError as e:
        return e.output.decode('cp850', errors='replace')
    except Exception as e:
        return f"Erro na execução do terminal: {e}"

def disparar_popup_powershell(texto_mensagem: str):
    """Gera um pop-up oficial do Windows via PowerShell de forma invisível."""
    cmd_pop = (
        f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -Command "
        f"\"Add-Type -AssemblyName System.Windows.Forms; "
        f"[System.Windows.Forms.MessageBox]::Show('{texto_mensagem}', 'Notificação do Sistema')\""
    )
    subprocess.Popen(f"C:\\Windows\\System32\\cmd.exe /c {cmd_pop}", shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def fechar_janela_em_primeiro_plano() -> str:
    """Identifica o processo focado em primeiro plano via Win32 API e força o encerramento."""
    script_powershell = (
        "$code = '[DllImport(\"user32.dll\")] public static extern IntPtr GetForegroundWindow();';" +
        "Add-Type -MemberDefinition $code -Name Win32 -NamespaceApi -Name 'Api';" +
        "$hwnd = [NamespaceApi.Api]::GetForegroundWindow();" +
        "if ($hwnd -ne 0) {" +
        "   $pid = Get-Process | Where-Object { $_.MainWindowHandle -eq $hwnd } | Select-Object -ExpandProperty Id -ErrorAction SilentlyContinue;" +
        "   if ($pid) {" +
        "       $processo = Get-Process -Id $pid;" +
        "       Stop-Process -Id $pid -Force;" +
        "       return $processo.Name;" +
        "   }" +
        "}" +
        "return 'Nenhum';"
    )
    cmd_completo = f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -Command \"{script_powershell}\""
    try:
        resultado = subprocess.check_output(cmd_completo, shell=True, stderr=subprocess.STDOUT)
        return resultado.decode('cp850', errors='replace').strip()
    except Exception as e:
        return f"Erro: {e}"

def obter_detalhes_rede() -> dict:
    """Consulta APIs de IP públicas ignorando validações rígidas de SSL para evitar falhas do Python 3.14"""
    dados_rede = {"ipv4": "Não detectado", "ipv6": "Não detectado", "geo": "Falha ao localizar"}
    
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
       
        resp_v4 = requests.get("http://ip-api.com", timeout=5, verify=False).json()
        if resp_v4.get("status") == "success":
            dados_rede["ipv4"] = resp_v4.get("query", "Não detectado")
            dados_rede["geo"] = f"{resp_v4.get('city')}, {resp_v4.get('regionName')} - {resp_v4.get('country')} ({resp_v4.get('isp')})"
    except:
        pass
        
    try:
        resp_v6 = requests.get("https://icanhazip.com", timeout=5, verify=False).text.strip()
        if ":" in resp_v6:
            dados_rede["ipv6"] = resp_v6
    except:
        pass
        
    return dados_rede

def obter_inventario_sistema() -> dict:
    """Coleta dados de hardware profundos usando comandos nativos do CMD (Sem bibliotecas externas)."""
    info = {
        "so": f"{platform.system()} {platform.release()} (Build {platform.version()})",
        "cpu": platform.processor(),
        "gpu": "Desconhecida",
        "placa_mae": "Desconhecida",
        "chrome": "Não instalado",
        "edge": "Não instalado"
    }
    
    try:
        
        out_gpu = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode('cp850').split('\n')
        if len(out_gpu) > 1:
            info["gpu"] = out_gpu[1].strip()
    except: pass

    try:
        
        out_board = subprocess.check_output("wmic baseboard get product,manufacturer", shell=True).decode('cp850').split('\n')
        if len(out_board) > 1:
            info["placa_mae"] = out_board[1].strip()
    except: pass

    
    caminhos_chrome = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    for caminho in caminhos_chrome:
        if os.path.exists(caminho):
            try:
                versao = subprocess.check_output(f'powershell (Get-Item "{caminho}").VersionInfo.ProductVersion', shell=True).decode().strip()
                info["chrome"] = f"Versão {versao}"
                break
            except: pass

    
    caminho_edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(caminho_edge):
        try:
            versao = subprocess.check_output(f'powershell (Get-Item "{caminho_edge}").VersionInfo.ProductVersion', shell=True).decode().strip()
            info["edge"] = f"Versão {versao}"
        except: pass

    return info

def alterar_volume_sistema(subir: bool):
    codigo_vbs = "CreateObject(\"WScript.Shell\").SendKeys(chr(&hAF))" if subir else "CreateObject(\"WScript.Shell\").SendKeys(chr(&hAE))"
    for _ in range(5):
        subprocess.Popen(f"mshta vbscript:Execute(\"{codigo_vbs}:close\")", shell=True)

def gerenciar_brilho_tela(porcentagem: int):
    cmd_brilho = f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -Command \"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(0, {porcentagem})\""
    subprocess.Popen(cmd_brilho, shell=True)

def desligar_monitor_fisico():
    cmd_desligar = "powershell -Command \"Add-Type -TypeDefinition '[DllImport(\"\"user32.dll\"\")] public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name Utils -Namespace Win32; [Win32.Utils]::SendMessage(0xFFFF, 0x0112, 0xF170, 2)\""
    subprocess.Popen(cmd_desligar, shell=True)
