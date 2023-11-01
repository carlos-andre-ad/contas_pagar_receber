
import tkinter as tk
import locale
import re
class Util():
    def __init__(self):
        pass    
    

    
    def mover_foco(self, event):
        widget = event.widget
        proximo_widget = widget.tk_focusNext()
        if proximo_widget:
            proximo_widget.focus_set()
    
    def formatar_data(self, event, entry_data):
        entrada = entry_data.get()
        if len(entrada) == 2:
            if event.keysym != 'BackSpace':
                entry_data.insert(tk.END, '/')
        elif len(entrada) == 5:
            if event.keysym != 'BackSpace':
                entry_data.insert(tk.END, '/')
        elif len(entrada) > 10:
            entry_data.delete(10, tk.END)
        elif not event.keysym in ('BackSpace', 'Left', 'Right'):
            if not event.char.isdigit():
                return 'break' 
        return None
    
    def formatar_valor(self, event, entry):
        entrada = entry.get()
        entrada = entrada.replace('R$', '').replace(' ', '')  # Remover 'R$' e espaços
        entrada = entrada.replace(',', '')  # Remover vírgulas
        entrada = entrada.replace('.', '')  # Remover pontos antigos

        if entrada:
            valor = float(entrada) / 100  # Converter para float e dividir por 100 para tratar as casas decimais
            entrada_formatada = f'R$ {valor:,.2f}'  # Formatar com separadores de milhar e 2 casas decimais
            entry.delete(0, tk.END)
            entry.insert(0, entrada_formatada)

        return None  
    
    def formatar_valor_real(self, valor):
        #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        #valor_formatado = locale.currency(valor, grouping=True, symbol="R$")
        return valor
    
    def extrair_numeros(self, texto):
        numeros = re.findall(r'\d+', texto)
        numeros_como_string = ''.join(numeros)
        return numeros_como_string    