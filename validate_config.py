#!/usr/bin/env python3
"""
Script to validate BeatHeritage V1 config against dataclasses
"""
import yaml
import sys
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent))

try:
    from osuT5.osuT5.config import *
    print("[OK] All config classes imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing config classes: {e}")
    sys.exit(1)

def validate_config():
    print("\n[INFO] Validating BeatHeritage V1 config...")
    
    config_path = "configs/train/beatheritage_v1.yaml"
    
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        print(f"[OK] Successfully loaded {config_path}")
    except Exception as e:
        print(f"[ERROR] Error loading config: {e}")
        return False
    
    print(f"\n[INFO] Top-level config sections: {list(config_data.keys())}")
    
    # Check each section
    sections_to_check = {
        'optim': OptimizerConfig,
        'dataloader': DataloaderConfig,
        'training': TrainingConfig,
        'loss': LossConfig,
        'metrics': MetricsConfig,
    }
    
    for section_name, config_class in sections_to_check.items():
        if section_name in config_data:
            section_data = config_data[section_name]
            if isinstance(section_data, dict):
                print(f"\n[INFO] Checking {section_name} section:")
                print(f"   Config keys: {list(section_data.keys())}")
                
                # Get dataclass fields
                import inspect
                class_fields = list(inspect.signature(config_class).parameters.keys())
                print(f"   Class fields: {class_fields}")
                
                # Check for mismatches
                config_keys = set(section_data.keys())
                class_fields_set = set(class_fields)
                
                missing_in_class = config_keys - class_fields_set
                missing_in_config = class_fields_set - config_keys
                
                if missing_in_class:
                    print(f"   [ERROR] Keys in config but NOT in class: {missing_in_class}")
                else:
                    print(f"   [OK] All config keys exist in class")
                
                if missing_in_config:
                    print(f"   [WARN] Keys in class but NOT in config: {missing_in_config}")
    
    # Check data.augmentation specifically
    if 'data' in config_data and 'augmentation' in config_data['data']:
        print(f"\n[INFO] Checking data.augmentation section:")
        aug_data = config_data['data']['augmentation']
        print(f"   Config keys: {list(aug_data.keys())}")
        
        import inspect
        aug_fields = list(inspect.signature(AugmentationConfig).parameters.keys())
        print(f"   Class fields: {aug_fields}")
        
        config_keys = set(aug_data.keys())
        class_fields_set = set(aug_fields)
        
        missing_in_class = config_keys - class_fields_set
        if missing_in_class:
            print(f"   [ERROR] Keys in config but NOT in AugmentationConfig: {missing_in_class}")
        else:
            print(f"   [OK] All augmentation config keys exist in class")
    
    print("\n[OK] Config validation completed!")
    return True

if __name__ == "__main__":
    validate_config()
