# The Others

Dette prosjektet er en liten Streamlit-applikasjon som viser fangstdata for utvalgte fiskearter. Appen visualiserer landingssteder på et kart og lar deg undersøke ferske landinger og historiske data.

## Filstruktur

- **The_Others.py** – hovedapplikasjonen som starter Streamlit og bruker funksjonene i `pages/mods/funcs.py`.
- **pages/mods/funcs.py** – modul med hjelpefunksjoner for grensesnitt, kart, grafer og tekst.
- **last_seddel.py** – eksempel på datalasting fra en pickle‑fil (ikke i repoet).
- **others_with_coordinates.csv** – datasett med salgs- og landingsinformasjon samt koordinater for mottak.
- **imgs/** – bilder brukt i appen.
- **pages/resources/** – logoer for applikasjonen.
- **tests/** – enkel pytest‑test av funksjonen `bubblecolor`.
- **requirements.txt** – nødvendige Python‑pakker.

## Komme i gang

Installer avhengighetene i et virtuelt miljø og start applikasjonen:

```bash
pip install -r requirements.txt
streamlit run The_Others.py
```

For å kjøre testene:

```bash
pytest
```

## Om dataene

`others_with_coordinates.csv` inneholder fangst- og landingsdata med koordinater for hvert mottak. `wellbore_exploration_all.csv` brukes i eksempelfunksjoner for kart, og `ListeKommunekoderKoordinater.pkl` gir koordinater til kommuner.

## Bidra

Pull requests er velkomne. Test gjerne endringene dine med `pytest` før du sender inn.
