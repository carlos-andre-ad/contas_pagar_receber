
import logging
import tempfile

class LogApp():
    def __init__(self, modulo):
        temp_dir = tempfile.gettempdir()
        print(modulo, temp_dir)
        self.modulo = modulo
        logging.basicConfig(level=logging.INFO, filename=f"{temp_dir}/financeiro.log", format="%(asctime)s - %(levelname)s - %(message)s")
    
    def logg(self, mensagem="Sucesso", metodo=None, tipo_mensagem="i" ,tipo=1):
        if metodo != None:
            metodo = f"{metodo} - "
        
        if (tipo_mensagem=="w"):            
            logging.warning(f"{self.modulo}: {metodo} {mensagem}")
        else:
            if (tipo_mensagem=="e"):
                logging.error(f"{self.modulo}: {metodo} {mensagem}") 
            else:
                logging.info(f"{self.modulo}: {metodo} {mensagem}")   