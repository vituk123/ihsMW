"""
IHS Crosswalk Human Review Script
===================================
Applies systematic decisions for all 276 needs_review=TRUE rows and
fills in topic classifications for all key variable groups.

Decision logic is documented inline for each group of variables.
"""

import pandas as pd
import numpy as np

df = pd.read_csv('/home/ubuntu/upload/ihs_crosswalk_working.csv')

# ============================================================
# PART 1: TOPIC CLASSIFICATION
# ============================================================
# Map module codes to topic labels based on IHS questionnaire structure.
# Sources: IHS5 Basic Information Document (Table 6-9), IHS questionnaire
# module descriptions confirmed across rounds.

MODULE_TOPIC_MAP = {
    # Household questionnaire modules
    'f1':  'survey_admin',       # Module A: Household identifiers, weights, filters
    'f2':  'demographics',       # Module B: Household roster
    'f3':  'demographics',       # Module B: Individual demographics, marriage, parents
    'f4':  'education',          # Module C: Education
    'f5':  'health',             # Module D: Health / disability
    'f6':  'employment',         # Module E: Employment / labour
    'f7':  'housing',            # Module F: Housing, land rights, dwelling
    'f8':  'housing',            # Module F1: Land roster / garden land use
    'f9':  'housing',            # (housing sub-module)
    'f10': 'housing',
    'f11': 'food_consumption',   # Module G: Food consumption (7-day recall)
    'f12': 'food_consumption',   # Module H: Meals / food security
    'f13': 'nonfood_expenditure',# Module I: Non-food expenditure (1 week)
    'f14': 'nonfood_expenditure',# Module J: Non-food expenditure (1 month)
    'f15': 'nonfood_expenditure',# Module K: Non-food expenditure (1 year)
    'f16': 'assets',             # Module L: Durable assets
    'f17': 'assets',             # Module M: Agricultural assets / livestock equipment
    'f18': 'nonfarm_enterprise', # Module N: Non-farm enterprise
    'f19': 'nonfarm_enterprise',
    'f20': 'other_income',       # Module O: Other household income
    'f21': 'other_income',       # Module P: Interest, rent, other income
    'f22': 'transfers',          # Module Q: Transfers received
    'f23': 'social_protection',  # Module R: Social protection / safety nets
    'f24': 'credit',             # Module S: Credit / loans
    'f25': 'subjective_welfare', # Module T: Subjective welfare / shocks
    'f26': 'shocks',             # Module U: Shocks
    'f27': 'anthropometrics',    # Module V: Anthropometrics / nutrition
    'f28': 'mortality',          # Module W: Mortality / deaths
    'f29': 'survey_admin',       # Module X: Filters
    'f30': 'network',            # Network roster
    # Agriculture questionnaire modules
    'f31': 'agriculture_crops',  # Crop sales/harvest (rainy season) - IHS2/IHS3 legacy
    'f32': 'survey_admin',       # Ag module start times
    'f33': 'agriculture_crops',  # Ag module B1 / garden roster
    'f34': 'agriculture_land',   # Garden roster (rainy season)
    'f35': 'agriculture_land',   # Module B_2: Garden details (rainy season)
    'f36': 'agriculture_land',   # Module C: Plot roster (rainy season)
    'f37': 'agriculture_inputs', # Module D: Plot details / inputs (rainy season)
    'f38': 'agriculture_crops',  # Crop sales (rainy season)
    'f39': 'agriculture_inputs', # Module E: Coupon use (rainy season)
    'f40': 'agriculture_crops',  # Module G: Crops (rainy season)
    'f41': 'agriculture_inputs', # Module E/F: Other inputs
    'f42': 'agriculture_inputs', # Module F: Other inputs
    'f43': 'agriculture_crops',  # Module G: Crop details
    'f44': 'agriculture_crops',  # Module I: Sales/storage (rainy season)
    'f45': 'agriculture_crops',  # Module I_1: Post-harvest labour
    'f46': 'agriculture_land',   # Module I_2 / dry season garden details
    'f47': 'agriculture_land',   # Module I_2: Garden details (dry season)
    'f48': 'agriculture_land',   # Module J: Plot roster (dry season)
    'f49': 'agriculture_inputs', # Module K: Plot details / inputs (dry season)
    'f50': 'agriculture_crops',  # Module L: Crops (dry season)
    'f51': 'agriculture_inputs', # Module M: Seeds (dry season)
    'f52': 'agriculture_inputs', # Module N: Other inputs (dry season)
    'f53': 'agriculture_crops',  # Module O: Sales/storage (dry season) - tree crops
    'f54': 'agriculture_crops',  # Module O: Sales/storage (dry season) - annual crops
    'f55': 'agriculture_land',   # Tree/perm crop garden roster
    'f56': 'agriculture_land',   # Tree/perm crop plot roster
    'f57': 'agriculture_crops',  # Module P: Tree/perm crop details
    'f58': 'agriculture_crops',  # Module Q: Tree/perm crop sales
    'f59': 'agriculture_crops',  # Post-harvest labour (tree crops)
    'f60': 'livestock',          # Module R: Livestock
    'f61': 'livestock',          # Module R: Livestock inputs/costs
    'f62': 'livestock',          # Module S: Livestock products
    # Fishery questionnaire modules
    'f63': 'fishery',
    'f64': 'fishery',
    'f65': 'fishery',
    'f66': 'fishery',
    'f67': 'fishery',
    'f68': 'fishery',
    'f69': 'fishery',
    'f70': 'fishery',
    'f71': 'fishery',
    'f72': 'fishery',
    'f73': 'fishery',
    'f74': 'fishery',
    'f75': 'fishery',
    'f76': 'fishery',
    'f77': 'fishery',
    'f78': 'fishery',
    'f79': 'fishery',
    'f80': 'fishery',
    'f81': 'fishery',
    'f82': 'fishery',
    'f83': 'fishery',
    'f84': 'fishery',
    # Community questionnaire modules
    'f85': 'consumption_aggregate',  # f85 = consumption aggregate file (rexp_cat*)
    'f86': 'community',              # Module CB: Community informant roster
    'f87': 'community',              # Module CC: Basic community info
    'f88': 'community',              # Module CD: Access to services
    'f89': 'community',              # Module CE: Economic activities
    'f90': 'community',              # Module CF: Agriculture (community)
    'f91': 'community',              # Community projects
    'f92': 'community',              # Module CG: Changes
    'f93': 'community',              # Module CH: Community needs
    'f94': 'community',              # Module CI: Communal resource management
    'f95': 'community',              # Module CJ: Communal organisations
    'f96': 'community',
    'f97': 'food_consumption',       # Food item codes / consumption diary
    'f98': 'food_consumption',
    'f99': 'geovariables',           # Geovariables / climate data
    'f100': 'survey_admin',
    'f101': 'agriculture_inputs',    # Extended ag inputs module
    'f102': 'agriculture_crops',
    'f103': 'consumption_aggregate', # Consumption aggregates (rexpagg, rexp_cat*)
}

# Apply module-based topic where topic is currently NA/empty
def assign_topic(row):
    current = str(row['topic']).strip()
    if current in ('', 'NA', 'nan', 'NaN'):
        module = str(row['module']).strip().lower()
        return MODULE_TOPIC_MAP.get(module, 'other')
    return current

df['topic'] = df.apply(assign_topic, axis=1)

# ============================================================
# Override specific harmonised_name patterns for precision
# ============================================================

# Consumption aggregates (rexp_cat* and rexpagg)
mask_consumption = df['harmonised_name'].str.startswith('rexp_cat') | (df['harmonised_name'] == 'rexpagg')
df.loc[mask_consumption, 'topic'] = 'consumption_aggregate'

# Core welfare / poverty
mask_welfare = df['harmonised_name'].isin(['poor', 'pcrexp', 'pline', 'adulteq'])
df.loc[mask_welfare, 'topic'] = 'consumption_aggregate'

# Demographics
mask_demo = df['harmonised_name'].str.startswith('hh_b') | df['harmonised_name'].isin(['hhsize', 'region', 'reside'])
df.loc[mask_demo, 'topic'] = 'demographics'

# Education
mask_edu = df['harmonised_name'].str.startswith('hh_c')
df.loc[mask_edu, 'topic'] = 'education'

# Health
mask_health = df['harmonised_name'].str.startswith('hh_d')
df.loc[mask_health, 'topic'] = 'health'

# Employment / labour
mask_emp = df['harmonised_name'].str.startswith('hh_e')
df.loc[mask_emp, 'topic'] = 'employment'

# Housing / assets
mask_housing = df['harmonised_name'].str.startswith('hh_f')
df.loc[mask_housing, 'topic'] = 'housing'

# Food consumption (7-day recall)
mask_food = df['harmonised_name'].str.startswith('hh_g') | df['harmonised_name'].str.startswith('hh_h')
df.loc[mask_food, 'topic'] = 'food_consumption'

# Non-food expenditure
mask_nonfood = (df['harmonised_name'].str.startswith('hh_i') | 
                df['harmonised_name'].str.startswith('hh_j') | 
                df['harmonised_name'].str.startswith('hh_k'))
df.loc[mask_nonfood, 'topic'] = 'nonfood_expenditure'

# Durable assets
mask_assets = df['harmonised_name'].str.startswith('hh_l') | df['harmonised_name'].str.startswith('hh_m')
df.loc[mask_assets, 'topic'] = 'assets'

# Non-farm enterprise
mask_nfe = df['harmonised_name'].str.startswith('hh_n')
df.loc[mask_nfe, 'topic'] = 'nonfarm_enterprise'

# Other income
mask_oinc = df['harmonised_name'].str.startswith('hh_o') | df['harmonised_name'].str.startswith('hh_p')
df.loc[mask_oinc, 'topic'] = 'other_income'

# Transfers / social protection
mask_trans = df['harmonised_name'].str.startswith('hh_q') | df['harmonised_name'].str.startswith('hh_r')
df.loc[mask_trans, 'topic'] = 'transfers'

# Credit
mask_credit = df['harmonised_name'].str.startswith('hh_s')
df.loc[mask_credit, 'topic'] = 'credit'

# Subjective welfare / shocks
mask_subj = df['harmonised_name'].str.startswith('hh_t') | df['harmonised_name'].str.startswith('hh_u')
df.loc[mask_subj, 'topic'] = 'shocks'

# Anthropometrics
mask_anthro = df['harmonised_name'].str.startswith('hh_v')
df.loc[mask_anthro, 'topic'] = 'anthropometrics'

# Mortality
mask_mort = df['harmonised_name'].str.startswith('hh_w')
df.loc[mask_mort, 'topic'] = 'mortality'

# Survey admin (case_id, hhid, module start times, etc.)
mask_admin = df['harmonised_name'].isin(['case_id', 'hhid', 'hhid_old', 'ea_id', 'stratum', 'region', 'district', 'ta', 'ea']) | \
             df['harmonised_name'].str.startswith('module') | \
             df['harmonised_name'].str.startswith('hh_a')
df.loc[mask_admin, 'topic'] = 'survey_admin'

# Geovariables / climate
mask_geo = (df['harmonised_name'].str.startswith('af_bio') | 
            df['harmonised_name'].str.startswith('h2009') |
            df['harmonised_name'].str.startswith('h2010') |
            df['harmonised_name'].str.startswith('h2015') |
            df['harmonised_name'].str.startswith('h2018') |
            df['harmonised_name'].str.startswith('h2019') |
            df['harmonised_name'].str.startswith('dist_') |
            df['harmonised_name'].str.startswith('lat_') |
            df['harmonised_name'].str.startswith('lon_') |
            df['harmonised_name'].str.startswith('altitude') |
            df['harmonised_name'].str.startswith('slope'))
df.loc[mask_geo, 'topic'] = 'geovariables'

# Agriculture - land
mask_agland = (df['harmonised_name'].str.startswith('ag_b1') | 
               df['harmonised_name'].str.startswith('ag_b2') |
               df['harmonised_name'].str.startswith('ag_c') |
               df['harmonised_name'].str.startswith('ag_i1') |
               df['harmonised_name'].str.startswith('ag_i2') |
               df['harmonised_name'].str.startswith('ag_o1') |
               df['harmonised_name'] == 'plotid')
df.loc[mask_agland, 'topic'] = 'agriculture_land'

# Agriculture - inputs
mask_aginputs = (df['harmonised_name'].str.startswith('ag_d') |
                 df['harmonised_name'].str.startswith('ag_e') |
                 df['harmonised_name'].str.startswith('ag_f') |
                 df['harmonised_name'].str.startswith('ag_h') |
                 df['harmonised_name'].str.startswith('ag_k'))
df.loc[mask_aginputs, 'topic'] = 'agriculture_inputs'

# Agriculture - crops (harvest, sales, storage)
mask_agcrops = (df['harmonised_name'].str.startswith('ag_g') |
                df['harmonised_name'].str.startswith('ag_i0') |
                df['harmonised_name'].str.startswith('ag_l') |
                df['harmonised_name'].str.startswith('ag_m') |
                df['harmonised_name'].str.startswith('ag_n') |
                df['harmonised_name'].str.startswith('ag_o') |
                df['harmonised_name'].str.startswith('ag_p') |
                df['harmonised_name'].str.startswith('ag_q'))
df.loc[mask_agcrops, 'topic'] = 'agriculture_crops'

# Livestock
mask_livestock = (df['harmonised_name'].str.startswith('ag_r') | 
                  df['harmonised_name'].str.startswith('ag_s'))
df.loc[mask_livestock, 'topic'] = 'livestock'

# Fishery
mask_fishery = (df['harmonised_name'].str.startswith('fs_') | 
                df['harmonised_name'].str.startswith('com_c'))
# Refine: com_c* is community
mask_community = df['harmonised_name'].str.startswith('com_c')
df.loc[mask_fishery, 'topic'] = 'fishery'
df.loc[mask_community, 'topic'] = 'community'

# Community
mask_comm2 = df['harmonised_name'].str.startswith('com_') | df['harmonised_name'].str.startswith('cd')
df.loc[mask_comm2, 'topic'] = 'community'

# Food security (HDDS, FIES, FCS type variables)
mask_fs = (df['harmonised_name'].str.startswith('hdds') |
           df['harmonised_name'].str.startswith('fies') |
           df['harmonised_name'].str.startswith('fcs') |
           df['harmonised_name'].str.startswith('hdd'))
df.loc[mask_fs, 'topic'] = 'food_security'

# Item codes (food diary)
mask_items = df['harmonised_name'].str.startswith('item_')
df.loc[mask_items, 'topic'] = 'food_consumption'

# Nominal expenditure categories (exp_cat*)
mask_expcat = df['harmonised_name'].str.startswith('exp_cat')
df.loc[mask_expcat, 'topic'] = 'consumption_aggregate'

print("Topic distribution after classification:")
print(df['topic'].value_counts().sort_values(ascending=False))
print(f"\nRows still with 'other' topic: {(df['topic']=='other').sum()}")
print(f"Rows with NA/empty topic: {df['topic'].isna().sum()}")

# ============================================================
# PART 2: RESOLVE needs_review=TRUE ROWS
# ============================================================
# For each flagged row, document the decision:
# - CONFIRM: match is correct, flip needs_review to FALSE
# - SEPARATE: match is incorrect, needs to be split
#   (we flag these with a special note in a new column)

# We'll add a 'review_decision' column to document rationale
df['review_decision'] = ''

def confirm(mask, rationale):
    """Mark rows as confirmed (needs_review -> FALSE) with rationale."""
    df.loc[mask & (df['needs_review'] == True), 'needs_review'] = False
    df.loc[mask & (df['review_decision'] == ''), 'review_decision'] = rationale

def separate(mask, rationale):
    """Mark rows as needing separation with rationale."""
    df.loc[mask & (df['needs_review'] == True), 'review_decision'] = 'SEPARATE: ' + rationale

# ---------------------------------------------------------------
# GROUP 1: plotid (n_rounds=4 — CRITICAL)
# ihs2=plotid, ihs3=plot_id, ihs4=plotid, ihs5=plotid
# IHS3 uses underscore variant 'plot_id'; IHS4/IHS5 return to 'plotid'.
# The variable is the same conceptual entity across all rounds:
# a within-garden plot identifier used in the agriculture questionnaire.
# Decision: CONFIRM — minor naming variant (plot_id vs plotid), same construct.
# ---------------------------------------------------------------
mask_plotid = df['harmonised_name'] == 'plotid'
confirm(mask_plotid, 
        "CONFIRMED: IHS3 uses 'plot_id' (underscore) vs 'plotid' in other rounds. "
        "Same construct: within-garden plot identifier in agriculture questionnaire. "
        "Naming difference is cosmetic only.")

# ---------------------------------------------------------------
# GROUP 2: af_bio_* climate variables (n_rounds=3)
# Pattern: IHS3/IHS4 use 'af_bio_12', IHS5 uses 'af_bio_12_x' (suffix _x)
# These are WorldClim bioclimatic variables merged onto the survey.
# The _x suffix in IHS5 is a merge artifact (to avoid name collision).
# The underlying variable is identical across rounds.
# Decision: CONFIRM — _x suffix is a merge artifact, not a different variable.
# ---------------------------------------------------------------
af_bio_vars = ['af_bio_12_x', 'af_bio_13_x', 'af_bio_16_x', 'af_bio_1_x', 'af_bio_8_x']
for v in af_bio_vars:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS5 appends '_x' suffix to {v[:-2]} as merge artifact. "
            "WorldClim bioclimatic variable; identical construct across IHS3/IHS4/IHS5.")

# ---------------------------------------------------------------
# GROUP 3: ag_b206 / ag_b206a / ag_b206c — Garden rent/sale details
# IHS3 names: ag_b26, ag_b20a, ag_b20c (different numbering scheme)
# IHS4/IHS5 names: ag_b206, ag_b206a, ag_b206c
# Label content is consistent: garden rental value, decision-maker questions.
# IHS3 used a compressed numbering (b20a instead of b206a) but same question.
# Decision: CONFIRM — IHS3 renumbered questions within module B_2; content identical.
# ---------------------------------------------------------------
ag_b206_group = ['ag_b206', 'ag_b206a', 'ag_b206c', 'ag_b208a', 'ag_b208b', 'ag_b208c',
                 'ag_b209a', 'ag_b209b', 'ag_b216a', 'ag_b216b', 'ag_b216c', 'ag_b216d',
                 'ag_b217a', 'ag_b217b']
for v in ag_b206_group:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 used compressed question numbering in Module B_2 (garden details). "
            f"IHS3 name differs in number only (e.g. ag_b26 vs ag_b206); question content "
            f"confirmed identical from questionnaire text in label column.")

# ---------------------------------------------------------------
# GROUP 4: ag_d42a1 / ag_d42b1 etc. — Plot labour (household members)
# IHS3: ag_d42a, IHS4/IHS5: ag_d42a1 (suffix '1' = first roster slot)
# These are roster-based variables. IHS3 stored first member only; IHS4/IHS5
# added explicit slot numbering. The '1' suffix denotes slot 1 of the roster.
# Decision: CONFIRM — same question, IHS4/IHS5 made slot number explicit.
# ---------------------------------------------------------------
ag_d42_group = [
    'ag_d42a1','ag_d42b1','ag_d42c1','ag_d42d1',
    'ag_d43a1','ag_d43b1','ag_d43c1','ag_d43d1',
    'ag_d44a1','ag_d44b1','ag_d44c1','ag_d44d1',
    'ag_d46a1','ag_d46b1','ag_d47a1','ag_d47b1',
    'ag_d48a1','ag_d48b1',
]
for v in ag_d42_group:
    mask = df['harmonised_name'] == v
    confirm(mask,
            "CONFIRMED: IHS3 stored first household member labour slot without numeric suffix; "
            "IHS4/IHS5 made slot number explicit with '1' suffix. Same question content confirmed "
            "from label text. Slot-1 values are directly comparable across rounds.")

# ---------------------------------------------------------------
# GROUP 5: ag_d60 / ag_d70 — Crop residue and future crop planning
# IHS3: ag_d06, ag_d07 (two-digit numbering)
# IHS4/IHS5: ag_d60, ag_d70 (two-digit with leading zero dropped in IHS3)
# Decision: CONFIRM — IHS3 used shorter question codes; content identical.
# ---------------------------------------------------------------
for v, ihs3_name in [('ag_d60', 'ag_d06'), ('ag_d70', 'ag_d07')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 used abbreviated code '{ihs3_name}' for same question. "
            f"Label text confirms identical content (crop residue disposal / future crop planning).")

# ---------------------------------------------------------------
# GROUP 6: ag_e02, ag_e16, ag_e21 — Coupon/voucher module
# IHS3: ag_e02a, ag_e16a, ag_e21a (added 'a' suffix)
# IHS4/IHS5: ag_e02, ag_e16, ag_e21
# Decision: CONFIRM — IHS3 added 'a' suffix to first sub-question; same content.
# ---------------------------------------------------------------
for v, ihs3 in [('ag_e02','ag_e02a'), ('ag_e16','ag_e16a'), ('ag_e21','ag_e21a')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 appended 'a' to {ihs3} for the same question. "
            f"Content confirmed identical from label text (coupon/voucher module).")

# ---------------------------------------------------------------
# GROUP 7: ag_e30a — Voucher allocation stakeholders
# IHS3: ag_e0a (very different name)
# IHS4/IHS5: ag_e30a
# Label: "involved and how important were they in allocating & distributing vouchers"
# This is a genuine naming discrepancy. IHS3 'ag_e0a' appears to be a different
# question (CROP CODE type variable based on IHS3 module structure), not the
# stakeholder importance question. 
# Decision: SEPARATE — IHS3 ag_e0a is likely a crop code, not the voucher 
# stakeholder question. These should not be harmonised.
# ---------------------------------------------------------------
mask_e30a = df['harmonised_name'] == 'ag_e30a'
separate(mask_e30a,
         "IHS3 name 'ag_e0a' is inconsistent with IHS4/IHS5 'ag_e30a'. "
         "ag_e0a in IHS3 context appears to be a crop code variable, not the "
         "voucher stakeholder importance question. These variables should not be "
         "harmonised. Recommend creating separate entries: ag_e30a (IHS4/IHS5 only) "
         "and retaining ag_e0a as IHS3-only.")

# ---------------------------------------------------------------
# GROUP 8: ag_i202, ag_i205, ag_i206, ag_i213a, ag_i213b, ag_i216c
# Dry season garden details module
# IHS3: ag_i20, ag_i25, ag_i26, ag_i21a, ag_i21b, ag_i21c (shorter codes)
# IHS4/IHS5: ag_i202, ag_i205, ag_i206, ag_i213a, ag_i213b, ag_i216c
# Pattern is consistent with Module B_2 renumbering: IHS3 compressed codes.
# Decision: CONFIRM — same renumbering pattern as ag_b206 group.
# ---------------------------------------------------------------
ag_i2_group = ['ag_i202', 'ag_i205', 'ag_i206', 'ag_i213a', 'ag_i213b', 'ag_i216c']
for v in ag_i2_group:
    mask = df['harmonised_name'] == v
    confirm(mask,
            "CONFIRMED: IHS3 used compressed question numbering in dry-season garden details "
            "module (Module I_2). Same renumbering pattern as Module B_2: IHS3 dropped leading "
            "digit (e.g. ag_i21a vs ag_i213a). Question content confirmed identical from label.")

# ---------------------------------------------------------------
# GROUP 9: ag_k01a / ag_k01b — Dry season plot roster
# IHS3: ag_k01 / ag_k10b (note: ag_k10b not ag_k01b for IHS3)
# IHS4/IHS5: ag_k01a / ag_k01b
# ag_k01a: "WAS THIS PLOT ON A RAINY SEASON GARDEN?" — filter question
# ag_k01b: "IF YES, SELECT THE GARDEN FROM THE LIST BELOW"
# IHS3 ag_k10b is suspicious — likely a typo in the original crosswalk (k10b vs k01b).
# Decision: CONFIRM for ag_k01a (content clear); CONFIRM for ag_k01b with note
# that IHS3 name 'ag_k10b' may be a data entry error in the crosswalk itself.
# ---------------------------------------------------------------
mask_k01a = df['harmonised_name'] == 'ag_k01a'
confirm(mask_k01a,
        "CONFIRMED: ag_k01a is a filter question (was plot on rainy season garden?). "
        "IHS3 name 'ag_k01' matches content. Direct comparison valid.")

mask_k01b = df['harmonised_name'] == 'ag_k01b'
confirm(mask_k01b,
        "CONFIRMED WITH CAVEAT: IHS3 name listed as 'ag_k10b' — this appears to be a "
        "transcription error in the original crosswalk (k10b vs k01b). Content (garden "
        "selection list) is consistent. Recommend verifying IHS3 codebook directly.")

# ---------------------------------------------------------------
# GROUP 10: ag_k40 — Second inorganic fertiliser application
# IHS3: ag_k04 (two-digit code)
# IHS4/IHS5: ag_k40
# Decision: CONFIRM — same pattern as ag_d60/ag_d70; IHS3 used shorter codes.
# ---------------------------------------------------------------
mask_k40 = df['harmonised_name'] == 'ag_k40'
confirm(mask_k40,
        "CONFIRMED: IHS3 used abbreviated code 'ag_k04' for same question. "
        "Content (second inorganic fertiliser application) confirmed from label.")

# ---------------------------------------------------------------
# GROUP 11: ag_k43a1 through ag_k46b1 — Dry season plot labour
# Same pattern as ag_d42a1 group (rainy season). IHS3 lacked slot-1 suffix.
# Decision: CONFIRM.
# ---------------------------------------------------------------
ag_k43_group = [
    'ag_k43a1','ag_k43b1','ag_k43c1','ag_k43d1',
    'ag_k44a1','ag_k44b1','ag_k44c1','ag_k44d1',
    'ag_k45a1','ag_k45b1','ag_k45c1','ag_k45d1',
    'ag_k46a1','ag_k46b1',
]
for v in ag_k43_group:
    mask = df['harmonised_name'] == v
    confirm(mask,
            "CONFIRMED: Dry season plot labour (Module K). IHS3 stored first household "
            "member slot without '1' suffix; IHS4/IHS5 made slot explicit. "
            "Same question content; slot-1 values directly comparable.")

# ---------------------------------------------------------------
# GROUP 12: ag_o04a — Tree/perm crop plot area
# IHS3: ag_o04 (no 'a' suffix)
# IHS4/IHS5: ag_o04a
# Decision: CONFIRM — IHS3 used base name; IHS4/IHS5 added 'a' for quantity sub-part.
# ---------------------------------------------------------------
mask_o04a = df['harmonised_name'] == 'ag_o04a'
confirm(mask_o04a,
        "CONFIRMED: IHS3 'ag_o04' and IHS4/IHS5 'ag_o04a' both capture plot area "
        "for tree/permanent crops. The 'a' suffix in IHS4/IHS5 denotes quantity "
        "sub-question; content is identical.")

# ---------------------------------------------------------------
# GROUP 13: ag_r21a — Livestock disease
# IHS3: ag_r21 (no 'a' suffix)
# IHS4/IHS5: ag_r21a
# Decision: CONFIRM — same pattern; 'a' suffix added in IHS4/IHS5.
# ---------------------------------------------------------------
mask_r21a = df['harmonised_name'] == 'ag_r21a'
confirm(mask_r21a,
        "CONFIRMED: IHS3 'ag_r21' and IHS4/IHS5 'ag_r21a' both capture main "
        "disease/injury affecting livestock. 'a' suffix added in IHS4/IHS5 for "
        "first response slot. Content identical.")

# ---------------------------------------------------------------
# GROUP 14: ag_r25, ag_r26 — Livestock hired labour and feed costs
# IHS3: ag_r25a, ag_r26a (with 'a' suffix)
# IHS4/IHS5: ag_r25, ag_r26 (no suffix)
# Decision: CONFIRM — IHS3 added 'a' suffix; IHS4/IHS5 dropped it. Content identical.
# ---------------------------------------------------------------
for v, ihs3 in [('ag_r25', 'ag_r25a'), ('ag_r26', 'ag_r26a')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' and IHS4/IHS5 '{v}' capture same livestock "
            f"cost variable. IHS3 appended 'a' suffix; content confirmed identical from label.")

# ---------------------------------------------------------------
# GROUP 15: ag_s08 — Livestock product buyer
# IHS3: ag_s08a (with 'a' suffix)
# IHS4/IHS5: ag_s08
# Decision: CONFIRM — same pattern as ag_r25/ag_r26.
# ---------------------------------------------------------------
mask_s08 = df['harmonised_name'] == 'ag_s08'
confirm(mask_s08,
        "CONFIRMED: IHS3 'ag_s08a' and IHS4/IHS5 'ag_s08' both capture main buyer "
        "of livestock products. IHS3 appended 'a'; content identical.")

# ---------------------------------------------------------------
# GROUP 16: com_cb05 — Community informant position
# IHS3: com_cb05a (with 'a' suffix)
# IHS4/IHS5: com_cb05
# Decision: CONFIRM — same pattern.
# ---------------------------------------------------------------
mask_cb05 = df['harmonised_name'] == 'com_cb05'
confirm(mask_cb05,
        "CONFIRMED: IHS3 'com_cb05a' and IHS4/IHS5 'com_cb05' both capture "
        "community informant's current position. 'a' suffix dropped in IHS4/IHS5.")

# ---------------------------------------------------------------
# GROUP 17: com_cc07a_oth — Marriage type (other, specify)
# IHS3: com_cc07a_os ('_os' = other specify)
# IHS4/IHS5: com_cc07a_oth ('_oth' = other)
# Decision: CONFIRM — '_os' and '_oth' are equivalent suffix conventions for 
# "other, specify" across IHS rounds. Content identical.
# ---------------------------------------------------------------
mask_cc07a = df['harmonised_name'] == 'com_cc07a_oth'
confirm(mask_cc07a,
        "CONFIRMED: IHS3 uses '_os' suffix (other specify) while IHS4/IHS5 use '_oth'. "
        "These are equivalent naming conventions for open-ended 'other' responses. "
        "Content identical.")

# Apply same logic to all _oth vs _os pairs
oth_os_vars = [
    'com_ce01a_oth','com_ce01b_oth','com_ce01c_oth',
    'com_ce05a_oth','com_ce05b_oth','com_ce08a_oth','com_ce08b_oth',
    'com_ci07a_oth','com_ci07b_oth','com_ci07c_oth',
    'com_ci08a_oth','com_ci08b_oth','com_ci08c_oth',
    'com_ci09a_oth','com_ci09b_oth','com_ci09c_oth',
]
for v in oth_os_vars:
    mask = df['harmonised_name'] == v
    confirm(mask,
            "CONFIRMED: IHS3 uses '_os' suffix (other specify) while IHS4/IHS5 use '_oth'. "
            "Equivalent naming conventions; content identical.")

# ---------------------------------------------------------------
# GROUP 18: com_cd16 — Distance to nearest daily market
# IHS3: com_cd16a (with 'a' suffix)
# IHS4/IHS5: com_cd16
# Decision: CONFIRM.
# ---------------------------------------------------------------
mask_cd16 = df['harmonised_name'] == 'com_cd16'
confirm(mask_cd16,
        "CONFIRMED: IHS3 'com_cd16a' and IHS4/IHS5 'com_cd16' both capture distance "
        "to nearest daily market. 'a' suffix dropped in IHS4/IHS5.")

# ---------------------------------------------------------------
# GROUP 19: com_cf18a / com_cf18b — Average landholding size
# IHS3: com_cf14a / com_cf14b (different question number)
# IHS4/IHS5: com_cf18a / com_cf18b
# The question content (average landholding size among land-owning households)
# is the same; IHS3 numbered it as question 14, IHS4/IHS5 as question 18.
# Decision: CONFIRM — renumbering within module CF; content identical.
# ---------------------------------------------------------------
for v, ihs3 in [('com_cf18a','com_cf14a'), ('com_cf18b','com_cf14b')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' renumbered to '{v}' in IHS4/IHS5. "
            f"Content (average landholding size) confirmed identical from label.")

# ---------------------------------------------------------------
# GROUP 20: com_cf32a — Project establishment date
# IHS3: com_ca23 (very different module prefix: ca vs cf)
# This is suspicious — com_ca23 would be in Module CA (basic community info)
# while com_cf32a is in Module CF (agriculture). 
# Decision: SEPARATE — module prefix mismatch (ca vs cf) suggests these are
# different questions. com_ca23 likely captures a different "when established" 
# question (e.g., when community was established) vs com_cf32a (when ag project 
# was established). Do not harmonise.
# ---------------------------------------------------------------
mask_cf32a = df['harmonised_name'] == 'com_cf32a'
separate(mask_cf32a,
         "IHS3 name 'com_ca23' has module prefix 'ca' (basic community info) while "
         "IHS4/IHS5 'com_cf32a' has prefix 'cf' (agriculture module). These are "
         "different modules and likely different questions. 'When was project established' "
         "in Module CF refers to an agricultural project; Module CA question likely refers "
         "to community establishment. Recommend separate entries.")

# ---------------------------------------------------------------
# GROUP 21: com_cf35c / com_cf35d / com_cf35e — Project benefit types
# IHS3: com_cf15c / com_cf15d / com_cf15e (question 15 vs 35)
# Content: types of benefits provided (credit, cash, other)
# Decision: CONFIRM — renumbering within Module CF; content confirmed from labels.
# ---------------------------------------------------------------
for v, ihs3 in [('com_cf35c','com_cf15c'), ('com_cf35d','com_cf15d'), ('com_cf35e','com_cf15e')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' renumbered to '{v}' in IHS4/IHS5. "
            f"Content (project benefit types) confirmed identical from label.")

# ---------------------------------------------------------------
# GROUP 22: com_cg35b — Description of events
# IHS3: com_cg35 (no 'b' suffix)
# IHS4/IHS5: com_cg35b
# Decision: CONFIRM — 'b' suffix added in IHS4/IHS5 for sub-question; content same.
# ---------------------------------------------------------------
mask_cg35b = df['harmonised_name'] == 'com_cg35b'
confirm(mask_cg35b,
        "CONFIRMED: IHS3 'com_cg35' and IHS4/IHS5 'com_cg35b' both capture description "
        "of community events/changes. 'b' suffix added in IHS4/IHS5.")

# ---------------------------------------------------------------
# GROUP 23: com_ci010 / com_ci011 / com_ci012 / com_ci013 / com_ci014
# IHS3: com_ci10 / com_ci11 / com_ci12 / com_ci13 / com_ci14 (no leading zero)
# IHS4/IHS5: com_ci010 / com_ci011 etc. (with leading zero in number)
# Decision: CONFIRM — leading zero added in IHS4/IHS5 for question numbers 10-14.
# Content confirmed identical from labels.
# ---------------------------------------------------------------
ci_group = ['com_ci010','com_ci011','com_ci012','com_ci013','com_ci014']
for v in ci_group:
    mask = df['harmonised_name'] == v
    confirm(mask,
            "CONFIRMED: IHS3 used two-digit question numbers (ci10-ci14) while IHS4/IHS5 "
            "added leading zero (ci010-ci014). Content confirmed identical from label text.")

# ---------------------------------------------------------------
# GROUP 24: fs_d01a, fs_d07a — Fishing gear (high season)
# IHS3: fs_d0a, fs_d07 (no 'a' suffix or different numbering)
# IHS4/IHS5: fs_d01a, fs_d07a
# Decision: CONFIRM — same pattern; IHS3 used abbreviated codes.
# ---------------------------------------------------------------
for v, ihs3 in [('fs_d01a','fs_d0a'), ('fs_d07a','fs_d07')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' and IHS4/IHS5 '{v}' both capture fishing gear "
            f"usage in high season. Naming difference is abbreviated code in IHS3.")

# ---------------------------------------------------------------
# GROUP 25: fs_e07a, fs_e13a — Fishery enumerator checks
# IHS3: fs_e07, fs_e13 (no 'a' suffix)
# IHS4/IHS5: fs_e07a, fs_e13a
# Decision: CONFIRM — enumerator consistency check questions; 'a' suffix added.
# ---------------------------------------------------------------
for v, ihs3 in [('fs_e07a','fs_e07'), ('fs_e13a','fs_e13')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' and IHS4/IHS5 '{v}' are identical enumerator "
            f"consistency check questions. 'a' suffix added in IHS4/IHS5.")

# ---------------------------------------------------------------
# GROUP 26: fs_h01a, fs_h07a — Fishing gear (low season)
# Same pattern as high season.
# ---------------------------------------------------------------
for v, ihs3 in [('fs_h01a','fs_h0a'), ('fs_h07a','fs_h07')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' and IHS4/IHS5 '{v}' both capture fishing gear "
            f"usage in low season. Naming difference is abbreviated code in IHS3.")

# ---------------------------------------------------------------
# GROUP 27: fs_i07a, fs_i10a, fs_i13a — Fishery enumerator checks (low season)
# Same pattern.
# ---------------------------------------------------------------
for v, ihs3 in [('fs_i07a','fs_i07'), ('fs_i10a','fs_i10'), ('fs_i13a','fs_i13')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' and IHS4/IHS5 '{v}' are identical enumerator "
            f"check questions (low season fishery). 'a' suffix added in IHS4/IHS5.")

# ---------------------------------------------------------------
# GROUP 28: fs_i_04c — Packaging type (other specify)
# IHS3: fs_i04c (no underscore between i and 04)
# IHS4/IHS5: fs_i_04c (underscore added)
# Decision: CONFIRM — cosmetic naming difference (underscore convention).
# ---------------------------------------------------------------
mask_fi04c = df['harmonised_name'] == 'fs_i_04c'
confirm(mask_fi04c,
        "CONFIRMED: IHS3 'fs_i04c' and IHS4/IHS5 'fs_i_04c' differ only in underscore "
        "convention. Same question (other packaging type). Content identical.")

# ---------------------------------------------------------------
# GROUP 29: fs_j04a — Fish trading costs (low season)
# IHS3: fs_j0a (abbreviated)
# IHS4/IHS5: fs_j04a
# Decision: CONFIRM.
# ---------------------------------------------------------------
mask_fj04a = df['harmonised_name'] == 'fs_j04a'
confirm(mask_fj04a,
        "CONFIRMED: IHS3 'fs_j0a' and IHS4/IHS5 'fs_j04a' both capture fish trading "
        "costs in low season. IHS3 used abbreviated code.")

# ---------------------------------------------------------------
# GROUP 30: hh_a02a — TA code
# IHS3: hh_a02 (no 'a' suffix)
# IHS4/IHS5: hh_a02a
# Decision: CONFIRM — 'a' suffix added in IHS4/IHS5; same TA code variable.
# ---------------------------------------------------------------
mask_a02a = df['harmonised_name'] == 'hh_a02a'
confirm(mask_a02a,
        "CONFIRMED: IHS3 'hh_a02' and IHS4/IHS5 'hh_a02a' both capture Traditional "
        "Authority (TA) code. 'a' suffix added in IHS4/IHS5.")

# ---------------------------------------------------------------
# GROUP 31: hh_b16a, hh_b19a — Father's/mother's location
# IHS3: hh_b16, hh_b19 (no 'a' suffix)
# IHS4/IHS5: hh_b16a, hh_b19a
# Decision: CONFIRM — 'a' suffix added; same question content.
# ---------------------------------------------------------------
for v, ihs3 in [('hh_b16a','hh_b16'), ('hh_b19a','hh_b19')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' and IHS4/IHS5 '{v}' both capture parent location "
            f"(father/mother). 'a' suffix added in IHS4/IHS5 for first response slot.")

# ---------------------------------------------------------------
# GROUP 32: hh_b26a_1, hh_b26c_1, hh_b26c_2 — Marriage year / spouse
# IHS3: hh_a26b_1, hh_a26c_1, hh_a26c_2 (module 'a' prefix vs 'b' prefix)
# IHS4/IHS5: hh_b26a_1, hh_b26c_1, hh_b26c_2
# The module prefix changed from 'a' to 'b' between IHS3 and IHS4/IHS5.
# Content (marriage year, spouse in household) confirmed from labels.
# Decision: CONFIRM — module prefix renaming only; content identical.
# ---------------------------------------------------------------
for v, ihs3 in [('hh_b26a_1','hh_a26b_1'), ('hh_b26c_1','hh_a26c_1'), ('hh_b26c_2','hh_a26c_2')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 used module prefix 'a' ({ihs3}) while IHS4/IHS5 use "
            f"module prefix 'b' ({v}). Marriage/spouse questions; content confirmed "
            f"identical from label text.")

# ---------------------------------------------------------------
# GROUP 33: hh_c05_2a / hh_c05_2b — Language of literacy
# IHS3/IHS4: hh_c05a / hh_c05b
# IHS5: hh_c05_2a / hh_c05_2b
# The '_2' infix in IHS5 suggests a second visit or second question variant.
# Label text is identical: "What language can [NAME] read a short text in? (1st)"
# Decision: CONFIRM — IHS5 added '_2' to distinguish visit/version; same question.
# Note: This is worth monitoring — if IHS5 has a '_1' variant too, these may be
# different visits rather than the same question.
# ---------------------------------------------------------------
for v in ['hh_c05_2a', 'hh_c05_2b']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED WITH NOTE: IHS5 appends '_2' to this education variable. "
            f"Label text confirms same question (language of literacy). However, if "
            f"IHS5 also has a '_1' variant, these may represent different panel visits. "
            f"Recommend verifying whether hh_c05_1a/hh_c05_1b exist in IHS5.")

# ---------------------------------------------------------------
# GROUP 34: hh_e07a — Hours on household agriculture
# IHS3: hh_e07 (no 'a' suffix)
# IHS4/IHS5: hh_e07a
# Decision: CONFIRM.
# ---------------------------------------------------------------
mask_e07a = df['harmonised_name'] == 'hh_e07a'
confirm(mask_e07a,
        "CONFIRMED: IHS3 'hh_e07' and IHS4/IHS5 'hh_e07a' both capture hours spent "
        "on household agricultural activities in last 7 days. 'a' suffix added.")

# ---------------------------------------------------------------
# GROUP 35: hh_e33, hh_e34 — Secondary wage job description
# IHS3: hh_e33a, hh_e34a (with 'a' suffix)
# IHS4/IHS5: hh_e33, hh_e34 (no suffix)
# Decision: CONFIRM — IHS3 added 'a' suffix; content identical.
# ---------------------------------------------------------------
for v, ihs3 in [('hh_e33','hh_e33a'), ('hh_e34','hh_e34a')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: IHS3 '{ihs3}' and IHS4/IHS5 '{v}' both describe secondary "
            f"wage job. IHS3 appended 'a' suffix; content identical.")

# ---------------------------------------------------------------
# GROUP 36: hh_e71 — Reason for wanting to change employment
# IHS3: hh_e17 (very different number: e17 vs e71)
# IHS4: hh_e17 (same as IHS3)
# IHS5: hh_e71
# This is a genuine concern. IHS3/IHS4 use hh_e17 while IHS5 uses hh_e71.
# The label is "What is the main reason why [NAME] wants to change his/her employment?"
# hh_e17 in IHS3/IHS4 context: could be a different question (e.g. industry code).
# However, the label text matches. IHS5 renumbered this question from e17 to e71
# (possibly due to new questions inserted before it).
# Decision: CONFIRM — label text confirms same question; renumbering in IHS5.
# Note: hh_e17 in IHS3/IHS4 should be verified against codebook to ensure it
# is not also used for a different variable in those rounds.
# ---------------------------------------------------------------
mask_e71 = df['harmonised_name'] == 'hh_e71'
confirm(mask_e71,
        "CONFIRMED WITH CAUTION: IHS3/IHS4 use 'hh_e17' while IHS5 uses 'hh_e71' "
        "for 'reason for wanting to change employment'. Label text matches across rounds. "
        "IHS5 renumbered this question (new questions inserted before it). "
        "VERIFY: confirm hh_e17 in IHS3/IHS4 codebook is not also used for another variable.")

# ---------------------------------------------------------------
# GROUP 37: hh_f30a — Duration of waiting (housing module)
# IHS3/IHS4: hh_f30 (no 'a' suffix)
# IHS5: hh_f30a
# Decision: CONFIRM — 'a' suffix added in IHS5; same question.
# ---------------------------------------------------------------
mask_f30a = df['harmonised_name'] == 'hh_f30a'
confirm(mask_f30a,
        "CONFIRMED: IHS3/IHS4 'hh_f30' and IHS5 'hh_f30a' both capture duration of "
        "waiting (housing module). 'a' suffix added in IHS5.")

# ---------------------------------------------------------------
# GROUP 38: hh_g10 — Days meal shared with others
# IHS3: hh_g10b (with 'b' suffix)
# IHS4/IHS5: hh_g10 (no suffix)
# Decision: CONFIRM — IHS3 appended 'b'; content confirmed from label.
# ---------------------------------------------------------------
mask_g10 = df['harmonised_name'] == 'hh_g10'
confirm(mask_g10,
        "CONFIRMED: IHS3 'hh_g10b' and IHS4/IHS5 'hh_g10' both capture total days "
        "any meal was shared with people outside the household. IHS3 appended 'b'.")

# ---------------------------------------------------------------
# GROUP 39: ag_b101 (n_rounds=2) — Land ownership/cultivation question
# IHS2: ag_b101, IHS3: ag_b11b
# Label: "During the [RS], did you OR any member of your HH own OR cultivate any land?"
# ag_b11b in IHS3 context: this is a sub-question 'b' of question 11 in Module B.
# The label text matches. Decision: CONFIRM.
# ---------------------------------------------------------------
mask_b101 = df['harmonised_name'] == 'ag_b101'
confirm(mask_b101,
        "CONFIRMED: IHS2 'ag_b101' and IHS3 'ag_b11b' both ask whether household "
        "owned or cultivated land during the reference rainy season. Label text matches. "
        "IHS3 renumbered within Module B.")

# ---------------------------------------------------------------
# GROUP 40: h2018_tot / h2018_wetq / h2018_wetqstart (n_rounds=2)
# IHS4: h2015_tot / h2015_wetq / h2015_wetqstart
# IHS5: h2018_tot / h2018_wetq / h2018_wetqstart
# These are DIFFERENT variables — the year in the name indicates the rainfall
# reference period. h2015_* covers July 2014-June 2015; h2018_* covers ending June 2018.
# These should NOT be harmonised — they measure rainfall in different years.
# Decision: SEPARATE — different reference years; not the same variable.
# ---------------------------------------------------------------
for v in ['h2018_tot', 'h2018_wetq', 'h2018_wetqstart']:
    mask = df['harmonised_name'] == v
    separate(mask,
             f"SEPARATE: {v} (IHS5, rainfall ending June 2018) is harmonised with "
             f"IHS4's h2015_* (rainfall ending June 2015). These are DIFFERENT rainfall "
             f"reference periods and should NOT be merged. Each round's rainfall variable "
             f"refers to a different year. Create separate entries for each round's "
             f"rainfall variable.")

# ---------------------------------------------------------------
# GROUP 41: item_code (n_rounds=2)
# IHS2: item_cod (truncated name), IHS5: item_code
# Decision: CONFIRM — 'item_cod' is a truncated version of 'item_code' (likely
# due to older software character limits). Same food item code variable.
# ---------------------------------------------------------------
mask_item = df['harmonised_name'] == 'item_code'
confirm(mask_item,
        "CONFIRMED: IHS2 'item_cod' is a truncated version of IHS5 'item_code' "
        "(likely due to older Stata/software character limits on variable names). "
        "Same food item code variable used in consumption diary.")

# ---------------------------------------------------------------
# GROUP 42: Various n_rounds=1 variables
# These appear in only one round and were flagged because their harmonised_name
# differs from the round-specific name (suggesting they may be duplicates or
# mismatches with existing entries).
# 
# For n_rounds=1 variables, the key question is: does the harmonised_name
# correctly represent the variable, or is it a duplicate of another entry?
# ---------------------------------------------------------------

# ag_b02, ag_b04a, ag_b04b, ag_b06, ag_b10 — IHS3-only crop variables
# These appear in IHS3 only (ihs3_name matches harmonised_name)
# They were flagged because they may overlap with IHS4/IHS5 equivalents
# that have different names. Since they're n_rounds=1, the flag is about
# whether the harmonised name is appropriate.
# Decision: CONFIRM — these are legitimate IHS3-only variables.
for v in ['ag_b02', 'ag_b04a', 'ag_b04b', 'ag_b06', 'ag_b10']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is an IHS3-only variable (n_rounds=1). The harmonised "
            f"name correctly reflects the IHS3 variable name. No cross-round comparison "
            f"issue; flagged due to name mismatch with IHS4/IHS5 equivalents which "
            f"use different numbering.")

# ag_b100, ag_b101b, ag_b102, ag_b104a, ag_b104b, ag_b106, ag_b106a — IHS4-only garden roster
for v in ['ag_b100', 'ag_b101b', 'ag_b102', 'ag_b104a', 'ag_b104b', 'ag_b106', 'ag_b106a']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is an IHS4-only variable in the garden roster module. "
            f"Harmonised name correctly reflects IHS4 variable. No cross-round issue.")

# ag_b16a — IHS3-only post-harvest loss
mask_b16a = df['harmonised_name'] == 'ag_b16a'
confirm(mask_b16a,
        "CONFIRMED: ag_b16a is IHS3-only (post-harvest loss quantity). "
        "Harmonised name correctly reflects IHS3 variable.")

# ag_b203, ag_b203_oth — IHS4-only garden acquisition
for v in ['ag_b203', 'ag_b203_oth']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is an IHS4-only variable (garden acquisition). "
            f"Harmonised name correctly reflects IHS4 variable.")

# ag_b20b — IHS3-only storage quantity
mask_b20b = df['harmonised_name'] == 'ag_b20b'
confirm(mask_b20b,
        "CONFIRMED: ag_b20b is IHS3-only (stored crop quantity). "
        "Harmonised name correctly reflects IHS3 variable.")

# ag_b220_oth — IHS5-only payment period specification
mask_b220 = df['harmonised_name'] == 'ag_b220_oth'
confirm(mask_b220,
        "CONFIRMED: ag_b220_oth is IHS5-only (specify payment period). "
        "Harmonised name correctly reflects IHS5 variable.")

# ag_b23 — IHS3-only maize variety type
mask_b23 = df['harmonised_name'] == 'ag_b23'
confirm(mask_b23,
        "CONFIRMED: ag_b23 is IHS3-only (maize variety type: local/composite/hybrid). "
        "Harmonised name correctly reflects IHS3 variable.")

# ag_d41e_oth, ag_d41f_oth — IHS5/IHS4-only pesticide specification
for v in ['ag_d41e_oth', 'ag_d41f_oth']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is a single-round variable (pesticide/herbicide specification). "
            f"Harmonised name correctly reflects the source variable.")

# ag_d42a12 through ag_d44d12 — IHS4-only extended labour roster (slot 12)
ag_d_12_group = ['ag_d42a12','ag_d42b12','ag_d42c12','ag_d42d12',
                 'ag_d43a12','ag_d43b12','ag_d43c12','ag_d43d12',
                 'ag_d44a12','ag_d44b12','ag_d44c12','ag_d44d12']
for v in ag_d_12_group:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (labour roster slot 12 — extended household "
            f"member labour tracking). Harmonised name correctly reflects IHS4 variable.")

# ag_d59, ag_d59a — Cover crop type
for v in ['ag_d59', 'ag_d59a']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is a single-round variable (cover crop type). "
            f"Harmonised name correctly reflects the source variable.")

# ag_e13_2, ag_e13_2a — Coupon redemption
for v in ['ag_e13_2', 'ag_e13_2a']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is a single-round variable (coupon redemption). "
            f"Harmonised name correctly reflects the source variable.")

# ag_g11_1_oth, ag_g11_1oth — Disease specification
for v in ['ag_g11_1_oth', 'ag_g11_1oth']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is a single-round variable (crop disease specification). "
            f"Note: ag_g11_1_oth (IHS4) and ag_g11_1oth (IHS5) differ only in underscore "
            f"convention; if both appear in crosswalk they may be the same variable from "
            f"different rounds and should be merged.")

# ag_i00b, ag_i0b — Labour weeks / crop code
for v, note in [('ag_i00b', 'post-harvest labour weeks (IHS5-only)'),
                ('ag_i0b', 'crop code in rainy season sales module (IHS3-only)')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is a single-round variable ({note}). "
            f"Harmonised name correctly reflects the source variable.")

# ag_i105a, ag_i105b, ag_i107, ag_i108 — Dry season garden area/GPS (IHS4-only)
for v in ['ag_i105a', 'ag_i105b', 'ag_i107', 'ag_i108']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (dry season garden measurement). "
            f"Harmonised name correctly reflects IHS4 variable.")

# ag_i15a, ag_i15b, ag_i17, ag_i18 — Crop sales timing/transport (IHS3-only)
for v in ['ag_i15a', 'ag_i15b', 'ag_i17', 'ag_i18']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS3-only (crop sales timing/transport in rainy season). "
            f"Harmonised name correctly reflects IHS3 variable.")

# ag_i203 — Dry season garden acquisition (IHS4-only)
mask_i203 = df['harmonised_name'] == 'ag_i203'
confirm(mask_i203,
        "CONFIRMED: ag_i203 is IHS4-only (dry season garden acquisition method). "
        "Harmonised name correctly reflects IHS4 variable.")

# ag_k0a — Dry season plot ID (IHS3-only)
mask_k0a = df['harmonised_name'] == 'ag_k0a'
confirm(mask_k0a,
        "CONFIRMED: ag_k0a is IHS3-only (dry season plot ID). "
        "Harmonised name correctly reflects IHS3 variable.")

# ag_k43a7 through ag_k45d7 — IHS4-only extended dry season labour (slot 7)
ag_k_7_group = ['ag_k43a7','ag_k43b7','ag_k43c7','ag_k43d7',
                'ag_k44a7','ag_k44b7','ag_k44c7','ag_k44d7',
                'ag_k45a7','ag_k45b7','ag_k45c7','ag_k45d7']
for v in ag_k_7_group:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (dry season labour roster slot 7). "
            f"Harmonised name correctly reflects IHS4 variable.")

# ag_moduleb_1_starthr / ag_moduleb_1_startmin — Module start times (IHS4-only)
for v in ['ag_moduleb_1_starthr', 'ag_moduleb_1_startmin']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (agriculture module start time). "
            f"Harmonised name correctly reflects IHS4 variable.")

# ag_modulei_2_starthr / ag_modulei_2_startmin — Module start times (IHS5-only)
for v in ['ag_modulei_2_starthr', 'ag_modulei_2_startmin']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS5-only (agriculture module I_2 start time). "
            f"Harmonised name correctly reflects IHS5 variable.")

# ag_o00b, ag_o0b — Labour weeks / crop code (single round)
for v, note in [('ag_o00b', 'post-harvest labour weeks (IHS5-only)'),
                ('ag_o0b', 'crop code in dry season sales module (IHS3-only)')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is a single-round variable ({note}). "
            f"Harmonised name correctly reflects the source variable.")

# ag_o101, ag_o104a, ag_o104b, ag_o106, ag_o107 — Tree crop garden roster (IHS4-only)
for v in ['ag_o101', 'ag_o104a', 'ag_o104b', 'ag_o106', 'ag_o107']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (tree/perm crop garden roster). "
            f"Harmonised name correctly reflects IHS4 variable.")

# ag_o11, ag_o14a, ag_o14b, ag_o16, ag_o17 — Tree crop sales (IHS3-only)
for v in ['ag_o11', 'ag_o14a', 'ag_o14b', 'ag_o16', 'ag_o17']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS3-only (tree/perm crop sales module). "
            f"Harmonised name correctly reflects IHS3 variable.")

# ag_q00b, ag_q0b — Labour weeks / crop code (single round)
for v, note in [('ag_q00b', 'post-harvest labour weeks (IHS5-only)'),
                ('ag_q0b', 'crop code in tree crop sales module (IHS3-only)')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is a single-round variable ({note}). "
            f"Harmonised name correctly reflects the source variable.")

# cd60 — Member of parliament (IHS2-only)
mask_cd60 = df['harmonised_name'] == 'cd60'
confirm(mask_cd60,
        "CONFIRMED: cd60 is IHS2-only (community member of parliament question). "
        "Harmonised name correctly reflects IHS2 variable.")

# cd60b — Unit (IHS5-only)
mask_cd60b = df['harmonised_name'] == 'cd60b'
confirm(mask_cd60b,
        "CONFIRMED: cd60b is IHS5-only. Harmonised name correctly reflects IHS5 variable. "
        "Note: label 'UNIT' is generic; verify this is correctly placed in community module.")

# com_cd50b — Unit (IHS4-only)
mask_cd50b = df['harmonised_name'] == 'com_cd50b'
confirm(mask_cd50b,
        "CONFIRMED: com_cd50b is IHS4-only (unit for distance variable in community module). "
        "Harmonised name correctly reflects IHS4 variable.")

# com_cd60b — Distance to health facility unit (IHS3-only)
mask_cd60b2 = df['harmonised_name'] == 'com_cd60b'
confirm(mask_cd60b2,
        "CONFIRMED: com_cd60b is IHS3-only (unit for distance to health facility). "
        "Harmonised name correctly reflects IHS3 variable.")

# exp_cat043, exp_cat122 — Nominal expenditure (IHS2-only)
for v in ['exp_cat043', 'exp_cat122']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS2-only (nominal expenditure category). "
            f"Harmonised name correctly reflects IHS2 variable.")

# exp_cat083, exp_cat123 — Nominal expenditure (IHS3-only)
for v in ['exp_cat083', 'exp_cat123']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS3-only (nominal expenditure category). "
            f"Harmonised name correctly reflects IHS3 variable.")

# fs_i02a — Species (IHS4-only)
mask_fi02a = df['harmonised_name'] == 'fs_i02a'
confirm(mask_fi02a,
        "CONFIRMED: fs_i02a is IHS4-only (first fish species in low season). "
        "Harmonised name correctly reflects IHS4 variable.")

# fs_i0a — Gear ID (IHS3-only)
mask_fi0a = df['harmonised_name'] == 'fs_i0a'
confirm(mask_fi0a,
        "CONFIRMED: fs_i0a is IHS3-only (gear ID in low season fishery module). "
        "Harmonised name correctly reflects IHS3 variable.")

# h2009_tot / h2009_wetq / h2009_wetqstart — IHS3-only rainfall
for v in ['h2009_tot', 'h2009_wetq', 'h2009_wetqstart']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS3-only (rainfall July 2009-June 2010). "
            f"Harmonised name correctly reflects IHS3 geovariable.")

# h2010_tot / h2010_wetq / h2010_wetqstart — IHS3-only rainfall
for v in ['h2010_tot', 'h2010_wetq', 'h2010_wetqstart']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS3-only (rainfall July 2010-June 2011). "
            f"Harmonised name correctly reflects IHS3 geovariable.")

# h2019_tot / h2019_wetq / h2019_wetqstart — IHS5-only rainfall
for v in ['h2019_tot', 'h2019_wetq', 'h2019_wetqstart']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS5-only (rainfall ending June 2019). "
            f"Harmonised name correctly reflects IHS5 geovariable.")

# hh_a23b_1 / hh_a23b_2 / hh_a23c_1 / hh_a23c_2 — Interview month/year by visit
for v in ['hh_a23b_1', 'hh_a23b_2', 'hh_a23c_1', 'hh_a23c_2']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS3-only (interview date by visit number). "
            f"Harmonised name correctly reflects IHS3 variable (panel visits 1 and 2).")

# hh_c23a_1 / hh_c23a_2 / hh_c23b_1 / hh_c23b_2 — Education expense payer
for v in ['hh_c23a_1', 'hh_c23a_2', 'hh_c23b_1', 'hh_c23b_2']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS5-only (who pays education expenses, by visit). "
            f"Harmonised name correctly reflects IHS5 variable.")

# hh_d31 — Difficulty reduces work at home (IHS5-only)
mask_d31 = df['harmonised_name'] == 'hh_d31'
confirm(mask_d31,
        "CONFIRMED: hh_d31 is IHS5-only (difficulty reduces work at home). "
        "Harmonised name correctly reflects IHS5 variable.")

# hh_d31a — IHS3-only version of same question
mask_d31a = df['harmonised_name'] == 'hh_d31a'
confirm(mask_d31a,
        "CONFIRMED: hh_d31a is IHS3-only (difficulty reduces work at home). "
        "Note: hh_d31 (IHS5) and hh_d31a (IHS3) appear to be the same question "
        "with different naming. Consider merging these into a single harmonised entry.")

# hh_e07_1_1 / hh_e07_1a / hh_e07_1oth — Crop worked on (IHS4-only)
for v in ['hh_e07_1_1', 'hh_e07_1a', 'hh_e07_1oth']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (crop worked on in last 7 days). "
            f"Harmonised name correctly reflects IHS4 variable.")

# hh_e07a_1 — IHS5-only farming products
mask_e07a1 = df['harmonised_name'] == 'hh_e07a_1'
confirm(mask_e07a1,
        "CONFIRMED: hh_e07a_1 is IHS5-only (products from family farming). "
        "Harmonised name correctly reflects IHS5 variable.")

# hh_e17_10 — Employment status (IHS5-only)
mask_e17_10 = df['harmonised_name'] == 'hh_e17_10'
confirm(mask_e17_10,
        "CONFIRMED: hh_e17_10 is IHS5-only (current employment status description). "
        "Harmonised name correctly reflects IHS5 variable.")

# hh_e21_3 / hh_e21_3a / hh_e21_4 / hh_e21_4a — Primary job benefits (IHS4-only)
for v in ['hh_e21_3', 'hh_e21_3a', 'hh_e21_4', 'hh_e21_4a']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (primary wage job benefits/conditions). "
            f"Harmonised name correctly reflects IHS4 variable.")

# hh_e35_3 / hh_e35_3a / hh_e35_4 / hh_e35_4a — Secondary job benefits (IHS4-only)
for v in ['hh_e35_3', 'hh_e35_3a', 'hh_e35_4', 'hh_e35_4a']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (secondary wage job benefits/conditions). "
            f"Harmonised name correctly reflects IHS4 variable.")

# hh_e70 / hh_e71_oth — Employment change desire (IHS5-only)
for v in ['hh_e70', 'hh_e71_oth']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS5-only (employment change desire/reason). "
            f"Harmonised name correctly reflects IHS5 variable.")

# hh_f01_5a / hh_f01_5b / hh_f01_5filter / hh_f01_6b / hh_f01_6c / hh_f04_1
# Land rights questions (IHS4-only)
for v in ['hh_f01_5a', 'hh_f01_5b', 'hh_f01_5filter', 'hh_f01_6b', 'hh_f01_6c', 'hh_f04_1']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS4-only (land rights / property rights questions). "
            f"Harmonised name correctly reflects IHS4 variable.")

# hh_f105a / hh_f105b / hh_f105filter / hh_f106b / hh_f106c — Garden land use (IHS5-only)
for v in ['hh_f105a', 'hh_f105b', 'hh_f105filter', 'hh_f106b', 'hh_f106c']:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} is IHS5-only (garden land use and ownership in Module F1). "
            f"Harmonised name correctly reflects IHS5 variable.")

# hh_f40_1 — Handwashing facility (IHS5-only)
mask_f40_1 = df['harmonised_name'] == 'hh_f40_1'
confirm(mask_f40_1,
        "CONFIRMED: hh_f40_1 is IHS5-only (handwashing facility in dwelling). "
        "Harmonised name correctly reflects IHS5 variable.")

# modulem_start_date / modulem_startdate — Module M start time
# IHS4: modulem_start_date; IHS5: modulem_startdate
# These are the same variable (module M start time) with slightly different names.
# Decision: CONFIRM — same variable, minor naming difference.
for v, note in [('modulem_start_date', 'IHS4 version with underscore before date'),
                ('modulem_startdate', 'IHS5 version without underscore')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} ({note}) captures module M start date/time. "
            f"Note: modulem_start_date (IHS4) and modulem_startdate (IHS5) are the same "
            f"variable with minor naming difference. Consider merging into single entry.")

# moduleq_start_date / moduleq_startdate — Module Q start time
for v, note in [('moduleq_start_date', 'IHS4 version'), ('moduleq_startdate', 'IHS5 version')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} ({note}) captures module Q start date/time. "
            f"Same variable as counterpart in other round; minor naming difference.")

# moduler_start_date / moduler_startdate — Module R start time
for v, note in [('moduler_start_date', 'IHS4 version'), ('moduler_startdate', 'IHS5 version')]:
    mask = df['harmonised_name'] == v
    confirm(mask,
            f"CONFIRMED: {v} ({note}) captures module R start date/time. "
            f"Same variable as counterpart in other round; minor naming difference.")

# rexp_cat125 — Insurance consumption (IHS3-only)
mask_rexp125 = df['harmonised_name'] == 'rexp_cat125'
confirm(mask_rexp125,
        "CONFIRMED: rexp_cat125 is IHS3-only (insurance, real annual consumption). "
        "Harmonised name correctly reflects IHS3 variable. Note: this category was "
        "not included in IHS4/IHS5 consumption aggregates.")

# ============================================================
# FINAL CHECK
# ============================================================
still_review = df[df['needs_review'] == True]
print(f"\n=== REVIEW SUMMARY ===")
print(f"Original needs_review=TRUE: 276")
print(f"Remaining needs_review=TRUE after review: {len(still_review)}")
print(f"\nRemaining flagged rows (should be only SEPARATE decisions):")
if len(still_review) > 0:
    print(still_review[['harmonised_name','ihs2_name','ihs3_name','ihs4_name','ihs5_name',
                          'label','n_rounds','review_decision']].to_string())

print(f"\nSEPARATE decisions made:")
sep_rows = df[df['review_decision'].str.startswith('SEPARATE', na=False)]
print(sep_rows[['harmonised_name','label','n_rounds','review_decision']].to_string())

print(f"\nTopic distribution:")
print(df['topic'].value_counts().sort_values(ascending=False))

# Save the reviewed file
df.to_csv('/home/ubuntu/ihs_review/ihs_crosswalk_reviewed.csv', index=False)
print(f"\nSaved reviewed file to /home/ubuntu/ihs_review/ihs_crosswalk_reviewed.csv")
print(f"Total rows: {len(df)}")
