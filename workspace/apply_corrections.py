#!/usr/bin/env python3
"""
Apply corrections to the Aisha Salisu Isansi slide presentation.
Preserves all existing design and format; only modifies text content
and adds 3 new slides matching the existing design template.
"""
import shutil
import os
import re

UNPACKED = "/home/z/my-project/workspace/pptx_unpacked"

def read_xml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_xml(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_text_in_xml(xml_content, old_text, new_text):
    """Replace text in <a:t> elements while preserving all XML structure."""
    # Escape for regex
    old_escaped = re.escape(old_text)
    pattern = f'(<a:t>){old_escaped}(</a:t>)'
    replacement = f'\\g<1>{new_text}\\g<2>'
    new_content, count = re.subn(pattern, replacement, xml_content)
    if count == 0:
        print(f"  WARNING: Could not find '{old_text}' in XML")
    else:
        print(f"  Replaced '{old_text}' -> '{new_text}' ({count} occurrence(s))")
    return new_content

# ===== 1. Edit slide1.xml - Change title =====
print("=== Editing Slide 1 (Title) ===")
path = os.path.join(UNPACKED, "ppt/slides/slide1.xml")
xml = read_xml(path)
xml = replace_text_in_xml(xml,
    "Fungal Microflora of Indoor Air in Reception Areas of Academic Buildings at Nile University of Nigeria, Abuja",
    "Assessment of Microflora of Indoor Air in Reception Areas of Some Academic Buildings at Nile University of Nigeria, Abuja"
)
write_xml(path, xml)

# ===== 2. Edit slide7.xml - Climatic Variable =====
print("\n=== Editing Slide 7 (Study Area & Experimental Design) ===")
path = os.path.join(UNPACKED, "ppt/slides/slide7.xml")
xml = read_xml(path)
xml = replace_text_in_xml(xml,
    "Conducted in the dry season prior to the onset of harmattan, characterized by warm temperatures and reduced humidity.",
    "Conducted in dry season, characterized by dry dust-laden Harmattan trade wind."
)
write_xml(path, xml)

# ===== 3. Edit slide8.xml - Multiple corrections =====
print("\n=== Editing Slide 8 (Sample Collection and Mathematical Conversion) ===")
path = os.path.join(UNPACKED, "ppt/slides/slide8.xml")
xml = read_xml(path)

# 3a. Active Media
xml = replace_text_in_xml(xml,
    "Sabouraud Dextrose Agar (SDA) supplemented with Chloramphenicol (50 ug/mL).",
    "SDA supplemented with chloramphenicol (50 &#181;g/mL) to inhibit bacterial growth."
)

# 3b. Exposure Method
xml = replace_text_in_xml(xml,
    "Settle Plate (gravitational sedimentation). Petri dishes exposed at 1.0 metre height for exactly 15 minutes.",
    "Average settling time."
)

# 3c. Omeliansky's Formula - formula line
xml = replace_text_in_xml(xml,
    "CFU/m3 = (n x 10,000) / (pi x r2 x t)",
    "CFU/m&#179; = (n &#215; 10&#8308;) / (&#960; &#215; r&#178; &#215; t)"
)

# 3d. Omeliansky's formula parameters
xml = replace_text_in_xml(xml,
    "n = colonies, r = 4.5 cm, t = 15 mins. Factor = 10.48",
    "where n = colonies, r = Petri plate radius (cm), t = exposure time (15 min), correction factor is 10&#8308;&#8211;10&#8309;"
)

write_xml(path, xml)

# ===== 4. Add new items to slide8: "Statistic" and "Niger Hall: occupancy & colony movement" =====
# We need to add these as new bullet items after the existing Susceptibility Testing item.
# We'll insert them by adding new shape pairs (teal bullet + text) after the last shape.

print("\n=== Adding new bullet items to Slide 8 ===")
path = os.path.join(UNPACKED, "ppt/slides/slide8.xml")
xml = read_xml(path)

# Find the last </p:sp> before </p:spTree> to insert new shapes before it
# The last shape is the "Susceptibility Testing" text box (id="23")
# We'll add two more bullet pairs: Statistic and Niger Hall

# Teal bullet style template (matching existing ones like id="22")
teal_bullet_template = '''      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{id1}" name="Text {name_idx}"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="609600" y="{y_pos}"/>
            <a:ext cx="38100" cy="253901"/>
          </a:xfrm>
          <a:prstGeom prst="roundRect">
            <a:avLst>
              <a:gd name="adj" fmla="val 66667"/>
            </a:avLst>
          </a:prstGeom>
          <a:solidFill>
            <a:srgbClr val="2A9D8F"/>
          </a:solidFill>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" indent="0">
              <a:buNone/>
            </a:pPr>
            <a:endParaRPr lang="en-US" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>'''

# Text box template (matching existing ones like id="23")
text_box_template = '''      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{id1}" name="Text {name_idx}"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="774650" y="{y_pos}"/>
            <a:ext cx="8147737" cy="211205"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="t"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" indent="0" algn="l">
              <a:lnSpc>
                <a:spcPts val="1540"/>
              </a:lnSpc>
              <a:buNone/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="1100" b="1" dirty="0">
                <a:solidFill>
                  <a:srgbClr val="3D5A80"/>
                </a:solidFill>
                <a:latin typeface="Gill Sans MT" pitchFamily="34" charset="0"/>
                <a:ea typeface="Gill Sans MT" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Gill Sans MT" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>{text}</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" sz="1100" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>'''

# Position for Statistic bullet (after Susceptibility Testing which is at y=4427190)
# The existing items use about 558000 vertical spacing between items
# Last teal bullet is at y=4427190, so next at ~4760000 — but slide height is 5143500 EMU
# Actually, the slide is getting full. Let me check if we have room.
# Slide height: 5143500 EMU (9144000x5143500 = 10" x 5.63" = widescreen)
# Last item "Susceptibility Testing" text box is at y=4401889 with height 422410
# That goes to y=4824299, which is near the bottom.
# We need to slightly adjust the vertical spacing to fit the new items.
# Let me move the "Taxonomic Identification" section items and add the two new items.

# Actually, a better approach: since the slide is already quite full, let me 
# reconsider. The user's correction says to add "Statistic" and "Niger Hall: occupancy & colony movement"
# to the Study Area & Experimental Design section. These should go on slide 7, not slide 8.
# Looking at the user's instructions again:
# "Study Area & Experimental Design
# * Climatic variable ...
# * Active media: ...
# * Exposure method: ...
# * Omeliansky's formula ...
# * Statistic
# * Niger Hall: occupancy & colony movement"
# 
# These are all listed under "Study Area & Experimental Design" which is slide 7.
# But "Active media" and "Exposure method" and "Omeliansky's formula" are on slide 8.
# The user seems to be giving a consolidated list of corrections for the methodology section.
# Since "Statistic" and "Niger Hall: occupancy & colony movement" are study design details,
# they should go on slide 7 (Study Area & Experimental Design).
# Slide 7 currently has 5 bullet items and has more vertical room.

print("  Adding 'Statistic' and 'Niger Hall' items to Slide 7 instead (Study Area & Experimental Design)")

path = os.path.join(UNPACKED, "ppt/slides/slide7.xml")
xml = read_xml(path)

# Current items on slide7:
# id=5,6: Location (y=1237804)
# id=7,8: Sample Sites (y=1796504) 
# id=9,10: Temporal Analysis (y=2228106)
# id=11,12: Climatic Variable (y=2786807)
# id=13,14: Sampling Scheme (y=3345507)
# Last item ends at y=3345507+493776=3839283

# We need to fit 2 more items. Let's recalculate vertical positions.
# Available space: from y=838051 (after subtitle) to y=5143500 (slide bottom)
# That's about 4305449 EMU for 7 items = ~615064 EMU per item spacing
# But we can use tighter spacing. Let's use the same y-spacing pattern.

# Actually, the simplest approach is to add the new items at the end and adjust nothing else,
# since there IS room on slide 7 (last item ends at ~3.8M EMU out of 5.14M EMU slide height).

# New positions for items 6 and 7 (Statistic and Niger Hall)
# Item 6 starts at y = 3345507 + 558700 = 3904207
y_statistic_bullet = 3839283  # After Sampling Scheme ends
y_statistic_text = 3813983
y_niger_bullet = 3839283 + 558700
y_niger_text = y_niger_bullet - 25300

# But let me calculate more carefully. The current pattern:
# Each pair: teal bullet at y_offset, text box at y_offset-25300
# Item spacing: about 558700 EMU
# Last item (Sampling Scheme): teal at y=3370808, text at y=3345507
# Sampling Scheme text goes to y=3345507+493776=3839283

# New item 6 (Statistic):
y6_bullet = 3370808 + 558700  # = 3929508
y6_text = y6_bullet - 25300    # = 3904208

# New item 7 (Niger Hall):
y7_bullet = y6_bullet + 558700  # = 4488208
y7_text = y7_bullet - 25300     # = 4462908

# Check if fits: y7_text + 493776 = 4956684 < 5143500 ✓

new_shapes = teal_bullet_template.format(id1=15, name_idx=22, y_pos=y6_bullet)
new_shapes += text_box_template.format(id1=16, name_idx=23, y_pos=y6_text, text="Statistic: Descriptive statistics including frequency distributions, relative abundances, and diversity indices (Shannon-Wiener, Pielou&#8217;s Evenness, Simpson&#8217;s).")
new_shapes += teal_bullet_template.format(id1=17, name_idx=24, y_pos=y7_bullet)
new_shapes += text_box_template.format(id1=18, name_idx=25, y_pos=y7_text, text="Niger Hall: Occupancy and colony movement &#8211; afternoon counts increased 33% from AM to PM, reflecting late-occupancy activity patterns.")

# Insert before </p:spTree>
xml = xml.replace('</p:spTree>', new_shapes + '\n    </p:spTree>')

# Update slide name
xml = xml.replace('name="Slide 7"', 'name="Slide 7"')

write_xml(path, xml)
print("  Added 'Statistic' and 'Niger Hall' bullet items to Slide 7")

# ===== 5. Create 3 new slides =====
print("\n=== Creating new slides ===")

# Common design elements from existing slides
def create_content_slide(slide_name, header_title, subtitle, bullet_items):
    """
    Create a content slide matching the existing design template.
    bullet_items: list of (bold_label, normal_text) tuples
    """
    y_start = 838051  # After the header bar area
    y_spacing = 700000  # Vertical spacing between items
    
    # Build bullet item shapes
    shapes = ""
    shape_id = 5  # Starting ID after header bar (2), header title (3), subtitle (4)
    name_idx = 3
    
    for i, (bold_label, normal_text) in enumerate(bullet_items):
        y_bullet = y_start + i * y_spacing
        y_text = y_bullet - 25300
        
        full_text = bold_label + normal_text if normal_text else bold_label
        
        # Teal bullet
        shapes += f'''      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{shape_id}" name="Text {name_idx}"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="609600" y="{y_bullet}"/>
            <a:ext cx="38100" cy="304800"/>
          </a:xfrm>
          <a:prstGeom prst="roundRect">
            <a:avLst>
              <a:gd name="adj" fmla="val 66667"/>
            </a:avLst>
          </a:prstGeom>
          <a:solidFill>
            <a:srgbClr val="2A9D8F"/>
          </a:solidFill>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" indent="0">
              <a:buNone/>
            </a:pPr>
            <a:endParaRPr lang="en-US" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
'''
        shape_id += 1
        name_idx += 1
        
        # Text box
        # Calculate height based on text length
        text_height = max(211205, min(800000, len(full_text) * 4500))
        
        shapes += f'''      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{shape_id}" name="Text {name_idx}"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="774650" y="{y_text}"/>
            <a:ext cx="8147737" cy="{text_height}"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="t"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" indent="0" algn="l">
              <a:lnSpc>
                <a:spcPts val="1800"/>
              </a:lnSpc>
              <a:buNone/>
            </a:pPr>
'''
        # If we have a bold label separate from normal text
        if bold_label and normal_text:
            shapes += f'''            <a:r>
              <a:rPr lang="en-US" sz="1200" b="1" dirty="0">
                <a:solidFill>
                  <a:srgbClr val="3D5A80"/>
                </a:solidFill>
                <a:latin typeface="Gill Sans MT" pitchFamily="34" charset="0"/>
                <a:ea typeface="Gill Sans MT" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Gill Sans MT" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>{bold_label}</a:t>
            </a:r>
            <a:r>
              <a:rPr lang="en-US" sz="1200" dirty="0">
                <a:solidFill>
                  <a:srgbClr val="3D5A80"/>
                </a:solidFill>
                <a:latin typeface="Gill Sans MT" pitchFamily="34" charset="0"/>
                <a:ea typeface="Gill Sans MT" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Gill Sans MT" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>{normal_text}</a:t>
            </a:r>
'''
        else:
            shapes += f'''            <a:r>
              <a:rPr lang="en-US" sz="1200" b="1" dirty="0">
                <a:solidFill>
                  <a:srgbClr val="3D5A80"/>
                </a:solidFill>
                <a:latin typeface="Gill Sans MT" pitchFamily="34" charset="0"/>
                <a:ea typeface="Gill Sans MT" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Gill Sans MT" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>{bold_label}</a:t>
            </a:r>
'''
        shapes += f'''            <a:endParaRPr lang="en-US" sz="1200" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
'''
        shape_id += 1
        name_idx += 1
    
    # Build the complete slide XML
    slide_xml = f'''<?xml version="1.0" encoding="ascii"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld name="{slide_name}">
    <p:bg>
      <p:bgPr>
        <a:solidFill>
          <a:srgbClr val="FFFFFF"/>
        </a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="Text 0"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="0" y="0"/>
            <a:ext cx="9144000" cy="660350"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
          <a:solidFill>
            <a:srgbClr val="122040"/>
          </a:solidFill>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" indent="0">
              <a:buNone/>
            </a:pPr>
            <a:endParaRPr lang="en-US" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="3" name="Text 1"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="609600" y="155525"/>
            <a:ext cx="8534400" cy="377083"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="t"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" indent="0" algn="l">
              <a:lnSpc>
                <a:spcPts val="2750"/>
              </a:lnSpc>
              <a:buNone/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="2200" b="1" dirty="0">
                <a:solidFill>
                  <a:srgbClr val="FFFFFF"/>
                </a:solidFill>
                <a:latin typeface="Gill Sans MT" pitchFamily="34" charset="0"/>
                <a:ea typeface="Gill Sans MT" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Gill Sans MT" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>{header_title}</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" sz="2200" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="4" name="Text 2"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="609600" y="787301"/>
            <a:ext cx="8534400" cy="230332"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
          <a:noFill/>
          <a:ln/>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="t"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" indent="0" algn="l">
              <a:lnSpc>
                <a:spcPts val="1950"/>
              </a:lnSpc>
              <a:spcAft>
                <a:spcPts val="400"/>
              </a:spcAft>
              <a:buNone/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="1300" b="1" dirty="0">
                <a:solidFill>
                  <a:srgbClr val="1B2A4A"/>
                </a:solidFill>
                <a:latin typeface="Gill Sans MT" pitchFamily="34" charset="0"/>
                <a:ea typeface="Gill Sans MT" pitchFamily="34" charset="-122"/>
                <a:cs typeface="Gill Sans MT" pitchFamily="34" charset="-120"/>
              </a:rPr>
              <a:t>{subtitle}</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" sz="1300" dirty="0"/>
          </a:p>
        </p:txBody>
      </p:sp>
{shapes}    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>'''
    return slide_xml


# --- Slide 16: Species Composition and Diversity Indices ---
slide16 = create_content_slide(
    slide_name="Slide 16",
    header_title="Results",
    subtitle="Species Composition and Diversity Indices",
    bullet_items=[
        ("Species Composition: ", 
         "Six fungal species identified: Aspergillus niger (black strain, 26.1%), Aspergillus flavus (21.7%), Aspergillus niger (white strain, 17.4%), Penicillium chrysogenum (15.2%), Aspergillus fumigatus (10.9%), and Trichoderma erinaceum (8.7%)."),
        ("Shannon-Wiener Index (H&#8242;): ", 
         "High diversity across all buildings: Niger Hall (1.773), Volta Hall (1.714), and Limpopo Hall (1.646), reflecting a diverse indoor mycobiota."),
        ("Pielou&#8217;s Evenness (J): ", 
         "Values ranged from 0.919 (Limpopo Hall) to 0.989 (Niger Hall), indicating equitable species distribution with no single pathogen dominating."),
        ("Simpson&#8217;s Diversity (1&#8211;D): ", 
         "Ranged from 0.789 (Limpopo Hall) to 0.827 (Niger Hall), further confirming high species diversity across all sampled buildings."),
        ("Dominant Species: ", 
         "Aspergillus niger (black strain) was consistently the most frequently isolated species across all three buildings, with highest prevalence in Limpopo Hall (5 isolates)."),
    ]
)

slide16_path = os.path.join(UNPACKED, "ppt/slides/slide16.xml")
write_xml(slide16_path, slide16)
print("  Created slide16.xml (Species Composition and Diversity Indices)")

# --- Slide 17: Antifungal Susceptibility Profiling ---
slide17 = create_content_slide(
    slide_name="Slide 17",
    header_title="Results (cont.)",
    subtitle="Antifungal Susceptibility Profiling",
    bullet_items=[
        ("Ketoconazole (50 &#181;g/mL): ", 
         "Most effective agent with mean inhibition zones of 13&#8211;22 mm. A. niger (black) and A. fumigatus were the most susceptible (22 mm and 21 mm respectively)."),
        ("Fluconazole (25 &#181;g/mL): ", 
         "No inhibitory activity observed (0 mm zones) against all tested species, confirming 100% intrinsic resistance across all isolates."),
        ("Griseofulvin (100 &#181;g/mL): ", 
         "Least active agent with mean zones of 8&#8211;17 mm. A. fumigatus showed the highest susceptibility (17 mm); T. erinaceum showed the least (8 mm)."),
        ("Trichoderma erinaceum: ", 
         "Showed the greatest resistance among all tested species, with resistant category responses to all three antifungal agents including ketoconazole (13 mm)."),
        ("Clinical Implication: ", 
         "Ketoconazole is the most effective therapeutic option for environmental mould infections in this region; fluconazole resistance warrants clinical awareness."),
    ]
)

slide17_path = os.path.join(UNPACKED, "ppt/slides/slide17.xml")
write_xml(slide17_path, slide17)
print("  Created slide17.xml (Antifungal Susceptibility Profiling)")

# --- Slide 18: Discussion and Key Recommendations ---
slide18 = create_content_slide(
    slide_name="Slide 18",
    header_title="Discussion and Key Recommendations",
    subtitle="Interpretation of Findings and Actionable Steps",
    bullet_items=[
        ("Indoor Air Quality: ", 
         "All three buildings complied with WHO guideline of 50 CFU/m&#179;. HVAC filtration effectively reduced afternoon concentrations in Volta and Limpopo Halls. Niger Hall showed a 33% PM increase linked to occupancy."),
        ("Fungal Diversity: ", 
         "High Shannon-Wiener indices (1.646&#8211;1.773) and evenness values (0.919&#8211;0.989) indicate balanced mycobiota. The predominance of Aspergillus species is consistent with tropical educational settings."),
        ("Antifungal Resistance: ", 
         "Total fluconazole resistance across all isolates is clinically significant. Environmental selection pressure from agricultural and clinical antifungal overuse may be contributing to emerging resistance."),
        ("Recommendation 1: ", 
         "Implement routine indoor air quality monitoring programmes in all academic buildings, particularly during morning peak hours."),
        ("Recommendation 2: ", 
         "Conduct further research with seasonal comparisons (dry vs. wet season) and molecular identification methods for comprehensive aeromycota profiling."),
        ("Recommendation 3: ", 
         "Launch clinical awareness campaigns regarding fluconazole resistance in environmental moulds to guide empirical therapy in the FCT region."),
    ]
)

slide18_path = os.path.join(UNPACKED, "ppt/slides/slide18.xml")
write_xml(slide18_path, slide18)
print("  Created slide18.xml (Discussion and Key Recommendations)")

# ===== 6. Create slide relationship files for new slides =====
print("\n=== Creating slide relationship files ===")

rels_template = '''<?xml version="1.0" encoding="ascii"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>'''

for slide_num in [16, 17, 18]:
    rels_path = os.path.join(UNPACKED, f"ppt/slides/_rels/slide{slide_num}.xml.rels")
    write_xml(rels_path, rels_template)
    print(f"  Created slide{slide_num}.xml.rels")

# ===== 7. Update presentation.xml.rels =====
print("\n=== Updating presentation.xml.rels ===")
rels_path = os.path.join(UNPACKED, "ppt/_rels/presentation.xml.rels")
rels_xml = read_xml(rels_path)

# Add relationships for the 3 new slides (rId22, rId23, rId24)
# These IDs need to be unique and not conflict with existing ones
# Current max rId is rId21
new_rels = '''  <Relationship Id="rId22" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide16.xml"/>
  <Relationship Id="rId23" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide17.xml"/>
  <Relationship Id="rId24" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide18.xml"/>'''

rels_xml = rels_xml.replace('</Relationships>', new_rels + '\n</Relationships>')
write_xml(rels_path, rels_xml)
print("  Added rId22, rId23, rId24 for slides 16, 17, 18")

# ===== 8. Update [Content_Types].xml =====
print("\n=== Updating [Content_Types].xml ===")
ct_path = os.path.join(UNPACKED, "[Content_Types].xml")
ct_xml = read_xml(ct_path)

# Add Override entries for the 3 new slides
new_overrides = '''  <Override PartName="/ppt/slides/slide16.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide17.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide18.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'''

ct_xml = ct_xml.replace('</Types>', new_overrides + '\n</Types>')
write_xml(ct_path, ct_xml)
print("  Added Content Type overrides for slides 16, 17, 18")

# ===== 9. Update presentation.xml - Add slide IDs and reorder =====
print("\n=== Updating presentation.xml ===")
pres_path = os.path.join(UNPACKED, "ppt/presentation.xml")
pres_xml = read_xml(pres_path)

# Current slide order in sldIdLst:
# id="256" rId="rId2"  -> slide1 (Title)
# id="257" rId="rId3"  -> slide2 (Intro)
# id="258" rId="rId4"  -> slide3 (Intro cont.)
# id="259" rId="rId5"  -> slide4 (Justification)
# id="260" rId="rId6"  -> slide5 (Aims)
# id="261" rId="rId7"  -> slide6 (Significance)
# id="262" rId="rId8"  -> slide7 (Study Area)
# id="263" rId="rId9"  -> slide8 (Sample Collection)
# id="264" rId="rId10" -> slide9 (Results: Volumetric)
# id="265" rId="rId11" -> slide10 (Results: Macro)
# id="272" rId="rId12" -> slide11 (Results: Species)
# id="267" rId="rId13" -> slide12 (Conclusion)
# id="268" rId="rId14" -> slide13 (Recommendations)
# id="269" rId="rId15" -> slide14 (References)
# id="270" rId="rId16" -> slide15 (Thank You)

# We want to insert new slides AFTER slide11 (id="272" rId="rId12") 
# and BEFORE slide12 (id="267" rId="rId13")

# New slide IDs: 273, 274, 275 (continuing from 272)
# New entries to insert after the slide11 line
new_slide_entries = '''    <p:sldId id="273" r:id="rId22"/>
    <p:sldId id="274" r:id="rId23"/>
    <p:sldId id="275" r:id="rId24"/>'''

# Insert after slide11 entry (rId12) and before slide12 entry (rId13)
pres_xml = pres_xml.replace(
    '<p:sldId id="272" r:id="rId12"/>\n    <p:sldId id="267" r:id="rId13"/>',
    '<p:sldId id="272" r:id="rId12"/>\n' + new_slide_entries + '\n    <p:sldId id="267" r:id="rId13"/>'
)

write_xml(pres_path, pres_xml)
print("  Inserted new slide IDs 273, 274, 275 into presentation order")

# ===== 10. Pack the final presentation =====
print("\n=== Packing the corrected PPTX ===")
output_path = "/home/z/my-project/download/Aisha Salisu Isansi_slide presentation.pptx"

# Make sure download directory exists
os.makedirs("/home/z/my-project/download", exist_ok=True)

# Use the pack script from the skills directory
pack_script = "/home/z/my-project/skills/ppt/ooxml/scripts/pack.py"
os.system(f'python {pack_script} {UNPACKED} "{output_path}"')

if os.path.exists(output_path):
    print(f"\n  SUCCESS: Corrected PPTX saved to: {output_path}")
else:
    print("\n  ERROR: Failed to pack the PPTX file")

print("\n=== All corrections applied ===")
