#!/usr/bin/env python3
"""
Test script to validate all config loading after fixes
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_config_loading():
    """Test loading various configs to ensure no ConfigKeyError"""
    print("Testing BeatHeritage Config Loading...")
    print("=" * 50)
    
    configs_to_test = [
        ("configs/inference/beatheritage_v1.yaml", "BeatHeritage V1 Inference"),
        ("configs/inference/default.yaml", "Default Inference"),
        ("configs/train/beatheritage_v1.yaml", "BeatHeritage V1 Training"),
        ("configs/train/default.yaml", "Default Training"),
        ("configs/diffusion/v1.yaml", "Diffusion V1"),
    ]
    
    success_count = 0
    total_count = len(configs_to_test)
    
    for config_path, config_name in configs_to_test:
        print(f"\n[TEST] {config_name}")
        print(f"       Path: {config_path}")
        
        if not os.path.exists(config_path):
            print(f"       Status: SKIPPED (file not found)")
            continue
            
        try:
            # Test Hydra config composition
            from hydra import compose, initialize_config_store
            from hydra.core.global_hydra import GlobalHydra
            from config import InferenceConfig, FidConfig, MaiModConfig
            from osuT5.osuT5.config import TrainConfig
            from osu_diffusion.config import DiffusionTrainConfig
            
            # Clear any existing Hydra instance
            GlobalHydra.instance().clear()
            
            # Determine config type and test accordingly
            if "inference" in config_path:
                # Test inference config
                with initialize_config_store(config_path="../configs", version_base=None):
                    config_name_only = Path(config_path).stem
                    cfg = compose(config_name=f"inference/{config_name_only}")
                    print(f"       Status: SUCCESS (loaded inference config)")
                    print(f"       Keys: {len(cfg.keys())} top-level keys")
                    
            elif "train" in config_path:
                # Test training config
                with initialize_config_store(config_path="../configs", version_base=None):
                    config_name_only = Path(config_path).stem
                    cfg = compose(config_name=f"train/{config_name_only}")
                    print(f"       Status: SUCCESS (loaded training config)")
                    print(f"       Keys: {len(cfg.keys())} top-level keys")
                    
            elif "diffusion" in config_path:
                # Test diffusion config
                with initialize_config_store(config_path="../configs", version_base=None):
                    config_name_only = Path(config_path).stem
                    cfg = compose(config_name=f"diffusion/{config_name_only}")
                    print(f"       Status: SUCCESS (loaded diffusion config)")
                    print(f"       Keys: {len(cfg.keys())} top-level keys")
            
            success_count += 1
            
        except Exception as e:
            print(f"       Status: FAILED")
            print(f"       Error: {str(e)}")
            if "ConfigKeyError" in str(e):
                # Extract the problematic key
                error_lines = str(e).split('\n')
                for line in error_lines:
                    if "Key" in line and "not in" in line:
                        print(f"       Issue: {line.strip()}")
                        break
    
    print(f"\n" + "=" * 50)
    print(f"SUMMARY: {success_count}/{total_count} configs loaded successfully")
    
    if success_count == total_count:
        print("All configs are working! No more ConfigKeyError issues.")
        return True
    else:
        print("Some configs still have issues. See details above.")
        return False

if __name__ == "__main__":
    success = test_config_loading()
    sys.exit(0 if success else 1)
