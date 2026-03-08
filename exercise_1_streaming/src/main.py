import os
from processor import CatalogProcessor
from reporter import QualityReporter

def main():
    #Definition of relative routes
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(base_path, "data", "input.csv")
    output_csv = os.path.join(base_path, "data", "episodes_clean.csv")
    report_md = os.path.join(base_path, "report.md")

    #The input file is checked before starting
    if not os.path.exists(input_csv):
        print(f"Error: No se encontró el archivo de entrada en {input_csv}")
        return

    #The components are initialized
    reporter = QualityReporter()
    processor = CatalogProcessor(input_csv, output_csv, reporter)

    #The processor is running
    print(f"--- Procesando catálogo desde: {input_csv} ---")
    processor.process()

    #The report is generated
    print(f"--- Generando reporte en: {report_md} ---")
    reporter.generate_report(report_md)

    print(f"\n¡Proceso completado!")

    print(f"Resultados en: {output_csv}")

if __name__ == "__main__":
    main()