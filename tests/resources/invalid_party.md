---
# Example metadata to be added to a model card.
id: foo  # Example: https://doi.org/10.5281/zenodo.14399779
summary: Pretrained multilingual Party model 
authors:
  - name: Benjamin Kiessling
license: Apache-2.0
software_name: party
software_hints:
- segmentation=both
language:
- ang
tags:
- multimodal
model_type:
- recognition
metrics:
  cer: 0.00
base_model:
- https://github.com/mittagessen/bytellama
---
# Llama Party
