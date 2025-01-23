import requests

def test_condicao_endpoint():
    """Testa o endpoint /area-tecnico/condicao/."""
    url = "http://localhost:8000/area-tecnico/condicao/"  # URL do seu endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para códigos de status ruins (4xx ou 5xx)
        print("Resposta do servidor:")
        print(response.text)  # Imprime o conteúdo da resposta
        assert False # força dar erro para debugar a saida no github action
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        assert False, f"Erro na requisição: {e}" # Falha o teste se houver um erro na requisição
