from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# --- DATASETS ---
# Base pots configuration. Pot 4 includes fixed teams; Play-off winners are dynamic.
BASE_POTS = {
    1: [
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
        {"isim": "Jordan", "kitalar": ["AS"]}, {"isim": "Cabo Verde", "kitalar": ["AF"]},
        {"isim": "Ghana", "kitalar": ["AF"]}, {"isim": "Curaçao", "kitalar": ["NA"]},
        {"isim": "Haiti", "kitalar": ["NA"]}, {"isim": "New Zealand", "kitalar": ["OC"]}
    ]
}

def check_valid_group(group, new_team):
    """
    Validates if a team can be added to a group based on FIFA constraints:
    1. Max 2 European teams per group. (at least 1)
    2. No other confederation can have more than 1 team per group.
    """
    eu_count = sum(1 for member in group if "EU" in member['kitalar'])
    new_team_continents = set(new_team['kitalar'])
    
    # Rule 1: UEFA Limit
    if "EU" in new_team_continents and eu_count >= 2:
        return False

    # Rule 2: Continental Separation (Composite Constraint for Play-offs)
    for member in group:
        member_continents = set(member['kitalar'])
        intersection = new_team_continents.intersection(member_continents)
        
        if intersection:
            if intersection == {"EU"}:
                continue
            else:
                return False 
    return True

def check_final_distribution(groups):
    """ Ensures every group has at least one European team. """
    for group in groups:
        has_eu = any("EU" in t['kitalar'] for t in group)
        if not has_eu:
            return False
    return True

def draw_simulation(user_playoff_winners):
    """ Executes the draw logic using backtracking/random shuffling. """
    pots = {k: [t.copy() for t in v] for k, v in BASE_POTS.items()}
    pots[4].extend(user_playoff_winners)
    
    groups = [[] for _ in range(12)]
    group_names = list("ABCDEFGHIJKL")

    # Step 1: Assign Hosts
    groups[0].append({"isim": "Mexico", "kitalar": ["NA"]})
    groups[1].append({"isim": "Canada", "kitalar": ["NA"]})
    groups[3].append({"isim": "USA", "kitalar": ["NA"]})

    # Step 2: Distribute Pot 1
    current_pot1 = pots[1][:]
    random.shuffle(current_pot1)
    for i in range(12):
        if len(groups[i]) == 0:
            groups[i].append(current_pot1.pop(0))

    # Step 3: Distribute Pots 2-4
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
            if not placed: return None

    if not check_final_distribution(groups): return None
    
    # Format Result
    result = []
    for idx, group_data in enumerate(groups):
        formatted_teams = []
        for t in group_data:
            display_kita = t['kitalar'][0] if len(t['kitalar']) == 1 else "MIXED"
            formatted_teams.append({"isim": t['isim'], "kita": display_kita})
            
        result.append({"name": group_names[idx], "teams": formatted_teams})
    return result

# --- ROUTES ---

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
    raw_playoff_winners = data.get('playoff_winners', [])
    
    cleaned_winners = []
    
    # Default placeholder data if request is empty
    if not raw_playoff_winners:
        cleaned_winners = [
            {"isim": "UEFA Path A", "kitalar": ["EU"]},
            {"isim": "UEFA Path B", "kitalar": ["EU"]},
            {"isim": "Türkiye", "kitalar": ["EU"]},
            {"isim": "UEFA Path D", "kitalar": ["EU"]},
            {"isim": "FIFA PO 1", "kitalar": ["NA", "AF", "OC"]},
            {"isim": "FIFA PO 2", "kitalar": ["AS", "SA", "NA"]}
        ]
    else:
        # Process and normalize input data
        for team in raw_playoff_winners:
            new_team = team.copy()
            if 'kitalar' not in new_team:
                new_team['kitalar'] = [new_team['kita']] if 'kita' in new_team else ["EU"]
            
            # Apply composite constraints for FIFA Play-offs
            po1_keywords = ["FIFA PO 1", "Jamaica", "DR Congo", "New Caledonia", "Y. Kaledonya", "DK Kongo", "Jamaika"]
            if any(k in new_team['isim'] for k in po1_keywords):
                new_team['kitalar'] = ["NA", "AF", "OC"]
                
            po2_keywords = ["FIFA PO 2", "Iraq", "Bolivia", "Suriname", "Irak", "Bolivya", "Surinam"]
            if any(k in new_team['isim'] for k in po2_keywords):
                new_team['kitalar'] = ["AS", "SA", "NA"]
                
            cleaned_winners.append(new_team)

    # Attempt draw generation
    success = False
    result = None
    attempt = 0
    
    while not success and attempt < 5000:
        attempt += 1
        result = draw_simulation(cleaned_winners)
        if result is not None:
            success = True
            
    if not success:
        return jsonify({"error": "Valid draw configuration not found. Please try again."}), 500
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)