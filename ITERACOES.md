
# Iterações — Triagio

Este arquivo registra o planejamento e os resultados efetivos das iterações da equipe. O processo geral está em `PROCESSO.md` e as histórias em `REQUISITOS.md`.

## Iteração de implementação inicial — planejamento proposto

**Situação:** proposta para discussão e aprovação dos quatro integrantes; não registrar como decisão tomada antes da reunião.

**Meta proposta:** permitir que um atendente localize um veículo cadastrado, registre sua entrada, preencha uma vistoria básica e a finalize; preparar a integração do acompanhamento por token pelo módulo do João.

**Duração prevista:** duas semanas, conforme `PROCESSO.md`.

**Início e encerramento:** preencher com as datas efetivamente combinadas na reunião.

**Capacidade:** preencher horas disponíveis de Kauane, Hemillio, Danilo e João. A capacidade não foi medida nem estimada pelos integrantes neste documento.

### Backlog e dependências

| Item | Prioridade do REQUISITOS.md | Responsável | Depende de | Pontos |
|---|---|---|---|---|
| HU-01 Cadastrar cliente e veículo | Must | Kauane | Estrutura Flask/SQLite | A estimar em equipe |
| HU-02 Agendar recepção | Must | Hemillio | HU-01 | A estimar em equipe |
| HU-03 Checklist e finalização | Must | Danilo | HU-01 e estrutura do banco | A estimar em equipe |
| HU-04 Fotos da vistoria | Must | Danilo | HU-03 | A estimar em equipe |
| HU-06 Acompanhamento por token | Must | João | HU-03 | A estimar em equipe |
| HU-07 Laudo simplificado | Must | João | HU-03 finalizada | A estimar em equipe |
| HU-05 Histórico por placa | Should | Kauane | HU-01 e HU-03 | A estimar em equipe |

**Método de estimativa proposto:** cada integrante estima as histórias usando escala 1, 2, 3, 5, 8, 13; divergências são discutidas, sem calcular uma falsa média de consenso. A equipe registra a rodada e os pontos aprovados.

**Recorte da iteração:** escolher o conjunto de histórias cuja soma caiba na capacidade; não declarar que todas as linhas serão entregues nesta iteração sem a estimativa.

### Plano técnico e integração

1. Hemillio entrega a fábrica Flask, `db`, migrações e base HTML.
2. Kauane entrega o modelo `Veiculo`; Hemillio entrega a tabela `agendamentos` se a vistoria for ligada à agenda.
3. Danilo integra modelos de vistoria, checklist, finalização e fotos em commits pequenos.
4. João integra a consulta por token e o laudo após a Vistoria estar estável.
5. Cada pessoa testa os critérios de aceitação do que escreveu; outra pessoa revisa o Pull Request.

### Quadro de acompanhamento

| Item | Situação | Responsável | Evidência |
|---|---|---|---|
| HU-01 | Não iniciada | Kauane | Issue e PR a registrar |
| HU-02 | Não iniciada | Hemillio | Issue e PR a registrar |
| HU-03 | Não iniciada | Danilo | Issue e PR a registrar |
| HU-04 | Não iniciada | Danilo | Issue e PR a registrar |
| HU-06 | Não iniciada | João | Issue e PR a registrar |
| HU-07 | Não iniciada | João | Issue e PR a registrar |
| HU-05 | Não iniciada | Kauane | Issue e PR a registrar |

Colunas sugeridas para issues: backlog, em andamento, em revisão, bloqueada, concluída. O limite de trabalho simultâneo deve ser acordado pela equipe.

### Definição de pronto

Conforme `PROCESSO.md` e `CONTRIBUTING.md`: critérios de aceitação cumpridos, PR revisado por pessoa diferente do autor, merge na `main`, issue fechada e documentação afetada atualizada. No código, acrescentar verificação executável e demonstração do fluxo sempre que possível.

### Preparação da demonstração

- [ ] Base com dados **fictícios** (não usar fotos nem placas reais identificáveis).
- [ ] Cadastro de veículo e associação com cliente.
- [ ] Agendamento, quando integrado.
- [ ] Criar vistoria, preencher avaria, combustível, pertences e salvar.
- [ ] Anexar uma imagem pequena de demonstração e conferir recusa de quinta foto e de arquivo acima de 3 MB.
- [ ] Finalizar e conferir a data/hora e a proibição de alteração.
- [ ] Abrir portal com token, se a HU-06 estiver no recorte entregue.
- [ ] Abrir laudo, se a HU-07 estiver no recorte entregue.
- [ ] Conferir que o projeto inicia a partir de `main` limpa e dependências documentadas.

### Fechamento e retrospectiva — preencher depois da execução

- **Histórias planejadas e concluídas:** pendente.
- **Pontos concluídos (velocidade observada):** pendente; não inventar números.
- **Demonstração e comentários de usuário/professor:** pendente.
- **O que funcionou:** pendente.
- **O que atrapalhou:** pendente.
- **Mudança para a iteração seguinte:** pendente.
