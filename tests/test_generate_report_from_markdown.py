from src.mia_consciousness.output import OutputGenerator

if __name__ == "__main__":
    markdown_file = "symbolic_optimization_real_memory.md"  # Usa il file generato dal test avanzato
    output_file = "symbolic_optimization_report.md"
    generator = OutputGenerator()
    report = generator.generate_report_from_markdown(markdown_file, output_file=output_file)
    print("Report scientifico generato in:", output_file)
    print("\n--- ANTEPRIMA REPORT ---\n")
    print(report[:1000], "...\n[troncato]") 