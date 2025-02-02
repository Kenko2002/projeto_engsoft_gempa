[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=paulossjunior_calculovolume&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=paulossjunior_calculovolume)


![Tests](https://img.shields.io/github/actions/workflow/status/paulossjunior/calculovolume/python-tests-sonar.yml?label=Tests&logo=github)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?logo=codecov)
![SonarCloud](https://img.shields.io/badge/SonarCloud-Passing-brightgreen?logo=sonarcloud)
![License](https://img.shields.io/badge/License-MIT-blue)

Este projeto é uma solução simples e eficiente para calcular o volume de um cilindro, com foco em **qualidade de código** e **boas práticas**. 🎯

Com testes automatizados, integração contínua via **GitHub Actions** e análise de qualidade com **SonarCloud**, estamos prontos para garantir um código **limpo, confiável e escalável**! 🚀

---

## 🛠️ Funcionalidades

- 📐 **Cálculo do Volume**: Implementa a fórmula \( V = \pi \cdot r^2 \cdot h \).
- ✅ **Validação de Dados**: Garante que o raio e a altura sejam valores positivos.
- 🔍 **Testes Automatizados**: Cobre casos válidos e inválidos.
- 📊 **Cobertura de Código**: Mede a cobertura com `pytest-cov`.
- 🤖 **Integração com CI/CD**:
  - **Testes Automatizados** via GitHub Actions.
  - **Qualidade de Código** com SonarCloud.

---

## 🏗️ Estrutura do Projeto

```
.
├── volume_cilindro.py       # Código principal
├── test_volume_cilindro.py  # Testes com pytest
├── .github/
│   └── workflows/
│       └── python-tests-sonar.yml  # Workflow para GitHub Actions
└── README.md                # Documentação
```

---

## 🧩 Como Usar

1. **Cálculo do Volume:**

   ```python
   from volume_cilindro import calcular_volume_cilindro

   raio = 3
   altura = 5
   volume = calcular_volume_cilindro(raio, altura)
   print(f"O volume do cilindro é: {volume:.2f}")
   ```

2. **Executando os Testes Localmente:**

   ```bash
   pytest --cov=volume_cilindro
   ```

3. **Gerando Relatório de Cobertura Localmente:**

   ```bash
   pytest --cov=volume_cilindro --cov-report=xml
   ```

---

## ⚙️ Integração com GitHub Actions

Este repositório utiliza o **GitHub Actions** para CI/CD. O workflow realiza os seguintes passos:

1. **Job de Testes:**
   - Roda os testes automatizados com `pytest`.
   - Gera o relatório de cobertura no formato XML.
   - Armazena o relatório como artefato.

2. **Job de SonarCloud:**
   - Faz o download do relatório gerado.
   - Envia os dados para o SonarCloud.

### 💻 Configuração do Workflow

1. Configure seu projeto no SonarCloud ([Iniciar](https://sonarcloud.io/)).
2. Gere um **token** no SonarCloud e adicione ao GitHub Secrets como `SONAR_TOKEN`.
3. Atualize o arquivo `.github/workflows/python-tests-sonar.yml` com:
   - O nome da organização: `-Dsonar.organization=seu_organizacao`.
   - O nome do projeto: `-Dsonar.projectKey=seu_projeto`.

---

## 🏆 Resultado Esperado

- **GitHub Actions:** 
  - ✅ Testes executados automaticamente.
  - 📂 Relatório de cobertura armazenado como artefato.

- **SonarCloud:** 
  - 🔍 Análise de qualidade do código.
  - 📊 Cobertura de código visível no painel.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.7+**
- **pytest** para testes.
- **pytest-cov** para cobertura.
- **GitHub Actions** para CI/CD.
- **SonarCloud** para análise de qualidade de código.

---
# Como Fazer um Kamehameha 🐉💥

**Atenção**: Este é um guia fictício para fãs de *Dragon Ball*. O Kamehameha é uma técnica de energia fictícia e não funciona no mundo real. Use apenas para roleplay, cosplay ou diversão!

---

## 📋 Pré-requisitos
- **Energia Ki (fictícia):** Você precisa acreditar que possui energia interior (ki) acumulada.
- **Postura Correta:** Inspirada no estilo da Tartaruga (Kame-Sennin).
- **Gritos Opcionais:** Quanto mais alto, mais poderoso (segundo as leis do anime).
- **Cabelo Estiloso (opcional):** Se seu cabelo ficar espetado ao carregar, você está no caminho certo.

---

## 🐢 Passo a Passo

### 1. **Posição Inicial**
- Afaste as pernas na largura dos ombros.
- Flexione levemente os joelhos.
- Estenda os braços para os lados, como se estivesse segurando uma esfera invisível.

### 2. **Foco no Ki**
- Feche os olhos e concentre-se em sua "energia interior".
- Imagine uma luz azul brilhante se formando entre suas mãos.
- **Dica avançada:** Grite **"Haaaaaa!"** para acelerar o processo.

### 3. **Carregando o Kamehameha**
- Junte as mãos na altura do quadril, palmas viradas para frente.
- Grite **"Ka... me... ha... me..."** lentamente, enquanto "puxa" energia imaginária.
- **Efeito Visual (opcional):** Balance os braços para trás como o Goku.

### 4. **Liberação do Poder**
- Quando sentir que a energia está no limite, empurre as mãos para frente.
- Grite **"HAAAAAA!"** com toda sua força.
- **Direcione o Ataque:** Aponte para um alvo imaginário (ex: uma montanha fictícia).

---

## ⚡ Dicas para Perfeição
- **Treine em Grupo:** Convide amigos para fazerem um Kamehameha em sincronia.
- **Use Efeitos Sonoros:** "Whooosh" e "Boom" aumentam o dano em 50% (na sua imaginação).
- **Roupas Rasgadas:** Funcionam como um multiplicador de poder (segundo as regras do anime).

---

## 🚫 Avisos Importantes
- Não tente isso em áreas públicas sem aviso prévio (você pode assustar os vizinhos).
- Nenhuma energia real será liberada, mas sua paixão por Dragon Ball pode aumentar drasticamente.

---

🌌 **Créditos:**  
Técnica desenvolvida pelo Mestre Kame-Sennin.  
Adaptado por [Seu Nome] para fins educacionais fictícios.  

🔄 **Próximo Tutorial:** Como voar usando o Bukujutsu (ou pelo menos pular bem alto).

# Como Voar de Foguete Para o Sol

---

## 📋 Pré-requisitos
- **Um Foguete**
- **Parceria Bilionária com a NASA**
- **Força de Vontade**