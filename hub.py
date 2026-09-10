def print_magico(msg,tempo=0.03):
    import time 
    for letra in msg:
        print(letra,end='',flush=True)
        time.sleep(tempo)

