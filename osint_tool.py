import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
from concurrent.futures import ThreadPoolExecutor, as_completed

# Rich UI Library Components
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.text import Text
    from rich import box
except ImportError:
    print("[!] Library 'rich' belum terinstal. Menginstal otomatis...")
    os.system('pip install rich')
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich import box

# Pastikan library phonenumbers dan pillow terinstall
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier
except ImportError:
    print("[!] Library 'phonenumbers' belum terinstal. Menginstal otomatis...")
    os.system('pip install phonenumbers')
    import phonenumbers
    from phonenumbers import geocoder, carrier

try:
    from PIL import Image
except ImportError:
    print("[!] Library 'Pillow' belum terinstal. Menginstal otomatis...")
    os.system('pip install Pillow')
    from PIL import Image

console = Console()
session = requests.Session() # Global session untuk optimasi performa requests

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    combined_text = Text()
    
    # Bagian "OW" (Cyan)
    combined_text.append(" ██████╗ ██╗    ██╗\n██╔═══██╗██║    ██║\n██║   ██║██║ █╗ ██║\n██║   ██║██║███╗██║\n╚██████╔╝╚███╔███╔╝\n ╚═════╝  ╚══╝╚══╝ ", style="bold cyan")
    
    # Bagian "SHI" (Merah)
    combined_text.append("███████╗██╗  ██╗██╗\n██╔════╝██║  ██║██║\n███████╗███████║██║\n╚════██║██╔══██║██║\n███████║██║  ██║██║\n╚══════╝╚═╝  ╚═╝╚═╝", style="bold red")
    
    # Bagian "N" (Cyan)
    combined_text.append("███╗    ██╗\n████╗  ██║\n██╔██╗ ██║\n██║╚██╗██║\n██║ ╚████║\n╚═╝  ╚═══╝", style="bold cyan")
    
    # Bagian "T" (Merah)
    combined_text.append("████████╗\n╚══██╔══╝\n   ██║   \n   ██║   \n   ██║   \n   ╚═╝   ", style="bold red")

    # Sub-text di bawah ASCII banner
    combined_text.append("\n\n[+] OWSHINT Framework v2.0 by Cerberuz69 [+]\n", style="bold white")
    
    console.print(Panel(combined_text, border_style="blue", box=box.DOUBLE, expand=False, justify="center"))

def track_username():
    console.print("\n[bold cyan][+][/bold cyan] [bold white]Fitur: Lacak Username[/bold white]")
    username = Prompt.ask("[bold yellow]Masukkan username target[/bold yellow]")
    
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter/X": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
    }
    
    table = Table(title=f"\nHasil Pelacakan Sosmed: {username}", box=box.ROUNDED, border_style="cyan")
    table.add_column("Platform", style="bold magenta", width=20)
    table.add_column("Status", style="bold", justify="center", width=15)
    table.add_column("URL", style="green")

    with console.status("[bold green]Sedang mencari profile...[/bold green]"):
        for platform, url in sites.items():
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = session.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    table.add_row(platform, "[green]Ditemukan[/green]", url)
                else:
                    table.add_row(platform, "[red]Tidak Ada[/red]", "-")
            except requests.RequestException:
                table.add_row(platform, "[yellow]Timeout/Error[/yellow]", "-")
                
    console.print(table)

def check_subdomain(sub, domain):
    urls = [
        f"https://{sub}.{domain}",
        f"http://{sub}.{domain}"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for target_url in urls:
        try:
            response = session.head(
                target_url,
                headers=headers,
                timeout=2.0,
                allow_redirects=True
            )
            if response.status_code < 400:
                return f"{sub}.{domain}", f"[bold green]Aktif ({response.status_code})[/bold green]"
        except:
            pass
    return None

def scan_web():
    console.print("\n[bold cyan][+][/bold cyan] [bold white]Fitur: Scanning Web Subdomain[/bold white]")
    domain = Prompt.ask("[bold yellow]Masukkan domain target (contoh: google.com)[/bold yellow]")
    
    # Common subdomains list untuk keperluan testing/recon umum
    common_subs = [
        "www", "mail", "ftp", "admin", "blog", "cpanel", "webmail", "ns1", "ns2",
        "api", "dev", "staging", "shop", "login", "secure", "test", "support"
    ]
    
    table = Table(title=f"\nHasil Scan Subdomain: {domain}", box=box.ROUNDED, border_style="cyan")
    table.add_column("Subdomain", style="bold magenta")
    table.add_column("Status", justify="center")

    results_found = False
    with console.status("[bold green]Sedang memindai subdomain (Multi-threading)...[/bold green]"):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_subdomain, sub, domain) for sub in common_subs]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    table.add_row(result[0], result[1])
                    results_found = True
                    
    if results_found:
        console.print(table)
    else:
        console.print("[bold yellow][!] Tidak ada subdomain umum aktif yang terdeteksi.[/bold yellow]")

def extract_metadata():
    console.print("\n[bold cyan][+][/bold cyan] [bold white]Fitur: Ekstrak Metadata Gambar[/bold white]")
    img_path = Prompt.ask("[bold yellow]Masukkan path/jalur file gambar (contoh: foto.jpg)[/bold yellow]")
    
    if not os.path.exists(img_path):
        console.print("[bold red][!] File tidak ditemukan![/bold red]")
        return
        
    try:
        image = Image.open(img_path)
        exif_data = image._getexif()
        
        if not exif_data:
            console.print("[bold yellow][!] Gambar tidak memiliki metadata EXIF.[/bold yellow]")
            return
            
        table = Table(title=f"\nMetadata: {os.path.basename(img_path)}", box=box.ROUNDED, border_style="cyan")
        table.add_column("Tag EXIF", style="bold magenta")
        table.add_column("Value / Nilai", style="green")
        
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            val_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            table.add_row(str(tag_name), val_str)
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red][!] Gagal mengekstrak metadata: {e}[/bold red]")

def track_phone():
    console.print("\n[bold cyan][+][/bold cyan] [bold white]Fitur: Lacak Informasi Nomor Telepon[/bold white]")
    phone_input = Prompt.ask("[bold yellow]Masukkan nomor telepon (contoh: +62812345678)[/bold yellow]")
    
    try:
        parsed_number = phonenumbers.parse(phone_input, None)
        if not phonenumbers.is_valid_number(parsed_number):
            console.print("[bold red][!] Format nomor telepon tidak valid atau tidak aktif![/bold red]")
            return
            
        negara = geocoder.description_for_number(parsed_number, "id")
        provider = carrier.name_for_number(parsed_number, "id")
        
        table = Table(title=f"\nInformasi Nomor: {phone_input}", box=box.ROUNDED, border_style="cyan")
        table.add_column("Kategori", style="bold magenta", width=25)
        table.add_column("Detail Data", style="green")
        
        table.add_row("Negara Asal", negara if negara else "Tidak Diketahui")
        table.add_row("Operator / Carrier", provider if provider else "Tidak Diketahui")
        table.add_row("Format Internasional", phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red][!] Terjadi kesalahan analisis: {e}[/bold red]")

def track_ip():
    console.print("\n[bold cyan][+][/bold cyan] [bold white]Fitur: Lacak Informasi IP Address[/bold white]")
    ip_target = Prompt.ask("[bold yellow]Masukkan IP Address target (contoh: 8.8.8.8)[/bold yellow]")
    
    url = f"http://ip-api.com/json/{ip_target}"
    
    with console.status("[bold green]Mengambil data geolokasi IP...[/bold green]"):
        try:
            response = session.get(url, timeout=5)
            data = response.json()
            
            if data.get("status") == "fail":
                console.print(f"[bold red][!] Gagal: {data.get('message')}[/bold red]")
                return
                
            table = Table(title=f"\nGeolokasi IP: {ip_target}", box=box.ROUNDED, border_style="cyan")
            table.add_column("Informasi", style="bold magenta", width=25)
            table.add_column("Detail", style="green")
            
            table.add_row("Negara", f"{data.get('country')} ({data.get('countryCode')})")
            table.add_row("Wilayah / Provinsi", str(data.get('regionName')))
            table.add_row("Kota", str(data.get('city')))
            table.add_row("ISP", str(data.get('isp')))
            table.add_row("Organisasi", str(data.get('org')))
            table.add_row("Koordinat Lat/Lon", f"{data.get('lat')}, {data.get('lon')}")
            
            console.print(table)
        except requests.RequestException:
            console.print("[bold red][!] Koneksi timeout atau gagal menghubungi server IP API.[/bold red]")

def main():
    while True:
        clear_screen()
        show_banner()
        
        menu_text = Text()
        menu_text.append("[1] ", style="bold cyan")
        menu_text.append("Lacak Username (Sosmed Expanded)\n", style="bold white")
        menu_text.append("[2] ", style="bold cyan")
        menu_text.append("Scanning Web Subdomain\n", style="bold white")
        menu_text.append("[3] ", style="bold cyan")
        menu_text.append("Ekstrak Metadata Gambar\n", style="bold white")
        menu_text.append("[4] ", style="bold cyan")
        menu_text.append("Lacak Nomor Telepon\n", style="bold white")
        menu_text.append("[5] ", style="bold cyan")
        menu_text.append("Lacak IP Address\n", style="bold white")
        menu_text.append("[6] ", style="bold red")
        menu_text.append("Keluar dari Framework", style="bold red")

        console.print(Panel(menu_text, title="[bold yellow]Daftar Modul OSINT[/bold yellow]", border_style="blue", expand=False))
        
        pilihan = Prompt.ask("\n[bold white]Pilih nomor menu[/bold white]", choices=["1", "2", "3", "4", "5", "6"], default="1")
        
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
            console.print("\n[bold red][!] Keluar dari program. Sampai jumpa kembali![/bold red]\n")
            break
            
        console.print("\n" + "─" * 50, style="dim white")
        input("\nTekan Enter untuk kembali ke menu utama...")

if __name__ == "__main__":
    main()
