import tkinter as tk
from tkinter import filedialog
from telas.CTkPDFViewer import *
import shutil
import customtkinter as ct
import os


class PDFView:
    def __init__(self,path, root):
        
        self.path = path
        self.root = root
        
        toolbar = ct.CTkFrame(self.root.frame_view_pdf, corner_radius=0, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="nsew")

        save_button = ct.CTkButton(toolbar, text="Salvar PDF", command=self.save_pdf, compound="right",  text_color=("gray10", "#DCE4EE"))
        save_button.grid(row=5, column=1, padx=10, pady=5, sticky="w") 
        
        voltar_button = ct.CTkButton(toolbar, text="Voltar", command=self.voltar, compound="right",  text_color=("gray10", "#DCE4EE"))
        voltar_button.grid(row=5, column=1, padx=155, pady=5, sticky="w")         


        self.pdf_viewer = CTkPDFViewer(self.root.frame_view_pdf, file=self.path)
        self.pdf_viewer.grid(row=1, column=0, sticky="nsew")

    
    def voltar(self):
        self.root.select_frame_by_name()
            
    def save_pdf(self):
        # Lógica para salvar o PDF
        nome = os.path.basename(self.path)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")], confirmoverwrite=True, initialfile=nome)
        if file_path:
            try:
                # Copia o arquivo PDF para o novo local
                shutil.copy(self.pdf_viewer.file, file_path)
                tk.messagebox.showinfo("Salvo", "Arquivo salvo com sucesso em {}".format(file_path))
            except Exception as e:
                tk.messagebox.showerror("Erro ao salvar", "Ocorreu um erro ao salvar o PDF:\n{}".format(str(e)))
