# Projeto — Triagio

## 1. Modelo de domínio

Diagrama em [`diagrams/dominio.mmd`](diagrams/dominio.mmd).

O objeto central é a **Vistoria**, que reúne o registro do estado de entrada do veículo e se relaciona às evidências, ao laudo e ao acesso do cliente.

| Classe | Origem no `REQUISITOS.md` | Observação |
|---|---|---|
| Cliente | HU-01 | Titular do cadastro usado no atendimento |
| Veiculo | HU-01, HU-05 | Identificado pela placa; concentra o histórico |
| Agendamento | HU-02 | Reserva de data/hora de recepção |
| Vistoria | HU-03 | Objeto central do fluxo |
| Avaria | HU-03 | Registro por região do veículo |
| Pertence | HU-03 | Item registrado durante a entrada |
| Foto | HU-04 | Evidência associada à vistoria |
| Laudo | HU-07 | Resultado simplificado da vistoria |
| TokenAcesso | HU-06 | Credencial para acompanhamento externo |

As associações e multiplicidades estão declaradas no diagrama.

## 2. Modelo de dados

Diagrama em [`diagrams/dados.mmd`](diagrams/dados.mmd).

### Decisões obrigatórias da passagem para dados

**Identidade**

- entidades usam chave artificial inteira como chave primária;
- `VEICULO.placa` é restrição de unicidade;
- `TOKEN_ACESSO.token` é restrição de unicidade.

**Apagamento**

- Cliente e Veículo usam desativação lógica (`ativo`) quando já possuem histórico;
- Vistoria não é apagada fisicamente no fluxo normal, pois é parte do histórico do veículo.

**Tempo**

- datas e horários são armazenados em formato ISO 8601;
- a aplicação deve tratar explicitamente o fuso utilizado ao gravar e exibir horários.

**Arquivos**

- fotos e PDF do laudo são armazenados como arquivos;
- o banco armazena caminho/nome e metadados necessários, evitando BLOBs no SQLite;
- cada foto respeita o limite de 3 MB e o máximo de 4 fotos por vistoria.

## 3. Comportamento

### 3.1 Estados da vistoria

Diagrama em [`diagrams/estados-vistoria.mmd`](diagrams/estados-vistoria.mmd).

Estados modelados a partir dos requisitos existentes:

- `EmPreenchimento`;
- `Finalizada`;
- `LaudoDisponivel`.

Nesta versão, não foi acrescentado comportamento novo apenas para completar o diagrama. Se a equipe identificar em validação um estado ou transição adicional, o `REQUISITOS.md` deve ser alterado antes ou junto da atualização do modelo.

### 3.2 Sequência do fluxo principal

Diagrama em [`diagrams/sequencia-triagem.mmd`](diagrams/sequencia-triagem.mmd).

O diagrama cobre cadastro/seleção do veículo, agendamento, vistoria, evidências, finalização, geração do laudo e consulta externa, incluindo a recusa de token inválido.

## 4. Distribuição de responsabilidades

| Parte | Sabe | Faz |
|---|---|---|
| Cliente | identificação e contato básico | associa-se aos veículos atendidos |
| Veiculo | placa, modelo, ano e situação de cadastro | concentra agendamentos e histórico de vistorias |
| Agendamento | veículo, data/hora e situação | reserva a recepção |
| Vistoria | veículo, situação, combustível e observações | controla o ciclo da triagem |
| Avaria | região e descrição | registra dano/condição observada |
| Pertence | descrição | registra item presente no veículo |
| Foto | caminho e metadados | referencia evidência fotográfica |
| Laudo | vistoria, data e arquivo | consolida o resultado da vistoria |
| TokenAcesso | token e data de criação | autoriza a consulta externa da vistoria |

## 5. Decisões de projeto

| Id | Decisão | Motivo | Consequência aceita |
|---|---|---|---|
| D-01 | Vistoria é o objeto central do domínio | O MVP gira em torno do fluxo de triagem/vistoria | As demais evidências dependem da vistoria |
| D-02 | Chave artificial como PK e placa como chave natural única | Evita usar dado de negócio como identidade interna | Há uma coluna `id` adicional |
| D-03 | Preservar histórico e usar desativação lógica para cadastros já referenciados | N5 exige histórico por placa | Registros inativos continuam no banco |
| D-04 | Consulta externa por link/token; placa fica para busca interna | N3 especifica link/QR, enquanto o README mencionava placa | É necessário gerar e validar token |
| D-05 | Fotos e laudos como arquivos, com caminho no banco | R2 identifica risco de armazenamento e o projeto usa SQLite | Backup precisa incluir banco e arquivos |
| D-06 | Datas em ISO 8601 com tratamento explícito de fuso | Evita ambiguidade de agendamentos e histórico | Conversão/formatação fica a cargo da aplicação |
| D-07 | Avarias podem ser registradas por região/lista no MVP | R1 prevê fallback caso a marcação gráfica atrase | Interface é menos visual, mas reduz risco técnico |

## 6. Conferência cruzada

A conferência entre descoberta, requisitos e modelos gerou as seguintes correções:

1. **Acesso externo:** havia divergência entre “consulta pela placa” e “link/QR Code”. A especificação passou a usar token/link externamente e placa internamente.
2. **Fotos:** o limite previsto na resposta ao risco R2 foi transformado em critério de aceitação e regra de negócio.
3. **Histórico:** o modelo de dados passou a preservar vistorias e cadastros referenciados, em vez de depender de remoção física.
4. **Rastreabilidade:** cada classe do modelo de domínio passou a apontar para as histórias que justificam sua existência.

## 7. Diagramas mantidos

A equipe mantém como fonte de projeto:

- `diagrams/dominio.mmd`;
- `diagrams/dados.mmd`;
- `diagrams/estados-vistoria.mmd`.

O diagrama de sequência é usado para esclarecer o fluxo principal e pode ser descartado futuramente se deixar de apoiar decisões, desde que isso seja registrado.

## 8. Histórico de revisão

- 2026-09-16: primeira versão da modelagem e das decisões de projeto.
