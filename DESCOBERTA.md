# Descoberta do problema

## Problema
O processo de recepção e triagem de veículos em oficinas mecânicas é realizado de forma manual (fichas em papel) e mensagens informais via aplicativo. O atendente gasta tempo preenchendo formulários físicos e reescrevendo informações, enquanto o cliente sofre com a falta de transparência sobre o estado do seu veículo e recorrentemente surgem divergências sobre avarias e riscos pré-existentes no pátio.
[Fontes: E1, E2, O1]

## Partes interessadas
| Parte | Categoria | Interesse | Poder | Contato |
|---|---|---|---|---|
| Atendente / Recepcionista |  | Agilizar a entrada do veículo e registrar avarias sem rasuras | Alto | <nome> |
| Cliente da Oficina |  | Acompanhar o status da vistoria e ter laudo transparente de entrada | Baixo | <nome> |
| Gerente / Dono | Decide e apoia | Reduzir contestação de danos e organizar a fila do pátio | Alto | <nome> |
| Mecânico / Técnico |  |  | Médio | <nome> |

## Personas
### 
### 

## Fontes consultadas
- E1: 
- E2: 
- O1: 
- D1: 

## Necessidades levantadas
| Id | Necessidade | Parte | Fonte | Situação |
|---|---|---|---|---|
| N1 | Registrar entrada do veículo com marcação de avarias pré-existentes e pertences | Atendente | E1, O1 | Confirmada |
| N2 | Anexar fotos do estado real do veículo na recepção | Atendente | E1, D1 | Confirmada |
| N3 | Acompanhar o status da vistoria e entrada remotamente por link ou QR Code | Cliente | E2 | Confirmada |
| N4 | Agendar horário de vistoria para evitar filas no pátio | Cliente | E2 | Confirmada |
| N5 | Consultar histórico completo de manutenções e vistorias anteriores pela placa | Gerente | E1 | Confirmada |

## Escopo
### Entra nesta versão
- Cadastro de clientes e veículos (placa, modelo, ano).
- Agendamento prévio de horários para triagem.
- Checklist digital de vistoria (avarias por região do veículo, nível de combustível, pertences e upload de fotos).
- Prontuário de histórico do veículo por placa.
- Portal do cliente para consulta pública de status via token/link.
- Emissão de laudo simplificado de vistoria de entrada em PDF/impressão.

### Fora de escopo nesta versão
- Módulo financeiro e emissão de notas fiscais (foco exclusivo na triagem e atendimento).
- Venda de peças e controle complexo de estoque (exige módulo de ERP dedicado).
- Pagamento de serviços online (evita integração com gateways de pagamento terceiros).

## Produto mínimo viável
A fatia escolhida para o MVP foca no **Fluxo Completo de Triagem e Vistoria**:
1. Cadastro do cliente/veículo e agendamento da recepção.
2. Preenchimento do checklist digital no pátio pelo atendente com registro de avarias.
3. Disponibilização da tela de acompanhamento para o cliente consultar o laudo pela placa.

*Critérios aplicados:* Validade direta para a dor da oficina, Viabilidade técnica para execução em Flask/SQLite por 4 pessoas e Exequibilidade cronológica em 4 sprints até o encontro 9.

## Riscos iniciais
| Id | Risco | Prob. | Impacto | Resposta | Ação e responsável |
|---|---|---|---|---|---|
| R1 | Dificuldade técnica na implementação da marcação gráfica de avarias no navegador | Média | Alto | Mitigar | Adotar seletores em lista/checkboxes por região do veículo (ex: Para-choque dianteiro, Porta D) caso o canvas interativo atrase. Responsável: <nome> |
| R2 | Sobrecarga no armazenamento por conta do upload de fotos do pátio | Média | Médio | Mitigar | Implementar validação e compressão de imagens no upload (limite de 3MB e máx 4 fotos por vistoria). Responsável: <nome> |
| R3 | Expansão indevida do escopo para funcionalidades de ERP/Oficina completa | Alta | Alto | Mitigar | Restringir o backlog estritamente às tarefas do Eixo de Atendimento e Triagem. Responsável: <nome> |

## Histórico de revisão
- 2026-09-02: versão inicial
