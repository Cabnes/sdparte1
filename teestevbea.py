import random
import threading
import time

def minha_funcao():
    # Esta é a função que você deseja chamar a cada 5 segundos
    print("Função chamada a cada 5 segundos")

def chamar_funcao_repetidamente():
    while True:
        minha_funcao()
        # Espera por 5 segundos antes de chamar a função novamente
        time.sleep(random.randint(0,5))

# Inicia o ciclo de chamadas da função
threading.Thread(target=chamar_funcao_repetidamente).start()


chamar_funcao_repetidamente()
