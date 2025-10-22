# Modelagem do domínio — ER Diagram (Checkpoint1)

![ER Diagram](diagram_myapp.png)

## Resumo
Diagrama gerado automaticamente via `django-extensions` (`graph_models`) a partir das models da app `myapp`. Mostra as entidades principais do sistema acadêmico: **Aluno**, **Professor**, **Turma**, **Disciplina** e a ligação com o model `User` do Django.

---

## Entidades e campos (visão concisa)

### Aluno
- **id** — BigAutoField (PK)  
- **turma** — ForeignKey → `Turma` (FK)  
- **user** — OneToOneField → `auth.User` (FK, identifica a conta do aluno)  
- **data_nascimento** — DateField  
- **matricula** — CharField

Observações: cada Aluno pertence a exatamente uma Turma (1:N Turma → Aluno). O `user` vincula o Aluno ao login/conta do Django (um-para-um).

---

### Professor
- **id** — BigAutoField (PK)  
- **user** — OneToOneField → `auth.User` (FK, identifica a conta do professor)  
- **departamento** — CharField

Observações: o Professor também usa `User` para autenticação; relação 1:1.

---

### Turma
- **id** — BigAutoField (PK)  
- **nome** — CharField

Observações: Turma possui vários Alunos (relação 1:N). No diagrama a associação foi nomeada `turma (alunos)`.

---

### Disciplina
- **id** — BigAutoField (PK)  
- **nome** — CharField

---

### User (Django `auth.User`)
- Representa contas de usuário do Django (username, email, senha, etc).  
- Relacionado por OneToOne com `Aluno` e `Professor` (cada conta pode ser um Aluno ou Professor).

---

## Cardinalidades principais (em palavras)
- **Turma 1 — N Aluno** (uma turma tem muitos alunos; cada aluno pertence a uma turma).
- **User 1 — 1 Aluno** (cada aluno tem uma conta do tipo `User`).
- **User 1 — 1 Professor** (cada professor tem uma conta do tipo `User`).
- **Disciplina**: atualmente isolada (0 relacionamentos); avaliar M2M se necessário.

---

## Como o diagrama foi gerado (comando usado)
No diretório onde está o `manage.py`:
```bash
python manage.py graph_models myapp -o docs/diagram_myapp.png --pygraphviz
```
(se usou `pydot`, substituir `--pygraphviz` por `--pydot`)

### Avisos observados na execução
Durante a geração apareceram avisos do Pango sobre fontes (ex.: `couldn't load font "Roboto..."`) — **são apenas warnings de renderização de fonte** e não impedem a criação da imagem; o Graphviz usa fontes alternativas automaticamente.

