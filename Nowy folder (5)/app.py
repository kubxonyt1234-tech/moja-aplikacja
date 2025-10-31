# app.py
from flask import Flask, render_template_string, request, redirect, url_for, session
import math
import random
import re

app = Flask(__name__)
app.secret_key = "sekretnyklucz_do_zmiany"  # zmień na losowy przed wystawieniem publicznie

# ------------------ KONFIG ------------------
ADMIN_PASSWORD = "1234"
PREMIUM_COST = 10  # koszt w monetach za premium
PREMIUM_EXTRA_COUNT = 50  # liczba dodatkowych pytań w premium

# ------------------ BAZY PYTAŃ ------------------
# basic_qa ~100 wpisów (możesz rozszerzyć)
basic_qa = {
    "jak masz na imię": "Jestem Scended AI, lokalny asystent.",
    "ile masz lat": "Nie mam wieku, jestem programem komputerowym.",
    "co potrafisz": "Odpowiadam na pytania, liczę i gram w papier-kamień-nożyce.",
    "jaka jest stolica polski": "Warszawa",
    "jaka jest stolica francji": "Paryż",
    "kto wynalazł telefon": "Alexander Graham Bell.",
    "kto napisał hamleta": "William Shakespeare.",
    "co to jest ai": "Sztuczna inteligencja to system komputerowy uczący się z danych.",
    "co to jest internet": "Globalna sieć komputerowa.",
    "co to jest python": "Popularny język programowania.",
    "co to jest dna": "Materiał genetyczny wszystkich organizmów żywych.",
    "jakie są kolory tęczy": "Czerwony, Pomarańczowy, Żółty, Zielony, Niebieski, Indygo, Fioletowy",
    "który jest najbliższy planetą słońca": "Merkury",
    "jak nazywa się największy ocean": "Ocean Spokojny",
    "co to jest grawitacja": "Siła przyciągania między ciałami posiadającymi masę.",
    "co to jest magnetyzm": "Zjawisko związane z oddziaływaniem pól magnetycznych.",
    "jakie są stany skupienia wody": "Lód, Woda, Para",
    "co to jest fotosynteza": "Proces, w którym rośliny zamieniają światło w energię.",
    "który jest najwyższy szczyt świata": "Mount Everest.",
    "jaki jest najbliższy nam księżyc": "Księżyc Ziemi.",
    "co to jest planeta": "Ciało niebieskie krążące wokół gwiazdy.",
    "co to jest gwiazda": "Ogromna kula gazowa wytwarzająca energię przez reakcje jądrowe.",
    "co to jest czarna dziura": "Obszar przestrzeni o tak silnej grawitacji, że nic nie może uciec.",
    "co to jest mgławica": "Obłok gazu i pyłu w kosmosie.",
    "ile wynosi liczba pi": "Około 3.14159.",
    "co to jest e": "Stała matematyczna ≈ 2.718.",
    "co to jest rok przestępny": "Rok z 29 dniami lutego.",
    "co to jest komputer kwantowy": "Komputer wykorzystujący zjawiska kwantowe do obliczeń.",
    "co to jest bitcoin": "Kryptowaluta działająca w sieci blockchain.",
    "co to jest blockchain": "Rozproszona baza danych dla kryptowalut.",
    "co to jest robot": "Maszyna wykonująca zaprogramowane zadania.",
    "co to jest dron": "Bezzałogowy statek powietrzny.",
    "co to jest uczenie maszynowe": "Technika AI polegająca na trenowaniu modeli na danych.",
    "co to jest neuron": "Komórka nerwowa w mózgu.",
    "co to jest synapsa": "Połączenie między neuronami.",
    "co to jest chemia": "Nauka o substancjach i reakcjach.",
    "co to jest fizyka": "Nauka o prawach przyrody.",
    "co to jest biologia": "Nauka o życiu.",
    "co to jest geografia": "Nauka o Ziemi.",
    "co to jest historia": "Nauka o przeszłości ludzi.",
    "co to jest matematyka": "Nauka o liczbach i strukturach.",
    "co to jest statystyka": "Nauka o analizie danych.",
    "co to jest programowanie obiektowe": "Paradygmat programowania z obiektami.",
    "co to jest java": "Język programowania.",
    "co to jest c++": "Język programowania.",
    "co to jest html": "Język znaczników dla stron WWW.",
    "co to jest css": "Stylowanie stron WWW.",
    "co to jest javascript": "Język skryptowy dla stron WWW.",
    "co to jest cpu": "Procesor komputera.",
    "co to jest gpu": "Procesor graficzny.",
    "co to jest ram": "Pamięć operacyjna.",
    "co to jest rom": "Pamięć stała.",
    "co to jest dysk ssd": "Szybki nośnik danych.",
    "co to jest dysk hdd": "Tradycyjny nośnik danych.",
    "co to jest sieć wifi": "Bezprzewodowa sieć komputerowa.",
    "co to jest bluetooth": "Technologia przesyłania danych na krótkie odległości.",
    "co to jest usb": "Uniwersalny standard podłączenia urządzeń.",
    "co to jest chmura": "Usługi w internecie do przechowywania danych.",
    "co to jest algorytm": "Zestaw kroków do rozwiązania problemu.",
    "co to jest baza danych": "Zbiór danych uporządkowanych według schematu.",
    "co to jest aplikacja": "Program komputerowy wykonujący określone zadania.",
    "co to jest system operacyjny": "Oprogramowanie zarządzające komputerem.",
    "co to jest sieć komputerowa": "Połączenie wielu komputerów w celu wymiany danych.",
    "co to jest chmura obliczeniowa": "Dostarczanie usług komputerowych przez internet.",
    "co to jest kod źródłowy": "Tekst programu w języku programowania.",
    "co to jest debugowanie": "Proces wyszukiwania i naprawiania błędów w programie.",
    "co to jest edytor tekstu": "Program do tworzenia i edycji tekstu.",
    "co to jest IDE": "Środowisko programistyczne do pisania kodu.",
    "co to jest git": "System kontroli wersji.",
    "co to jest github": "Platforma do przechowywania kodu i współpracy.",
    "co to jest openai": "Firma zajmująca się sztuczną inteligencją.",
    "co to jest model językowy": "Program uczący się języka i generujący tekst.",
    "co to jest token": "Podstawowa jednostka w modelu językowym.",
    "co to jest API": "Interfejs programowania aplikacji.",
    "co to jest protokół": "Zestaw reguł komunikacji w sieci.",
    "co to jest serwer": "Komputer udostępniający zasoby w sieci.",
    "co to jest klient": "Program korzystający z zasobów serwera.",
    "co to jest plik": "Zbiór danych zapisany na nośniku.",
    "co to jest folder": "Katalog do przechowywania plików.",
    "co to jest kompilator": "Program tłumaczący kod źródłowy na język maszynowy.",
    "co to jest interpreter": "Program wykonujący kod źródłowy bezpośrednio.",
}

# premium_qa ~50 pytań
premium_qa = {
    "kiedy wynaleziono koło": "Około 3500 roku p.n.e.",
    "ile planet ma układ słoneczny": "8 planet.",
    "kto stworzył teorię względności": "Albert Einstein.",
    "kto odkrył amerykę": "Krzysztof Kolumb.",
    "kiedy powstał internet": "W latach 60. XX wieku.",
    "co to jest nanotechnologia": "Dziedzina nauki zajmująca się strukturami w nanoskali.",
    "co to jest wirus": "Pasożyt komórkowy powodujący choroby.",
    "co to jest bakteria": "Jednokomórkowy organizm.",
    "co to jest sztuka": "Wyraz emocji i wyobraźni człowieka.",
    "co to jest filozofia": "Nauka o naturze bytu i myślenia.",
    "co to jest socjologia": "Nauka o społeczeństwie.",
    "co to jest ekonomia": "Nauka o gospodarowaniu zasobami.",
    "co to jest polityka": "Sposób zarządzania państwem.",
    "co to jest prawo": "Zbiór zasad obowiązujących w społeczeństwie.",
    "co to jest etyka": "Nauka o moralności.",
    "co to jest religia": "System wierzeń i praktyk duchowych.",
    "co to jest metawersum": "Wirtualny świat połączony z internetem.",
    "co to jest cyberbezpieczeństwo": "Ochrona danych i systemów komputerowych.",
    "co to jest kwant": "Najmniejsza porcja energii.",
    "co to jest teoria strun": "Model opisujący cząstki jako drgające struny.",
    "co to jest czarna materia": "Niewidoczna substancja we wszechświecie.",
    "co to jest czarna energia": "Energia powodująca przyspieszanie ekspansji wszechświata.",
    "co to jest neuronowa sieć": "Model AI wzorowany na mózgu.",
    "co to jest deep learning": "Zaawansowana forma uczenia maszynowego.",
    "co to jest python flask": "Framework do tworzenia aplikacji webowych w Pythonie.",
    "co to jest fastapi": "Nowoczesny framework webowy w Pythonie.",
    "co to jest render": "Usługa hostowania aplikacji online.",
    "co to jest docker": "Platforma do konteneryzacji aplikacji.",
    "co to jest linux": "System operacyjny open-source.",
    "co to jest windows": "System operacyjny firmy Microsoft.",
    "co to jest macos": "System operacyjny firmy Apple.",
    "co to jest bios": "Podstawowe oprogramowanie płyty głównej.",
    "co to jest pixel": "Najmniejszy element obrazu.",
    "co to jest rozdzielczość": "Ilość pikseli w obrazie.",
    "co to jest fps": "Klatki na sekundę w animacji.",
    "co to jest shader": "Program sterujący renderowaniem grafiki.",
    "co to jest ray tracing": "Technika symulacji światła w grafice 3D.",
    "co to jest unity": "Silnik do tworzenia gier.",
    "co to jest unreal engine": "Zaawansowany silnik gier.",
    "co to jest pixel art": "Grafika zbudowana z małych pikseli.",
    "co to jest 3d modeling": "Tworzenie obiektów trójwymiarowych.",
    "co to jest animacja": "Tworzenie ruchu w obrazie.",
    "co to jest symulacja": "Odwzorowanie zjawisk wirtualnie.",
    "co to jest skrypt": "Zbiór instrukcji wykonywanych automatycznie.",
    "co to jest backend": "Logika serwera aplikacji.",
    "co to jest frontend": "Interfejs widoczny dla użytkownika.",
    "co to jest fullstack": "Połączenie frontendu i backendu.",
    "co to jest cloud computing": "Dostarczanie usług komputerowych przez internet.",
    "co to jest vpn": "Sieć prywatna chroniąca połączenie.",
}

# ------------------ FUNKCJE MATEMATYCZNE ------------------
def gcd(a, b):
    return math.gcd(a, b)

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def parse_n_numbers(s):
    """Zwraca listę liczb całkowitych z podanego ciągu (np. '2,3' lub '2 3')."""
    parts = re.split(r'[,\s]+', s.strip())
    nums = []
    for p in parts:
        if p == "":
            continue
        try:
            nums.append(int(p))
        except:
            # jeśli nie da się rzutować na int, pomiń
            pass
    return nums

def calculate_expression(expr):
    """
    Obsługuje:
    - wyrażenia arytmetyczne ( + - * / ( ) )   np. 2*2, 5+3-1, (2+3)*4
    - NWD (nwd2,3 lub nwd 2 3)
    - NWW (nww3,6 lub nww 3 6)
    Zwraca string z wynikiem lub None jeśli niepoprawne.
    """
    if not expr or not isinstance(expr, str):
        return None
    s = expr.strip().lower()
    s = s.replace(",", ".")  # przecinki w liczbach jako kropki (dla dzielenia)
    s = s.replace("x", "*")

    # obsługa nwd / nww (możliwe formy: nwd2,3 ; nwd 2 3 ; nwd(2,3))
    if s.startswith("nwd"):
        tail = s[3:].strip()
        tail = tail.strip("() ")
        nums = parse_n_numbers(tail)
        if len(nums) >= 2:
            res = nums[0]
            for n in nums[1:]:
                res = gcd(res, n)
            return str(res)
        else:
            return "Błąd NWD: podaj co najmniej dwie liczby, np. NWD 12,18"
    if s.startswith("nww"):
        tail = s[3:].strip()
        tail = tail.strip("() ")
        nums = parse_n_numbers(tail)
        if len(nums) >= 2:
            res = nums[0]
            for n in nums[1:]:
                res = lcm(res, n)
            return str(res)
        else:
            return "Błąd NWW: podaj co najmniej dwie liczby, np. NWW 4,6"

    # jeśli użytkownik pisze "nwd 12 8" bez bezpośredniego prefixu, spróbuj znaleźć
    m = re.match(r'.*\bnwd\b\s*[:\(\s]*([0-9,\s]+)', s)
    if m:
        nums = parse_n_numbers(m.group(1))
        if len(nums) >= 2:
            res = nums[0]
            for n in nums[1:]:
                res = gcd(res, n)
            return str(res)
    m2 = re.match(r'.*\bnww\b\s*[:\(\s]*([0-9,\s]+)', s)
    if m2:
        nums = parse_n_numbers(m2.group(1))
        if len(nums) >= 2:
            res = nums[0]
            for n in nums[1:]:
                res = lcm(res, n)
            return str(res)

    # pozostałe: wyrażenie arytmetyczne - bezpieczna evaluacja
    # zezwalamy tylko na cyfry, spacje, .+-*/() 
    allowed = re.compile(r'^[0-9\.\+\-\*\/\(\)\s]+$')
    expr_clean = expr.replace(",", ".").replace("x", "*")
    if allowed.match(expr_clean.strip()):
        try:
            # eval jest tutaj stosowany na oczyszczonym wyrażeniu (bez liter), 
            # nadal stosuj ostrożność, ale do prostych obliczeń jest OK
            value = eval(expr_clean, {"__builtins__": None}, {})
            # jeśli to float bez ułamka, pokaż jako int
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            return str(value)
        except ZeroDivisionError:
            return "Błąd: dzielenie przez zero"
        except Exception:
            return None
    return None

# ------------------ HELPERS SESJI ------------------
def init_session():
    if "coins" not in session:
        session["coins"] = 0
    if "premium" not in session:
        session["premium"] = False
    if "game" not in session:
        session["game"] = False
    if "game_enabled" not in session:
        session["game_enabled"] = True
    if "admin" not in session:
        session["admin"] = False

# ------------------ ROUTES ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    init_session()
    response = ""
    if request.method == "POST":
        raw = (request.form.get("message") or "").strip()
        msg = raw.lower().strip()
        if not msg:
            response = ""
        else:
            # polecenia systemowe
            if msg == "/gra start":
                if session.get("game_enabled", True):
                    session["game"] = True
                    response = "Gra papier-kamień-nożyce rozpoczęta! Wpisz: kamień, papier lub nożyce."
                else:
                    response = "Gra jest wyłączona przez administratora."
            elif msg == "/gra stop":
                session["game"] = False
                response = "Gra zakończona."
            elif msg == "/kup premium" or msg == "kup premium" or msg == "kup premium.":
                if session["premium"]:
                    response = "Masz już premium."
                elif session["coins"] >= PREMIUM_COST:
                    session["coins"] -= PREMIUM_COST
                    session["premium"] = True
                    response = f"Kupiłeś wersję premium! Odblokowano +{PREMIUM_EXTRA_COUNT} pytań."
                else:
                    response = f"Nie masz wystarczająco monet. Koszt: {PREMIUM_COST}."
            else:
                # jeśli gra aktywna i użytkownik wpisuje ruch
                if session.get("game"):
                    if msg in ["kamień", "papier", "nożyce"]:
                        bot = random.choice(["kamień", "papier", "nożyce"])
                        if msg == bot:
                            result = "Remis!"
                        elif (msg == "kamień" and bot == "nożyce") or (msg == "papier" and bot == "kamień") or (msg == "nożyce" and bot == "papier"):
                            result = "Wygrałeś!"
                            session["coins"] += 1
                        else:
                            result = "Przegrałeś!"
                            session["coins"] -= 1
                        response = f"Bot wybrał {bot}. {result}"
                        # nie szukamy QA dalej
                    else:
                        # nie jest to ruch — nadal próbujemy odpowiedzieć normalnie
                        # najpierw spróbuj matematyki
                        calc = calculate_expression(raw)
                        if calc is not None:
                            response = f"Wynik: {calc}"
                        else:
                            # QA: łączymy base + premium jeśli premium = True
                            qa_pool = dict(basic_qa)
                            if session.get("premium"):
                                qa_pool.update(premium_qa)
                            response = qa_pool.get(msg, "Nie znam odpowiedzi na to pytanie.")
                else:
                    # gra nieaktywna: obsługa matematyki i QA
                    calc = calculate_expression(raw)
                    if calc is not None:
                        response = f"Wynik: {calc}"
                    else:
                        qa_pool = dict(basic_qa)
                        if session.get("premium"):
                            qa_pool.update(premium_qa)
                        response = qa_pool.get(msg, "Nie znam odpowiedzi na to pytanie.")

    return render_template_string("""
    <!doctype html>
    <html lang="pl">
    <head>
      <meta charset="utf-8">
      <title>Scended AI (web)</title>
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <style>
        :root { --bg:#1e1e1e; --panel:#333; --accent:#2ecc71; --muted:#555; --text:#fff; }
        body { margin:0; font-family:Arial,Helvetica,sans-serif; background:var(--bg); color:var(--text); display:flex; flex-direction:column; height:100vh; }
        header{padding:12px; border-bottom:1px solid rgba(255,255,255,0.03);}
        main{flex:1; display:flex; flex-direction:column; padding:12px; box-sizing:border-box;}
        #chatbox{flex:1; background:#222; border-radius:8px; padding:12px; overflow:auto;}
        .message.user{background:#4d4d4d; padding:8px; border-radius:6px; margin:6px 0; max-width:80%;}
        .message.ai{background:var(--accent); padding:8px; border-radius:6px; margin:6px 0; max-width:80%;}
        form{display:flex; gap:8px; margin-top:10px;}
        input[type=text]{flex:1; padding:10px; border-radius:6px; border:none; background:var(--panel); color:var(--text); font-size:14px;}
        button{padding:10px 12px; border-radius:6px; border:none; background:var(--muted); color:white; cursor:pointer;}
        .top-info{display:flex; justify-content:space-between; align-items:center;}
        .small{font-size:13px; color: #ddd;}
        .admin-link a{color:#fff; text-decoration:none; background:#444; padding:6px 8px; border-radius:6px;}
        .hint{font-size:13px;color:#bbb;margin-top:6px;}
      </style>
    </head>
    <body>
      <header>
        <div class="top-info">
          <div><strong>Scended AI</strong></div>
          <div>
            <span class="small">💰 Monety: {{coins}}</span>
            &nbsp;&nbsp;
            <span class="small">Premium: {{premium}}</span>
            &nbsp;&nbsp;
            <span class="admin-link"><a href="/admin">Panel Admina</a></span>
          </div>
        </div>
      </header>
      <main>
        <div id="chatbox">
          {% if response %}
            <div class="message ai"><strong>Scended AI:</strong> {{response}}</div>
          {% else %}
            <div class="hint">Wpisz pytanie, komendę lub wyrażenie matematyczne (np. 2*2, 12/4, NWD12,18, NWW4,6). Komenda: <code>/gra start</code>, kup premium: <code>/kup premium</code></div>
          {% endif %}
        </div>

        <form method="post">
          <input type="text" name="message" placeholder="Wpisz pytanie lub wyrażenie (np. 2*2 albo NWD12,18)" autofocus>
          <button type="submit">Wyślij</button>
        </form>
      </main>
    </body>
    </html>
    """, response=response, coins=session["coins"], premium=session["premium"])

# ------------------ PANEL ADMINA ------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    init_session()
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    msg = ""
    if request.method == "POST":
        # dodawanie monet
        if "add_coins" in request.form:
            try:
                amount = int(request.form.get("add_coins") or 0)
                session["coins"] += amount
                msg = f"Dodano {amount} monet do aktualnej sesji."
            except:
                msg = "Błąd: podaj liczbę całkowitą."
        # dodawanie pytania
        elif "new_q" in request.form and "new_a" in request.form:
            q = (request.form.get("new_q") or "").strip().lower()
            a = (request.form.get("new_a") or "").strip()
            place = request.form.get("place", "basic")
            if q and a:
                if place == "basic":
                    basic_qa[q] = a
                else:
                    premium_qa[q] = a
                msg = "Dodano nowe pytanie."
            else:
                msg = "Uzupełnij pytanie i odpowiedź."
        elif "toggle_game" in request.form:
            session["game_enabled"] = not session.get("game_enabled", True)
            msg = f"Gra {'włączona' if session['game_enabled'] else 'wyłączona'}."
        elif "logout" in request.form:
            session["admin"] = False
            return redirect(url_for("index"))

    return render_template_string("""
    <!doctype html>
    <html lang="pl">
    <head>
      <meta charset="utf-8">
      <title>Panel Admina</title>
      <style>
        body{background:#111;color:#fff;font-family:Arial;padding:20px;}
        input,select,textarea{padding:8px;border-radius:6px;border:none;margin:6px 0;width:100%;}
        .box{background:#1b1b1b;padding:16px;border-radius:8px;max-width:700px;margin:auto;}
        button{padding:8px 10px;border-radius:6px;border:none;background:#2b2b2b;color:#fff;cursor:pointer;}
        label{font-size:14px;}
        a{color:#9fe;}
      </style>
    </head>
    <body>
      <div class="box">
        <h2>Panel Admina</h2>
        <p style="color:lightgreen;">{{msg}}</p>

        <h3>Dodaj monety (do bieżącej sesji)</h3>
        <form method="post">
          <input type="number" name="add_coins" placeholder="Ilość monet (np. 10)">
          <button type="submit">Dodaj monety</button>
        </form>

        <h3>Dodaj pytanie/odpowiedź</h3>
        <form method="post">
          <input type="text" name="new_q" placeholder="Nowe pytanie (w małych literach)">
          <input type="text" name="new_a" placeholder="Odpowiedź">
          <label>Dodaj do: 
            <select name="place">
              <option value="basic">Podstawowe</option>
              <option value="premium">Premium</option>
            </select>
          </label>
          <button type="submit">Dodaj pytanie</button>
        </form>

        <h3>Kontrola gry</h3>
        <form method="post">
          <input type="hidden" name="toggle_game" value="1">
          <button type="submit">Włącz/Wyłącz grę (aktualnie: {{ 'włączona' if session.game_enabled else 'wyłączona' }})</button>
        </form>

        <h3>Wyloguj admina</h3>
        <form method="post">
          <input type="hidden" name="logout" value="1">
          <button type="submit">Wyloguj</button>
        </form>

        <p><a href="/">← Powrót do aplikacji</a></p>
      </div>
    </body>
    </html>
    """, msg=msg)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    init_session()
    if request.method == "POST":
        pwd = request.form.get("password") or ""
        if pwd == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return render_template_string("""
            <p style="color:red;text-align:center;">Niepoprawne hasło</p>
            <p style="text-align:center;"><a href="/admin/login">Spróbuj ponownie</a></p>
            """)
    return '''
    <!doctype html><html><head><meta charset="utf-8"><title>Login Admin</title></head>
    <body style="background:#111;color:#fff;font-family:Arial;">
      <div style="max-width:400px;margin:80px auto;padding:20px;background:#1b1b1b;border-radius:8px;">
        <h2>Logowanie Admin</h2>
        <form method="post">
          <input type="password" name="password" placeholder="Hasło admina" style="width:100%;padding:8px;border-radius:6px;border:none;margin-bottom:8px;">
          <button style="padding:8px 12px;border-radius:6px;border:none;background:#2b2b2b;color:#fff;">Zaloguj</button>
        </form>
        <p style="margin-top:10px;"><a href="/" style="color:#9fe;">← Powrót</a></p>
      </div>
    </body></html>
    '''

# ------------------ URUCHOMIENIE ------------------
if __name__ == "__main__":
    # dla hostingu: app.run(host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
