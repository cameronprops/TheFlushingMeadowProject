"""Evidence-labelled orthographic survey board from a generated registration manifest."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw(manifest_path,out):
 d=json.loads(Path(manifest_path).read_text())
 fig,ax=plt.subplots(figsize=(14.4,8.5),dpi=160)
 fig.patch.set_facecolor('#f8f7f5');ax.set_facecolor('#f8f7f5')
 colors={'PUBLIC_ENTRANCE_LOBBY_REFERENCE_ONLY':'#e5aa16','ESCALATOR_ONE_EXISTING_ENVELOPE':'#277ba8',
 'ESCALATOR_TWO_EXISTING_ENVELOPE':'#d86c37','RETURN_BRIDGE_EXISTING_DECK':'#008f79',
 'PERISPHERE_RUNTIME_LOWER_SHELL':'#746c99','TRYLON_RUNTIME_EXTERIOR_SHELL':'#5c666b'}
 names={'PUBLIC_ENTRANCE_LOBBY_REFERENCE_ONLY':'LOBBY MODEL ENVELOPE',
 'ESCALATOR_ONE_EXISTING_ENVELOPE':'ESCALATOR 1 · EXISTING PROXY',
 'ESCALATOR_TWO_EXISTING_ENVELOPE':'ESCALATOR 2 · EXISTING PROXY',
 'RETURN_BRIDGE_EXISTING_DECK':'RETURN BRIDGE · DECK PROXY ONLY',
 'PERISPHERE_RUNTIME_LOWER_SHELL':'PERISPHERE LOWER SHELL (RUNTIME)',
 'TRYLON_RUNTIME_EXTERIOR_SHELL':'TRYLON EXTERIOR SHELL (RUNTIME)'}
 for i,rec in enumerate(d['objects']):
  label=rec['label'];a=rec['bbox_min_xyz_m'];b=rec['bbox_max_xyz_m'];col=colors[label]
  ax.add_patch(Rectangle((a[0],a[1]),b[0]-a[0],b[1]-a[1],lw=2 if 'BRIDGE' in label else 1.5,linestyle='-' if 'BRIDGE' in label else '--',edgecolor=col,facecolor='none'))
  ax.plot((a[0]+b[0])/2,(a[1]+b[1])/2,marker='+',ms=7,color=col,zorder=5)
  left=37; top=47-i*6.1
  ax.text(left,top,names[label],color=col,fontsize=10,fontweight='bold',va='center')
  ax.text(left,top-2.2,f'X {a[0]:.2f}..{b[0]:.2f} m  |  Y {a[1]:.2f}..{b[1]:.2f} m',color='#464a50',fontsize=8,va='center')
  ax.annotate('',xy=((a[0]+b[0])/2,(a[1]+b[1])/2),xytext=(left-1,top),arrowprops={'arrowstyle':'-','color':col,'lw':.7,'alpha':.55})
 ax.text(-63,59,'FMP 1939  |  THEME CENTER BRIDGE & ENTRY',fontsize=17,fontweight='bold',color='#202a33')
 ax.text(-63,56,'VERIFIED MODEL-SPACE CONTROL ENVELOPES  ·  NOT A HISTORICAL SECTION',fontsize=10,color='#4e606e')
 ax.text(-62,51,'NOT YET BUILT',fontweight='bold',color='#b34b36',fontsize=10)
 ax.text(-62,48.5,'Public entrance canopy + signage',color='#b34b36',fontsize=9)
 ax.text(-62,46.1,'Enclosed escalator chamber finish',color='#b34b36',fontsize=9)
 ax.text(-62,43.7,'Historically matched bridge arch',color='#b34b36',fontsize=9)
 ax.set_xlim(-67,103);ax.set_ylim(-3,64);ax.set_aspect('equal',adjustable='box')
 ax.set_xlabel('Model X  (metres, unregistered)',fontsize=10);ax.set_ylabel('Model Y  (metres)',fontsize=10)
 ax.grid(True,alpha=.18,linestyle=':')
 fig.text(.12,.025,'Data source: source-hash-verified v005 GLB. Each rectangle is a model-local axis-aligned bounding control only. No historical curves or door shapes are inferred.',fontsize=8,color='#4d5259')
 fig.subplots_adjust(left=.07,right=.97,top=.94,bottom=.11)
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 fig.savefig(out,facecolor=fig.get_facecolor());plt.close(fig)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('out');v=p.parse_args();draw(v.manifest,v.out)
