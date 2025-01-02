# HTRMoPo

HTRMoPo is a schema and an implementation for an automatic text recognition
model repository hosted on the [Zenodo](https://zenodo.org) research data
infrastructure. It is designed to enable discoverability of models across a
wide number of software and ATR-related tasks and aid in model selection.

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
htrmopo directory, containing both a python library and command line drivers.

### CLI

The `htrmopo` command line tool is used to query the repository, download
existing models, and upload and update items to it.

To get a listing of all models:

    ~> htrmopo list
    Retrieving model list ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ DOI                         ┃ summary                                                                                                                                                                                                      ┃ model type  ┃ keywords                                                                                                 ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ 10.5281/zenodo.5617782      │                                                                                                                                                                                                              │             │                                                                                                          │
    │ ├── 10.5281/zenodo.6669508  │ Cremma-Medieval Old French Model (Litterature)                                                                                                                                                               │ recognition │ kraken_pytorch                                                                                           │
    │ └── 10.5281/zenodo.5617783  │ Cremma-Medieval Old French Model (Litterature)                                                                                                                                                               │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.10066218     │                                                                                                                                                                                                              │             │                                                                                                          │
    │ ├── 10.5281/zenodo.12743230 │ CATMuS Medieval 1.5.0                                                                                                                                                                                        │ recognition │ kraken_pytorch; handwritten text recognition; htr; middle ages                                           │
    │ └── 10.5281/zenodo.10066219 │ CATMuS Medieval                                                                                                                                                                                              │ recognition │ kraken_pytorch; handwritten text recognition; htr; middle ages                                           │
    │ 10.5281/zenodo.7051644      │ Printed Persian Base Model Trained on the OpenITI Corpus                                                                                                                                                     │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.6891851      │                                                                                                                                                                                                              │             │                                                                                                          │
    │ ├── 10.5281/zenodo.7933402  │ Fraktur model trained from enhanced Austrian Newspapers dataset                                                                                                                                              │ recognition │ kraken_pytorch; Fraktur; Latin                                                                           │
    │ └── 10.5281/zenodo.6891852  │ Fraktur model trained from enhanced Austrian Newspapers dataset                                                                                                                                              │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.13736584     │ Model trained on 11th century manuscripts to produce expanded transcription (Latin).                                                                                                                         │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.10602307     │ CATMuS-Print (Small, 2024-01-30) - Diachronic model for French prints and other languages                                                                                                                    │ recognition │                                                                                                          │
    ....


To fetch the metadata for a single model (both v0 and v1 schema):

    ~> htrmopo show 10.5281/zenodo.7547437
                                                 HTR model for documentary Latin, Old French and Spanish medieval manuscripts (11th-16th)                                              
    ┌──────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ DOI              │ 10.5281/zenodo.10800223                                                                                                                                      │
    │ concept DOI      │ 10.5281/zenodo.7547437                                                                                                                                       │
    │ publication date │ 2024-03-14T01:47:02+00:00                                                                                                                                    │
    │ model type       │ recognition                                                                                                                                                  │
    │ script           │ Latin                                                                                                                                                        │
    │ alphabet         │ ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ a b c d e f g h i j k l m n o p  │
    │                  │ q r s t u v w x y z { | } ~ ¡ £ § ª « ¬ ° ¶ º » ½ ¾ À Ä Ç È É Ë Ï Û Ü à á â ä æ ç è é ê ë ì í î ï ñ ò ó ô ö ù ú û ü ÿ ā ă ē ĕ ę ī ō ŏ œ ŭ ƒ ȩ ˀ ο а е о с ᗅ  │
    │                  │ – — ‘ ’ ” „ † … ⁖ ₎ 〈 〉 ✳ ꝫ                                                                                                                                │
    │                  │ 0x9, SPACE, 0x92, 0x97, NO-BREAK SPACE, COMBINING MACRON, COMBINING LATIN SMALL LETTER A, COMBINING LATIN SMALL LETTER E, COMBINING LATIN SMALL LETTER O,    │
    │                  │ COMBINING LATIN SMALL LETTER U, COMBINING LATIN SMALL LETTER C, WORD JOINER, 0xf2f7                                                                          │
    │ keywords         │ Handwritten text recognition                                                                                                                                 │
    │                  │ Handwritten text recognition for Medieval manuscripts                                                                                                        │
    │                  │ Digital Paleography                                                                                                                                          │
    │ metrics          │ cer: 7.82                                                                                                                                                    │
    │ license          │ MIT                                                                                                                                                          │
    │ creators         │ Torres Aguilar, Sergio (https://orcid.org/0000-0002-1801-3147) (University of Luxembourg)                                                                    │
    │                  │ Jolivet, Vincent (École nationale des chartes)                                                                                                               │
    │                  │ Sergio Torres Aguilar (University of Luxembourg)                                                                                                             │
    │ description      │ The model was trained on diplomatic transcriptions of documentary manuscripts from the Late-medieval period (12-15th) and early modernity (16th). The        │
    │                  │ training and evaluation sets entail 215k lines and 2.4M of tokens using open source corpora.                                                                 │
    │                  │                                                                                                                                                              │
    └──────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Downloading a single model:

    ~> htrmopo get 10.5281/zenodo.7547437 
    Processing ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
    Model name: /home/mittagessen/.local/share/htrmopo/0ac39ba5-8f85-5ea1-913a-f84a13ca756f

Models are placed per default in reproducible locations in the application state dir printed after the download is finished. The `-o` option allows customization of that behavior:

    ~> htrmopo get -o manu 10.5281/zenodo.7547437
    Processing ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
    Model name: /home/mittagessen/manu
