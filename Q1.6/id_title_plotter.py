import matplotlib.pyplot as plt
import locale

# ==========================================
# 1. DATA DEFINITIONS
# ==========================================

# Title Column Data
title_bounds = [
    "½ Sold", "(#1.146)", "(#1.292)", "(#1.53)", "(#1.7904)", "(#13.39)", "(#2.42)", "(#3.64)", "(#5.41)", "(#8.2)", 
    "1970-05-01", "1986-06-05", "1995-04-20", "1998-07-22", "2000-07-01", "2002-05-04", "2004-02-23", "2005-06-03", 
    "2006-07-19", "2007-11-17", "2009-06-15", "2011-03-04", "2012-03-19", "2013-01-30", "364 Days Later", 
    "A Man on His Own", "Abschied", "Alan John Tew", "An Inside Tip", "Arrivée d'un train à Perrache", 
    "Back from Paris", "Behind the Scenes", "Black Shadows on the Silver Screen", "Brent jord", 
    "Çanakkale Destani 1915", "Checkmate", "CNN Special Reports: The Moses Project", "Courtes histoires de train", 
    "Dappledown Farm", "Death Without Consent", "DHL Presents Major League Baseball Hometown Heroes", "DNA", 
    "Drop Out", "El depósito", "Enter! The World of the Shinigami", "Fake It & Make It", "Fire Dragon", 
    "Fredriks prao", "Geoffrey Hughes", "Gradostroiteli", "Happy Ending", "Hidden Treasure", "Hounded", 
    "Icelandic Geysir", "Inside the Capsule", "Japanese Bravery: An Incident in the War", "Jumping Jackpot", 
    "Kidtu ahdamu baiti", "L'affaire Nicolas Le Floch", "La première gamelle", "Le mariage aux épingles", 
    "Life for Life", "Lost!", "Malaya", "Meet the Protest", "Mirukî howaito no ichiya", "Mr & Mrs", "Naked Killer", 
    "Nikolaj Koppel", "Oakland Street: Rough Plumbing", "Opera and Human Sat Nav", "Paris: Part 2", 
    "Picnic Without Ants", "Pour qui fait-il bon vivre en Russie?", "Quando il gioco si fa duro", 
    "Ren's Pecs/An Abe Divided", "Roman Numeral Series IX", "Samstag", "Secret Cutting", "Shirley's Fired", 
    "Smile", "Spiel im Sommerwind", "Strohfeuer", "Taibhse le Seans", "That Man Is Mine", 
    "The Boys of Barr na Sráide", "The Devil's Playhouse", "The Gland of Rotted Apples", "The King of Curtains", 
    "The Most Beautiful Baby in Bedrock", "The Red Man's View", "The Terrible Scrap of Paper", "They Have Names", 
    "Tommy Trinder", "Trust", "Uncle's Namesakes", "Vernon Loves Carol and Cake", "Was He Justified?", 
    "Who's Your Caddy? - Part Three", "Yago no se casa", "Zzim"
]

title_mcv_freqs = [
    0.0044333334, 0.0036333334, 0.0034666667, 0.0034666667, 0.0034333332, 0.0028666668, 0.0026, 0.0023, 
    0.0017666667, 0.0016333334, 0.0015666666, 0.0011333333, 0.0011, 0.0010666667, 0.0010333334, 0.0010333334, 
    0.001, 0.00093333336, 0.00093333336, 0.0009, 0.0009, 0.00086666667, 0.00083333335, 0.00076666666, 
    0.00073333335, 0.0007, 0.00066666666, 0.00066666666, 0.00066666666, 0.00063333334, 0.00056666665, 
    0.00056666665, 0.00056666665, 0.00053333334, 0.0005, 0.00046666668, 0.00046666668, 0.00046666668, 
    0.00046666668, 0.00043333333, 0.00043333333, 0.00043333333, 0.00043333333, 0.0004, 0.0004, 0.0004, 
    0.0004, 0.0004, 0.0004, 0.00036666667, 0.00036666667, 0.00036666667, 0.00036666667, 0.00036666667, 
    0.00036666667, 0.00036666667, 0.00036666667, 0.00036666667, 0.00033333333, 0.00033333333, 0.00033333333, 
    0.00033333333, 0.00033333333, 0.00033333333, 0.0003, 0.0003, 0.0003, 0.0003, 0.0003, 0.0003, 0.0003, 
    0.0003, 0.0003, 0.00026666667, 0.00026666667, 0.00026666667, 0.00026666667, 0.00026666667, 0.00026666667, 
    0.00026666667, 0.00026666667, 0.00026666667, 0.00026666667, 0.00026666667, 0.00023333334, 0.00023333334, 
    0.00023333334, 0.00023333334, 0.00023333334, 0.00023333334, 0.00023333334, 0.00023333334, 0.00023333334, 
    0.00023333334, 0.0002, 0.0002, 0.0002, 0.0002, 0.0002, 0.0002
]

# ID Column Data
id_bounds_raw = [
    12, 25280, 53534, 79947, 106289, 131810, 154868, 180073, 207351, 232218, 257071, 280816, 306824, 331600, 
    357455, 380795, 407045, 433154, 459598, 482896, 508723, 532028, 558641, 582407, 608528, 633437, 659486, 
    683077, 707380, 733583, 757627, 778913, 803301, 827407, 852375, 878102, 902024, 928492, 953231, 979551, 
    1005587, 1033221, 1058277, 1085955, 1113329, 1140712, 1164933, 1189161, 1214358, 1240681, 1264602, 1289155, 
    1314469, 1341125, 1370231, 1395134, 1417901, 1443129, 1469222, 1492990, 1517754, 1543101, 1569015, 1594568, 
    1621824, 1646561, 1671605, 1696857, 1723117, 1750229, 1776188, 1803342, 1829023, 1854419, 1877585, 1901771, 
    1927212, 1950909, 1975558, 2001825, 2028941, 2053452, 2077466, 2104544, 2129123, 2153046, 2178934, 2204544, 
    2227031, 2252483, 2277592, 2303504, 2328091, 2353631, 2378546, 2402688, 2429510, 2454455, 2479673, 2505637, 
    2528292
]

# Shared Base Data
title_bucket_height = (1.0 - sum(title_mcv_freqs)) / (len(title_bounds) - 1)


# ==========================================
# 2. PLOT 1: TITLE COLUMN (BASIC SCALAR METHOD)
# ==========================================
def string_to_scalar_basic(s):
    val = 0.0
    for i, byte in enumerate(s.encode('utf-8', errors='ignore')[:8]):
        val += byte / (256.0 ** (i + 1))
    return val

buggy_x_vals = [string_to_scalar_basic(b) for b in title_bounds]
buggy_widths = [buggy_x_vals[i+1] - buggy_x_vals[i] for i in range(len(buggy_x_vals)-1)]
buggy_heights = [title_bucket_height] * len(buggy_widths)

plt.figure(figsize=(18, 7))
plt.bar(buggy_x_vals[:-1], buggy_heights, width=buggy_widths, align='edge', edgecolor='black', color='skyblue')
plt.xticks(buggy_x_vals, title_bounds, rotation=90, fontsize=6)
plt.ylabel(f"Frequency", fontsize=12)
plt.title("Attempted String-to-Scalar Histogram for 'title' Column", fontsize=14)
plt.tight_layout()
plt.savefig("title_scalar_histogram.png")
plt.close()

print("\n1. Generated 'title_scalar_histogram.png':")
print("   - For the conversion method, attempted to replicate the way Postgres converts, but it is extremely challenging to do it locally. This is using a basic byte-distance conversion, but it does not exactly replicate what Postgres does.")


# ==========================================
# 3. PLOT 2: TITLE COLUMN (ORDINAL EQUI-DEPTH)
# ==========================================
ordinal_x_vals = list(range(len(title_bounds)))
ordinal_widths = [1] * (len(title_bounds) - 1)

plt.figure(figsize=(18, 7))
plt.bar(ordinal_x_vals[:-1], buggy_heights, width=ordinal_widths, align='edge', edgecolor='black', color='lightgreen')
plt.xticks(ordinal_x_vals, title_bounds, rotation=90, fontsize=6)
plt.ylabel(f"Frequency (Approx. {title_bucket_height:.5f})", fontsize=12)
plt.title("Equi-Depth Histogram for 'title' Column (Dummy Spacing)", fontsize=14)
plt.xlim(0, len(title_bounds) - 1)
plt.margins(x=0)
plt.tight_layout()
plt.savefig("title_ordinal_histogram.png")
plt.close()

print("\n2. Generated 'title_ordinal_histogram.png':")
print("   - This is just a dummy equi-depth histogram, assuming that all titles are equally spaced. No, this is not the reality.")


# ==========================================
# 4. PLOT 3: TITLE COLUMN (NATIVE COLLATiON)
# ==========================================
try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    print("\nWarning: Could not set native locale. Defaulting to 'C'.")

def string_to_scalar_locale(s):
    sort_key = locale.strxfrm(s)
    key_bytes = sort_key.encode('utf-8', errors='ignore')
    val = 0.0
    for i, byte in enumerate(key_bytes[:12]):
        val += byte / (256.0 ** (i + 1))
    return val

locale_x_vals = [string_to_scalar_locale(b) for b in title_bounds]
locale_widths = [locale_x_vals[i+1] - locale_x_vals[i] for i in range(len(locale_x_vals)-1)]

plt.figure(figsize=(18, 7))
plt.bar(locale_x_vals[:-1], buggy_heights, width=locale_widths, align='edge', edgecolor='black', color='mediumpurple')
plt.xticks(locale_x_vals, title_bounds, rotation=90, fontsize=6)
plt.ylabel(f"Frequency", fontsize=12)
plt.title("Native MacOS Collation Histogram for 'title' Column", fontsize=14)
plt.tight_layout()
plt.savefig("title_native_collation_histogram.png")
plt.close()

print("\n3. Generated 'title_native_collation_histogram.png':")
print("   - This script hooks directly into the MacOS C-library 'strxfrm' function to fetch real dictionary weights.")
print("   - It applies Postgres' base-256 scalar math to those weights to map the true mathematical spacing. I am unsure if it worked or not but attempted to replicate the Postgres behavior as closely as possible.\n")


# ==========================================
# 5. PLOT 4: ID COLUMN (INTEGER DEPTH)
# ==========================================
id_bucket_height = 1.0 / (len(id_bounds_raw) - 1)
id_widths = [id_bounds_raw[i+1] - id_bounds_raw[i] for i in range(len(id_bounds_raw)-1)]
id_heights = [id_bucket_height] * len(id_widths)

plt.figure(figsize=(18, 7))
plt.bar(id_bounds_raw[:-1], id_heights, width=id_widths, align='edge', edgecolor='black', color='salmon')

plt.xticks(id_bounds_raw, [str(b) for b in id_bounds_raw], rotation=90, fontsize=6)
plt.ylabel(f"Frequency (Exact: {id_bucket_height:.2f})", fontsize=12)
plt.title("Equi-Depth Histogram for 'id' Column", fontsize=14)
plt.xlim(min(id_bounds_raw), max(id_bounds_raw))
plt.margins(x=0)
plt.tight_layout()
plt.savefig("id_histogram.png")
plt.close()

print("\n4. Generated 'id_histogram.png':")
print("   - There are no MCVs. It is an equi-depth, equi-width histogram, and it is plotted perfectly.\n")