# Machine Translation APIs

# Setup

1. Download the models from the following Google Drive Link and place the `mt-models` folder in this directory

Link: https://drive.google.com/drive/folders/1fyRlqU8fMp8RF2rxrrufv-DO9slcA5_E?usp=sharing

2. Install the conda environment using the `env_shivam_nmt.yml` file.


# Current Deployment

# API Links

English-Marathi: https://www.cfilt.iitb.ac.in/en-mr-v1/

English-Hindi: https://www.cfilt.iitb.ac.in/en-hi-v1/

Hindi-Marathi: https://www.cfilt.iitb.ac.in/hi-mr-v1/

# API Input and Output Format

## English-Marathi

### Input

```
{
    "input": [
        {
            "source": "The rivers in India play an important role in the lives of the people."
        },
        {
            "source": "Danius said, \"Right now we are doing nothing. I have called and sent emails to his closest collaborator and received very friendly replies. For now, that is certainly enough.\""
        }
    ],
    "config": {
        "language": {
            "sourceLanguage": "en",
            "targetLanguage": "mr"
            }
    }
}
```

### Output

```

{
    "config": {
        "language": {
            "sourceLanguage": "en",
            "targetLanguage": "mr"
        }
    },
    "output": [
        {
            "source": "The rivers in India play an important role in the lives of the people.",
            "target": "भारतातील नद्या लोकांच्या जीवनात महत्त्वपूर्ण भूमिका बजावतात."
        },
        {
            "source": "Danius said, \"Right now we are doing nothing. I have called and sent emails to his closest collaborator and received very friendly replies. For now, that is certainly enough.\"",
            "target": "डॅनियस म्हणाला,  सध्या आम्ही काहीच करत नाही. मी त्याच्या जवळच्या सहकाऱ्याला ईमेल कॉल केले आहेत आणि त्यांना खूप मैत्रीपूर्ण उत्तरे मिळाली आहेत. आत्ताच, हे पुरेसे आहे."
        }
    ]
}

```

## English-Hindi

### Input

```
{
    "input": [
        {
            "source": "The rivers in India play an important role in the lives of the people."
        },
        {
            "source": "Danius said, \"Right now we are doing nothing. I have called and sent emails to his closest collaborator and received very friendly replies. For now, that is certainly enough.\""
        }
    ],
    "config": {
        "language": {
            "sourceLanguage": "en",
            "targetLanguage": "mr"
            }
    }
}
```

### Output

```
{
    "config": {
        "language": {
            "sourceLanguage": "en",
            "targetLanguage": "mr"
        }
    },
    "output": [
        {
            "source": "The rivers in India play an important role in the lives of the people.",
            "target": "भारत में नदियां लोगों के जीवन में महत्वपूर्ण भूमिका निभाती हैं।"
        },
        {
            "source": "Danius said, \"Right now we are doing nothing. I have called and sent emails to his closest collaborator and received very friendly replies. For now, that is certainly enough.\"",
            "target": "डेनियस ने कहा, अभी हम कुछ नहीं कर रहे हैं। मैंने उनके करीबी सहयोगी को फोन किया और ईमेल भेजे और बहुत दोस्ताना जवाब मिले। अभी के लिए यह काफी है।"
        }
    ]
}
```

## Hindi-Marathi

### Input
```
{
    "input": [
        {
            "source": "भारत में नदियां लोगों के जीवन में महत्वपूर्ण भूमिका निभाती हैं ।"
        },
        {
            "source": "पेड़ बहुत ऊंचा है ।"
        }
    ],
    "config": {
        "language": {
            "sourceLanguage": "hi",
            "targetLanguage": "mr"
            },
        "model": "No filtering"
    }
}
```

### Output

```
{
    "config": {
        "language": {
            "sourceLanguage": "hi",
            "targetLanguage": "mr"
        },
        "model": "No filtering"
    },
    "output": [
        {
            "source": "भारत में नदियां लोगों के जीवन में महत्वपूर्ण भूमिका निभाती हैं ।",
            "target": "भारतात नद्या म्हणजे लोकांच्या जीवनात महत्त्वाची भूमिका बजावतात."
        },
        {
            "source": "पेड़ बहुत ऊंचा है ।",
            "target": "वृक्ष खूप उंच आहे."
        }
    ]
}
```