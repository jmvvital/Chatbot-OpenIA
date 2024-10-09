import time
from openai import OpenAI

client = OpenAI()
ASSISTANT_ID = ""  # ID do assistente

# Contexto inicial para o sistema
#context = """ 
#    Você se chama BIOS
#"""

# Função para pegar a última mensagem da thread
def get_latest_message(thread_id):
    message_response = client.beta.threads.messages.list(thread_id=thread_id)
    messages = message_response.data
    return messages[0] if messages else None

# Início da conversa
print("Bem Vindo! Escreva 'exit' para sair.")

# Primeiro input do usuário
mensagem = input("Você: ")

# Criando a Thread com a primeira mensagem do usuário
thread = client.beta.threads.create(
    messages=[
        #{"role": "system", "content": context},  # Adicionando o contexto
        {"role": "user", "content": mensagem}
    ]
)

# Loop para a conversa contínua
while True:
    # Enviando a Thread para o assistente responder
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f"Run Created: {run.id}")

    # Aguardando conclusão do processamento da resposta
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run Status: {run.status}")
        time.sleep(1)

    # Quando completado, pegando a última mensagem da conversa
    latest_message = get_latest_message(thread.id)
    
    if latest_message:
        print(f"BOT: {latest_message.content[0].text.value}")

    # Usuário insere a próxima mensagem
    mensagem = input("Você: ")

    # Encerrar se o usuário digitar "exit"
    if mensagem.lower() == "exit":
        break

    # Adicionando a nova mensagem do usuário à Thread existente
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",  # Definindo o papel como "user"
        content=mensagem  # Enviando o conteúdo da mensagem
    )

print("Conversa encerrada.")
