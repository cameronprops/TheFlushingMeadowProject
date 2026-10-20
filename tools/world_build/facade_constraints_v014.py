#!/usr/bin/env python3
"""Evidence-constrained WF0028 interpretive facade dimensions; no building changes."""
import json
FT=0.3048
ART=[
 ("MODERN_MEDICINE","SOUTH_LARGE_BUILDING",36,34,"WF28-A032"),
 ("PRIMITIVE_CIVILIZED","AVENUE_PATRIOTS",15,30,"WF28-A031"),
 ("HIPPOCRATES","AVENUE_PATRIOTS_HAMILTON_CORNER",14,21,"WF28-A030"),
 ("THE_PICNIC","GARDEN_COURT",14,110,"WF28-A033")]
def schedule(provisional_height=9.,margin=0.):
    if provisional_height<=0 or margin<0:raise ValueError("invalid height/margin")
    items=[]
    for name,facade,h_ft,w_ft,source in ART:
        h,w=h_ft*FT,w_ft*FT
        items.append(dict(art_id=name,facade_key=facade,source_id=source,
          documented_artwork_height_m=round(h,4),documented_artwork_width_m=round(w,4),
          absolute_minimum_facade_height_m_if_fully_on_wall=round(h,4),
          hypothetical_height_with_margin_m=round(h+margin,4),
          fits_existing_proxy=h<=provisional_height,
          existing_proxy_height_deficit_m=round(max(0,h-provisional_height),4),
          placement_verified=False,facade_height_verified=False))
    return dict(schema="fmp.wf0028.facade_constraints.v014",
        parent_model="WF0028_1939_Architectural_References_v013",
        historical_geometry_modified=False,
        provisional_height_m=provisional_height,margin_m=margin,items=items,
        limitations=["Artwork sizes are not building sizes.",
                     "Each facade requires independently validated elevation.",
                     "Historical placement, wall top and site registration unverified."])
if __name__=="__main__":print(json.dumps(schedule(),indent=2))
