# Triagio — Sistema Web de Atendimento e Triagem para Oficina

Sistema web simples e intuitivo desenvolvido como projeto prático para a disciplina de Engenharia de Software, focado na digitalização da entrada e vistoria de veículos em oficinas mecânicas.

---

## O Problema

Oficinas mecânicas enfrentam gargalos no processo de recepção e triagem de veículos, incluindo perda de histórico de avarias pré-existentes, contestação de danos no pátio, agendamentos conflitantes e falta de transparência no acompanhamento pelo cliente. 

O **Triagio** resolve essa dor digitalizando a entrada do veículo, permitindo a realização de checklists digitais com fotos, gestão simples de agendamentos e disponibilização de um portal para o cliente acompanhar o status do serviço pela placa.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** Flask (Simples, leve e rápido)
* **Frontend:** HTML5, CSS3 e Bootstrap 5 (design responsivo)
* **Banco de Dados:** SQLite (nativo do Python, sem necessidade de configuração de servidor)

---

## Composição do Time

| Integrante | Eixo de Responsabilidade | Módulo Principal |
| :--- | :--- | :--- |
| **Kauane Coimbra Sousa https://github.com/KauaneCoimbra** | CRM, Frota & Histórico | Cadastro de clientes, veículos e histórico por placa |
| **Hemillio Oliveira Santos https://github.com/Hemillio** | Agendamento & Recepção | Calendário de vistorias, fila de espera e horários |
| **Danilo Feitosa do Carmo https://github.com/danilofeitosac** | Checklist Digital | Vistoria de avarias, fotos do pátio e registro de pertences |
| **João Mateus Monteiro Batista https://github.com/jotaaa728** | Portal do Cliente | Acompanhamento do status pela placa e emissão do laudo |

---

## Instruções de Execução

### Pré-requisitos
* **Git** instalado
* **Python** (versão 3.10 ou superior)
