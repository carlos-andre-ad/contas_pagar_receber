import tkinter as tk
from tkinter import filedialog
from Utils.CTkPDFViewer import *
import shutil
import customtkinter as ct


class PDFView:
    def __init__(self,path):
        
        self.path = path

        pdf_viewer_window = tk.Toplevel()
        pdf_viewer_window.title("Visualizador de PDF")
        largura_tela = pdf_viewer_window.winfo_screenwidth()
        altura_tela = pdf_viewer_window.winfo_screenheight()
        pdf_viewer_window.geometry(f"{largura_tela}x{altura_tela}+0+0")
        pdf_viewer_window.grid_columnconfigure(0, weight=1)
        pdf_viewer_window.attributes('-fullscreen', True)  # Maximizar a janela
        pdf_viewer_window.attributes('-toolwindow', True)   # Remover bordas e barra de título

        toolbar = ct.CTkFrame(pdf_viewer_window, corner_radius=0, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="nsew")

        save_button = ct.CTkButton(toolbar, text="Salvar PDF", command=self.save_pdf, compound="right",  text_color=("gray10", "#DCE4EE"))
        save_button.grid(row=5, column=1, padx=10, pady=5, sticky="w") 
        
        close_button = ct.CTkButton(toolbar, text="Fechar", command=pdf_viewer_window.destroy, compound="right",  text_color=("gray10", "#DCE4EE"))
        close_button.grid(row=5, column=1, padx=150, pady=5, sticky="w") 

        pdf_viewer = CTkPDFViewer(pdf_viewer_window, file=self.path)
        pdf_viewer.grid(row=1, column=0, sticky="nsew")
        pdf_viewer_window.grid_rowconfigure(1, weight=1)
        ct.set_appearance_mode("Dark")

            
    def save_pdf(self):
        # Lógica para salvar o PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if file_path:
            try:
                # Copia o arquivo PDF para o novo local
                shutil.copy(self.pdf_viewer.file, file_path)
                tk.messagebox.showinfo("Salvo", "PDF salvo com sucesso em {}".format(file_path))
            except Exception as e:
                tk.messagebox.showerror("Erro ao salvar", "Ocorreu um erro ao salvar o PDF:\n{}".format(str(e)))
