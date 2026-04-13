#!/usr/bin/env python3
"""
Simple test to verify BeatHeritage V1 config loads without errors
"""
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

def test_beatheritage_config():
    try:
        # Clear any existing Hydra instance
        GlobalHydra.instance().clear()
        
        # Initialize Hydra with config path
        initialize(config_path='configs', version_base=None)
        
        # Try to compose BeatHeritage V1 config
        cfg = compose(config_name='inference/beatheritage_v1')
        
        print("SUCCESS: BeatHeritage V1 config loaded without errors!")
        print(f"Top-level keys: {len(list(cfg.keys()))}")
        
        # Check for new sections
        new_sections = [k for k in cfg.keys() if k in ['advanced_features', 'quality_control', 'performance', 'metadata', 'postprocessor', 'integrations']]
        if new_sections:
            print(f"New sections found: {new_sections}")
        
        # Check for position_refinement
        if hasattr(cfg, 'position_refinement'):
            print(f"position_refinement: {cfg.position_refinement}")
        
        return True
        
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False
    finally:
        GlobalHydra.instance().clear()

if __name__ == "__main__":
    success = test_beatheritage_config()
    if success:
        print("\nAll BeatHeritage V1 config issues have been resolved!")
    else:
        print("\nSome config issues remain.")
