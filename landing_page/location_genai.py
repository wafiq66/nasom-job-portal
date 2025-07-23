import google.generativeai as genai
from decouple import config
from functools import lru_cache
from django.core.cache import cache
# Create your views here.

#this is the API key configuration
genai.configure(api_key=config("AI_API_KEY"))

#Method to get the query by using AI
@lru_cache(maxsize=128)
def generate_search_queries(query):
    model = genai.GenerativeModel("gemini-1.5-flash")

    system_instruction = """
        You are a Malaysian location interpreter. You will be given a location input from a user — often informal, abbreviated, or colloquial — referring to a place within Malaysia.

        Your task is to process that input and output the correct, normalized **city/district** and its corresponding **state**.

        Your output rules:

        - Always output the **city or district name**, followed by a semicolon, then the **state name**;
        - Even if there is only one result, always separate it as two values (e.g., “Petaling Jaya; Selangor”);
        - If the input could refer to multiple valid locations, return each city-state pair on a new line (each line formatted as `<city or district>; <state>`);
        - Use the most **commonly known**, **real**, and **official** names in Malaysia;
        - Recognize common abbreviations and slang (e.g., "pj" → "Petaling Jaya", "kl" → "Kuala Lumpur");
        - If the input refers to a **region** (e.g., “north”, “pantai timur”), list relevant major cities for that region with their states;
        - Keep your output clean — no explanation, no extra formatting, no quotes, just lines of location pairs;

        Assume all inputs are places within Malaysia. Your job is to identify and normalize them clearly and consistently.
        """

    response = model.generate_content(
        contents=[system_instruction, query],  # Move instruction into contents
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    )

    # Extract response text
    if response and response.text:
        return response.text.split(";")  # Convert response into list
    return []



location_groups = {
    # Johor
    'johor': ['johor'],
    'batu pahat': ['batu', 'batu pahat'],
    'johor bahru': ['jb', 'johor', 'johor bahru'],
    'kluang': ['kluang'],
    'kota tinggi': ['kota', 'kota tinggi'],
    'muar': ['muar'],
    'pontian': ['pontian'],
    'segamat': ['segamat'],
    'mersing': ['mersing'],
    'tangkak': ['tangkak'],
    
    # Kedah
    'kedah': ['kedah'],
    'baling': ['baling'],
    'kota setar': ['kota', 'setar', 'kota setar'],
    'kubang pasu': ['kubang', 'pasu', 'kubang pasu'],
    'kulim': ['kulim'],
    'langkawi': ['langkawi'],
    'padang terap': ['padang', 'terap', 'padang terap'],
    'pokok sena': ['pokok', 'sena', 'pokok sena'],
    'pendang': ['pendang'],
    'sik': ['sik'],
    'yan': ['yan'],
    
    # Kelantan
    'kelantan': ['kelantan'],
    'bachok': ['bachok'],
    'gua musang': ['gua', 'musang', 'gua musang'],
    'jeli': ['jeli'],
    'kota bharu': ['kota', 'bharu', 'kota bharu'],
    'kuala krai': ['kuala', 'krai', 'kuala krai'],
    'machang': ['machang'],
    'pasir mas': ['pasir', 'mas', 'pasir mas'],
    'pasir puteh': ['puteh', 'pasir puteh'],
    'tanah merah': ['tanah', 'merah', 'tanah merah'],
    'tumpat': ['tumpat'],

    # Melaka
    'melaka': ['melaka'],
    'alor gajah': ['alor', 'gajah', 'alor gajah'],
    'melaka tengah': ['melaka', 'tengah', 'melaka tengah'],
    'jelebu': ['jelebu'],
    'jernih': ['jernih'],

    # Negeri Sembilan
    'negeri sembilan': ['negeri sembilan','sembilan'],
    'seremban': ['seremban'],
    'port dickson': ['port', 'dickson', 'port dickson'],
    'rembau': ['rembau'],
    'tampin': ['tampin'],

    # Pahang
    'pahang': ['pahang'],
    'bentong': ['bentong'],
    'berau': ['berau'],
    'cameroon highlands': ['cameroon', 'highlands', 'cameroon highlands'],
    'jerantut': ['jerantut'],
    'kuantan': ['kuantan'],
    'lipis': ['lipis'],
    'maran': ['maran'],
    'pekan': ['pekan'],
    'raub': ['raub'],
    'rompin': ['rompin'],
    'temerloh': ['temerloh'],

    # Penang
    'penang': ['penang'],
    'seberang perai utara': ['seberang', 'utara', 'seberang perai utara'],
    'seberang perai tengah': ['seberang tengah', 'seberang perai tengah'],
    'seberang perai selatan': ['seberang selatan', 'seberang perai selatan'],
    'timur laut': ['timur', 'laut', 'timur laut'],
    'barat daya': ['barat', 'daya', 'barat daya'],
    'george town': ['george', 'georgetown', 'george town'],

    # Perak
    'perak': ['perak'],
    'bagan datuk': ['bagan datuk'],
    'bagan serai': ['bagan serai'],
    'batang padang': ['batang padang'],
    'hilir perak': ['hilir perak'],
    'kinta': ['kinta'],
    'kerian': ['kerian'],
    'larut matang': ['larut', 'matang', 'larut matang'],
    'lenggong': ['lenggong'],
    'manjung': ['manjung'],
    'perak tengah': ['perak tengah'],
    'selama': ['selama'],
    'slim river': ['slim river'],

    # Perlis
    'perlis': ['perlis'],
    'arau': ['arau'],
    'kangar': ['kangar'],
    'padang besar': ['padang besar'],

    # Putrajaya / Kuala Lumpur
    'putrajaya': ['putrajaya'],
    'kuala lumpur': ['kl', 'kuala', 'lumpur', 'kuala lumpur'],

    # Selangor
    'selangor': ['selangor'],
    'gombak': ['gombak'],
    'hulu langat': ['hulu langat'],
    'hulu selangor': ['hulu selangor'],
    'klang': ['klang'],
    'kuala langat': ['kuala langat'],
    'kuala selangor': ['kuala selangor'],
    'petaling': ['petaling'],
    'sabak bernam': ['sabak', 'bernam', 'sabak bernam'],
    'sepang': ['sepang'],
    'shah alam': ['shah', 'alam', 'shah alam'],
    'petaling jaya': ['pj', 'petaling jaya'],

    # Sabah
    'sabah': ['sabah'],
    'kota kinabalu': ['kk', 'kota kinabalu'],
    'penampang': ['penampang'],
    'tuaran': ['tuaran'],
    'sandakan': ['sandakan'],
    'tawau': ['tawau'],
    'lahad datu': ['lahad', 'datu', 'lahad datu'],
    'kinabatangan': ['kinabatangan'],

    # Sarawak
    'sarawak': ['sarawak'],
    'kuching': ['kuching'],
    'samarahan': ['samarahan'],
    'sibu': ['sibu'],
    'bintulu': ['bintulu'],
    'miri': ['miri'],
    'limbang': ['limbang'],
    'kapit': ['kapit'],

    # Terengganu
    'terengganu': ['terengganu'],
    'besut': ['besut'],
    'dungun': ['dungun'],
    'hulu terengganu': ['hulu terengganu'],
    'kemaman': ['kemaman'],
    'kuala nerus': ['kuala nerus'],
    'kuala terengganu': ['kuala terengganu'],
    'marang': ['marang'],
    'setiu': ['setiu'],
}

LOCATION_SYNONYMS = {}

for canonical_name, synonyms in location_groups.items():
    for synonym in synonyms:
        LOCATION_SYNONYMS[synonym.lower()] = canonical_name

def normalize_location_input(user_input):
    user_input = user_input.lower().strip()
    return LOCATION_SYNONYMS.get(user_input, user_input)


def get_location_result(location_input):
    standard_input = normalize_location_input(location_input)
    result = cache.get(standard_input)
    if result is None:
        result = generate_search_queries(location_input)
        cache.set(location_input, result, timeout=3600)  # 1 hour cache
    return result

