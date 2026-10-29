# Contrato do módulo de agendamentos — Triagio

Este arquivo detalha a implementação da HU-02 e os critérios CA-02.1 a CA-02.4. É uma proposta técnica, não um enunciado novo da disciplina.

## Dependências

- `app/extensions.py` exporta a instância compartilhada `db`.
- `app/clientes/models.py` exporta `Veiculo` (`__tablename__ = 'veiculos'`, com `id`, `placa`, `modelo`, `ano`, `ativo`).
- `app/agendamentos/models.py` exporta `Agendamento` (`__tablename__ = 'agendamentos'`, com `id`, `veiculo_id`, `data_hora`, `status`).
- `app/templates/base.html` define `{% block content %}`.
- Danilo pode ler `Agendamento.id` e `Agendamento.veiculo_id` para criar uma vistoria ligada ao agendamento.

## Capacidade e agendamentos simultâneos — decisão da equipe

O sistema Triagio foi pensado para oficinas de grande porte, com vários mecânicos e atendimentos simultâneos.

Nesta primeira versão, será permitido cadastrar dois ou mais veículos para o mesmo horário de início.

O sistema não terá uma restrição de unicidade sobre a data e hora dos agendamentos.

Em uma versão futura, será implementado um controle de capacidade de atendimento, considerando a quantidade de mecânicos, vagas ou baias disponíveis.

Até essa implementação, o sistema não verificará automaticamente se a oficina possui capacidade para todos os agendamentos simultâneos.

## Rotas propostas

| Método | Caminho | Entrada | Resposta de sucesso | Erro |
|---|---|---|---|---|
| GET | `/agendamentos` | nenhuma | 200, lista ordenada por data | — |
| GET | `/agendamentos/novo` | nenhuma | 200, formulário | — |
| POST | `/agendamentos/novo` | `veiculo_id`, `data_hora` | 303 para lista | 422, veículo ou data/hora inválidos |


## Dados

- `veiculo_id`: inteiro positivo de veículo existente e ativo.
- `data_hora`: campo HTML `datetime-local` em horário de Palmas.
- Persistência: data/hora convertida para UTC, ISO 8601 com `+00:00`.
- `status`: `Agendado` nesta primeira versão (outros estados dependem de requisito futuro).
- Nenhum dado de cliente é duplicado no agendamento; placa/modelo vêm do relacionamento com `Veiculo`.

## Critérios de aceite deste incremento

- CA-02.1: formulário permite escolher veículo existente e horário.
- CA-02.2: agendamento salvo tem vínculo de banco com aquele veículo.
- CA-02.3: o sistema permite agendar veículos diferentes para o mesmo horário.
- CA-02.4: o sistema apresenta mensagens claras quando o veículo ou a data e hora informados são inválidos.

## Limite de operação

Rotas internas sem autenticação nesta implementação inicial: **uso exclusivamente local, com veículos fictícios**. Proteger o acesso e formulários contra CSRF antes de publicar a aplicação na internet.