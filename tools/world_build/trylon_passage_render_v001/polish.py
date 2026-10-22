from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
r=Path('/mnt/data/trylon_arch_render')
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(F,19);bold=ImageFont.truetype(B,24);small=ImageFont.truetype(F,16)
def polish(src,dst,kicker):
 im=Image.open(r/src).convert('RGB');d=ImageDraw.Draw(im)
 w,h=im.size
 d.rectangle([0,0,w,93],fill='#192e3b')
 d.text((42,18),'TRYLON BASE  |  EXTERIOR ELEVATION',font=bold,fill='white')
 d.text((42,51),kicker,font=small,fill='#bdd1db')
 d.rectangle([0,h-166,w,h],fill='#f8fafb')
 d.line((72,h-165,w-72,h-165),fill='#c6d2da',width=2)
 d.text((72,h-150),'MODEL GEOMETRY',font=small,fill='#243d4c')
 d.text((72,h-124),'Stone = unchanged cladding gap    Dark blue = structural framing',font=font,fill='#284555')
 d.text((72,h-92),'Green boxes = proposed 2.4 m × 2.4 m aperture envelopes; NOT actual finished doors',font=font,fill='#087b5d')
 d.text((72,h-60),'Visible members may be behind the opening in projection; collision checks are separate.',font=small,fill='#526a78')
 d.text((72,h-35),'Actual FMP_ThemeCenter_Assembled_Runtime_v005.glb  |  1939 working reconstruction',font=small,fill='#526a78')
 im.save(r/dst)
 return im
pre=polish('07_source_frame_elevation.png','10_original_trylon_elevation.png','Source frame preserved in v005, inactive for visitor rendering')
post=polish('08_current_frame_elevation.png','11_runtime_trylon_elevation.png','Active v004 shared-aperture frame in v005 runtime assembly')
a=Image.new('RGB',(2460,930),'white');a.paste(pre,(0,0));a.paste(post,(1230,0))
d=ImageDraw.Draw(a);d.rectangle((1229,0,1233,930),fill='#ffffff');a.save(r/'12_before_after_trylon_entrance.png')
