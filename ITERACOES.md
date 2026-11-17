
# Iterações — Triagio

> **Registro de planejamento, execução e acompanhamento**  
> **Disciplina:** Engenharia de Software — UFT  
> **Equipe:** Hemillio, Kauane, Danilo e João  
> **Atualização documental:** 17/11/2026
>
> **Como ler este documento:** a Seção 1 preserva o **planejamento inicial proposto**; as seções seguintes registram **entregas e evidências posteriores**. O planejamento inicial não deve ser interpretado como a situação atual. Datas de sprint, pontos de esforço e resultados de avaliações não registrados não foram inventados.

Este arquivo acompanha o planejamento e os resultados das iterações da equipe. O processo geral está descrito em [PROCESSO.md](PROCESSO.md), as histórias em [REQUISITOS.md](REQUISITOS.md), as decisões técnicas em [PROJETO.md](PROJETO.md) e [ARQUITETURA.md](ARQUITETURA.md).

---

## 1. Planejamento inicial — proposta registrada

> **Registro histórico.** Esta seção mantém as intenções do início do projeto, tal como apresentadas no `ITERACOES.md` inicial. Os estados “Não iniciada” e as pendências de estimativa pertencem àquele momento; a execução posterior está documentada na Seção 2.

### 1.1 Objetivo e limites propostos

- **Situação na elaboração:** proposta para discussão e aprovação dos quatro integrantes; o documento original não registrou a data de aprovação da equipe.
- **Meta proposta:** permitir que um atendente localize um veículo cadastrado, registre sua entrada, preencha uma vistoria básica e a finalize; preparar a integração do acompanhamento por token no módulo do João.
- **Duração prevista:** duas semanas, conforme referência do planejamento inicial ao [PROCESSO.md](PROCESSO.md).
- **Início e encerramento efetivos da iteração inicial:** não registrados no planejamento original.
- **Capacidade da equipe:** o documento previa levantar as horas disponíveis de Kauane, Hemillio, Danilo e João; não apresentou uma capacidade medida.

### 1.2 Backlog inicial, dependências e responsáveis

| Item | Prioridade inicial | Responsável | Dependência prevista | Pontos no planejamento inicial |
|---|---|---|---|---|
| HU-01 — Cadastrar cliente e veículo | Must | Kauane | Estrutura Flask/SQLite | A estimar em equipe |
| HU-02 — Agendar recepção | Must | Hemillio | HU-01 | A estimar em equipe |
| HU-03 — Checklist e finalização | Must | Danilo | HU-01 e estrutura do banco | A estimar em equipe |
| HU-04 — Fotos da vistoria | Must | Danilo | HU-03 | A estimar em equipe |
| HU-06 — Acompanhamento por token | Must | João | HU-03 | A estimar em equipe |
| HU-07 — Laudo simplificado | Must | João | HU-03 finalizada | A estimar em equipe |
| HU-05 — Histórico por placa/veículo | Should | Kauane | HU-01 e HU-03 | A estimar em equipe |

**Método de estimativa proposto originalmente:** cada integrante estimaria as histórias em escala 1, 2, 3, 5, 8 e 13. Divergências seriam discutidas até chegar a uma estimativa consensual. **Não há estimativas finais comprovadas nesse registro**; por isso, não são atribuídos pontos retroativamente.

**Recorte de iteração proposto:** selecionar histórias cuja soma de esforço coubesse na capacidade disponível, sem declarar que todas seriam entregues em uma única iteração antes da estimativa.

### 1.3 Plano técnico e integração propostos

1. Hemillio entregaria a fábrica Flask, a configuração de banco de dados, as migrações e a base HTML.
2. Kauane entregaria o modelo de veículo; Hemillio entregaria a tabela de agendamentos, se a vistoria estivesse ligada à agenda.
3. Danilo integraria modelos de vistoria, checklist, finalização e fotografias em commits menores.
4. João integraria a consulta por token e a geração de laudo após estabilização da vistoria.
5. Cada integrante testaria seus critérios de aceitação; outra pessoa revisaria o Pull Request.

### 1.4 Quadro de acompanhamento — situação inicial (histórico)

| Item | Situação na elaboração do plano | Responsável | Evidência prevista |
|---|---|---|---|
| HU-01 | Não iniciada | Kauane | Issue e PR a registrar |
| HU-02 | Não iniciada | Hemillio | Issue e PR a registrar |
| HU-03 | Não iniciada | Danilo | Issue e PR a registrar |
| HU-04 | Não iniciada | Danilo | Issue e PR a registrar |
| HU-06 | Não iniciada | João | Issue e PR a registrar |
| HU-07 | Não iniciada | João | Issue e PR a registrar |
| HU-05 | Não iniciada | Kauane | Issue e PR a registrar |

As colunas previstas para acompanhamento eram backlog, em andamento, em revisão, bloqueada e concluída. O grupo posteriormente organizou um quadro Kanban no GitHub Projects (Seção 3).

### 1.5 Definição de pronto proposta

Segundo as regras de [PROCESSO.md](PROCESSO.md) e [CONTRIBUTING.md](CONTRIBUTING.md), uma entrega seria considerada pronta após atender aos critérios de aceitação, passar por revisão de outra pessoa, ter o PR integrado à `main` e manter a documentação pertinente atualizada. Sempre que possível, deveria incluir teste executável e demonstração do fluxo.

### 1.6 Roteiro inicial para demonstração (histórico)

Os itens abaixo eram **verificações planejadas**, não registros de que cada demonstração ocorreu nessa época:

- [ ] Utilizar base com dados fictícios, sem fotos ou placas reais identificáveis.
- [ ] Demonstrar cadastro de veículo e associação ao cliente.
- [ ] Demonstrar agendamento, quando integrado.
- [ ] Criar vistoria, registrar avaria, combustível e pertences, e salvar.
- [ ] Anexar foto de demonstração e verificar restrições de upload previstas nos critérios.
- [ ] Finalizar vistoria e conferir data/hora e bloqueio de alterações.
- [ ] Abrir o portal por token, caso HU-06 faça parte do recorte.
- [ ] Abrir o laudo, caso HU-07 faça parte do recorte.
- [ ] Verificar a execução do projeto a partir de uma `main` atualizada e com dependências instaladas.

### 1.7 Fechamento e retrospectiva previstos inicialmente

O arquivo inicial deixava por preencher: histórias planejadas e concluídas, pontos concluídos (velocidade observada), demonstração e comentários, pontos positivos, dificuldades e mudanças para a próxima iteração. As informações comprovadas posteriormente são registradas a seguir; o que depende de avaliação/reunião real continua identificado como pendente.

---

## 2. Execução — situação das histórias de usuário

> **Atualização com base no histórico de desenvolvimento apresentado pela equipe até 17/11/2026.** Os links abaixo permitem consultar as entregas. A conclusão técnica da implementação não equivale, por si só, a uma validação formal do professor ou a uma demonstração completa para usuários reais.

| História | Responsável principal | Situação técnica informada | Evidências no GitHub |
|---|---|---|---|
| HU-01 — Cadastro de clientes e veículos | Kauane | Implementada | [PR #6](https://github.com/Hemillio/triagio/pull/6), [PR #7](https://github.com/Hemillio/triagio/pull/7), correções no [PR #9](https://github.com/Hemillio/triagio/pull/9) |
| HU-02 — Agendamento de recepção | Hemillio | Implementada | [PR #8](https://github.com/Hemillio/triagio/pull/8) |
| HU-03 — Checklist e finalização da vistoria | Danilo | Implementada | [PR #10](https://github.com/Hemillio/triagio/pull/10) |
| HU-04 — Fotografias da vistoria | Danilo | Implementada | [PR #14](https://github.com/Hemillio/triagio/pull/14) |
| HU-05 — Histórico de vistorias | Kauane | Implementada | [PR #13](https://github.com/Hemillio/triagio/pull/13) |
| HU-06 — Acompanhamento por token | João | Implementada | [PR #11](https://github.com/Hemillio/triagio/pull/11) |
| HU-07 — Laudo em PDF | João | Implementada | [PR #12](https://github.com/Hemillio/triagio/pull/12) |

**Leitura correta:** “Implementada” significa que há evidências de código e integração relatadas pela equipe; não implica que o grupo tenha medido ou aprovado pontos de história posteriormente.

### 2.1 Entregas complementares (além das histórias acima)

| Tipo de trabalho | Evidências |
|---|---|
| Planejamento e contratos iniciais | [PR #1](https://github.com/Hemillio/triagio/pull/1), [PR #2](https://github.com/Hemillio/triagio/pull/2), [PR #3](https://github.com/Hemillio/triagio/pull/3), [PR #5](https://github.com/Hemillio/triagio/pull/5) |
| Estrutura Flask e banco compartilhado | [PR #4](https://github.com/Hemillio/triagio/pull/4) |
| Correções de cadastro | [PR #9](https://github.com/Hemillio/triagio/pull/9) |
| Padronização de interface, formulários, navegação e datas | [PR #15](https://github.com/Hemillio/triagio/pull/15) |
| Integração contínua (CI) com GitHub Actions | [PR #16](https://github.com/Hemillio/triagio/pull/16) |

Os PRs devem ser consultados para conferir autores, revisões, datas de merge e arquivos alterados. O registro retrospectivo acima **não atribui automaticamente uma data de conclusão à história inteira** apenas com base na data de abertura de um PR.

### 2.2 Testes e integração contínua

- **Testes locais:** a equipe registrou execução de `python -m pytest -q` com **33 testes aprovados**.
- **Integração contínua:** foi criado `.github/workflows/testes.yml` para executar o `pytest` em Pull Requests voltados à `main` e em `push` na `main`.
- **Evidência observada:** na aba **Actions**, o grupo conferiu execuções com status de sucesso tanto no PR #16 quanto após seu merge.
- **Limite da evidência:** a quantidade exata de testes executados no ambiente do GitHub deve ser confirmada no log do job; o indicador verde sozinho confirma sucesso do workflow, não a contagem detalhada.
- **CD (entrega/implantação contínua):** ainda não estava configurado no último acompanhamento; foi identificado como trabalho futuro/pendente de execução.

---

## 3. Quadro Kanban do grupo

**Ferramenta:** GitHub Projects.  
**Quadro:** [Triagio — Quadro de Tarefas](https://github.com/users/Hemillio/projects/1).

O grupo usa um fluxo visual para registrar tarefas, responsáveis e entregas:

| Coluna | Significado |
|---|---|
| Backlog | Ideias e atividades futuras ainda não priorizadas para execução imediata |
| Ready | Atividades definidas e prontas para iniciar |
| In progress | Atividades que estão sendo executadas |
| In review | Atividades aguardando conferência, revisão ou aprovação |
| Done | Atividades concluídas |

Em registro apresentado pela equipe, o quadro já reunia **16 cartões de Pull Requests em `Done`**. Isso mostra entregas concluídas no repositório, mas **não significa que todos os 16 PRs pertenceram à mesma iteração**. O status e a quantidade de cartões podem mudar após esta atualização.

### 3.1 Responsabilidades por módulo

| Integrante | Área principal no desenvolvimento |
|---|---|
| Hemillio | Arquitetura, estrutura Flask, agendamentos, interface e configuração de CI |
| Kauane | Clientes, veículos e histórico |
| Danilo | Checklist, finalização de vistorias e fotografias |
| João | Portal de acompanhamento por token e laudos |

A atribuição de cada cartão deve representar as contribuições reais; trabalhos compartilhados podem ter mais de um responsável.

### 3.2 Trabalho ainda planejado ou em andamento

**Não registrar os itens abaixo como concluídos antes de existirem evidências.** A posição exata no quadro deve acompanhar a execução real:

- **CD — entrega/implantação contínua:** pendente de implementação e validação; a equipe manifestou intenção de colocá-la em `Ready`.
- **Refinamento visual/CSS:** possível trabalho contínuo posterior ao PR #15; confirmar se há tarefa realmente em `In progress` e qual é seu escopo novo.
- **Segurança e privacidade:** revisão técnica recomendada antes de implantação pública.
- **Implantação e operação:** definir ambiente, variáveis de configuração, acesso, armazenamento e procedimentos de manutenção.
- **Apresentação/review final:** preparar demonstração e evidências solicitadas na disciplina.

---

## 4. Registro do Review Parcial (encontro 9)

**Situação informada pela equipe:** a turma/grupo avançou além desse conteúdo, mas **não realizou uma sessão formal de Review Parcial** para o Triagio.

Consequentemente:

- Não são atribuídos comentários, notas, defeitos ou solicitações a um professor ou a outra equipe.
- Não há uma ata de observações de avaliadores a apresentar como se a sessão tivesse ocorrido.
- Eventuais correções podem ser documentadas como revisões internas ou alterações identificadas pelo próprio grupo, vinculadas aos PRs correspondentes.
- Caso o professor solicite um registro substitutivo, a equipe deverá confirmar com ele o formato aceito.

Este registro não afirma que uma atividade avaliativa obrigatória foi formalmente cumprida.

---

## 5. Histórico de entregas e separação em iterações

### 5.1 O que o histórico comprova

Os Pull Requests e seus commits permitem verificar **o que mudou**, **quem contribuiu**, **quando a alteração foi registrada** e **quando houve integração à `main`**. O quadro Projects permite acompanhar o estado de cada cartão.

### 5.2 O que ainda precisa ser reconstruído

No arquivo inicial não foram registradas datas efetivas, estimativas finais ou recortes de cada sprint. Por isso, **não é possível afirmar que os PRs #1 a #16 equivalem a uma, duas ou mais iterações de duração fixa** apenas olhando a coluna `Done`.

A equipe precisa identificar, com base em decisões reais e evidências, os limites dos ciclos que executou. Se não houve sprints formalmente delimitadas, registrar que o trabalho ocorreu em fluxo contínuo com entregas incrementais, em vez de inventar ciclos passados.

### 5.3 Registro das iterações efetivamente identificadas

| Iteração/ciclo | Período real | Objetivo acordado | Trabalho comprometido no início | Entregas no período | Evidência |
|---|---|---|---|---|---|
| Iteração inicial proposta | **Não registrado** | Cadastro, recepção e vistoria básica; preparar token | **Recorte não confirmado** | Ver Seção 2, sem atribuir tudo a esta única iteração | Planejamento inicial e PRs |
| Última iteração solicitada pelo professor | **A identificar pela equipe** | **A confirmar** | **A confirmar** | **A reconstruir pelas datas dos PRs e tarefas** | GitHub Projects + histórico de PRs |

> **Ação de validação:** completar esta tabela após verificar as datas efetivas e a lista de tarefas que já estava planejada no início da última iteração. Não reconstruir “planejamento inicial” a partir de entregas conhecidas sem indicar que se trata de reconstituição retrospectiva.

---

## 6. Burndown Chart — última iteração

**Situação:** dados históricos insuficientes para gerar um gráfico real neste momento. Esta seção registra o método adotado e os campos que faltam, em vez de inventar uma curva.

### 6.1 Critério de medição

A equipe deverá utilizar **quantidade de tarefas restantes** se não existirem pontos de história aprovados. Se existirem estimativas consensuais documentadas, poderá utilizar **pontos restantes**, identificando claramente a unidade no gráfico.

A comparação deve partir de um **escopo inicial da iteração** e considerar a conclusão de cada tarefa na sua data efetiva. Tarefas adicionadas ou retiradas do escopo precisam ser registradas como mudanças de escopo.

### 6.2 Dados necessários

| Campo | Valor / evidência |
|---|---|
| Nome da última iteração | A confirmar |
| Data de início | A confirmar |
| Data de encerramento | A confirmar |
| Unidade de medida | Tarefas restantes, caso não haja pontos formalizados |
| Tarefas planejadas no início | A identificar |
| Quantidade inicial de trabalho | A calcular com base no escopo confirmado |
| Data de conclusão de cada tarefa | Consultar issues, PRs, commits e registros de review |
| Adições/remoções de escopo | Registrar, se ocorreram |

### 6.3 Tabela para apuração diária

Preencher **uma linha por dia da iteração** após identificar o período real.

| Data | Trabalho restante ideal | Trabalho restante observado | Tarefas concluídas no dia | Alteração de escopo / observação |
|---|---:|---:|---|---|
| A preencher | — | — | — | A confirmar |

A linha **ideal** começa com o trabalho planejado e chega a zero ao final do período. A linha **observada** considera apenas os registros verificáveis de conclusão. Se sobrou trabalho, o valor final observado permanece acima de zero.

### 6.4 Gráfico e interpretação

- **Gráfico:** a gerar após o preenchimento da tabela 6.3, com título *Burndown — última iteração do Triagio*.
- **Eixo X:** datas/dias da iteração.
- **Eixo Y:** trabalho restante (na unidade escolhida).
- **Séries:** `Ideal` e `Observado`.
- **Interpretação:** explicar atrasos, adiantamentos e alterações de escopo com base em registros reais, sem atribuir causas não documentadas.

O gráfico será adicionado aqui após a conferência dos dados com os quatro integrantes.

---

## 7. Retrospectiva e próximos passos

### 7.1 Aspectos observáveis nas evidências

- O desenvolvimento foi dividido por módulos e integrado por Pull Requests.
- A equipe utilizou revisão de código antes de incorporar mudanças ao projeto.
- Foram implementados testes automatizados e um workflow de CI no GitHub Actions.
- O quadro Kanban foi criado para centralizar o acompanhamento das tarefas.

### 7.2 Dificuldades e pontos de melhoria documentais

- O planejamento original não foi acompanhado no próprio arquivo com atualização contínua das situações das histórias.
- Datas efetivas e estimativas de esforço não foram registradas de maneira suficiente para produzir automaticamente o Burndown.
- É necessário distinguir o histórico geral do repositório do escopo da última iteração.

### 7.3 Decisões pendentes de validação pelo grupo

- [ ] Confirmar as datas e o escopo da última iteração.
- [ ] Identificar a conclusão diária das tarefas dessa iteração.
- [ ] Validar e inserir o Burndown Chart real.
- [ ] Confirmar situações e responsáveis atuais no GitHub Projects.
- [ ] Registrar uma retrospectiva efetivamente discutida entre os quatro integrantes.
- [ ] Definir e executar a tarefa de CD, se exigida na disciplina.
- [ ] Revisar segurança, implantação e demonstração final com dados fictícios.

---

## 8. Evidências e links de consulta

- **Repositório:** <https://github.com/Hemillio/triagio>
- **Pull Requests:** <https://github.com/Hemillio/triagio/pulls?q=is%3Apr>
- **Quadro Kanban:** <https://github.com/users/Hemillio/projects/1>
- **GitHub Actions:** <https://github.com/Hemillio/triagio/actions>
- **Documento de processo:** [PROCESSO.md](PROCESSO.md)
- **Requisitos e histórias:** [REQUISITOS.md](REQUISITOS.md)
- **Contribuição e revisão:** [CONTRIBUTING.md](CONTRIBUTING.md)

**Nota de integridade documental:** esta versão reúne o planejamento visível nos registros fornecidos pelo grupo e a evolução conhecida até 17/11/2026. Antes de mesclar na `main`, conferir no GitHub a correspondência exata dos PRs, as datas efetivas, a autoria e eventuais mudanças posteriores. Os campos não comprovados permanecem identificados como pendentes, em vez de apresentados como fatos.
