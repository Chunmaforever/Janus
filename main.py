import argparse
import yaml
import sys
import os

# Adapt path for local imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from janus.faces.forward import JanusForward
from janus.faces.backward import JanusBackward

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Janus Project: AI-Powered Patent Analysis")
    parser.add_argument('--mode', choices=['forward', 'backward'], required=True, help="Analysis mode: 'forward' (Attack) or 'backward' (Defense)")
    parser.add_argument('--config', default='config/janus_config.yaml', help="Path to configuration file")
    parser.add_argument('--target_claim', type=str, help="Target claim text (overrides config if provided)")
    parser.add_argument('--competitor', type=str, default="Competitor Inc.", help="Name of competitor to analyze")
    
    args = parser.parse_args()
    
    # Load Config
    config = load_config(args.config)
    
    # Run Mode
    if args.mode == 'forward':
        print(f"🎭 Starting Janus Forward (Infringement Search) against {args.competitor}...")
        janus = JanusForward(config)
    else:
        print(f"🎭 Starting Janus Backward (Validity Defense) against {args.competitor}...")
        janus = JanusBackward(config)
        
    # Example Input (if not provided via args)
    claim_text = args.target_claim or "A system comprising a processor; a memory; and a display unit configured to show results."
    
    result = janus.run_analysis(claim_text, args.competitor)
    
    # Display Result
    print("\n--- Analysis Result ---")
    print(yaml.dump(result, sort_keys=False))

if __name__ == "__main__":
    main()
