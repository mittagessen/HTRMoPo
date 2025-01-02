---
# Example metadata to be added to a model card.
id: {id_0}  # Example: https://doi.org/10.5281/zenodo.14399779
summary: {summary_0}  # A one-line summary of the model
authors:
  - name: {name_0}
    affiliation: {affiliation_0}  # Affiliation is optional.
  - name: {name_1}
license: {license_0}  # Example: Apache-2.0
license_name: {license_name_0}  # When license == 'other-*' give your license name here
license_link: {license_link_0}  # When license == 'other-*' give the location of the full license text here.
software_name: {software_name_0}  # Example: kraken
software_hints:
- {software_hint_0}  #  List of free-text values that allow the software to determine compatibility, e.g. minimum version numbers or segmentation types.
language:  # List of ISO 693-3 language codes
- {lang_0}  # Example: ang
- {lang_1}  # Example: syr
script:  # List of ISO 15924 script codes
- {script_0}  # Example: Arab
- {script_1}  # Example: Syrc
tags:  # free-text field tags
- {tag_0}  # Example: syriac
- {tag_1}  # Example: liturgical
model_type:  # List of one or more functions this model performs. 
- {model_type_0}  # Example: segmentation
- {model_type_1}  # Example: reading order
metrics:  # Undefined dictionary mapping validation/test metrics to values
  {metric_0}: {metric_val_0}  # Example: cer: 0.01
  {metric_1}: {metric_val_1}  # Example: wer: 0.05
datasets:
- {dataset_0}  # Example: https://github.com/OpenITI/arabic_print_data.git
base_model:  # base model this model has been fine-tuned on. Might be more than one. Should be PIDs/URLs
- {base_model_0}  # Example: https://github.com/mittagessen/bytellama
citation: {citation_0}  # Example: https://inria.hal.science/hal-04591043
---
# {model_name}

<!-- Here should be a summary of the model and what it does. -->

## Architecture

<!-- An explanation of the model architecture if it is novel or not part of an established ATR software --!>

## Uses

<!-- A description of what this model can be used for, e.g. if it is a generalized recognition model or for a particular document/hand --!>

## Transcription guidelines, Normalization, and Transformations 

<!-- An optional section describing the rules employed during transcription and any algorithmic transformations of the text --!>

## Bias, Risks, and Limitations

<!--A short discussion about biases and limitations of the model. --!>

## How to Get Started with the Model

<!-- An optional quickstart on how the model can be used with the software it's been designed for. --!>

## Training Details

### Training Data

<!-- Details about the training data --!>

### Training Procedure and Hyperparameters

<!-- A short summary of the training hyperparameters --!>

## Evaluation

### Testing Data, Factors & Metrics

<!-- Details about the testing data and metrics computed on them. --!>

#### Testing Data

#### Metrics

## Citation

<!-- An optional citation if the model is associated with any publication --!>


