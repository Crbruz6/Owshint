import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def track_username():
    console.print("\n[bold cyan][+][/bold cyan] [bold]Fitur: Lacak Username[/bold]")
    username = Prompt.ask("[bold yellow]Masukkan username target[/bold yellow]")
    
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter/X": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}"
    }
    
    table = Table(title=f"Hasil Pelacakan: {username}")
    table.add_column("Platform", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("URL", style="green")

    with console.status("[bold green]Sedang mencari...[/bold green]") as status:
        for platform, url in sites.items():
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    table.add_row(platform, "[green]Ditemukan[/green]", url)
                else:
                    table.add_row(platform, "[red]Tidak Ada[/red]", "-")
            except requests.RequestException:
                table.add_row(platform, "[yellow]Error/Timeout[/yellow]", "-")
                
    console.print(table)

def scan_web():
    console.print("\n[bold cyan][+][/bold cyan] [bold]Fitur: Scanning Web Subdomain[/bold]")
    domain = Prompt.ask("[bold yellow]Masukkan domain target (contoh: google.com)[/bold yellow]")
    
    subdomains = ["www", "mail", "ftp", "admin", "blog", "api", "dev", "test"]
    
    table = Table(title=f"Subdomain Terdeteksi untuk: {domain}")
    table.add_column("Subdomain", style="cyan")
    table.add_column("Status", style="bold green")
    
    with console.status("[bold green]Memindai subdomain...[/bold green]") as status:
        for sub in subdomains:
            target_url = f"http://{sub}.{domain}"
            try:
                response = requests.get(target_url, timeout=3)
                if response.status_code == 200:
                    table.add_row(f"{sub}.{domain}", f"Aktif (HTTP {response.status_code})")
            except requests.RequestException:
                pass 
                
    console.print(table)

def extract_metadata():
    console.print("\n[bold cyan][+][/bold cyan] [bold]Fitur: Ekstrak Metadata Gambar[/bold]")
    img_path = Prompt.ask("[bold yellow]Masukkan path/jalur file gambar (contoh: foto.jpg)[/bold yellow]")
    
    if not os.path.exists(img_path):
        console.print("[bold red]\[!] File tidak ditemukan![/bold red]")
        return
        
    try:
        image = Image.open(img_path)
        exif_data = image._getexif()
        
        if not exif_data:
            console.print("[bold yellow]\[!] Gambar tidak memiliki metadata EXIF.[/bold yellow]")
            return
            
        table = Table(title=f"Metadata: {os.path.basename(img_path)}")
        table.add_column("Tag", style="cyan")
        table.add_column("Value", style="green")
        
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            val_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            table.add_row(str(tag_name), val_str)
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]\[!] Gagal mengekstrak metadata: {e}[/bold red]")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = """
 ██████╗ ██╗    ██╗███████╗██╗  ██╗██╗███╗   ██╗████████╗
██╔═══██╗██║    ██║██╔════╝██║  ██║██║████╗  ██║╚══██╔══╝
██║   ██║██║ █╗ ██║███████╗███████║██║██╔██╗ ██║   ██║   
██║   ██║██║███╗██║╚════██║██╔══██║██║██║╚██╗██║   ██║   
╚██████╔╝╚███╔███╔╝███████║██║  ██║██║██║ ╚████║   ██║   
 ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   
             [bold red]OWSHINT Framework by Cerberuz69[/bold red]
        """
        console.print(Panel(banner, style="bold blue", expand=False))
        
        console.print("[1] Lacak Username")
        console.print("[2] Scanning Web Subdomain")
        console.print("[3] Ekstrak Metadata Gambar")
        console.print("[4] Keluar\n")
        
        pilihan = Prompt.ask("[bold white]Pilih menu[/bold white]", choices=["1", "2", "3", "4"])
        
        if pilihan == "1":
            track_username()
        elif pilihan == "2":
            scan_web()
        elif pilihan == "3":
            extract_metadata()
        elif pilihan == "4":
            console.print("[bold red]Keluar dari program. Sampai jumpa![/bold red]")
            break
            
        input("\nTekan Enter untuk kembali ke menu utama...")

if __name__ == "__main__":
    main()
  
