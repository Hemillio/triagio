# Triagio — Sistema Web de Atendimento e Triagem para Oficina

Sistema web desenvolvido como projeto prático da disciplina de Engenharia de Software, com foco na digitalização da recepção, triagem e vistoria de veículos em oficinas mecânicas.

## Problema

O processo de recepção e triagem de veículos em oficinas pode depender de fichas em papel e mensagens informais. Isso favorece retrabalho, perda de histórico, conflitos de agendamento e divergências sobre avarias pré-existentes.

## Proposta

O Triagio organiza o fluxo de entrada do veículo por meio de:

- cadastro de clientes e veículos;
- agendamento da recepção;
- checklist digital de vistoria;
- registro de avarias, nível de combustível e pertences;
- anexação de fotos;
- histórico de vistorias por placa;
- acompanhamento do status por link/token;
- emissão de laudo simplificado de entrada.

## MVP (Projeto Mínimo Viável)

O MVP cobre o fluxo principal de triagem e vistoria:

1. cadastrar ou localizar cliente e veículo;
2. agendar a recepção;
3. iniciar a vistoria;
4. preencher o checklist e anexar evidências;
5. finalizar a vistoria;
6. gerar o laudo;
7. disponibilizar acompanhamento ao cliente.

## Tecnologias previstas

- Python 3
- Flask
- HTML5
- CSS3
- Bootstrap 5
- SQLite

## Equipe

| Integrante | GitHub | Eixo de responsabilidade | Módulo principal |
|---|---|---|---|
| Kauane Coimbra Sousa | KauaneCoimbra | CRM, Frota & Histórico | Cadastro de clientes, veículos e histórico por placa |
| Hemillio Oliveira Santos | Hemillio | Agendamento & Recepção | Agenda de vistorias, fila e horários |
| Danilo Feitosa do Carmo | danilofeitosac | Checklist Digital | Vistoria, avarias, fotos e pertences |
| João Mateus Monteiro Batista | jotaaa728 | Portal do Cliente | Acompanhamento e laudo |

## Artefatos de Engenharia de Software

- [`DESCOBERTA.md`](DESCOBERTA.md): problema, partes interessadas, necessidades, escopo, MVP e riscos.
- [`PROCESSO.md`](PROCESSO.md): processo de desenvolvimento adotado pela equipe.
- [`REQUISITOS.md`](REQUISITOS.md): backlog, critérios de aceitação, regras e restrições.
- [`PROJETO.md`](PROJETO.md): modelos, decisões e responsabilidades de projeto.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): convenções de contribuição.
- [`diagrams/`](diagrams/): definições textuais dos diagramas Mermaid.

## Execução

Até o estado atual do repositório usado como base para esta documentação, não há aplicação executável versionada na `main`. As instruções de execução deverão ser atualizadas assim que a implementação Flask for adicionada.
