🎨 Passo 1: Colocar a imagem na pasta do projeto

Certifique-se de que a sua imagem convertida em formato de ícone do Windows (com a extensão obrigatoriamente .ico) esteja salva dentro da pasta hack_cam-cell, exatamente com o nome icone.ico (junto do arquivo main.py) [1.1].

🛠️ Passo 2: Executar o Comando de Build com Ícone

Abra o terminal do seu VS Code na pasta do projeto e execute este comando completo. Ele une o parâmetro de arquivo único, modo invisível e a injeção da imagem [1.1]:
powershell
& c:\python314\python.exe -m PyInstaller --onefile --noconsole --icon=icone.ico --name="GestorCentralV3" main.py
Use o código com cuidado.

📂 Passo 3: Pegar o seu arquivo final personalizado

O PyInstaller vai processar os módulos e compactar o design visual do ícone no arquivo [1.1]. Assim que o processo terminar no terminal:

1. Abra a pasta hack_cam-cell no seu Windows Explorer.
2. Acesse a pasta dist [1.1].
3. O seu executável GestorCentralV3.exe estará lá dentro, operando de forma invisível e já exibindo o desenho do seu ícone customizado na interface do Windows [1.1]!
