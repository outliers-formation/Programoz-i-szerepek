# Programozói álláspiac elemzése

### Áttekintés

Ez a projekt a magyarországi informatikai álláspiacot elemzi, különös tekintettel a programozói pozíciókra. A vizsgálat célja, hogy feltárja az álláshirdetésekben szereplő, gyakran több szakmai területet is átfedő elvárásokat, megerősítve azt a feltételezést, miszerint egy-egy pozícióra nem egyetlen, hanem több IT szakértelemmel rendelkező jelöltet keresnek.

---

### Módszertan és technológiák

A munkafolyamat több lépésből állt, amelynek jelentős részét az adatgyűjtés és az adat előkészítése tette ki. A projektben tudatosan támaszkodtam **nyelvi modellekre** (mint amilyen a Google Gemini), amelyek segítettek a programozói hirdetések kategorizálásában és a technológiai elvárások kinyerésében.

1.  **Adatgyűjtés:** 17 napon keresztül gyűjtöttem a programozói álláshirdetéseket egy állásportálról.
2.  **Adat előkészítés:** Az adatok tisztítása és a szövegek egységesítése után a hirdetéseket három fő kategóriába soroltam: technológiai elvárások, személyes készségek és általános ismeretek.
3.  **Elemzés:** A fő elemzés **gráfelmélet** segítségével történt. Kétpólusú gráfot (`bipartite graph`) hoztam létre, amely összeköti az álláshirdetéseket a bennük szereplő technológiákkal. Ebből a gráfelméleti modellből kinyert adatok segítségével pedig felderítettem, hogy mely technológiák és szakmai területek fordulnak elő együtt a leggyakrabban.

---

### Főbb megállapítások

A Louvain algoritmus közösségdetektálása alapján a technológiák klaszterekbe rendeződtek, amelyek jól körülírható szakmai területeket jelölnek. Ez megerősíti a projekt kezdeti feltevését: az álláspiacon nem csupán egy-egy technológiát keresnek, hanem a technológiák jól meghatározott **kombinációit**, amelyek komplex szerepköröket alakítanak ki.

* **Közösség 2 (Microsoft/Vállalati):** `C#`, `.NET`, `SQL`, `Power Automate` és `SAP`.
* **Közösség 0 (Webfejlesztés):** `JavaScript`, `React`, `Angular` és `PHP`.
* **Közösség 1 (Felhő/Java):** `Java`, `AWS`, `Azure` és `API` fejlesztés.
* **Közösség 3 (DevOps/Rendszer):** `Python`, `DevOps`, `Linux` és `Node.js`.

A teljes elemzés a `ws_!.ipynb` jegyzetfüzetben található.
