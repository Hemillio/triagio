# Guia para executar o pacote local do Triagio

Este guia vale para o pacote gerado pelo workflow de entrega contínua após a CI passar na main. A execução é local, para demonstração acadêmica com dados fictícios.

## 1. Baixar e extrair o pacote

No GitHub, abra Actions, selecione a execução de Entrega contínua - pacote local e baixe o artefato triagio-<hash>. Extraia o ZIP em uma pasta de demonstração.

## 2. Preparar o ambiente

O projeto usa Python 3.14. Abra um terminal dentro da pasta extraída e crie um ambiente virtual.

### Windows PowerShell

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS ou Linux

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## 3. Preparar o banco e iniciar

Com o ambiente virtual ativo, execute:

```bash
flask --app run.py db upgrade
flask --app run.py run --debug
```

Abra http://127.0.0.1:5000. Para encerrar, pressione Ctrl+C no terminal.

## 4. Limites da demonstração

- Use somente dados fictícios.
- Mantenha o servidor acessível apenas na própria máquina (127.0.0.1).
- Não use o servidor de desenvolvimento para publicação na internet ou uso real.
- O banco e os arquivos criados durante a demonstração ficam em instance/ da pasta extraída; mantenha essa pasta fora do GitHub.
