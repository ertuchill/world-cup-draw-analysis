from app import draw_simulation
import collections
import time

def run_scenario_analysis(target_country="Croatia", simulation_count=10000):
    
    # SİMÜLASYON İÇİN KULLANILACAK PLAY-OFF PLACEHOLDER'LARI
    # Diğerleri ise "Composite" (Bileşik) kısıtlarıyla giriyor.
    simulation_participants = [
        {"isim": "UEFA Path A", "kitalar": ["EU"]},
        {"isim": "UEFA Path B", "kitalar": ["EU"]},
        {"isim": "UEFA PATH C", "kitalar": ["EU"]},
        {"isim": "UEFA Path D", "kitalar": ["EU"]},
        
        # Bu top gelirse, o grupta NA, AF veya OC olamaz.
        {"isim": "FIFA PO 1", "kitalar": ["NA", "AF", "OC"]}, 
        
        # Bu top gelirse, o grupta AS, SA veya NA olamaz.
        {"isim": "FIFA PO 2", "kitalar": ["AS", "SA", "NA"]}
    ]

    opponent_stats = collections.Counter()
    
    print(f"\n🚀 {target_country} için {simulation_count} simülasyon çalıştırılıyor...")
    start_time = time.time()
    successful_draws = 0
    
    while successful_draws < simulation_count:
        # Her tur aynı "Placeholder" setiyle dönüyor, çünkü kısıtlar sabit.
        result = draw_simulation(simulation_participants)
        
        if result:
            successful_draws += 1
            
            # Hedef ülkenin grubunu bul
            target_group = None
            for group in result:
                # App.py artık formatted döndüğü için 'isim' yine anahtardır
                team_names = [t['isim'] for t in group['teams']]
                if target_country in team_names:
                    target_group = team_names
                    break
            
            if target_group:
                for member_name in target_group:
                    if member_name != target_country:
                        opponent_stats[member_name] += 1
            
            if successful_draws % (simulation_count // 5) == 0:
                print(f"   ... %{int(successful_draws/simulation_count*100)} tamamlandı.")

    duration = time.time() - start_time
    
    print(f"\n✅ Analiz bitti! ({duration:.2f} sn)")
    print("="*60)
    print(f"📊 {target_country.upper()} - OLASI RAKİPLER")
    print("="*60)
    print(f"{'RAKİP TAKIM':<30} | {'OLASILIK':<10}")
    print("-" * 60)
    
    # Sıralı yazdır
    for team, count in opponent_stats.most_common():
        prob = (count / simulation_count) * 100
        # Placeholder isimlerini daha anlaşılır kılabiliriz çıktı verirken
        display_name = team
        if team == "FIFA PO 1": display_name = "FIFA PO 1 (Jam/DRC/NC)"
        if team == "FIFA PO 2": display_name = "FIFA PO 2 (Iraq/Bol/Sur)"
            
        print(f"{display_name:<30} | %{prob:.2f}")

if __name__ == "__main__":
    run_scenario_analysis("Croatia", 10000)