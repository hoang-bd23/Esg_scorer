import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .core.pdf_extractor import PDFExtractor
from .core.scoring_engine import RuleBasedScoringEngine
from .core.keywords import KLD_KEYWORDS

app = typer.Typer(help="Hệ thống chấm điểm ESG tự động cho doanh nghiệp")
console = Console()

@app.command()
def score(
    pdf_path: str = typer.Argument(..., help="Đường dẫn đến file PDF báo cáo"),
    company_name: str = typer.Option("Unknown", "--name", "-n", help="Tên doanh nghiệp"),
    year: int = typer.Option(2024, "--year", "-y", help="Năm báo cáo"),
    use_cache: bool = typer.Option(True, "--cache/--no-cache", help="Sử dụng text cache")
):
    """
    Chấm điểm ESG cho MỘT doanh nghiệp từ file báo cáo PDF.
    """
    if not Path(pdf_path).exists():
        console.print(f"[bold red]Không tìm thấy file: {pdf_path}[/bold red]")
        raise typer.Exit(1)
        
    console.print(f"[cyan]Đang trích xuất văn bản từ {pdf_path}...[/cyan]")
    extractor = PDFExtractor()
    text = extractor.extract_text(pdf_path, use_cache=use_cache)
    console.print(f"[green]Đã trích xuất {len(text)} ký tự.[/green]")
    
    console.print("[cyan]Đang chạy Engine đánh giá ESG...[/cyan]")
    engine = RuleBasedScoringEngine(KLD_KEYWORDS)
    
    result = engine.evaluate(company_name, year, text)
    
    # Hiển thị kết quả bằng Rich Table
    table = Table(title=f"Kết quả ESG Score: {company_name} ({year})")
    table.add_column("Thành phần", justify="left", style="cyan", no_wrap=True)
    table.add_column("Strengths (Điểm cộng)", justify="center", style="green")
    table.add_column("Concerns (Điểm trừ)", justify="center", style="red")
    table.add_column("Net Score", justify="center", style="bold yellow")
    
    for comp in result.components.values():
        table.add_row(
            comp.name.value,
            str(comp.strengths.total_score),
            str(comp.concerns.total_score),
            str(comp.net_score)
        )
        
    console.print(table)
    
    stat_table = Table(title="Tổng hợp")
    stat_table.add_column("E Score", style="green")
    stat_table.add_column("S Score", style="blue")
    stat_table.add_column("G Score", style="magenta")
    stat_table.add_column("Total ESG Score", style="bold yellow")
    
    stat_table.add_row(
        str(result.e_score),
        str(result.s_score),
        str(result.g_score),
        str(result.total_esg_score)
    )
    console.print(stat_table)

from .services.batch_service import BatchScoringService
from .services.export_service import ExcelExporter

@app.command()
def batch(
    folder_path: str = typer.Argument(..., help="Thư mục chứa các file PDF"),
    output: str = typer.Option("results.xlsx", "--output", "-o", help="File Excel output"),
    workers: int = typer.Option(4, "--workers", "-n", help="Số lượng luồng song song"),
    use_cache: bool = typer.Option(True, "--cache/--no-cache", help="Sử dụng text cache")
):
    """
    Chấm điểm ESG hàng loạt cho thư mục chứa nhiều file PDF (Tối ưu cho 700-800 file).
    """
    if not Path(folder_path).is_dir():
        console.print(f"[bold red]Không tìm thấy thư mục: {folder_path}[/bold red]")
        raise typer.Exit(1)
        
    console.print(f"[cyan]Bắt đầu chấm điểm hàng loạt thư mục: {folder_path} với {workers} luồng[/cyan]")
    
    batch_service = BatchScoringService(use_cache=use_cache)
    results = batch_service.process_folder(folder_path, max_workers=workers)
    
    if not results:
        console.print("[yellow]Không có file PDF nào được xử lý thành công.[/yellow]")
        raise typer.Exit(0)
        
    console.print(f"[green]Đã xử lý xong {len(results)} doanh nghiệp. Đang xuất Excel...[/green]")
    ExcelExporter.export_batch_results(results, output)
    console.print(f"[bold green]Hoàn tất! Kết quả đã lưu tại {output}[/bold green]")

if __name__ == "__main__":
    app()
