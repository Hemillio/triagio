# Triagio

Sistema web acadêmico para apoiar a recepção e a triagem de veículos em oficinas. O projeto reúne cadastro de clientes e veículos, agendamento, vistoria, histórico do veículo e acompanhamento do cliente por token.

> **Demonstração local:** o sistema ainda não tem autenticação para a área interna nem proteção CSRF nos formulários. Use somente em ambiente local e com dados fictícios. Não o publique nem use dados reais sem definir e implementar as proteções necessárias.

## Funcionalidades

- Cadastro de clientes e veículos, com consulta de veículos pela placa.
- Agendamento de recepção e visualização da agenda.
- Abertura e preenchimento de vistorias com nível de combustível, observações, avarias e pertences.
- Envio de até quatro fotos por vistoria. Cada arquivo pode ter até 3 MiB e deve ser JPEG, PNG ou WEBP.
- Finalização da vistoria, que impede novas alterações no checklist e o envio de fotos.
- Histórico de vistorias associado ao veículo.
- Geração de um link com token aleatório para acompanhar o estado da vistoria.
- Geração e consulta de laudo em PDF depois da finalização.

## Fluxo básico

1. Cadastre um cliente e seu veículo, ou localize um veículo já cadastrado.
2. Crie um agendamento, se necessário.
3. Abra uma vistoria para o veículo, preencha o checklist e anexe as evidências.
4. Finalize a vistoria.
5. Na área de acesso do portal, gere o link para o cliente. Depois da finalização, gere o laudo PDF.
6. O cliente acompanha a situação e acessa o laudo pelo link com token.

As funcionalidades são acessadas pela página inicial e pela navegação do sistema. O módulo de vistorias não possui uma página de listagem em `/vistorias`: as telas dependem do veículo ou da vistoria, por exemplo `/vistorias/nova/<id_do_veiculo>` e `/vistorias/<id_da_vistoria>`.

## Tecnologias

- Python 3.14 (versão usada na integração contínua)
- Flask e Flask-SQLAlchemy
- Flask-Migrate e Alembic para migrações do banco
- SQLite por padrão
- Pillow para validar imagens
- ReportLab para gerar PDFs
- Bootstrap 5.3.3 para a interface
- pytest para testes

## Requisitos

- Python 3.14 instalado.
- Git para clonar o repositório.
- Acesso à internet para instalar os pacotes Python e carregar o Bootstrap do CDN.

## Instalação e execução

Clone o repositório e acesse a pasta:

```bash
git clone https://github.com/Hemillio/triagio.git
cd triagio
```

Crie e ative um ambiente virtual. No Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No macOS ou Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Opcionalmente, crie um arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

No macOS ou Linux, use `cp .env.example .env`. Para demonstração local, o banco SQLite fica em `instance/triagio.db`. O `.env.example` também mostra como definir `TRIAGIO_SECRET_KEY`, `TRIAGIO_DATABASE_URL` e `TRIAGIO_TIMEZONE`. Não use a chave de exemplo em um ambiente compartilhado ou publicado.

Crie ou atualize as tabelas e inicie o servidor de desenvolvimento:

```bash
flask --app run.py db upgrade
flask --app run.py run --debug
```

Abra <http://127.0.0.1:5000> no navegador. Para interromper o servidor, pressione `Ctrl+C` no terminal.

## Testes

Com o ambiente virtual ativo e as dependências instaladas:

```bash
python -m pytest -q
```

O GitHub Actions executa esse mesmo comando em pushes para `main` e em pull requests direcionados à `main`.

## Arquivos locais

O banco, as fotos enviadas e os PDFs gerados ficam sob `instance/`, que não é versionada:

- Banco SQLite: `instance/triagio.db`.
- Fotos de vistorias: `instance/uploads/vistorias/`.
- Laudos PDF: `instance/laudos/`.

Faça cópias de segurança desses arquivos se precisar preservar dados locais. Os registros do banco referenciam as fotos e os PDFs armazenados no disco.

## Limitações conhecidas

- A área interna não exige login e os formulários ainda não têm proteção CSRF.
- Os links de acompanhamento usam um token secreto na URL; o sistema não oferece expiração ou revogação do token.
- Fotos e laudos são armazenados no disco local. Hospedagem, armazenamento externo e política de backup não estão configurados.
- Use apenas dados fictícios nesta versão acadêmica local.

## Documentação do projeto

- [`REQUISITOS.md`](REQUISITOS.md): histórias, prioridades e critérios de aceitação.
- [`ARQUITETURA.md`](ARQUITETURA.md) e [`PROJETO.md`](PROJETO.md): módulos, integração e decisões de projeto.
- [`contrato/`](contrato/): contratos dos módulos.
- [`ITERACOES.md`](ITERACOES.md) e [`PROCESSO.md`](PROCESSO.md): planejamento e processo de desenvolvimento.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): fluxo de branches, pull requests e revisão.
- [`diagrams/`](diagrams/): diagramas do projeto.

## Equipe

| Integrante | GitHub | Responsabilidade principal |
|---|---|---|
| Kauane Coimbra Sousa | [KauaneCoimbra](https://github.com/KauaneCoimbra) | Clientes, veículos e histórico |
| Hemillio Oliveira Santos | [Hemillio](https://github.com/Hemillio) | Agendamento e recepção |
| Danilo Feitosa do Carmo | [danilofeitosac](https://github.com/danilofeitosac) | Vistorias, checklist, avarias, fotos e pertences |
| João Mateus Monteiro Batista | [jotaaa728](https://github.com/jotaaa728) | Portal do cliente e laudos |
