
## 🏁 Sprint 1

### 🏆 Sprint Goal
> Desenvolver a base funcional do sistema: receber perguntas dos usuários, enviar para dois modelos LLMs, coletar avaliações individuais e armazenar os dados para posterior análise e treinamento.

### 📂 Tarefas Sprint 1

| Status | Tarefa | Descrição | User Story Relacionada | Definition of Done (DoD) |
|:---|:---|:---|:---|:---|
| Done | Criar estrutura de banco de dados (DDL) | Criar tabelas `pergunta`, `resposta` e `comparacao` no PostgreSQL | Como Cientista de Dados, quero ter acesso ao histórico de perguntas, respostas e avaliações | Scripts executados e banco validado sem erros. |
| Done | Desenvolver função para envio de pergunta (App.py) | Permitir ao usuário inserir perguntas para teste | Como Avaliador, quero enviar minhas perguntas para realizar diversos testes personalizados | Pergunta enviada, armazenada e utilizada na sequência. |
| Done | Integrar chamadas às APIs de LLM (Groq API) | Consultar dois modelos diferentes e obter respostas | Como Avaliador, quero obter respostas de 2 modelos de linguagem | As duas respostas devem ser recebidas e impressas corretamente. |
| Done | Criar coleta de avaliações individuais (chat1) | Solicitar notas para relevância, linguagem, veracidade e ética | Como Avaliador, quero dar notas para as respostas de acordo com critérios pré-definidos | Todas notas recebidas (1 a 5) para ambas as respostas. |
| Done | Adicionar justificativas textuais às avaliações | Coletar textos de explicação para cada nota dada | Como Avaliador, quero explicar minhas avaliações com textos | Textos associados corretamente às respectivas notas. |
| Done | Salvar avaliações no banco de dados (operationsBD.py) | Inserir perguntas, respostas e avaliações no banco | Como Cientista de Dados, quero ter acesso ao histórico de perguntas, respostas e avaliações | Todos os dados persistidos e disponíveis para consulta. |

