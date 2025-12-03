from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# --- VERİ YAPISI ---
# Artık 'kita' yerine 'kitalar' listesi kullanıyoruz.
# Böylece bir Play-off topu birden fazla kıtayı temsil edebiliyor.

BASE_POTS = {
    1: [
        # Ev sahipleri manuel eklenecek
        {"isim": "Spain", "kitalar": ["EU"]}, {"isim": "Argentina", "kitalar": ["SA"]}, 
        {"isim": "France", "kitalar": ["EU"]}, {"isim": "England", "kitalar": ["EU"]}, 
        {"isim": "Brazil", "kitalar": ["SA"]}, {"isim": "Portugal", "kitalar": ["EU"]}, 
        {"isim": "Netherlands", "kitalar": ["EU"]}, {"isim": "Belgium", "kitalar": ["EU"]}, 
        {"isim": "Germany", "kitalar": ["EU"]}
    ],
    2: [
        {"isim": "Croatia", "kitalar": ["EU"]}, {"isim": "Morocco", "kitalar": ["AF"]},
        {"isim": "Colombia", "kitalar": ["SA"]}, {"isim": "Uruguay", "kitalar": ["SA"]},
        {"isim": "Switzerland", "kitalar": ["EU"]}, {"isim": "Japan", "kitalar": ["AS"]},
        {"isim": "Senegal", "kitalar": ["AF"]}, {"isim": "IR Iran", "kitalar": ["AS"]},
        {"isim": "Korea Republic", "kitalar": ["AS"]}, {"isim": "Ecuador", "kitalar": ["SA"]},
        {"isim": "Austria", "kitalar": ["EU"]}, {"isim": "Australia", "kitalar": ["AS"]}
    ],
    3: [
        {"isim": "Norway", "kitalar": ["EU"]}, {"isim": "Panama", "kitalar": ["NA"]},
        {"isim": "Egypt", "kitalar": ["AF"]}, {"isim": "Algeria", "kitalar": ["AF"]},
        {"isim": "Scotland", "kitalar": ["EU"]}, {"isim": "Paraguay", "kitalar": ["SA"]},
        {"isim": "Tunisia", "kitalar": ["AF"]}, {"isim": "Côte d'Ivoire", "kitalar": ["AF"]},
        {"isim": "Uzbekistan", "kitalar": ["AS"]}, {"isim": "Qatar", "kitalar": ["AS"]},
        {"isim": "Saudi Arabia", "kitalar": ["AS"]}, {"isim": "South Africa", "kitalar": ["AF"]}
    ],
    4: [
        # Sabit 4. Torba
        {"isim": "Jordan", "kitalar": ["AS"]}, {"isim": "Cabo Verde", "kitalar": ["AF"]},
        {"isim": "Ghana", "kitalar": ["AF"]}, {"isim": "Curaçao", "kitalar": ["NA"]},
        {"isim": "Haiti", "kitalar": ["NA"]}, {"isim": "New Zealand", "kitalar": ["OC"]}
    ]
}

def check_valid_group(group, new_team):
    """
    Grup kurallarını kontrol eder.
    new_team: Eklenecek aday takım
    """
    eu_count = 0
    
    # Yeni takımın yasaklı kıtaları (Set kümesi olarak)
    new_team_continents = set(new_team['kitalar'])
    
    # 1. AVRUPA SAYISI KONTROLÜ
    # Gruptaki mevcut Avrupalıları say
    for member in group:
        if "EU" in member['kitalar']:
            eu_count += 1
            
    # Eğer yeni takım Avrupalıysa (veya Avrupa ihtimali varsa) ve kota dolduysa
    if "EU" in new_team_continents and eu_count >= 2:
        return False

    # 2. KITA ÇAKIŞMASI KONTROLÜ (Composite Constraint)
    for member in group:
        member_continents = set(member['kitalar'])
        
        # İki kümenin kesişimini al (Ortak kıtalar)
        intersection = new_team_continents.intersection(member_continents)
        
        # Eğer ortak kıta varsa:
        if intersection:
            # Eğer ortak olan tek şey Avrupa ise sorun yok (Max 2 kuralı zaten yukarıda bakıldı)
            if intersection == {"EU"}:
                continue
            # Avrupa dışında bir çakışma varsa (Örn: NA ile NA, veya [NA,AF] ile NA) -> YASAK
            else:
                return False
                
    return True

def check_final_distribution(groups):
    for group in groups:
        # Her grupta en az 1 Avrupa olmalı
        # (Basitlik adına: İçinde 'EU' barındıran herhangi bir takım varsa sayar)
        has_eu = False
        for t in group:
            if "EU" in t['kitalar']:
                has_eu = True
                break
        if not has_eu:
            return False
    return True

def draw_simulation(user_playoff_winners):
    # Veri setini kopyala
    pots = {k: [t.copy() for t in v] for k, v in BASE_POTS.items()}
    
    # 4. Torbaya Play-off kazananlarını (veya placeholderlarını) ekle
    # Frontend'den gelen veri yapısı: {"isim": "...", "kitalar": ["NA", "AF"]} şeklinde olmalı
    pots[4].extend(user_playoff_winners)
    
    groups = [[] for _ in range(12)]
    group_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    # --- ADIM 1: EV SAHİPLERİ ---
    groups[0].append({"isim": "Mexico", "kitalar": ["NA"]})
    groups[1].append({"isim": "Canada", "kitalar": ["NA"]})
    groups[3].append({"isim": "USA", "kitalar": ["NA"]})

    # --- ADIM 2: 1. TORBA DAĞITIM ---
    current_pot1 = pots[1][:]
    random.shuffle(current_pot1)
    for i in range(12):
        if len(groups[i]) == 0:
            groups[i].append(current_pot1.pop(0))

    # --- ADIM 3: DİĞER TORBALAR ---
    for pot_num in range(2, 5):
        current_pot = pots[pot_num][:]
        random.shuffle(current_pot)
        
        for i in range(12):
            placed = False
            random.shuffle(current_pot)
            for team in current_pot:
                if check_valid_group(groups[i], team):
                    groups[i].append(team)
                    current_pot.remove(team)
                    placed = True
                    break
            if not placed: return None # Deadlock

    if not check_final_distribution(groups): return None
    
    # Sonuç Formatı (Frontend için tek bir 'kita' stringi dönmek yeterli görsellik için)
    result = []
    for idx, group_data in enumerate(groups):
        formatted_teams = []
        for t in group_data:
            # Görsel olarak ilk kıtayı veya özel stringi gösterelim
            display_kita = t['kitalar'][0] if len(t['kitalar']) == 1 else "MIXED"
            formatted_teams.append({"isim": t['isim'], "kita": display_kita})
            
        result.append({
            "name": group_names[idx],
            "teams": formatted_teams
        })
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/analysis')
def analysis_page():
    return render_template('analysis.html')

@app.route('/api/draw', methods=['POST'])
def api_draw():
    data = request.json
    # Frontend'den gelen play-off verisi.
    # Eğer "Simülasyona Bırak" denildiyse veya analiz yapılıyorsa,
    # burada "Placeholder" mantığını kullanacağız.
    playoff_winners = data.get('playoff_winners', [])
    
    # Hata önleyici: Eğer boş gelirse varsayılanları koy
    if not playoff_winners:
        # Varsayılan (Placeholder) Yapı
        playoff_winners = [
            {"isim": "UEFA Path A", "kitalar": ["EU"]},
            {"isim": "UEFA Path B", "kitalar": ["EU"]},
            {"isim": "Türkiye", "kitalar": ["EU"]}, # Varsayılan biz olalım
            {"isim": "UEFA Path D", "kitalar": ["EU"]},
            {"isim": "FIFA PO 1", "kitalar": ["NA", "AF", "OC"]}, # KARIŞIK KITA!
            {"isim": "FIFA PO 2", "kitalar": ["AS", "SA", "NA"]}  # KARIŞIK KITA!
        ]

    success = False
    result = None
    attempt = 0
    
    while not success and attempt < 5000:
        attempt += 1
        result = draw_simulation(playoff_winners)
        if result is not None:
            success = True
            
    if not success:
        return jsonify({"error": "Uygun kura bulunamadı, kısıtlar çok sıkı!"}), 500
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)