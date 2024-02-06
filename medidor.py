from serial import Serial
from datetime import datetime
import tkinter as tk
from tkinter import font

# Função para retornar a data dd/mm/aaaa
def consultar_data():
    data = datetime.now()
    dia = data.day
    mes = data.month
    ano = data.year

    return f'{dia:02d}/{mes:02d}/{ano}'

# Função para retornar o horario de brasília hh:mm
def consultar_horario():
    data = datetime.now()
    hora = data.hour
    minutos = data.minute

    return f'{hora:02d}:{minutos:02d}'

# Função para atualizar a label onde contem os valores da temperatura e umidade
def atualizar_label(temperatura, umidade):
    temp.config(text=f'{temperatura}ºC')
    umid.config(text=f'{umidade}%')
    janela.update()

# Função principal, onde verificara a porta serial
# e criará um log.cvs das medições
#
def verificar_porta_serial():
    global porta_serial
    # Ler dados da porta serial
    dados = porta_serial.readline().decode('utf-8').strip()

    # COndição para verificar se a porta serial enviou dados
    if len(dados) > 0:
        lista_dados = dados.split(';')

        temperatura = lista_dados[0][:5]
        umidade = lista_dados[1][:5]

        with open('log_medicoes.csv', 'a+') as medicoes:
            medicoes.seek(0)
            linhas = medicoes.readlines()

            if len(linhas) > 0:# Se existir valores no arquivo colocara os valores registrados
                data = consultar_data()
                horario = consultar_horario()
                informacoes = f'{data};{horario};{temperatura};{umidade}\n'
                medicoes.write(informacoes)

            else:# Ira criar um cabeçalho e em seguida colocara os valores regitrados
                cabecalho = 'data;hora;temperatura;umidade\n'
                medicoes.write(cabecalho)

                data = consultar_data()
                horario = consultar_horario()
                
                informacoes = f'{data};{horario};{temperatura};{umidade}\n'
                medicoes.write(informacoes)


        atualizar_label(temperatura, umidade)

    # Agendar a próxima verificação após 60000 milissegundos (1 hora)
    janela.after(5000, verificar_porta_serial)

# Função que encerra a janela e fecha a conexão da porta serial
def on_closing():
    porta_serial.close()
    janela.destroy()

# Configurar a porta serial 
porta_serial = Serial('COM7', 9600, timeout=1)

# Criar a janela
janela = tk.Tk()
janela.title('Medidor')
janela.geometry('230x180')

# Carregar uma fonte 
fonte_titulo = font.Font(family='Helvetica', size=16, weight='bold')
fonte_info = font.Font(family='Helvetica', size=14, weight='bold')

# Label temperatura
temp_label = tk.Label(janela, text='Temperatura', font=fonte_titulo)
temp_label.pack(pady=3)
# Label onde conterá os valores da temperatura
temp = tk.Label(janela, text='', font=fonte_info)
temp.pack(pady=1)

tk.Label(janela, text='').pack(pady=2)# Apenas expaçamento entre as labels

# Label umidade
umid_label = tk.Label(janela, text='Umidade', font=fonte_titulo)
umid_label.pack(pady=3)
# Label onde conterá os valores da umidade
umid = tk.Label(janela, text='', font=fonte_info)
umid.pack(pady=1)

# Configurar a função de encerramento
janela.protocol('WM_DELETE_WINDOW', on_closing)

# Iniciar a verificação da porta serial após 60000 milissegundos (60 segundos)
janela.after(5000, verificar_porta_serial)

# Iniciar o loop principal da interface gráfica
janela.mainloop()
