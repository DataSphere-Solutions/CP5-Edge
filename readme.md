# Edge Computing - CP5 - Data Logger / Dashboard
Olá, bem-vindo ao nosso trabalho do Check Point 5 de Edge Computing! Nós somos a empresa Data Sphere da turma 1ESPH, e é um imenso prazer apresentar este projeto.

![Data Sphere1000x1000](https://github.com/ianmonteirom/CP2-Edge/assets/152393807/0fe80a9b-6290-417d-8367-2abe3824d0b0)
Logo da nossa equipe
## O que é a Data Sphere?
A Data Sphere Solutions é uma empresa fictícia representando a nossa equipe, formada pelos alunos: 
-  <a href="https://www.linkedin.com/in/artur-alves-tenca-b1ba862b6/">Artur Alves</a> - RM 555171 
- <a href="https://www.linkedin.com/in/giuliana-lucas-85b4532b6/">Giuliana Lucas</a> - RM 557597
- <a href="https://www.linkedin.com/in/ian-monteiro-moreira-a4543a2b7/">Ian Monteiro</a> - RM 558652 
- <a href="https://www.linkedin.com/in/igor-brunelli-ralo-39143a2b7/">Igor Brunelli</a> - RM 555035
- <a href="https://www.linkedin.com/in/matheus-estev%C3%A3o-5248b9238/">Matheus Alcântara</a> - RM 558193

## Máquina Virtual hospedada na Nuvem
Utilizando a Microsoft Azure, hospedamos e configuramos uma máquina virtual (VM) com Ubuntu Server de sistema operacional. Nela, instalamos o Docker, o Docker Compose e o Fiware Descomplicado do professor Fábrio Cabrini, e abrimos as portas necessárias para todas as comunicações neste projeto serem possíveis.
![image](https://github.com/user-attachments/assets/40755ca2-5925-4e9e-a063-1c94e3953cbb)

## Simulação no Wokwi
Utilizando o simulador online Wokwi e configurando o código corretamente para a comunicação dos dados, podemos enviar os valores de luminosidade, umidade e temperatura captados pelos sensores LDR e DHT para o Postman:
![image](https://github.com/user-attachments/assets/6e7e57d1-fd03-48a4-8a38-1bcc5d2b7088)

- Link do Projeto: https://wokwi.com/projects/410952264842122241

## Postman
Utilizando o Postman para ler a coleção do API do Fiware Descomplicado (adaptado para este Checkpoint) e configurando o IP público da VM, fazemos os health checks e confirmamos que está tudo comunicando corretamente.
![image](https://github.com/user-attachments/assets/7b1031b4-1573-4ad7-8c35-3b113f16056a)
Através do Postman, podemos verificar os valores de luminosidade, umidade e temperatura que estão sendo enviados pelo Wokwi:
![image](https://github.com/user-attachments/assets/86e87e41-a210-4941-809e-d76d8e84cb9b)
![image](https://github.com/user-attachments/assets/f44b98dd-b6a7-4964-9c7f-73a24f7e3d8b)
![image](https://github.com/user-attachments/assets/56b9e19f-4f39-42fa-a841-9368b22966d7)

Podemos também pedir um número específico de valores salvos pelo STH-Comet (neste caso, 30):
![image](https://github.com/user-attachments/assets/85022632-e4ed-4757-ab99-19e9d777d4f8)
![image](https://github.com/user-attachments/assets/5cf80513-415f-4bbc-94d9-60364efad37d)
![image](https://github.com/user-attachments/assets/6d64c188-ae32-4d70-b7ad-1f6a4d199741)







## Código do Projeto
```

```
