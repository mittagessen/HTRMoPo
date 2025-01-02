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

## How does it work ?

Install the python library and prepare a model card for your ATR model, no
matter of segmentation, recognition, reading order, postcorrection, ....
Afterwards you need to create an account on [Zenodo](https://zenodo.org) and
create an API access token as described
[here](https://developers.zenodo.org/#creating-a-personal-access-token).

With the HTRMoPo reference implementation and the access token you can then
create model deposits on Zenodo. Deposits will be immediately accessible to the
whole world but won't be discoverable until the community inclusion request is
manually approved by one of the repository administrators.

Using a research data infrastructure like Zenodo assures long-term
accessibility of the deposited models while also enabling good scientific
practices like reproducibility and crediting contributions.

## Deposits

Each model 

## Python Library

A reference implementation to interact with the repository on Zenodo is in the
htrmopo directory, containing both a python library and command line drivers.

The library can be installed using pip:

    ~> pip install htrmopo

### CLI

The `htrmopo` command line tool is used to query the repository, download
existing models, and upload and update items to it.

#### Querying the repository

To get a listing of all models:

    ~> htrmopo list
    Retrieving model list ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ DOI                         ┃ summary                                                                                                                                   ┃ model type  ┃ keywords                                                                                                 ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ 10.5281/zenodo.7547437      │                                                                                                                                           │             │                                                                                                          │
    │ ├── 10.5281/zenodo.10800223 │ HTR model for documentary Latin, Old French and Spanish medieval manuscripts (11th-16th)                                                  │ recognition │ Handwritten text recognition; Handwritten text recognition for Medieval manuscripts; Digital Paleography │
    │ └── 10.5281/zenodo.7547438  │ HTR model for documentary Latin and Old French medieval manuscripts (12th-15th)                                                           │ recognition │ Handwritten text recognition; Handwritten text recognition for Medieval manuscripts; Digital Paleography │
    │ 10.5281/zenodo.7050269      │                                                                                                                                           │             │                                                                                                          │
    │ └── 10.5281/zenodo.7050270  │ Printed Arabic-Script Base Model Trained on the OpenITI Corpus                                                                            │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.6542743      │                                                                                                                                           │             │                                                                                                          │
    │ └── 10.5281/zenodo.6542744  │ LECTAUREP Contemporary French Model (Administration)                                                                                      │ recognition │ kraken_pytorch; HTR; transcription model; recognition model; French; Contemporary French                 │
    │ 10.5281/zenodo.13814199     │                                                                                                                                           │             │                                                                                                          │
    │ └── 10.5281/zenodo.13814200 │ Segmentation model for historical Samaritan Manuscripts for one column pages, model trained on 13 pentateuchal Samaritan manuscripts      │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.6891851      │                                                                                                                                           │             │                                                                                                          │
    │ ├── 10.5281/zenodo.7933402  │ Fraktur model trained from enhanced Austrian Newspapers dataset                                                                           │ recognition │ kraken_pytorch; Fraktur; Latin                                                                           │
    │ └── 10.5281/zenodo.6891852  │ Fraktur model trained from enhanced Austrian Newspapers dataset                                                                           │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.8193497      │                                                                                                                                           │             │                                                                                                          │
    │ └── 10.5281/zenodo.8193498  │ Transcription model for Lucien Peraire's handwriting (French, 20th century)                                                               │ recognition │ kraken_pytorch; HTR; Peraire; Manu McFrench; contemporary handwriting; French                            │
    │ 10.5281/zenodo.5468664      │                                                                                                                                           │             │                                                                                                          │
    │ └── 10.5281/zenodo.5468665  │ Medieval Hebrew manuscripts in Sephardi bookhand version 1.0                                                                              │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.10592715     │                                                                                                                                           │             │                                                                                                          │
    │ └── 10.5281/zenodo.10592716 │ CATMuS-Print (Large, 2024-01-30) - Diachronic model for French prints and other languages                                                 │ recognition │ kraken_pytorch; optical text recognition                                                                 │
    │ 10.5281/zenodo.7051645      │                                                                                                                                           │             │                                                                                                          │
    │ ├── 10.5281/zenodo.14585602 │ Printed Urdu Base Model Trained on the OpenITI Corpus                                                                                     │ recognition │ automatic-text-recognition                                                                               │
    │ ├── 10.5281/zenodo.14574660 │ Printed Urdu Base Model Trained on the OpenITI Corpus                                                                                     │ recognition │ kraken_pytorch                                                                                           │
    │ └── 10.5281/zenodo.7051646  │ Printed Urdu Base Model Trained on the OpenITI Corpus                                                                                     │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.5468285      │                                                                                                                                           │             │                                                                                                          │
    │ └── 10.5281/zenodo.5468286  │ Medieval Hebrew manuscripts version 1.0                                                                                                   │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.6657808      │                                                                                                                                           │             │                                                                                                          │
    │ ├── 10.5281/zenodo.10886224 │ Model train on openly licensed data from HTR-United from the 17th century to the 21st were used.                                          │ recognition │ kraken_pytorch                                                                                           │
    │ ├── 10.5281/zenodo.6657809  │ Model train on openly licensed data from HTR-United. All French manuscript data from the 17th century to the 21st were used (72k lines).  │ recognition │ kraken_pytorch                                                                                           │
    │ └── 10.5281/zenodo.10874058 │ Model train on openly licensed data from HTR-United. All French manuscript data from the 17th century to the 21st were used.              │ recognition │ kraken_pytorch                                                                                           │
    │ 10.5281/zenodo.7234165      │                                                                                                                                           │             │                                                                                                          │
    ....

Records are represented in a tree structure in the left-most column. The DOI at
the root of each tree is a [concept DOI](https://zenodo.org/help/versioning)
which always links to the most recent version of a model. The leaves of the
tree are particular versions of the record ordered chronologically. Either type
of DOI is acceptable as arguments for the functions below although it is
recommended to reference a concrete version in contexts where reproducibility
is desired.

To fetch the metadata for a single model (both v0 and v1 schema):

    ~> htrmopo show 10.5281/zenodo.10800223
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

Models are placed per default in reproducible locations in the application
state dir printed after the download is finished. The `-o` option allows
customization of that behavior:

    ~> htrmopo get -o manu 10.5281/zenodo.7547437
    Processing ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
    Model name: /home/mittagessen/manu

#### Publishing models

There are two modes of publishing ATR models with the `htrmopo` command. The
first creates new stand-alone deposits while the second one creates a new
version of an existing record that will all be grouped under the same concept
DOI. Updating a model deposit is usually done when a prior model is retrained
with additional training data, the metadata has been refined, or additional
evaluation has been done.

The calls for both modes are very similar, the only difference being `-d`
option giving the DOI of an existing model deposit in the repository:

    ~> htrmopo publish -i model_card.md -a ${ACCESS_TOKEN} model_dir
    Uploading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
    model PID: 10.5072/zenodo.146629
 
    ~> htrmopo publish -d 10.5072/zenodo.146502 -i model_card.md -a ${ACCESS_TOKEN} model_dir
    Uploading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
    model PID: 10.5072/zenodo.146627
