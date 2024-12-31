# HTRMoPo

HTRMoPo is a intended to provide a schema for automatic text recognition model
repositories that enables discoverability and aids in model selection.

There are two versions of the schema: `v0` and `v1`. `v0` is the legacy kraken
model schema for the Zenodo repository that is fairly limited, in particular by
not supporting non-recognition models and providing limited ways of
incorporating model cards. `v1` is intended for all kinds of machine learning
models involved in ATR independent of software.

## Schema

### v0

v0 is conserved for historical interest mostly. Records in v0 format consist of
a JSON metadata file and at most a single model file that is referenced in it.

### v1

Repository records following the v1 schema consist of a Markdown model card
with a YAML metadata front matter and an arbitrary number of files in the
record. There is an [example for the model card](schema/v1/model_card.md) that
is inspired by the huggingface example template but in principle model cards
are free form. The front matter can be validated against a JSON schema found
[here](schema/v1/metadata.schema.json).

## Python Library

A reference implementation to interact with the repository on Zenodo is in the
htrmopo directory.
