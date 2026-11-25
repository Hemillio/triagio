# Guia para executar o pacote local do Triagio

Este guia vale para o Artifact ZIP produzido depois que os testes e a validação do pacote passam em um push para main. A execução no computador do Hemillio é manual e serve para uma demonstração acadêmica com dados fictícios.

## 1. Baixar e extrair o pacote

No GitHub, abra Actions, selecione a execução de **Testes automatizados - Triagio** referente ao commit integrado e baixe o Artifact triagio-<hash>. O job de pacote só aparece em pushes para main e só publica o ZIP depois de validar a extração, as migrações e a rota inicial. Extraia o ZIP em uma pasta de demonstração.

## 2. Preparar o ambiente

O projeto usa Python 3.14. Abra um terminal dentro da pasta extraída e crie um ambiente virtual.

### Windows PowerShell

    py -3.14 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Copy-Item .env.example .env

### macOS ou Linux

    python3.14 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    cp .env.example .env

## 3. Preparar o banco e iniciar

Com o ambiente virtual ativo, execute:

    flask --app run.py db upgrade
    flask --app run.py run --host 127.0.0.1 --no-debugger --no-reload

Abra http://127.0.0.1:5000. Mantenha o servidor limitado a 127.0.0.1 e com debug desligado. Para encerrar, pressione Ctrl+C no terminal.

## 4. Limites da demonstração

- Use somente dados fictícios.
- Mantenha o servidor acessível apenas na própria máquina (127.0.0.1) e com debug desligado.
- Não use o servidor de desenvolvimento para publicação na internet ou uso real.
- O banco e os arquivos criados durante a demonstração ficam em instance/ da pasta extraída; mantenha essa pasta fora do GitHub.

O Artifact tem retenção curta (7 dias). A apresentação demonstra entrega e validação automatizadas; a inicialização no computador continua manual.
