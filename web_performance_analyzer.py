from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO

class WebCrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Performance Analyzer")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#2c3e50")
        
        # Carregar ícone
        try:
            icon_url = "https://cdn-icons-png.flaticon.com/512/3094/3094843.png"
            response = requests.get(icon_url)
            icon_img = Image.open(BytesIO(response.content))
            self.root.iconphoto(True, ImageTk.PhotoImage(icon_img))
        except:
            pass
        
        self.setup_ui()
        self.driver = None
        self.running = False
        
    def setup_ui(self):
        # Frame de cabeçalho
        header_frame = tk.Frame(self.root, bg="#3498db", height=120)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Título
        title_label = tk.Label(
            header_frame, 
            text="Web Performance Analyzer", 
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#3498db"
        )
        title_label.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Entrada de URL
        url_frame = tk.LabelFrame(main_frame, text="URL para Análise", font=("Arial", 10, "bold"), bg="#ecf0f1")
        url_frame.pack(fill="x", padx=15, pady=15)
        
        self.url_entry = ttk.Entry(url_frame, font=("Arial", 11), width=70)
        self.url_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.url_entry.insert(0, "https://www.example.com")
        
        # Botões de controle
        btn_frame = tk.Frame(main_frame, bg="#ecf0f1")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.start_btn = ttk.Button(
            btn_frame, 
            text="Iniciar Análise", 
            command=self.start_crawler,
            style="Accent.TButton"
        )
        self.start_btn.pack(side="left", padx=(0, 10))
        
        self.stop_btn = ttk.Button(
            btn_frame, 
            text="Parar", 
            command=self.stop_crawler,
            state="disabled"
        )
        self.stop_btn.pack(side="left")
        
        ttk.Button(
            btn_frame, 
            text="Salvar Como...", 
            command=self.save_as
        ).pack(side="right")
        
        # Área de logs
        log_frame = tk.LabelFrame(main_frame, text="Logs de Execução", font=("Arial", 10, "bold"), bg="#ecf0f1")
        log_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.log_area = scrolledtext.ScrolledText(
            log_frame, 
            font=("Consolas", 10), 
            bg="#2c3e50", 
            fg="#ecf0f1",
            insertbackground="white"
        )
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_area.config(state="disabled")
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief="sunken", 
            anchor="w"
        )
        status_bar.pack(side="bottom", fill="x")
        
        # Configurar estilos
        self.setup_styles()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configurar cores
        style.configure("TFrame", background="#ecf0f1")
        style.configure("TLabel", background="#ecf0f1", foreground="#2c3e50")
        style.configure("TButton", font=("Arial", 10), padding=6)
        style.configure("Accent.TButton", background="#3498db", foreground="white", font=("Arial", 10, "bold"))
        style.map("Accent.TButton", 
                 background=[("active", "#2980b9"), ("disabled", "#bdc3c7")],
                 foreground=[("disabled", "#7f8c8d")])
        
        style.configure("TLabelFrame", background="#ecf0f1")
        style.configure("TEntry", font=("Arial", 11))
        
    def log_message(self, message, tag=None):
        self.log_area.config(state="normal")
        self.log_area.insert("end", message + "\n", tag)
        self.log_area.see("end")
        self.log_area.config(state="disabled")
        self.status_var.set(message)
        self.root.update()
        
    def start_crawler(self):
        if self.running:
            return
            
        url = self.url_entry.get().strip()
        if not url.startswith("http"):
            messagebox.showerror("Erro", "Por favor, insira uma URL válida (começando com http/https)")
            return
        
        self.running = True
        self.start_btn.state(["disabled"])
        self.stop_btn.state(["!disabled"])
        self.log_area.config(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.config(state="disabled")
        
        self.log_message("🚀 Iniciando análise de desempenho...")
        self.log_message(f"🔍 URL analisada: {url}")
        
        # Iniciar thread para a execução do crawler
        threading.Thread(target=self.run_crawler, args=(url,), daemon=True).start()
        
    def stop_crawler(self):
        self.running = False
        self.log_message("⏹️ Parando análise...")
        self.stop_btn.state(["disabled"])
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        
    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if file_path:
            try:
                if hasattr(self, 'df_final'):
                    self.df_final.to_excel(file_path, index=False)
                    messagebox.showinfo("Sucesso", f"Dados salvos em:\n{file_path}")
                else:
                    messagebox.showwarning("Aviso", "Nenhum dado disponível para salvar")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar arquivo:\n{str(e)}")
    
    def run_crawler(self, url):
        try:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=options)
            
            self.log_message("🌐 Acessando PageSpeed Insights...")
            self.driver.get("https://pagespeed.web.dev/")
            
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
            
            self.log_message("📤 Enviando URL para análise...")
            search_input = self.driver.find_element(By.TAG_NAME, "input")
            search_input.clear()
            search_input.send_keys(url)
            
            analyze_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Analisar']"))
            )
            analyze_button.click()
            
            self.log_message("⏳ Aguarde, análise em andamento...")
            resultados = self.coletar_dados()
            
            self.df_novo = pd.DataFrame(resultados, columns=["Data", "Métrica", "Valor", "Contexto"])
            self.df_final = self.df_novo
            
            self.log_message(f"✅ Análise concluída! {len(self.df_novo)} métricas coletadas")
            self.log_message("💾 Dados prontos para exportação")
            
            # Mostrar preview dos dados
            self.log_message("\n📋 Amostra dos dados coletados:")
            sample_data = self.df_novo.head(5)
            for _, row in sample_data.iterrows():
                self.log_message(f"  - {row['Métrica']}: {row['Valor']} ({row['Contexto']})")
            
            self.log_message("\n⭐ Clique em 'Salvar Como...' para exportar os resultados")
            
        except Exception as e:
            self.log_message(f"❌ Erro durante a execução: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
            self.running = False
            self.start_btn.state(["!disabled"])
            self.stop_btn.state(["disabled"])
    
    def get_date_string(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    def coletar_dados(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-labelledby='mobile_tab'], [aria-labelledby='desktop_tab']"))
        )
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        date_string = self.get_date_string()
        resultados = []
        
        abas = {
            'mobile_tab': 'Mobile',
            'desktop_tab': 'Desktop'
        }
        
        contexto_labels = ['URL atual', 'Origem']
        self.log_message(f"📊 Coletando dados para {len(abas)} dispositivos...")
        
        for aba_id, aba_nome in abas.items():
            aba = soup.select_one(f"[aria-labelledby='{aba_id}']")
            if not aba:
                continue
            
            blocos = aba.select(".zqSD3")
            botoes = aba.select(".jdJzpe")
            
            for i, (bloco, botao) in enumerate(zip(blocos, botoes)):
                tipo_contexto = contexto_labels[i] if i < len(contexto_labels) else 'Desconhecido'
                contexto = f"{aba_nome} ({tipo_contexto})"
                
                if botao.has_attr("disabled"):
                    self.log_message(f"⚠️ {contexto} indisponível para análise.")
                    continue
                
                nomes = bloco.select(".eNGozb")
                valores = bloco.select(".f49ZR")
                
                for nome, valor in zip(nomes, valores):
                    nome_metrica = nome.text.strip() if nome else "N/A"
                    valor_metrica = valor.text.strip() if valor else "N/A"
                    resultados.append([date_string, nome_metrica, valor_metrica, contexto])
                
                self.log_message(f"✓ Dados coletados para {contexto}")
        
        return resultados

if __name__ == "__main__":
    root = tk.Tk()
    app = WebCrawlerApp(root)
    
    # Carregar e exibir logo
    try:
        logo_url = "https://i.imgur.com/Kv8e6dG.png"
        response = requests.get(logo_url)
        logo_img = Image.open(BytesIO(response.content))
        logo_img = logo_img.resize((200, 80), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        
        logo_label = tk.Label(root, image=logo_photo, bg="#2c3e50")
        logo_label.image = logo_photo
        logo_label.place(x=20, y=15)
    except:
        pass
    
    root.mainloop()