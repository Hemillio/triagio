# Descoberta do problema

## Problema

O processo de recepção e triagem de veículos em oficinas mecânicas é realizado de forma manual (fichas em papel) e mensagens informais via aplicativo. O atendente gasta tempo preenchendo formulários físicos e reescrevendo informações, enquanto o cliente sofre com a falta de transparência sobre o estado do seu veículo e podem surgir divergências sobre avarias e riscos pré-existentes no pátio.

## Partes interessadas

| Parte | Papel no sistema | Interesse | Poder |
|---|---|---|---|
| Atendente / Recepcionista | Usuário operacional | Agilizar a entrada do veículo e registrar a vistoria sem rasuras | Alto |
| Cliente da oficina | Usuário/parte afetada | Acompanhar o status e ter um registro transparente da entrada | Baixo |
| Gerente / Dono | Decide e apoia | Reduzir contestação de danos e organizar o fluxo do pátio | Alto |
| Mecânico / Técnico | Usuário indireto | Receber o veículo com informações claras sobre sua condição de entrada | Médio |

## Evidências de elicitação

- `E1`: entrevista real — **pendente**;
- `E2`: entrevista real — **pendente**;
- `O1`: observação real — **pendente**;
- `D1`: documento ou evidência complementar — **pendente**.

## Personas


## Necessidades levantadas

| Id | Necessidade | Parte interessada | Origem registrada no projeto |
|---|---|---|---|
| N1 | Registrar a entrada do veículo com avarias pré-existentes e pertences | Atendente | E1, O1 |
| N2 | Anexar fotos do estado real do veículo na recepção | Atendente | E1, D1 |
| N3 | Acompanhar o status da vistoria e entrada remotamente por link ou QR Code | Cliente | E2 |
| N4 | Agendar horário de vistoria para evitar filas no pátio | Cliente | E2 |
| N5 | Consultar histórico de manutenções e vistorias anteriores pela placa | Gerente | E1 |

## Escopo

### Entra nesta versão

- Cadastro de clientes e veículos (placa, modelo, ano).
- Agendamento prévio de horários para triagem.
- Checklist digital de vistoria: avarias por região, nível de combustível, pertences e fotos.
- Histórico do veículo por placa.
- Portal do cliente para consulta de status por link/token.
- Emissão de laudo simplificado de vistoria de entrada em PDF/impressão.

### Fora de escopo

- Módulo financeiro e emissão de notas fiscais.
- Venda de peças e controle complexo de estoque.
- Pagamento de serviços online.

## Produto mínimo viável

O MVP foca no fluxo completo de triagem e vistoria:

1. cadastro do cliente e do veículo;
2. agendamento da recepção;
3. preenchimento do checklist digital;
4. registro de avarias, pertences e fotos;
5. conclusão da vistoria;
6. disponibilização de acompanhamento e laudo.

## Riscos iniciais

| Id | Risco | Probabilidade | Impacto | Resposta |
|---|---|---|---|---|
| R1 | Dificuldade técnica na marcação gráfica de avarias no navegador | Média | Alto | Usar seletores por região do veículo como alternativa |
| R2 | Sobrecarga no armazenamento por upload de fotos | Média | Médio | Limitar a 4 fotos por vistoria e 3 MB por foto |
| R3 | Expansão do escopo para funcionalidades de ERP completo | Alta | Alto | Restringir o backlog ao eixo de atendimento e triagem |

## Histórico de revisão

- 2026-09-02: versão inicial.
- 2026-09-16: revisão de consistência e explicitação das evidências ainda não documentadas.
