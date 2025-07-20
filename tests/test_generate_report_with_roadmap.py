from src.mia_consciousness.output import OutputGenerator

if __name__ == "__main__":
    markdown_file = "symbolic_iterative_pipeline_memory.md"  # Memoria generata dalla pipeline iterativa
    roadmap_file = "roadmap.md"  # Roadmap generata dalla pipeline iterativa
    output_file = "symbolic_iterative_report.md"
    generator = OutputGenerator()
    report = generator.generate_report_from_markdown(markdown_file, output_file=output_file, roadmap_file=roadmap_file)
    print("Report scientifico generato in:", output_file)
    print("\n--- ANTEPRIMA REPORT ---\n")
    print(report[:1200], "...\n[troncato]") 