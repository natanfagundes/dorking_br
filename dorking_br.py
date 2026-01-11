import requests
import argparse
import json
import csv
import time
import urllib.parse
from datetime import datetime
from typing import List, Dict
import sys
from dataclasses import dataclass

@dataclass
class ResultadoDork:
    titulo: str
    url: str
    trecho: str
    operador_usado: str
    consulta: str
    data_hora: str

class FerramentaGoogleDorking:
    def __init__(self):
        self.resultados: List[ResultadoDork] = []
        self.sessao = requests.Session()
        self.sessao.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        
        self.dorks_db = {
            "intitle": {"objetivo": "Pesquisa no título da página", "mistura": "sim", "sozinho": "sim", "serviços": ["web","imagens","grupos","notícias"]},
            "allintitle": {"objetivo": "Título da página (todas palavras)", "mistura": "não", "sozinho": "sim", "serviços": ["web","imagens","grupos","notícias"]},
            "inurl": {"objetivo": "Pesquisa na URL", "mistura": "sim", "sozinho": "sim", "serviços": ["web","imagens","grupos","notícias"]},
            "allinurl": {"objetivo": "URL (todas palavras)", "mistura": "não", "sozinho": "sim", "serviços": ["web","imagens","grupos","notícias"]},
            "filetype": {"objetivo": "Pesquisa arquivos específicos", "mistura": "sim", "sozinho": "não muito", "serviços": ["web","grupos"]},
            "allintext": {"objetivo": "Apenas texto da página", "mistura": "não muito", "sozinho": "sim", "serviços": ["web","imagens","grupos","notícias"]},
            "site": {"objetivo": "Pesquisa site específico", "mistura": "sim", "sozinho": "não muito", "serviços": ["web","imagens","grupos"]},
            "link": {"objetivo": "Links para páginas", "mistura": "não", "sozinho": "não muito", "serviços": ["web"]},
            "inanchor": {"objetivo": "Texto âncora de links", "mistura": "sim", "sozinho": "sim", "serviços": ["web","imagens","grupos","notícias"]},
            "numrange": {"objetivo": "Localiza números", "mistura": "sim", "sozinho": "não muito", "serviços": ["web","imagens","grupos"]},
            "daterange": {"objetivo": "Faixa de datas", "mistura": "sim", "sozinho": "não muito", "serviços": ["web","grupos"]},
            "author": {"objetivo": "Autor do grupo", "mistura": "sim", "sozinho": "não muito", "serviços": ["grupos","notícias"]},
            "group": {"objetivo": "Nome do grupo", "mistura": "não muito", "sozinho": "sim", "serviços": ["grupos"]},
            "insubject": {"objetivo": "Assunto do grupo", "mistura": "sim", "sozinho": "como intitle", "serviços": ["grupos"]},
            "msgid": {"objetivo": "ID da mensagem do grupo", "mistura": "não", "sozinho": "não muito", "serviços": ["grupos"]}
        }
    
    def banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║           FERRAMENTA GOOGLE DORKING v2.0 - BRASIL            ║
║                APENAS TESTES AUTORIZADOS!                    ║
║                 Feito por Natan Fagundes                     ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def mostrar_tabela_dorks(self):
        """Mostra tabela COMPLETA dos dorks em PT-BR"""
        print("\n" + "="*130)
        print("📋 TABELA COMPLETA - OPERADORES GOOGLE DORKING")
        print("="*130)
        print(f"{'Operador':<12} {'Objetivo':<30} {'Mistura':<8} {'Sozinho':<10} {'Web':<5} {'Imagens':<8} {'Grupos':<8} {'Notícias':<8}")
        print("-"*130)
        
        for op, dados in self.dorks_db.items():
            web = "✅" if "web" in dados["serviços"] else "❌"
            imagens = "✅" if "imagens" in dados["serviços"] else "❌"
            grupos = "✅" if "grupos" in dados["serviços"] else "❌"
            noticias = "✅" if "notícias" in dados["serviços"] else "❌"
            
            print(f"{op:<12} {dados['objetivo']:<30} {dados['mistura']:<8} {dados['sozinho']:<10} "
                  f"{web:<5} {imagens:<8} {grupos:<8} {noticias:<8}")
        
        print("="*130)
    
    def gerar_exemplos_praticos(self):
        """Exemplos práticos para pentest"""
        exemplos = {
            "📂 Vazamento de Banco de Dados": [
                'intitle:"index of" "database.sql"',
                'filetype:sql "INSERT INTO" -github',
                'inurl:backup filetype:sql'
            ],
            "🔐 Painéis Admin Expostos": [
                'intitle:"admin login" OR "painel administrativo"',
                'inurl:admin filetype:php',
                'allintext:"usuário" "senha" login'
            ],
            "⚙️ Arquivos de Configuração": [
                'filetype:env "DB_PASSWORD" OR "DB_SENHA"',
                'intext:"API_KEY" filetype:txt',
                'intitle:"index of" ".env"'
            ],
            "📄 Documentos Sensíveis": [
                'filetype:pdf "confidencial" OR "secreto"',
                'filetype:doc "uso interno"',
                'inurl:curriculo filetype:pdf site:*.br'
            ],
            "🔍 Brasil Específico": [
                'site:*.gov.br filetype:pdf "confidencial"',
                'intext:"CNPJ" filetype:txt',
                'intitle:"admin" inurl:login site:*.br'
            ]
        }
        
        print("\n" + "="*70)
        print("🎯 EXEMPLOS PRÁTICOS PARA PENTEST (COPIE E COLE!)")
        print("="*70)
        for categoria, dorks in exemplos.items():
            print(f"\n{categoria}:")
            for dork in dorks:
                print(f"   🔍 {dork}")
                print(f"   📎 https://google.com/search?q={urllib.parse.quote(dork)}")
    
    def construir_dork(self, operador: str, palavra_chave: str, site: str = None, tipo_arquivo: str = None) -> str:
        """Constrói dork automaticamente"""
        partes = []
        
        if operador in self.dorks_db:
            partes.append(f"{operador}:\"{palavra_chave}\"")
        else:
            partes.append(f'"{palavra_chave}"')
        
        if site:
            partes.append(f"site:{site}")
        if tipo_arquivo:
            partes.append(f"filetype:{tipo_arquivo}")
        
        return " ".join(partes)
    
    def modo_interativo(self):
        """Modo interativo em português"""
        print("\n🛠️  CONSTRUTOR DE DORK INTERATIVO")
        print("-" * 50)
        
        print("Operadores disponíveis: intitle, inurl, filetype, site, etc")
        operador = input("🔍 Operador: ").strip().lower()
        palavra_chave = input("📝 Palavra-chave: ").strip()
        site = input("🌐 Site (ex: target.com.br) [opcional]: ").strip()
        tipo_arquivo = input("📄 Tipo (pdf/sql/env/txt) [opcional]: ").strip()
        
        dork = self.construir_dork(operador, palavra_chave, site or None, tipo_arquivo or None)
        print(f"\n✅ DORK GERADO: {dork}")
        print(f"\n🔗 URL PRONTA: https://www.google.com/search?q={urllib.parse.quote(dork)}")
        print("\n📋 Copie e cole no Google!")
        
        salvar = input("\n💾 Salvar no arquivo? (s/n): ").lower()
        if salvar == 's':
            self.salvar_resultados()
    
    def salvar_resultados(self, nome_arquivo: str = None, formato: str = "json"):
        """Salva resultados em arquivo"""
        if not nome_arquivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"resultados_dorking_{timestamp}.{formato}"
        
        dados = [r.__dict__ for r in self.resultados]
        
        try:
            if formato == "json":
                with open(nome_arquivo, 'w', encoding='utf-8') as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)
            elif formato == "csv":
                with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
                    if dados:
                        writer = csv.DictWriter(f, fieldnames=dados[0].keys())
                        writer.writeheader()
                        writer.writerows(dados)
            
            print(f"\n💾 Salvo com sucesso: {nome_arquivo} ({len(self.results)} resultados)")
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
    
    def busca_rapida(self, palavras: List[str]):
        """Busca rápida simulada para demo"""
        print(f"\n🔍 BUSCA RÁPIDA: {' '.join(palavras)}")
        print("✅ Dork gerado e pronto para o Google!")
        print(f"📋 URL: https://www.google.com/search?q={urllib.parse.quote(' '.join(palavras))}")
        
        resultado_demo = ResultadoDork(
            "Resultado Demo", 
            "https://exemplo.com", 
            "Trecho demo do resultado", 
            palavras[0] if palavras else "intitle",
            " ".join(palavras),
            str(datetime.now())
        )
        self.resultados.append(resultado_demo)
        
        self.mostrar_resultados()
    
    def mostrar_resultados(self):
        """Mostra resultados bonitinho"""
        print("\n" + "="*90)
        print("📊 RESULTADOS ENCONTRADOS")
        print("="*90)
        
        if not self.resultados:
            print("Nenhum resultado encontrado")
            return
        
        print(f"Total: {len(self.resultados)} resultados")
        print("-"*90)
        
        for i, res in enumerate(self.resultados[:10], 1):
            print(f"{i:2d}. [{res.operador_usado}] {res.titulo[:60]:<60} | {res.url[:50]}")

def main():
    ferramenta = FerramentaGoogleDorking()
    ferramenta.banner()
    
    parser = argparse.ArgumentParser(description="Ferramenta Google Dorking BR")
    parser.add_argument("--tabela", "-t", action="store_true", help="Mostrar tabela dos dorks")
    parser.add_argument("--exemplos", "-e", action="store_true", help="Exemplos práticos")
    parser.add_argument("--interativo", "-i", action="store_true", help="Modo interativo")
    parser.add_argument("--busca", "-b", nargs="*", help="Busca rápida")
    parser.add_argument("--salvar", "-s", help="Salvar resultados")
    
    args = parser.parse_args()
    
    if args.tabela:
        ferramenta.mostrar_tabela_dorks()
    elif args.exemplos:
        ferramenta.mostrar_tabela_dorks()
        ferramenta.gerar_exemplos_praticos()
    elif args.interativo:
        ferramenta.modo_interativo()
    elif args.busca:
        ferramenta.busca_rapida(args.busca)
        if args.salvar:
            ferramenta.salvar_resultados(args.salvar)
        else:
            salvar = input("\n💾 Salvar resultados? (s/n): ").lower()
            if salvar == 's':
                ferramenta.salvar_resultados()
    else:
        # Modo padrão - mostra tudo!
        print("👋 Bem-vindo à Ferramenta Google Dorking BR!")
        ferramenta.mostrar_tabela_dorks()
        ferramenta.gerar_exemplos_praticos()
        print("\n💡 Use --interativo para criar dorks personalizados!")
        print("\n🔥 Comandos rápidos:")
        print("   python dorking_br.py --interativo")
        print("   python dorking_br.py --exemplos")
        print("   python dorking_br.py --busca intitle:admin senha")

if __name__ == "__main__":
    main()
