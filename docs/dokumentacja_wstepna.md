# Dokumentacja wstępna

### Jędrzej Grabski, Maksym Bieńkowski

---

# Algorytm roju cząstek z modyfikacjami dotyczącymi współczynnika bezwładności.

## Analiza problemu

Ideą Algorytmu Roju Cząstek (PSO - _Particle Swarm Optimalization_), jest symulowanie populacji ("roju"), która rozwija się na podstawie wiedzy pojedynczych osobników ("cząstek") oraz pewnej wiedzy dzielonej. Każda z cząstek posiada swoją pozycję w przestrzeni rozwiązań, prędkość oraz kierunek w jakim się porusza. Ponadto zapamiętywane jest najlepsze rozwiązanie znalezione do tej pory przez każdą z cząstek (optimum lokalne), a także najlepsze rozwiązanie z całego roju (optimum globalne).

Ruch każdej cząstki, jest zależny od odległości od poznanych optimówm oraz kilku paramterów.

Współczynnik bezwładności jest parametrem, który reguluje wpływ poprzedniego ruchu, na bieżący – jeśli poprzedni krok był długi, wpłynie to na zwiększenie długości kroku następnego.

Widzimy, że dzięki zastosowaniu takiego rozwiązania, cząstki roju mogą szybciej pokonywać długie dystanse, gdzie należy wykonać serię długich kroków. Może on jednak wprowadzać też zjawisko "przestrzelenia" w późniejszych etapach algorytmu, gdy zależy nam na zbieganiu do optimum.

## Propozycja rozwiązania

Problem ten spróbjemy zniwelować poprzez wprowadzenie dynamicznej zmiany współczynnika bezwładności, zależnego od numeru iteracji algorytmu. Współczynnik będzie stopniowo zmniejszał się, w miarę pracy algorytmu. Dzięki temu, będziemy mogli korzystać ze zwiększonej ekslporacji przestrzeni na początku algorytmu, a następnie z bardziej precyzyjnej zbieżności wokół optimów pod koniec pracy.

## Przyjęte założenia

- Przestrzeń rozwiązań: Zakładamy, że przestrzeń rozwiązań jest ciągła, ograniczona i wielowymiarowa, a wartości funkcji celu są dobrze zdefiniowane w całej przestrzeni.

- Funkcja celu: Funkcja celu jest różnorodna, tj. może być jedno- lub wielomodalna, aby przetestować algorytm w różnych warunkach.

- Początkowa populacja: Pozycje cząstek w roju są inicjalizowane losowo z rozkładem jednostajnym w granicach przestrzeni rozwiązań. Początkowe prędkości cząstek będą losowane z rozkładem jednostajnym na bazie ograniczeń przestrzeni przeszukiwań.

- Parametry algorytmu:
  - Liczba cząstek w roju oraz liczba iteracji są ustalane na początku i pozostają stałe w trakcie pracy algorytmu.
  - Parametry wpływające na ruch cząstek (np. współczynniki wpływu optimum lokalnego i globalnego) są dobrane na podstawie literatury.
  - Dynamiczny współczynnik bezwładności: Zmiana współczynnika bezwładności następuje zgodnie z wzorem $w'=w*u^{-k}$, gdzie $w \in [0,1]$ to bazowy współczynnik bezwładności, $u \in [1.0001, 1.005]$ to siła wytracania wartości współczynnika, a $k$ to numer iteracji.

## Sposób badania jakości rozwiązania

- Porównanie algorytmów:
  - Algorytm PSO z dynamicznym współczynnikiem bezwładności zostanie porównany z klasyczną wersją tego algorytmu (ze stałym współczynnikiem).
  - Testy zostaną przeprowadzone na publicznych benchmarkach funkcji optymalizacyjnych.
- Kryteria oceny:
  - Jakość rozwiązania: Różnica wartości funkcji celu algorytmu od optimum globalnego dla danego problemu optymalizacji po określonej liczbie iteracji.
  - Szybkość zbieżności: Analiza tempa zbilżania się do optimum, mierzona przez ilość iteracji po której zostało osiągnięte otoczenie $\epsilon$ optimum globalnego.
- Proces badawczy:
  - Testy zostaną przeprowadzone na przestrzeniach o różnych wymiarach, aby ocenić wpływ wymiarowości na działanie algorytmu.
- Wizualizacje
  – Przedstawienie trajektorii cząstek na łatwych do zwizualizowania przestrzeniach zostaną graficznie przedstawione na dwu-wymiarowym wykresie.
  – Wyniki funkcji celu w zależności od iteracji zostaną przedstawione w trudniejszych do zwizualizowania przestrzeniach.

## Środowisko

- Projekt będzie realizowany w środowisku Python.
- Narzędziem do zarządzania środowiskiem wirtualnym będzie PDM.
- Do wizualizacji przebiegów działań algorytmów zostanie użyta bilbioteka _matplotlib_
