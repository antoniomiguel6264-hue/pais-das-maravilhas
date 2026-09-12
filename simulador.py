import tkinter as tk

class SimuladorComputador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Fluxo da CPU - V2")
        self.root.geometry("500x300")
        
        # Componente: Memória RAM
        self.lbl_ram = tk.Label(root, text="RAM\n[ Dado: 42 ]", bg="lightblue", width=15, height=4, relief="groove")
        self.lbl_ram.pack(side="left", padx=40)
        
        # Componente: Registrador da CPU
        self.lbl_cpu = tk.Label(root, text="CPU (Registrador)\n[ Vazio ]", bg="lightgray", width=15, height=4, relief="groove")
        self.lbl_cpu.pack(side="right", padx=40)
        
        # Botão para iniciar o fluxo (corrigido de btn_buss para btn_bus)
        self.btn_bus = tk.Button(root, text="Buscar Dado (Fetch)", command=self.simular_fluxo)
        self.btn_bus.pack(side="bottom", pady=20)

    def simular_fluxo(self):
        # Desabilita o botão para evitar cliques repetidos durante a animação
        self.btn_bus.config(state="disabled")
        
        # Reseta o estado visual da CPU para o padrão
        self.lbl_cpu.config(text="CPU (Registrador)\n[ Vazio ]", bg="lightgray")
        
        # Etapa 1: Destaca a RAM (Lendo o dado)
        self.lbl_ram.config(bg="yellow")
        
        # Etapa 2: Substituído o time.sleep() pelo .after() do Tkinter
        # Isso agenda a função 'finalizar_fluxo' para rodar após 1000ms (1 segundo) sem travar a interface
        self.root.after(1000, self.finalizar_fluxo)

    def finalizar_fluxo(self):
        # RAM volta ao normal
        self.lbl_ram.config(bg="lightblue")
        
        # CPU recebe o dado e acende em verde
        self.lbl_cpu.config(text="CPU (Registrador)\n[ Dado: 42 ]", bg="lightgreen")
        
        # Reativa o botão para permitir uma nova simulação
        self.btn_bus.config(state="normal")

# Inicializa o programa
if __name__ == "__main__":
    janela = tk.Tk()
    app = SimuladorComputador(janela)
    janela.mainloop()
