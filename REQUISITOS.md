# Requisitos — Triagio

## 1. Objetivo

Este documento transforma as necessidades e o escopo registrados em `DESCOBERTA.md` em itens verificáveis de backlog.

Convenções:

- `HU-xx`: história de usuário;
- `CA-xx.y`: critério de aceitação;
- `RN-xx`: regra de negócio;
- `RQ-xx`: restrição/qualidade.

## 2. Backlog priorizado

| Id | História de usuário | Origem | Prioridade |
|---|---|---|---|
| HU-01 | Como atendente, quero cadastrar cliente e veículo para iniciar o atendimento | Escopo/MVP | Must |
| HU-02 | Como cliente/atendente, quero agendar a recepção do veículo para reduzir conflito de horários | N4 | Must |
| HU-03 | Como atendente, quero preencher a vistoria digital para registrar o estado de entrada do veículo | N1 | Must |
| HU-04 | Como atendente, quero anexar fotos à vistoria para registrar evidências do estado do veículo | N2 | Must |
| HU-05 | Como gerente, quero consultar o histórico de vistorias pela placa para recuperar registros anteriores | N5 | Should |
| HU-06 | Como cliente, quero acompanhar a vistoria por link/token para consultar o status remotamente | N3 | Must |
| HU-07 | Como atendente/cliente, quero gerar e consultar um laudo simplificado da vistoria | Escopo | Must |

## 3. Critérios de aceitação

### HU-01 — Cadastrar cliente e veículo

- **CA-01.1:** o atendente informa, no mínimo, nome do cliente, placa, modelo e ano do veículo.
- **CA-01.2:** a placa identifica unicamente um veículo no cadastro.
- **CA-01.3:** após o cadastro, o veículo fica associado ao cliente.
- **CA-01.4:** se a placa já existir, o sistema não cria um segundo veículo com a mesma placa e informa o conflito.

### HU-02 — Agendar recepção

- **CA-02.1:** é possível selecionar um veículo cadastrado e uma data/hora para a recepção.
- **CA-02.2:** o agendamento fica associado ao veículo.
- **CA-02.3:** o sistema não confirma dois agendamentos incompatíveis para o mesmo horário quando isso gerar conflito na agenda.
- **CA-02.4:** o sistema informa claramente quando o horário escolhido não estiver disponível.

### HU-03 — Preencher vistoria digital

- **CA-03.1:** a vistoria fica associada ao veículo.
- **CA-03.2:** o atendente consegue registrar avarias por região do veículo.
- **CA-03.3:** o atendente consegue registrar o nível de combustível.
- **CA-03.4:** o atendente consegue registrar pertences encontrados no veículo.
- **CA-03.5:** a vistoria permanece em estado de preenchimento até ser finalizada.
- **CA-03.6:** ao finalizar, o sistema registra data/hora da conclusão.

### HU-04 — Anexar fotos

- **CA-04.1:** cada foto fica associada a uma vistoria.
- **CA-04.2:** são aceitas no máximo 4 fotos por vistoria.
- **CA-04.3:** cada arquivo pode ter no máximo 3 MB.
- **CA-04.4:** arquivo que ultrapassar o limite é recusado com mensagem compreensível.

### HU-05 — Consultar histórico pela placa

- **CA-05.1:** o usuário interno pesquisa um veículo pela placa.
- **CA-05.2:** o sistema lista as vistorias anteriores associadas ao veículo.
- **CA-05.3:** cada item do histórico exibe ao menos data, situação e acesso ao respectivo registro/laudo quando existente.

### HU-06 — Acompanhar vistoria por link/token

- **CA-06.1:** uma vistoria disponibilizada ao cliente recebe um token de acesso único.
- **CA-06.2:** o cliente acessa o acompanhamento pelo link/token sem entrar na área administrativa.
- **CA-06.3:** token inexistente ou inválido não exibe dados da vistoria.
- **CA-06.4:** a tela apresenta o status atual e o laudo quando ele estiver disponível.

### HU-07 — Gerar laudo simplificado

- **CA-07.1:** uma vistoria finalizada pode gerar um laudo.
- **CA-07.2:** o laudo reúne os principais dados da vistoria, incluindo veículo, data, avarias e observações.
- **CA-07.3:** o laudo pode ser visualizado e preparado para PDF/impressão.
- **CA-07.4:** o laudo fica associado à vistoria que o originou.

## 4. Regras de negócio

- **RN-01:** a placa do veículo é única no cadastro.
- **RN-02:** uma vistoria pertence a exatamente um veículo.
- **RN-03:** uma vistoria aceita no máximo 4 fotos e cada foto possui limite de 3 MB.
- **RN-04:** apenas vistoria finalizada pode gerar laudo.
- **RN-05:** a consulta externa do cliente usa link/token; a placa é usada para consulta interna de histórico.

## 5. Restrições e qualidade

- **RQ-01:** o MVP não deve armazenar dados pessoais sensíveis.
- **RQ-02:** segredos e configurações locais não devem ser versionados no repositório.
- **RQ-03:** alterações integradas à `main` devem passar por revisão conforme `CONTRIBUTING.md`.

## 6. Rastreabilidade

| Necessidade/Origem | Requisitos derivados |
|---|---|
| N1 | HU-03 |
| N2 | HU-04 |
| N3 | HU-06 |
| N4 | HU-02 |
| N5 | HU-05 |
| Escopo/MVP | HU-01, HU-07 |
| R2 | CA-04.2, CA-04.3, RN-03 |

## 7. Ponto de consistência resolvido

O material original usa duas formulações para o acesso do cliente: o `README.md` menciona consulta pela placa, enquanto `DESCOBERTA.md` registra link/QR Code. Para deixar o requisito verificável, esta versão adota explicitamente:

- **placa** para localizar o histórico na área interna;
- **link/token** para acesso externo do cliente.

## 8. Histórico de revisão

- 2026-09-16: primeira versão
