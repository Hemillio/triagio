# Arquitetura — Triagio

## 1. Objetivo e contexto

Este documento descreve as decisões técnicas propostas para transformar os modelos do `PROJETO.md` e os critérios do `REQUISITOS.md` em uma aplicação web executável. O Triagio cobre recepção e triagem de veículos em oficina, não um ERP completo.

## 2. Arquitetura escolhida

A aplicação é um **monólito Flask**, com páginas HTML montadas no servidor usando Jinja e Bootstrap 5. O código é separado por módulos de responsabilidade, mas utiliza uma única aplicação, um banco SQLite e uma fábrica Flask.

- Navegador: visualização dos formulários e envio das ações HTTP.
- Flask/Blueprints: rotas e composição de respostas.
- Domínio: entidades e regras de cliente, agendamento, vistoria e portal.
- Flask-SQLAlchemy: persistência das entidades e transações.
- Flask-Migrate: migrações versionadas da estrutura do banco.
- SQLite: persistência de desenvolvimento e demonstração local.
- Sistema de arquivos local: fotografias e arquivos de laudo; banco guarda caminhos e metadados.

Fonte: `diagrams/arquitetura.mmd`.

## 3. Responsabilidade de cada módulo

| Módulo | Responsável | Dados/regras principais |
|---|---|---|
| `clientes` | Kauane | Cliente, Veiculo, placa única, histórico interno |
| `agendamentos` | Hemillio | Agendamento, recepção e conflito de horário |
| `vistorias` | Danilo | Vistoria, Avaria, Pertence, Foto, finalização |
| `portal` | João Mateus | Acompanhamento por token e laudo |

Os módulos compartilham `app.extensions.db` e não criam configurações independentes. Modelos de outros integrantes são **importados**, nunca copiados.

## 4. Onde o sistema executa

Na demonstração, o navegador se conecta ao Flask local. A aplicação e o SQLite ficam na máquina de desenvolvimento. Os anexos são mantidos sob `instance/`, excluídos do Git. A definição de hospedagem de produção ficará para uma decisão futura, acompanhada de autenticação, segurança, backups e política de acesso.

Fonte: `diagrams/implantacao.mmd`.

## 5. Decisões e alternativas

| ID | Decisão | Justificativa | Alternativa não escolhida / custo aceito |
|---|---|---|---|
| A-01 | Monólito Flask com HTML/Jinja | Menor complexidade para o MVP e stack já escolhida no README | Frontend separado + API: mais infraestrutura e contratos; a aplicação não é um SPA |
| A-02 | Blueprints por responsabilidade | Trabalho paralelo dos quatro integrantes | Um arquivo único de rotas causaria conflitos e acoplamento |
| A-03 | Uma instância de SQLAlchemy e migrações no Git | Consistência do esquema e histórico de alterações | Criar tabelas manualmente de formas diferentes em cada notebook |
| A-04 | SQLite local para desenvolvimento | Tecnologia aprovada no README; uso simples em demonstração | Outro banco exigiria instalação e administração adicional |
| A-05 | Fotografias em arquivos; caminho no banco | Evita BLOBs e segue o PROJETO.md | Backup deve reunir o banco e os uploads |
| A-06 | Agendamento com capacidade de um início por horário | Interpretação inicial de conflito da HU-02, sujeita a validação da equipe | Ainda não modela duração de serviço nem capacidade de múltiplas baias |
| A-07 | Hora local na entrada; UTC ISO 8601 no banco | Evita ambiguidade na leitura de agenda e vistoria | Exige conversão para exibição |
| A-08 | Interface interna sem login somente em ambiente local de demonstração | Permite construir o primeiro incremento sem adicionar uma HU que não consta do backlog | **Não pode ser exposta publicamente com dados reais**; autenticação/CSRF antes de uso real |
| A-09 | Fábrica `create_app(test_config=None)` | Permite banco em memória nos testes e registro de módulos conforme integração | A equipe precisa preservar os nomes do contrato |

## 6. Verificações e fronteiras

- A interface pode ajudar o usuário, mas **o servidor valida** placa/vínculo, horário, estado e arquivos.
- O banco garante integridade de chaves estrangeiras e unicidade do horário de agendamento desta versão.
- O cadastro de Cliente e Veiculo pertence à Kauane; a agenda usa `veiculo_id` existente.
- A vistoria pertence ao Danilo; a agenda apenas disponibiliza o agendamento selecionável.
- Token e laudo pertencem ao João; não entram no módulo de agendamento.
- Fotografias, `.env`, SQLite local, `.venv` e segredos **não são versionados**.

## 7. Qualidade, riscos e restrições

| Requisito/risco | Resposta arquitetural desta versão |
|---|---|
| RN-01: placa única | Restrição no modelo de Veiculo da Kauane |
| CA-02.3: conflitos | Unicidade do instante de recepção, validada pelo servidor e pelo banco, após acordo da equipe |
| RN-02: vistoria ligada a veículo | Chave estrangeira não nula no módulo de Danilo |
| RN-03: até 4 fotos de até 3 MB | Validação no servidor, dentro do módulo de Danilo |
| RN-04: laudo somente de vistoria finalizada | Regra no módulo do João |
| RN-05: token externo, placa somente interna | Rotas distintas e sem exposição da busca por placa no portal |
| RQ-01: não armazenar dados pessoais sensíveis | Dados mínimos de demonstração, sem informações reais |
| RQ-02: segredos fora do Git | `.gitignore`, `.env.example` sem credenciais reais |
| RQ-03: integração revisada | Branches, PRs e revisão cruzada conforme CONTRIBUTING.md |

## 8. Pontos em aberto

- Confirmar em reunião a capacidade da recepção e a regra de conflito de horários.
- Definir autenticação e autorização da área interna antes de qualquer implantação pública.
- Revisar segurança de formulários (CSRF) e proteção dos arquivos antes de uso com dados reais.
- Escolher servidor, banco e estratégia de backup para produção numa etapa futura.

## 9. Histórico

- 2026-10-28: proposta inicial de arquitetura para implementação, sujeita à aprovação/revisão do grupo.