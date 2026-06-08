import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Pastikan library phonenumbers sudah terinstall: pip install phonenumbers
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier
except ImportError:
    phonenumbers = None

console = Console()

def track_username():
    console.print("\n[bold cyan][+][/bold cyan] [bold]Fitur: Lacak Username[/bold]")
    username = Prompt.ask("[bold yellow]Masukkan username target[/bold yellow]")
    
    # Menambahkan opsi media sosial yang lebih banyak
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter/X": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
    }
    
    table = Table(title=f"Hasil Pelacakan Sosmed: {username}")
    table.add_column("Platform", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("URL", style="green")

    with console.status("[bold green]Sedang mencari...[/bold green]") as status:
        for platform, url in sites.items():
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
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

def track_phone():
    console.print("\n[bold cyan][+][/bold cyan] [bold]Fitur: Lacak Informasi Nomor Telepon[/bold]")
    if not phonenumbers:
        console.print("[bold red]\[!] Library 'phonenumbers' belum terinstall. Jalankan: pip install phonenumbers[/bold red]")
        return

    phone_input = Prompt.ask("[bold yellow]Masukkan nomor telepon target (Format Internasional, contoh: +62812345678)[/bold yellow]")
    
    try:
        parsed_number = phonenumbers.parse(phone_input, None)
        if not phonenumbers.is_valid_number(parsed_number):
            console.print("[bold red]\[!] Format nomor telepon tidak valid![/bold red]")
            return
            
        negara = geocoder.description_for_number(parsed_number, "id")
        provider = carrier.name_for_number(parsed_number, "id")
        
        table = Table(title=f"Informasi Nomor: {phone_input}")
        table.add_column("Kategori", style="cyan")
        table.add_column("Detail", style="green")
        
        table.add_row("Negara Asal", negara if negara else "Tidak Diketahui")
        table.add_row("Operator / Carrier", provider if provider else "Tidak Diketahui")
        table.add_row("Format Internasional", phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]\[!] Terjadi kesalahan analisis: {e}[/bold red]")

def track_ip():
    console.print("\n[bold cyan][+][/bold cyan] [bold]Fitur: Lacak Informasi IP Address[/bold]")
    ip_target = Prompt.ask("[bold yellow]Masukkan IP Address target (contoh: 8.8.8.8)[/bold yellow]")
    
    url = f"http://ip-api.com/json/{ip_target}"
    
    with console.status("[bold green]Mengambil data geolokasi IP...[/bold green]") as status:
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get("status") == "fail":
                console.print(f"[bold red]\[!] Gagal: {data.get('message')}[/bold red]")
                return
                
            table = Table(title=f"Geolokasi IP: {ip_target}")
            table.add_column("Informasi", style="cyan")
            table.add_column("Detail", style="green")
            
            table.add_row("Negara", f"{data.get('country')} ({data.get('countryCode')})")
            table.add_row("Wilayah / Provinsi", data.get('regionName'))
            table.add_row("Kota", data.get('city'))
            table.add_row("ISP", data.get('isp'))
            table.add_row("Organisasi", data.get('org'))
            table.add_row("Koordinat Lat/Lon", f"{data.get('lat')}, {data.get('lon')}")
            
            console.print(table)
        except requests.RequestException:
            console.print("[bold red]\[!] Koneksi timeout atau gagal menghubungi server IP API.[/bold red]")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = """
 ██████╗ ██╗    ██╗███████╗██╗  ██╗██╗███╗    ██╗████████╗
██╔═══██╗██║    ██║██╔════╝██║  ██║██║████╗  ██║╚══██╔══╝
██║   ██║██║ █╗ ██║███████╗███████║██║██╔██╗ ██║   ██║   
██║   ██║██║███╗██║╚════██║██╔══██║██║██║╚██╗██║   ██║   
╚██████╔╝╚███╔███╔╝███████║██║  ██║██║██║ ╚████║   ██║   
 ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   
             [bold red]OWSHINT Framework by Cerberuz69[/bold red]
        """
        console.print(Panel(banner, style="bold blue", expand=False))
        
        console.print("[1] Lacak Username (Sosmed Expanded)")
        console.print("[2] Scanning Web Subdomain")
        console.print("[3] Ekstrak Metadata Gambar")
        console.print("[4] Lacak Nomor Telepon")
        console.print("[5] Lacak IP Address")
        console.print("[6] Keluar\n")
        
        pilihan = Prompt.ask("[bold white]Pilih menu[/bold white]", choices=["1", "2", "3", "4", "5", "6"])
        
        if pilihan == "1":
            track_username()
        elif pilihan == "2":
            scan_web()
        elif pilihan == "3":
            extract_metadata()
        elif pilihan == "4":
            track_phone()
        elif pilihan == "5":
            track_ip()
        elif pilihan == "6":
            console.print("[bold red]Keluar dari program. Sampai jumpa![/bold red]")
            break
            
        input("\nTekan Enter untuk kembali ke menu utama...")

if __name__ == "__main__":
    main()
