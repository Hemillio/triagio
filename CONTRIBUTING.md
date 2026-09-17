# Como contribuir

Este arquivo registra as convenções de contribuição do projeto Triagio.

## Ramos

Todo trabalho deve partir de uma `main` atualizada.

Padrões:

- `feat/<descricao-curta>` — nova funcionalidade;
- `fix/<descricao-curta>` — correção;
- `docs/<descricao-curta>` — documentação;
- `refactor/<descricao-curta>` — reorganização sem mudança de comportamento;
- `test/<descricao-curta>` — testes;
- `chore/<descricao-curta>` — manutenção do projeto.

Exemplos:

```text
feat/checklist-vistoria
docs/requisitos
fix/agendamento-duplicado
```

Não realizar commits diretamente na `main`.

## Commits

Usar mensagens no padrão Conventional Commits:

```text
tipo(escopo): resumo curto
```

Exemplos:

```text
feat(vistoria): adiciona registro de avarias
docs(requisitos): detalha critérios da HU-03
fix(agenda): impede conflito de horário
```

Quando houver issue correspondente, referenciá-la no commit ou no pull request.

## Pull requests

Cada pull request deve:

- tratar de um único item de backlog ou mudança coerente;
- explicar o que foi alterado;
- indicar como revisar/testar;
- apontar a issue relacionada, quando existir;
- atualizar documentação e diagramas quando a mudança afetar requisitos ou projeto;
- ser revisado por uma pessoa diferente do autor.

Prazo esperado para primeira revisão: até 24 horas, quando possível.

Após aprovação, a integração deve ser feita na `main` e o ramo de trabalho pode ser removido.

## Revisão

O revisor deve verificar:

- aderência ao requisito e aos critérios de aceitação;
- clareza da mudança;
- impacto em outros módulos;
- necessidade de atualizar `REQUISITOS.md`, `PROJETO.md` ou diagramas;
- ausência de segredos, arquivos locais e artefatos gerados.

## Divergência técnica

A discussão deve permanecer registrada no pull request.

Se não houver acordo após dois ciclos de comentários:

1. o responsável pelo módulo afetado apresenta a decisão e a justificativa;
2. se a decisão envolver mais de um módulo, a equipe decide por maioria simples;
3. a decisão final e sua consequência ficam registradas no próprio pull request e, quando for decisão de projeto, no `PROJETO.md`.

## Definição de pronto

Um item está pronto quando:

- seus critérios de aceitação foram atendidos;
- foi revisado por outro integrante;
- foi integrado à `main`;
- a issue relacionada foi encerrada;
- a documentação afetada foi atualizada.
