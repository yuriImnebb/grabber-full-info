import os
import sys
import asyncio
import threading
import io
import discord
import psutil

import config
import core_cmd
import core_perif
import core_media

print("🤖 [START] Carregando configuracoes do sistema...")

intents = discord.Intents.default()
intents.message_content = True

class PainelAdministrativoCentral(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_print_ativo = False
        self.tarefa_print = None

    async def on_ready(self):
        print(f"✅ [DISCORD] Bot logado com sucesso como: {self.user}")
        canal = self.get_channel(config.ID_CANAL_CENTRAL)
        if canal:
            embed = discord.Embed(
                title="⚡ Estrutura Modular v3.5 Estável",
                description="Painel administrativo unificado ativo com monitoramento e logs no terminal.",
                color=discord.Color.green()
            )
            embed.add_field(name="Operador do Sistema", value=f"`{os.getlogin()}`", inline=True)
            embed.set_footer(text="Digite !ajuda para listar todos os comandos integrados.")
            await canal.send(embed=embed)
            print("📩 [DISCORD] Mensagem de boas-vindas enviada para o canal.")
        else:
            print(f"❌ [ERRO] Nao foi possivel encontrar o canal com o ID: {config.ID_CANAL_CENTRAL}")

    async def tirar_print_nativo(self, canal, msg_conteudo=""):
        print("📸 [AÇÃO] Executando captura de tela nativa via PowerShell...")
        try:
            caminho_temp = os.path.join(os.environ["TEMP"], "print_temp.png")
            cmd_ps = (
                "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -Command "
                "\"Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.SendKeys]::SendWait('{PRTSC}'); "
                "Start-Sleep -Milliseconds 250; "
                "if ([System.Windows.Forms.Clipboard]::ContainsImage()) { "
                "  \$img = [System.Windows.Forms.Clipboard]::GetImage(); "
                "  \$img.Save('" + caminho_temp + "', [System.Drawing.Imaging.ImageFormat]::Png); "
                "}\""
            )
            os.system(cmd_ps)
            
            if os.path.exists(caminho_temp):
                await canal.send(content=msg_conteudo, file=discord.File(caminho_temp))
                print("📤 [AÇÃO] Print enviado com sucesso para o Discord.")
                try: os.remove(caminho_temp)
                except: pass
            else:
                await canal.send("⚠️ Nao foi possivel capturar a imagem do monitor.")
                print("⚠️ [AVISO] PowerShell nao gerou o arquivo de imagem.")
        except Exception as e:
            await canal.send(f"❌ Falha tecnica no print: {e}")
            print(f"❌ [ERRO PRINT] {e}")

    async def ciclo_captura_cinco_segundos(self, canal):
        while self.loop_print_ativo:
            await self.tirar_print_nativo(canal, "📸 **Monitoramento Continuo (5s):**")
            await asyncio.sleep(5)

    async def on_message(self, message):
        if message.author == self.user or message.channel.id != config.ID_CANAL_CENTRAL:
            return
        if message.author.id != config.MEU_ID_DO_DISCORD:
            return

        comando_bruto = message.content.strip()
        comando_limpo = comando_bruto.lower()
        partes = comando_bruto.split(" ")

        cmd_principal = partes[0].lower() if len(partes) > 0 else ""

        print(f"💬 [CHAT] Mensagem recebida: '{comando_bruto}' | Comando Detectado: '{cmd_principal}'")

        #  MENU DE COMANDOS
        if comando_limpo == "!ajuda":
            ajuda_txt = (
                " **Painel Administrativo v3.5 - Lista de Comandos:**\n\n"
                " **Auditoria e Inventario Optico:**\n"
                " `!status` - Uso atual de CPU e memoria RAM.\n"
                " `!rede` - Exibe IPv4, IPv6 e localizacao do provedor.\n"
                " `!sistema` - Varredura completa de hardware e navegadores.\n"
                " `!camera` - Liga a webcam e tira uma foto em alta definicao.\n"
                " `!print` / `!print5s` - Capturas de tela estaticas e ciclicas nativas.\n"
                " `!pararprint5s` - Para as capturas automaticas do monitor.\n\n"
                " **Hardware e Perifericos:**\n"
                " `!volume+` / `!volume-` - Controle de audio do Windows.\n"
                " `!brilho <0-100>` - Ajuste de iluminacao do monitor.\n"
                " `!apagartela` - Desliga as telas fisicas (Modo suspensao).\n"
                " `!msg <texto>` - Caixa de dialogo na tela do Windows.\n"
                " `!fechar` - Encerra o aplicativo em primeiro plano."
            )
            await message.channel.send(ajuda_txt)
            return

        if comando_limpo == "!camera":
            print("📸 [AÇÃO] Solicitando imagem da webcam...")
            await message.channel.send("📸 **Acionando barramento de midia e regulando lentes...**")
            bytes_foto = core_media.capturar_foto_webcam()
            if bytes_foto:
                arr_bytes = io.BytesIO(bytes_foto)
                await message.channel.send(content="📸 **Foto capturada pela Webcam:**", file=discord.File(fp=arr_bytes, filename="webcam.jpg"))
                print("📤 [AÇÃO] Foto da webcam enviada para o Discord.")
            else:
                await message.channel.send("⚠️ Nenhuma camera ativa detectada ou barramento ocupado.")
                print("⚠️ [AVISO] Falha ao ler frames da webcam.")
            return

        if comando_limpo == "!sistema":
            print("🔎 [AÇÃO] Buscando informacoes de hardware...")
            await message.channel.send("🔎 Executando varredura rapida nos barramentos... Aguarde...")
            hw = core_cmd.obter_inventario_sistema()
            embed = discord.Embed(title="🖥️ Inventario Tecnico do Sistema", color=discord.Color.blue())
            embed.add_field(name="Sistema Operacional", value=f"`{hw['so']}`", inline=False)
            embed.add_field(name="Processador (CPU)", value=f"`{hw['cpu']}`", inline=False)
            embed.add_field(name="Placa de Video (GPU)", value=f"`{hw['gpu']}`", inline=False)
            embed.add_field(name="Placa-Mae (Motherboard)", value=f"`{hw['placa_mae']}`", inline=False)
            embed.add_field(name="Google Chrome", value=f"`{hw['chrome']}`", inline=True)
            embed.add_field(name="Microsoft Edge", value=f"`{hw['edge']}`", inline=True)
            await message.channel.send(embed=embed)
            return

        if comando_limpo == "!rede":
            print(" [AÇÃO] Coletando dados geograficos e IPs da maquina...")
            await message.channel.send("🔍 Consultando barramentos de rede via subsistema Windows... Aguarde...")
            try:
                cmd_v4 = "powershell -Command \"(Invoke-RestMethod -Uri 'http://ip-api.com') | ConvertTo-Json\""
                saida_v4 = core_cmd.executar_comando_prompt(cmd_v4)
                
                cmd_v6 = "powershell -Command \"Invoke-RestMethod -Uri 'https://icanhazip.com'\""
                saida_v6 = core_cmd.executar_comando_prompt(cmd_v6).strip()
                if "Erro" in saida_v6 or len(saida_v6) > 45: saida_v6 = "Nao disponivel ou sem suporte local"

                import json
                dados = json.loads(saida_v4)
                
                embed = discord.Embed(title=" Informacoes de Conectividade do Sistema", color=discord.Color.purple())
                embed.add_field(name="Endereco IPv4 Publico", value=f"`{dados.get('query', 'Nao detectado')}`", inline=False)
                embed.add_field(name="Endereco IPv6", value=f"`{saida_v6}`", inline=False)
                embed.add_field(name="Geolocalizacao / Provedor", value=f"`{dados.get('city')}, {dados.get('regionName')} - {dados.get('country')} ({dados.get('isp')})`", inline=False)
                await message.channel.send(embed=embed)
            except Exception as e:
                await message.channel.send(f"❌ Erro ao decodificar dados de rede: {e}")
                print(f"❌ [ERRO REDE] {e}")
            return

        if cmd_principal == "!msg" and len(partes) >= 2:
            mensagem_popup = " ".join(partes[1:])
            print(f"💬 [AÇÃO] Abrindo pop-up com a mensagem: '{mensagem_popup}'")
            core_cmd.disparar_popup_powershell(mensagem_popup)
            await message.channel.send(f" Pop-up enviado com sucesso: `{mensagem_popup}`")
            return

        if comando_limpo == "!fechar":
            print("🛑 [AÇÃO] Solicitando fechamento do app em primeiro plano...")
            await message.channel.send("⏳ Derrubando o processo em primeiro plano...")
            proc = core_cmd.fechar_janela_em_primeiro_plano()
            if proc == "Nenhum": await message.channel.send("⚠️ Nenhum software focado na frente.")
            else: await message.channel.send(f"✅ Processo **`{proc}.exe`** encerra do com sucesso!")
            return

        if comando_limpo == "!status":
            await message.channel.send(f"📊 **Metricas:**\n• CPU: {psutil.cpu_percent()}%\n• RAM: {psutil.virtual_memory().percent}%")
            return

        if comando_limpo == "!volume+":
            core_cmd.alterar_volume_sistema(subir=True)
            await message.channel.send("🔊 Volume aumentado.")
            return

        if comando_limpo == "!volume-":
            core_cmd.alterar_volume_sistema(subir=False)
            await message.channel.send("🔉 Volume diminuido.")
            return

        if cmd_principal == "!brilho" and len(partes) >= 2:
            try:
                nivel = int(partes[1])
                if 0 <= nivel <= 100:
                    core_cmd.gerenciar_brilho_tela(nivel)
                    await message.channel.send(f"🔆 Brilho ajustado para `{nivel}%`.")
                else: await message.channel.send("⚠️ Brilho deve ser entre 0 e 100.")
            except: await message.channel.send("❌ Uso correto: `!brilho 70`")
            return

        if comando_limpo == "!apagartela":
            print("🌙 [AÇÃO] Mandando monitores dormirem...")
            core_cmd.desligar_monitor_fisico()
            await message.channel.send("🌙 Sinal enviado aos monitores.")
            return

        if comando_limpo == "!print5s":
            if self.loop_print_ativo: return
            print("🔄 [AÇÃO] Ativando loop de capturas (5s)...")
            self.loop_print_ativo = True
            self.tarefa_print = asyncio.create_task(self.ciclo_captura_cinco_segundos(message.channel))
            await message.channel.send("🔄 Monitoramento de 5 segundos ligado.")
            return

        if comando_limpo == "!pararprint5s":
            if not self.loop_print_ativo: return
            print("🛑 [AÇÃO] Parando loop de capturas.")
            self.loop_print_ativo = False
            if self.tarefa_print: self.tarefa_print.cancel()
            await message.channel.send("🛑 Monitoramento de 5 segundos desligado.")
            return

        if comando_limpo == "!print":
            await self.tirar_print_nativo(message.channel)
            return

        if comando_limpo == "!quit":
            if core_perif.fechar_jogo_force(): await message.channel.send("✅ Encerramento enviado!")
            return

        if cmd_principal == "!tecla" and len(partes) >= 2:
            core_perif.pressionar_tecla_especial(partes[1])
            await message.channel.send(f"⌨️ Tecla `{partes[1]}` simulada.")
            return

        if cmd_principal == "!digitar" and len(partes) >= 2:
            core_perif.simular_digitacao(" ".join(partes[1:]))
            await message.channel.send("✅ Texto inserido.")
            return

      
        print(f"💻 [CMD] Executando comando direto no prompt: {comando_bruto}")
        resultado = core_cmd.executar_comando_prompt(comando_bruto)
        if resultado.strip():
            await message.channel.send(f"```cmd\n{resultado[:1900]}\n```")

if __name__ == "__main__":
    print("🤖 [START] Conectando au gateway do Discord...")
    bot = PainelAdministrativoCentral(intents=intents)
    bot.run(config.DISCORD_TOKEN)
