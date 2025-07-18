#!/usr/bin/env python3
"""
M.I.A. Consciousness Research System - PC Optimized Version
Main entry point for rigorous consciousness research

This system implements evidence-based consciousness research using
multiple Ollama models with scientific rigor and critical analysis.
"""

import os
import sys
import json
import time
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mia_consciousness import (
    ConsciousnessResearcher,
    ResearchProtocol,
    ResearchConfig,
    OutputGenerator
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mia_research.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from JSON file"""
    
    default_config = {
        "models": {
            "mathematical": "llama3.2:3b",
            "physical": "mistral:7b", 
            "neural": "llama3.2:3b",
            "empirical": "llama3.2:1b",
            "critical": "mistral:7b",
            "synthesis": "llama3.2:3b"
        },
        "research_parameters": {
            "confidence_threshold": 0.7,
            "max_iterations": 5,
            "timeout_minutes": 10,
            "parallel_processing": False,
            "memory_optimization": True
        },
        "output_settings": {
            "generate_pdf": True,
            "include_raw_data": True,
            "scientific_format": True,
            "clinical_applications": True
        }
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults
                for key, value in user_config.items():
                    if isinstance(value, dict) and key in default_config:
                        default_config[key].update(value)
                    else:
                        default_config[key] = value
        except Exception as e:
            logger.warning(f"Error loading config: {e}. Using defaults.")
    
    return default_config

def verify_ollama_setup(models: Dict[str, str]) -> bool:
    """Verify Ollama is installed and models are available"""
    
    try:
        import subprocess
        
        # Check if ollama is installed
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            logger.error("Ollama not found. Please install Ollama first.")
            return False
            
        logger.info(f"Ollama version: {result.stdout.strip()}")
        
        # Check available models
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=30)
        available_models = result.stdout
        
        missing_models = []
        for role, model in models.items():
            if model not in available_models:
                missing_models.append(model)
        
        if missing_models:
            logger.warning(f"Missing models: {missing_models}")
            logger.info("Run: ollama pull <model_name> for each missing model")
            return False
            
        logger.info("All required models are available")
        return True
        
    except Exception as e:
        logger.error(f"Error verifying Ollama setup: {e}")
        return False

def create_output_directory() -> Path:
    """Create timestamped output directory"""
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"output/research_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Output directory: {output_dir}")
    return output_dir

def run_consciousness_research(config: Dict[str, Any], 
                             protocol_name: str = "comprehensive",
                             output_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Run comprehensive consciousness research"""
    
    logger.info("🧠 Starting M.I.A. Consciousness Research System")
    logger.info("=" * 60)
    
    # Create output directory
    if output_dir is None:
        output_dir = create_output_directory()
    
    # Initialize research system
    logger.info("🔧 Initializing research system...")
    
    research_config = ResearchConfig(
        models=config["models"],
        parameters=config["research_parameters"],
        output_settings=config["output_settings"]
    )
    
    researcher = ConsciousnessResearcher(research_config)
    
    # Define research protocols
    protocols = {
        "comprehensive": ResearchProtocol(
            name="Comprehensive Consciousness Analysis",
            objective="Conduct rigorous multi-domain consciousness research",
            methodology=[
                "Mathematical framework development",
                "Physical mechanism analysis", 
                "Neural correlate validation",
                "Empirical protocol design",
                "Critical analysis and review",
                "Synthesis and integration"
            ],
            success_criteria=[
                "Mathematical consistency achieved",
                "Physical plausibility demonstrated",
                "Neural evidence validated",
                "Empirical testability confirmed",
                "Critical issues addressed",
                "Unified framework developed"
            ],
            domains=["mathematical", "physical", "neural", "empirical", "critical", "synthesis"]
        ),
        "neural_validation": ResearchProtocol(
            name="Neural Correlates Validation",
            objective="Validate neural correlates of consciousness",
            methodology=[
                "NCCs literature review",
                "Meta-analysis of effect sizes", 
                "Replication assessment",
                "Clinical validation protocols"
            ],
            success_criteria=[
                "Effect size > 0.5",
                "Replication rate > 70%",
                "Clinical sensitivity > 80%"
            ],
            domains=["neural", "empirical", "critical"]
        ),
        "mathematical_framework": ResearchProtocol(
            name="Mathematical Framework Development", 
            objective="Develop mathematical framework for consciousness quantification",
            methodology=[
                "Information theory application",
                "Network analysis metrics",
                "Statistical validation",
                "Computational implementation"
            ],
            success_criteria=[
                "Mathematical consistency",
                "Empirical correlation > 0.6", 
                "Computational tractability"
            ],
            domains=["mathematical", "physical", "critical"]
        )
    }
    
    # Select protocol
    if protocol_name not in protocols:
        logger.warning(f"Unknown protocol: {protocol_name}. Using comprehensive.")
        protocol_name = "comprehensive"
    
    protocol = protocols[protocol_name]
    logger.info(f"🔬 Executing protocol: {protocol.name}")
    
    # Execute research
    try:
        results = researcher.execute_protocol(protocol)
        
        logger.info("✅ Research protocol completed!")
        logger.info(f"📊 Summary:")
        logger.info(f"   • Domains analyzed: {len(results.get('domain_results', {}))}")
        logger.info(f"   • Average confidence: {results.get('summary', {}).get('average_confidence', 0):.2f}")
        logger.info(f"   • Overall grade: {results.get('assessment', {}).get('overall_grade', 'Unknown')}")
        
        # Generate outputs
        logger.info("📄 Generating research outputs...")
        
        output_generator = OutputGenerator(config["output_settings"])
        output_files = output_generator.generate_all_outputs(results, output_dir)
        
        logger.info("📁 Generated files:")
        for file_type, file_path in output_files.items():
            logger.info(f"   • {file_type}: {file_path}")
        
        # Save configuration used
        config_file = output_dir / "research_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return {
            "results": results,
            "output_files": output_files,
            "output_directory": str(output_dir),
            "config_used": config
        }
        
    except Exception as e:
        logger.error(f"❌ Error in research execution: {e}")
        raise

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description="M.I.A. Consciousness Research System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Run comprehensive research
  python main.py --protocol neural_validation      # Run neural validation only
  python main.py --config custom_config.json       # Use custom configuration
  python main.py --verify-setup                    # Verify Ollama setup only
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        default="config.json",
        help="Configuration file path (default: config.json)"
    )
    
    parser.add_argument(
        "--protocol", "-p", 
        default="comprehensive",
        choices=["comprehensive", "neural_validation", "mathematical_framework"],
        help="Research protocol to execute (default: comprehensive)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory (default: auto-generated)"
    )
    
    parser.add_argument(
        "--verify-setup", "-v",
        action="store_true",
        help="Verify Ollama setup and exit"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true", 
        help="Reduce logging output"
    )
    
    args = parser.parse_args()
    
    # Adjust logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    # Load configuration
    config = load_config(args.config)
    
    # Verify setup
    if not verify_ollama_setup(config["models"]):
        if args.verify_setup:
            sys.exit(1)
        else:
            logger.error("Ollama setup verification failed. Use --verify-setup for details.")
            sys.exit(1)
    
    if args.verify_setup:
        logger.info("✅ Ollama setup verified successfully!")
        sys.exit(0)
    
    # Prepare output directory
    output_dir = None
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Run research
        final_results = run_consciousness_research(
            config=config,
            protocol_name=args.protocol,
            output_dir=output_dir
        )
        
        print("\n" + "="*60)
        print("🎉 M.I.A. Consciousness Research Completed Successfully!")
        print("="*60)
        print(f"📁 Output directory: {final_results['output_directory']}")
        print(f"📊 Research grade: {final_results['results'].get('assessment', {}).get('overall_grade', 'Unknown')}")
        print(f"🎯 Confidence: {final_results['results'].get('summary', {}).get('average_confidence', 0):.2f}")
        print("\n📄 Generated files:")
        for file_type, file_path in final_results['output_files'].items():
            print(f"   • {file_type}: {file_path}")
        print("\n✅ Research complete! Check the output directory for detailed results.")
        
    except KeyboardInterrupt:
        logger.info("Research interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

