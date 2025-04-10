# RAG Workshop: Leren werken met PDF-documenten en Large Language Models

Deze repository bevat een workshop notebook waarin je leert hoe je Retrieval Augmented Generation (RAG) kunt toepassen op PDF-documenten zoals regioplannen. Je leert hoe je een vectordatabase kunt maken met ChromaDB en hoe je deze kunt gebruiken voor het beantwoorden van vragen met behulp van Large Language Models.

## Workshop Notebook

Het workshop notebook bevat stapsgewijze instructies om:
1. PDF-documenten in te laden en te verwerken
2. Een vectordatabase te creëren met ChromaDB
3. Queries uit te voeren op de vectordatabase
4. RAG-technieken toe te passen om vragen te beantwoorden

## Google Colab Instructies

Het wordt aanbevolen om het workshop notebook via Google Colab te gebruiken voor de beste ervaring:

1. Ga naar [Google Colab](https://colab.research.google.com/)
2. Klik op 'Bestand' > 'Openen'
3. Selecteer het tabblad 'GitHub'
4. Plak de URL van deze repository
5. Selecteer het workshop notebook om te openen

Je hebt een Google-account nodig om Colab te gebruiken. Het notebook wordt uitgevoerd in de cloud, dus je hoeft niets lokaal te installeren.

## OpenAI API-sleutel

Voor het uitvoeren van het notebook heb je een OpenAI API-sleutel nodig. Volg de instructies in het notebook voor het instellen van je API-sleutel.

---

# Achtergrond: PDF naar Chroma Database Builder

De onderstaande informatie beschrijft het script dat wordt gebruikt om de vectordatabase te bouwen. Dit is achtergrond informatie en niet nodig voor het volgen van de workshop.

Dit script verwerkt PDF-bestanden (zoals regioplannen) en maakt een vectordatabase met behulp van ChromaDB en OpenAI embeddings. De vectordatabase kan worden gebruikt voor Retrieval Augmented Generation (RAG) toepassingen.

## Vereisten

- Python 3.8+
- OpenAI API-sleutel (voor het genereren van embeddings)
- PDF-bestanden die je wilt verwerken

## Installatie

1. Clone deze repository of download de bestanden.

2. Installeer de benodigde afhankelijkheden:
   ```bash
   pip install -r requirements.txt
   ```

3. Stel je OpenAI API-sleutel in (optioneel, je wordt hierom gevraagd als deze niet is ingesteld):
   ```bash
   export OPENAI_API_KEY=jouw_api_sleutel_hier
   ```

## Gebruik

Basisgebruik:
```bash
python build_chroma_db.py /pad/naar/pdf/map
```

Dit verwerkt alle PDF-bestanden in de opgegeven map en maakt een Chroma-database aan op de standaardlocatie (`chroma_db_regioplannen`).

### Geavanceerde opties

```bash
python build_chroma_db.py /pad/naar/pdf/map --output aangepaste_db_map --chunk-size 1500 --chunk-overlap 150 --embedding-model text-embedding-3-large
```

Commandoregelopties:
- `pdf_directory`: Map met te verwerken PDF-bestanden (verplicht)
- `--output`, `-o`: Map voor het opslaan van de ChromaDB-database (standaard: chroma_db_regioplannen)
- `--chunk-size`: Grootte van tekstfragmenten (standaard: 1000)
- `--chunk-overlap`: Overlap tussen fragmenten (standaard: 200)
- `--embedding-model`: Te gebruiken OpenAI embedding model (standaard: text-embedding-3-small)

## Hoe het werkt

1. Het script scant de opgegeven map op PDF-bestanden.
2. Elke PDF wordt ingeladen en omgezet naar tekst met PyPDFLoader.
3. De tekst wordt opgesplitst in behapbare fragmenten met RecursiveCharacterTextSplitter.
4. OpenAI's embedding model zet deze tekstfragmenten om in vectorembeddings.
5. De fragmenten en hun embeddings worden opgeslagen in een ChromaDB vectordatabase.

## Opmerkingen

- Het verwerken van een groot aantal PDF's kan tijd kosten en OpenAI API-credits verbruiken.
- Zorg ervoor dat je voldoende schijfruimte hebt voor de vectordatabase (afhankelijk van het aantal en de grootte van de PDF's).
- De kwaliteit van je RAG-toepassing is afhankelijk van de kwaliteit van de PDF's en de gebruikte fragmentatiestrategie. 

## TO DOs

- [ ] Voeg metadata toe aan de vectordatabase (ik gebruik nu de `all_pdfs` folder zonder ordening).